# Claude Code Guidelines for OpenStudio-Toolkit

This document standardizes how Claude Code interacts with the OpenStudio-Toolkit project.

---

## Commands

### Install (Development Mode)

```bash
pip install -e .
```

Editable mode is **preferred** for development. Changes take effect immediately without reinstalling.

### Test

```bash
# Run specific test
python test_wizard.py

# Run all tests (when pytest suite exists)
pytest
```

---

## Project Architecture

This project follows a **functional, task-based architecture**. Understanding these core concepts is critical:

### Core Concepts

#### 1. Task

A **Task** is an **atomic unit of work** that transforms an OpenStudio model.

**Key Characteristics:**

- Located in: `src/openstudio_toolkit/tasks/`
- **NOT a class** - It is a Python module with two required functions
- Stateless and functional (no side effects)
- Returns a **new** model (immutable pattern)

**Required Functions:**

```python
def validator(osm_model: openstudio.model.Model, **kwargs) -> Dict[str, Any]:
    """
    Validates prerequisites before task execution.

    Returns:
        Dict with keys:
        - 'status': 'READY' or 'ERROR'
        - 'messages': List of validation messages
    """
    pass

def run(osm_model: openstudio.model.Model, **kwargs) -> openstudio.model.Model:
    """
    Executes the task logic on the model.

    Returns:
        New OpenStudio Model object with changes applied
    """
    pass
```

**Example Task Locations:**

- `tasks/model_setup/normalize_space_names.py`
- `tasks/model_qa_qc/calculate_wwr_by_space.py`
- `tasks/measures/apply_space_type_and_construction_set_wizard.py`

#### 2. Workflow

A **Workflow** is a **script that orchestrates multiple Tasks in sequence**.

**Key Characteristics:**

- Located in: `src/openstudio_toolkit/workflows/`
- Composes Tasks to achieve complex operations
- Handles intermediate state between tasks
- Functional composition pattern

**Example Pattern:**

```python
# workflows/example_workflow.py
from openstudio_toolkit.tasks.model_setup import normalize_space_names
from openstudio_toolkit.tasks.model_qa_qc import calculate_wwr_by_space

def run_workflow(model: openstudio.model.Model) -> openstudio.model.Model:
    """Orchestrates multiple tasks."""
    # Task 1
    model = normalize_space_names.run(model)

    # Task 2
    model = calculate_wwr_by_space.run(model, threshold=0.4)

    return model
```

#### 3. Measure

A **Measure** is a **logic unit that relies on external Ruby code** (OpenStudio Measure).

**Components:**

##### a) Resource (Ruby Files)

- Location: `src/openstudio_toolkit/resources/measures/<MeasureName>/`
- Contains:
  - `measure.rb` - Main Ruby implementation
  - `measure.xml` - Metadata and argument definitions
  - `LICENSE.md`, `README.md` - Documentation

**Example:**

```text
resources/measures/SpaceTypeAndConstructionSetWizard/
├── measure.rb
├── measure.xml
├── README.md
└── LICENSE.md
```

##### b) Wrapper Task (Python)

- Location: `src/openstudio_toolkit/tasks/measures/<measure_task>.py`
- A Python Task that uses `MeasureRunner` to execute Ruby code via OpenStudio CLI
- Follows the same `validator()` + `run()` pattern

**Example:**

```python
# tasks/measures/apply_space_type_and_construction_set_wizard.py
from openstudio_toolkit.utils.measure_runner import MeasureRunner

def run(osm_model: openstudio.model.Model, building_type: str, ...) -> openstudio.model.Model:
    """Wrapper that executes the Ruby measure via CLI."""
    runner = MeasureRunner()
    result = runner.run(
        model_path=temp_osm_path,
        measure_dir=str(measure_dir),
        arguments=measure_args,
        run_simulation=False
    )
    return result_model
```

---

## Folder Structure

```text
src/openstudio_toolkit/
├── osm_objects/          # Wrappers for OpenStudio SDK objects
│   ├── building.py       # Functions to work with Building objects
│   ├── spaces.py         # Functions to work with Space objects
│   └── ...
│
├── tasks/                # Atomic logic modules (Tasks)
│   ├── measures/         # Wrapper Tasks for Ruby measures
│   │   ├── __init__.py
│   │   └── apply_space_type_and_construction_set_wizard.py
│   ├── model_setup/      # Model preparation Tasks
│   │   ├── normalize_space_names.py
│   │   └── ...
│   ├── model_qa_qc/      # Quality assurance Tasks
│   ├── results_analysis/ # Post-simulation analysis Tasks
│   └── simulation_setup/ # Simulation configuration Tasks
│
├── workflows/            # Composed workflows (orchestrate Tasks)
│   └── __init__.py
│
├── utils/                # Helper utilities
│   ├── measure_runner.py # Executes Ruby measures via OpenStudio CLI
│   ├── osm_utils.py      # OSM file utilities
│   └── ...
│
└── resources/            # Static assets (downloaded/bundled resources)
    └── measures/         # Ruby measure files
        └── SpaceTypeAndConstructionSetWizard/
            ├── measure.rb
            └── measure.xml
```

---

## Coding Standards

### Programming Paradigm

**Functional Programming** - NOT Object-Oriented for business logic

**Rules:**

- ❌ NO classes for Task logic
- ✅ Pure functions that transform data
- ✅ Immutable operations (return new objects, don't modify inputs)
- ✅ Stateless functions (no global state)
- ✅ Single Responsibility Principle (one function = one job)

### Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| **Files** | `snake_case.py` | `apply_space_type_wizard.py` |
| **Functions** | `snake_case()` | `def run_simulation():` |
| **Variables** | `snake_case` | `building_type = "Office"` |
| **Constants** | `UPPER_SNAKE_CASE` | `BUILDING_TYPES = [...]` |
| **Modules** | `snake_case` | `from tasks.model_setup import ...` |

### Type Hints (MANDATORY)

**ALL functions MUST have strict type hints:**

```python
from typing import Dict, Any, List
import openstudio

# ✅ CORRECT
def validator(
    osm_model: openstudio.model.Model,
    building_type: str,
    template: str,
    climate_zone: str,
    create_space_types: bool = True
) -> Dict[str, Any]:
    """All parameters and return values must be typed."""
    pass

# ❌ WRONG
def validator(osm_model, building_type, template):
    """Missing type hints - NOT ACCEPTABLE"""
    pass
```

### Language

- **English ONLY** for:
  - Code (variable names, function names, comments)
  - Documentation (docstrings, README files)
  - Commit messages

### Import Standards

**Order:**

1. Standard library
2. Third-party packages
3. Local imports

**Modern Practices:**

```python
# Standard library
import os
import tempfile
from pathlib import Path
from typing import Dict, Any, List

# Use importlib.resources (NOT pkg_resources - deprecated)
from importlib.resources import files

# Third-party
import openstudio
import pandas as pd

# Local imports
from openstudio_toolkit.utils.measure_runner import MeasureRunner
```

---

## Code Examples

### ✅ GOOD: Functional Task Pattern

```python
# tasks/model_setup/normalize_space_names.py
import openstudio
from typing import Dict, Any

def validator(osm_model: openstudio.model.Model) -> Dict[str, Any]:
    """Validate prerequisites."""
    if len(osm_model.getSpaces()) == 0:
        return {"status": "ERROR", "messages": ["No spaces found"]}
    return {"status": "READY", "messages": ["Validation passed"]}

def run(osm_model: openstudio.model.Model) -> openstudio.model.Model:
    """Normalize space names in the model."""
    # Work with model (functional, returns new model)
    return modified_model
```

### ❌ BAD: Class-based Pattern

```python
# ❌ DO NOT DO THIS
class SpaceNormalizer:
    def __init__(self, model):
        self.model = model  # Mutable state - BAD

    def normalize(self):
        # Modifies self.model - BAD
        pass
```

---

## Dependencies

- **Python**: >= 3.8 (minimum), **3.9+ recommended** for `importlib.resources`
- **OpenStudio**: Requires separate installation (SDK + CLI)
- **Python Packages**: `pandas`, `pytest`, `openpyxl`

Install via:

```bash
pip install -e .
```

---

## Key Principles for Claude

When working on this project, Claude should:

1. ✅ **Always use functional patterns** - No classes for Task logic
2. ✅ **Maintain strict type hints** - Every function parameter and return value
3. ✅ **Follow snake_case naming** - Files, functions, variables
4. ✅ **Use `importlib.resources`** - NOT `pkg_resources` (deprecated)
5. ✅ **Return new objects** - Never mutate input parameters
6. ✅ **Implement Task pattern** - Every Task needs `validator()` + `run()`
7. ✅ **Write in English** - Code, comments, docs, commit messages
8. ✅ **Understand Measure architecture** - Resource (Ruby) + Wrapper Task (Python)

---

## Quick Reference

| Concept | Definition | Location |
|---------|-----------|----------|
| **Task** | Atomic unit with `validator()` + `run()` | `tasks/` |
| **Workflow** | Orchestrates multiple Tasks | `workflows/` |
| **Measure Resource** | Ruby measure files (external logic) | `resources/measures/` |
| **Measure Wrapper** | Python Task that executes Ruby measure | `tasks/measures/` |
| **Utility** | Helper functions | `utils/` |
| **OSM Object** | OpenStudio object wrappers | `osm_objects/` |
