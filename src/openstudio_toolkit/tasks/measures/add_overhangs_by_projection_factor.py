import logging
import os
import tempfile
from pathlib import Path
from typing import Any

import openstudio

from openstudio_toolkit.utils.measure_runner import MeasureRunner

# Configure logger
logger = logging.getLogger(__name__)

# Valid values for measure arguments
FACADES = ["North", "East", "South", "West"]

def validator(
    osm_model: openstudio.model.Model,
    projection_factor: float = 0.5,
    facade: str = "South",
    remove_ext_space_shading: bool = False,
    construction: str | None = None
) -> dict[str, Any]:
    """
    Validate that required arguments are provided and the measure resource exists.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - projection_factor (float): The overhang depth divided by the window height.
    - facade (str): Cardinal direction (North, East, South, West).
    - remove_ext_space_shading (bool): If True, deletes pre-existing space shading surfaces.
    - construction (str, optional): Handle or Name of a construction for the overhangs.

    Returns:
    - Dict[str, Any]: Status dictionary with 'status' ('READY' or 'ERROR') and 'messages'.
    """
    messages = []

    # Validate types
    if not isinstance(projection_factor, (int, float)):
        messages.append(f"ERROR: Argument 'projection_factor' must be a number. Got {type(projection_factor)}.")
    elif projection_factor < 0:
        messages.append(f"ERROR: Argument 'projection_factor' cannot be negative. Got {projection_factor}.")

    if not isinstance(facade, str):
        messages.append(f"ERROR: Argument 'facade' must be a string. Got {type(facade)}.")
    elif facade not in FACADES:
        messages.append(f"ERROR: Invalid facade '{facade}'. Must be one of {FACADES}.")

    if not isinstance(remove_ext_space_shading, bool):
        messages.append(f"ERROR: Argument 'remove_ext_space_shading' must be a boolean. Got {type(remove_ext_space_shading)}.")

    # Validate construction if provided
    if construction:
        # Check if it's a valid construction in the model
        found = False
        # Try finding by handle first
        try:
            handle = openstudio.toUUID(construction)
            obj = osm_model.getObject(handle)
            if obj.is_initialized():
                if obj.get().iddObject().type() == openstudio.IddObjectType("OS:Construction"):
                    found = True
        except:
            pass
        
        # Try finding by name if not found by handle
        if not found:
            for const in osm_model.getConstructions():
                if const.nameString() == construction:
                    found = True
                    break
        
        if not found:
            messages.append(f"ERROR: Construction '{construction}' not found in the model.")

    if messages:
        logger.error(f"Validation failed for AddOverhangsByProjectionFactor: {messages}")
        return {"status": "ERROR", "messages": messages}

    # Check if measure resource exists
    try:
        measure_dir = Path(__file__).parent.parent.parent / "resources" / "measures" / "AddOverhangsByProjectionFactor"
        if not measure_dir.exists():
            msg = "ERROR: Measure resource 'AddOverhangsByProjectionFactor' not found."
            logger.error(msg)
            return {"status": "ERROR", "messages": [msg]}
    except Exception as e:
        msg = f"ERROR: Could not locate measure resource: {e}"
        logger.error(msg)
        return {"status": "ERROR", "messages": [msg]}

    runner = MeasureRunner()
    if not runner.verify_measure_content(str(measure_dir)):
        msg = "ERROR: Measure resource is invalid (missing measure.xml)."
        logger.error(msg)
        return {"status": "ERROR", "messages": [msg]}

    logger.info("AddOverhangsByProjectionFactor validation successful.")
    return {"status": "READY", "messages": ["OK: All validations passed."]}

def run(
    osm_model: openstudio.model.Model,
    projection_factor: float = 0.5,
    facade: str = "South",
    remove_ext_space_shading: bool = False,
    construction: str | None = None
) -> openstudio.model.Model:
    """
    Execute the Add Overhangs by Projection Factor measure on the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - projection_factor (float): The overhang depth divided by the window height.
    - facade (str): Cardinal direction.
    - remove_ext_space_shading (bool): If True, deletes pre-existing space shading surfaces.
    - construction (str, optional): Handle or Name of a construction for the overhangs.

    Returns:
    - openstudio.model.Model: New Model object with the measure applied.

    Raises:
    - RuntimeError: If measure execution fails.
    """
    logger.info("Starting Add Overhangs by Projection Factor task...")

    # Validate inputs
    validation = validator(
        osm_model=osm_model,
        projection_factor=projection_factor,
        facade=facade,
        remove_ext_space_shading=remove_ext_space_shading,
        construction=construction
    )
    if validation["status"] != "READY":
        raise RuntimeError(f"Validation failed: {validation['messages']}")

    # Measure arguments
    # Note: construction needs to be passed as its name or handle as expected by the Ruby measure
    measure_args = {
        "projection_factor": projection_factor,
        "facade": facade,
        "remove_ext_space_shading": remove_ext_space_shading
    }
    
    if construction:
        measure_args["construction"] = construction

    # Get measure directory
    measure_dir = Path(__file__).parent.parent.parent / "resources" / "measures" / "AddOverhangsByProjectionFactor"

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
            run_simulation=False
        )

        # Load the resulting model
        translator = openstudio.osversion.VersionTranslator()
        loaded_model = translator.loadModel(result["osm_path"])
        if loaded_model.is_initialized():
            result_model = loaded_model.get()
            logger.info("Add Overhangs by Projection Factor task completed successfully.")
            return result_model
        else:
            raise RuntimeError("Failed to load the model after measure execution.")

    finally:
        # Clean up temporary files
        if os.path.exists(temp_osm_path):
            os.unlink(temp_osm_path)
        if 'result' in locals() and os.path.exists(result["osm_path"]):
            os.unlink(result["osm_path"])
