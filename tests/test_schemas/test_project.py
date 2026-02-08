"""Tests for the ProjectSpec and TaskStep schemas."""

from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from openstudio_toolkit.schemas.project import ProjectSpec, TaskStep


class TestTaskStep:
    def test_minimal(self):
        step = TaskStep(task="model_setup.normalize_space_names")
        assert step.task == "model_setup.normalize_space_names"
        assert step.params == {}
        assert step.skip_if is None

    def test_with_params(self):
        step = TaskStep(
            task="simulation_setup.set_output_variables",
            params={"frequency": "hourly", "variables": ["Zone Mean Air Temperature"]},
        )
        assert step.params["frequency"] == "hourly"

    def test_with_skip_condition(self):
        step = TaskStep(task="model_qa_qc.calculate_wwr", skip_if="no_windows")
        assert step.skip_if == "no_windows"


class TestProjectSpec:
    def test_minimal(self):
        spec = ProjectSpec(
            name="Test Project",
            model_path=Path("data/models/test.osm"),
        )
        assert spec.name == "Test Project"
        assert spec.version == "1.0"
        assert spec.weather_path is None
        assert spec.pipeline == []
        assert spec.outputs == {}

    def test_full(self):
        spec = ProjectSpec(
            name="R2F-Office-Hub",
            version="2.0",
            model_path=Path("data/models/R2F-Office-Hub_v003.osm"),
            weather_path=Path("data/weather/budapest.epw"),
            pipeline=[
                TaskStep(task="model_setup.normalize_space_names"),
                TaskStep(task="model_setup.rename_surfaces_based_on_space_names"),
                TaskStep(
                    task="model_qa_qc.calculate_wwr_by_space",
                    params={"output_path": "reports/wwr.xlsx"},
                ),
            ],
            outputs={"wwr_report": Path("data/reports/wwr.xlsx")},
        )
        assert len(spec.pipeline) == 3
        assert spec.pipeline[2].params["output_path"] == "reports/wwr.xlsx"
        assert "wwr_report" in spec.outputs

    def test_missing_required_fields(self):
        with pytest.raises(ValidationError):
            ProjectSpec(version="1.0")  # Missing name and model_path

    def test_from_dict(self):
        data = {
            "name": "Test",
            "model_path": "models/test.osm",
            "pipeline": [
                {"task": "model_setup.normalize_space_names"},
            ],
        }
        spec = ProjectSpec.model_validate(data)
        assert spec.name == "Test"
        assert len(spec.pipeline) == 1
