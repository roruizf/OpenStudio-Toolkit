"""Tests for the TaskResult and ValidationResult schemas."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from openstudio_toolkit.schemas.results import TaskResult, ValidationResult


class TestValidationResult:
    def test_valid_ready(self):
        v = ValidationResult(status="READY", messages=["All checks passed."])
        assert v.status == "READY"
        assert len(v.messages) == 1

    def test_valid_skip(self):
        v = ValidationResult(status="SKIP")
        assert v.messages == []

    def test_valid_error(self):
        v = ValidationResult(status="ERROR", messages=["Model has no spaces."])
        assert v.status == "ERROR"

    def test_invalid_status(self):
        with pytest.raises(ValidationError):
            ValidationResult(status="INVALID")


class TestTaskResult:
    def test_success(self):
        r = TaskResult(status="SUCCESS", task_name="normalize_space_names", updated_count=10)
        assert r.status == "SUCCESS"
        assert r.updated_count == 10
        assert r.errors == 0

    def test_partial_success(self):
        r = TaskResult(status="PARTIAL_SUCCESS", updated_count=5, errors=2, messages=["warn1", "warn2"])
        assert r.errors == 2
        assert len(r.messages) == 2

    def test_from_legacy_dict(self):
        legacy = {
            "status": "SUCCESS",
            "updated_count": 8,
            "errors": 0,
            "messages": ["All spaces updated."],
        }
        r = TaskResult.from_legacy_dict(legacy, task_name="update_spaces")
        assert r.task_name == "update_spaces"
        assert r.updated_count == 8

    def test_from_legacy_dict_with_assigned_count(self):
        legacy = {
            "status": "PARTIAL_SUCCESS",
            "assigned_count": 5,
            "errors": 1,
            "messages": [],
        }
        r = TaskResult.from_legacy_dict(legacy)
        assert r.updated_count == 5

    def test_defaults(self):
        r = TaskResult(status="ERROR")
        assert r.task_name == ""
        assert r.updated_count == 0
        assert r.errors == 0
        assert r.messages == []
        assert r.duration_seconds is None

    def test_invalid_status(self):
        with pytest.raises(ValidationError):
            TaskResult(status="UNKNOWN")
