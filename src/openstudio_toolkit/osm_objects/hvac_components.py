import openstudio
import pandas as pd
import logging
from typing import Dict, Any, List, Optional
from openstudio_toolkit.utils import helpers

# Configure logger
logger = logging.getLogger(__name__)

# --------------------------------------------------
#  ***** OS:Coil:Cooling:DX:VariableRefrigerantFlow
# --------------------------------------------------

def get_coil_cooling_dx_variable_refrigerant_flow_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: Optional[str] = None, 
    name: Optional[str] = None, 
    _object_ref: Optional[openstudio.model.CoilCoolingDXVariableRefrigerantFlow] = None
) -> Dict[str, Any]:
    """
    Retrieve attributes of an OS:Coil:Cooling:DX:VariableRefrigerantFlow from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.CoilCoolingDXVariableRefrigerantFlow, optional): Direct object reference.

    Returns:
    - Dict[str, Any]: A dictionary containing coil attributes.
    """
    target_object = helpers.fetch_object(
        osm_model, "CoilCoolingDXVariableRefrigerantFlow", handle, name, _object_ref)

    if target_object is None:
        return {}

    return {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else "Unnamed Cooling Coil DX VRF",
        'Availability Schedule Name': target_object.availabilitySchedule().name().get() if target_object.availabilitySchedule().name().is_initialized() else None,
        'Rated Total Cooling Capacity {W}': target_object.ratedTotalCoolingCapacity().get() if target_object.ratedTotalCoolingCapacity().is_initialized() else 'autosize',
        'Rated Sensible Heat Ratio': target_object.ratedSensibleHeatRatio().get() if target_object.ratedSensibleHeatRatio().is_initialized() else 'autosize',
        'Rated Air Flow Rate {m3/s}': target_object.ratedAirFlowRate().get() if target_object.ratedAirFlowRate().is_initialized() else 'autosize',
        'Cooling Capacity Ratio Modifier Function of Temperature Curve Name': target_object.coolingCapacityRatioModifierFunctionofTemperatureCurve().name().get() if target_object.coolingCapacityRatioModifierFunctionofTemperatureCurve().name().is_initialized() else None,
        'Cooling Capacity Modifier Curve Function of Flow Fraction Name': target_object.coolingCapacityModifierCurveFunctionofFlowFraction().name().get() if target_object.coolingCapacityModifierCurveFunctionofFlowFraction().name().is_initialized() else None
    }

def get_all_coil_cooling_dx_variable_refrigerant_flow_objects_as_dicts(osm_model: openstudio.model.Model) -> List[Dict[str, Any]]:
    """
    Retrieve attributes for all OS:Coil:Cooling:DX:VariableRefrigerantFlow objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing coil attributes.
    """
    all_objects = osm_model.getCoilCoolingDXVariableRefrigerantFlows()
    return [get_coil_cooling_dx_variable_refrigerant_flow_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_coil_cooling_dx_variable_refrigerant_flow_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:Coil:Cooling:DX:VariableRefrigerantFlow objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all Coil:Cooling:DX:VariableRefrigerantFlow attributes.
    """
    all_objects_dicts = get_all_coil_cooling_dx_variable_refrigerant_flow_objects_as_dicts(osm_model)
    df = pd.DataFrame(all_objects_dicts)

    if not df.empty and 'Name' in df.columns:
        df = df.sort_values(by='Name', ascending=True).reset_index(drop=True)

    logger.info(f"Retrieved {len(df)} Coil:Cooling:DX:VRF objects from the model.")
    return df

# --------------------------------------------------
#  ***** OS:Coil:Heating:DX:VariableRefrigerantFlow
# --------------------------------------------------

def get_coil_heating_dx_variable_refrigerant_flow_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: Optional[str] = None, 
    name: Optional[str] = None, 
    _object_ref: Optional[openstudio.model.CoilHeatingDXVariableRefrigerantFlow] = None
) -> Dict[str, Any]:
    """
    Retrieve attributes of an OS:Coil:Heating:DX:VariableRefrigerantFlow from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.CoilHeatingDXVariableRefrigerantFlow, optional): Direct object reference.

    Returns:
    - Dict[str, Any]: A dictionary containing coil attributes.
    """
    target_object = helpers.fetch_object(
        osm_model, "CoilHeatingDXVariableRefrigerantFlow", handle, name, _object_ref)

    if target_object is None:
        return {}

    return {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else "Unnamed Heating Coil DX VRF",
        'Availability Schedule Name': target_object.availabilitySchedule().name().get() if target_object.availabilitySchedule().name().is_initialized() else None,
        'Rated Total Heating Capacity {W}': target_object.ratedTotalHeatingCapacity().get() if target_object.ratedTotalHeatingCapacity().is_initialized() else 'autosize',
        'Rated Air Flow Rate {m3/s}': target_object.ratedAirFlowRate().get() if target_object.ratedAirFlowRate().is_initialized() else 'autosize',
        'Air Inlet Node Name': target_object.inletPort() if hasattr(target_object, 'inletPort') else None,
        'Air Outlet Node Name': target_object.outletPort() if hasattr(target_object, 'outletPort') else None,
        'Heating Capacity Ratio Modifier Function of Temperature Curve Name': target_object.heatingCapacityRatioModifierFunctionofTemperatureCurve().name().get() if target_object.heatingCapacityRatioModifierFunctionofTemperatureCurve().name().is_initialized() else None,
        'Heating Capacity Modifier Function of Flow Fraction Curve Name': target_object.heatingCapacityModifierFunctionofFlowFractionCurve().name().get() if target_object.heatingCapacityModifierFunctionofFlowFractionCurve().name().is_initialized() else None
    }

def get_all_coil_heating_dx_variable_refrigerant_flow_objects_as_dicts(osm_model: openstudio.model.Model) -> List[Dict[str, Any]]:
    """
    Retrieve attributes for all OS:Coil:Heating:DX:VariableRefrigerantFlow objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing coil attributes.
    """
    all_objects = osm_model.getCoilHeatingDXVariableRefrigerantFlows()
    return [get_coil_heating_dx_variable_refrigerant_flow_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_coil_heating_dx_variable_refrigerant_flow_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:Coil:Heating:DX:VariableRefrigerantFlow objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all Coil:Heating:DX:VariableRefrigerantFlow attributes.
    """
    all_objects_dicts = get_all_coil_heating_dx_variable_refrigerant_flow_objects_as_dicts(osm_model)
    df = pd.DataFrame(all_objects_dicts)

    if not df.empty and 'Name' in df.columns:
        df = df.sort_values(by='Name', ascending=True).reset_index(drop=True)

    logger.info(f"Retrieved {len(df)} Coil:Heating:DX:VRF objects from the model.")
    return df

# --------------------------------------------------
#  ***** OS:Fan:ConstantVolume *********************
# --------------------------------------------------

def get_fan_constant_volume_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: Optional[str] = None, 
    name: Optional[str] = None, 
    _object_ref: Optional[openstudio.model.FanConstantVolume] = None
) -> Dict[str, Any]:
    """
    Retrieve attributes of an OS:Fan:ConstantVolume from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.FanConstantVolume, optional): Direct object reference.

    Returns:
    - Dict[str, Any]: A dictionary containing fan attributes.
    """
    target_object = helpers.fetch_object(
        osm_model, "FanConstantVolume", handle, name, _object_ref)

    if target_object is None:
        return {}

    return {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else "Unnamed Fan CV",
        'Availability Schedule Name': target_object.availabilitySchedule().name().get() if target_object.availabilitySchedule().name().is_initialized() else None,
        'Fan Total Efficiency': target_object.fanTotalEfficiency(),
        'Pressure Rise {Pa}': target_object.pressureRise(),
        'Maximum Flow Rate {m3/s}': target_object.maximumFlowRate().get() if target_object.maximumFlowRate().is_initialized() else 'autosize',
        'Motor Efficiency': target_object.motorEfficiency(),
        'Motor In Airstream Fraction': target_object.motorInAirstreamFraction(),
        'Air Inlet Node Name': target_object.inletPort() if hasattr(target_object, 'inletPort') else None,
        'Air Outlet Node Name': target_object.outletPort() if hasattr(target_object, 'outletPort') else None,
        'End-Use Subcategory': target_object.endUseSubcategory()
    }

def get_all_fan_constant_volume_objects_as_dicts(osm_model: openstudio.model.Model) -> List[Dict[str, Any]]:
    """
    Retrieve attributes for all OS:Fan:ConstantVolume objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing fan attributes.
    """
    all_objects = osm_model.getFanConstantVolumes()
    return [get_fan_constant_volume_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_fan_constant_volume_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:Fan:ConstantVolume objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all Fan:ConstantVolume attributes.
    """
    all_objects_dicts = get_all_fan_constant_volume_objects_as_dicts(osm_model)
    df = pd.DataFrame(all_objects_dicts)

    if not df.empty and 'Name' in df.columns:
        df = df.sort_values(by='Name', ascending=True).reset_index(drop=True)

    logger.info(f"Retrieved {len(df)} Fan:ConstantVolume objects from the model.")
    return df

# --------------------------------------------------
#  ***** OS:Fan:OnOff ******************************
# --------------------------------------------------

def get_fan_on_off_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: Optional[str] = None, 
    name: Optional[str] = None, 
    _object_ref: Optional[openstudio.model.FanOnOff] = None
) -> Dict[str, Any]:
    """
    Retrieve attributes of an OS:Fan:OnOff from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.FanOnOff, optional): Direct object reference.

    Returns:
    - Dict[str, Any]: A dictionary containing fan attributes.
    """
    target_object = helpers.fetch_object(
        osm_model, "FanOnOff", handle, name, _object_ref)

    if target_object is None:
        return {}

    return {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else "Unnamed Fan OnOff",
        'Availability Schedule Name': target_object.availabilitySchedule().name().get() if target_object.availabilitySchedule().name().is_initialized() else None,
        'Fan Total Efficiency': target_object.fanTotalEfficiency(),
        'Pressure Rise {Pa}': target_object.pressureRise(),
        'Maximum Flow Rate {m3/s}': target_object.maximumFlowRate().get() if target_object.maximumFlowRate().is_initialized() else 'autosize',
        'Motor Efficiency': target_object.motorEfficiency(),
        'Motor In Airstream Fraction': target_object.motorInAirstreamFraction().get() if target_object.motorInAirstreamFraction().is_initialized() else None,
        'Air Inlet Node Name': target_object.inletPort() if hasattr(target_object, 'inletPort') else None,
        'Air Outlet Node Name': target_object.outletPort() if hasattr(target_object, 'outletPort') else None,
        'Fan Power Ratio Function of Speed Ratio Curve Name': target_object.fanPowerRatioFunctionofSpeedRatioCurve().nameString(),
        'Fan Efficiency Ratio Function of Speed Ratio Curve Name': target_object.fanEfficiencyRatioFunctionofSpeedRatioCurve().nameString(),
        'End-Use Subcategory': target_object.endUseSubcategory()
    }

def get_all_fan_on_off_objects_as_dicts(osm_model: openstudio.model.Model) -> List[Dict[str, Any]]:
    """
    Retrieve attributes for all OS:Fan:OnOff objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing fan attributes.
    """
    all_objects = osm_model.getFanOnOffs()
    return [get_fan_on_off_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_fan_on_off_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:Fan:OnOff objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all Fan:OnOff attributes.
    """
    all_objects_dicts = get_all_fan_on_off_objects_as_dicts(osm_model)
    df = pd.DataFrame(all_objects_dicts)

    if not df.empty and 'Name' in df.columns:
        df = df.sort_values(by='Name', ascending=True).reset_index(drop=True)

    logger.info(f"Retrieved {len(df)} Fan:OnOff objects from the model.")
    return df

# --------------------------------------------------
#  ***** OS:HeatExchanger:AirToAir:SensibleAndLatent
# --------------------------------------------------

def get_hx_air_to_air_sensible_and_latent_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: Optional[str] = None, 
    name: Optional[str] = None, 
    _object_ref: Optional[openstudio.model.HeatExchangerAirToAirSensibleAndLatent] = None
) -> Dict[str, Any]:
    """
    Retrieve attributes of an OS:HeatExchanger:AirToAir:SensibleAndLatent from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.HeatExchangerAirToAirSensibleAndLatent, optional): Direct object reference.

    Returns:
    - Dict[str, Any]: A dictionary containing HX attributes.
    """
    target_object = helpers.fetch_object(
        osm_model, "HeatExchangerAirToAirSensibleAndLatent", handle, name, _object_ref)

    if target_object is None:
        return {}

    return {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else "Unnamed HX",      
        'Availability Schedule Name': target_object.availabilitySchedule().name().get() if target_object.availabilitySchedule().name().is_initialized() else None,
        'Nominal Supply Air Flow Rate {m3/s}': target_object.nominalSupplyAirFlowRate().get() if target_object.nominalSupplyAirFlowRate().is_initialized() else 'autosize',
        'Sensible Effectiveness at 100% Heating Air Flow {dimensionless}': target_object.sensibleEffectivenessat100HeatingAirFlow(),
        'Latent Effectiveness at 100% Heating Air Flow {dimensionless}': target_object.latentEffectivenessat100HeatingAirFlow(),
        'Sensible Effectiveness at 100% Cooling Air Flow {dimensionless}': target_object.sensibleEffectivenessat100CoolingAirFlow(),
        'Latent Effectiveness at 100% Cooling Air Flow {dimensionless}': target_object.latentEffectivenessat100CoolingAirFlow(),
        'Supply Air Inlet Node Name': target_object.supplyAirInletNode().get().name().get() if target_object.supplyAirInletNode().is_initialized() else None,
        'Supply Air Outlet Node Name': target_object.supplyAirOutletNode().get().name().get() if target_object.supplyAirOutletNode().is_initialized() else None,
        'Exhaust Air Inlet Node Name': target_object.exhaustAirInletNode().get().name().get() if target_object.exhaustAirInletNode().is_initialized() else None,
        'Exhaust Air Outlet Node Name': target_object.exhaustAirOutletNode().get().name().get() if target_object.exhaustAirOutletNode().is_initialized() else None,
        'Nominal Electric Power {W}': target_object.nominalElectricPower(),
        'Supply Air Outlet Temperature Control': target_object.supplyAirOutletTemperatureControl(),
        'Heat Exchanger Type': target_object.heatExchangerType(),
        'Frost Control Type': target_object.frostControlType(),
        'Threshold Temperature {C}': target_object.thresholdTemperature(),
        'Initial Defrost Time Fraction {dimensionless}': target_object.initialDefrostTimeFraction(),
        'Rate of Defrost Time Fraction Increase {1/K}': target_object.rateofDefrostTimeFractionIncrease(),
        'Economizer Lockout': target_object.economizerLockout(),
        'Sensible Effectiveness of Heating Air Flow Curve Name': target_object.sensibleEffectivenessofHeatingAirFlowCurve().get().name().get() if target_object.sensibleEffectivenessofHeatingAirFlowCurve().is_initialized() else None,
        'Latent Effectiveness of Heating Air Flow Curve Name': target_object.latentEffectivenessofHeatingAirFlowCurve().get().name().get() if target_object.latentEffectivenessofHeatingAirFlowCurve().is_initialized() else None,
        'Sensible Effectiveness of Cooling Air Flow Curve Name': target_object.sensibleEffectivenessofCoolingAirFlowCurve().get().name().get() if target_object.sensibleEffectivenessofCoolingAirFlowCurve().is_initialized() else None,
        'Latent Effectiveness of Cooling Air Flow Curve Name': target_object.latentEffectivenessofCoolingAirFlowCurve().get().name().get() if target_object.latentEffectivenessofCoolingAirFlowCurve().is_initialized() else None
    }

def get_all_hx_air_to_air_sensible_and_latent_objects_as_dicts(osm_model: openstudio.model.Model) -> List[Dict[str, Any]]:
    """
    Retrieve attributes for all OS:HeatExchanger:AirToAir:SensibleAndLatent objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing HX attributes.
    """
    all_objects = osm_model.getHeatExchangerAirToAirSensibleAndLatents()
    return [get_hx_air_to_air_sensible_and_latent_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_hx_air_to_air_sensible_and_latent_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:HeatExchanger:AirToAir:SensibleAndLatent objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all HX attributes.
    """
    all_objects_dicts = get_all_hx_air_to_air_sensible_and_latent_objects_as_dicts(osm_model)
    df = pd.DataFrame(all_objects_dicts)

    if not df.empty and 'Name' in df.columns:
        df = df.sort_values(by='Name', ascending=True).reset_index(drop=True)

    logger.info(f"Retrieved {len(df)} HeatExchanger:AirToAir:SensibleAndLatent objects from the model.")
    return df

# --------------------------------------------------
#  ***** OS:AirConditioner:VariableRefrigerantFlow
# --------------------------------------------------

def get_air_conditioner_variable_refrigerant_flow_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: Optional[str] = None, 
    name: Optional[str] = None, 
    _object_ref: Optional[openstudio.model.AirConditionerVariableRefrigerantFlow] = None
) -> Dict[str, Any]:
    """
    Retrieve attributes of an OS:AirConditioner:VariableRefrigerantFlow from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.AirConditionerVariableRefrigerantFlow, optional): Direct object reference.

    Returns:
    - Dict[str, Any]: A dictionary containing VRF AC attributes.
    """
    target_object = helpers.fetch_object(
        osm_model, "AirConditionerVariableRefrigerantFlow", handle, name, _object_ref)

    if target_object is None:
        return {}

    return {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else "Unnamed VRF AC",
        'Availability Schedule Name': target_object.availabilitySchedule().name().get() if target_object.availabilitySchedule().name().is_initialized() else None,
        'Gross Rated Total Cooling Capacity {W}': target_object.grossRatedTotalCoolingCapacity(),
        'Gross Rated Cooling COP {W/W}': target_object.grossRatedCoolingCOP(),
        'Minimum Outdoor Temperature in Cooling Mode {C}': target_object.minimumOutdoorTemperatureinCoolingMode(),
        'Maximum Outdoor Temperature in Cooling Mode {C}': target_object.maximumOutdoorTemperatureinCoolingMode(),
        'Cooling Capacity Ratio Modifier Function of Low Temperature Curve Name': target_object.coolingCapacityRatioModifierFunctionofLowTemperatureCurve().get().name().get() if target_object.coolingCapacityRatioModifierFunctionofLowTemperatureCurve().is_initialized() else None,
        'Cooling Capacity Ratio Boundary Curve Name': target_object.coolingCapacityRatioBoundaryCurve().get().name().get() if target_object.coolingCapacityRatioBoundaryCurve().is_initialized() else None,
        'Cooling Capacity Ratio Modifier Function of High Temperature Curve Name': target_object.coolingCapacityRatioModifierFunctionofHighTemperatureCurve().get().name().get() if target_object.coolingCapacityRatioModifierFunctionofHighTemperatureCurve().is_initialized() else None,
        'Cooling Energy Input Ratio Modifier Function of Low Temperature Curve Name': target_object.coolingEnergyInputRatioModifierFunctionofLowTemperatureCurve().get().name().get() if target_object.coolingEnergyInputRatioModifierFunctionofLowTemperatureCurve().is_initialized() else None,
        'Cooling Energy Input Ratio Boundary Curve Name': target_object.coolingEnergyInputRatioBoundaryCurve().get().name().get() if target_object.coolingEnergyInputRatioBoundaryCurve().is_initialized() else None,
        'Cooling Energy Input Ratio Modifier Function of High Temperature Curve Name': target_object.coolingEnergyInputRatioModifierFunctionofHighTemperatureCurve().get().name().get() if target_object.coolingEnergyInputRatioModifierFunctionofHighTemperatureCurve().is_initialized() else None,
        'Cooling Energy Input Ratio Modifier Function of Low Part-Load Ratio Curve Name': target_object.coolingEnergyInputRatioModifierFunctionofLowPartLoadRatioCurve().get().name().get() if target_object.coolingEnergyInputRatioModifierFunctionofLowPartLoadRatioCurve().is_initialized() else None,
        'Cooling Energy Input Ratio Modifier Function of High Part-Load Ratio Curve Name': target_object.coolingEnergyInputRatioModifierFunctionofHighPartLoadRatioCurve().get().name().get() if target_object.coolingEnergyInputRatioModifierFunctionofHighPartLoadRatioCurve().is_initialized() else None,
        'Cooling Combination Ratio Correction Factor Curve Name': target_object.coolingCombinationRatioCorrectionFactorCurve().get().name().get() if target_object.coolingCombinationRatioCorrectionFactorCurve().is_initialized() else None,
        'Cooling Part-Load Fraction Correlation Curve Name': target_object.coolingPartLoadFractionCorrelationCurve().get().name().get() if target_object.coolingPartLoadFractionCorrelationCurve().is_initialized() else None,
        'Gross Rated Heating Capacity {W}': target_object.grossRatedHeatingCapacity(),
        'Rated Heating Capacity Sizing Ratio {W/W}': target_object.ratedHeatingCapacitySizingRatio(),
        'Rated Heating COP {W/W}': target_object.ratedHeatingCOP(),
        'Minimum Outdoor Temperature in Heating Mode {C}': target_object.minimumOutdoorTemperatureinHeatingMode(),
        'Maximum Outdoor Temperature in Heating Mode {C}': target_object.maximumOutdoorTemperatureinHeatingMode(),
        'Heating Capacity Ratio Modifier Function of Low Temperature Curve Name': target_object.heatingCapacityRatioModifierFunctionofLowTemperatureCurve().get().name().get() if target_object.heatingCapacityRatioModifierFunctionofLowTemperatureCurve().is_initialized() else None,
        'Heating Capacity Ratio Boundary Curve Name': target_object.heatingCapacityRatioBoundaryCurve().get().name().get() if target_object.heatingCapacityRatioBoundaryCurve().is_initialized() else None,
        'Heating Capacity Ratio Modifier Function of High Temperature Curve Name': target_object.heatingCapacityRatioModifierFunctionofHighTemperatureCurve().get().name().get() if target_object.heatingCapacityRatioModifierFunctionofHighTemperatureCurve().is_initialized() else None,
        'Heating Energy Input Ratio Modifier Function of Low Temperature Curve Name': target_object.heatingEnergyInputRatioModifierFunctionofLowTemperatureCurve().get().name().get() if target_object.heatingEnergyInputRatioModifierFunctionofLowTemperatureCurve().is_initialized() else None,
        'Heating Energy Input Ratio Boundary Curve Name': target_object.heatingEnergyInputRatioBoundaryCurve().get().name().get() if target_object.heatingEnergyInputRatioBoundaryCurve().is_initialized() else None,
        'Heating Energy Input Ratio Modifier Function of High Temperature Curve Name': target_object.heatingEnergyInputRatioModifierFunctionofHighTemperatureCurve().get().name().get() if target_object.heatingEnergyInputRatioModifierFunctionofHighTemperatureCurve().is_initialized() else None,
        'Heating Performance Curve Outdoor Temperature Type': target_object.heatingPerformanceCurveOutdoorTemperatureType(),
        'Heating Energy Input Ratio Modifier Function of Low Part-Load Ratio Curve Name': target_object.heatingEnergyInputRatioModifierFunctionofLowPartLoadRatioCurve().get().name().get() if target_object.heatingEnergyInputRatioModifierFunctionofLowPartLoadRatioCurve().is_initialized() else None,
        'Heating Energy Input Ratio Modifier Function of High Part-Load Ratio Curve Name': target_object.heatingEnergyInputRatioModifierFunctionofHighPartLoadRatioCurve().get().name().get() if target_object.heatingEnergyInputRatioModifierFunctionofHighPartLoadRatioCurve().is_initialized() else None,
        'Heating Combination Ratio Correction Factor Curve Name': target_object.heatingCombinationRatioCorrectionFactorCurve().get().name().get() if target_object.heatingCombinationRatioCorrectionFactorCurve().is_initialized() else None,
        'Heating Part-Load Fraction Correlation Curve Name': target_object.heatingPartLoadFractionCorrelationCurve().get().name().get() if target_object.heatingPartLoadFractionCorrelationCurve().is_initialized() else None,
        'Minimum Heat Pump Part-Load Ratio {dimensionless}': target_object.minimumHeatPumpPartLoadRatio(),
        'Zone Name for Master Thermostat Location': target_object.zoneforMasterThermostatLocation().get().name().get() if target_object.zoneforMasterThermostatLocation().is_initialized() else None,
        'Master Thermostat Priority Control Type': target_object.masterThermostatPriorityControlType(),
        'Thermostat Priority Schedule Name': target_object.thermostatPrioritySchedule().get().name().get() if target_object.thermostatPrioritySchedule().is_initialized() else None,
        'Heat Pump Waste Heat Recovery': target_object.heatPumpWasteHeatRecovery(),
        'Equivalent Piping Length used for Piping Correction Factor in Cooling Mode {m}': target_object.equivalentPipingLengthusedforPipingCorrectionFactorinCoolingMode(),
        'Vertical Height used for Piping Correction Factor {m}': target_object.verticalHeightusedforPipingCorrectionFactor(),
        'Piping Correction Factor for Length in Cooling Mode Curve Name': target_object.pipingCorrectionFactorforLengthinCoolingModeCurve().get().name().get() if target_object.pipingCorrectionFactorforLengthinCoolingModeCurve().is_initialized() else None,
        'Piping Correction Factor for Height in Cooling Mode Coefficient {1/m}': target_object.pipingCorrectionFactorforHeightinCoolingModeCoefficient(),
        'Equivalent Piping Length used for Piping Correction Factor in Heating Mode {m}': target_object.equivalentPipingLengthusedforPipingCorrectionFactorinHeatingMode(),
        'Piping Correction Factor for Length in Heating Mode Curve Name': target_object.pipingCorrectionFactorforLengthinHeatingModeCurve().get().name().get() if target_object.pipingCorrectionFactorforLengthinHeatingModeCurve().is_initialized() else None,
        'Piping Correction Factor for Height in Heating Mode Coefficient {1/m}': target_object.pipingCorrectionFactorforHeightinHeatingModeCoefficient(),
        'Crankcase Heater Power per Compressor {W}': target_object.crankcaseHeaterPowerperCompressor(),
        'Number of Compressors {dimensionless}': target_object.numberofCompressors(),
        'Ratio of Compressor Size to Total Compressor Capacity {W/W}': target_object.ratioofCompressorSizetoTotalCompressorCapacity(),
        'Maximum Outdoor Dry-bulb Temperature for Crankcase Heater {C}': target_object.maximumOutdoorDrybulbTemperatureforCrankcaseHeater(),
        'Defrost Strategy': target_object.defrostStrategy(),
        'Defrost Control': target_object.defrostControl(),
        'Defrost Energy Input Ratio Modifier Function of Temperature Curve Name': target_object.defrostEnergyInputRatioModifierFunctionofTemperatureCurve().get().name().get() if target_object.defrostEnergyInputRatioModifierFunctionofTemperatureCurve().is_initialized() else None,
        'Defrost Time Period Fraction {dimensionless}': target_object.defrostTimePeriodFraction(),
        'Resistive Defrost Heater Capacity {W}': target_object.resistiveDefrostHeaterCapacity(),
        'Maximum Outdoor Dry-bulb Temperature for Defrost Operation {C}': target_object.maximumOutdoorDrybulbTemperatureforDefrostOperation(),
        'Condenser Type': target_object.condenserType(),
        'Condenser Inlet Node Name': target_object.condenserInletNode().get().name().get() if target_object.condenserInletNode().is_initialized() else None,
        'Condenser Outlet Node Name': target_object.condenserOutletNode().get().name().get() if target_object.condenserOutletNode().is_initialized() else None,
        'Water Condenser Volume Flow Rate {m3/s}': target_object.waterCondenserVolumeFlowRate(),
        'Evaporative Condenser Effectiveness {dimensionless}': target_object.evaporativeCondenserEffectiveness(),
        'Evaporative Condenser Air Flow Rate {m3/s}': target_object.evaporativeCondenserAirFlowRate(),
        'Evaporative Condenser Pump Rated Power Consumption {W}': target_object.evaporativeCondenserPumpRatedPowerConsumption(),
        'Basin Heater Capacity {W/K}': target_object.basinHeaterCapacity(),
        'Basin Heater Setpoint Temperature {C}': target_object.basinHeaterSetpointTemperature(),
        'Basin Heater Operating Schedule Name': target_object.basinHeaterOperatingSchedule().get().name().get() if target_object.basinHeaterOperatingSchedule().is_initialized() else None,
        'Fuel Type': target_object.fuelType(),
        'Minimum Outdoor Temperature in Heat Recovery Mode {C}': target_object.minimumOutdoorTemperatureinHeatRecoveryMode(),
        'Maximum Outdoor Temperature in Heat Recovery Mode {C}': target_object.maximumOutdoorTemperatureinHeatRecoveryMode(),
        'Heat Recovery Cooling Capacity Modifier Curve Name': target_object.heatRecoveryCoolingCapacityModifierCurve().get().name().get() if target_object.heatRecoveryCoolingCapacityModifierCurve().is_initialized() else None,
        'Initial Heat Recovery Cooling Capacity Fraction {W/W}': target_object.initialHeatRecoveryCoolingCapacityFraction(),
        'Heat Recovery Cooling Capacity Time Constant {hr}': target_object.heatRecoveryCoolingCapacityTimeConstant(),
        'Heat Recovery Cooling Energy Modifier Curve Name': target_object.heatRecoveryCoolingEnergyModifierCurve().get().name().get() if target_object.heatRecoveryCoolingEnergyModifierCurve().is_initialized() else None,
        'Initial Heat Recovery Cooling Energy Fraction {W/W}': target_object.initialHeatRecoveryCoolingEnergyFraction(),
        'Heat Recovery Cooling Energy Time Constant {hr}': target_object.heatRecoveryCoolingEnergyTimeConstant(),
        'Heat Recovery Heating Capacity Modifier Curve Name': target_object.heatRecoveryHeatingCapacityModifierCurve().get().name().get() if target_object.heatRecoveryHeatingCapacityModifierCurve().is_initialized() else None,
        'Initial Heat Recovery Heating Capacity Fraction {W/W}': target_object.initialHeatRecoveryHeatingCapacityFraction(),
        'Heat Recovery Heating Capacity Time Constant {hr}': target_object.heatRecoveryHeatingCapacityTimeConstant(),
        'Heat Recovery Heating Energy Modifier Curve Name': target_object.heatRecoveryHeatingEnergyModifierCurve().get().name().get() if target_object.heatRecoveryHeatingEnergyModifierCurve().is_initialized() else None,
        'Initial Heat Recovery Heating Energy Fraction {W/W}': target_object.initialHeatRecoveryHeatingEnergyFraction(),
        'Heat Recovery Heating Energy Time Constant {hr}': target_object.heatRecoveryHeatingEnergyTimeConstant()
    }

def get_all_air_conditioner_variable_refrigerant_flow_objects_as_dicts(osm_model: openstudio.model.Model) -> List[Dict[str, Any]]:
    """
    Retrieve attributes for all OS:AirConditioner:VariableRefrigerantFlow objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing VRF AC attributes.
    """
    all_objects = osm_model.getAirConditionerVariableRefrigerantFlows()
    return [get_air_conditioner_variable_refrigerant_flow_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_air_conditioner_variable_refrigerant_flow_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:AirConditioner:VariableRefrigerantFlow objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all AirConditioner:VariableRefrigerantFlow attributes.
    """
    all_objects_dicts = get_all_air_conditioner_variable_refrigerant_flow_objects_as_dicts(osm_model)
    df = pd.DataFrame(all_objects_dicts)

    if not df.empty and 'Name' in df.columns:
        df = df.sort_values(by='Name', ascending=True).reset_index(drop=True)

    logger.info(f"Retrieved {len(df)} AirConditioner:VariableRefrigerantFlow objects from the model.")
    return df

#-----------------------
#--- OS:Coil:Heating:Gas
#------------------------

# --------------------------------------------------
#  ***** OS:Coil:Heating:Gas ***********************
# --------------------------------------------------

def get_coil_heating_gas_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: Optional[str] = None, 
    name: Optional[str] = None, 
    _object_ref: Optional[openstudio.model.CoilHeatingGas] = None
) -> Dict[str, Any]:
    """
    Retrieve attributes of an OS:Coil:Heating:Gas from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.CoilHeatingGas, optional): Direct object reference.

    Returns:
    - Dict[str, Any]: A dictionary containing coil attributes.
    """
    target_object = helpers.fetch_object(
        osm_model, "CoilHeatingGas", handle, name, _object_ref)

    if target_object is None:
        return {}

    return {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else "Unnamed Heating Coil Gas",
        'Availability Schedule Name': target_object.availabilitySchedule().name().get() if target_object.availabilitySchedule().name().is_initialized() else None,
        'Gas Burner Efficiency': target_object.gasBurnerEfficiency(),
        'Nominal Capacity {W}': target_object.nominalCapacity().get() if target_object.nominalCapacity().is_initialized() else 'autosize',
        'Air Inlet Node Name': target_object.inletPort() if hasattr(target_object, 'inletPort') else None,
        'Air Outlet Node Name': target_object.outletPort() if hasattr(target_object, 'outletPort') else None,
        'Temperature Setpoint Node Name': target_object.temperatureSetpointNode().get().name().get() if target_object.temperatureSetpointNode().is_initialized() else None,
        'On Cycle Parasitic Electric Load {W}': target_object.onCycleParasiticElectricLoad(),
        'Part Load Fraction Correlation Curve Name': target_object.partLoadFractionCorrelationCurve().get().name().get() if target_object.partLoadFractionCorrelationCurve().is_initialized() else None,
        'Off Cycle Parasitic Gas Load {W}': target_object.offCycleParasiticGasLoad()                           
    }

def get_all_coil_heating_gas_objects_as_dicts(osm_model: openstudio.model.Model) -> List[Dict[str, Any]]:
    """
    Retrieve attributes for all OS:Coil:Heating:Gas objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing coil attributes.
    """
    all_objects = osm_model.getCoilHeatingGass()
    return [get_coil_heating_gas_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_coil_heating_gas_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:Coil:Heating:Gas objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all Coil:Heating:Gas attributes.
    """
    all_objects_dicts = get_all_coil_heating_gas_objects_as_dicts(osm_model)
    df = pd.DataFrame(all_objects_dicts)

    if not df.empty and 'Name' in df.columns:
        df = df.sort_values(by='Name', ascending=True).reset_index(drop=True)

    logger.info(f"Retrieved {len(df)} Coil:Heating:Gas objects from the model.")
    return df

#---------------------------
#--- OOS:Coil:Heating:Water
#---------------------------
# --------------------------------------------------
#  ***** OS:Coil:Heating:Water *********************
# --------------------------------------------------

def get_coil_heating_water_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: Optional[str] = None, 
    name: Optional[str] = None, 
    _object_ref: Optional[openstudio.model.CoilHeatingWater] = None
) -> Dict[str, Any]:
    """
    Retrieve attributes of an OS:Coil:Heating:Water from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.CoilHeatingWater, optional): Direct object reference.

    Returns:
    - Dict[str, Any]: A dictionary containing coil attributes.
    """
    target_object = helpers.fetch_object(
        osm_model, "CoilHeatingWater", handle, name, _object_ref)

    if target_object is None:
        return {}

    return {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else "Unnamed Heating Coil Water",
        'Availability Schedule Name': target_object.availabilitySchedule().name().get() if target_object.availabilitySchedule().name().is_initialized() else None,
        'U-Factor Times Area Value {W/K}': target_object.uFactorTimesAreaValue().get() if target_object.uFactorTimesAreaValue().is_initialized() else 'autosize',
        'Maximum Water Flow Rate {m3/s}': target_object.maximumWaterFlowRate().get() if target_object.maximumWaterFlowRate().is_initialized() else 'autosize',
        'Water Inlet Node Name': target_object.waterInletNode().get().name().get() if target_object.waterInletNode().is_initialized() else None,
        'Water Outlet Node Name': target_object.waterOutletNode().get().name().get() if target_object.waterOutletNode().is_initialized() else None,
        'Air Inlet Node Name': target_object.airInletNode().get().name().get() if target_object.airInletNode().is_initialized() else None,
        'Air Outlet Node Name': target_object.airOutletNode().get().name().get() if target_object.airOutletNode().is_initialized() else None,
        'Performance Input Method': target_object.performanceInputMethod(),
        'Rated Capacity {W}': target_object.ratedCapacity().get() if target_object.ratedCapacity().is_initialized() else 'autosize',
        'Rated Inlet Water Temperature {C}': target_object.ratedInletWaterTemperature(),
        'Rated Inlet Air Temperature {C}': target_object.ratedInletAirTemperature(),
        'Rated Outlet Water Temperature {C}': target_object.ratedOutletWaterTemperature(),
        'Rated Outlet Air Temperature {C}': target_object.ratedOutletAirTemperature(),
        'Rated Ratio for Air and Water Convection': target_object.ratedRatioForAirAndWaterConvection()
    }

def get_all_coil_heating_water_objects_as_dicts(osm_model: openstudio.model.Model) -> List[Dict[str, Any]]:
    """
    Retrieve attributes for all OS:Coil:Heating:Water objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing coil attributes.
    """
    all_objects = osm_model.getCoilHeatingWaters()
    return [get_coil_heating_water_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_coil_heating_water_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:Coil:Heating:Water objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all Coil:Heating:Water attributes.
    """
    all_objects_dicts = get_all_coil_heating_water_objects_as_dicts(osm_model)
    df = pd.DataFrame(all_objects_dicts)

    if not df.empty and 'Name' in df.columns:
        df = df.sort_values(by='Name', ascending=True).reset_index(drop=True)

    logger.info(f"Retrieved {len(df)} Coil:Heating:Water objects from the model.")
    return df

#---------------------------
#--- OOS:Coil:Cooling:Water
#---------------------------

# --------------------------------------------------
#  ***** OS:Coil:Cooling:Water *********************
# --------------------------------------------------

def get_coil_cooling_water_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: Optional[str] = None, 
    name: Optional[str] = None, 
    _object_ref: Optional[openstudio.model.CoilCoolingWater] = None
) -> Dict[str, Any]:
    """
    Retrieve attributes of an OS:Coil:Cooling:Water from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.CoilCoolingWater, optional): Direct object reference.

    Returns:
    - Dict[str, Any]: A dictionary containing coil attributes.
    """
    target_object = helpers.fetch_object(
        osm_model, "CoilCoolingWater", handle, name, _object_ref)

    if target_object is None:
        return {}

    return {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else "Unnamed Cooling Coil Water",
        'Availability Schedule Name': target_object.availabilitySchedule().name().get() if target_object.availabilitySchedule().name().is_initialized() else None,
        'Design Water Flow Rate {m3/s}': target_object.designWaterFlowRate().get() if target_object.designWaterFlowRate().is_initialized() else 'autosize',
        'Design Air Flow Rate {m3/s}': target_object.designAirFlowRate().get() if target_object.designAirFlowRate().is_initialized() else 'autosize',
        'Design Inlet Water Temperature {C}': target_object.designInletWaterTemperature().get() if target_object.designInletWaterTemperature().is_initialized() else 'autosize',
        'Design Inlet Air Temperature {C}': target_object.designInletAirTemperature().get() if target_object.designInletAirTemperature().is_initialized() else 'autosize',        
        'Design Outlet Air Temperature {C}': target_object.designOutletAirTemperature().get() if target_object.designOutletAirTemperature().is_initialized() else 'autosize',
        'Design Inlet Air Humidity Ratio {kg-H2O/kg-air}': target_object.designInletAirHumidityRatio().get() if target_object.designInletAirHumidityRatio().is_initialized() else 'autosize',
        'Design Outlet Air Humidity Ratio {kg-H2O/kg-air}': target_object.designOutletAirHumidityRatio().get() if target_object.designOutletAirHumidityRatio().is_initialized() else 'autosize',
        'Water Inlet Node Name': target_object.waterInletNode().get().name().get() if target_object.waterInletNode().is_initialized() else None,
        'Water Outlet Node Name': target_object.waterOutletNode().get().name().get() if target_object.waterOutletNode().is_initialized() else None,
        'Air Inlet Node Name': target_object.airInletNode().get().name().get() if target_object.airInletNode().is_initialized() else None,
        'Air Outlet Node Name': target_object.airOutletNode().get().name().get() if target_object.airOutletNode().is_initialized() else None,
        'Heat Exchanger Configuration': target_object.heatExchangerConfiguration()        
    }

def get_all_coil_cooling_water_objects_as_dicts(osm_model: openstudio.model.Model) -> List[Dict[str, Any]]:
    """
    Retrieve attributes for all OS:Coil:Cooling:Water objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing coil attributes.
    """
    all_objects = osm_model.getCoilCoolingWaters()
    return [get_coil_cooling_water_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_coil_cooling_water_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:Coil:Cooling:Water objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all Coil:Cooling:Water attributes.
    """
    all_objects_dicts = get_all_coil_cooling_water_objects_as_dicts(osm_model)
    df = pd.DataFrame(all_objects_dicts)

    if not df.empty and 'Name' in df.columns:
        df = df.sort_values(by='Name', ascending=True).reset_index(drop=True)

    logger.info(f"Retrieved {len(df)} Coil:Cooling:Water objects from the model.")
    return df


# --------------------------------------------------
#  ***** OS:Pump:VariableSpeed *********************
# --------------------------------------------------


# --------------------------------------------------
#  ***** OS:Pump:VariableSpeed *********************
# --------------------------------------------------

def get_pump_variable_speed_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: Optional[str] = None, 
    name: Optional[str] = None, 
    _object_ref: Optional[openstudio.model.PumpVariableSpeed] = None
) -> Dict[str, Any]:
    """
    Retrieve attributes of an OS:Pump:VariableSpeed from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.PumpVariableSpeed, optional): Direct object reference.

    Returns:
    - Dict[str, Any]: A dictionary containing pump attributes.
    """
    target_object = helpers.fetch_object(
        osm_model, "PumpVariableSpeed", handle, name, _object_ref)

    if target_object is None:
        return {}

    return {
        'Handle': str(target_object.handle()), 
        'Name': target_object.name().get() if target_object.name().is_initialized() else "Unnamed Pump VS", 
        'Inlet Node Name': target_object.inletPort() if hasattr(target_object, 'inletPort') else None, 
        'Outlet Node Name': target_object.outletPort() if hasattr(target_object, 'outletPort') else None, 
        'Rated Flow Rate {m3/s}': target_object.ratedFlowRate().get() if target_object.ratedFlowRate().is_initialized() else 'autosize', 
        'Rated Pump Head {Pa}': target_object.ratedPumpHead(), 
        'Rated Power Consumption {W}': target_object.ratedPowerConsumption().get() if target_object.ratedPowerConsumption().is_initialized() else 'autosize',
        'Motor Efficiency': target_object.motorEfficiency(), 
        'Fraction of Motor Inefficiencies to Fluid Stream': target_object.fractionofMotorInefficienciestoFluidStream(), 
        'Coefficient 1 of the Part Load Performance Curve': target_object.coefficient1ofthePartLoadPerformanceCurve(), 
        'Coefficient 2 of the Part Load Performance Curve': target_object.coefficient2ofthePartLoadPerformanceCurve(), 
        'Coefficient 3 of the Part Load Performance Curve': target_object.coefficient3ofthePartLoadPerformanceCurve(), 
        'Coefficient 4 of the Part Load Performance Curve': target_object.coefficient4ofthePartLoadPerformanceCurve(), 
        'Minimum Flow Rate {m3/s}': target_object.minimumFlowRate(), 
        'Pump Control Type': target_object.pumpControlType(), 
        'Pump Flow Rate Schedule Name': target_object.pumpFlowRateSchedule().get().name().get() if target_object.pumpFlowRateSchedule().is_initialized() else None, 
        'Skin Loss Radiative Fraction': target_object.skinLossRadiativeFraction(), 
        'Design Power Sizing Method': target_object.designPowerSizingMethod(), 
        'Design Electric Power per Unit Flow Rate {W/(m3/s)}': target_object.designElectricPowerPerUnitFlowRate(), 
        'Design Shaft Power per Unit Flow Rate per Unit Head {W-s/m3-Pa}': target_object.designShaftPowerPerUnitFlowRatePerUnitHead(), 
        'Design Minimum Flow Rate Fraction': target_object.designMinimumFlowRateFraction(), 
        'End-Use Subcategory': target_object.endUseSubcategory()
    }

def get_all_pump_variable_speed_objects_as_dicts(osm_model: openstudio.model.Model) -> List[Dict[str, Any]]:
    """
    Retrieve attributes for all OS:Pump:VariableSpeed objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing pump attributes.
    """
    all_objects = osm_model.getPumpVariableSpeeds()
    return [get_pump_variable_speed_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_pump_variable_speed_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:Pump:VariableSpeed objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all Pump:VariableSpeed attributes.
    """
    all_objects_dicts = get_all_pump_variable_speed_objects_as_dicts(osm_model)
    df = pd.DataFrame(all_objects_dicts)

    if not df.empty and 'Name' in df.columns:
        df = df.sort_values(by='Name', ascending=True).reset_index(drop=True)

    logger.info(f"Retrieved {len(df)} Pump:VariableSpeed objects from the model.")
    return df


# --------------------------------------------------
#  ***** OS:Chiller:Electric:EIR *******************
# --------------------------------------------------


# --------------------------------------------------
#  ***** OS:Chiller:Electric:EIR *******************
# --------------------------------------------------

def get_chiller_electric_eir_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: Optional[str] = None, 
    name: Optional[str] = None, 
    _object_ref: Optional[openstudio.model.ChillerElectricEIR] = None
) -> Dict[str, Any]:
    """
    Retrieve attributes of an OS:Chiller:Electric:EIR from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.ChillerElectricEIR, optional): Direct object reference.

    Returns:
    - Dict[str, Any]: A dictionary containing chiller attributes.
    """  
    target_object = helpers.fetch_object(
        osm_model, "ChillerElectricEIR", handle, name, _object_ref)

    if target_object is None:
        return {}

    return {
        'Handle': str(target_object.handle()), 
        'Name': target_object.name().get() if target_object.name().is_initialized() else "Unnamed Chiller", 
        'Reference Capacity {W}': target_object.referenceCapacity().get() if target_object.referenceCapacity().is_initialized() else 'autosize', 
        'Reference COP {W/W}': target_object.referenceCOP(), 
        'Reference Leaving Chilled Water Temperature {C}': target_object.referenceLeavingChilledWaterTemperature(), 
        'Reference Entering Condenser Fluid Temperature {C}': target_object.referenceEnteringCondenserFluidTemperature(), 
        'Reference Chilled Water Flow Rate {m3/s}': target_object.referenceChilledWaterFlowRate().get() if target_object.referenceChilledWaterFlowRate().is_initialized() else 'autosize', 
        'Reference Condenser Fluid Flow Rate {m3/s}': target_object.referenceCondenserFluidFlowRate().get() if target_object.referenceCondenserFluidFlowRate().is_initialized() else 'autosize', 
        'Cooling Capacity Function of Temperature Curve Name': target_object.coolingCapacityFunctionOfTemperature().name().get() if target_object.coolingCapacityFunctionOfTemperature().name().is_initialized() else None, 
        'Electric Input to Cooling Output Ratio Function of Temperature Curve Name': target_object.electricInputToCoolingOutputRatioFunctionOfTemperature().name().get() if target_object.electricInputToCoolingOutputRatioFunctionOfTemperature().name().is_initialized() else None,  
        'Electric Input to Cooling Output Ratio Function of Part Load Ratio Curve Name': target_object.electricInputToCoolingOutputRatioFunctionOfPLR().name().get() if target_object.electricInputToCoolingOutputRatioFunctionOfPLR().name().is_initialized() else None, 
        'Minimum Part Load Ratio': target_object.minimumPartLoadRatio(), 
        'Maximum Part Load Ratio': target_object.maximumPartLoadRatio(), 
        'Optimum Part Load Ratio': target_object.optimumPartLoadRatio(), 
        'Minimum Unloading Ratio': target_object.minimumUnloadingRatio(), 
        'Chilled Water Inlet Node Name': target_object.supplyInletNode().get().name().get() if target_object.supplyInletNode().is_initialized() else None, 
        'Chilled Water Outlet Node Name': target_object.supplyOutletNode().get().name().get() if target_object.supplyOutletNode().is_initialized() else None, 
        'Condenser Inlet Node Name': target_object.condenserInletNode().get().name().get() if target_object.condenserInletNode().is_initialized() else None, 
        'Condenser Outlet Node Name': target_object.condenserOutletNode().get().name().get() if target_object.condenserOutletNode().is_initialized() else None, 
        'Condenser Type': target_object.condenserType(), 
        'Condenser Fan Power Ratio {W/W}': target_object.condenserFanPowerRatio(), 
        'Leaving Chilled Water Lower Temperature Limit {C}': target_object.leavingChilledWaterLowerTemperatureLimit(), 
        'Chiller Flow Mode': target_object.chillerFlowMode(), 
        'Design Heat Recovery Water Flow Rate {m3/s}': target_object.designHeatRecoveryWaterFlowRate().get() if target_object.designHeatRecoveryWaterFlowRate().is_initialized() else 'autosize', 
        'Heat Recovery Inlet Node Name': target_object.heatRecoveryInletNode().get().name().get() if target_object.heatRecoveryInletNode().is_initialized() else None, 
        'Heat Recovery Outlet Node Name': target_object.heatRecoveryOutletNode().get().name().get() if target_object.heatRecoveryOutletNode().is_initialized() else None, 
        'Sizing Factor': target_object.sizingFactor(), 
        'Basin Heater Capacity {W/K}': target_object.basinHeaterCapacity(), 
        'Basin Heater Setpoint Temperature {C}': target_object.basinHeaterSetpointTemperature(), 
        'Basin Heater Operating Schedule Name': target_object.basinHeaterSchedule().get().name().get() if target_object.basinHeaterSchedule().is_initialized() else None, 
        'Condenser Heat Recovery Relative Capacity Fraction': target_object.condenserHeatRecoveryRelativeCapacityFraction(), 
        'Heat Recovery Leaving Temperature Setpoint Node Name': target_object.heatRecoveryLeavingTemperatureSetpointNode().get().name().get() if target_object.heatRecoveryLeavingTemperatureSetpointNode().is_initialized() else None, 
        'End-Use Subcategory': target_object.endUseSubcategory()
    }

def get_all_chiller_electric_eir_objects_as_dicts(osm_model: openstudio.model.Model) -> List[Dict[str, Any]]:
    """
    Retrieve attributes for all OS:Chiller:Electric:EIR objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing chiller attributes.
    """
    all_objects = osm_model.getChillerElectricEIRs()
    return [get_chiller_electric_eir_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_chiller_electric_eir_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:Chiller:Electric:EIR objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all Chiller:Electric:EIR attributes.
    """
    all_objects_dicts = get_all_chiller_electric_eir_objects_as_dicts(osm_model)
    df = pd.DataFrame(all_objects_dicts)

    if not df.empty and 'Name' in df.columns:
        df = df.sort_values(by='Name', ascending=True).reset_index(drop=True)

    logger.info(f"Retrieved {len(df)} Chiller:Electric:EIR objects from the model.")
    return df