"""P2.3 edge, compatibility, and caller-owned artifact evidence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import openstudio

from openstudio_toolkit.extractors import inspect_model
from openstudio_toolkit.osm_objects import spaces as legacy_spaces
from openstudio_toolkit.schemas import serialize_inventory

TOOLKIT_ROOT = Path(__file__).resolve().parents[2]


def _load_model(path: Path) -> openstudio.model.Model:
    loaded = openstudio.osversion.VersionTranslator().loadModel(str(path))
    assert loaded.is_initialized()
    return loaded.get()


def test_null_relationships_and_orphan_coordinate_frames(tmp_path: Path) -> None:
    model = openstudio.model.Model()
    floor_points = openstudio.Point3dVector()
    for x, y in ((0.0, 0.0), (0.0, 4.0), (6.0, 4.0), (6.0, 0.0)):
        floor_points.append(openstudio.Point3d(x, y, 0.0))
    space_optional = openstudio.model.Space.fromFloorPrint(floor_points, 3.0, model)
    assert space_optional.is_initialized()
    space_optional.get().setName("Unassigned-Space")

    orphan_points = openstudio.Point3dVector()
    for x, y in ((10.0, 0.0), (10.0, 2.0), (13.0, 2.0), (13.0, 0.0)):
        orphan_points.append(openstudio.Point3d(x, y, 1.0))
    orphan_surface = openstudio.model.Surface(orphan_points, model)
    orphan_surface.setName("Orphan-Surface")

    orphan_subsurface = openstudio.model.SubSurface(orphan_points, model)
    orphan_subsurface.setName("Orphan-SubSurface")

    path = tmp_path / "nullable-relationships.osm"
    model.save(str(path), True)
    inventory = inspect_model(path).inventory

    space = next(record for record in inventory.spaces if record.name == "Unassigned-Space")
    surface = next(record for record in inventory.surfaces if record.name == "Orphan-Surface")
    subsurface = next(record for record in inventory.subsurfaces if record.name == "Orphan-SubSurface")

    assert space.story_handle is None
    assert space.story_name is None
    assert space.thermal_zone_handle is None
    assert space.thermal_zone_name is None
    assert surface.space_handle is None
    assert surface.coordinate_system == "model"
    assert subsurface.surface_handle is None
    assert subsurface.coordinate_system == "model"
    assert all(
        record.coordinate_system == "space_local"
        for record in inventory.surfaces
        if record.space_handle == space.handle
    )


def test_canonical_space_fields_match_legacy_human_projection() -> None:
    path = TOOLKIT_ROOT / "tests" / "resources" / "small_office.osm"
    legacy_by_handle = {
        record["Handle"]: record for record in legacy_spaces.get_all_space_objects_as_dicts(_load_model(path))
    }
    inventory = inspect_model(path).inventory

    for canonical in inventory.spaces:
        legacy = legacy_by_handle[canonical.handle]
        assert canonical.name == legacy["Name"]
        assert canonical.space_type_name == legacy["Space Type Name"]
        assert canonical.story_name == legacy["Building Story Name"]
        assert canonical.thermal_zone_name == legacy["Thermal Zone Name"]
        assert canonical.part_of_total_floor_area == legacy["Part of Total Floor Area"]
        assert canonical.floor_area_m2 == legacy["Floor Area {m2}"]
        assert canonical.volume_m3 == legacy["Volume {m3}"]
        assert canonical.x_origin_m == legacy["X Origin {m}"]
        assert canonical.y_origin_m == legacy["Y Origin {m}"]
        assert canonical.z_origin_m == legacy["Z Origin {m}"]
        assert canonical.direction_of_relative_north_deg == legacy["Direction of Relative North {deg}"]


def test_caller_can_write_and_verify_office_hub_artifact_in_tmp(tmp_path: Path) -> None:
    source = TOOLKIT_ROOT / "examples" / "R2F-Office-Hub.osm"
    run = inspect_model(source, registered_path="fixtures/R2F-Office-Hub.osm")
    artifact = serialize_inventory(run.inventory)
    output = tmp_path / "R2F-Office-Hub.inventory.json"

    output.write_bytes(artifact.content)
    persisted = output.read_bytes()
    decoded = json.loads(persisted)

    assert persisted == artifact.content
    assert hashlib.sha256(persisted).hexdigest() == artifact.sha256
    assert decoded["schema_version"] == "0.1.0"
    assert decoded["counts"] == {
        "spaces": 36,
        "stories": 2,
        "subsurfaces": 53,
        "surfaces": 278,
        "thermal_zones": 36,
    }
    assert not hasattr(run, "write")
