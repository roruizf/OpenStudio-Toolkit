# Antigravity Project Guidelines: OpenStudio-Toolkit

This document defines the rules, patterns, and constraints for Antigravity when modifying the OpenStudio-Toolkit.

---

## 1. Development Workflow (Mandatory)
- **Branching**: ALL feature development and refactoring MUST occur on a new feature branch (e.g., `feature/optimization`). NEVER commit directly to `main`.
- **Testing**: A `tests/` directory must be created. All changes must be verified with `pytest` within the feature branch before seeking merge approval.
- **Baseline**: Use the folder `examples/` (e.g., `cabana-60.osm`) to create baseline verification tests.

## 2. Architecture & Design Patterns
- **Paradigm**: Strict Functional Programming. No classes for business logic (Data Classes or Typed Dicts are allowed for structures).
- **Task Pattern**: Every task in `src/openstudio_toolkit/tasks/` must implement:
    - `validator(model, **kwargs) -> Dict[str, Any]`: Returns `{'status': 'READY'|'SKIP'|'ERROR', 'messages': [...]}`.
    - `run(model, **kwargs) -> openstudio.model.Model`: Returns the modified model.
- **Input Pattern**: For batch operations, use `List[Dict[str, Any]]` as the argument type (not DataFrames). This ensures inputs are JSON-serializable and decoupled from pandas.
- **Return Pattern**: Action/Update functions (e.g., `update_spaces`, `assign_stories`) MUST return a **Status Dictionary**:
    ```python
    {
        "status": "SUCCESS" | "PARTIAL_SUCCESS" | "ERROR",
        "updated_count": int,
        "errors": int,
        "messages": List[str]
    }
    ```

## 3. OpenStudio Coding Standards (CRITICAL)
- **Handle Conversion**: NEVER use `openstudio.Handle(string)`. ALWAYS use `openstudio.toUUID(string)` to convert handle strings to UUID objects.
- **Object Retrieval**: Use `src/openstudio_toolkit/utils/helpers.py`:
    - `helpers.fetch_object(model, type, handle, name)`: Standardizes lookup by checking Handle first, then Name.
- **Safety**: Always use `if optional.is_initialized():` before calling `.get()` to prevent C++ level crashes (Segment Faults).
- **Attributes**: When extracting data to dicts, if an optional attribute is not initialized, set the value to `None` (not a placeholder string like "Unnamed").

## 4. Refactoring & Performance
- **"Smart Shortcut" Pattern**: Fix N+1 performance issues in `osm_objects`:
    - `get_x_as_dict` should accept an internal `_object_ref=None` parameter.
    - `get_all_x_as_dicts` should iterate objects and pass the direct reference to avoiding re-fetching.

## 5. Code Quality Constraints
- **Type Hints**: Mandatory for ALL parameters and return values.
- **Logging**: Replace `print()` with `logging.getLogger(__name__)`.
    - **Summary Pattern**: Log a summary at the end of batch operations (e.g., *"Assigned X stories, Skipped Y entries"*).
- **Explicitness**: Do not hide logic. Explicit is better than implicit.

## 6. Dependencies
- **Core**: Python >= 3.9 (as per `pyproject.toml`).
- **Libraries**: `pandas`, `pytest`, `openpyxl`.
- **SDK**: `openstudio` (Python bindings).

---
*Last Updated: 2025-12-23*
