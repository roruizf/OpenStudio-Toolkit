"""Verification artifact (item 7): compare rows and diff rows with the contract's fixed schema.

``compare_rows`` is the comparison of the model against the mapping (item 5). ``diff_rows`` is the
parent -> child diff (item 6) crossed with the same mapping: a row that nobody asked for becomes
``not_requested`` (meaning confirmed by Roberto: a change between parent and child that nobody asked
for in the mapping).

Rule (approved by Roberto, 2026-10-27): a diff row is requested when its object is a load
(``people``, ``lights``, ``electric_equipment``) or the definition of one, of a family present in the
mapping, and that load reaches a Space or Thermal Zone named in the mapping for that family. A load
reaches the Spaces it hangs on: its Space, or every Space whose space type (own, or the building's when
the Space has none) is the load's space type. A definition reaches what its loads reach. A changed row
counts what the object reaches in the parent or in the child (a light moved from one Space to another
touches both); a removed row, in the parent; an added row, in the child. Every other row is
``not_requested``, including added and removed objects; their direction stays in ``field``
(``(object added)`` / ``(object removed)``), since such rows have no field of their own.

FPM4 Baseline v9 -> v10 with a lighting mapping: the 21 diff rows (outdoor air on the n01 spaces, fan
efficiencies, pump and tower power) are all ``not_requested``.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import pandas as pd

from openstudio_toolkit._sdk import opt
from openstudio_toolkit.analysis.compare import (
    COMPARE_COLUMNS,
    COMPARE_STATUS_VALUES,
    SCOPES,
    LoadMapping,
    compare_to_mapping,
)
from openstudio_toolkit.analysis.diff import DIFF_COLUMNS, DIFF_MATCH_METHODS, diff_models

__all__ = [
    "COMPARE_COLUMNS",
    "COMPARE_STATUS_VALUES",
    "DIFF_COLUMNS",
    "DIFF_MATCH_METHODS",
    "DIFF_STATUS_VALUES",
    "compare_rows",
    "diff_rows",
]

DIFF_STATUS_VALUES = ("changed", "added", "removed", "not_requested")

# diff family -> (mapping family, model getter of its objects, whether the objects are definitions)
_LOAD_FAMILIES: dict[str, tuple[str, str, bool]] = {
    "people": ("people", "getPeoples", False),
    "people_definition": ("people", "getPeopleDefinitions", True),
    "lights": ("lights", "getLightss", False),
    "lights_definition": ("lights", "getLightsDefinitions", True),
    "electric_equipment": ("electric_equipment", "getElectricEquipments", False),
    "electric_equipment_definition": ("electric_equipment", "getElectricEquipmentDefinitions", True),
}

_DIRECTION = {"added": "(object added)", "removed": "(object removed)"}


def compare_rows(model: Any, mapping: LoadMapping, by: str = "space", tolerance: float = 1e-6) -> pd.DataFrame:
    """Rows of the compare artifact: ``compare_to_mapping`` with the contract's columns."""
    return compare_to_mapping(model, mapping, by=by, tolerance=tolerance)[list(COMPARE_COLUMNS)]


class _Reach:
    """Names of the Spaces or Thermal Zones each load object of one model reaches, by (family, name)."""

    def __init__(self, model: Any, by: str) -> None:
        self._model = model
        self._by = by
        self._cache: dict[str, dict[str, set[str]]] = {}
        self._scope_by_type: dict[str, set[str]] | None = None

    def _scope(self, space: Any) -> str | None:
        if self._by == "space":
            return str(space.nameString())
        zone = opt(space.thermalZone())
        return str(zone.nameString()) if zone is not None else None

    def _load(self, load: Any) -> set[str]:
        space = opt(load.space())
        if space is not None:
            scope = self._scope(space)
            return {scope} if scope is not None else set()
        space_type = opt(load.spaceType())
        if space_type is None:
            return set()
        if self._scope_by_type is None:
            self._scope_by_type = {}
            for each in self._model.getSpaces():
                resolved, scope = opt(each.spaceType()), self._scope(each)
                if resolved is not None and scope is not None:
                    self._scope_by_type.setdefault(str(resolved.handle()), set()).add(scope)
        return self._scope_by_type.get(str(space_type.handle()), set())

    def __call__(self, family: str, name: str) -> set[str]:
        if family not in self._cache:
            _, getter, is_definition = _LOAD_FAMILIES[family]
            by_name: dict[str, set[str]] = {}
            for obj in getattr(self._model, getter)():
                loads = obj.instances() if is_definition else [obj]
                by_name[str(obj.nameString())] = set().union(*(self._load(load) for load in loads))
            self._cache[family] = by_name
        return self._cache[family].get(name, set())


def diff_rows(
    parent: Any,
    child: Any,
    mapping: LoadMapping,
    by: str = "space",
    families: Iterable[str] | None = None,
    include_topology: bool = False,
) -> pd.DataFrame:
    """Rows of the diff artifact: ``diff_models`` with ``not_requested`` assigned against ``mapping``.

    ``families`` and ``include_topology`` are passed to ``diff_models``; ``by`` says what the mapping's
    keys name, as in ``compare_to_mapping``.
    """
    if by not in SCOPES:
        raise ValueError(f"by must be one of {', '.join(SCOPES)}, not {by!r}")
    df = diff_models(parent, child, families=families, include_topology=include_topology)
    reach = {"parent": _Reach(parent, by), "child": _Reach(child, by)}

    def requested(row: Any) -> bool:
        load = _LOAD_FAMILIES.get(row.family)
        if load is None or load[0] not in mapping:
            return False
        sides = {"changed": ("parent", "child"), "removed": ("parent",), "added": ("child",)}[row.status]
        touched = set().union(*(reach[side](row.family, row.key) for side in sides))
        return not touched.isdisjoint(mapping[load[0]])

    statuses, fields = [], []
    for row in df.itertuples(index=False):
        if requested(row):
            statuses.append(row.status)
            fields.append(row.field)
        else:
            statuses.append("not_requested")
            fields.append(_DIRECTION.get(row.status, row.field))
    df["status"] = statuses
    df["field"] = fields
    return df[list(DIFF_COLUMNS)]
