"""Project specification schema - the core of the spec-driven approach.

A ProjectSpec defines the complete intent for a modeling workflow:
what model to operate on, what tasks to run, and where to put outputs.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class TaskStep(BaseModel):
    """A single step in a project pipeline."""

    task: str = Field(
        ...,
        description="Dotted path to the task module, e.g. 'model_setup.normalize_space_names'.",
    )
    params: dict[str, Any] = Field(
        default_factory=dict,
        description="Keyword arguments passed to the task's run() function.",
    )
    skip_if: str | None = Field(
        default=None,
        description="Optional condition expression. If truthy, this step is skipped.",
    )


class ProjectSpec(BaseModel):
    """Declarative specification for a modeling project.

    This is designed to be serialized as YAML or TOML, allowing users to define
    their intent in a configuration file that the system executes with rigor.

    Example YAML::

        name: R2F-Office-Hub
        version: "1.0"
        model_path: data/models/R2F-Office-Hub_v003.osm
        weather_path: data/weather/budapest.epw
        pipeline:
          - task: model_setup.normalize_space_names
          - task: model_setup.rename_surfaces_based_on_space_names
          - task: model_setup.set_space_surfacearea_height_volume
          - task: model_qa_qc.calculate_wwr_by_space
        outputs:
          wwr_report: data/reports/wwr.xlsx
    """

    name: str = Field(..., description="Human-readable project name.")
    version: str = Field(default="1.0", description="Spec format version.")
    model_path: Path = Field(..., description="Path to the base .osm model file.")
    weather_path: Path | None = Field(default=None, description="Path to the .epw weather file.")
    pipeline: list[TaskStep] = Field(default_factory=list, description="Ordered list of tasks to execute.")
    outputs: dict[str, Path] = Field(default_factory=dict, description="Named output paths (e.g. 'wwr_report': 'path.xlsx').")
