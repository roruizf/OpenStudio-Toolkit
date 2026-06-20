"""Portable semantic report for geometry inventory validation."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from openstudio_toolkit.schemas.findings import Finding, ProfileStatus, sort_findings

REPORT_SCHEMA_VERSION: Literal["0.1.0"] = "0.1.0"
VALIDATOR_SUITE: Literal["geometry-inventory"] = "geometry-inventory"
VALIDATOR_SUITE_VERSION: Literal["0.1.0"] = "0.1.0"
ValidationCheck = Literal["integrity", "spatial", "naming"]


class GeometryValidationReport(BaseModel):
    """Deterministic validation facts linked to one semantic inventory."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["0.1.0"] = REPORT_SCHEMA_VERSION
    inventory_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    validator_suite: Literal["geometry-inventory"] = VALIDATOR_SUITE
    validator_suite_version: Literal["0.1.0"] = VALIDATOR_SUITE_VERSION
    checks_run: list[ValidationCheck]
    naming_profile_id: str | None = None
    naming_profile_version: str | None = None
    naming_profile_status: ProfileStatus | None = None
    findings: list[Finding] = Field(default_factory=list)

    @field_validator("checks_run")
    @classmethod
    def normalize_checks(cls, checks: list[ValidationCheck]) -> list[ValidationCheck]:
        order: dict[ValidationCheck, int] = {"integrity": 0, "spatial": 1, "naming": 2}
        return sorted(set(checks), key=order.__getitem__)

    @field_validator("findings")
    @classmethod
    def normalize_findings(cls, findings: list[Finding]) -> list[Finding]:
        return sort_findings(findings)

    @model_validator(mode="after")
    def naming_identity_matches_checks(self) -> GeometryValidationReport:
        if not {"integrity", "spatial"}.issubset(self.checks_run):
            raise ValueError("geometry validation reports require integrity and spatial checks")
        identity = (
            self.naming_profile_id,
            self.naming_profile_version,
            self.naming_profile_status,
        )
        if "naming" in self.checks_run:
            if any(value is None for value in identity):
                raise ValueError("naming profile identity is required when naming was run")
            for finding in self.findings:
                if finding.code.startswith("naming.") and (
                    finding.profile_id != self.naming_profile_id
                    or finding.profile_version != self.naming_profile_version
                ):
                    raise ValueError("naming finding profile identity does not match report")
        elif any(value is not None for value in identity):
            raise ValueError("naming profile identity requires the naming check")
        elif any(finding.code.startswith("naming.") for finding in self.findings):
            raise ValueError("naming findings require the naming check")
        return self


@dataclass(frozen=True, slots=True)
class ValidationArtifact:
    content: bytes
    sha256: str


def _canonical_json(value: object) -> str:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def serialize_validation_report(report: GeometryValidationReport) -> ValidationArtifact:
    """Serialize and hash a report without writing it."""
    content = _canonical_json(report.model_dump(mode="json")).encode("utf-8")
    return ValidationArtifact(content=content, sha256=hashlib.sha256(content).hexdigest())


def render_validation_report_markdown(report: GeometryValidationReport) -> str:
    """Render a deterministic human projection of a validation report."""
    counts = {severity: 0 for severity in ("blocker", "major", "minor", "observation")}
    for finding in report.findings:
        counts[finding.severity] += 1

    profile = "Naming not run"
    if "naming" in report.checks_run:
        profile = (
            f"{report.naming_profile_id}@{report.naming_profile_version} "
            f"({report.naming_profile_status})"
        )
    lines = [
        "# Geometry Validation Report",
        "",
        f"- Inventory SHA-256: `{report.inventory_sha256}`",
        f"- Validator suite: `{report.validator_suite}@{report.validator_suite_version}`",
        f"- Checks run: `{', '.join(report.checks_run)}`",
        f"- Naming profile: {profile}",
        "",
        "## Summary",
        "",
        f"- Blocker: {counts['blocker']}",
        f"- Major: {counts['major']}",
        f"- Minor: {counts['minor']}",
        f"- Observation: {counts['observation']}",
        "",
        "## Findings",
    ]
    if not report.findings:
        lines.extend(["", "No findings."])
    for index, finding in enumerate(report.findings, start=1):
        lines.extend(
            [
                "",
                f"### {index}. `{finding.code}`",
                "",
                f"- Severity: `{finding.severity}`",
                f"- Object: `{finding.object_type}` / `{finding.object_name or ''}` / `{finding.object_handle or ''}`",
                f"- Message: {finding.message}",
                f"- Related handles: `{_canonical_json(finding.related_handles)}`",
                f"- Evidence: `{_canonical_json(finding.evidence)}`",
                f"- Suggested action: {finding.suggested_action or ''}",
            ]
        )
    return "\n".join(lines) + "\n"
