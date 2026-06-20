"""Composition of pure geometry inventory validators."""

from __future__ import annotations

import json

from openstudio_toolkit.schemas.findings import Finding, NamingProfile, sort_findings
from openstudio_toolkit.schemas.inventory import ModelInventory, serialize_inventory
from openstudio_toolkit.schemas.validation import GeometryValidationReport, ValidationCheck
from openstudio_toolkit.validators.integrity import validate_inventory_integrity
from openstudio_toolkit.validators.naming import validate_model_object_naming
from openstudio_toolkit.validators.spatial import validate_spatial_assignments


def _deduplicate(findings: list[Finding]) -> list[Finding]:
    unique: dict[str, Finding] = {}
    for finding in findings:
        key = json.dumps(
            finding.model_dump(mode="json"),
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        unique.setdefault(key, finding)
    return sort_findings(list(unique.values()))


def validate_geometry_inventory(
    inventory: ModelInventory,
    *,
    naming_profile: NamingProfile | None = None,
) -> list[Finding]:
    """Compose geometry validators without implying an omitted check passed."""
    findings = validate_inventory_integrity(inventory) + validate_spatial_assignments(inventory)
    if naming_profile is not None:
        findings += validate_model_object_naming(inventory, naming_profile)
    return _deduplicate(findings)


def build_geometry_validation_report(
    inventory: ModelInventory,
    *,
    naming_profile: NamingProfile | None = None,
) -> GeometryValidationReport:
    """Build portable evidence linked to the canonical semantic inventory."""
    checks: list[ValidationCheck] = ["integrity", "spatial"]
    inventory_sha256 = serialize_inventory(inventory).sha256
    findings = validate_geometry_inventory(inventory, naming_profile=naming_profile)
    if naming_profile is None:
        return GeometryValidationReport(
            inventory_sha256=inventory_sha256,
            checks_run=checks,
            findings=findings,
        )
    checks.append("naming")
    return GeometryValidationReport(
        inventory_sha256=inventory_sha256,
        checks_run=checks,
        naming_profile_id=naming_profile.profile_id,
        naming_profile_version=naming_profile.version,
        naming_profile_status=naming_profile.status,
        findings=findings,
    )
