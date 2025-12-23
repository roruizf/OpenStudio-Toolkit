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
        'Name': target_story.name().get() if target_story.name().is_initialized() else "Unnamed Story",
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

def set_stories_to_spaces(osm_model: openstudio.model.Model, space_story_dict_list: List[Dict[str, str]]) -> None:
    """
    Assign BuildingStory objects to Spaces based on a mapping list.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - space_story_dict_list (List[Dict[str, str]]): List of dicts with 'Handle' (Space) and 'Story' (Name).

    Returns:
    - None
    """
    count = 0
    for entry in space_story_dict_list:
        space_handle = entry.get('Handle')
        story_name = entry.get('Story')
        
        if not space_handle or not story_name:
            continue
            
        space_opt = osm_model.getSpace(openstudio.toUUID(space_handle))
        story_opt = osm_model.getBuildingStoryByName(story_name)
        
        if space_opt.is_initialized() and story_opt.is_initialized():
            space_opt.get().setBuildingStory(story_opt.get())
            count += 1
        else:
            logger.warning(f"Could not assign story '{story_name}' to space handle {space_handle}.")

    logger.info(f"Assigned stories to {count} spaces.")
