"""Profile-driven naming checks over canonical inventory relationships."""

from __future__ import annotations

import re
from typing import Any

from openstudio_toolkit.schemas.findings import (
    Finding,
    FindingObjectType,
    FindingSeverity,
    NamingProfile,
    sort_findings,
)
from openstudio_toolkit.schemas.inventory import ModelInventory

_POSITIVE_SEQUENCE = re.compile(r"[1-9][0-9]*")


def _finding(
    profile: NamingProfile,
    *,
    code: str,
    message: str,
    object_type: FindingObjectType,
    object_handle: str | None,
    object_name: str | None,
    evidence: dict[str, Any],
    suggested_action: str,
    severity: FindingSeverity = "minor",
    related_handles: list[str] | None = None,
) -> Finding:
    return Finding(
        code=code,
        severity=severity,
        message=message,
        object_type=object_type,
        object_handle=object_handle,
        object_name=object_name,
        related_handles=related_handles or [],
        evidence=evidence,
        suggested_action=suggested_action,
        profile_id=profile.profile_id,
        profile_version=profile.version,
    )


def _profile_findings(inventory: ModelInventory, profile: NamingProfile) -> list[Finding]:
    findings: list[Finding] = []
    spaces = {space.handle: space for space in inventory.spaces}
    missing_fields: list[str] = []
    if inventory.spaces and profile.space_pattern is None:
        missing_fields.append("space_pattern")
    resolved_counts = [
        len(zone.space_handles)
        for zone in inventory.thermal_zones
        if zone.space_handles and all(handle in spaces for handle in zone.space_handles)
    ]
    if 1 in resolved_counts and profile.one_to_one_zone_template is None:
        missing_fields.append("one_to_one_zone_template")
    if any(count > 1 for count in resolved_counts) and profile.multi_space_zone_pattern is None:
        missing_fields.append("multi_space_zone_pattern")
    if profile.status == "draft":
        findings.append(
            _finding(
                profile,
                code="naming.profile.draft",
                severity="observation",
                message="Naming validation used a draft profile.",
                object_type="model",
                object_handle=None,
                object_name=inventory.building.name,
                evidence={"profile_status": profile.status},
                suggested_action="Obtain human approval before claiming project naming conformance.",
            )
        )
    if missing_fields:
        findings.append(
            _finding(
                profile,
                code="naming.profile.incomplete",
                severity="observation",
                message="The naming profile lacks grammar required by this inventory.",
                object_type="model",
                object_handle=None,
                object_name=inventory.building.name,
                evidence={"missing_fields": sorted(missing_fields)},
                suggested_action="Complete and version the project naming profile.",
            )
        )
    return findings


def _space_findings(inventory: ModelInventory, profile: NamingProfile) -> list[Finding]:
    if profile.space_pattern is None:
        return []
    findings: list[Finding] = []
    pattern = re.compile(profile.space_pattern)
    for space in inventory.spaces:
        if space.name and pattern.fullmatch(space.name) is None:
            findings.append(
                _finding(
                    profile,
                    code="naming.space.profile_mismatch",
                    message="Space name does not match the project profile pattern.",
                    object_type="space",
                    object_handle=space.handle,
                    object_name=space.name,
                    evidence={"actual": space.name, "space_pattern": profile.space_pattern},
                    suggested_action="Review the Space name against the approved project grammar.",
                )
            )
    return findings


def _zone_findings(inventory: ModelInventory, profile: NamingProfile) -> list[Finding]:
    findings: list[Finding] = []
    spaces = {space.handle: space for space in inventory.spaces}
    multi_pattern = re.compile(profile.multi_space_zone_pattern) if profile.multi_space_zone_pattern else None
    for zone in inventory.thermal_zones:
        if not zone.name or not zone.space_handles or any(handle not in spaces for handle in zone.space_handles):
            continue
        members = [spaces[handle] for handle in zone.space_handles]
        if any(space.name is None for space in members):
            continue
        if len(members) == 1 and profile.one_to_one_zone_template is not None:
            expected = profile.one_to_one_zone_template.format(space_name=members[0].name)
            if zone.name != expected:
                findings.append(
                    _finding(
                        profile,
                        code="naming.thermal_zone.one_to_one_mismatch",
                        message="One-Space ThermalZone name does not match its Space-derived name.",
                        object_type="thermal_zone",
                        object_handle=zone.handle,
                        object_name=zone.name,
                        related_handles=[members[0].handle],
                        evidence={"actual": zone.name, "expected": expected},
                        suggested_action="Rename the ThermalZone through a reviewed naming change set.",
                    )
                )
        elif len(members) > 1:
            if multi_pattern is None:
                findings.append(
                    _finding(
                        profile,
                        code="naming.thermal_zone.multi_space_rule_missing",
                        severity="observation",
                        message="A multi-Space ThermalZone has no project naming rule.",
                        object_type="thermal_zone",
                        object_handle=zone.handle,
                        object_name=zone.name,
                        related_handles=[space.handle for space in members],
                        evidence={"space_count": len(members)},
                        suggested_action="Define and approve a multi-Space zone grammar.",
                    )
                )
            elif multi_pattern.fullmatch(zone.name) is None:
                findings.append(
                    _finding(
                        profile,
                        code="naming.thermal_zone.multi_space_mismatch",
                        message="Multi-Space ThermalZone name does not match the project pattern.",
                        object_type="thermal_zone",
                        object_handle=zone.handle,
                        object_name=zone.name,
                        related_handles=[space.handle for space in members],
                        evidence={"actual": zone.name, "multi_space_zone_pattern": profile.multi_space_zone_pattern},
                        suggested_action="Review the ThermalZone name against the approved project grammar.",
                    )
                )
    return findings


def _surface_findings(inventory: ModelInventory, profile: NamingProfile) -> list[Finding]:
    findings: list[Finding] = []
    spaces = {space.handle: space for space in inventory.spaces}
    surfaces = {surface.handle: surface for surface in inventory.surfaces}
    separator = profile.surface_separator
    for surface in inventory.surfaces:
        if not surface.name or surface.space_handle not in spaces:
            continue
        owner = spaces[surface.space_handle]
        if not owner.name:
            continue
        relationship = surface.outside_boundary_condition
        related_handles = [owner.handle]
        if surface.adjacent_surface_handle is not None:
            adjacent = surfaces.get(surface.adjacent_surface_handle)
            if adjacent is None or adjacent.space_handle not in spaces:
                continue
            adjacent_space = spaces[adjacent.space_handle]
            if not adjacent_space.name:
                continue
            relationship = adjacent_space.name
            related_handles.extend([adjacent.handle, adjacent_space.handle])
        owner_prefix = f"{owner.name}{separator}"
        base = separator.join((owner.name, surface.surface_type, relationship))
        expected_prefix = f"{base}{separator}" if profile.require_surface_sequence else base
        if not surface.name.startswith(owner_prefix):
            code = "naming.surface.owner_mismatch"
            message = "Surface name does not expose its actual owning Space."
            evidence = {"actual": surface.name, "expected_owner_prefix": owner_prefix}
        elif not surface.name.startswith(expected_prefix):
            code = "naming.surface.relationship_mismatch"
            message = "Surface name does not expose its actual type and boundary relationship."
            evidence = {"actual": surface.name, "expected_prefix": expected_prefix}
        elif profile.require_surface_sequence and _POSITIVE_SEQUENCE.fullmatch(
            surface.name[len(expected_prefix) :]
        ) is None:
            code = "naming.surface.sequence_missing"
            message = "Surface name lacks a required positive sequence."
            evidence = {"actual": surface.name, "expected_prefix": expected_prefix}
        elif not profile.require_surface_sequence and surface.name != base:
            code = "naming.surface.relationship_mismatch"
            message = "Surface name contains content beyond the derived relationship name."
            evidence = {"actual": surface.name, "expected": base}
        else:
            continue
        findings.append(
            _finding(
                profile,
                code=code,
                message=message,
                object_type="surface",
                object_handle=surface.handle,
                object_name=surface.name,
                related_handles=related_handles,
                evidence=evidence,
                suggested_action="Preview a relationship-derived Surface rename for human review.",
            )
        )
    return findings


def _subsurface_findings(inventory: ModelInventory, profile: NamingProfile) -> list[Finding]:
    findings: list[Finding] = []
    surfaces = {surface.handle: surface for surface in inventory.surfaces}
    separator = profile.subsurface_separator
    for subsurface in inventory.subsurfaces:
        if not subsurface.name or subsurface.surface_handle not in surfaces:
            continue
        parent = surfaces[subsurface.surface_handle]
        if not parent.name:
            continue
        parent_prefix = f"{parent.name}{separator}"
        base = separator.join((parent.name, subsurface.subsurface_type))
        expected_prefix = f"{base}{separator}" if profile.require_subsurface_sequence else base
        if not subsurface.name.startswith(parent_prefix):
            code = "naming.subsurface.parent_mismatch"
            message = "SubSurface name does not inherit its actual parent Surface name."
            evidence = {"actual": subsurface.name, "expected_parent_prefix": parent_prefix}
        elif profile.require_subsurface_sequence and (
            not subsurface.name.startswith(expected_prefix)
            or _POSITIVE_SEQUENCE.fullmatch(subsurface.name[len(expected_prefix) :]) is None
        ):
            code = "naming.subsurface.type_or_sequence_mismatch"
            message = "SubSurface type or required sequence does not match the derived name."
            evidence = {"actual": subsurface.name, "expected_prefix": expected_prefix}
        elif not profile.require_subsurface_sequence and subsurface.name != base:
            code = "naming.subsurface.type_or_sequence_mismatch"
            message = "SubSurface name differs from its derived parent and type name."
            evidence = {"actual": subsurface.name, "expected": base}
        else:
            continue
        findings.append(
            _finding(
                profile,
                code=code,
                message=message,
                object_type="subsurface",
                object_handle=subsurface.handle,
                object_name=subsurface.name,
                related_handles=[parent.handle],
                evidence=evidence,
                suggested_action="Preview a parent-derived SubSurface rename for human review.",
            )
        )
    return findings


def validate_model_object_naming(inventory: ModelInventory, profile: NamingProfile) -> list[Finding]:
    """Return deterministic profile-driven naming findings."""
    return sort_findings(
        _profile_findings(inventory, profile)
        + _space_findings(inventory, profile)
        + _zone_findings(inventory, profile)
        + _surface_findings(inventory, profile)
        + _subsurface_findings(inventory, profile)
    )
