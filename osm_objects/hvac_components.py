import openstudio
import pandas as pd

def get_all_coil_cooling_dx_variable_refrigerant_flow_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all Coil Cooling DX Variable Refrigerant Flow Objects from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all thermal zones.
    """

    all_coil_cooling_dx_vrfs = osm_model.getCoilCoolingDXVariableRefrigerantFlows()

    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_coil_cooling_dx_vrfs],
        'Name': [x.name().get() for x in all_coil_cooling_dx_vrfs],
        'Availability Schedule': [x.availabilitySchedule().name().get() for x in all_coil_cooling_dx_vrfs],
        'Rated Total Cooling Capacity {W}': [x.ratedTotalCoolingCapacity().get() if not x.ratedTotalCoolingCapacity().isNull() else None for x in all_coil_cooling_dx_vrfs],
        'Rated Sensible Heat Ratio': [x.ratedSensibleHeatRatio().get() if not x.ratedSensibleHeatRatio().isNull() else None for x in all_coil_cooling_dx_vrfs],
        'Rated Air Flow Rate {m3/s}': [x.ratedAirFlowRate().get() if not x.ratedAirFlowRate().isNull() else None for x in all_coil_cooling_dx_vrfs],
        'Cooling Capacity Ratio Modifier Function of Temperature Curve': [x.coolingCapacityRatioModifierFunctionofTemperatureCurve().name().get() if not x.coolingCapacityRatioModifierFunctionofTemperatureCurve().name().isNull() else None for x in all_coil_cooling_dx_vrfs],
        'Cooling Capacity Modifier Curve Function of Flow Fraction': [x.coolingCapacityModifierCurveFunctionofFlowFraction().name().get() if not x.coolingCapacityModifierCurveFunctionofFlowFraction().name().isNull() else None for x in all_coil_cooling_dx_vrfs]
    }
    
    # Create a DataFrame of Coil Cooling DX Variable Refrigerant Flow Objects.
    all_coil_cooling_dx_vrfs_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_coil_cooling_dx_vrfs_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_coil_cooling_dx_vrfs_df = all_coil_cooling_dx_vrfs_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(
        f"The OSM model contains {all_coil_cooling_dx_vrfs_df.shape[0]} sizing zones")

    return all_coil_cooling_dx_vrfs_df


def get_all_coil_heating_dx_variable_refrigerant_flow_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all Coil Heating DX Variable Refrigerant Flow Objects from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all thermal zones.
    """

    all_coil_heating_dx_vrfs = osm_model.getCoilHeatingDXVariableRefrigerantFlows()

    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_coil_heating_dx_vrfs],
        'Name': [x.name().get() for x in all_coil_heating_dx_vrfs],
        'Availability Schedule': [x.availabilitySchedule().name().get() for x in all_coil_heating_dx_vrfs],
        'Rated Total Heating Capacity {W}': [x.ratedTotalHeatingCapacity().get() if not x.ratedTotalHeatingCapacity().isNull() else None for x in all_coil_heating_dx_vrfs],
        'Rated Air Flow Rate {m3/s}': [x.ratedAirFlowRate().get() if not x.ratedAirFlowRate().isNull() else None for x in all_coil_heating_dx_vrfs],
        'Coil Air Inlet Node': None,
        'Coil Air Outlet Node': None,
        'Heating Capacity Ratio Modifier Function of Temperature Curve': [x.heatingCapacityRatioModifierFunctionofTemperatureCurve().name().get() if not x.heatingCapacityRatioModifierFunctionofTemperatureCurve().name().isNull() else None for x in all_coil_heating_dx_vrfs],
        'Heating Capacity Modifier Function of Flow Fraction Curve': [x.heatingCapacityModifierFunctionofFlowFractionCurve().name().get() if not x.heatingCapacityModifierFunctionofFlowFractionCurve().name().isNull() else None for x in all_coil_heating_dx_vrfs]
    }
    
    # Create a DataFrame of Coil Heating DX Variable Refrigerant Flow Objects.
    all_coil_heating_dx_vrfs_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_coil_heating_dx_vrfs_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_coil_heating_dx_vrfs_df = all_coil_heating_dx_vrfs_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(
        f"The OSM model contains {all_coil_heating_dx_vrfs_df.shape[0]} sizing zones")

    return all_coil_heating_dx_vrfs_df

def get_all_fan_constant_volume_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all Fan Constant Volume Objects from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all thermal zones.
    """

    all_fan_constant_volume = osm_model.getFanConstantVolumes()
    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_fan_constant_volume],
        'Name': [x.name().get() for x in all_fan_constant_volume],
        'Availability Schedule Name': [x.availabilitySchedule().name().get() if not x.availabilitySchedule().name().isNull() else None for x in all_fan_constant_volume],
        'Fan Total Efficiency': [x.fanTotalEfficiency() for x in all_fan_constant_volume],
        'Pressure Rise {Pa}': [x.pressureRise() for x in all_fan_constant_volume],
        'Maximum Flow Rate {m3/s}': [x.maximumFlowRate().get() if not x.maximumFlowRate().isNull() else None for x in all_fan_constant_volume],
        'Motor Efficiency': None,
        'Motor In Airstream Fraction': None,
        'Air Inlet Node Name': None,
        'Air Outlet Node Name': None,
        'End-Use Subcategory': [x.endUseSubcategory() for x in all_fan_constant_volume]
        }

    # Create a DataFrame of Fan Constant Volume Objects.
    all_fan_constant_volume_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_fan_constant_volume_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_fan_constant_volume_df = all_fan_constant_volume_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(
        f"The OSM model contains {all_fan_constant_volume_df.shape[0]} Fan Constant Volume Objects")

    return all_fan_constant_volume_df

def get_all_fan_on_off_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all Fan On Off Objects from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all thermal zones.
    """

    all_fan_on_off = osm_model.getFanOnOffs()
    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_fan_on_off],
        'Name': [x.name().get() for x in all_fan_on_off],
        'Availability Schedule Name': [x.availabilitySchedule().name().get() if not x.availabilitySchedule().name().isNull() else None for x in all_fan_on_off],
        'Fan Total Efficiency': [x.fanTotalEfficiency() for x in all_fan_on_off],
        'Pressure Rise {Pa}': [x.pressureRise() for x in all_fan_on_off],
        'Maximum Flow Rate {m3/s}': [x.maximumFlowRate().get() if not x.maximumFlowRate().isNull() else None for x in all_fan_on_off],
        'Motor Efficiency': None,
        'Motor In Airstream Fraction': None,
        'Air Inlet Node Name': None,
        'Air Outlet Node Name': None,
        'Fan Power Ratio Function of Speed Ratio Curve Name': [x.fanPowerRatioFunctionofSpeedRatioCurve().nameString() for x in all_fan_on_off],
        'Fan Efficiency Ratio Function of Speed Ratio Curve Name': [x.fanEfficiencyRatioFunctionofSpeedRatioCurve().nameString() for x in all_fan_on_off],
        'End-Use Subcategory': [x.endUseSubcategory() for x in all_fan_on_off]
        }

    # Create a DataFrame of Fan On Off Objects.
    all_fan_on_off_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_fan_on_off_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_fan_on_off_df = all_fan_on_off_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(
        f"The OSM model contains {all_fan_on_off_df.shape[0]} Fan On Off Objects")

    return all_fan_on_off_df

def get_all_hx_air_to_air_sensible_and_latent_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:  
  
  """
      Retrieve all Heat Exchanger Air To Air Sensible And Latent Objects from the OpenStudio model and organize them into a pandas DataFrame.

      Parameters:
      - osm_model (openstudio.model.Model): The OpenStudio Model object.

      Returns:
      - pd.DataFrame: DataFrame containing information about all Heat Exchanger Air To Air Sensible And Latent.
  """
  all_hx_air_to_air_sensible_and_latent = osm_model.getHeatExchangerAirToAirSensibleAndLatents()

  # Define attributes to retrieve in a dictionary
  object_attr = {
                'Handle': [str(x.handle()) for x in all_hx_air_to_air_sensible_and_latent],
                'Name': [x.name().get() for x in all_hx_air_to_air_sensible_and_latent],      
                'Availability Schedule': [x.availabilitySchedule().name().get() if not x.availabilitySchedule().name().isNull() else None for x in all_hx_air_to_air_sensible_and_latent],
                'Nominal Supply Air Flow Rate {m3/s}': [x.nominalSupplyAirFlowRate().get() if not x.nominalSupplyAirFlowRate().isNull() else None for x in all_hx_air_to_air_sensible_and_latent],
                'Sensible Effectiveness at 100% Heating Air Flow {dimensionless}': [x.sensibleEffectivenessat100HeatingAirFlow() for x in all_hx_air_to_air_sensible_and_latent],
                'Latent Effectiveness at 100% Heating Air Flow {dimensionless}': [x.latentEffectivenessat100HeatingAirFlow() for x in all_hx_air_to_air_sensible_and_latent],
                'Sensible Effectiveness at 100% Cooling Air Flow {dimensionless}': [x.sensibleEffectivenessat100CoolingAirFlow() for x in all_hx_air_to_air_sensible_and_latent],
                'Latent Effectiveness at 100% Cooling Air Flow {dimensionless}': [x.latentEffectivenessat100CoolingAirFlow() for x in all_hx_air_to_air_sensible_and_latent],
                'Supply Air Inlet Node': None,
                'Supply Air Outlet Node': None,
                'Exhaust Air Inlet Node': None,
                'Exhaust Air Outlet Node': None,
                'Nominal Electric Power {W}': [x.nominalElectricPower() for x in all_hx_air_to_air_sensible_and_latent],
                'Supply Air Outlet Temperature Control': [x.supplyAirOutletTemperatureControl() for x in all_hx_air_to_air_sensible_and_latent],
                'Heat Exchanger Type': [x.heatExchangerType() for x in all_hx_air_to_air_sensible_and_latent],
                'Frost Control Type': [x.frostControlType() for x in all_hx_air_to_air_sensible_and_latent],
                'Threshold Temperature {C}': [x.thresholdTemperature() for x in all_hx_air_to_air_sensible_and_latent],
                'Initial Defrost Time Fraction {dimensionless}': [x.initialDefrostTimeFraction() for x in all_hx_air_to_air_sensible_and_latent],
                'Rate of Defrost Time Fraction Increase {1/K}': [x.rateofDefrostTimeFractionIncrease() for x in all_hx_air_to_air_sensible_and_latent],
                'Economizer Lockout': [x.economizerLockout() for x in all_hx_air_to_air_sensible_and_latent],
                'Sensible Effectiveness of Heating Air Flow Curve Name': None,
                'Latent Effectiveness of Heating Air Flow Curve Name': None,
                'Sensible Effectiveness of Cooling Air Flow Curve Name': None,
                'Latent Effectiveness of Cooling Air Flow Curve Name': None
                }
  # Create a DataFrame of Heat Exchanger Air To Air Sensible And Latent Objects.
  all_hx_air_to_air_sensible_and_latent_df = pd.DataFrame(columns=object_attr.keys())
  for key in object_attr.keys():
      all_hx_air_to_air_sensible_and_latent_df[key] = object_attr[key]

  # Sort the DataFrame alphabetically by the Name column and reset indexes
  all_hx_air_to_air_sensible_and_latent_df = all_hx_air_to_air_sensible_and_latent_df.sort_values(
      by='Name', ascending=True).reset_index(drop=True)

  print(
      f"The OSM model contains {all_hx_air_to_air_sensible_and_latent_df.shape[0]} Heat Exchanger Air To Air Sensible And Latent Objects Objects")
  return all_hx_air_to_air_sensible_and_latent_df