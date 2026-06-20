"""Canonical read-only records for the OpenStudio model inventory."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from openstudio_toolkit.runtime import RuntimeInfo

SCHEMA_VERSION: Literal["0.1.0"] = "0.1.0"
CoordinateSystem = Literal["space_local", "model"]


def osm_field(
    default: Any = ...,
    *,
    osm_label: str,
    sdk_accessor: str,
    legacy_key: str | None = None,
    lineage_note: str | None = None,
) -> Any:
    """Declare OpenStudio lineage without changing the canonical field name."""
    metadata: dict[str, Any] = {
        "osm_label": osm_label,
        "sdk_accessor": sdk_accessor,
        "legacy_key": legacy_key,
        "lineage_note": lineage_note,
    }
    schema_extra: dict[str, Any] = {"openstudio": metadata}
    return Field(default, json_schema_extra=schema_extra)


def _sorted_handles(handles: list[str]) -> list[str]:
    return sorted(handles)


def _record_sort_key(record: Any) -> tuple[str, str]:
    return ((record.name or "").casefold(), record.handle)


class InventoryRecord(BaseModel):
    """Strict top-level-frozen base for build-once inventory records."""

    # Pydantic freezing is shallow: nested collections remain mutable by design in 0.1.x.
    model_config = ConfigDict(extra="forbid", frozen=True)


class SourceIdentityRecord(InventoryRecord):
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    size_bytes: int = Field(ge=0)


class SourceRecord(SourceIdentityRecord):
    path: str
    filename: str


class RuntimeRecord(InventoryRecord):
    python_version: str
    python_executable: str
    openstudio_version: str
    energyplus_version: str
    openstudio_module_path: str

    @classmethod
    def from_runtime_info(cls, runtime: RuntimeInfo) -> RuntimeRecord:
        return cls.model_validate(runtime.to_dict())


class BuildingRecord(InventoryRecord):
    handle: str = osm_field(osm_label="Handle", sdk_accessor="Building.handle()", legacy_key="Handle")
    name: str | None = osm_field(osm_label="Name", sdk_accessor="Building.name()", legacy_key="Name")
    north_axis_deg: float = osm_field(
        osm_label="North Axis {deg}", sdk_accessor="Building.northAxis()", legacy_key="North Axis {deg}"
    )
    floor_area_m2: float = osm_field(
        osm_label="Floor Area {m2}",
        sdk_accessor="Building.floorArea()",
        lineage_note="Derived by the SDK; not a direct OS:Building text field.",
    )
    conditioned_floor_area_m2: float | None = osm_field(
        osm_label="Conditioned Floor Area {m2}",
        sdk_accessor="Building.conditionedFloorArea()",
        lineage_note="Derived optional SDK value; not a direct OS:Building text field.",
    )


class StoryRecord(InventoryRecord):
    handle: str = osm_field(osm_label="Handle", sdk_accessor="BuildingStory.handle()", legacy_key="Handle")
    name: str | None = osm_field(osm_label="Name", sdk_accessor="BuildingStory.name()", legacy_key="Name")
    nominal_z_m: float | None = osm_field(
        osm_label="Nominal Z Coordinate {m}",
        sdk_accessor="BuildingStory.nominalZCoordinate()",
        legacy_key="Nominal Z Coordinate {m}",
    )
    nominal_floor_to_floor_height_m: float | None = osm_field(
        osm_label="Nominal Floor to Floor Height {m}",
        sdk_accessor="BuildingStory.nominalFloortoFloorHeight()",
        legacy_key="Nominal Floor to Floor Height {m}",
    )
    nominal_floor_to_ceiling_height_m: float | None = osm_field(
        osm_label="Nominal Floor to Ceiling Height {m}",
        sdk_accessor="BuildingStory.nominalFloortoCeilingHeight()",
        legacy_key="Nominal Floor to Ceiling Height {m}",
    )
    space_handles: list[str] = Field(default_factory=list)

    _sort_space_handles = field_validator("space_handles")(_sorted_handles)


class SpaceRecord(InventoryRecord):
    handle: str = osm_field(osm_label="Handle", sdk_accessor="Space.handle()", legacy_key="Handle")
    name: str | None = osm_field(osm_label="Name", sdk_accessor="Space.name()", legacy_key="Name")
    story_handle: str | None = osm_field(
        osm_label="Building Story Name",
        sdk_accessor="Space.buildingStory().handle()",
        lineage_note="The OSM text stores a handle even though the IDD label says Name.",
    )
    story_name: str | None = osm_field(
        osm_label="Building Story Name",
        sdk_accessor="Space.buildingStory().name()",
        legacy_key="Building Story Name",
        lineage_note="Resolved human label derived from the OSM reference.",
    )
    thermal_zone_handle: str | None = osm_field(
        osm_label="Thermal Zone Name",
        sdk_accessor="Space.thermalZone().handle()",
        lineage_note="The OSM text stores a handle even though the IDD label says Name.",
    )
    thermal_zone_name: str | None = osm_field(
        osm_label="Thermal Zone Name",
        sdk_accessor="Space.thermalZone().name()",
        legacy_key="Thermal Zone Name",
        lineage_note="Resolved human label derived from the OSM reference.",
    )
    space_type_handle: str | None = osm_field(
        osm_label="Space Type Name",
        sdk_accessor="Space.spaceType().handle()",
        lineage_note="The OSM text stores a handle even though the IDD label says Name.",
    )
    space_type_name: str | None = osm_field(
        osm_label="Space Type Name",
        sdk_accessor="Space.spaceType().name()",
        legacy_key="Space Type Name",
        lineage_note="Resolved human label derived from the OSM reference.",
    )
    part_of_total_floor_area: bool = osm_field(
        osm_label="Part of Total Floor Area",
        sdk_accessor="Space.partofTotalFloorArea()",
        legacy_key="Part of Total Floor Area",
    )
    floor_area_m2: float = osm_field(
        osm_label="Floor Area {m2}", sdk_accessor="Space.floorArea()", legacy_key="Floor Area {m2}"
    )
    volume_m3: float = osm_field(osm_label="Volume {m3}", sdk_accessor="Space.volume()", legacy_key="Volume {m3}")
    x_origin_m: float = osm_field(osm_label="X Origin {m}", sdk_accessor="Space.xOrigin()", legacy_key="X Origin {m}")
    y_origin_m: float = osm_field(osm_label="Y Origin {m}", sdk_accessor="Space.yOrigin()", legacy_key="Y Origin {m}")
    z_origin_m: float = osm_field(osm_label="Z Origin {m}", sdk_accessor="Space.zOrigin()", legacy_key="Z Origin {m}")
    direction_of_relative_north_deg: float = osm_field(
        osm_label="Direction of Relative North {deg}",
        sdk_accessor="Space.directionofRelativeNorth()",
        legacy_key="Direction of Relative North {deg}",
    )
    surface_handles: list[str] = Field(default_factory=list)

    _sort_surface_handles = field_validator("surface_handles")(_sorted_handles)


class ThermalZoneRecord(InventoryRecord):
    handle: str = osm_field(osm_label="Handle", sdk_accessor="ThermalZone.handle()", legacy_key="Handle")
    name: str | None = osm_field(osm_label="Name", sdk_accessor="ThermalZone.name()", legacy_key="Name")
    multiplier: int = osm_field(
        osm_label="Multiplier", sdk_accessor="ThermalZone.multiplier()", legacy_key="Multiplier"
    )
    space_handles: list[str] = Field(default_factory=list)

    _sort_space_handles = field_validator("space_handles")(_sorted_handles)


class Point3D(InventoryRecord):
    x_m: float
    y_m: float
    z_m: float


class SurfaceRecord(InventoryRecord):
    handle: str = osm_field(osm_label="Handle", sdk_accessor="Surface.handle()", legacy_key="Handle")
    name: str | None = osm_field(osm_label="Name", sdk_accessor="Surface.name()", legacy_key="Name")
    space_handle: str | None = osm_field(
        osm_label="Space Name",
        sdk_accessor="Surface.space().handle()",
        lineage_note="The OSM text stores a handle even though the IDD label says Name.",
    )
    space_name: str | None = osm_field(
        osm_label="Space Name",
        sdk_accessor="Surface.space().name()",
        legacy_key="Space Name",
        lineage_note="Resolved human label derived from the OSM reference.",
    )
    surface_type: str = osm_field(
        osm_label="Surface Type", sdk_accessor="Surface.surfaceType()", legacy_key="Surface Type"
    )
    outside_boundary_condition: str = osm_field(
        osm_label="Outside Boundary Condition",
        sdk_accessor="Surface.outsideBoundaryCondition()",
        legacy_key="Outside Boundary Condition",
    )
    adjacent_surface_handle: str | None = osm_field(
        osm_label="Outside Boundary Condition Object",
        sdk_accessor="Surface.adjacentSurface().handle()",
        lineage_note="Canonical relationship uses a handle; legacy output resolves a name.",
    )
    construction_handle: str | None = osm_field(
        osm_label="Construction Name",
        sdk_accessor="Surface.construction().handle()",
        lineage_note="The OSM text stores a handle even though the IDD label says Name.",
    )
    construction_name: str | None = osm_field(
        osm_label="Construction Name",
        sdk_accessor="Surface.construction().name()",
        legacy_key="Construction Name",
        lineage_note="Resolved human label derived from the OSM reference.",
    )
    sun_exposure: str = osm_field(
        osm_label="Sun Exposure", sdk_accessor="Surface.sunExposure()", legacy_key="Sun Exposure"
    )
    wind_exposure: str = osm_field(
        osm_label="Wind Exposure", sdk_accessor="Surface.windExposure()", legacy_key="Wind Exposure"
    )
    gross_area_m2: float = osm_field(
        osm_label="Gross Area {m2}", sdk_accessor="Surface.grossArea()", lineage_note="Derived SDK geometry value."
    )
    net_area_m2: float = osm_field(
        osm_label="Net Area {m2}", sdk_accessor="Surface.netArea()", lineage_note="Derived SDK geometry value."
    )
    coordinate_system: CoordinateSystem
    vertices: list[Point3D] = Field(default_factory=list)
    subsurface_handles: list[str] = Field(default_factory=list)

    _sort_subsurface_handles = field_validator("subsurface_handles")(_sorted_handles)


class SubSurfaceRecord(InventoryRecord):
    handle: str = osm_field(osm_label="Handle", sdk_accessor="SubSurface.handle()", legacy_key="Handle")
    name: str | None = osm_field(osm_label="Name", sdk_accessor="SubSurface.name()", legacy_key="Name")
    surface_handle: str | None = osm_field(
        osm_label="Surface Name",
        sdk_accessor="SubSurface.surface().handle()",
        lineage_note="The OSM text stores a handle even though the IDD label says Name.",
    )
    surface_name: str | None = osm_field(
        osm_label="Surface Name",
        sdk_accessor="SubSurface.surface().name()",
        legacy_key="Surface Name",
        lineage_note="Resolved human label derived from the OSM reference.",
    )
    subsurface_type: str = osm_field(
        osm_label="Sub Surface Type",
        sdk_accessor="SubSurface.subSurfaceType()",
        legacy_key="Sub Surface Type",
    )
    construction_handle: str | None = osm_field(
        osm_label="Construction Name",
        sdk_accessor="SubSurface.construction().handle()",
        lineage_note="The OSM text stores a handle even though the IDD label says Name.",
    )
    construction_name: str | None = osm_field(
        osm_label="Construction Name",
        sdk_accessor="SubSurface.construction().name()",
        legacy_key="Construction Name",
        lineage_note="Resolved human label derived from the OSM reference.",
    )
    multiplier: float = osm_field(
        osm_label="Multiplier", sdk_accessor="SubSurface.multiplier()", legacy_key="Multiplier"
    )
    gross_area_m2: float = osm_field(
        osm_label="Gross Area {m2}", sdk_accessor="SubSurface.grossArea()", lineage_note="Derived SDK geometry value."
    )
    net_area_m2: float = osm_field(
        osm_label="Net Area {m2}", sdk_accessor="SubSurface.netArea()", lineage_note="Derived SDK geometry value."
    )
    coordinate_system: CoordinateSystem
    vertices: list[Point3D] = Field(default_factory=list)


class ModelCounts(InventoryRecord):
    stories: int = Field(ge=0)
    spaces: int = Field(ge=0)
    thermal_zones: int = Field(ge=0)
    surfaces: int = Field(ge=0)
    subsurfaces: int = Field(ge=0)


class ModelInventory(InventoryRecord):
    schema_version: Literal["0.1.0"] = SCHEMA_VERSION
    source: SourceIdentityRecord
    building: BuildingRecord
    counts: ModelCounts
    stories: list[StoryRecord] = Field(default_factory=list)
    spaces: list[SpaceRecord] = Field(default_factory=list)
    thermal_zones: list[ThermalZoneRecord] = Field(default_factory=list)
    surfaces: list[SurfaceRecord] = Field(default_factory=list)
    subsurfaces: list[SubSurfaceRecord] = Field(default_factory=list)

    @field_validator("stories", "spaces", "thermal_zones", "surfaces", "subsurfaces")
    @classmethod
    def sort_records(cls, records: list[Any]) -> list[Any]:
        # Normalization occurs at construction; callers must not mutate records before serialization.
        return sorted(records, key=_record_sort_key)

    @model_validator(mode="after")
    def counts_match_collections(self) -> ModelInventory:
        observed = ModelCounts(
            stories=len(self.stories),
            spaces=len(self.spaces),
            thermal_zones=len(self.thermal_zones),
            surfaces=len(self.surfaces),
            subsurfaces=len(self.subsurfaces),
        )
        if self.counts != observed:
            raise ValueError(f"Inventory counts do not match collections: expected {observed.model_dump()}")
        return self


class InventoryRun(InventoryRecord):
    """Provenance envelope excluded from the canonical semantic hash."""

    source: SourceRecord
    runtime: RuntimeRecord
    inventory: ModelInventory

    @model_validator(mode="after")
    def source_identity_matches_inventory(self) -> InventoryRun:
        if (
            self.source.sha256 != self.inventory.source.sha256
            or self.source.size_bytes != self.inventory.source.size_bytes
        ):
            raise ValueError("Run source identity does not match the inventory source identity")
        return self


@dataclass(frozen=True, slots=True)
class InventoryArtifact:
    content: bytes
    sha256: str


def serialize_inventory(inventory: ModelInventory) -> InventoryArtifact:
    """Serialize an inventory to stable UTF-8 JSON and hash those exact bytes."""
    content = json.dumps(
        inventory.model_dump(mode="json"),
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return InventoryArtifact(content=content, sha256=hashlib.sha256(content).hexdigest())
