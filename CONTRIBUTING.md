# OpenStudio-Toolkit Contribution Guidelines

This document defines the architectural patterns, coding standards, and constraints for all contributors (developers and AI agents) working on the OpenStudio-Toolkit.

---

## 1. Development Workflow (Mandatory)
- **Branching**: ALL feature development and refactoring MUST occur on a new feature branch (e.g., `feature/optimization`). NEVER commit directly to `main`.
- **Testing**: A `tests/` directory must be created. All changes must be verified with `pytest` within the feature branch before seeking merge approval.
- **Baseline**: Use the folder `examples/` (e.g., `cabana-60.osm`) to create baseline verification tests.

## 2. Project Architecture

This project follows a **functional, task-based architecture**.

### Core Concepts

#### A. Task (`src/openstudio_toolkit/tasks/`)
An **atomic unit of work** that transforms an OpenStudio model.
- **Structure**: NOT a class. Pure Python module.
- **Required Functions**:
    - `validator(model, **kwargs) -> Dict[str, Any]`: Returns `{'status': 'READY'|'SKIP'|'ERROR', 'messages': [...]}`.
    - `run(model, **kwargs) -> openstudio.model.Model`: Returns the modified model (immutable pattern).

#### B. Workflow (`src/openstudio_toolkit/workflows/`)
A script that **orchestrates multiple Tasks** in sequence. Composes tasks to achieve complex operations.

#### C. Measure (`src/openstudio_toolkit/resources/measures/`)
A logic unit relying on **external Ruby code**.
- **Resources**: Ruby files live in `resources/measures/`.
- **Wrapper**: A Python Task in `tasks/measures/` uses `MeasureRunner` to execute the Ruby code via CLI.

#### D. OSM Objects (`src/openstudio_toolkit/osm_objects/`)
Wrappers for OpenStudio SDK objects to provide pythonic accessors/mutators.

## 3. Design Patterns & API Standards

- **Paradigm**: Strict Functional Programming. No classes for business logic (Data Classes allowed for structures).
- **Input Pattern**: For batch operations, use `List[Dict[str, Any]]` as the argument type (not DataFrames).
- **Return Pattern**: Action/Update functions (e.g., `update_spaces`) MUST return a **Status Dictionary**:
    ```python
    {
        "status": "SUCCESS" | "PARTIAL_SUCCESS" | "ERROR",
        "updated_count": int,
        "errors": int,
        "messages": List[str]
    }
    ```
- **Identification Pattern**: For `update_*_data` operations, `Handle` is the MANDATORY identifier to ensure safe renaming and consistent object referencing.
- **Import Pattern**: Use `importlib.resources` for non-code assets (NEVER `pkg_resources`).
- **Language**: English ONLY for code, comments, and commits.

## 4. OpenStudio Coding Standards (CRITICAL)

- **Handle Conversion**: NEVER use `openstudio.Handle(string)`. ALWAYS use `openstudio.toUUID(string)` to convert handle strings to UUID objects.
- **Object Retrieval**: Use `src/openstudio_toolkit/utils/helpers.py`:
    - `helpers.fetch_object(model, type, handle, name)`: Standardizes lookup by checking Handle first, then Name.
- **Safety**: Always use `if optional.is_initialized():` before calling `.get()` to prevent C++ level crashes (Segment Faults).
- **Attributes**: When extracting data to dicts, if an optional attribute is not initialized, set the value to `None` (not a placeholder string).

## 5. Refactoring & Performance

- **"Smart Shortcut" Pattern**: Fix N+1 performance issues in `osm_objects`:
    - `get_x_as_dict` should accept an internal `_object_ref=None` parameter.
    - `get_all_x_as_dicts` should iterate objects and pass the direct reference to avoid re-fetching.

## 6. Code Quality Constraints
- **Type Hints**: Mandatory for ALL parameters and return values.
- **Logging**: Replace `print()` with `logging.getLogger(__name__)`.
    - **Summary Pattern**: Log a summary at the end of batch operations.
- **Explicitness**: Do not hide logic. Explicit is better than implicit.

## 7. Dependencies
- **Core**: Python >= 3.9 (recommended 3.9+ for `importlib`).
- **Libraries**: `pandas`, `pytest`, `openpyxl`.
- **SDK**: `openstudio` (Python bindings) + CLI.

---
*Last Updated: 2025-12-23*
