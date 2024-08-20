import openstudio
import pandas as pd


def get_all_sizing_zone_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all zone Sizing Zone Objects from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all thermal zones.
    """

    all_sizing_zones = osm_model.getSizingZones()

    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_sizing_zones],
        'Zone or ZoneList Name': [x.thermalZone().name().get() for x in all_sizing_zones],
        'Zone Cooling Design Supply Air Temperature Input Method': [x.zoneCoolingDesignSupplyAirTemperatureInputMethod() for x in all_sizing_zones],
        'Zone Cooling Design Supply Air Temperature {C}': [x.zoneCoolingDesignSupplyAirTemperature() for x in all_sizing_zones],
        'Zone Cooling Design Supply Air Temperature Difference {deltaC}': [x.zoneCoolingDesignSupplyAirTemperatureDifference() for x in all_sizing_zones],
        'Zone Heating Design Supply Air Temperature Input Method': [x.zoneHeatingDesignSupplyAirTemperatureInputMethod() for x in all_sizing_zones],
        'Zone Heating Design Supply Air Temperature {C}': [x.zoneHeatingDesignSupplyAirTemperature() for x in all_sizing_zones],
        'Zone Heating Design Supply Air Temperature Difference {deltaC}': [x.zoneHeatingDesignSupplyAirTemperatureDifference() for x in all_sizing_zones],
        'Zone Cooling Design Supply Air Humidity Ratio {kg-H2O/kg-air}': [x.zoneCoolingDesignSupplyAirHumidityRatio() for x in all_sizing_zones],
        'Zone Heating Design Supply Air Humidity Ratio {kg-H2O/kg-air}': [x.zoneHeatingDesignSupplyAirHumidityRatio() for x in all_sizing_zones],
        'Zone Heating Sizing Factor': [x.zoneHeatingSizingFactor() for x in all_sizing_zones],
        'Zone Cooling Sizing Factor': [x.zoneCoolingSizingFactor() for x in all_sizing_zones],
        'Cooling Design Air Flow Method': [x.coolingDesignAirFlowMethod() for x in all_sizing_zones],
        'Cooling Design Air Flow Rate {m3/s}': [x.coolingDesignAirFlowRate() for x in all_sizing_zones],
        'Cooling Minimum Air Flow per Zone Floor Area {m3/s-m2}': [x.coolingMinimumAirFlowperZoneFloorArea() for x in all_sizing_zones],
        'Cooling Minimum Air Flow {m3/s}': [x.coolingMinimumAirFlow() for x in all_sizing_zones],
        'Cooling Minimum Air Flow Fraction': [x.coolingMinimumAirFlowFraction() for x in all_sizing_zones],
        'Heating Design Air Flow Method': [x.heatingDesignAirFlowMethod() for x in all_sizing_zones],
        'Heating Design Air Flow Rate {m3/s}': [x.heatingDesignAirFlowRate() for x in all_sizing_zones],
        'Heating Maximum Air Flow per Zone Floor Area {m3/s-m2}': [x.heatingMaximumAirFlowperZoneFloorArea() for x in all_sizing_zones],
        'Heating Maximum Air Flow {m3/s}': [x.heatingMaximumAirFlow() for x in all_sizing_zones],
        'Heating Maximum Air Flow Fraction': [x.heatingMaximumAirFlowFraction() for x in all_sizing_zones],
        'Account for Dedicated Outdoor Air System': [x.accountforDedicatedOutdoorAirSystem() for x in all_sizing_zones],
        'Dedicated Outdoor Air System Control Strategy': [x.dedicatedOutdoorAirSystemControlStrategy() for x in all_sizing_zones],
        'Dedicated Outdoor Air Low Setpoint Temperature for Design {C}': [x.dedicatedOutdoorAirLowSetpointTemperatureforDesign() for x in all_sizing_zones],
        'Dedicated Outdoor Air High Setpoint Temperature for Design {C}': [x.dedicatedOutdoorAirHighSetpointTemperatureforDesign() for x in all_sizing_zones],
        'Zone Load Sizing Method': [x.zoneLoadSizingMethod() for x in all_sizing_zones],
        'Zone Latent Cooling Design Supply Air Humidity Ratio Input Method': [x.zoneLatentCoolingDesignSupplyAirHumidityRatioInputMethod() for x in all_sizing_zones],
        'Zone Dehumidification Design Supply Air Humidity Ratio {kgWater/kgDryAir}': [x.zoneDehumidificationDesignSupplyAirHumidityRatio() for x in all_sizing_zones],
        'Zone Cooling Design Supply Air Humidity Ratio Difference {kgWater/kgDryAir}': [x.zoneCoolingDesignSupplyAirHumidityRatioDifference() for x in all_sizing_zones],
        'Zone Latent Heating Design Supply Air Humidity Ratio Input Method': [x.zoneLatentHeatingDesignSupplyAirHumidityRatioInputMethod() for x in all_sizing_zones],
        'Zone Humidification Design Supply Air Humidity Ratio {kgWater/kgDryAir}': [x.zoneHumidificationDesignSupplyAirHumidityRatio() for x in all_sizing_zones],
        'Zone Humidification Design Supply Air Humidity Ratio Difference {kgWater/kgDryAir}': [x.zoneHumidificationDesignSupplyAirHumidityRatioDifference() for x in all_sizing_zones]
        }
    # Create a DataFrame of all thermal zones.
    all_sizing_zones_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_sizing_zones_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_sizing_zones_df = all_sizing_zones_df.sort_values(
        by='Zone or ZoneList Name', ascending=True).reset_index(drop=True)

    print(
        f"The OSM model contains {all_sizing_zones_df.shape[0]} sizing zones")

    return all_sizing_zones_df