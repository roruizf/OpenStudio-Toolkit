import openstudio
import tempfile
import os
from pathlib import Path
from typing import Dict, Any, List
from importlib.resources import files

from openstudio_toolkit.utils.measure_runner import MeasureRunner

# Valid values for measure arguments
BUILDING_TYPES = [
    "SecondarySchool",
    "PrimarySchool",
    "SmallOffice",
    "MediumOffice",
    "LargeOffice",
    "SmallHotel",
    "LargeHotel",
    "Warehouse",
    "RetailStandalone",
    "RetailStripmall",
    "QuickServiceRestaurant",
    "FullServiceRestaurant",
    "MidriseApartment",
    "HighriseApartment",
    "Hospital",
    "Outpatient",
    "SuperMarket",
    "Laboratory",
    "LargeDataCenterLowITE",
    "LargeDataCenterHighITE",
    "SmallDataCenterLowITE",
    "SmallDataCenterHighITE",
    "Courthouse",
    "College"
]

CLIMATE_ZONES = [
    "ASHRAE 169-2013-1A",
    "ASHRAE 169-2013-1B",
    "ASHRAE 169-2013-2A",
    "ASHRAE 169-2013-2B",
    "ASHRAE 169-2013-3A",
    "ASHRAE 169-2013-3B",
    "ASHRAE 169-2013-3C",
    "ASHRAE 169-2013-4A",
    "ASHRAE 169-2013-4B",
    "ASHRAE 169-2013-4C",
    "ASHRAE 169-2013-5A",
    "ASHRAE 169-2013-5B",
    "ASHRAE 169-2013-5C",
    "ASHRAE 169-2013-6A",
    "ASHRAE 169-2013-6B",
    "ASHRAE 169-2013-7A",
    "ASHRAE 169-2013-8A"
]

TEMPLATES = [
    "DOE Ref Pre-1980",
    "DOE Ref 1980-2004",
    "90.1-2004",
    "90.1-2007",
    "90.1-2010",
    "90.1-2013",
    "90.1-2016",
    "90.1-2019",
    "ComStock DOE Ref Pre-1980",
    "ComStock DOE Ref 1980-2004",
    "ComStock 90.1-2004",
    "ComStock 90.1-2007",
    "ComStock 90.1-2010",
    "ComStock 90.1-2013",
    "ComStock 90.1-2016",
    "ComStock 90.1-2019"
]


def validator(osm_model: openstudio.model.Model, building_type: str, template: str, climate_zone: str, create_space_types: bool = True, create_construction_set: bool = True, set_building_defaults: bool = True) -> Dict[str, Any]:
    """
    Validates that required arguments are provided and the measure resource exists.

    Args:
        osm_model: The OpenStudio Model object.
        building_type: Building type for standards.
        template: Standards template.
        climate_zone: Climate zone for standards.
        create_space_types: Whether to create space types.
        create_construction_set: Whether to create construction set.
        set_building_defaults: Whether to set building defaults using new objects.

    Returns:
        Dict with 'status' ('READY', 'ERROR') and 'messages' (list of strings).
    """
    messages = []

    # Check required arguments are strings and not empty
    required_args = [building_type, template, climate_zone]
    arg_names = ['building_type', 'template', 'climate_zone']
    for name, arg in zip(arg_names, required_args):
        if not isinstance(arg, str):
            messages.append(f"ERROR: Argument '{name}' must be a string")
        elif not arg.strip():
            messages.append(f"ERROR: Argument '{name}' cannot be empty")

    if messages:
        return {"status": "ERROR", "messages": messages}

    # Validate building_type
    if building_type not in BUILDING_TYPES:
        messages.append(
            f"ERROR: Invalid building_type '{building_type}'. "
            f"Must be one of: {', '.join(BUILDING_TYPES)}"
        )

    # Validate climate_zone
    if climate_zone not in CLIMATE_ZONES:
        messages.append(
            f"ERROR: Invalid climate_zone '{climate_zone}'. "
            f"Must be one of: {', '.join(CLIMATE_ZONES)}"
        )

    # Validate template
    if template not in TEMPLATES:
        messages.append(
            f"ERROR: Invalid template '{template}'. "
            f"Must be one of: {', '.join(TEMPLATES)}"
        )

    if messages:
        return {"status": "ERROR", "messages": messages}

    # Check if measure resource exists using importlib.resources
    try:
        measure_dir = Path(str(
            files('openstudio_toolkit.resources.measures').joinpath('SpaceTypeAndConstructionSetWizard')
        ))

        if not measure_dir.exists():
            messages.append(
                "ERROR: Measure resource 'SpaceTypeAndConstructionSetWizard' not found")
            return {"status": "ERROR", "messages": messages}
    except Exception as e:
        messages.append(f"ERROR: Could not locate measure resource: {e}")
        return {"status": "ERROR", "messages": messages}

    runner = MeasureRunner()
    if not runner.verify_measure_content(str(measure_dir)):
        messages.append(
            "ERROR: Measure resource is invalid (missing measure.xml)")
        return {"status": "ERROR", "messages": messages}

    messages.append("OK: All validations passed")
    return {"status": "READY", "messages": messages}


def run(osm_model: openstudio.model.Model, building_type: str, template: str, climate_zone: str, create_space_types: bool = True, create_construction_set: bool = True, set_building_defaults: bool = True) -> openstudio.model.Model:
    """
    Executes the Space Type and Construction Set Wizard measure on the model.

    Args:
        osm_model: The OpenStudio Model object.
        building_type: Building type for standards.
        template: Standards template.
        climate_zone: Climate zone for standards.
        create_space_types: Whether to create space types.
        create_construction_set: Whether to create construction set.
        set_building_defaults: Whether to set building defaults using new objects.

    Returns:
        New OpenStudio Model object with the measure applied.

    Raises:
        RuntimeError: If measure execution fails.
    """
    print("INFO: Starting Space Type and Construction Set Wizard task...")

    # Validate again (though validator should have been called first)
    validation = validator(osm_model, building_type, template,
                           climate_zone, create_space_types, create_construction_set, set_building_defaults)
    if validation["status"] != "READY":
        raise RuntimeError(f"Validation failed: {validation['messages']}")

    # Prepare measure arguments
    measure_args = {
        "building_type": building_type,
        "climate_zone": climate_zone,
        "template": template,
        "create_space_types": create_space_types,
        "create_construction_set": create_construction_set,
        "set_building_defaults": set_building_defaults
    }

    # Get measure directory using importlib.resources
    measure_dir = Path(str(
        files('openstudio_toolkit.resources.measures').joinpath('SpaceTypeAndConstructionSetWizard')
    ))

    # Save current model to temporary OSM file
    with tempfile.NamedTemporaryFile(suffix='.osm', delete=False) as temp_file:
        temp_osm_path = temp_file.name

    osm_model.save(temp_osm_path, True)

    try:
        # Run the measure
        runner = MeasureRunner()
        result = runner.run(
            model_path=temp_osm_path,
            measure_dir=str(measure_dir),
            arguments=measure_args,
            run_simulation=False  # CRITICAL: Measures only mode
        )

        # Load the resulting model
        translator = openstudio.osversion.VersionTranslator()
        result_model = translator.loadModel(result["osm_path"]).get()

        print("INFO: Space Type and Construction Set Wizard task completed successfully")
        return result_model

    finally:
        # Clean up temporary files
        if os.path.exists(temp_osm_path):
            os.unlink(temp_osm_path)
        if 'result' in locals() and os.path.exists(result["osm_path"]):
            os.unlink(result["osm_path"])
