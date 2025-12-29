import openstudio
import pandas as pd
import numpy as np
import logging
from typing import Dict, Any, List, Optional
from openstudio_toolkit.utils import helpers

# Configure logger
logger = logging.getLogger(__name__)

def get_building_unit_as_dict(
    osm_model: openstudio.model.Model, 
    unit_handle: Optional[str] = None, 
    unit_name: Optional[str] = None, 
    _object_ref: Optional[openstudio.model.BuildingUnit] = None
) -> Dict[str, Any]:
    """
    Retrieve attributes of a BuildingUnit object from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - unit_handle (str, optional): The handle of the unit to retrieve.
    - unit_name (str, optional): The name of the unit to retrieve.
    - _object_ref (openstudio.model.BuildingUnit, optional): Direct object reference.

    Returns:
    - Dict[str, Any]: A dictionary containing building unit attributes:
        - 'Handle'
        - 'Name'
        - 'Rendering Color'
        - 'Building Unit Type'
    """
    target_unit = helpers.fetch_object(
        osm_model, "BuildingUnit", unit_handle, unit_name, _object_ref)

    if target_unit is None:
        return {}

    return {
        'Handle': str(target_unit.handle()),
        'Name': target_unit.name().get() if target_unit.name().is_initialized() else None,
        'Rendering Color': target_unit.renderingColor().get().name().get() if target_unit.renderingColor().is_initialized() else None,
        'Building Unit Type': target_unit.buildingUnitType()
    }

def get_all_building_units_as_dicts(osm_model: openstudio.model.Model) -> List[Dict[str, Any]]:
    """
    Retrieve attributes for all BuildingUnit objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing building unit attributes.
    """
    all_objects = osm_model.getBuildingUnits()
    return [get_building_unit_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_building_unit_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all BuildingUnit attributes and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all building unit attributes.
    """
    all_objects_dicts = get_all_building_units_as_dicts(osm_model)
    df = pd.DataFrame(all_objects_dicts)

    if not df.empty and 'Name' in df.columns:
        df = df.sort_values(by='Name', ascending=True).reset_index(drop=True)

    logger.info(f"Retrieved {len(df)} building unit objects from the model.")
    return df

def create_new_building_unit_objects(osm_model: openstudio.model.Model, building_units_to_create_df: pd.DataFrame) -> None:
    """
    Create new BuildingUnit objects based on a DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - building_units_to_create_df (pd.DataFrame): DataFrame of unit data to create.

    Returns:
    - None
    """
    df = building_units_to_create_df.replace(np.nan, None)
    count = 0

    for _, row in df.iterrows():
        new_unit = openstudio.model.BuildingUnit(osm_model)
        if row.get('Name'):
            new_unit.setName(row['Name'])

        if row.get('Building Unit Type'):
            new_unit.setBuildingUnitType(str(row['Building Unit Type']))

        if row.get('Rendering Color'):
            render_opt = osm_model.getRenderingColorByName(row['Rendering Color'])
            if render_opt.is_initialized():
                new_unit.setRenderingColor(render_opt.get())
            else:
                new_color = openstudio.model.RenderingColor(osm_model)
                new_color.setName(row['Rendering Color'])
                new_unit.setRenderingColor(new_color)
        
        count += 1

    logger.info(f"Successfully created {count} new BuildingUnit objects.")

def update_building_unit_objects(osm_model: openstudio.model.Model, building_units_to_update_df: pd.DataFrame) -> None:
    """
    Update attributes of existing BuildingUnit objects based on a DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - building_units_to_update_df (pd.DataFrame): DataFrame containing updated unit data.

    Returns:
    - None
    """
    df = building_units_to_update_df.replace(np.nan, None)
    count = 0

    for _, row in df.iterrows():
        target_unit = helpers.fetch_object(osm_model, "BuildingUnit", row.get('Handle'), row.get('Name'))
        if not target_unit:
            continue

        if row.get('Name'):
            target_unit.setName(row['Name'])

        if row.get('Building Unit Type'):
            target_unit.setBuildingUnitType(str(row['Building Unit Type']))

        if row.get('Rendering Color'):
            render_opt = osm_model.getRenderingColorByName(row['Rendering Color'])
            if render_opt.is_initialized():
                target_unit.setRenderingColor(render_opt.get())
        
        count += 1

    logger.info(f"Successfully updated {count} BuildingUnit objects.")

def assign_spaces_to_building_units(osm_model: openstudio.model.Model, space_unit_mapping: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Assign BuildingUnit objects to Space objects based on a mapping list.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - space_unit_mapping (List[Dict[str, str]]): List of dictionaries, where each dict contains:
        - 'Space Handle': The space handle (string) - required
        - 'Building Unit Handle': The unit handle (string) - optional
        - 'Building Unit Name': The unit name (string) - optional
        Note: Must provide either 'Building Unit Handle' OR 'Building Unit Name'

    Returns:
    - Dict[str, Any]: A dictionary containing:
        - 'status': 'SUCCESS' if at least one assignment succeeded, 'ERROR' if all failed
        - 'assigned': Number of spaces successfully assigned to units
        - 'skipped': Number of entries skipped due to errors
        - 'messages': List of warning/error messages
    """
    count = 0
    skipped = 0
    messages = []
    
    for entry in space_unit_mapping:
        space_handle = entry.get('Space Handle')
        unit_handle = entry.get('Building Unit Handle')
        unit_name = entry.get('Building Unit Name')
        
        # Validate required space handle
        if not space_handle:
            msg = "Skipping entry: missing 'Space Handle'"
            logger.warning(msg)
            messages.append(msg)
            skipped += 1
            continue
        
        # Validate that at least one unit identifier is provided
        if not unit_handle and not unit_name:
            msg = f"Skipping space {space_handle}: missing both 'Building Unit Handle' and 'Building Unit Name'"
            logger.warning(msg)
            messages.append(msg)
            skipped += 1
            continue
        
        # Retrieve space object
        space_opt = osm_model.getSpace(openstudio.toUUID(space_handle))
        if not space_opt.is_initialized():
            msg = f"Space with handle {space_handle} not found in model"
            logger.warning(msg)
            messages.append(msg)
            skipped += 1
            continue
        
        # Retrieve unit object using helpers.fetch_object for flexibility
        unit = helpers.fetch_object(osm_model, "BuildingUnit", unit_handle, unit_name)
        if not unit:
            identifier = unit_handle if unit_handle else unit_name
            msg = f"Building unit '{identifier}' not found in model"
            logger.warning(msg)
            messages.append(msg)
            skipped += 1
            continue
        
        # Assign unit to space
        space_opt.get().setBuildingUnit(unit)
        count += 1
    
    # Determine status
    status = "SUCCESS" if count > 0 else "ERROR"
    
    logger.info(f"Assigned building units to {count} spaces. Skipped {skipped} entries.")
    
    return {
        "status": status,
        "assigned": count,
        "skipped": skipped,
        "messages": messages
    }

def remove_unit_from_spaces(osm_model: openstudio.model.Model, space_handles: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Remove the BuildingUnit assignment from specified spaces (or all if none provided).

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - space_handles (Optional[List[str]]): List of space handles to process. 
      If None or empty, the operation will attempt to remove units from ALL spaces in the model.

    Returns:
    - Dict[str, Any]: A dictionary containing:
        - 'status': 'SUCCESS' if successful, 'ERROR' if no spaces found or processed
        - 'modified': Number of spaces that had their unit removed
        - 'total_processed': Total number of spaces checked
        - 'messages': List of valid actions or warnings
    """
    logger.info("Starting task to remove building units from spaces...")
    
    modified_count = 0
    messages = []
    
    # Determine target spaces
    if space_handles:
        target_spaces = []
        for handle in space_handles:
            space_opt = osm_model.getSpace(openstudio.toUUID(handle))
            if space_opt.is_initialized():
                target_spaces.append(space_opt.get())
            else:
                msg = f"Warning: Space with handle {handle} not found."
                logger.warning(msg)
                messages.append(msg)
    else:
        target_spaces = osm_model.getSpaces()
        if not target_spaces:
            msg = "No spaces found in the model."
            logger.warning(msg)
            return {"status": "ERROR", "modified": 0, "total_processed": 0, "messages": [msg]}
            
    # Process spaces
    for space in target_spaces:
        if space.buildingUnit().is_initialized():
            space.resetBuildingUnit()
            modified_count += 1
            
    status = "SUCCESS"
    completion_msg = f"Successfully removed building units from {modified_count} spaces out of {len(target_spaces)} processed."
    logger.info(completion_msg)
    messages.append(completion_msg)
    
    return {
        "status": status,
        "modified": modified_count,
        "total_processed": len(target_spaces),
        "messages": messages
    }

def get_spaces_in_unit(osm_model: openstudio.model.Model, 
                       unit_handle: Optional[str] = None, 
                       unit_name: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Retrieve all spaces assigned to a specific BuildingUnit.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - unit_handle (str, optional): The handle of the unit.
    - unit_name (str, optional): The name of the unit.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries representing the spaces in the unit.
                             Returns empty list if unit not found or has no spaces.
    """
    # Import locally to avoid circular dependency
    from openstudio_toolkit.osm_objects import spaces

    target_unit = helpers.fetch_object(osm_model, "BuildingUnit", unit_handle, unit_name)
    
    if not target_unit:
        identifier = unit_handle if unit_handle else unit_name
        logger.warning(f"Building unit '{identifier}' not found.")
        return []

    # Get spaces associated with the unit
    unit_spaces = target_unit.spaces()
    logger.info(f"Found {len(unit_spaces)} spaces in unit '{target_unit.name().get() if target_unit.name().is_initialized() else 'Unnamed Unit'}'.")
    
    # Convert space objects to dictionaries
    return [spaces.get_space_object_as_dict(osm_model, _object_ref=space) for space in unit_spaces]

def delete_building_unit(osm_model: openstudio.model.Model, 
                         unit_handle: Optional[str] = None, 
                         unit_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Delete a BuildingUnit object from the model.
    Note: Spaces assigned to this unit will simply be unassigned (orphaned), not deleted.
    
    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - unit_handle (str, optional): The handle of the unit.
    - unit_name (str, optional): The name of the unit.
    
    Returns:
    - Dict[str, Any]: Status dictionary with keys:
        - 'status': 'SUCCESS' or 'ERROR'
        - 'message': Description of the action taken
    """
    target_unit = helpers.fetch_object(osm_model, "BuildingUnit", unit_handle, unit_name)
    identifier = unit_name if unit_name else (unit_handle if unit_handle else "Unknown")
    
    if not target_unit:
        msg = f"Building unit '{identifier}' not found in model."
        logger.warning(msg)
        return {
            "status": "ERROR",
            "message": msg
        }
    
    initial_name = target_unit.name().get() if target_unit.name().is_initialized() else "Unnamed"
    
    # Remove the unit itself
    target_unit.remove()
    
    action_msg = f"Deleted building unit '{initial_name}'."
    logger.info(action_msg)
    
    return {
        "status": "SUCCESS",
        "message": action_msg
    }
