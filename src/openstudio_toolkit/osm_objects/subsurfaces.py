import openstudio
import pandas as pd
import logging
from typing import List, Dict, Any, Optional

from openstudio_toolkit.utils import helpers

# Configure logger
logger = logging.getLogger(__name__)

import math

# --------------------------------------------------
#  ***** OS:SubSurface *****************************
# --------------------------------------------------

def get_subsurface_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: Optional[str] = None, 
    name: Optional[str] = None, 
    _object_ref: Optional[openstudio.model.SubSurface] = None,
    method: str = '8-Point',
    enriched_data: bool = False
) -> Dict[str, Any]:
    """
    Retrieve attributes of an OS:SubSurface from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.SubSurface, optional): Direct object reference.
    - method (str): Orientation classification method ('4-Point' or '8-Point').
    - enriched_data (bool): If True, includes calculated fields like Orientation and Azimuth. Defaults to False.

    Returns:
    - Dict[str, Any]: A dictionary containing subsurface attributes.
    """
    target_object = helpers.fetch_object(
        osm_model, "SubSurface", handle, name, _object_ref)

    if target_object is None:
        return {}
    
    # 1. Pure OSM Attributes (Mirroring .osm file)
    subsurface_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Sub Surface Type': target_object.subSurfaceType(),
        'Construction Name': target_object.construction().get().name().get() if target_object.construction().is_initialized() else None,
        'Surface Name': target_object.surface().get().name().get() if target_object.surface().is_initialized() else None,
        'Outside Boundary Condition Object': target_object.outsideBoundaryCondition(),
        'View Factor to Ground': None,
        'Multiplier': target_object.multiplier(),
        'Number of Vertices': None
    }

    # 2. Enriched Data (Added Intelligence/Calculated Fields)
    if enriched_data:
        orientation_data = calculate_subsurface_orientation(target_object, method)
        subsurface_dict.update({
            'Azimuth': orientation_data['Azimuth'],
            'Orientation': orientation_data['Orientation'],
            'Frame and Divider Name': target_object.windowPropertyFrameAndDivider().get().name().get() if target_object.windowPropertyFrameAndDivider().is_initialized() else None,
            'Number of Vertices': len(target_object.vertices())
        })

    return subsurface_dict

def get_all_subsurface_objects_as_dicts(osm_model: openstudio.model.Model) -> List[Dict[str, Any]]:
    """
    Retrieve attributes for all OS:SubSurface objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing subsurface attributes.
    """
    all_objects = osm_model.getSubSurfaces()
    return [get_subsurface_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_subsurface_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:SubSurface objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all SubSurface attributes.
    """
    all_objects_dicts = get_all_subsurface_objects_as_dicts(osm_model)
    df = pd.DataFrame(all_objects_dicts)

    if not df.empty and 'Name' in df.columns:
        df = df.sort_values(by='Name', ascending=True).reset_index(drop=True)

    logger.info(f"Retrieved {len(df)} SubSurface objects from the model.")
    return df

def calculate_subsurface_orientation(subsurface: openstudio.model.SubSurface, method: str = '8-Point') -> Dict[str, Any]:
    """
    Calculate the absolute azimuth and classification for a subsurface.
    Uses the parent surface's normal and space rotation.
    
    Parameters:
    - method (str): '4-Point' for cardinal directions, '8-Point' for cardinal+intercardinal (default).
    """
    parent_surface_opt = subsurface.surface()
    if not parent_surface_opt.is_initialized():
        return {'Azimuth': None, 'Orientation': 'Unknown'}
        
    parent_surface = parent_surface_opt.get()
    
    # 1. Get relative azimuth from parent normal
    normal = parent_surface.outwardNormal()
    rel_azimuth = math.degrees(math.atan2(normal.x(), normal.y())) % 360

    # 2. Get Rotation offset
    space = parent_surface.space().get() if parent_surface.space().is_initialized() else None
    if not space:
        return {'Azimuth': round(rel_azimuth, 2), 'Orientation': 'Unknown'}
        
    space_rot = space.directionofRelativeNorth()
    building_rot = space.model().getBuilding().northAxis()
    total_offset = (space_rot + building_rot) % 360

    # 3. Calculate Absolute Azimuth
    abs_azimuth = (rel_azimuth + total_offset) % 360

    # 4. Classify
    label = "Unknown"
    if method == '4-Point':
        if 315 <= abs_azimuth < 360 or 0 <= abs_azimuth < 45: label = "North"
        elif 45 <= abs_azimuth < 135: label = "East"
        elif 135 <= abs_azimuth < 225: label = "South"
        elif 225 <= abs_azimuth < 315: label = "West"
    else: # Default 8-Point
        if (abs_azimuth >= 337.5) or (abs_azimuth < 22.5): label = "North"
        elif 22.5 <= abs_azimuth < 67.5: label = "Northeast"
        elif 67.5 <= abs_azimuth < 112.5: label = "East"
        elif 112.5 <= abs_azimuth < 157.5: label = "Southeast"
        elif 157.5 <= abs_azimuth < 202.5: label = "South"
        elif 202.5 <= abs_azimuth < 247.5: label = "Southwest"
        elif 247.5 <= abs_azimuth < 292.5: label = "West"
        elif 292.5 <= abs_azimuth < 337.5: label = "Northwest"

    return {'Azimuth': round(abs_azimuth, 2), 'Orientation': label}