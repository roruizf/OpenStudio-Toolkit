"""P1 acceptance tests for the verified OpenStudio runtime."""

from __future__ import annotations

import hashlib
from pathlib import Path

import openstudio
import pytest

from openstudio_toolkit.runtime import (
    SUPPORTED_PYTHON_MINORS,
    RuntimeInfo,
    RuntimeMismatchError,
    assert_reference_runtime,
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_reference_runtime_is_active() -> None:
    runtime = assert_reference_runtime()

    assert tuple(int(part) for part in runtime.python_version.split(".")[:2]) in SUPPORTED_PYTHON_MINORS
    assert runtime.openstudio_version == "3.11.0"
    assert runtime.energyplus_version == "25.2.0"
    assert "site-packages/openstudio" in runtime.openstudio_module_path


def test_runtime_mismatch_fails_loudly() -> None:
    ambient_mismatch = RuntimeInfo(
        python_version="3.8.12",
        python_executable="/ambient/python3",
        openstudio_version="3.6.1",
        energyplus_version="23.1.0",
        openstudio_module_path="/ambient/site-packages/openstudio/__init__.py",
    )

    with pytest.raises(RuntimeMismatchError, match="Reference runtime mismatch"):
        assert_reference_runtime(ambient_mismatch)


def test_binding_loads_fixture_without_modifying_source() -> None:
    fixture = Path(__file__).resolve().parents[1] / "resources" / "small_office.osm"
    before = _sha256(fixture)

    loaded_model = openstudio.osversion.VersionTranslator().loadModel(str(fixture))

    assert loaded_model.is_initialized()
    assert len(loaded_model.get().getSpaces()) == 6
    assert _sha256(fixture) == before
