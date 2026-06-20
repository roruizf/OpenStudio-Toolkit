"""Tests for the canonical P2.1 model inventory contract."""

from __future__ import annotations

import json

import pytest
from pydantic import ValidationError

from openstudio_toolkit.schemas.inventory import (
    BuildingRecord,
    InventoryRun,
    ModelCounts,
    ModelInventory,
    RuntimeRecord,
    SourceIdentityRecord,
    SourceRecord,
    SpaceRecord,
    StoryRecord,
    serialize_inventory,
)


def _source_identity() -> SourceIdentityRecord:
    return SourceIdentityRecord(sha256="a" * 64, size_bytes=42)


def _source() -> SourceRecord:
    return SourceRecord(sha256="a" * 64, size_bytes=42, path="models/example.osm", filename="example.osm")


def _runtime() -> RuntimeRecord:
    return RuntimeRecord(
        python_version="3.13.10",
        python_executable="/runtime/python",
        openstudio_version="3.10.0",
        energyplus_version="25.1.0",
        openstudio_module_path="/runtime/openstudio/__init__.py",
    )


def _building() -> BuildingRecord:
    return BuildingRecord(
        handle="building-1",
        name="Example",
        north_axis_deg=0.0,
        floor_area_m2=100.0,
        conditioned_floor_area_m2=None,
    )


def _inventory(
    *,
    building: BuildingRecord | None = None,
    stories: list[StoryRecord] | None = None,
) -> ModelInventory:
    story_records = stories or []
    return ModelInventory(
        source=_source_identity(),
        building=building or _building(),
        counts=ModelCounts(
            stories=len(story_records), spaces=0, thermal_zones=0, surfaces=0, subsurfaces=0
        ),
        stories=story_records,
    )


def test_inventory_rejects_inconsistent_counts() -> None:
    with pytest.raises(ValidationError, match="Inventory counts do not match collections"):
        ModelInventory(
            source=_source_identity(),
            building=_building(),
            counts=ModelCounts(stories=1, spaces=0, thermal_zones=0, surfaces=0, subsurfaces=0),
        )


def test_records_and_relationship_handles_are_sorted() -> None:
    stories = [
        StoryRecord(
            handle="story-b",
            name="Level B",
            nominal_z_m=3.0,
            nominal_floor_to_floor_height_m=None,
            nominal_floor_to_ceiling_height_m=None,
            space_handles=["space-2", "space-1"],
        ),
        StoryRecord(
            handle="story-a",
            name="Level A",
            nominal_z_m=0.0,
            nominal_floor_to_floor_height_m=None,
            nominal_floor_to_ceiling_height_m=None,
            space_handles=[],
        ),
    ]

    inventory = _inventory(stories=stories)

    assert [story.handle for story in inventory.stories] == ["story-a", "story-b"]
    assert inventory.stories[1].space_handles == ["space-1", "space-2"]


def test_canonical_serialization_is_byte_deterministic() -> None:
    first = _inventory(
        stories=[
            StoryRecord(
                handle="story-b",
                name="B",
                nominal_z_m=None,
                nominal_floor_to_floor_height_m=None,
                nominal_floor_to_ceiling_height_m=None,
            ),
            StoryRecord(
                handle="story-a",
                name="A",
                nominal_z_m=None,
                nominal_floor_to_floor_height_m=None,
                nominal_floor_to_ceiling_height_m=None,
            ),
        ]
    )
    second = _inventory(stories=list(reversed(first.stories)))

    first_artifact = serialize_inventory(first)
    second_artifact = serialize_inventory(second)

    assert first_artifact.content == second_artifact.content
    assert first_artifact.sha256 == second_artifact.sha256
    assert json.loads(first_artifact.content)["building"]["conditioned_floor_area_m2"] is None


def test_nested_collections_follow_build_once_contract() -> None:
    inventory = _inventory(
        stories=[
            StoryRecord(
                handle="story-a",
                name="A",
                nominal_z_m=None,
                nominal_floor_to_floor_height_m=None,
                nominal_floor_to_ceiling_height_m=None,
                space_handles=["space-a"],
            )
        ]
    )
    before = serialize_inventory(inventory)

    inventory.stories[0].space_handles.append("space-b")
    after = serialize_inventory(inventory)

    assert before.sha256 != after.sha256


@pytest.mark.parametrize("non_finite", [float("nan"), float("inf"), float("-inf")])
def test_canonical_serialization_rejects_non_finite_floats(non_finite: float) -> None:
    building = _building().model_copy(update={"floor_area_m2": non_finite})

    with pytest.raises(ValueError, match="Out of range float values"):
        serialize_inventory(_inventory(building=building))


def test_unicode_serialization_is_utf8_and_deterministic() -> None:
    inventory = _inventory(building=_building().model_copy(update={"name": "Café-1"}))

    first = serialize_inventory(inventory)
    second = serialize_inventory(inventory)

    assert first.content == second.content
    assert "Café-1".encode() in first.content
    assert b"Caf\\u00e9-1" not in first.content


def test_inventory_records_forbid_unknown_fields() -> None:
    data = _source().model_dump()
    data["unexpected"] = True

    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        SourceRecord.model_validate(data)


def test_run_envelope_source_identity_must_match_inventory() -> None:
    with pytest.raises(ValidationError, match="Run source identity does not match"):
        InventoryRun(
            source=SourceRecord(
                sha256="b" * 64,
                size_bytes=42,
                path="models/example.osm",
                filename="example.osm",
            ),
            runtime=_runtime(),
            inventory=_inventory(),
        )


def test_space_field_lineage_preserves_openstudio_labels() -> None:
    floor_area_metadata = SpaceRecord.model_fields["floor_area_m2"].json_schema_extra
    story_handle_metadata = SpaceRecord.model_fields["story_handle"].json_schema_extra

    assert floor_area_metadata["openstudio"] == {
        "osm_label": "Floor Area {m2}",
        "sdk_accessor": "Space.floorArea()",
        "legacy_key": "Floor Area {m2}",
        "lineage_note": None,
    }
    assert story_handle_metadata["openstudio"]["osm_label"] == "Building Story Name"
    assert "stores a handle" in story_handle_metadata["openstudio"]["lineage_note"]
