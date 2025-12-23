import openstudio
import pandas as pd
import logging
from typing import List, Dict, Any, Optional

from openstudio_toolkit.utils import helpers

# Configure logger
logger = logging.getLogger(__name__)

# --------------------------------------------------
#  ***** OS:Space **********************************
# --------------------------------------------------

def get_space_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: Optional[str] = None, 
    name: Optional[str] = None, 
    _object_ref: Optional[openstudio.model.Space] = None
) -> Dict[str, Any]:
    """
    Retrieve attributes of an OS:Space from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.Space, optional): Direct object reference.

    Returns:
    - Dict[str, Any]: A dictionary containing space attributes.
    """
    target_object = helpers.fetch_object(
        osm_model, "Space", handle, name, _object_ref)

    if target_object is None:
        return {}

    return {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Space Type Name': target_object.spaceType().get().name().get() if target_object.spaceType().is_initialized() else None,
        'Default Construction Set Name': target_object.defaultConstructionSet().get().name().get() if target_object.defaultConstructionSet().is_initialized() else None,
        'Default Schedule Set Name': target_object.defaultScheduleSet().get().name().get() if target_object.defaultScheduleSet().is_initialized() else None,
        'Direction of Relative North {deg}': target_object.directionofRelativeNorth(),
        'X Origin {m}': target_object.xOrigin(),
        'Y Origin {m}': target_object.yOrigin(),
        'Z Origin {m}': target_object.zOrigin(),
        'Building Story Name': target_object.buildingStory().get().name().get() if target_object.buildingStory().is_initialized() else None,
        'Thermal Zone Name': target_object.thermalZone().get().name().get() if target_object.thermalZone().is_initialized() else None,
        'Part of Total Floor Area': target_object.partofTotalFloorArea(),
        'Design Specification Outdoor Air Object Name': target_object.designSpecificationOutdoorAir().get().name().get() if target_object.designSpecificationOutdoorAir().is_initialized() else None,
        'Building Unit Name': target_object.buildingUnit().get().name().get() if target_object.buildingUnit().is_initialized() else None,
        'Volume {m3}': target_object.volume(),
        'Ceiling Height {m}': target_object.ceilingHeight(),
        'Floor Area {m2}': target_object.floorArea()
    }

def get_all_space_objects_as_dicts(osm_model: openstudio.model.Model) -> List[Dict[str, Any]]:
    """
    Retrieve attributes for all OS:Space objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing space attributes.
    """
    all_objects = osm_model.getSpaces()
    return [get_space_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_space_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:Space objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all Space attributes.
    """
    all_objects_dicts = get_all_space_objects_as_dicts(osm_model)
    df = pd.DataFrame(all_objects_dicts)

    if not df.empty and 'Name' in df.columns:
        df = df.sort_values(by='Name', ascending=True).reset_index(drop=True)

    logger.info(f"Retrieved {len(df)} Space objects from the model.")
    return df


def update_spaces_data(osm_model: openstudio.model.Model, spaces_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Batch update non-geometric attributes of spaces.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - spaces_data (List[Dict[str, Any]]): List of dictionaries containing space data to update.
        Each dictionary should contain:
        - 'Handle': The space handle (preferred identifier) OR 'Name' (alternative identifier).
        Optional attributes to update:
        - 'Name': New name for the space.
        - 'Space Type Name': Name of the SpaceType to assign.
        - 'Building Story Name': Name of the BuildingStory to assign.
        - 'Thermal Zone Name': Name of the ThermalZone to assign.
        - 'Default Construction Set Name': Name of the Construction Set to assign.
        - 'Default Schedule Set Name': Name of the Schedule Set to assign.
        - 'Part of Total Floor Area': Boolean (True/False).
        - 'Design Specification Outdoor Air Object Name': Name of the DesignSpecOA object.

    Returns:
    - Dict[str, Any]: Status dictionary with 'status', 'updated_count', 'errors', 'messages'.
    """
    updated_count = 0
    errors = 0
    messages = []
    
    logger.info("Starting batch update of spaces...")

    for entry in spaces_data:
        # 1. Identify Target Space
        handle = entry.get('Handle')
        name = entry.get('Name')
        
        target_space = helpers.fetch_object(osm_model, "Space", handle, name)
        
        if not target_space:
            identifier = handle if handle else name
            msg = f"Skipping entry: Space '{identifier}' not found."
            logger.warning(msg)
            messages.append(msg)
            errors += 1
            continue
            
        changes_made = False
        
        # 2. Update Name (if different)
        if 'Name' in entry and entry['Name'] and entry['Name'] != target_space.name().get():
             target_space.setName(entry['Name'])
             changes_made = True

        # 3. Update Relationships (Lookup by Name)
        
        # Space Type
        if 'Space Type Name' in entry:
            st_name = entry['Space Type Name']
            if st_name: # If string provided, look it up
                # Can use generic helper or specific get method. Generic is safer if we trust helper.
                # However, helper returns 'Any', we need SpaceType. 
                # Let's use direct model lookup for clarity on type
                st_opt = osm_model.getSpaceTypeByName(st_name)
                if st_opt.is_initialized():
                    target_space.setSpaceType(st_opt.get())
                    changes_made = True
                else:
                    msg = f"Warning: Space Type '{st_name}' not found for space '{target_space.name().get()}'"
                    logger.warning(msg)
                    messages.append(msg)
            else: # If None/Empty string provided, clear the assignment? 
                # Usually we reset if explicitly None, but 'if st_name' catches that.
                # Let's handle explicit reset if needed, but for now strict update.
                pass 

        # Building Story
        if 'Building Story Name' in entry:
            story_name = entry['Building Story Name']
            if story_name:
                story_opt = osm_model.getBuildingStoryByName(story_name)
                if story_opt.is_initialized():
                    target_space.setBuildingStory(story_opt.get())
                    changes_made = True
                else:
                    msg = f"Warning: Building Story '{story_name}' not found for space '{target_space.name().get()}'"
                    logger.warning(msg)
                    messages.append(msg)

        # Thermal Zone
        if 'Thermal Zone Name' in entry:
            tz_name = entry['Thermal Zone Name']
            if tz_name:
                tz_opt = osm_model.getThermalZoneByName(tz_name)
                if tz_opt.is_initialized():
                    target_space.setThermalZone(tz_opt.get())
                    changes_made = True
                else:
                    msg = f"Warning: Thermal Zone '{tz_name}' not found for space '{target_space.name().get()}'"
                    logger.warning(msg)
                    messages.append(msg)

        # Default Construction Set
        if 'Default Construction Set Name' in entry:
            cs_name = entry['Default Construction Set Name']
            if cs_name:
                cs_opt = osm_model.getDefaultConstructionSetByName(cs_name)
                if cs_opt.is_initialized():
                    target_space.setDefaultConstructionSet(cs_opt.get())
                    changes_made = True
                else:
                     msg = f"Warning: Construction Set '{cs_name}' not found for space '{target_space.name().get()}'"
                     logger.warning(msg)
                     messages.append(msg)

        # Default Schedule Set
        if 'Default Schedule Set Name' in entry:
            ss_name = entry['Default Schedule Set Name']
            if ss_name:
                ss_opt = osm_model.getDefaultScheduleSetByName(ss_name)
                if ss_opt.is_initialized():
                    target_space.setDefaultScheduleSet(ss_opt.get())
                    changes_made = True
                else:
                     msg = f"Warning: Schedule Set '{ss_name}' not found for space '{target_space.name().get()}'"
                     logger.warning(msg)
                     messages.append(msg)

        # Design Spec OA
        if 'Design Specification Outdoor Air Object Name' in entry:
            oa_name = entry['Design Specification Outdoor Air Object Name']
            if oa_name:
                oa_opt = osm_model.getDesignSpecificationOutdoorAirByName(oa_name)
                if oa_opt.is_initialized():
                    target_space.setDesignSpecificationOutdoorAir(oa_opt.get())
                    changes_made = True
                else:
                     msg = f"Warning: Design Spec OA '{oa_name}' not found for space '{target_space.name().get()}'"
                     # logger.warning(msg) # Optional logging
                     messages.append(msg)

        # 4. Simple Types
        if 'Part of Total Floor Area' in entry:
            val = entry['Part of Total Floor Area']
            if val is not None:
                target_space.setPartofTotalFloorArea(bool(val))
                changes_made = True

        if changes_made:
            updated_count += 1

    status = "SUCCESS" if updated_count > 0 or (len(spaces_data) > 0 and errors == 0) else "ERROR"
    if errors > 0 and updated_count > 0:
        status = "PARTIAL_SUCCESS"
        
    logger.info(f"Finished batch update. Updated: {updated_count}, Errors: {errors}")
    
    return {
        "status": status,
        "updated_count": updated_count,
        "errors": errors,
        "messages": messages
    }
