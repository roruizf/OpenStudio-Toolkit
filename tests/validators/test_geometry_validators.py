"""Pure validator tests over synthetic and extracted inventories."""

from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from openstudio_toolkit.extractors import inspect_model
from openstudio_toolkit.schemas import (
    BuildingRecord,
    GeometryValidationReport,
    ModelCounts,
    ModelInventory,
    NamingProfile,
    Point3D,
    SourceIdentityRecord,
    SpaceRecord,
    StoryRecord,
    SubSurfaceRecord,
    SurfaceRecord,
    ThermalZoneRecord,
    render_validation_report_markdown,
    serialize_inventory,
    serialize_validation_report,
)
from openstudio_toolkit.validators import (
    build_geometry_validation_report,
    validate_geometry_inventory,
    validate_inventory_integrity,
    validate_model_object_naming,
    validate_spatial_assignments,
)
from openstudio_toolkit.validators.integrity import AREA_ABSOLUTE_TOLERANCE_M2, AREA_RELATIVE_TOLERANCE

TOOLKIT_ROOT = Path(__file__).resolve().parents[2]
VERTICES = [
    Point3D(x_m=0.0, y_m=0.0, z_m=0.0),
    Point3D(x_m=1.0, y_m=0.0, z_m=0.0),
    Point3D(x_m=1.0, y_m=1.0, z_m=0.0),
]


def _inventory(
    *,
    stories: list[StoryRecord] | None = None,
    spaces: list[SpaceRecord] | None = None,
    zones: list[ThermalZoneRecord] | None = None,
    surfaces: list[SurfaceRecord] | None = None,
    subsurfaces: list[SubSurfaceRecord] | None = None,
) -> ModelInventory:
    story_records = stories if stories is not None else [_story()]
    space_records = spaces if spaces is not None else [_space()]
    zone_records = zones if zones is not None else [_zone()]
    surface_records = surfaces if surfaces is not None else [_surface()]
    subsurface_records = subsurfaces if subsurfaces is not None else []
    return ModelInventory(
        source=SourceIdentityRecord(sha256="a" * 64, size_bytes=42),
        building=BuildingRecord(
            handle="building-1",
            name="Building",
            north_axis_deg=0.0,
            floor_area_m2=10.0,
            conditioned_floor_area_m2=10.0,
        ),
        counts=ModelCounts(
            stories=len(story_records),
            spaces=len(space_records),
            thermal_zones=len(zone_records),
            surfaces=len(surface_records),
            subsurfaces=len(subsurface_records),
        ),
        stories=story_records,
        spaces=space_records,
        thermal_zones=zone_records,
        surfaces=surface_records,
        subsurfaces=subsurface_records,
    )


def _story(**changes: object) -> StoryRecord:
    data: dict[str, object] = {
        "handle": "story-1",
        "name": "Story 1",
        "nominal_z_m": 0.0,
        "nominal_floor_to_floor_height_m": 3.0,
        "nominal_floor_to_ceiling_height_m": 2.8,
        "space_handles": ["space-1"],
    }
    data.update(changes)
    return StoryRecord.model_validate(data)


def _zone(**changes: object) -> ThermalZoneRecord:
    data: dict[str, object] = {
        "handle": "zone-1",
        "name": "Zone 1",
        "multiplier": 1,
        "space_handles": ["space-1"],
    }
    data.update(changes)
    return ThermalZoneRecord.model_validate(data)


def _space(**changes: object) -> SpaceRecord:
    data: dict[str, object] = {
        "handle": "space-1",
        "name": "Space 1",
        "story_handle": "story-1",
        "story_name": "Story 1",
        "thermal_zone_handle": "zone-1",
        "thermal_zone_name": "Zone 1",
        "space_type_handle": None,
        "space_type_name": None,
        "part_of_total_floor_area": True,
        "floor_area_m2": 10.0,
        "volume_m3": 30.0,
        "x_origin_m": 0.0,
        "y_origin_m": 0.0,
        "z_origin_m": 0.0,
        "direction_of_relative_north_deg": 0.0,
        "surface_handles": ["surface-1"],
    }
    data.update(changes)
    return SpaceRecord.model_validate(data)


def _surface(**changes: object) -> SurfaceRecord:
    data: dict[str, object] = {
        "handle": "surface-1",
        "name": "Space 1_Wall_Outdoors_1",
        "space_handle": "space-1",
        "space_name": "Space 1",
        "surface_type": "Wall",
        "outside_boundary_condition": "Outdoors",
        "adjacent_surface_handle": None,
        "construction_handle": None,
        "construction_name": None,
        "sun_exposure": "SunExposed",
        "wind_exposure": "WindExposed",
        "gross_area_m2": 10.0,
        "net_area_m2": 10.0,
        "coordinate_system": "space_local",
        "vertices": VERTICES,
        "subsurface_handles": [],
    }
    data.update(changes)
    return SurfaceRecord.model_validate(data)


def _subsurface(**changes: object) -> SubSurfaceRecord:
    data: dict[str, object] = {
        "handle": "subsurface-1",
        "name": "Space 1_Wall_Outdoors_1_Window_1",
        "surface_handle": "surface-1",
        "surface_name": "Space 1_Wall_Outdoors_1",
        "subsurface_type": "FixedWindow",
        "construction_handle": None,
        "construction_name": None,
        "multiplier": 1.0,
        "gross_area_m2": 1.0,
        "net_area_m2": 1.0,
        "coordinate_system": "space_local",
        "vertices": VERTICES,
    }
    data.update(changes)
    return SubSurfaceRecord.model_validate(data)


def _codes(inventory: ModelInventory) -> list[str]:
    return [finding.code for finding in validate_inventory_integrity(inventory)]


def test_valid_inventory_is_clean_and_validators_are_pure() -> None:
    inventory = _inventory()
    before = serialize_inventory(inventory)

    assert validate_inventory_integrity(inventory) == []
    assert validate_spatial_assignments(inventory) == []
    assert serialize_inventory(inventory) == before


def test_unresolved_and_nonreciprocal_relationships_are_blockers() -> None:
    unresolved = _inventory(spaces=[_space(story_handle="missing-story")])
    nonreciprocal = _inventory(stories=[_story(space_handles=[])])

    unresolved_finding = next(
        finding
        for finding in validate_inventory_integrity(unresolved)
        if finding.code == "integrity.reference.unresolved"
    )
    nonreciprocal_finding = next(
        finding
        for finding in validate_inventory_integrity(nonreciprocal)
        if finding.code == "integrity.relationship.nonreciprocal"
    )
    assert unresolved_finding.severity == "blocker"
    assert nonreciprocal_finding.severity == "blocker"


def test_duplicate_name_severity_depends_on_object_class() -> None:
    spaces = [
        _space(surface_handles=[], name="Duplicate"),
        _space(
            handle="space-2",
            name="Duplicate",
            story_handle=None,
            story_name=None,
            thermal_zone_handle=None,
            thermal_zone_name=None,
            surface_handles=[],
        ),
    ]
    surfaces = [
        _surface(name="Duplicate Surface"),
        _surface(handle="surface-2", name="Duplicate Surface", space_handle=None, space_name=None),
    ]
    inventory = _inventory(stories=[], zones=[], spaces=spaces, surfaces=surfaces)
    duplicates = [
        finding for finding in validate_inventory_integrity(inventory) if finding.code == "integrity.name.duplicate"
    ]

    assert {(finding.object_type, finding.severity) for finding in duplicates} == {
        ("space", "major"),
        ("surface", "minor"),
    }


def test_geometry_and_subsurface_area_tolerance() -> None:
    invalid = _inventory(
        spaces=[_space(floor_area_m2=0.0, volume_m3=-1.0)],
        surfaces=[_surface(vertices=[])],
    )
    assert {
        "integrity.geometry.nonpositive_space_area",
        "integrity.geometry.nonpositive_space_volume",
        "integrity.geometry.invalid_surface_polygon",
    }.issubset(_codes(invalid))

    surface_area = 10.0
    tolerance = max(AREA_ABSOLUTE_TOLERANCE_M2, surface_area * AREA_RELATIVE_TOLERANCE)
    surface = _surface(gross_area_m2=surface_area, subsurface_handles=["subsurface-1"])
    within = _inventory(
        surfaces=[surface],
        subsurfaces=[_subsurface(gross_area_m2=surface_area + tolerance)],
    )
    beyond = _inventory(
        surfaces=[surface],
        subsurfaces=[_subsurface(gross_area_m2=surface_area + 2 * tolerance)],
    )
    assert "integrity.geometry.subsurface_exceeds_surface" not in _codes(within)
    assert "integrity.geometry.subsurface_exceeds_surface" in _codes(beyond)


def test_spatial_findings_cover_null_assignments_but_not_space_type() -> None:
    inventory = _inventory(
        stories=[_story(space_handles=[])],
        zones=[_zone(space_handles=[])],
        spaces=[
            _space(
                story_handle=None,
                story_name=None,
                thermal_zone_handle=None,
                thermal_zone_name=None,
                surface_handles=[],
            )
        ],
        surfaces=[_surface(space_handle=None, space_name=None, coordinate_system="model")],
        subsurfaces=[_subsurface(surface_handle=None, surface_name=None, coordinate_system="model")],
    )
    codes = {finding.code for finding in validate_spatial_assignments(inventory)}

    assert codes == {
        "spatial.space.missing_story",
        "spatial.space.missing_thermal_zone",
        "spatial.space.no_surfaces",
        "spatial.story.no_spaces",
        "spatial.subsurface.missing_surface",
        "spatial.surface.missing_space",
        "spatial.thermal_zone.no_spaces",
    }
    assert "spatial.space.missing_space_type" not in codes


def test_office_hub_has_no_broken_or_orphan_relationships() -> None:
    inventory = inspect_model(TOOLKIT_ROOT / "examples" / "R2F-Office-Hub.osm").inventory
    findings = validate_inventory_integrity(inventory) + validate_spatial_assignments(inventory)
    forbidden = {
        "integrity.reference.unresolved",
        "integrity.relationship.nonreciprocal",
        "spatial.surface.missing_space",
        "spatial.subsurface.missing_surface",
    }

    assert not ({finding.code for finding in findings} & forbidden)


def _profile(**changes: object) -> NamingProfile:
    data: dict[str, object] = {
        "profile_id": "synthetic",
        "version": "1.0",
        "status": "approved",
        "space_pattern": r"Space [0-9]+",
        "one_to_one_zone_template": "TZ-{space_name}",
        "multi_space_zone_pattern": r"TZ-GROUP-[0-9]+",
    }
    data.update(changes)
    return NamingProfile.model_validate(data)


def test_naming_validator_accepts_relationship_derived_names() -> None:
    inventory = _inventory(zones=[_zone(name="TZ-Space 1")])

    assert validate_model_object_naming(inventory, _profile()) == []


def test_draft_incomplete_profile_emits_one_observation_per_profile_defect() -> None:
    profile = NamingProfile(profile_id="draft", version="1", status="draft")
    findings = validate_model_object_naming(_inventory(), profile)

    assert [finding.code for finding in findings] == [
        "naming.profile.draft",
        "naming.profile.incomplete",
    ]
    incomplete = findings[1]
    assert incomplete.evidence["missing_fields"] == ["one_to_one_zone_template", "space_pattern"]


def test_surface_diagnostic_precedence_emits_only_upstream_defect() -> None:
    surface = _surface(name="WrongOwner_BadType_BadBoundary_0")
    findings = validate_model_object_naming(_inventory(surfaces=[surface]), _profile())

    surface_findings = [finding for finding in findings if finding.object_type == "surface"]
    assert [finding.code for finding in surface_findings] == ["naming.surface.owner_mismatch"]


def test_surface_matching_never_splits_owner_name_or_confuses_prefixes() -> None:
    owner_name = "B2-1.21__sales-manager-office"
    inventory = _inventory(
        spaces=[_space(name=owner_name)],
        surfaces=[_surface(name=f"{owner_name}_Wall_Outdoors_1", space_name=owner_name)],
        zones=[_zone(name=f"TZ-{owner_name}")],
    )
    profile = _profile(space_pattern=r"B2-.+", one_to_one_zone_template="TZ-{space_name}")

    assert validate_model_object_naming(inventory, profile) == []

    collision = _inventory(
        spaces=[_space(name="B2-0.1")],
        surfaces=[_surface(name="B2-0.10_Wall_Outdoors_1", space_name="B2-0.1")],
        zones=[_zone(name="TZ-B2-0.1")],
    )
    codes = [finding.code for finding in validate_model_object_naming(collision, _profile(space_pattern=r"B2-.+"))]
    assert "naming.surface.owner_mismatch" in codes


def test_boundary_token_adjacent_space_collision_is_documented_behavior() -> None:
    spaces = [
        _space(name="ZoneA", surface_handles=["surface-1"]),
        _space(
            handle="space-2",
            name="Outdoors",
            story_handle=None,
            story_name=None,
            thermal_zone_handle=None,
            thermal_zone_name=None,
            surface_handles=["surface-2"],
        ),
    ]
    surfaces = [
        _surface(
            name="ZoneA_Wall_Outdoors_1",
            adjacent_surface_handle="surface-2",
        ),
        _surface(
            handle="surface-2",
            name="Outdoors_Wall_ZoneA_1",
            space_handle="space-2",
            space_name="Outdoors",
            adjacent_surface_handle="surface-1",
        ),
    ]
    inventory = _inventory(spaces=spaces, zones=[], surfaces=surfaces)
    profile = _profile(space_pattern=r"(?:ZoneA|Outdoors)")

    assert validate_model_object_naming(inventory, profile) == []


def test_subsurface_reports_parent_before_type_or_sequence() -> None:
    parent = _surface(subsurface_handles=["subsurface-1"])
    stale = _subsurface(name="WrongParent_BadType_0")
    findings = validate_model_object_naming(
        _inventory(surfaces=[parent], subsurfaces=[stale]),
        _profile(),
    )

    assert [finding.code for finding in findings if finding.object_type == "subsurface"] == [
        "naming.subsurface.parent_mismatch"
    ]


def test_surface_relationship_precedes_sequence_diagnostic() -> None:
    relationship = _inventory(surfaces=[_surface(name="Space 1_Wall_Ground_0")])
    sequence = _inventory(surfaces=[_surface(name="Space 1_Wall_Outdoors_0")])

    assert [
        finding.code
        for finding in validate_model_object_naming(relationship, _profile())
        if finding.object_type == "surface"
    ] == ["naming.surface.relationship_mismatch"]
    assert [
        finding.code
        for finding in validate_model_object_naming(sequence, _profile())
        if finding.object_type == "surface"
    ] == ["naming.surface.sequence_missing"]


def test_multi_space_zone_requires_explicit_shape_rule() -> None:
    spaces = [
        _space(surface_handles=[]),
        _space(
            handle="space-2",
            name="Space 2",
            story_handle=None,
            story_name=None,
            thermal_zone_handle="zone-1",
            thermal_zone_name="Group Zone",
            surface_handles=[],
        ),
    ]
    zone = _zone(name="Group Zone", space_handles=["space-1", "space-2"])
    inventory = _inventory(stories=[], spaces=spaces, zones=[zone], surfaces=[])

    missing = validate_model_object_naming(inventory, _profile(multi_space_zone_pattern=None))
    mismatch = validate_model_object_naming(inventory, _profile())

    assert "naming.thermal_zone.multi_space_rule_missing" in {finding.code for finding in missing}
    assert "naming.thermal_zone.multi_space_mismatch" in {finding.code for finding in mismatch}


def test_unresolved_zone_membership_is_left_to_integrity_validator() -> None:
    zone = _zone(name="Wrong", space_handles=["space-1", "missing-space"])
    findings = validate_model_object_naming(_inventory(zones=[zone]), _profile())

    assert not any(finding.code.startswith("naming.thermal_zone.") for finding in findings)


def test_composer_and_report_distinguish_naming_not_run() -> None:
    inventory = _inventory()
    before = serialize_inventory(inventory)
    report = build_geometry_validation_report(inventory)

    assert report.checks_run == ["integrity", "spatial"]
    assert report.naming_profile_id is None
    assert validate_geometry_inventory(inventory) == []
    assert "Naming not run" in render_validation_report_markdown(report)
    assert serialize_inventory(inventory) == before


def test_report_and_markdown_are_portable_and_deterministic() -> None:
    inventory = _inventory(spaces=[_space(story_handle="missing-story")])
    report = build_geometry_validation_report(inventory, naming_profile=_profile(status="draft"))
    artifact = serialize_validation_report(report)
    rebuilt = GeometryValidationReport.model_validate(report.model_dump(mode="json"))

    assert serialize_validation_report(rebuilt) == artifact
    assert render_validation_report_markdown(rebuilt) == render_validation_report_markdown(report)
    assert report.inventory_sha256 == serialize_inventory(inventory).sha256


def test_report_enforces_checks_and_profile_identity() -> None:
    inventory_sha256 = serialize_inventory(_inventory()).sha256
    with pytest.raises(ValidationError, match="require integrity and spatial"):
        GeometryValidationReport(inventory_sha256=inventory_sha256, checks_run=["naming"])
    with pytest.raises(ValidationError, match="identity is required"):
        GeometryValidationReport(
            inventory_sha256=inventory_sha256,
            checks_run=["integrity", "spatial", "naming"],
        )


def test_report_serialization_rejects_non_finite_evidence() -> None:
    report = build_geometry_validation_report(_inventory(spaces=[_space(story_handle="missing-story")]))
    finding = report.findings[0].model_copy(update={"evidence": {"value": float("nan")}})
    invalid = report.model_copy(update={"findings": [finding]})

    with pytest.raises(ValueError, match="Out of range float values"):
        serialize_validation_report(invalid)
    with pytest.raises(ValueError, match="Out of range float values"):
        render_validation_report_markdown(invalid)


def test_markdown_evidence_key_order_is_canonical() -> None:
    report = build_geometry_validation_report(_inventory(spaces=[_space(story_handle="missing-story")]))
    finding = report.findings[0]
    first = report.model_copy(update={"findings": [finding.model_copy(update={"evidence": {"b": 2, "a": 1}})]})
    second = report.model_copy(update={"findings": [finding.model_copy(update={"evidence": {"a": 1, "b": 2}})]})

    assert render_validation_report_markdown(first) == render_validation_report_markdown(second)
