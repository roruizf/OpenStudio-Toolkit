"""Apply a mapping of requested per-Space loads to a model (item 4).

Adopts the contract of ``base_model_space_loads.py`` (r2f-simulation-os, ``materialize_space_loads``):
the mapping is family -> {Space name -> absolute value}, the same ``LoadMapping`` that
``analysis.compare`` checks, so after a successful apply ``compare_to_mapping`` on the output reports
every row as ``match``. Kept from that contract: the input model is never modified (the result is saved
to another file); everything is validated before the model is touched; a Space that does not exist is
an error; a requested 0 creates no load (zero-object rule); a Space that already has a load of the
family is refused; the EnergyPlus forward translator runs before saving.

Changes approved by Roberto (2026-10-28, "ok 4"), with the evidence in ``v0.3-evidence/apply_proto.py``:

- ``existing="update"`` (opt-in): when the Space already has exactly one load of the family, with
  multiplier 1 and a definition no other load uses, only the definition's value is set (as an absolute
  value). Fractions, schedule, names and handles stay. On Office Hub actual-017 with the G3.7 lighting
  mapping, the diff is 36 rows, ``Lighting Level`` only; deleting and recreating the loads lost the
  definition fractions (144 rows). Anything else (two loads, a shared definition, a multiplier, a
  requested 0) is refused.
- A Space that receives a load of the family from its space type (its own, else the building's) is
  always refused: a space type is shared, so a load added on the Space would be summed to it (on
  reference-011 the r2f check passes and the lighting doubles, 15,570.39 W instead of 7,784.85 W).
- Keys are Space names only; values are plain numbers (no definition-level fractions).
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import openstudio

from openstudio_toolkit._sdk import opt, related
from openstudio_toolkit.analysis.compare import LoadMapping

EXISTING_MODES = ("refuse", "update")
_ZERO = 1e-9


@dataclass(frozen=True)
class _Family:
    loads: str  # load list accessor on Space and SpaceType
    definition_field: str  # definition reference field of the load
    make_definition: Callable[[Any], Any]
    make_load: Callable[[Any], Any]
    to_definition: str  # cast of the load's definition
    set_value: str  # absolute-value setter on the definition
    label: str  # name suffix of the created objects


_FAMILIES: dict[str, _Family] = {
    "people": _Family(
        "people", "People Definition Name", openstudio.model.PeopleDefinition, openstudio.model.People,
        "to_PeopleDefinition", "setNumberofPeople", "People",
    ),
    "lights": _Family(
        "lights", "Lights Definition Name", openstudio.model.LightsDefinition, openstudio.model.Lights,
        "to_LightsDefinition", "setLightingLevel", "Lights",
    ),
    "electric_equipment": _Family(
        "electricEquipment", "Electric Equipment Definition Name", openstudio.model.ElectricEquipmentDefinition,
        openstudio.model.ElectricEquipment, "to_ElectricEquipmentDefinition", "setDesignLevel",
        "Electric Equipment",
    ),
}


@dataclass(frozen=True)
class ApplyResult:
    """What apply did for one family."""

    family: str
    spaces_created: int
    spaces_updated: int
    spaces_skipped_zero: int
    total_value: float


class ApplyError(RuntimeError):
    """The model and the mapping disagree in a way apply refuses to guess past; nothing was written.

    ``problems`` lists every refusal found, one line each (all families, all Spaces).
    """

    def __init__(self, problems: list[str]) -> None:
        super().__init__("apply refused:\n" + "\n".join(f"- {p}" for p in problems))
        self.problems = problems


def _load_model(path: Path) -> Any:
    model = opt(openstudio.osversion.VersionTranslator().loadModel(openstudio.path(str(path))))
    if model is None:
        raise ValueError(f"OSM failed to load: {path}")
    return model


def _plan(model: Any, mapping: LoadMapping, existing: str) -> tuple[list[tuple[str, str, Any, float, Any]], list[str]]:
    """(family, Space name, Space, value, load to update or None) for every entry, and the refusals."""
    spaces = {s.nameString(): s for s in model.getSpaces()}
    plan: list[tuple[str, str, Any, float, Any]] = []
    problems: list[str] = []
    for family, values in mapping.items():
        config = _FAMILIES[family]
        for name, value in values.items():
            space = spaces.get(name)
            if space is None:
                problems.append(f"[{family}] Space {name!r} is not in the model")
                continue
            space_type = opt(space.spaceType())
            inherited = list(getattr(space_type, config.loads)()) if space_type is not None else []
            if inherited:
                problems.append(
                    f"[{family}] Space {name!r} receives {len(inherited)} load(s) from space type "
                    f"{space_type.nameString()!r} (shared by every Space of that type): "
                    "a load on the Space would be added to it"
                )
                continue
            own = list(getattr(space, config.loads)())
            if not own:
                plan.append((family, name, space, float(value), None))
                continue
            if existing == "refuse":
                problems.append(
                    f"[{family}] Space {name!r} already has {len(own)} load(s) "
                    f"({', '.join(x.nameString() for x in own)}); "
                    'decide whether to replace them, or pass existing="update"'
                )
                continue
            reason = _not_updatable(own, config, float(value))
            if reason:
                problems.append(f"[{family}] Space {name!r}: {reason}")
                continue
            plan.append((family, name, space, float(value), own[0]))
    return plan, problems


def _not_updatable(own: list[Any], config: _Family, value: float) -> str | None:
    if len(own) > 1:
        return f"{len(own)} loads ({', '.join(x.nameString() for x in own)}); update needs exactly one"
    load = own[0]
    if abs(value) < _ZERO:
        return f"0 requested and {load.nameString()!r} exists; remove it explicitly (zero-object rule)"
    if related(load, config.definition_field) is None:
        return f"{load.nameString()!r} has no definition (orphan)"
    if load.multiplier() != 1:
        return f"{load.nameString()!r} has multiplier {load.multiplier()}"
    definition = load.definition()
    users = len(definition.instances())
    if users > 1:
        return f"definition {definition.nameString()!r} is shared by {users} loads"
    return None


def apply_mapping(
    model_input: str | Path,
    model_output: str | Path,
    mapping: LoadMapping,
    *,
    existing: str = "refuse",
) -> tuple[ApplyResult, ...]:
    """Write ``model_output``: ``model_input`` with the per-Space loads of ``mapping``.

    ``mapping`` is family (``people``, ``lights``, ``electric_equipment``) -> {Space name -> absolute
    value (people, W)}. ``existing`` says what to do with a Space that already has a load of the family:
    ``"refuse"`` (default) or ``"update"`` (see the module docstring). Returns one result per family, in
    mapping order.

    Raises:
        ValueError: bad arguments (unknown family or mode, empty mapping, output equal to input).
        ApplyError: refusals found while validating; the output is not written.
    """
    source, target = Path(model_input), Path(model_output)
    if existing not in EXISTING_MODES:
        raise ValueError(f"existing must be one of {', '.join(EXISTING_MODES)}, not {existing!r}")
    unknown = sorted(name for name in mapping if name not in _FAMILIES)
    if unknown:
        raise ValueError(f"unknown families: {', '.join(unknown)} (use {', '.join(_FAMILIES)})")
    if not any(mapping.values()):
        raise ValueError("the mapping requests nothing")
    if source.resolve() == target.resolve():
        raise ValueError("model_output must differ from model_input: the input model is never modified")

    model = _load_model(source)
    plan, problems = _plan(model, mapping, existing)
    if problems:
        raise ApplyError(problems)

    counts = {family: [0, 0, 0, 0.0] for family in mapping}
    for family, name, space, value, load in plan:
        config, count = _FAMILIES[family], counts[family]
        if load is not None:
            definition = opt(getattr(load.definition(), config.to_definition)())
            getattr(definition, config.set_value)(value)
            count[1] += 1
        elif abs(value) < _ZERO:
            count[2] += 1
            continue
        else:
            definition = config.make_definition(model)
            definition.setName(f"{name} {config.label} Definition")
            getattr(definition, config.set_value)(value)
            new = config.make_load(definition)
            new.setName(f"{name} {config.label}")
            new.setSpace(space)
            count[0] += 1
        count[3] += value

    openstudio.energyplus.ForwardTranslator().translateModel(model)
    if not model.save(openstudio.path(str(target)), True):
        raise OSError(f"could not save {target}")
    return tuple(ApplyResult(f, int(c[0]), int(c[1]), int(c[2]), float(c[3])) for f, c in counts.items())
