import openstudio
import pandas as pd
import logging
from typing import List, Dict, Any, Optional

from openstudio_toolkit.utils import helpers

# Configure logger
logger = logging.getLogger(__name__)

# --------------------------------------------------
#  ***** OS:SubSurface *****************************
# --------------------------------------------------

def get_subsurface_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: Optional[str] = None, 
    name: Optional[str] = None, 
    _object_ref: Optional[openstudio.model.SubSurface] = None
) -> Dict[str, Any]:
    """
    Retrieve attributes of an OS:SubSurface from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.SubSurface, optional): Direct object reference.

    Returns:
    - Dict[str, Any]: A dictionary containing subsurface attributes.
    """
    target_object = helpers.fetch_object(
        osm_model, "SubSurface", handle, name, _object_ref)

    if target_object is None:
        return {}

    return {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Sub Surface Type': target_object.subSurfaceType(),
        'Construction Name': target_object.construction().get().name().get() if target_object.construction().is_initialized() else None,
        'Surface Name': target_object.surface().get().name().get() if target_object.surface().is_initialized() else None,
        'Outside Boundary Condition Object': target_object.outsideBoundaryCondition(),
        'Frame and Divider Name': target_object.windowPropertyFrameAndDivider().get().name().get() if target_object.windowPropertyFrameAndDivider().is_initialized() else None,
        'Multiplier': target_object.multiplier(),
        'Number of Vertices': len(target_object.vertices())
    }

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
