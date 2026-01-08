import openstudio
import logging
import os
from pathlib import Path
from typing import Optional

from openstudio_toolkit.utils.measure_runner import MeasureRunner
from openstudio_toolkit.utils.osm_utils import save_model_as_osm_file, load_osm_file_as_model

# Configure logger
logger = logging.getLogger(__name__)

def validator(osm_model: openstudio.model.Model) -> bool:
    """
    Validate the OpenStudio model before running the Hard Size HVAC measure.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio model to validate.

    Returns:
    - bool: True if the model is valid, False otherwise.
    """
    if osm_model is None:
        logger.error("Invalid model: None")
        return False
    
    # Check if there are any HVAC components that could be sized
    if not osm_model.getAirLoopHVACs() and not osm_model.getPlantLoops() and not osm_model.getZoneHVACComponents():
        logger.warning("Model has no HVAC components (AirLoop, PlantLoop, or ZoneHVAC). Sizing may have no effect.")
    
    return True

def run(
    osm_model: openstudio.model.Model,
    output_path: Optional[str] = None
) -> openstudio.model.Model:
    """
    Apply the Hard Size HVAC measure to an OpenStudio model.
    This measure runs a sizing run and applies autosized values back to the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio model to apply the measure to.
    - output_path (str, optional): Path to save the resulting OSM file.

    Returns:
    - openstudio.model.Model: The modified OpenStudio model.
    """
    if not validator(osm_model):
        raise ValueError("Model validation failed for Hard Size HVAC measure.")

    # Get the measure directory (relative to this file)
    # Resources are at src/openstudio_toolkit/resources/measures/HardSizeHvac
    # Current file is at src/openstudio_toolkit/tasks/measures/hard_size_hvac.py
    measure_dir = str(Path(__file__).parent.parent.parent / "resources" / "measures" / "HardSizeHvac")
    
    # Temporary file for the initial model
    temp_input_osm = "temp_input_hard_size.osm"
    save_model_as_osm_file(osm_model, temp_input_osm)
    
    try:
        runner = MeasureRunner()
        # This measure has no arguments
        arguments = {}
        
        # Execute the measure
        result = runner.run(
            model_path=temp_input_osm,
            measure_dir=measure_dir,
            arguments=arguments,
            run_simulation=False # The measure does its own sizing run
        )
        
        # Load the result model using our utility
        result_osm_path = result["osm_path"]
        result_model = load_osm_file_as_model(result_osm_path)
        
        # Save to output path if provided
        if output_path:
            save_model_as_osm_file(result_model, output_path)
            
        return result_model

    finally:
        # Cleanup temporary input file
        if os.path.exists(temp_input_osm):
            os.remove(temp_input_osm)
