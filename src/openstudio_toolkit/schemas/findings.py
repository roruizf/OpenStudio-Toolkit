"""Structured deterministic findings and project naming profiles."""

from __future__ import annotations

import re
import string
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue, field_validator, model_validator

FindingSeverity = Literal["blocker", "major", "minor", "observation"]
FindingObjectType = Literal[
    "model",
    "building_story",
    "space",
    "thermal_zone",
    "surface",
    "subsurface",
]
ProfileStatus = Literal["draft", "approved"]

_SEVERITY_RANK: dict[FindingSeverity, int] = {
    "blocker": 0,
    "major": 1,
    "minor": 2,
    "observation": 3,
}


class Finding(BaseModel):
    """One revision-scoped technical observation produced by a pure validator."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    code: str = Field(pattern=r"^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)+$")
    severity: FindingSeverity
    message: str = Field(min_length=1)
    object_type: FindingObjectType
    object_handle: str | None
    object_name: str | None
    related_handles: list[str] = Field(default_factory=list)
    evidence: dict[str, JsonValue] = Field(default_factory=dict)
    suggested_action: str | None
    profile_id: str | None = None
    profile_version: str | None = None

    @field_validator("related_handles")
    @classmethod
    def sort_related_handles(cls, handles: list[str]) -> list[str]:
        return sorted(set(handles))

    @model_validator(mode="after")
    def profile_identity_is_complete(self) -> Finding:
        if (self.profile_id is None) != (self.profile_version is None):
            raise ValueError("profile_id and profile_version must be supplied together")
        return self


class NamingProfile(BaseModel):
    """Explicit project grammar for P3.2 naming validation."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    profile_id: str = Field(min_length=1)
    version: str = Field(min_length=1)
    status: ProfileStatus
    space_pattern: str | None = None
    one_to_one_zone_template: str | None = None
    multi_space_zone_pattern: str | None = None
    surface_separator: str = Field(default="_", min_length=1)
    subsurface_separator: str = Field(default="_", min_length=1)
    require_surface_sequence: bool = True
    require_subsurface_sequence: bool = True

    @field_validator("space_pattern", "multi_space_zone_pattern")
    @classmethod
    def patterns_compile(cls, pattern: str | None) -> str | None:
        if pattern is not None:
            try:
                re.compile(pattern)
            except re.error as exc:
                raise ValueError(f"invalid naming regex: {exc}") from exc
        return pattern

    @field_validator("one_to_one_zone_template")
    @classmethod
    def zone_template_references_space(cls, template: str | None) -> str | None:
        if template is not None:
            parsed = list(string.Formatter().parse(template))
            fields = {field_name for _, field_name, _, _ in parsed if field_name is not None}
            if fields != {"space_name"}:
                raise ValueError("one_to_one_zone_template must use only {space_name}")
            if any(
                format_spec or conversion
                for _, field_name, format_spec, conversion in parsed
                if field_name is not None
            ):
                raise ValueError("one_to_one_zone_template does not support conversions or format specs")
        return template


def sort_findings(findings: list[Finding]) -> list[Finding]:
    """Return findings in stable review order without changing their content."""
    return sorted(
        findings,
        key=lambda finding: (
            _SEVERITY_RANK[finding.severity],
            finding.code,
            finding.object_type,
            (finding.object_name or "").casefold(),
            finding.object_handle or "",
        ),
    )
