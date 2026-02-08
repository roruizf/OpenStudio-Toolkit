"""Standardized result schemas for tasks and validations."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class ValidationResult(BaseModel):
    """Result of a task validator() call.

    Every task module exposes a validator() function that returns this structure
    to indicate whether the task can proceed.
    """

    status: Literal["READY", "SKIP", "ERROR"] = Field(
        ..., description="Whether the task is ready to run, should be skipped, or has an error."
    )
    messages: list[str] = Field(default_factory=list, description="Human-readable validation messages.")


class TaskResult(BaseModel):
    """Standardized result returned by task run() functions and batch update operations.

    All update/mutation operations in osm_objects and tasks return this structure.
    """

    status: Literal["SUCCESS", "PARTIAL_SUCCESS", "SKIP", "ERROR"] = Field(
        ..., description="Overall outcome of the operation."
    )
    task_name: str = Field(default="", description="Qualified name of the task that produced this result.")
    updated_count: int = Field(default=0, description="Number of objects successfully modified.")
    errors: int = Field(default=0, description="Number of objects that failed to update.")
    messages: list[str] = Field(default_factory=list, description="Detailed per-object messages (warnings, errors).")
    duration_seconds: float | None = Field(default=None, description="Wall-clock time for the operation.")

    @classmethod
    def from_legacy_dict(cls, d: dict, task_name: str = "") -> TaskResult:
        """Create a TaskResult from the legacy dict format used by existing osm_objects update functions.

        Existing code returns: {"status": ..., "updated_count": ..., "errors": ..., "messages": [...]}
        This factory adapts that format to the new schema.
        """
        return cls(
            status=d.get("status", "ERROR"),
            task_name=task_name,
            updated_count=d.get("updated_count", d.get("assigned_count", 0)),
            errors=d.get("errors", 0),
            messages=d.get("messages", []),
        )
