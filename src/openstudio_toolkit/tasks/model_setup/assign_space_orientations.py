import openstudio
import logging
from typing import Dict, List, Any
from openstudio_toolkit.osm_objects.spaces import calculate_space_orientation

# Configure logger
logger = logging.getLogger(__name__)

def get_space_orientations(osm_model: openstudio.model.Model) -> List[Dict[str, Any]]:
    """
    Calculate and retrieve orientations for all spaces in the model.
    """
    results = []
    for space in osm_model.getSpaces():
        # Uses the robust calculation from the spaces module
        orientation = calculate_space_orientation(space)
        results.append({
            'Space Handle': str(space.handle()),
            'Space Name': space.name().get() if space.name().is_initialized() else None,
            'Orientation': orientation
        })
    return results

def validator(osm_model: openstudio.model.Model) -> Dict[str, Any]:
    """
    Standard task validator.
    """
    spaces = osm_model.getSpaces()
    if len(spaces) == 0:
        msg = "ERROR: Model contains no spaces."
        logger.error(msg)
        return {"status": "ERROR", "messages": [msg]}
    
    return {"status": "READY", "messages": [f"Ready to analyze {len(spaces)} spaces."]}

def run(osm_model: openstudio.model.Model) -> openstudio.model.Model:
    """
    Execute the assign orientations task. 
    Currently, this calculates data; future versions may write to Space attributes.
    """
    orientations = get_space_orientations(osm_model)
    logger.info(f"Calculated orientations for {len(orientations)} spaces.")
    return osm_model
