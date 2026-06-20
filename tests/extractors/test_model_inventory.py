"""P2.2 acceptance tests for read-only SDK inventory extraction."""

from __future__ import annotations

import hashlib
from pathlib import Path

import openstudio
import pytest

from openstudio_toolkit.extractors import InputChangedError, ModelLoadError, inspect_model
from openstudio_toolkit.runtime import RuntimeMismatchError
from openstudio_toolkit.schemas import InventoryRun, RuntimeRecord, SourceRecord, serialize_inventory

TOOLKIT_ROOT = Path(__file__).resolve().parents[2]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_small_fixture_is_read_only_and_complete() -> None:
    path = TOOLKIT_ROOT / "tests" / "resources" / "small_office.osm"
    before = _sha256(path)

    run = inspect_model(path, registered_path="fixtures/small_office.osm")
    inventory = run.inventory

    assert run.source.path == "fixtures/small_office.osm"
    assert inventory.source.sha256 == before
    assert _sha256(path) == before
    assert inventory.counts.spaces == 6
    assert inventory.counts.thermal_zones == 6
    assert inventory.counts.surfaces == 43
    assert inventory.counts.subsurfaces == 23


def test_office_hub_relationships_resolve_and_serialize_deterministically() -> None:
    path = TOOLKIT_ROOT / "examples" / "R2F-Office-Hub.osm"

    first_run = inspect_model(path)
    second_run = inspect_model(path)
    first = first_run.inventory
    second = second_run.inventory

    assert first.counts.model_dump() == {
        "stories": 2,
        "spaces": 36,
        "thermal_zones": 36,
        "surfaces": 278,
        "subsurfaces": 53,
    }
    story_handles = {story.handle for story in first.stories}
    zone_handles = {zone.handle for zone in first.thermal_zones}
    space_handles = {space.handle for space in first.spaces}
    surface_handles = {surface.handle for surface in first.surfaces}
    subsurface_handles = {subsurface.handle for subsurface in first.subsurfaces}

    assert all(space.story_handle in story_handles for space in first.spaces)
    assert all(space.thermal_zone_handle in zone_handles for space in first.spaces)
    assert all(surface.space_handle in space_handles for surface in first.surfaces)
    assert all(subsurface.surface_handle in surface_handles for subsurface in first.subsurfaces)
    assert {handle for story in first.stories for handle in story.space_handles} == space_handles
    assert {handle for zone in first.thermal_zones for handle in zone.space_handles} == space_handles
    assert {handle for space in first.spaces for handle in space.surface_handles} == surface_handles
    assert {
        handle for surface in first.surfaces for handle in surface.subsurface_handles
    } == subsurface_handles
    assert all(
        surface.adjacent_surface_handle is None or surface.adjacent_surface_handle in surface_handles
        for surface in first.surfaces
    )
    assert serialize_inventory(first) == serialize_inventory(second)


def test_space_local_vertices_survive_translation_rotation_and_reload(tmp_path: Path) -> None:
    model = openstudio.model.Model()
    points = openstudio.Point3dVector()
    for x, y in ((0.0, 0.0), (0.0, 5.0), (10.0, 5.0), (10.0, 0.0)):
        points.append(openstudio.Point3d(x, y, 0.0))

    space_optional = openstudio.model.Space.fromFloorPrint(points, 3.0, model)
    assert space_optional.is_initialized()
    space = space_optional.get()
    space.setName("Translated-Rotated-Space")
    space.setXOrigin(10.0)
    space.setYOrigin(20.0)
    space.setZOrigin(2.0)
    space.setDirectionofRelativeNorth(30.0)
    path = tmp_path / "coordinate-frame.osm"
    model.save(str(path), True)

    inventory = inspect_model(path).inventory
    space_record = next(record for record in inventory.spaces if record.name == "Translated-Rotated-Space")
    surface_record = next(record for record in inventory.surfaces if record.space_handle == space_record.handle)
    local_vertex = surface_record.vertices[0]
    source_surface = model.getSurface(openstudio.toUUID(surface_record.handle)).get()
    source_vertex = source_surface.vertices()[0]
    transformed = space.transformation() * source_vertex

    assert (space_record.x_origin_m, space_record.y_origin_m, space_record.z_origin_m) == (10.0, 20.0, 2.0)
    assert space_record.direction_of_relative_north_deg == 30.0
    assert surface_record.coordinate_system == "space_local"
    assert (local_vertex.x_m, local_vertex.y_m, local_vertex.z_m) == (
        source_vertex.x(),
        source_vertex.y(),
        source_vertex.z(),
    )
    assert (transformed.x(), transformed.y(), transformed.z()) != (
        local_vertex.x_m,
        local_vertex.y_m,
        local_vertex.z_m,
    )


def test_invalid_osm_raises_explicit_load_error(tmp_path: Path) -> None:
    path = tmp_path / "invalid.osm"
    path.write_text("not an OpenStudio model", encoding="utf-8")

    with pytest.raises(ModelLoadError, match="could not load model"):
        inspect_model(path)


def test_input_hash_change_fails_loudly(monkeypatch: pytest.MonkeyPatch) -> None:
    path = TOOLKIT_ROOT / "tests" / "resources" / "small_office.osm"
    real_hash = _sha256(path)
    hashes = iter((real_hash, "b" * 64))
    monkeypatch.setattr("openstudio_toolkit.extractors.model_inventory._sha256", lambda _: next(hashes))

    with pytest.raises(InputChangedError, match="changed during extraction"):
        inspect_model(path)


def test_runtime_assertion_is_a_hard_gate(monkeypatch: pytest.MonkeyPatch) -> None:
    path = TOOLKIT_ROOT / "tests" / "resources" / "small_office.osm"

    def fail_runtime() -> None:
        raise RuntimeMismatchError("test mismatch")

    monkeypatch.setattr("openstudio_toolkit.extractors.model_inventory.assert_reference_runtime", fail_runtime)

    with pytest.raises(RuntimeMismatchError, match="test mismatch"):
        inspect_model(path)


def test_semantic_hash_is_portable_across_envelope_paths() -> None:
    path = TOOLKIT_ROOT / "tests" / "resources" / "small_office.osm"
    local_run = inspect_model(path, registered_path="project/models/small_office.osm")
    remote_run = InventoryRun(
        source=SourceRecord(
            sha256=local_run.source.sha256,
            size_bytes=local_run.source.size_bytes,
            path="/different/machine/small_office.osm",
            filename=local_run.source.filename,
        ),
        runtime=RuntimeRecord(
            python_version=local_run.runtime.python_version,
            python_executable="/different/runtime/python",
            openstudio_version=local_run.runtime.openstudio_version,
            energyplus_version=local_run.runtime.energyplus_version,
            openstudio_module_path="/different/runtime/openstudio/__init__.py",
        ),
        inventory=local_run.inventory,
    )

    assert serialize_inventory(local_run.inventory) == serialize_inventory(remote_run.inventory)
