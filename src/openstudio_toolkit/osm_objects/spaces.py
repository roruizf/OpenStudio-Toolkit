import openstudio
import pandas as pd
import logging
from typing import List, Dict, Any, Optional

from openstudio_toolkit.utils import helpers

# Configure logger
logger = logging.getLogger(__name__)

import math

# --------------------------------------------------
#  ***** OS:Space **********************************
# --------------------------------------------------

def get_space_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: Optional[str] = None, 
    name: Optional[str] = None, 
    _object_ref: Optional[openstudio.model.Space] = None,
    enriched_data: bool = False
) -> Dict[str, Any]:
    """
    Retrieve attributes of an OS:Space from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.Space, optional): Direct object reference.
    - enriched_data (bool): If True, includes calculated fields like Orientation. Defaults to False.

    Returns:
    - Dict[str, Any]: A dictionary containing space attributes.
    """
    target_object = helpers.fetch_object(
        osm_model, "Space", handle, name, _object_ref)

    if target_object is None:
        return {}

    # 1. Pure OSM Attributes (Mirroring .osm file)
    space_dict = {
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

    # 2. Enriched Data (Added Intelligence/Calculated Fields)
    if enriched_data:
        space_dict['Orientation'] = calculate_space_orientation(target_object)

    return space_dict

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
        Each dict MUST contain:
        - 'Handle': The space handle (required identifier).
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
        # 1. Identify Target Space (ONLY via Handle)
        handle = entry.get('Handle')
        
        if not handle:
            msg = "Skipping entry: 'Handle' is required for updates."
            logger.warning(msg)
            messages.append(msg)
            errors += 1
            continue

        target_space = helpers.fetch_object(osm_model, "Space", handle=handle)
        
        if not target_space:
            msg = f"Skipping entry: Space with handle '{handle}' not found."
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

def calculate_space_orientation(space: openstudio.model.Space) -> str:
    """
    Determine a single representative absolute orientation for a space based on the area-weighted 
    outward normal vectors of its exterior surfaces, accounting for building rotation.
    """
    total_x = 0.0
    total_y = 0.0
    exterior_found = False
    
    # Area-by-cardinal direction trackers (Absolute)
    orientations_area = {
        "North": 0.0,
        "Northeast": 0.0,
        "East": 0.0,
        "Southeast": 0.0,
        "South": 0.0,
        "Southwest": 0.0,
        "West": 0.0,
        "Northwest": 0.0
    }

    # Total Rotation (Space + Building) in degrees clockwise
    space_rot = space.directionofRelativeNorth()
    building_rot = space.model().getBuilding().northAxis()
    total_rot_deg = (space_rot + building_rot) % 360
    rad = math.radians(total_rot_deg)

    for surface in space.surfaces():
        if surface.outsideBoundaryCondition() == "Outdoors" and surface.surfaceType().lower() == "wall":
            exterior_found = True
            area = surface.grossArea()
            normal = surface.outwardNormal()
            
            # Rotate local normal vector to Absolute North coordinates
            # CW rotation: (x', y') = (x cos theta + y sin theta, -x sin theta + y cos theta)
            abs_x = normal.x() * math.cos(rad) + normal.y() * math.sin(rad)
            abs_y = -normal.x() * math.sin(rad) + normal.y() * math.cos(rad)
            
            # Accumulate vector components
            total_x += abs_x * area
            total_y += abs_y * area
            
            # Categorize this specific surface for the tie-breaker
            abs_az_surf = math.degrees(math.atan2(abs_x, abs_y)) % 360
            
            if (abs_az_surf >= 337.5) or (abs_az_surf < 22.5): orientations_area["North"] += area
            elif 22.5 <= abs_az_surf < 67.5: orientations_area["Northeast"] += area
            elif 67.5 <= abs_az_surf < 112.5: orientations_area["East"] += area
            elif 112.5 <= abs_az_surf < 157.5: orientations_area["Southeast"] += area
            elif 157.5 <= abs_az_surf < 202.5: orientations_area["South"] += area
            elif 202.5 <= abs_az_surf < 247.5: orientations_area["Southwest"] += area
            elif 247.5 <= abs_az_surf < 292.5: orientations_area["West"] += area
            elif 292.5 <= abs_az_surf < 337.5: orientations_area["Northwest"] += area

    if not exterior_found:
        return "Interior"

    # Final Resultant Azimuth
    vector_magnitude = math.sqrt(total_x**2 + total_y**2)
    
    # Tie-breaker for balanced exposures
    if vector_magnitude < 0.01:
        max_orient = max(orientations_area, key=orientations_area.get)
        return max_orient if orientations_area[max_orient] > 0 else "Interior"

    # Resultant absolute azimuth
    res_azimuth = math.degrees(math.atan2(total_x, total_y)) % 360
    
    if (res_azimuth >= 337.5) or (res_azimuth < 22.5): return "North"
    elif 22.5 <= res_azimuth < 67.5: return "Northeast"
    elif 67.5 <= res_azimuth < 112.5: return "East"
    elif 112.5 <= res_azimuth < 157.5: return "Southeast"
    elif 157.5 <= res_azimuth < 202.5: return "South"
    elif 202.5 <= res_azimuth < 247.5: return "Southwest"
    elif 247.5 <= res_azimuth < 292.5: return "West"
    elif 292.5 <= res_azimuth < 337.5: return "Northwest"
    return "Unknown"