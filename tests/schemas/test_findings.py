"""Contract tests for deterministic P3 findings."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from openstudio_toolkit.schemas import Finding, NamingProfile, sort_findings


def _finding(**changes: object) -> Finding:
    data: dict[str, object] = {
        "code": "integrity.reference.unresolved",
        "severity": "blocker",
        "message": "A reference is unresolved.",
        "object_type": "space",
        "object_handle": "space-1",
        "object_name": "Space 1",
        "related_handles": ["surface-2", "surface-1", "surface-1"],
        "evidence": {"field": "surface_handles"},
        "suggested_action": None,
        "profile_id": None,
        "profile_version": None,
    }
    data.update(changes)
    return Finding.model_validate(data)


@pytest.mark.parametrize(
    ("field", "value"),
    [("severity", "critical"), ("object_type", "space_type")],
)
def test_finding_rejects_unknown_enums(field: str, value: str) -> None:
    with pytest.raises(ValidationError):
        _finding(**{field: value})


def test_finding_rejects_extra_fields() -> None:
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        _finding(disposition="accepted")


def test_related_handles_are_sorted_and_unique() -> None:
    assert _finding().related_handles == ["surface-1", "surface-2"]


def test_profile_identity_must_be_complete() -> None:
    with pytest.raises(ValidationError, match="must be supplied together"):
        _finding(profile_id="east-gate")


def test_naming_profile_validates_regex_and_zone_template() -> None:
    with pytest.raises(ValidationError, match="invalid naming regex"):
        NamingProfile(profile_id="test", version="1", status="draft", space_pattern="[")
    with pytest.raises(ValidationError, match="must use only"):
        NamingProfile(
            profile_id="test",
            version="1",
            status="approved",
            one_to_one_zone_template="TZ-{zone_name}",
        )


@pytest.mark.parametrize("field", ["surface_separator", "subsurface_separator"])
def test_naming_profile_rejects_empty_separators(field: str) -> None:
    with pytest.raises(ValidationError, match="at least 1 character"):
        NamingProfile.model_validate({"profile_id": "test", "version": "1", "status": "draft", field: ""})


@pytest.mark.parametrize("template", ["TZ-{space_name}-{zone_name}", "TZ-{space_name!r}"])
def test_zone_template_rejects_unsupported_fields_and_conversions(template: str) -> None:
    with pytest.raises(ValidationError):
        NamingProfile(
            profile_id="test",
            version="1",
            status="approved",
            one_to_one_zone_template=template,
        )


def test_finding_order_is_deterministic_and_severity_first() -> None:
    findings = [
        _finding(code="spatial.story.no_spaces", severity="observation", object_handle="story-1"),
        _finding(code="integrity.name.duplicate", severity="major", object_handle="space-2"),
        _finding(code="integrity.name.duplicate", severity="major", object_handle="space-1"),
    ]

    assert [finding.object_handle for finding in sort_findings(findings)] == [
        "space-1",
        "space-2",
        "story-1",
    ]
