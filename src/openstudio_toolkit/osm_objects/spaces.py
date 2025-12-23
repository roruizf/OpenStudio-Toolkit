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
        'Name': target_object.name().get() if target_object.name().is_initialized() else "Unnamed Space",
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
