"""Verified OpenStudio runtime profile for controlled toolkit execution."""

from __future__ import annotations

import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

REFERENCE_PYTHON_MINOR = (3, 13)
# Python 3.14 segfaults in the OpenStudio binding (measured 2026-06-20 with Python 3.14.1; see AGENTS.md, Runtime).
SUPPORTED_PYTHON_MINORS = ((3, 11), (3, 12), (3, 13))
REFERENCE_OPENSTUDIO_VERSION = "3.11.0"
REFERENCE_ENERGYPLUS_VERSION = "25.2.0"


class RuntimeMismatchError(RuntimeError):
    """Raised when execution does not match the verified runtime profile."""


@dataclass(frozen=True)
class RuntimeInfo:
    """Observed versions and paths for the active OpenStudio binding."""

    python_version: str
    python_executable: str
    openstudio_version: str
    energyplus_version: str
    openstudio_module_path: str

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible runtime record."""
        return asdict(self)


def inspect_runtime() -> RuntimeInfo:
    """Inspect the active interpreter and OpenStudio binding."""
    try:
        import openstudio
    except ImportError as exc:
        raise RuntimeMismatchError(
            "OpenStudio is not importable. Run this project through the uv-managed environment."
        ) from exc

    return RuntimeInfo(
        python_version=".".join(str(part) for part in sys.version_info[:3]),
        python_executable=str(Path(sys.executable).resolve()),
        openstudio_version=openstudio.openStudioVersion(),
        energyplus_version=openstudio.energyPlusVersion(),
        openstudio_module_path=str(Path(openstudio.__file__).resolve()),
    )


def assert_reference_runtime(runtime: RuntimeInfo | None = None) -> RuntimeInfo:
    """Return runtime facts or fail when the reference profile is not active."""
    observed = runtime or inspect_runtime()
    mismatches: list[str] = []

    python_minor = tuple(int(part) for part in observed.python_version.split(".")[:2])
    if python_minor not in SUPPORTED_PYTHON_MINORS:
        supported = ", ".join(f"{major}.{minor}" for major, minor in SUPPORTED_PYTHON_MINORS)
        mismatches.append(f"Python {observed.python_version} (expected one of {supported})")
    if observed.openstudio_version != REFERENCE_OPENSTUDIO_VERSION:
        mismatches.append(
            f"OpenStudio {observed.openstudio_version} (expected {REFERENCE_OPENSTUDIO_VERSION})"
        )
    if observed.energyplus_version != REFERENCE_ENERGYPLUS_VERSION:
        mismatches.append(
            f"EnergyPlus {observed.energyplus_version} (expected {REFERENCE_ENERGYPLUS_VERSION})"
        )

    if mismatches:
        raise RuntimeMismatchError("Reference runtime mismatch: " + "; ".join(mismatches))

    return observed
