import openstudio
import pandas as pd
import numpy as np
import logging
from typing import Dict, Any, List, Optional
from openstudio_toolkit.utils import helpers

# Configure logger
logger = logging.getLogger(__name__)

# --------------------------------------------------
#  ***** OS:Sizing:Zone ****************************
# --------------------------------------------------

def get_sizing_zone_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: Optional[str] = None, 
    name: Optional[str] = None, 
    _object_ref: Optional[openstudio.model.SizingZone] = None
) -> Dict[str, Any]:
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
        'Zone Name': target_object.thermalZone().name().get() if target_object.thermalZone().name().is_initialized() else "Unnamed Zone",
        'Zone Cooling Design Supply Air Temperature Input Method': target_object.zoneCoolingDesignSupplyAirTemperatureInputMethod(),
        'Zone Cooling Design Supply Air Temperature {C}': target_object.zoneCoolingDesignSupplyAirTemperature(),
        'Zone Cooling Design Supply Air Temperature Difference {deltaC}': target_object.zoneCoolingDesignSupplyAirTemperatureDifference(),
        'Zone Heating Design Supply Air Temperature Input Method': target_object.zoneHeatingDesignSupplyAirTemperatureInputMethod(),
        'Zone Heating Design Supply Air Temperature {C}': target_object.zoneHeatingDesignSupplyAirTemperature(),
        'Zone Heating Design Supply Air Temperature Difference {deltaC}': target_object.zoneHeatingDesignSupplyAirTemperatureDifference(),
        'Zone Cooling Design Supply Air Humidity Ratio {kg-H2O/kg-air}': target_object.zoneCoolingDesignSupplyAirHumidityRatio(),
        'Zone Heating Design Supply Air Humidity Ratio {kg-H2O/kg-air}': target_object.zoneHeatingDesignSupplyAirHumidityRatio(),
        'Zone Heating Sizing Factor': target_object.zoneHeatingSizingFactor(),
        'Zone Cooling Sizing Factor': target_object.zoneCoolingSizingFactor(),
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
        'Dedicated Outdoor Air Low Setpoint Temperature for Design {C}': target_object.dedicatedOutdoorAirLowSetpointTemperatureforDesign(),
        'Dedicated Outdoor Air High Setpoint Temperature for Design {C}': target_object.dedicatedOutdoorAirHighSetpointTemperatureforDesign(),
        'Zone Load Sizing Method': target_object.zoneLoadSizingMethod(),
        'Zone Latent Cooling Design Supply Air Humidity Ratio Input Method': target_object.zoneLatentCoolingDesignSupplyAirHumidityRatioInputMethod(),
        'Zone Dehumidification Design Supply Air Humidity Ratio {kgWater/kgDryAir}': target_object.zoneDehumidificationDesignSupplyAirHumidityRatio(),
        'Zone Cooling Design Supply Air Humidity Ratio Difference {kgWater/kgDryAir}': target_object.zoneCoolingDesignSupplyAirHumidityRatioDifference(),
        'Zone Latent Heating Design Supply Air Humidity Ratio Input Method': target_object.zoneLatentHeatingDesignSupplyAirHumidityRatioInputMethod(),
        'Zone Humidification Design Supply Air Humidity Ratio {kgWater/kgDryAir}': target_object.zoneHumidificationDesignSupplyAirHumidityRatio(),
        'Zone Humidification Design Supply Air Humidity Ratio Difference {kgWater/kgDryAir}': target_object.zoneHumidificationDesignSupplyAirHumidityRatioDifference()
    }

def get_all_sizing_zone_objects_as_dicts(osm_model: openstudio.model.Model) -> List[Dict[str, Any]]:
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
    all_objects_dicts = get_all_sizing_zone_objects_as_dicts(osm_model)
    df = pd.DataFrame(all_objects_dicts)

    if not df.empty and 'Zone Name' in df.columns:
        df = df.sort_values(by='Zone Name', ascending=True).reset_index(drop=True)

    logger.info(f"Retrieved {len(df)} Sizing:Zone objects from the model.")
    return df

# --------------------------------------------------
#  ***** OS:Sizing:System **************************
# --------------------------------------------------

def get_sizing_system_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: Optional[str] = None, 
    name: Optional[str] = None, 
    _object_ref: Optional[openstudio.model.SizingSystem] = None
) -> Dict[str, Any]:
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
        'AirLoop Name': target_object.airLoopHVAC().name().get() if target_object.airLoopHVAC().name().is_initialized() else "Unnamed Air Loop",    
        'Type of Load to Size On': target_object.typeofLoadtoSizeOn(),
        'Design Outdoor Air Flow Rate {m3/s}': target_object.designOutdoorAirFlowRate().get() if not target_object.isDesignOutdoorAirFlowRateAutosized() else 'autosize',    
        'Central Heating Maximum System Air Flow Ratio': target_object.centralHeatingMaximumSystemAirFlowRatio().get() if not target_object.isCentralHeatingMaximumSystemAirFlowRatioAutosized() else 'autosize',
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
        'Cooling Design Capacity {W}': target_object.coolingDesignCapacity().get() if not target_object.isCoolingDesignCapacityAutosized() else 'autosize',
        'Cooling Design Capacity Per Floor Area {W/m2}': target_object.coolingDesignCapacityPerFloorArea(),
        'Fraction of Autosized Cooling Design Capacity': target_object.fractionofAutosizedCoolingDesignCapacity(),
        'Heating Design Capacity Method': target_object.heatingDesignCapacityMethod(), 
        'Heating Design Capacity {W}': target_object.heatingDesignCapacity().get() if not target_object.isHeatingDesignCapacityAutosized() else 'autosize',
        'Heating Design Capacity Per Floor Area {W/m2}': target_object.heatingDesignCapacityPerFloorArea(),
        'Fraction of Autosized Heating Design Capacity': target_object.fractionofAutosizedHeatingDesignCapacity(),
        'Central Cooling Capacity Control Method': target_object.centralCoolingCapacityControlMethod(),
        'Occupant Diversity': target_object.occupantDiversity().get() if not target_object.isOccupantDiversityAutosized() else 'autosize',
    }

def get_all_air_sizing_system_objects_as_dicts(osm_model: openstudio.model.Model) -> List[Dict[str, Any]]:
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
    all_objects_dicts = get_all_air_sizing_system_objects_as_dicts(osm_model)
    df = pd.DataFrame(all_objects_dicts)

    if not df.empty and 'AirLoop Name' in df.columns:
        df = df.sort_values(by='AirLoop Name', ascending=True).reset_index(drop=True)

    logger.info(f"Retrieved {len(df)} Sizing:System objects from the model.")
    return df
