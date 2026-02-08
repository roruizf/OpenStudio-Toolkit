import logging
from typing import Any

import openstudio
import pandas as pd

# Configure logger
logger = logging.getLogger(__name__)

#-----------------------------
#--- OS:Controller:OutdoorAir
#-----------------------------

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
        if osm_object is None:
            logger.warning(
                f"No Controller:OutdoorAir object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getControllerOutdoorAirByName(name)
        if not osm_object:
            logger.warning(
                f"No Controller:OutdoorAir object found with the name: {name}")
            return {}

    target_object = osm_object.get()
    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Relief Air Outlet Node Name': None,
        'Return Air Node Name': None,
        'Mixed Air Node Name': None,
        'Actuator Node Name': None,
        'Minimum Outdoor Air Flow Rate {m3/s}': target_object.minimumOutdoorAirFlowRate().get() if not target_object.isMinimumOutdoorAirFlowRateAutosized() else 'autosize',
        'Maximum Outdoor Air Flow Rate {m3/s}': target_object.maximumOutdoorAirFlowRate().get() if not target_object.isMaximumOutdoorAirFlowRateAutosized() else 'autosize',
        'Economizer Control Type': target_object.getEconomizerControlType(),
        'Economizer Control Action Type': target_object.getEconomizerControlActionType(),
        'Economizer Maximum Limit Dry-Bulb Temperature {C}': target_object.getEconomizerMaximumLimitDryBulbTemperature().get() if target_object.getEconomizerMaximumLimitDryBulbTemperature().is_initialized() else None,
        'Economizer Maximum Limit Enthalpy {J/kg}': target_object.getEconomizerMinimumLimitDryBulbTemperature().get() if target_object.getEconomizerMinimumLimitDryBulbTemperature().is_initialized() else None,
        'Economizer Maximum Limit Dewpoint Temperature {C}': None,
        'Electronic Enthalpy Limit Curve Name': None,
        'Economizer Minimum Limit Dry-Bulb Temperature {C}': None,
        'Lockout Type': target_object.getLockoutType(),
        'Minimum Limit Type': target_object.getMinimumLimitType(),
        'Minimum Outdoor Air Schedule Name': target_object.minimumOutdoorAirSchedule().get().name().get() if target_object.minimumOutdoorAirSchedule().is_initialized() else None,
        'Minimum Fraction of Outdoor Air Schedule Name': target_object.minimumFractionofOutdoorAirSchedule().get().name().get() if target_object.minimumFractionofOutdoorAirSchedule().is_initialized() else None,
        'Maximum Fraction of Outdoor Air Schedule Name': target_object.maximumFractionofOutdoorAirSchedule().get().name().get() if target_object.maximumFractionofOutdoorAirSchedule().is_initialized() else None,
        'Controller Mechanical Ventilation': target_object.controllerMechanicalVentilation().name().get(),
        'Time of Day Economizer Control Schedule Name': None,
        'High Humidity Control': target_object.getHighHumidityControl().get() if target_object.getHighHumidityControl().is_initialized() else None,
        'Humidistat Control Zone Name': None,
        'High Humidity Outdoor Air Flow Ratio': None,
        'Control High Indoor Humidity Based on Outdoor Humidity Ratio': None,
        'Heat Recovery Bypass Control Type': target_object.getHeatRecoveryBypassControlType().get() if target_object.getHeatRecoveryBypassControlType().is_initialized() else None,        
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

    all_objects_dicts = get_all_controller_outdoor_air_objects_as_dicts(osm_model)

    # Create a DataFrame of all Controller:OutdoorAir objects.
    all_objects_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_objects_df = all_objects_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    logger.info(f"The OSM model contains {all_objects_df.shape[0]} Controller:OutdoorAir objects")

    return all_objects_df