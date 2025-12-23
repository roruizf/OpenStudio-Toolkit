import openstudio
import pandas as pd
import logging
from typing import List, Dict, Any, Optional

from openstudio_toolkit.utils import helpers

# Configure logger
logger = logging.getLogger(__name__)

# --------------------------------------------------
#  ***** OS:Surface ********************************
# --------------------------------------------------

def get_surface_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: Optional[str] = None, 
    name: Optional[str] = None, 
    _object_ref: Optional[openstudio.model.Surface] = None
) -> Dict[str, Any]:
    """
    Retrieve attributes of an OS:Surface from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.Surface, optional): Direct object reference.

    Returns:
    - Dict[str, Any]: A dictionary containing surface attributes.
    """
    target_object = helpers.fetch_object(
        osm_model, "Surface", handle, name, _object_ref)

    if target_object is None:
        return {}

    return {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else "Unnamed Surface",
        'Surface Type': target_object.surfaceType(),
        'Construction Name': target_object.construction().get().name().get() if target_object.construction().is_initialized() else None,        
        'Space Name': target_object.space().get().name().get() if target_object.space().is_initialized() else None,
        'Outside Boundary Condition': target_object.outsideBoundaryCondition(),
        'Adjacent Surface Name': target_object.adjacentSurface().get().name().get() if target_object.adjacentSurface().is_initialized() else None,
        'Sun Exposure': target_object.sunExposure(),
        'Wind Exposure': target_object.windExposure(),
        'Number of Vertices': len(target_object.vertices())
    }

def get_all_surface_objects_as_dicts(osm_model: openstudio.model.Model) -> List[Dict[str, Any]]:
    """
    Retrieve attributes for all OS:Surface objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing surface attributes.
    """
    all_objects = osm_model.getSurfaces()
    return [get_surface_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_surface_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:Surface objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all Surface attributes.
    """
    all_objects_dicts = get_all_surface_objects_as_dicts(osm_model)
    df = pd.DataFrame(all_objects_dicts)

    if not df.empty and 'Name' in df.columns:
        df = df.sort_values(by='Name', ascending=True).reset_index(drop=True)

    logger.info(f"Retrieved {len(df)} Surface objects from the model.")
    return df
