import openstudio
import pandas as pd
import numpy as np
import logging
from typing import Dict, Any, List, Optional
from openstudio_toolkit.utils import helpers

# Configure logger
logger = logging.getLogger(__name__)

def get_building_story_as_dict(
    osm_model: openstudio.model.Model, 
    story_handle: Optional[str] = None, 
    story_name: Optional[str] = None, 
    _object_ref: Optional[openstudio.model.BuildingStory] = None
) -> Dict[str, Any]:
    """
    Retrieve attributes of a BuildingStory object from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - story_handle (str, optional): The handle of the story to retrieve.
    - story_name (str, optional): The name of the story to retrieve.
    - _object_ref (openstudio.model.BuildingStory, optional): Direct object reference.

    Returns:
    - Dict[str, Any]: A dictionary containing story attributes.
    """
    target_story = helpers.fetch_object(
        osm_model, "BuildingStory", story_handle, story_name, _object_ref)

    if target_story is None:
        return {}

    return {
        'Handle': str(target_story.handle()),
        'Name': target_story.name().get() if target_story.name().is_initialized() else None,
        'Nominal Z Coordinate {m}': target_story.nominalZCoordinate().get() if target_story.nominalZCoordinate().is_initialized() else None,
        'Nominal Floor to Floor Height {m}': target_story.nominalFloortoFloorHeight().get() if target_story.nominalFloortoFloorHeight().is_initialized() else None,
        'Default Construction Set Name': target_story.defaultConstructionSet().get().name().get() if target_story.defaultConstructionSet().is_initialized() else None,
        'Default Schedule Set Name': target_story.defaultScheduleSet().get().name().get() if target_story.defaultScheduleSet().is_initialized() else None,
        'Group Rendering Name': target_story.renderingColor().get().name().get() if target_story.renderingColor().is_initialized() else None,
        'Nominal Floor to Ceiling Height {m}': target_story.nominalFloortoCeilingHeight().get() if target_story.nominalFloortoCeilingHeight().is_initialized() else None
    }

def get_all_building_stories_as_dicts(osm_model: openstudio.model.Model) -> List[Dict[str, Any]]:
    """
    Retrieve attributes for all BuildingStory objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing story attributes.
    """
    all_objects = osm_model.getBuildingStorys()
    return [get_building_story_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_building_stories_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all BuildingStory attributes and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all building story attributes.
    """
    all_objects_dicts = get_all_building_stories_as_dicts(osm_model)
    df = pd.DataFrame(all_objects_dicts)

    if not df.empty and 'Name' in df.columns:
        df = df.sort_values(by='Name', ascending=True).reset_index(drop=True)

    logger.info(f"Retrieved {len(df)} building story objects from the model.")
    return df

def create_new_building_stories_objects(osm_model: openstudio.model.Model, building_stories_to_create_df: pd.DataFrame) -> None:
    """
    Create new BuildingStory objects based on a DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - building_stories_to_create_df (pd.DataFrame): DataFrame of story data to create.

    Returns:
    - None
    """
    df = building_stories_to_create_df.replace(np.nan, None)
    count = 0

    for _, row in df.iterrows():
        new_story = openstudio.model.BuildingStory(osm_model)
        if row['Name']:
            new_story.setName(row['Name'])

        if row['Nominal Z Coordinate {m}'] is not None:
            new_story.setNominalZCoordinate(row['Nominal Z Coordinate {m}'])

        if row['Nominal Floor to Floor Height {m}'] is not None:
            new_story.setNominalFloortoFloorHeight(row['Nominal Floor to Floor Height {m}'])

        if row['Default Construction Set Name']:
            const_set_opt = osm_model.getDefaultConstructionSetByName(row['Default Construction Set Name'])
            if const_set_opt.is_initialized():
                new_story.setDefaultConstructionSet(const_set_opt.get())

        if row['Default Schedule Set Name']:
            sched_set_opt = osm_model.getDefaultScheduleSetByName(row['Default Schedule Set Name'])
            if sched_set_opt.is_initialized():
                new_story.setDefaultScheduleSet(sched_set_opt.get())

        if row['Group Rendering Name']:
            render_opt = osm_model.getRenderingColorByName(row['Group Rendering Name'])
            if render_opt.is_initialized():
                new_story.setRenderingColor(render_opt.get())
            else:
                new_color = openstudio.model.RenderingColor(osm_model)
                new_color.setName(row['Group Rendering Name'])
                new_story.setRenderingColor(new_color)

        if row['Nominal Floor to Ceiling Height {m}'] is not None:
            new_story.setNominalFloortoCeilingHeight(row['Nominal Floor to Ceiling Height {m}'])
        
        count += 1

    logger.info(f"Successfully created {count} new BuildingStory objects.")

def update_building_stories_objects(osm_model: openstudio.model.Model, building_stories_to_update_df: pd.DataFrame) -> None:
    """
    Update attributes of existing BuildingStory objects based on a DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - building_stories_to_update_df (pd.DataFrame): DataFrame containing updated story data.

    Returns:
    - None
    """
    df = building_stories_to_update_df.replace(np.nan, None)
    count = 0

    for _, row in df.iterrows():
        target_story = helpers.fetch_object(osm_model, "BuildingStory", row.get('Handle'), row.get('Name'))
        if not target_story:
            continue

        if row.get('Name'):
            target_story.setName(row['Name'])

        if row.get('Nominal Z Coordinate {m}') is not None:
            target_story.setNominalZCoordinate(row['Nominal Z Coordinate {m}'])

        if row.get('Nominal Floor to Floor Height {m}') is not None:
            target_story.setNominalFloortoFloorHeight(row['Nominal Floor to Floor Height {m}'])

        if row.get('Nominal Floor to Ceiling Height {m}') is not None:
            target_story.setNominalFloortoCeilingHeight(row['Nominal Floor to Ceiling Height {m}'])

        if row.get('Default Construction Set Name'):
            const_opt = osm_model.getDefaultConstructionSetByName(row['Default Construction Set Name'])
            if const_opt.is_initialized():
                target_story.setDefaultConstructionSet(const_opt.get())

        if row.get('Default Schedule Set Name'):
            sched_opt = osm_model.getDefaultScheduleSetByName(row['Default Schedule Set Name'])
            if sched_opt.is_initialized():
                target_story.setDefaultScheduleSet(sched_opt.get())

        if row.get('Group Rendering Name'):
            render_opt = osm_model.getRenderingColorByName(row['Group Rendering Name'])
            if render_opt.is_initialized():
                target_story.setRenderingColor(render_opt.get())
        
        count += 1

    logger.info(f"Successfully updated {count} BuildingStory objects.")

def assign_spaces_to_building_stories(osm_model: openstudio.model.Model, space_story_mapping: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Assign BuildingStory objects to Space objects based on a mapping list.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - space_story_mapping (List[Dict[str, str]]): List of dictionaries, where each dict contains:
        - 'Space Handle': The space handle (string) - required
        - 'Building Story Handle': The story handle (string) - optional
        - 'Building Story Name': The story name (string) - optional
        Note: Must provide either 'Building Story Handle' OR 'Building Story Name'

    Returns:
    - Dict[str, Any]: A dictionary containing:
        - 'status': 'SUCCESS' if at least one assignment succeeded, 'ERROR' if all failed
        - 'assigned': Number of spaces successfully assigned to stories
        - 'skipped': Number of entries skipped due to errors
        - 'messages': List of warning/error messages
    """
    count = 0
    skipped = 0
    messages = []
    
    for entry in space_story_mapping:
        space_handle = entry.get('Space Handle')
        story_handle = entry.get('Building Story Handle')
        story_name = entry.get('Building Story Name')
        
        # Validate required space handle
        if not space_handle:
            msg = "Skipping entry: missing 'Space Handle'"
            logger.warning(msg)
            messages.append(msg)
            skipped += 1
            continue
        
        # Validate that at least one story identifier is provided
        if not story_handle and not story_name:
            msg = f"Skipping space {space_handle}: missing both 'Building Story Handle' and 'Building Story Name'"
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
        
        # Retrieve story object using helpers.fetch_object for flexibility
        story = helpers.fetch_object(osm_model, "BuildingStory", story_handle, story_name)
        if not story:
            identifier = story_handle if story_handle else story_name
            msg = f"Building story '{identifier}' not found in model"
            logger.warning(msg)
            messages.append(msg)
            skipped += 1
            continue
        
        # Assign story to space
        space_opt.get().setBuildingStory(story)
        count += 1
    
    # Determine status
    status = "SUCCESS" if count > 0 else "ERROR"
    
    logger.info(f"Assigned building stories to {count} spaces. Skipped {skipped} entries.")
    
    return {
        "status": status,
        "assigned": count,
        "skipped": skipped,
        "messages": messages
    }


def remove_story_from_spaces(osm_model: openstudio.model.Model, space_handles: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Remove the BuildingStory assignment from specified spaces (or all if none provided).

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - space_handles (Optional[List[str]]): List of space handles to process. 
      If None or empty, the operation will attempt to remove stories from ALL spaces in the model.

    Returns:
    - Dict[str, Any]: A dictionary containing:
        - 'status': 'SUCCESS' if successful, 'ERROR' if no spaces found or processed
        - 'modified': Number of spaces that had their story removed
        - 'total_processed': Total number of spaces checked
        - 'messages': List of valid actions or warnings
    """
    logger.info("Starting task to remove building stories from spaces...")
    
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
        if space.buildingStory().is_initialized():
            space.resetBuildingStory()
            modified_count += 1
            
    status = "SUCCESS"
    completion_msg = f"Successfully removed building stories from {modified_count} spaces out of {len(target_spaces)} processed."
    logger.info(completion_msg)
    messages.append(completion_msg)
    
    return {
        "status": status,
        "modified": modified_count,
        "total_processed": len(target_spaces),
        "messages": messages
    }


def get_spaces_in_story(osm_model: openstudio.model.Model, 
                        story_handle: Optional[str] = None, 
                        story_name: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Retrieve all spaces assigned to a specific BuildingStory.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - story_handle (str, optional): The handle of the story.
    - story_name (str, optional): The name of the story.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries representing the spaces in the story.
                            Returns empty list if story not found or has no spaces.
    """
    # Import locally to avoid circular dependency
    from openstudio_toolkit.osm_objects import spaces

    target_story = helpers.fetch_object(osm_model, "BuildingStory", story_handle, story_name)
    
    if not target_story:
        identifier = story_handle if story_handle else story_name
        logger.warning(f"Building story '{identifier}' not found.")
        return []

    # Get spaces associated with the story
    story_spaces = target_story.spaces()
    logger.info(f"Found {len(story_spaces)} spaces in story '{target_story.name().get() if target_story.name().is_initialized() else 'Unnamed Story'}'.")
    
    # Convert space objects to dictionaries
    return [spaces.get_space_object_as_dict(osm_model, _object_ref=space) for space in story_spaces]


def delete_building_story(osm_model: openstudio.model.Model, 
                          story_handle: Optional[str] = None, 
                          story_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Delete a BuildingStory object from the model.
    Note: Spaces assigned to this story will simply be unassigned (orphaned), not deleted.
    
    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - story_handle (str, optional): The handle of the story.
    - story_name (str, optional): The name of the story.
    
    Returns:
    - Dict[str, Any]: Status dictionary with keys:
        - 'status': 'SUCCESS' or 'ERROR'
        - 'message': Description of the action taken
    """
    target_story = helpers.fetch_object(osm_model, "BuildingStory", story_handle, story_name)
    identifier = story_name if story_name else (story_handle if story_handle else "Unknown")
    
    if not target_story:
        msg = f"Building story '{identifier}' not found in model."
        logger.warning(msg)
        return {
            "status": "ERROR",
            "message": msg
        }
    
    initial_name = target_story.name().get() if target_story.name().is_initialized() else "Unnamed"
    
    # Remove the story itself
    target_story.remove()
    
    action_msg = f"Deleted building story '{initial_name}'."
    logger.info(action_msg)
    
    return {
        "status": "SUCCESS",
        "message": action_msg
    }

