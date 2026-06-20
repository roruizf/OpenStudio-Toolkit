"""R2F geometry-phase spatial assignment checks over canonical inventory."""

from __future__ import annotations

from openstudio_toolkit.schemas.findings import Finding, FindingObjectType, FindingSeverity, sort_findings
from openstudio_toolkit.schemas.inventory import ModelInventory


def _finding(
    *,
    code: str,
    severity: FindingSeverity,
    message: str,
    object_type: FindingObjectType,
    object_handle: str,
    object_name: str | None,
    suggested_action: str,
) -> Finding:
    return Finding(
        code=code,
        severity=severity,
        message=message,
        object_type=object_type,
        object_handle=object_handle,
        object_name=object_name,
        evidence={},
        suggested_action=suggested_action,
    )


def validate_spatial_assignments(inventory: ModelInventory) -> list[Finding]:
    """Return deterministic R2F geometry-phase assignment findings."""
    findings: list[Finding] = []
    for space in inventory.spaces:
        if space.story_handle is None:
            findings.append(
                _finding(
                    code="spatial.space.missing_story",
                    severity="major",
                    message="Space has no BuildingStory assignment.",
                    object_type="space",
                    object_handle=space.handle,
                    object_name=space.name,
                    suggested_action="Assign the Space to its expected BuildingStory or approve an exception.",
                )
            )
        if space.thermal_zone_handle is None:
            findings.append(
                _finding(
                    code="spatial.space.missing_thermal_zone",
                    severity="major",
                    message="Space has no candidate ThermalZone assignment.",
                    object_type="space",
                    object_handle=space.handle,
                    object_name=space.name,
                    suggested_action="Assign a candidate ThermalZone or record an approved exception.",
                )
            )
        if not space.surface_handles:
            findings.append(
                _finding(
                    code="spatial.space.no_surfaces",
                    severity="blocker",
                    message="Space contains no Surfaces.",
                    object_type="space",
                    object_handle=space.handle,
                    object_name=space.name,
                    suggested_action="Create or repair the Space enclosure geometry.",
                )
            )
    for surface in inventory.surfaces:
        if surface.space_handle is None:
            findings.append(
                _finding(
                    code="spatial.surface.missing_space",
                    severity="major",
                    message="Surface is not assigned to a Space.",
                    object_type="surface",
                    object_handle=surface.handle,
                    object_name=surface.name,
                    suggested_action="Assign the Surface to its owning Space or remove orphan geometry.",
                )
            )
    for subsurface in inventory.subsurfaces:
        if subsurface.surface_handle is None:
            findings.append(
                _finding(
                    code="spatial.subsurface.missing_surface",
                    severity="major",
                    message="SubSurface is not assigned to a parent Surface.",
                    object_type="subsurface",
                    object_handle=subsurface.handle,
                    object_name=subsurface.name,
                    suggested_action="Assign the SubSurface to its parent Surface or remove orphan geometry.",
                )
            )
    for zone in inventory.thermal_zones:
        if not zone.space_handles:
            findings.append(
                _finding(
                    code="spatial.thermal_zone.no_spaces",
                    severity="observation",
                    message="ThermalZone contains no Spaces.",
                    object_type="thermal_zone",
                    object_handle=zone.handle,
                    object_name=zone.name,
                    suggested_action="Review whether the empty ThermalZone should remain in the model.",
                )
            )
    for story in inventory.stories:
        if not story.space_handles:
            findings.append(
                _finding(
                    code="spatial.story.no_spaces",
                    severity="observation",
                    message="BuildingStory contains no Spaces.",
                    object_type="building_story",
                    object_handle=story.handle,
                    object_name=story.name,
                    suggested_action="Review whether the empty BuildingStory should remain in the model.",
                )
            )
    return sort_findings(findings)
