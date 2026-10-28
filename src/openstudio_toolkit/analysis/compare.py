"""Compare a model against a mapping of requested load values, by Space or Thermal Zone (item 5).

The mapping has the shape ``base_model_space_loads.py`` (r2f-simulation-os) materializes: family ->
{Space or Thermal Zone name -> absolute value}, with the dump family names ``people`` (people),
``lights`` (W) and ``electric_equipment`` (W). The same object is meant to be the input of ``apply``
(item 4), which imports it from here; compare never imports ``transforms``.

What is compared is the total OpenStudio resolves for the Space or Thermal Zone, i.e. what EnergyPlus
simulates, not what is written on the load objects (approved by Roberto, 2026-10-27). It includes
loads on the Space and on its space type (its own, or the building's when the Space has none), any
design method (absolute, per floor area, per person) and each load's multiplier. A Thermal Zone is the
sum of its Spaces, without the zone multiplier. In R2F-Office-Hub.osm the record asks 5 W of lighting
for ``0.05-Storage``: the light on the Space has 5 W, but its Storage space type adds 10.5 W, so the
row is ``differs`` with 15.5 W in the model.

Status: ``match`` within ``tolerance`` (absolute); ``differs`` otherwise; ``missing`` when the Space or
Zone does not exist, when no load of the family reaches it and a non-zero value was requested (zero
requested and nothing there is a match), or when a load that reaches it has no definition (an orphan:
the total cannot be resolved; the reference findings say why). ``difference`` is model - requested.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import pandas as pd

from openstudio_toolkit._sdk import opt, related

COMPARE_COLUMNS = ("family", "key", "field", "requested", "in_model", "difference", "status")
COMPARE_STATUS_VALUES = ("match", "differs", "missing")
SCOPES = ("space", "thermal_zone")

LoadMapping = Mapping[str, Mapping[str, float]]
"""Family -> {Space or Thermal Zone name -> requested absolute value}."""

# family -> (field label, total accessor on Space/ThermalZone, load list accessor on Space/SpaceType,
# definition reference field of the load)
_FAMILIES: dict[str, tuple[str, str, str, str]] = {
    "people": ("Number of People {people}", "numberOfPeople", "people", "People Definition Name"),
    "lights": ("Lighting Level {W}", "lightingPower", "lights", "Lights Definition Name"),
    "electric_equipment": (
        "Design Level {W}",
        "electricEquipmentPower",
        "electricEquipment",
        "Electric Equipment Definition Name",
    ),
}

COMPARE_FAMILIES = tuple(_FAMILIES)


def _loads(space: Any, accessor: str) -> list[Any]:
    """Loads of one family that reach a Space: on the Space and on its resolved space type."""
    found = list(getattr(space, accessor)())
    space_type = opt(space.spaceType())
    if space_type is not None:
        found += list(getattr(space_type, accessor)())
    return found


def compare_to_mapping(
    model: Any,
    mapping: LoadMapping,
    by: str = "space",
    tolerance: float = 1e-6,
) -> pd.DataFrame:
    """One row per requested (family, key), with the columns of ``COMPARE_COLUMNS``, in mapping order.

    ``by`` is ``"space"`` or ``"thermal_zone"``: what the keys of the mapping name. Spaces or Zones not
    in the mapping are not reported.
    """
    if by not in SCOPES:
        raise ValueError(f"by must be one of {', '.join(SCOPES)}, not {by!r}")
    unknown = sorted(name for name in mapping if name not in _FAMILIES)
    if unknown:
        raise ValueError(f"unknown families: {', '.join(unknown)} (use {', '.join(_FAMILIES)})")

    if by == "space":
        scopes = {s.nameString(): (s, [s]) for s in model.getSpaces()}
    else:
        scopes = {z.nameString(): (z, list(z.spaces())) for z in model.getThermalZones()}

    rows: list[tuple[Any, ...]] = []
    for family, requested_by_key in mapping.items():
        label, total, accessor, definition_field = _FAMILIES[family]
        for key, requested in requested_by_key.items():
            scope = scopes.get(key)
            found = [load for space in scope[1] for load in _loads(space, accessor)] if scope else []
            orphan = any(related(load, definition_field) is None for load in found)
            if scope is None or orphan or (not found and abs(requested) > tolerance):
                rows.append((family, key, label, requested, None, None, "missing"))
                continue
            in_model = float(getattr(scope[0], total)()) if found else 0.0
            difference = in_model - requested
            status = "match" if abs(difference) <= tolerance else "differs"
            rows.append((family, key, label, requested, in_model, difference, status))

    return pd.DataFrame(rows, columns=list(COMPARE_COLUMNS))
