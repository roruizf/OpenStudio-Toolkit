# OpenStudio Toolkit

A Python library that provides structured access to OpenStudio Model (OSM) elements through a set of straightforward functions. It allows users to extract, analyze, and modify building energy models by transforming OpenStudio objects into Python-friendly data structures (dictionaries, lists, and Pandas DataFrames).

**Built by**: [Roberto Ruiz](https://github.com/roruizf)

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Available Modules](#available-modules)
- [Available Tasks](#available-tasks)
- [Example Workflows](#example-workflows)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Features

### Core Functionality

**OSM Objects Module** - Pythonic access to OpenStudio model entities:
- Building Structure (building, stories)
- Spatial Elements (spaces, thermal zones, surfaces, subsurfaces, space types)
- HVAC Systems (air loops, components, sizing, zone equipment)
- Materials & Constructions
- Internal Loads & Schedules
- Simulation Outputs
- Component Curves & Controllers
- Exterior Equipment

**Utilities Module** - Helper functions for common operations:
- Excel import/export utilities
- OSM model utilities
- EnergyPlus utilities
- Jupyter notebook helpers

**Pre-built Tasks** - Ready-to-use automation tasks:
- Model Setup (normalize names, rename surfaces/subsurfaces, set space properties)
- Model QA/QC (calculate WWR by space)
- Simulation Setup (configure output variables)
- Results Analysis (extract timeseries from SQL)

---

## Prerequisites

- **Python** 3.8 or higher
- **OpenStudio** 3.x or higher (with Python bindings)
- **Operating System**: Windows, macOS, or Linux

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/roruizf/OpenStudio-Toolkit.git
cd OpenStudio-Toolkit
```

### 2. Install OpenStudio Python Package

This toolkit requires the OpenStudio Python package to be installed in your environment.

**Recommended (tested and verified):**

```bash
pip install openstudio==3.7.0
```

**Note:** Version 3.7.0 has been fully tested with this toolkit. Other versions (3.x or higher) may work but are not guaranteed. If you choose to use a different version, you do so at your own risk.

### 3. Install the Toolkit

**Option A: Install in Editable Mode (Recommended for Development)**

```bash
pip install -e .
```

This installs the package in "editable mode" - any changes you make to the source code are immediately reflected without reinstalling. Perfect for development and experimentation.

**Option B: Install in Standard Mode (Recommended for Regular Use)**

```bash
pip install .
```

This installs the package as a standard library. Use this if you just want to use the toolkit without modifying it.

**Both options install the required dependencies:**
- pandas
- pytest
- openpyxl

---

## Quick Start

Here's a simple example to get started:

```python
import openstudio
from openstudio_toolkit.osm_objects import spaces, thermal_zones
from openstudio_toolkit.tasks.model_setup import normalize_space_names

# Load an OpenStudio model
translator = openstudio.osversion.VersionTranslator()
osm_model = translator.loadModel("path/to/model.osm").get()

# Extract spaces as a DataFrame
spaces_df = spaces.get_all_space_objects_as_dataframe(osm_model)
print(spaces_df.head())

# Run a pre-built task to normalize space names
validation = normalize_space_names.validator(osm_model)
if validation["status"] == "READY":
    osm_model = normalize_space_names.run(osm_model)
    osm_model.save("path/to/updated_model.osm", True)
```

---

## Available Modules

### OSM Objects

| Module | Description |
|--------|-------------|
| `building` | Building-level properties and methods |
| `building_stories` | Story definitions and attributes |
| `spaces` | Space geometry and absolute orientations (8-point) |
| `thermal_zones` | Thermal zone definitions |
| `surfaces` | Wall, floor, roof, and ceiling surfaces with azimuth and orientation (4/8-point) |
| `subsurfaces` | Windows, doors, and skylights with azimuth and orientation (4/8-point) |
| `space_types` | Space type assignments and properties |
| `materials` | Material definitions |
| `constructions` | Construction assemblies |
| `loads` | Internal loads (people, lights, equipment) |
| `schedules` | Schedule definitions and rulesets |
| `hvac_air_loops` | Air loop HVAC systems |
| `hvac_components` | HVAC equipment components |
| `hvac_sizing` | HVAC sizing parameters |
| `hvac_zone` | Zone-level HVAC equipment |
| `outputs` | Simulation output requests |
| `component_curves` | Performance curves |
| `controllers` | Controller objects |
| `exterior_equipment` | Exterior equipment definitions |

### Utilities

| Module | Description |
|--------|-------------|
| `excel_utils` | Excel file read/write operations |
| `osm_utils` | General OSM manipulation utilities |
| `eplus_utils` | EnergyPlus-related utilities |
| `notebook_helpers` | Jupyter notebook convenience functions |

---

## Available Tasks

Tasks are pre-built, validated workflows for common modeling operations. Each task includes a `validator()` function to check preconditions and a `run()` function to execute the task.

### Model Setup

| Task | Description |
|------|-------------|
| `normalize_space_names` | Replace spaces/underscores with hyphens in space names |
| `rename_surfaces_based_on_space_names` | Rename surfaces using their parent space names |
| `rename_subsurfaces_based_on_space_and_surface_names` | Rename subsurfaces using space and surface names |
| `set_space_surfacearea_height_volume` | Calculate and set space geometric properties |

### Model QA/QC

| Task | Description |
|------|-------------|
| `calculate_wwr_by_space` | Calculate window-to-wall ratio for each space |

### Measures

| Task | Description |
|------|-------------|
| `apply_space_type_and_construction_set_wizard` | Applies Space Types and Construction Sets based on Building Type, Climate Zone, and Template (ASHRAE/DOE standards) |
| `create_view_model_html` | Generates a standalone HTML report with 3D geometry visualization and model statistics |

### Simulation Setup

| Task | Description |
|------|-------------|
| `set_output_variables` | Configure simulation output variables |

### Results Analysis

| Task | Description |
|------|-------------|
| `get_timeseries_from_sql` | Extract timeseries data from EnergyPlus SQL output |

**Example Task Usage:**

```python
from openstudio_toolkit.tasks.model_setup import normalize_space_names

# Validate before running
result = normalize_space_names.validator(osm_model)
print(result["messages"])

if result["status"] == "READY":
    osm_model = normalize_space_names.run(osm_model)
```

---

## Example Workflows

The `notebooks/` directory contains Jupyter notebook examples organized by workflow type:

### 1. Model Setup
- `1.1_Normalize_Space_Names.ipynb` - Clean up space naming conventions
- `1.2_Rename_Surfaces_Based_on_Space_Names.ipynb` - Systematic surface renaming
- `1.3_Rename_Subsurfaces_Based_on_Space_and_Surface_Names.ipynb` - Subsurface naming
- `1.4_Set_Space_SurfaceArea_Height_Volume.ipynb` - Calculate space geometry

### 2. Model QA/QC
- `2.1_Calculate_WWR_by_Space.ipynb` - Window-to-wall ratio analysis

### 3. Simulation Setup
- `3.1_Set_Output_Variables.ipynb` - Configure simulation outputs

### 4. Results Analysis
- `4.1_Get_Timeseries_from_SQL.ipynb` - Extract and analyze simulation results

---

## Project Structure

```
OpenStudio-Toolkit/
├── src/openstudio_toolkit/        # Core library
│   ├── osm_objects/                # OSM object modules
│   ├── utils/                      # Utility functions
│   ├── tasks/                      # Pre-built task modules
│   │   ├── model_setup/
│   │   ├── model_qa_qc/
│   │   ├── simulation_setup/
│   │   └── results_analysis/
│   └── workflows/                  # Workflow orchestration
├── notebooks/                      # Example Jupyter notebooks
│   ├── 1_Model_Setup/
│   ├── 2_Model_QA_QC/
│   ├── 3_Simulation_Setup/
│   └── 4_Results_Analysis/
├── examples/                       # Example OSM files
├── tests/                          # Unit tests
├── pyproject.toml                  # Project configuration
└── README.md
```

---

## Testing

Run the test suite with pytest:

```bash
pytest tests/
```

Run specific test modules:

```bash
pytest tests/osm_objects/test_spaces.py
pytest tests/utils/test_osm_utils.py
```

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Related Projects

- [openstudio-mcp-server](https://github.com/roruizf/openstudio-mcp-server) - Model Context Protocol server for OpenStudio
- [OpenStudio](https://github.com/NREL/OpenStudio) - Cross-platform collection of software tools for building energy modeling

---

**Questions or Issues?** Please open an issue on [GitHub](https://github.com/roruizf/OpenStudio-Toolkit/issues).
