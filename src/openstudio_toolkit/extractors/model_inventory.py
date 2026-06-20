"""Read-only linear extraction of the canonical OpenStudio model inventory."""

from __future__ import annotations

import hashlib
from collections import defaultdict
from pathlib import Path
from typing import Any

import openstudio

from openstudio_toolkit.runtime import assert_reference_runtime
from openstudio_toolkit.schemas.inventory import (
    BuildingRecord,
    InventoryRun,
    ModelCounts,
    ModelInventory,
    Point3D,
    RuntimeRecord,
    SourceIdentityRecord,
    SourceRecord,
    SpaceRecord,
    StoryRecord,
    SubSurfaceRecord,
    SurfaceRecord,
    ThermalZoneRecord,
)


class InventoryExtractionError(RuntimeError):
    """Base error for canonical model inventory extraction."""


class ModelLoadError(InventoryExtractionError):
    """Raised when an OSM input cannot be loaded."""


class InputChangedError(InventoryExtractionError):
    """Raised when the registered source changes during extraction."""


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _name(model_object: Any) -> str | None:
    optional_name = model_object.name()
    return optional_name.get() if optional_name.is_initialized() else None


def _reference(optional_object: Any) -> tuple[str | None, str | None]:
    if not optional_object.is_initialized():
        return None, None
    model_object = optional_object.get()
    return str(model_object.handle()), _name(model_object)


def _optional_float(optional_value: Any) -> float | None:
    return float(optional_value.get()) if optional_value.is_initialized() else None


def _points(vertices: Any) -> list[Point3D]:
    return [Point3D(x_m=vertex.x(), y_m=vertex.y(), z_m=vertex.z()) for vertex in vertices]


def _load_model(path: Path) -> openstudio.model.Model:
    loaded = openstudio.osversion.VersionTranslator().loadModel(str(path))
    if not loaded.is_initialized():
        raise ModelLoadError(f"OpenStudio could not load model: {path}")
    return loaded.get()


def inspect_model(path: Path, *, registered_path: str | None = None) -> InventoryRun:
    """Extract a portable inventory plus a non-hashed provenance envelope."""
    runtime = assert_reference_runtime()
    input_path = Path(path)
    if not input_path.is_file():
        raise ModelLoadError(f"OSM input does not exist or is not a file: {input_path}")

    source_hash = _sha256(input_path)
    source_size = input_path.stat().st_size
    model = _load_model(input_path)

    building = model.getBuilding()
    story_objects = list(model.getBuildingStorys())
    space_objects = list(model.getSpaces())
    zone_objects = list(model.getThermalZones())
    surface_objects = list(model.getSurfaces())
    subsurface_objects = list(model.getSubSurfaces())

    story_space_handles: defaultdict[str, list[str]] = defaultdict(list)
    zone_space_handles: defaultdict[str, list[str]] = defaultdict(list)
    space_surface_handles: defaultdict[str, list[str]] = defaultdict(list)
    surface_subsurface_handles: defaultdict[str, list[str]] = defaultdict(list)

    spaces: list[SpaceRecord] = []
    for space in space_objects:
        space_handle = str(space.handle())
        story_handle, story_name = _reference(space.buildingStory())
        zone_handle, zone_name = _reference(space.thermalZone())
        space_type_handle, space_type_name = _reference(space.spaceType())
        if story_handle is not None:
            story_space_handles[story_handle].append(space_handle)
        if zone_handle is not None:
            zone_space_handles[zone_handle].append(space_handle)

        spaces.append(
            SpaceRecord(
                handle=space_handle,
                name=_name(space),
                story_handle=story_handle,
                story_name=story_name,
                thermal_zone_handle=zone_handle,
                thermal_zone_name=zone_name,
                space_type_handle=space_type_handle,
                space_type_name=space_type_name,
                part_of_total_floor_area=space.partofTotalFloorArea(),
                floor_area_m2=space.floorArea(),
                volume_m3=space.volume(),
                x_origin_m=space.xOrigin(),
                y_origin_m=space.yOrigin(),
                z_origin_m=space.zOrigin(),
                direction_of_relative_north_deg=space.directionofRelativeNorth(),
                surface_handles=[],
            )
        )

    surfaces: list[SurfaceRecord] = []
    for surface in surface_objects:
        surface_handle = str(surface.handle())
        parent_space_handle, space_name = _reference(surface.space())
        adjacent_handle, _ = _reference(surface.adjacentSurface())
        construction_handle, construction_name = _reference(surface.construction())
        if parent_space_handle is not None:
            space_surface_handles[parent_space_handle].append(surface_handle)

        surfaces.append(
            SurfaceRecord(
                handle=surface_handle,
                name=_name(surface),
                space_handle=parent_space_handle,
                space_name=space_name,
                surface_type=surface.surfaceType(),
                outside_boundary_condition=surface.outsideBoundaryCondition(),
                adjacent_surface_handle=adjacent_handle,
                construction_handle=construction_handle,
                construction_name=construction_name,
                sun_exposure=surface.sunExposure(),
                wind_exposure=surface.windExposure(),
                gross_area_m2=surface.grossArea(),
                net_area_m2=surface.netArea(),
                vertices=_points(surface.vertices()),
                subsurface_handles=[],
            )
        )

    subsurfaces: list[SubSurfaceRecord] = []
    for subsurface in subsurface_objects:
        subsurface_handle = str(subsurface.handle())
        parent_surface_handle, surface_name = _reference(subsurface.surface())
        construction_handle, construction_name = _reference(subsurface.construction())
        if parent_surface_handle is not None:
            surface_subsurface_handles[parent_surface_handle].append(subsurface_handle)

        subsurfaces.append(
            SubSurfaceRecord(
                handle=subsurface_handle,
                name=_name(subsurface),
                surface_handle=parent_surface_handle,
                surface_name=surface_name,
                subsurface_type=subsurface.subSurfaceType(),
                construction_handle=construction_handle,
                construction_name=construction_name,
                multiplier=subsurface.multiplier(),
                gross_area_m2=subsurface.grossArea(),
                net_area_m2=subsurface.netArea(),
                vertices=_points(subsurface.vertices()),
            )
        )

    # Relationships are populated from the already traversed collections.
    spaces = [
        SpaceRecord.model_validate(
            {**space.model_dump(), "surface_handles": space_surface_handles[space.handle]}
        )
        for space in spaces
    ]
    surfaces = [
        SurfaceRecord.model_validate(
            {**surface.model_dump(), "subsurface_handles": surface_subsurface_handles[surface.handle]}
        )
        for surface in surfaces
    ]

    stories = [
        StoryRecord(
            handle=str(story.handle()),
            name=_name(story),
            nominal_z_m=_optional_float(story.nominalZCoordinate()),
            nominal_floor_to_floor_height_m=_optional_float(story.nominalFloortoFloorHeight()),
            nominal_floor_to_ceiling_height_m=_optional_float(story.nominalFloortoCeilingHeight()),
            space_handles=story_space_handles[str(story.handle())],
        )
        for story in story_objects
    ]
    thermal_zones = [
        ThermalZoneRecord(
            handle=str(zone.handle()),
            name=_name(zone),
            multiplier=zone.multiplier(),
            space_handles=zone_space_handles[str(zone.handle())],
        )
        for zone in zone_objects
    ]

    counts = ModelCounts(
        stories=len(stories),
        spaces=len(spaces),
        thermal_zones=len(thermal_zones),
        surfaces=len(surfaces),
        subsurfaces=len(subsurfaces),
    )
    inventory = ModelInventory(
        source=SourceIdentityRecord(sha256=source_hash, size_bytes=source_size),
        building=BuildingRecord(
            handle=str(building.handle()),
            name=_name(building),
            north_axis_deg=building.northAxis(),
            floor_area_m2=building.floorArea(),
            conditioned_floor_area_m2=_optional_float(building.conditionedFloorArea()),
        ),
        counts=counts,
        stories=stories,
        spaces=spaces,
        thermal_zones=thermal_zones,
        surfaces=surfaces,
        subsurfaces=subsurfaces,
    )

    try:
        final_hash = _sha256(input_path)
    except OSError as exc:
        raise InputChangedError(f"OSM input became unavailable during extraction: {input_path}") from exc
    if final_hash != source_hash:
        raise InputChangedError(f"OSM input changed during extraction: {input_path}")

    return InventoryRun(
        source=SourceRecord(
            path=registered_path if registered_path is not None else str(input_path),
            filename=input_path.name,
            sha256=source_hash,
            size_bytes=source_size,
        ),
        runtime=RuntimeRecord.from_runtime_info(runtime),
        inventory=inventory,
    )
