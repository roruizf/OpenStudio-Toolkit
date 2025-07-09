# OpenStudio Toolkit

The OpenStudio Toolkit is a Python library that provides structured access to OpenStudio Model (OSM) elements through a set of straightforward functions. It allows users to extract, analyze, and modify building energy models by transforming OpenStudio objects into Python-friendly data structures, including dictionaries, lists of dictionaries, and Pandas DataFrames. This library is designed to assist modelers in automating and accelerating common OpenStudio modeling tasks. Furthermore, it can eventually serve as a foundation for building more sophisticated and specific help tools, such as APIs or even Google Sheets parser tools.

## Project Overview

This project, **OpenStudio Toolkit**, is a Python-based library and set of utilities designed to interact with and manipulate OpenStudio models. It provides structured modules for handling various OpenStudio Model (OSM) objects, utility functions, and example workflows demonstrated through Jupyter notebooks.

## High-Level Architecture

The project is organized into several key components:

*   **Core Library** (`src/openstudio_toolkit`): The main Python package containing modules for OpenStudio object manipulation and general utilities.
*   **Entry Points/Scripts**: Standalone Python scripts and Jupyter notebooks that utilize the core library for specific tasks or demonstrations.
*   **Configuration**: Project metadata and dependencies defined in `pyproject.toml`.
*   **Testing Framework**: A dedicated suite for ensuring the correctness and reliability of the core library modules.

The primary relationship is that the **Entry Points/Scripts** consume and utilize the functionalities exposed by the **Core Library**. The **Testing Framework** validates the **Core Library**.

## Core Library: openstudio_toolkit

The core of this project resides within the `src/openstudio_toolkit` directory. It is structured into two main sub-packages: `osm_objects` and `utils`.

### OSM Objects Module

The `src/openstudio_toolkit/osm_objects` module is dedicated to providing Pythonic representations and manipulation capabilities for various OpenStudio model entities. Each file within this module typically corresponds to a specific category of OpenStudio objects.

Key internal parts include:

*   **Building Structure**: Modules for defining and interacting with the overall building and its stories.
    *   `building.py`
    *   `building_stories.py`
*   **Spatial Elements**: Modules for managing spaces, thermal zones, surfaces, and subsurfaces.
    *   `spaces.py`
    *   `thermal_zones.py`
    *   `surfaces.py`
    *   `subsurfaces.py`
    *   `space_types.py`
*   **HVAC Systems**: Modules for handling various HVAC components, air loops, and sizing.
    *   `hvac_air_loops.py`
    *   `hvac_components.py`
    *   `hvac_sizing.py`
    *   `hvac_zone.py`
*   **Materials and Constructions**: Modules for defining and managing building materials and constructions.
    *   `materials.py`
    *   `constructions.py`
*   **Loads and Schedules**: Modules for managing internal loads and schedules.
    *   `loads.py`
    *   `schedules.py`
*   **Other**:
    *   `component_curves.py`
    *   `controllers.py`
    *   `exterior_equipment.py`

### Utilities Module

The `src/openstudio_toolkit/utils` module provides general-purpose helper functions that support the functionality of the `osm_objects` module and other scripts.

Key internal parts include:

*   **Excel Utilities**: Functions for interacting with Excel files, likely for data import/export or reporting.
    *   `excel_utils.py`
*   **OSM Utilities**: General utility functions specifically for OpenStudio models that don't fit into a specific object category.
    *   `osm_utils.py`
*   **Setup**: Potentially for initial setup or configuration.
    *   `setup.py`

<!-- ## Testing Framework (not yet implemented)

The `tests` directory contains unit tests to ensure the correctness and stability of the `openstudio_toolkit` library. The structure mirrors the `src` directory, with separate test files for each module.

*   **OSM Objects Tests**: Tests for the `osm_objects` module.
*   **Utilities Tests**: Tests for the `utils` module. -->
