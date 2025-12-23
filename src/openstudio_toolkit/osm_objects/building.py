import openstudio
import pandas as pd

import logging
from typing import List, Dict, Any, Optional

# Configure logger
logger = logging.getLogger(__name__)

def get_building_object_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve attributes of the Building object from the OpenStudio Model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all Building attributes.
    """

    # Get building in the OpenStudio model.
    building = osm_model.getBuilding()

    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(building.handle())],
        'Name': [building.name().get()],
        'Building Sector Type': None,
        'North Axis {deg}': [building.northAxis()],
        'Nominal Floor to Floor Height {m}': None,
        'Space Type Name': [building.spaceType().get().name().get() if not building.spaceType().isNull() else None],
        'Default Construction Set Name': [building.defaultConstructionSet().get().name().get() if not building.defaultConstructionSet().isNull() else None],
        'Default Schedule Set Name': [building.defaultScheduleSet().get().name().get() if not building.defaultScheduleSet().isNull() else None],
        'Standards Number of Stories': None,
        'Standards Number of Above Ground Stories': None,
        'Standards Template': None,
        'Standards Building Type': [building.standardsBuildingType().get() if not building.standardsBuildingType().isNull() else None],
        'Standards Number of Living Units': None,
        'Relocatable': None,
        'Nominal Floor to Ceiling Height {m}': None
    }

    # Create a DataFrame of building.
    building_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        building_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    building_df = building_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    logger.info(f"Retrieved Building object from the model.")
    return building_df
