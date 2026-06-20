"""Project-independent integrity checks for canonical model inventories."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from typing import Any

from openstudio_toolkit.schemas.findings import Finding, FindingObjectType, FindingSeverity, sort_findings
from openstudio_toolkit.schemas.inventory import ModelInventory

AREA_ABSOLUTE_TOLERANCE_M2 = 1e-6
AREA_RELATIVE_TOLERANCE = 1e-6


def _finding(
    *,
    code: str,
    severity: FindingSeverity,
    message: str,
    object_type: FindingObjectType,
    object_handle: str | None,
    object_name: str | None,
    related_handles: Iterable[str] = (),
    evidence: dict[str, Any] | None = None,
    suggested_action: str | None = None,
) -> Finding:
    return Finding(
        code=code,
        severity=severity,
        message=message,
        object_type=object_type,
        object_handle=object_handle,
        object_name=object_name,
        related_handles=list(related_handles),
        evidence=evidence or {},
        suggested_action=suggested_action,
    )


def _unresolved_reference_findings(inventory: ModelInventory) -> list[Finding]:
    findings: list[Finding] = []
    story_handles = {record.handle for record in inventory.stories}
    zone_handles = {record.handle for record in inventory.thermal_zones}
    space_handles = {record.handle for record in inventory.spaces}
    surface_handles = {record.handle for record in inventory.surfaces}
    subsurface_handles = {record.handle for record in inventory.subsurfaces}

    def check(
        *,
        owner_type: FindingObjectType,
        owner_handle: str,
        owner_name: str | None,
        field: str,
        target: str | None,
        known: set[str],
    ) -> None:
        if target is not None and target not in known:
            findings.append(
                _finding(
                    code="integrity.reference.unresolved",
                    severity="blocker",
                    message=f"{field} references an object absent from the inventory.",
                    object_type=owner_type,
                    object_handle=owner_handle,
                    object_name=owner_name,
                    related_handles=[target],
                    evidence={"field": field, "referenced_handle": target},
                    suggested_action="Repair the model relationship before geometry release.",
                )
            )

    for story in inventory.stories:
        for handle in story.space_handles:
            check(
                owner_type="building_story",
                owner_handle=story.handle,
                owner_name=story.name,
                field="space_handles",
                target=handle,
                known=space_handles,
            )
    for zone in inventory.thermal_zones:
        for handle in zone.space_handles:
            check(
                owner_type="thermal_zone",
                owner_handle=zone.handle,
                owner_name=zone.name,
                field="space_handles",
                target=handle,
                known=space_handles,
            )
    for space in inventory.spaces:
        check(
            owner_type="space",
            owner_handle=space.handle,
            owner_name=space.name,
            field="story_handle",
            target=space.story_handle,
            known=story_handles,
        )
        check(
            owner_type="space",
            owner_handle=space.handle,
            owner_name=space.name,
            field="thermal_zone_handle",
            target=space.thermal_zone_handle,
            known=zone_handles,
        )
        for handle in space.surface_handles:
            check(
                owner_type="space",
                owner_handle=space.handle,
                owner_name=space.name,
                field="surface_handles",
                target=handle,
                known=surface_handles,
            )
    for surface in inventory.surfaces:
        check(
            owner_type="surface",
            owner_handle=surface.handle,
            owner_name=surface.name,
            field="space_handle",
            target=surface.space_handle,
            known=space_handles,
        )
        check(
            owner_type="surface",
            owner_handle=surface.handle,
            owner_name=surface.name,
            field="adjacent_surface_handle",
            target=surface.adjacent_surface_handle,
            known=surface_handles,
        )
        for handle in surface.subsurface_handles:
            check(
                owner_type="surface",
                owner_handle=surface.handle,
                owner_name=surface.name,
                field="subsurface_handles",
                target=handle,
                known=subsurface_handles,
            )
    for subsurface in inventory.subsurfaces:
        check(
            owner_type="subsurface",
            owner_handle=subsurface.handle,
            owner_name=subsurface.name,
            field="surface_handle",
            target=subsurface.surface_handle,
            known=surface_handles,
        )
    return findings


def _nonreciprocal_findings(inventory: ModelInventory) -> list[Finding]:
    findings: list[Finding] = []
    stories = {record.handle: record for record in inventory.stories}
    zones = {record.handle: record for record in inventory.thermal_zones}
    spaces = {record.handle: record for record in inventory.spaces}
    surfaces = {record.handle: record for record in inventory.surfaces}
    subsurfaces = {record.handle: record for record in inventory.subsurfaces}

    def add(owner: Any, owner_type: FindingObjectType, field: str, related: str) -> None:
        findings.append(
            _finding(
                code="integrity.relationship.nonreciprocal",
                severity="blocker",
                message=f"{field} is not reciprocated by the related object.",
                object_type=owner_type,
                object_handle=owner.handle,
                object_name=owner.name,
                related_handles=[related],
                evidence={"field": field, "related_handle": related},
                suggested_action="Reconcile both sides of the model relationship.",
            )
        )

    for space in inventory.spaces:
        if space.story_handle in stories and space.handle not in stories[space.story_handle].space_handles:
            add(space, "space", "story_handle", space.story_handle)
        if space.thermal_zone_handle in zones and space.handle not in zones[space.thermal_zone_handle].space_handles:
            add(space, "space", "thermal_zone_handle", space.thermal_zone_handle)
        for handle in space.surface_handles:
            if handle in surfaces and surfaces[handle].space_handle != space.handle:
                add(space, "space", "surface_handles", handle)
    for story in inventory.stories:
        for handle in story.space_handles:
            if handle in spaces and spaces[handle].story_handle != story.handle:
                add(story, "building_story", "space_handles", handle)
    for zone in inventory.thermal_zones:
        for handle in zone.space_handles:
            if handle in spaces and spaces[handle].thermal_zone_handle != zone.handle:
                add(zone, "thermal_zone", "space_handles", handle)
    for surface in inventory.surfaces:
        if surface.space_handle in spaces and surface.handle not in spaces[surface.space_handle].surface_handles:
            add(surface, "surface", "space_handle", surface.space_handle)
        if surface.adjacent_surface_handle in surfaces:
            adjacent = surfaces[surface.adjacent_surface_handle]
            if adjacent.adjacent_surface_handle != surface.handle:
                add(surface, "surface", "adjacent_surface_handle", adjacent.handle)
        for handle in surface.subsurface_handles:
            if handle in subsurfaces and subsurfaces[handle].surface_handle != surface.handle:
                add(surface, "surface", "subsurface_handles", handle)
    for subsurface in inventory.subsurfaces:
        if (
            subsurface.surface_handle in surfaces
            and subsurface.handle not in surfaces[subsurface.surface_handle].subsurface_handles
        ):
            add(subsurface, "subsurface", "surface_handle", subsurface.surface_handle)
    return findings


def _name_findings(inventory: ModelInventory) -> list[Finding]:
    findings: list[Finding] = []
    collections: list[tuple[FindingObjectType, list[Any]]] = [
        ("building_story", list(inventory.stories)),
        ("space", list(inventory.spaces)),
        ("thermal_zone", list(inventory.thermal_zones)),
        ("surface", list(inventory.surfaces)),
        ("subsurface", list(inventory.subsurfaces)),
    ]
    for object_type, records in collections:
        grouped: defaultdict[str, list[Any]] = defaultdict(list)
        for record in records:
            if record.name is None or not record.name.strip():
                findings.append(
                    _finding(
                        code="integrity.name.missing",
                        severity="minor",
                        message=f"{object_type} has no visible name.",
                        object_type=object_type,
                        object_handle=record.handle,
                        object_name=record.name,
                        suggested_action="Assign a traceable visible name.",
                    )
                )
            else:
                grouped[record.name.strip().casefold()].append(record)
        for duplicates in grouped.values():
            if len(duplicates) > 1:
                ordered = sorted(duplicates, key=lambda record: record.handle)
                severity: FindingSeverity = "major" if object_type in {"space", "thermal_zone"} else "minor"
                findings.append(
                    _finding(
                        code="integrity.name.duplicate",
                        severity=severity,
                        message=f"{len(ordered)} {object_type} objects share the same visible name.",
                        object_type=object_type,
                        object_handle=ordered[0].handle,
                        object_name=ordered[0].name,
                        related_handles=[record.handle for record in ordered[1:]],
                        evidence={"duplicate_name": ordered[0].name, "count": len(ordered)},
                        suggested_action="Assign unique visible names or register a justified exception.",
                    )
                )
    return findings


def _geometry_findings(inventory: ModelInventory) -> list[Finding]:
    findings: list[Finding] = []
    for space in inventory.spaces:
        if space.floor_area_m2 <= 0:
            findings.append(
                _finding(
                    code="integrity.geometry.nonpositive_space_area",
                    severity="major",
                    message="Space floor area is not positive.",
                    object_type="space",
                    object_handle=space.handle,
                    object_name=space.name,
                    evidence={"floor_area_m2": space.floor_area_m2},
                    suggested_action="Inspect the Space floor geometry.",
                )
            )
        if space.volume_m3 <= 0:
            findings.append(
                _finding(
                    code="integrity.geometry.nonpositive_space_volume",
                    severity="major",
                    message="Space volume is not positive.",
                    object_type="space",
                    object_handle=space.handle,
                    object_name=space.name,
                    evidence={"volume_m3": space.volume_m3},
                    suggested_action="Inspect Space height and enclosure geometry.",
                )
            )
    surfaces = {record.handle: record for record in inventory.surfaces}
    subsurfaces_by_surface: defaultdict[str, list[Any]] = defaultdict(list)
    for surface in inventory.surfaces:
        if len(surface.vertices) < 3 or surface.gross_area_m2 <= 0:
            findings.append(
                _finding(
                    code="integrity.geometry.invalid_surface_polygon",
                    severity="blocker",
                    message="Surface polygon or gross area is invalid.",
                    object_type="surface",
                    object_handle=surface.handle,
                    object_name=surface.name,
                    evidence={"vertex_count": len(surface.vertices), "gross_area_m2": surface.gross_area_m2},
                    suggested_action="Repair the Surface geometry before release.",
                )
            )
    for subsurface in inventory.subsurfaces:
        if subsurface.surface_handle in surfaces:
            subsurfaces_by_surface[subsurface.surface_handle].append(subsurface)
        if len(subsurface.vertices) < 3 or subsurface.gross_area_m2 <= 0:
            findings.append(
                _finding(
                    code="integrity.geometry.invalid_subsurface_polygon",
                    severity="major",
                    message="SubSurface polygon or gross area is invalid.",
                    object_type="subsurface",
                    object_handle=subsurface.handle,
                    object_name=subsurface.name,
                    evidence={
                        "vertex_count": len(subsurface.vertices),
                        "gross_area_m2": subsurface.gross_area_m2,
                    },
                    suggested_action="Repair or remove the invalid SubSurface.",
                )
            )
    for surface_handle, children in subsurfaces_by_surface.items():
        surface = surfaces[surface_handle]
        child_area = sum(child.gross_area_m2 * child.multiplier for child in children)
        tolerance = max(AREA_ABSOLUTE_TOLERANCE_M2, surface.gross_area_m2 * AREA_RELATIVE_TOLERANCE)
        if child_area - surface.gross_area_m2 > tolerance:
            findings.append(
                _finding(
                    code="integrity.geometry.subsurface_exceeds_surface",
                    severity="major",
                    message="Aggregated SubSurface area exceeds the parent Surface area.",
                    object_type="surface",
                    object_handle=surface.handle,
                    object_name=surface.name,
                    related_handles=[child.handle for child in children],
                    evidence={
                        "surface_gross_area_m2": surface.gross_area_m2,
                        "subsurface_gross_area_m2": child_area,
                        "tolerance_m2": tolerance,
                    },
                    suggested_action="Inspect opening geometry and multipliers.",
                )
            )
    return findings


def validate_inventory_integrity(inventory: ModelInventory) -> list[Finding]:
    """Return deterministic project-independent integrity findings."""
    return sort_findings(
        _unresolved_reference_findings(inventory)
        + _nonreciprocal_findings(inventory)
        + _name_findings(inventory)
        + _geometry_findings(inventory)
    )
