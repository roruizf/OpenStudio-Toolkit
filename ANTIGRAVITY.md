# Antigravity Project Guidelines: OpenStudio-Toolkit

This document defines the rules and constraints for Antigravity when modifying the OpenStudio-Toolkit.

---

## 1. Development Workflow (Mandatory)
- **Branching**: ALL feature development and refactoting MUST occur on a new feature branch (e.g., `feature/optimization`). NEVER commit directly to `main`.
- **Testing**: A `tests/` directory must be created. All changes must be verified with `pytest` within the feature branch before seeking merge approval.
- **Baseline**: Use the folder `examples/` (e.g., `cabana-60.osm`) to create baseline verification tests.

## 2. Architecture & Design Patterns
- **Paradigm**: Strict Functional Programming. No classes for business logic. 
- **Task Pattern**: Every task in `src/openstudio_toolkit/tasks/` must implement `validator(model, **kwargs)` and `run(model, **kwargs)`.
- **Refactoring Pattern**: Use the **"Smart Shortcut"** to fix N+1 performance issues in `osm_objects`:
    - Functions like `get_x_as_dict` should add an internal `_object_ref=None` parameter.
    - `get_all_x_as_dicts` should pass the actual OpenStudio object into that parameter.
- **Helper Usage**: Common logic (validation, dynamic lookup) belongs in `src/openstudio_toolkit/utils/helpers.py`.

## 3. Code Standards & Constraints
- **Explicitness**: DO NOT hide `.is_initialized().get()` logic in attribute dictionaries. This is considered informative and must be kept explicit as per user preference.
- **Safety**: Always use `if optional.is_initialized():` before calling `.get()` to prevent C++ level crashes (Segment Faults).
- **Type Hints**: Mandatory for all parameters and return values.
- **Logging**: Replace `print()` with `logging.getLogger(__name__)` to allow external control of library verbosity.

## 4. Dependencies
- **Core**: Python >= 3.9 (as per `pyproject.toml`).
- **Libraries**: `pandas`, `pytest`, `openpyxl`.
- **SDK**: `openstudio` (Python bindings).

---
*Created by Antigravity on 2025-12-22*
