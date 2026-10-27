import logging

import openstudio
import pandas as pd

from openstudio_toolkit._sdk import opt, optional_name
from openstudio_toolkit.osm_objects._base import build_dataframe

# Configure logger
logger = logging.getLogger(__name__)

BUILDING_COLUMNS = (
    'Handle',
    'Name',
    'Building Sector Type',
    'North Axis {deg}',
    'Nominal Floor to Floor Height {m}',
    'Space Type Name',
    'Default Construction Set Name',
    'Default Schedule Set Name',
    'Standards Number of Stories',
    'Standards Number of Above Ground Stories',
    'Standards Template',
    'Standards Building Type',
    'Standards Number of Living Units',
    'Relocatable',
    'Nominal Floor to Ceiling Height {m}',
)


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
        'Handle': str(building.handle()),
        'Name': opt(building.name()),
        'Building Sector Type': None,
        'North Axis {deg}': building.northAxis(),
        'Nominal Floor to Floor Height {m}': None,
        'Space Type Name': optional_name(building.spaceType()),
        'Default Construction Set Name': optional_name(building.defaultConstructionSet()),
        'Default Schedule Set Name': optional_name(building.defaultScheduleSet()),
        'Standards Number of Stories': None,
        'Standards Number of Above Ground Stories': None,
        'Standards Template': None,
        'Standards Building Type': opt(building.standardsBuildingType()),
        'Standards Number of Living Units': None,
        'Relocatable': None,
        'Nominal Floor to Ceiling Height {m}': None
    }

    return build_dataframe(
        [object_attr], "Building", sort_by="Name", columns=BUILDING_COLUMNS)
