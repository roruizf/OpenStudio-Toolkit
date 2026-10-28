import logging
from typing import Any

import openstudio
import pandas as pd

from openstudio_toolkit._sdk import opt, optional_name, related_name
from openstudio_toolkit.osm_objects._base import build_dataframe

# Configure logger
logger = logging.getLogger(__name__)

#-----------------------------
#--- OS:Controller:OutdoorAir
#-----------------------------

CONTROLLER_OUTDOOR_AIR_COLUMNS = (
    'Handle',
    'Name',
    'Relief Air Outlet Node Name',
    'Return Air Node Name',
    'Mixed Air Node Name',
    'Actuator Node Name',
    'Minimum Outdoor Air Flow Rate {m3/s}',
    'Maximum Outdoor Air Flow Rate {m3/s}',
    'Economizer Control Type',
    'Economizer Control Action Type',
    'Economizer Maximum Limit Dry-Bulb Temperature {C}',
    'Economizer Maximum Limit Enthalpy {J/kg}',
    'Economizer Maximum Limit Dewpoint Temperature {C}',
    'Electronic Enthalpy Limit Curve Name',
    'Economizer Minimum Limit Dry-Bulb Temperature {C}',
    'Lockout Type',
    'Minimum Limit Type',
    'Minimum Outdoor Air Schedule Name',
    'Minimum Fraction of Outdoor Air Schedule Name',
    'Maximum Fraction of Outdoor Air Schedule Name',
    'Controller Mechanical Ventilation',
    'Time of Day Economizer Control Schedule Name',
    'High Humidity Control',
    'Humidistat Control Zone Name',
    'High Humidity Outdoor Air Flow Ratio',
    'Control High Indoor Humidity Based on Outdoor Humidity Ratio',
    'Heat Recovery Bypass Control Type',
    'Economizer Operation Staging',
)


def get_controller_outdoor_air_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: str | None = None, 
    name: str | None = None
) -> dict[str, Any]:
    """
    Retrieve attributes of an OS:Controller:OutdoorAir object from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.

    Returns:
    - Dict[str, Any]: A dictionary containing Controller:OutdoorAir attributes.
    """
    if handle is not None and name is not None:
        raise ValueError(
            "Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError(
            "Either 'handle' or 'name' must be provided.")

    if handle is not None:
        osm_object = osm_model.getControllerOutdoorAir(handle)
        if not osm_object:
            logger.warning(
                f"No Controller:OutdoorAir object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getControllerOutdoorAirByName(name)
        if not osm_object:
            logger.warning(
                f"No Controller:OutdoorAir object found with the name: {name}")
            return {}

    target_object = opt(osm_object)
    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': opt(target_object.name()),
        'Relief Air Outlet Node Name': None,
        'Return Air Node Name': None,
        'Mixed Air Node Name': None,
        'Actuator Node Name': None,
        'Minimum Outdoor Air Flow Rate {m3/s}': 'Autosize' if target_object.isMinimumOutdoorAirFlowRateAutosized() else opt(target_object.minimumOutdoorAirFlowRate()),
        'Maximum Outdoor Air Flow Rate {m3/s}': 'Autosize' if target_object.isMaximumOutdoorAirFlowRateAutosized() else opt(target_object.maximumOutdoorAirFlowRate()),
        'Economizer Control Type': target_object.getEconomizerControlType(),
        'Economizer Control Action Type': target_object.getEconomizerControlActionType(),
        'Economizer Maximum Limit Dry-Bulb Temperature {C}': opt(target_object.getEconomizerMaximumLimitDryBulbTemperature()),
        'Economizer Maximum Limit Enthalpy {J/kg}': opt(target_object.getEconomizerMinimumLimitDryBulbTemperature()),
        'Economizer Maximum Limit Dewpoint Temperature {C}': None,
        'Electronic Enthalpy Limit Curve Name': None,
        'Economizer Minimum Limit Dry-Bulb Temperature {C}': None,
        'Lockout Type': target_object.getLockoutType(),
        'Minimum Limit Type': target_object.getMinimumLimitType(),
        'Minimum Outdoor Air Schedule Name': optional_name(target_object.minimumOutdoorAirSchedule()),
        'Minimum Fraction of Outdoor Air Schedule Name': optional_name(target_object.minimumFractionofOutdoorAirSchedule()),
        'Maximum Fraction of Outdoor Air Schedule Name': optional_name(target_object.maximumFractionofOutdoorAirSchedule()),
        'Controller Mechanical Ventilation': related_name(target_object, "Controller Mechanical Ventilation"),
        'Time of Day Economizer Control Schedule Name': None,
        'High Humidity Control': opt(target_object.getHighHumidityControl()),
        'Humidistat Control Zone Name': None,
        'High Humidity Outdoor Air Flow Ratio': None,
        'Control High Indoor Humidity Based on Outdoor Humidity Ratio': None,
        'Heat Recovery Bypass Control Type': opt(target_object.getHeatRecoveryBypassControlType()),        
        'Economizer Operation Staging': target_object.economizerOperationStaging()
    }
    return object_dict


def get_all_controller_outdoor_air_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict[str, Any]]:
    """
    Retrieve attributes for all OS:Controller:OutdoorAir objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing Controller:OutdoorAir attributes.
    """

    # Get all Controller:OutdoorAir objects in the OpenStudio model.
    all_objects = osm_model.getControllerOutdoorAirs()

    all_objects_dicts = []

    for target_object in all_objects:
        object_handle = str(target_object.handle())
        object_dict = get_controller_outdoor_air_object_as_dict(osm_model, object_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts

def get_all_controller_outdoor_air_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:Controller:OutdoorAir objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all Controller:OutdoorAir attributes.
    """

    return build_dataframe(
        get_all_controller_outdoor_air_objects_as_dicts(osm_model), "Controller:OutdoorAir",
        sort_by="Name", columns=CONTROLLER_OUTDOOR_AIR_COLUMNS)