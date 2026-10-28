"""Where a model object sits in the building: Space, Thermal Zone and System (visible report only).

Approved by Roberto (2026-10-27, item 7 B): every row of the report gets three columns, Space,
Thermal Zone and System (air loop, plant loop or VRF outdoor unit), and the report is split by
building part. These columns are not part of the contract's artifact schema.

Rules, from the location prototype (``v0.3-evidence/locate_proto.py``) and its two faults fixed:

- A Space, Thermal Zone or System is its own location; a Space also gives its Thermal Zone, a space
  type gives the Spaces whose resolved space type it is (own, else the building's).
- An object is placed by what it points to (a light -> its Space, a sub surface -> its surface -> its
  Space, a ``Sizing:Zone`` -> its zone), by the loop it is a component of (OpenStudio's own loop
  component lists, also through the node a setpoint manager controls), and by the lists that hold it
  (``ZoneHVAC:EquipmentList`` -> zone, ``ZoneTerminalUnitList`` -> VRF outdoor unit). All of these are
  kept: an air terminal gets its Thermal Zone and its air loop.
- An object placed by none of these takes the locations of everything that uses it. A schedule,
  construction or curve used in several places has several entries in a column, which the report
  shows as "shared (used by N)" with the list.
- ``AdditionalProperties``, ``StandardsInformation`` and ``Schedule:Rule`` objects sit where their owner
  (the first object they point to) sits.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

from openstudio_toolkit.extractors.generic import ObjectRecord

SPACE, ZONE, SPACE_TYPE, BUILDING = "OS:Space", "OS:ThermalZone", "OS:SpaceType", "OS:Building"
SYSTEM_TYPES = frozenset({"OS:AirLoopHVAC", "OS:PlantLoop", "OS:AirConditioner:VariableRefrigerantFlow"})
TOPOLOGY_TYPES = frozenset({"OS:Connection", "OS:Node", "OS:PortList"})
# Lists hold their members: whatever a list belongs to, its members belong to too.
LIST_TYPES = frozenset(
    {
        "OS:ZoneHVAC:EquipmentList",
        "OS:ZoneTerminalUnitList",
        "OS:ModelObjectList",
        "OS:AvailabilityManagerAssignmentList",
    }
)
OWNED_TYPES = frozenset(
    {
        "OS:AdditionalProperties",
        "OS:StandardsInformation:Construction",
        "OS:StandardsInformation:Material",
        "OS:Schedule:Rule",
    }
)
_FORWARD_DEPTH = 3


@dataclass(frozen=True)
class Location:
    """Names of the Spaces, Thermal Zones and Systems an object belongs to (empty when unplaced)."""

    spaces: tuple[str, ...] = ()
    zones: tuple[str, ...] = ()
    systems: tuple[str, ...] = ()
    system_types: tuple[str, ...] = ()

    def __bool__(self) -> bool:
        return bool(self.spaces or self.zones or self.systems)


@dataclass
class _Found:
    spaces: set[str] = field(default_factory=set)
    zones: set[str] = field(default_factory=set)
    systems: set[str] = field(default_factory=set)

    def __bool__(self) -> bool:
        return bool(self.spaces or self.zones or self.systems)

    def add(self, other: _Found) -> None:
        self.spaces |= other.spaces
        self.zones |= other.zones
        self.systems |= other.systems


class Locator:
    """Locations of the objects of one model, by handle."""

    def __init__(self, model: Any, records: list[ObjectRecord]) -> None:
        self.records = {r.handle: r for r in records}
        self._sources: dict[str, list[str]] = defaultdict(list)
        for r in records:
            for f in r.fields:
                if f.target is not None and f.target in self.records:
                    self._sources[f.target].append(r.handle)
        self._space_zone = {
            h: self._target(r, "Thermal Zone Name") for h, r in self.records.items() if r.idd_type == SPACE
        }
        building_type = next((self._target(r, "Space Type Name") for r in records if r.idd_type == BUILDING), None)
        self._spaces_by_type: dict[str, set[str]] = defaultdict(set)
        for h, r in self.records.items():
            if r.idd_type == SPACE:
                resolved = self._target(r, "Space Type Name") or building_type
                if resolved is not None:
                    self._spaces_by_type[resolved].add(h)
        # OpenStudio's own loop component lists (vectors, nothing dereferenced through a field).
        self._loops: dict[str, set[str]] = defaultdict(set)
        for loop in [*model.getAirLoopHVACs(), *model.getPlantLoops()]:
            members = list(loop.components())
            if hasattr(loop, "oaComponents"):
                members += list(loop.oaComponents())
            for member in members:
                self._loops[str(member.handle())].add(str(loop.handle()))
        self._memo: dict[str, _Found] = {}

    @staticmethod
    def _target(record: ObjectRecord, field_name: str) -> str | None:
        return next((f.target for f in record.fields if f.name == field_name), None)

    def _type(self, handle: str) -> str:
        return self.records[handle].idd_type

    def _name(self, handle: str) -> str:
        return self.records[handle].name or handle

    def _base(self, handle: str) -> _Found | None:
        """Location of a Space, Thermal Zone, System or space type; None for any other object."""
        kind = self._type(handle)
        if kind == SPACE:
            zone = self._space_zone.get(handle)
            return _Found({handle}, {zone} if zone else set())
        if kind == ZONE:
            return _Found(zones={handle})
        if kind in SYSTEM_TYPES:
            return _Found(systems={handle})
        if kind == SPACE_TYPE:
            found = _Found()
            for space in self._spaces_by_type.get(handle, ()):
                found.add(self._base(space))  # type: ignore[arg-type]
            return found
        return None

    def _targets(self, handle: str) -> list[str]:
        return [f.target for f in self.records[handle].fields if f.target is not None and f.target in self.records]

    def _forward(self, handle: str) -> _Found:
        """Bases reached by following references, nearest depth only, never through topology or lists."""
        seen, frontier = {handle}, [handle]
        for _ in range(_FORWARD_DEPTH):
            found, following = _Found(), []
            for current in frontier:
                for target in self._targets(current):
                    if target in seen:
                        continue
                    seen.add(target)
                    base = self._base(target)
                    if base is not None:
                        found.add(base)
                    elif self._type(target) not in TOPOLOGY_TYPES | LIST_TYPES:
                        following.append(target)
            if found:
                return found
            frontier = following
        return _Found()

    def _loop(self, handle: str) -> _Found:
        """Loops the object is a component of, directly or through a node it points to."""
        loops = set(self._loops.get(handle, ()))
        for target in self._targets(handle):
            if self._type(target) == "OS:Node":
                loops |= self._loops.get(target, set())
        return _Found(systems=loops)

    def _locate(self, handle: str) -> _Found:
        if handle in self._memo:
            return self._memo[handle]
        self._memo[handle] = _Found()  # cycle guard: an object in progress adds nothing
        base = self._base(handle)
        if base is not None:
            self._memo[handle] = base
            return base
        kind = self._type(handle)
        if kind in OWNED_TYPES:
            owner = self._owner(handle)
            found = self._locate(owner) if owner is not None else _Found()
            self._memo[handle] = found
            return found
        found = self._forward(handle)
        found.add(self._loop(handle))
        # Parts of an object (its rules, properties, standards information) point to it but do not use it.
        users = [
            s
            for s in self._sources.get(handle, ())
            if self._type(s) not in TOPOLOGY_TYPES and not (self._type(s) in OWNED_TYPES and self._owner(s) == handle)
        ]
        lists = [s for s in users if self._type(s) in LIST_TYPES]
        others = [s for s in users if self._type(s) not in LIST_TYPES]
        for each in lists:
            found.add(self._locate(each))
        # Placed by nothing of its own: it sits where its users sit. A single user that is not a Space
        # level object also owns it (a coil inside a unitary system or a VRF terminal).
        if not found or (not found.spaces and len(others) == 1):
            for each in others:
                found.add(self._locate(each))
        self._memo[handle] = found
        return found

    def locate(self, handle: str) -> Location:
        found = self._locate(handle)
        return Location(
            spaces=tuple(sorted(self._name(h) for h in found.spaces)),
            zones=tuple(sorted(self._name(h) for h in found.zones)),
            systems=tuple(sorted(self._name(h) for h in found.systems)),
            system_types=tuple(sorted({self._type(h) for h in found.systems})),
        )

    def _owner(self, handle: str) -> str | None:
        """Owner of an ``OWNED_TYPES`` object: the first object it points to."""
        return next(iter(self._targets(handle)), None)

    def owner_type(self, handle: str) -> str | None:
        """IDD type of the owner of an ``OWNED_TYPES`` object."""
        owner = self._owner(handle)
        return self._type(owner) if owner is not None else None
