import logging
from typing import Any

import openstudio

# Configure logger
logger = logging.getLogger(__name__)

def validator(osm_model: openstudio.model.Model, spaces_data: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Validate that the model and input data are ready for the space data update task.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - spaces_data (List[Dict[str, Any]]): A list of dictionaries, where each represents a space and its data to be updated.
                                         Each dictionary must contain a 'Name' or 'Handle' key.

    Returns:
    - Dict[str, Any]: A dictionary with validation 'status' and 'messages'.
    """
    messages = []
    
    if not spaces_data:
        msg = "ERROR: The input 'spaces_data' list is empty."
        logger.error(msg)
        return {"status": "ERROR", "messages": [msg]}

    # Check if all dicts have a required key (Name or Handle)
    if not all('Name' in d or 'Handle' in d for d in spaces_data):
        msg = "ERROR: Each dictionary in 'spaces_data' must have a 'Name' or 'Handle' key."
        logger.error(msg)
        return {"status": "ERROR", "messages": [msg]}

    # Check that spaces from the data exist in the model
    missing_count = 0
    for space_dict in spaces_data:
        space_name = space_dict.get('Name')
        if space_name and not osm_model.getSpaceByName(space_name).is_initialized():
            missing_count += 1

    if missing_count > 0:
        msg = f"WARNING: {missing_count} spaces from the provided data were not found in the model and will be skipped."
        logger.warning(msg)
        messages.append(msg)
    
    msg = f"OK: Ready to process {len(spaces_data)} data entries."
    logger.info(msg)
    messages.append(msg)
    return {"status": "READY", "messages": messages}

def run(osm_model: openstudio.model.Model, spaces_data: list[dict[str, Any]]) -> openstudio.model.Model:
    """
    Update geometric properties (Floor Area, Volume, Ceiling Height) for spaces based on a provided list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object to modify.
    - spaces_data (List[Dict[str, Any]]): List of dictionaries containing the data to update.

    Returns:
    - openstudio.model.Model: The updated OpenStudio Model object.
    """
    logger.info("Starting 'Set Space Data' task...")
    
    updated_count = 0
    for space_dict in spaces_data:
        space_name = space_dict.get('Name')
        space_handle = space_dict.get('Handle')
        
        target_space = None
        if space_handle:
            st_obj = osm_model.getSpace(openstudio.toUUID(space_handle))
            if st_obj.is_initialized():
                target_space = st_obj.get()
        elif space_name:
            st_obj = osm_model.getSpaceByName(space_name)
            if st_obj.is_initialized():
                target_space = st_obj.get()
                
        if target_space:
            # Update properties if they differ from input
            if 'Floor Area {m2}' in space_dict:
                val = space_dict['Floor Area {m2}']
                if target_space.floorArea() != val:
                    target_space.setFloorArea(val)

            if 'Volume {m3}' in space_dict:
                val = space_dict['Volume {m3}']
                if target_space.volume() != val:
                    target_space.setVolume(val)

            if 'Ceiling Height {m}' in space_dict:
                val = space_dict['Ceiling Height {m}']
                if target_space.ceilingHeight() != val:
                    target_space.setCeilingHeight(val)
            
            updated_count += 1
            
    logger.info(f"Task finished. Geometric data for {updated_count} spaces was processed.")
    return osm_model