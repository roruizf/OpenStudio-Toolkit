# Reference Runtime Profile

Status: Verified for toolkit Python operations
Verified: 2026-06-20

## Profile

| Component | Version |
|---|---|
| Python | 3.13.x |
| OpenStudio Python wheel | 3.10.0 |
| EnergyPlus reported by binding | 25.1.0 |
| Environment manager | uv |

OpenStudio is installed from the pinned PyPI wheel through `uv`. Controlled toolkit execution must call `assert_reference_runtime()` before loading project inputs.

```bash
uv sync --dev
uv run python -c "from openstudio_toolkit.runtime import assert_reference_runtime; print(assert_reference_runtime())"
```

## P1 Evidence

OpenStudio and the Python dependencies were compared under CPython 3.10.19, 3.12.7, 3.13.10, and 3.14.1. Python 3.10, 3.12, and 3.13 imported the binding and loaded the fixture successfully. Python 3.14.1 could import the module but exited with `SIGSEGV` (`139`) when constructing `openstudio.model.Model` or `VersionTranslator`. Python 3.13 is therefore the newest tested stable version compatible with the OpenStudio 3.10.0 native binding.

The final profile was proven with a CPython 3.13.10 uv environment:

- The imported module resolved inside the uv environment, not the ambient Anaconda interpreter.
- `openstudio.openStudioVersion()` returned `3.10.0`.
- `openstudio.energyPlusVersion()` returned `25.1.0`.
- `tests/resources/small_office.osm` loaded successfully with 6 spaces, 6 thermal zones, 43 surfaces, and 23 subsurfaces.
- The fixture SHA-256 remained `eb0fe62b53531d8367ce51627b0c83ea4c7043ef620f6793eb985d835edc3a94` before and after loading.
- A synthetic representation of the known ambient Python 3.8/OpenStudio 3.6.1 stack fails the runtime assertion.
- The locked environment resolved Pandas 3.0.3, Pydantic 2.13.4, OpenPyXL 3.1.5, and pytest 9.1.1.
- The complete baseline and P1 suite passed: 86 tests.

## Boundary

This profile verifies Python SDK operations only. The PyPI wheel did not expose a usable OpenStudio CLI path in this environment: `openstudio.getOpenStudioCLI()` returned `.`. CLI execution, EnergyPlus simulation, measures requiring the CLI, and system OpenStudio installation remain unverified and outside P1.
