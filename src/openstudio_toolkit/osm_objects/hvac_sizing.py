import logging
from typing import Any

import openstudio
import pandas as pd

from openstudio_toolkit._sdk import opt, related_name
from openstudio_toolkit.osm_objects._base import build_dataframe
from openstudio_toolkit.utils import helpers

# Configure logger
logger = logging.getLogger(__name__)

# --------------------------------------------------
#  ***** OS:Sizing:Zone ****************************
# --------------------------------------------------

SIZING_ZONE_COLUMNS = (
    'Handle',
    'Zone Name',
    'Zone Cooling Design Supply Air Temperature Input Method',
    'Zone Cooling Design Supply Air Temperature {C}',
    'Zone Cooling Design Supply Air Temperature Difference {deltaC}',
    'Zone Heating Design Supply Air Temperature Input Method',
    'Zone Heating Design Supply Air Temperature {C}',
    'Zone Heating Design Supply Air Temperature Difference {deltaC}',
    'Zone Cooling Design Supply Air Humidity Ratio {kg-H2O/kg-air}',
    'Zone Heating Design Supply Air Humidity Ratio {kg-H2O/kg-air}',
    'Zone Heating Sizing Factor',
    'Zone Cooling Sizing Factor',
    'Cooling Design Air Flow Method',
    'Cooling Design Air Flow Rate {m3/s}',
    'Cooling Minimum Air Flow per Zone Floor Area {m3/s-m2}',
    'Cooling Minimum Air Flow {m3/s}',
    'Cooling Minimum Air Flow Fraction',
    'Heating Design Air Flow Method',
    'Heating Design Air Flow Rate {m3/s}',
    'Heating Maximum Air Flow per Zone Floor Area {m3/s-m2}',
    'Heating Maximum Air Flow {m3/s}',
    'Heating Maximum Air Flow Fraction',
    'Account for Dedicated Outdoor Air System',
    'Dedicated Outdoor Air System Control Strategy',
    'Dedicated Outdoor Air Low Setpoint Temperature for Design {C}',
    'Dedicated Outdoor Air High Setpoint Temperature for Design {C}',
    'Zone Load Sizing Method',
    'Zone Latent Cooling Design Supply Air Humidity Ratio Input Method',
    'Zone Dehumidification Design Supply Air Humidity Ratio {kgWater/kgDryAir}',
    'Zone Cooling Design Supply Air Humidity Ratio Difference {kgWater/kgDryAir}',
    'Zone Latent Heating Design Supply Air Humidity Ratio Input Method',
    'Zone Humidification Design Supply Air Humidity Ratio {kgWater/kgDryAir}',
    'Zone Humidification Design Supply Air Humidity Ratio Difference {kgWater/kgDryAir}',
)


def get_sizing_zone_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: str | None = None, 
    name: str | None = None, 
    _object_ref: openstudio.model.SizingZone | None = None
) -> dict[str, Any]:
    """
    Retrieve attributes of an OS:Sizing:Zone object from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.SizingZone, optional): Direct object reference.

    Returns:
    - Dict[str, Any]: A dictionary containing sizing zone attributes.
    """
    target_object = helpers.fetch_object(
        osm_model, "SizingZone", handle, name, _object_ref)

    if target_object is None:
        return {}

    return {
        'Handle': str(target_object.handle()),
        'Zone Name': related_name(target_object, "Zone or ZoneList Name"),
        'Zone Cooling Design Supply Air Temperature Input Method': target_object.zoneCoolingDesignSupplyAirTemperatureInputMethod(),
        'Zone Cooling Design Supply Air Temperature {C}': target_object.zoneCoolingDesignSupplyAirTemperature(),
        'Zone Cooling Design Supply Air Temperature Difference {deltaC}': target_object.zoneCoolingDesignSupplyAirTemperatureDifference(),
        'Zone Heating Design Supply Air Temperature Input Method': target_object.zoneHeatingDesignSupplyAirTemperatureInputMethod(),
        'Zone Heating Design Supply Air Temperature {C}': target_object.zoneHeatingDesignSupplyAirTemperature(),
        'Zone Heating Design Supply Air Temperature Difference {deltaC}': target_object.zoneHeatingDesignSupplyAirTemperatureDifference(),
        'Zone Cooling Design Supply Air Humidity Ratio {kg-H2O/kg-air}': target_object.zoneCoolingDesignSupplyAirHumidityRatio(),
        'Zone Heating Design Supply Air Humidity Ratio {kg-H2O/kg-air}': target_object.zoneHeatingDesignSupplyAirHumidityRatio(),
        'Zone Heating Sizing Factor': opt(target_object.zoneHeatingSizingFactor()),
        'Zone Cooling Sizing Factor': opt(target_object.zoneCoolingSizingFactor()),
        'Cooling Design Air Flow Method': target_object.coolingDesignAirFlowMethod(),
        'Cooling Design Air Flow Rate {m3/s}': target_object.coolingDesignAirFlowRate(),
        'Cooling Minimum Air Flow per Zone Floor Area {m3/s-m2}': target_object.coolingMinimumAirFlowperZoneFloorArea(),
        'Cooling Minimum Air Flow {m3/s}': target_object.coolingMinimumAirFlow(),
        'Cooling Minimum Air Flow Fraction': target_object.coolingMinimumAirFlowFraction(),
        'Heating Design Air Flow Method': target_object.heatingDesignAirFlowMethod(),
        'Heating Design Air Flow Rate {m3/s}': target_object.heatingDesignAirFlowRate(),
        'Heating Maximum Air Flow per Zone Floor Area {m3/s-m2}': target_object.heatingMaximumAirFlowperZoneFloorArea(),
        'Heating Maximum Air Flow {m3/s}': target_object.heatingMaximumAirFlow(),
        'Heating Maximum Air Flow Fraction': target_object.heatingMaximumAirFlowFraction(),
        'Account for Dedicated Outdoor Air System': target_object.accountforDedicatedOutdoorAirSystem(),
        'Dedicated Outdoor Air System Control Strategy': target_object.dedicatedOutdoorAirSystemControlStrategy(),
        'Dedicated Outdoor Air Low Setpoint Temperature for Design {C}': 'Autosize' if target_object.isDedicatedOutdoorAirLowSetpointTemperatureforDesignAutosized() else opt(target_object.dedicatedOutdoorAirLowSetpointTemperatureforDesign()),
        'Dedicated Outdoor Air High Setpoint Temperature for Design {C}': 'Autosize' if target_object.isDedicatedOutdoorAirHighSetpointTemperatureforDesignAutosized() else opt(target_object.dedicatedOutdoorAirHighSetpointTemperatureforDesign()),
        'Zone Load Sizing Method': target_object.zoneLoadSizingMethod(),
        'Zone Latent Cooling Design Supply Air Humidity Ratio Input Method': target_object.zoneLatentCoolingDesignSupplyAirHumidityRatioInputMethod(),
        'Zone Dehumidification Design Supply Air Humidity Ratio {kgWater/kgDryAir}': opt(target_object.zoneDehumidificationDesignSupplyAirHumidityRatio()),
        'Zone Cooling Design Supply Air Humidity Ratio Difference {kgWater/kgDryAir}': target_object.zoneCoolingDesignSupplyAirHumidityRatioDifference(),
        'Zone Latent Heating Design Supply Air Humidity Ratio Input Method': target_object.zoneLatentHeatingDesignSupplyAirHumidityRatioInputMethod(),
        'Zone Humidification Design Supply Air Humidity Ratio {kgWater/kgDryAir}': opt(target_object.zoneHumidificationDesignSupplyAirHumidityRatio()),
        'Zone Humidification Design Supply Air Humidity Ratio Difference {kgWater/kgDryAir}': target_object.zoneHumidificationDesignSupplyAirHumidityRatioDifference()
    }

def get_all_sizing_zone_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict[str, Any]]:
    """
    Retrieve attributes for all OS:Sizing:Zone objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing sizing zone attributes.
    """
    all_objects = osm_model.getSizingZones()
    return [get_sizing_zone_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_sizing_zone_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:Sizing:Zone objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all Sizing:Zone attributes.
    """
    return build_dataframe(
        get_all_sizing_zone_objects_as_dicts(osm_model), "Sizing:Zone",
        sort_by="Zone Name", columns=SIZING_ZONE_COLUMNS)

# --------------------------------------------------
#  ***** OS:Sizing:System **************************
# --------------------------------------------------

SIZING_SYSTEM_COLUMNS = (
    'Handle',
    'AirLoop Name',
    'Type of Load to Size On',
    'Design Outdoor Air Flow Rate {m3/s}',
    'Central Heating Maximum System Air Flow Ratio',
    'Preheat Design Temperature {C}',
    'Preheat Design Humidity Ratio {kg-H2O/kg-Air}',
    'Precool Design Temperature {C}',
    'Precool Design Humidity Ratio {kg-H2O/kg-Air}',
    'Central Cooling Design Supply Air Temperature {C}',
    'Central Heating Design Supply Air Temperature {C}',
    'Sizing Option',
    '100% Outdoor Air in Cooling',
    '100% Outdoor Air in Heating',
    'Central Cooling Design Supply Air Humidity Ratio {kg-H2O/kg-Air}',
    'Central Heating Design Supply Air Humidity Ratio {kg-H2O/kg-Air}',
    'Cooling Design Air Flow Method',
    'Cooling Design Air Flow Rate {m3/s}',
    'Heating Design Air Flow Method',
    'Heating Design Air Flow Rate {m3/s}',
    'System Outdoor Air Method',
    'Zone Maximum Outdoor Air Fraction {dimensionless}',
    'Cooling Supply Air Flow Rate Per Floor Area {m3/s-m2}',
    'Cooling Fraction of Autosized Cooling Supply Air Flow Rate',
    'Cooling Supply Air Flow Rate Per Unit Cooling Capacity {m3/s-W}',
    'Heating Supply Air Flow Rate Per Floor Area {m3/s-m2}',
    'Heating Fraction of Autosized Heating Supply Air Flow Rate',
    'Heating Supply Air Flow Rate Per Unit Heating Capacity {m3/s-W}',
    'Cooling Design Capacity Method',
    'Cooling Design Capacity {W}',
    'Cooling Design Capacity Per Floor Area {W/m2}',
    'Fraction of Autosized Cooling Design Capacity',
    'Heating Design Capacity Method',
    'Heating Design Capacity {W}',
    'Heating Design Capacity Per Floor Area {W/m2}',
    'Fraction of Autosized Heating Design Capacity',
    'Central Cooling Capacity Control Method',
    'Occupant Diversity',
)


def get_sizing_system_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: str | None = None, 
    name: str | None = None, 
    _object_ref: openstudio.model.SizingSystem | None = None
) -> dict[str, Any]:
    """
    Retrieve attributes of an OS:Sizing:System object from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.SizingSystem, optional): Direct object reference.

    Returns:
    - Dict[str, Any]: A dictionary containing sizing system attributes.
    """
    target_object = helpers.fetch_object(
        osm_model, "SizingSystem", handle, name, _object_ref)

    if target_object is None:
        return {}

    return {
        'Handle': str(target_object.handle()),
        'AirLoop Name': related_name(target_object, "AirLoop Name"),
        'Type of Load to Size On': target_object.typeofLoadtoSizeOn(),
        'Design Outdoor Air Flow Rate {m3/s}': 'Autosize' if target_object.isDesignOutdoorAirFlowRateAutosized() else opt(target_object.designOutdoorAirFlowRate()),    
        'Central Heating Maximum System Air Flow Ratio': 'Autosize' if target_object.isCentralHeatingMaximumSystemAirFlowRatioAutosized() else opt(target_object.centralHeatingMaximumSystemAirFlowRatio()),
        'Preheat Design Temperature {C}': target_object.preheatDesignTemperature(),
        'Preheat Design Humidity Ratio {kg-H2O/kg-Air}': target_object.preheatDesignHumidityRatio(),
        'Precool Design Temperature {C}': target_object.precoolDesignTemperature(),
        'Precool Design Humidity Ratio {kg-H2O/kg-Air}': target_object.precoolDesignHumidityRatio(),
        'Central Cooling Design Supply Air Temperature {C}': target_object.centralCoolingDesignSupplyAirTemperature(),
        'Central Heating Design Supply Air Temperature {C}': target_object.centralHeatingDesignSupplyAirTemperature(),
        'Sizing Option': target_object.sizingOption(),
        '100% Outdoor Air in Cooling': target_object.allOutdoorAirinCooling(),
        '100% Outdoor Air in Heating': target_object.allOutdoorAirinHeating(),    
        'Central Cooling Design Supply Air Humidity Ratio {kg-H2O/kg-Air}': target_object.centralCoolingDesignSupplyAirHumidityRatio(),
        'Central Heating Design Supply Air Humidity Ratio {kg-H2O/kg-Air}': target_object.centralHeatingDesignSupplyAirHumidityRatio(),
        'Cooling Design Air Flow Method': target_object.coolingDesignAirFlowMethod(),
        'Cooling Design Air Flow Rate {m3/s}': target_object.coolingDesignAirFlowRate(),
        'Heating Design Air Flow Method': target_object.heatingDesignAirFlowMethod(),
        'Heating Design Air Flow Rate {m3/s}': target_object.heatingDesignAirFlowRate(),
        'System Outdoor Air Method': target_object.systemOutdoorAirMethod(),
        'Zone Maximum Outdoor Air Fraction {dimensionless}': target_object.zoneMaximumOutdoorAirFraction(),
        'Cooling Supply Air Flow Rate Per Floor Area {m3/s-m2}': target_object.coolingSupplyAirFlowRatePerFloorArea(),
        'Cooling Fraction of Autosized Cooling Supply Air Flow Rate': target_object.coolingFractionofAutosizedCoolingSupplyAirFlowRate(),
        'Cooling Supply Air Flow Rate Per Unit Cooling Capacity {m3/s-W}': target_object.coolingSupplyAirFlowRatePerUnitCoolingCapacity(),
        'Heating Supply Air Flow Rate Per Floor Area {m3/s-m2}': target_object.heatingSupplyAirFlowRatePerFloorArea(),
        'Heating Fraction of Autosized Heating Supply Air Flow Rate': target_object.heatingFractionofAutosizedCoolingSupplyAirFlowRate(),
        'Heating Supply Air Flow Rate Per Unit Heating Capacity {m3/s-W}': target_object.heatingSupplyAirFlowRatePerUnitHeatingCapacity(),
        'Cooling Design Capacity Method': target_object.coolingDesignCapacityMethod(),
        'Cooling Design Capacity {W}': 'Autosize' if target_object.isCoolingDesignCapacityAutosized() else opt(target_object.coolingDesignCapacity()),
        'Cooling Design Capacity Per Floor Area {W/m2}': target_object.coolingDesignCapacityPerFloorArea(),
        'Fraction of Autosized Cooling Design Capacity': target_object.fractionofAutosizedCoolingDesignCapacity(),
        'Heating Design Capacity Method': target_object.heatingDesignCapacityMethod(), 
        'Heating Design Capacity {W}': 'Autosize' if target_object.isHeatingDesignCapacityAutosized() else opt(target_object.heatingDesignCapacity()),
        'Heating Design Capacity Per Floor Area {W/m2}': target_object.heatingDesignCapacityPerFloorArea(),
        'Fraction of Autosized Heating Design Capacity': target_object.fractionofAutosizedHeatingDesignCapacity(),
        'Central Cooling Capacity Control Method': target_object.centralCoolingCapacityControlMethod(),
        'Occupant Diversity': 'Autosize' if target_object.isOccupantDiversityAutosized() else opt(target_object.occupantDiversity()),
    }

def get_all_air_sizing_system_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict[str, Any]]:
    """
    Retrieve attributes for all OS:Sizing:System objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing sizing system attributes.
    """
    all_objects = osm_model.getSizingSystems()
    return [get_sizing_system_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_air_sizing_system_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:Sizing:System objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all Sizing:System attributes.
    """
    return build_dataframe(
        get_all_air_sizing_system_objects_as_dicts(osm_model), "Sizing:System",
        sort_by="AirLoop Name", columns=SIZING_SYSTEM_COLUMNS)
