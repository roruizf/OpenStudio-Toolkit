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
