import openstudio
import logging
from typing import Dict, List, Any

# Configure logger
logger = logging.getLogger(__name__)

def _is_normalized(space_name: str) -> bool:
    """
    Check if a space name is already normalized (contains no spaces or underscores).

    Parameters:
    - space_name (str): The name of the space to check.

    Returns:
    - bool: True if the name contains no spaces or underscores, False otherwise.
    """
    return " " not in space_name and "_" not in space_name

def validator(osm_model: openstudio.model.Model) -> Dict[str, Any]:
    """
    Validate that the model possesses spaces and check if they require name normalization.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object to validate.

    Returns:
    - Dict[str, Any]: A dictionary containing the validation 'status' ('READY', 'SKIP', or 'ERROR') and a list of 'messages'.
    """
    spaces = osm_model.getSpaces()
    if len(spaces) == 0:
        msg = "ERROR: Model contains no spaces to normalize."
        logger.error(msg)
        return {"status": "ERROR", "messages": [msg]}

    # Check if any space name actually needs normalization
    needs_normalization = any(not _is_normalized(s.name().get() if s.name().is_initialized() else "") for s in spaces)

    if not needs_normalization:
        messages = [f"OK: Found {len(spaces)} spaces.", "INFO: All space names are already normalized. Nothing to do."]
        logger.info("All space names are already normalized.")
        return {"status": "SKIP", "messages": messages}
    
    msg = f"OK: Found {len(spaces)} spaces. Some require normalization."
    logger.info(msg)
    return {"status": "READY", "messages": [msg]}

def run(osm_model: openstudio.model.Model) -> openstudio.model.Model:
    """
    Normalize all space names in the model by replacing spaces and underscores with hyphens and removing trailing/leading whitespace.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object to process.

    Returns:
    - openstudio.model.Model: The updated OpenStudio Model object.
    """
    logger.info("Starting normalize space names task...")
    
    spaces_renamed_count = 0
    for space in osm_model.getSpaces():
        if not space.name().is_initialized():
            continue
            
        original_name = space.name().get()
        # Replace spaces and underscores with hyphens, and strip whitespace
        normalized_name = original_name.replace(" ", "-").replace("_", "-").strip()
        
        if original_name != normalized_name:
            space.setName(normalized_name)
            spaces_renamed_count += 1
            
    logger.info(f"Task finished. {spaces_renamed_count} space names were normalized.")
    return osm_model