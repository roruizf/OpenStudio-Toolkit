"""Shared pytest fixtures for the OpenStudio Toolkit test suite.

Fixtures use ``scope="session"`` to load OSM models only once per test run,
since model loading via VersionTranslator is expensive (~1-2s per file).
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest


def _find_osm(relative_path: str) -> Path:
    """Resolve an OSM file path relative to the toolkit root."""
    base_dir = Path(__file__).resolve().parent.parent
    path = base_dir / relative_path
    if path.exists():
        return path
    raise FileNotFoundError(f"OSM file not found at {path}")


@pytest.fixture(scope="session")
def small_office_model():
    """Small office model for fast unit tests."""
    import openstudio

    osm_path = _find_osm("tests/resources/small_office.osm")
    vt = openstudio.osversion.VersionTranslator()
    optional_m = vt.loadModel(str(osm_path))
    if optional_m.isNull():
        pytest.skip(f"Could not load model at {osm_path}")
    return optional_m.get()


@pytest.fixture(scope="session")
def office_hub_model():
    """R2F Office Hub model for integration tests.

    This is a larger model with spaces, zones, HVAC, materials, etc.
    Skipped if the file is not present (it lives in examples/).
    """
    import openstudio

    try:
        osm_path = _find_osm("examples/R2F-Office-Hub.osm")
    except FileNotFoundError:
        pytest.skip("R2F-Office-Hub.osm not available")
        return None

    vt = openstudio.osversion.VersionTranslator()
    optional_m = vt.loadModel(str(osm_path))
    if optional_m.isNull():
        pytest.skip(f"Could not load model at {osm_path}")
    return optional_m.get()


@pytest.fixture(scope="session")
def empty_model():
    """An empty OpenStudio model for edge-case testing."""
    import openstudio

    return openstudio.model.Model()
