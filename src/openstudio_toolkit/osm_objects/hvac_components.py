import logging
from typing import Any

import openstudio
import pandas as pd

from openstudio_toolkit._sdk import opt, optional_name, related_name
from openstudio_toolkit.osm_objects._base import build_dataframe
from openstudio_toolkit.utils import helpers

# Configure logger
logger = logging.getLogger(__name__)

# --------------------------------------------------
#  ***** OS:Coil:Cooling:DX:VariableRefrigerantFlow
# --------------------------------------------------

COIL_COOLING_DX_VARIABLE_REFRIGERANT_FLOW_COLUMNS = (
    'Handle',
    'Name',
    'Availability Schedule Name',
    'Rated Total Cooling Capacity {W}',
    'Rated Sensible Heat Ratio',
    'Rated Air Flow Rate {m3/s}',
    'Cooling Capacity Ratio Modifier Function of Temperature Curve Name',
    'Cooling Capacity Modifier Curve Function of Flow Fraction Name',
)

def get_coil_cooling_dx_variable_refrigerant_flow_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: str | None = None, 
    name: str | None = None, 
    _object_ref: openstudio.model.CoilCoolingDXVariableRefrigerantFlow | None = None
) -> dict[str, Any]:
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
        'Name': opt(target_object.name()) if target_object.name().is_initialized() else "Unnamed Cooling Coil DX VRF",
        'Availability Schedule Name': related_name(target_object, "Availability Schedule"),
        'Rated Total Cooling Capacity {W}': opt(target_object.ratedTotalCoolingCapacity()) if target_object.ratedTotalCoolingCapacity().is_initialized() else 'autosize',
        'Rated Sensible Heat Ratio': opt(target_object.ratedSensibleHeatRatio()) if target_object.ratedSensibleHeatRatio().is_initialized() else 'autosize',
        'Rated Air Flow Rate {m3/s}': opt(target_object.ratedAirFlowRate()) if target_object.ratedAirFlowRate().is_initialized() else 'autosize',
        'Cooling Capacity Ratio Modifier Function of Temperature Curve Name': related_name(target_object, "Cooling Capacity Ratio Modifier Function of Temperature Curve"),
        'Cooling Capacity Modifier Curve Function of Flow Fraction Name': related_name(target_object, "Cooling Capacity Modifier Curve Function of Flow Fraction")
    }

def get_all_coil_cooling_dx_variable_refrigerant_flow_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict[str, Any]]:
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
    return build_dataframe(
        all_objects_dicts, "Coil:Cooling:DX:VRF", sort_by="Name",
        columns=COIL_COOLING_DX_VARIABLE_REFRIGERANT_FLOW_COLUMNS)

# --------------------------------------------------
#  ***** OS:Coil:Heating:DX:VariableRefrigerantFlow
# --------------------------------------------------

COIL_HEATING_DX_VARIABLE_REFRIGERANT_FLOW_COLUMNS = (
    'Handle',
    'Name',
    'Availability Schedule Name',
    'Rated Total Heating Capacity {W}',
    'Rated Air Flow Rate {m3/s}',
    'Heating Capacity Ratio Modifier Function of Temperature Curve Name',
    'Heating Capacity Modifier Function of Flow Fraction Curve Name',
)

def get_coil_heating_dx_variable_refrigerant_flow_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: str | None = None, 
    name: str | None = None, 
    _object_ref: openstudio.model.CoilHeatingDXVariableRefrigerantFlow | None = None
) -> dict[str, Any]:
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
        'Name': opt(target_object.name()) if target_object.name().is_initialized() else "Unnamed Heating Coil DX VRF",
        'Availability Schedule Name': related_name(target_object, "Availability Schedule"),
        'Rated Total Heating Capacity {W}': opt(target_object.ratedTotalHeatingCapacity()) if target_object.ratedTotalHeatingCapacity().is_initialized() else 'autosize',
        'Rated Air Flow Rate {m3/s}': opt(target_object.ratedAirFlowRate()) if target_object.ratedAirFlowRate().is_initialized() else 'autosize',
        'Heating Capacity Ratio Modifier Function of Temperature Curve Name': related_name(target_object, "Heating Capacity Ratio Modifier Function of Temperature Curve"),
        'Heating Capacity Modifier Function of Flow Fraction Curve Name': related_name(target_object, "Heating Capacity Modifier Function of Flow Fraction Curve")
    }

def get_all_coil_heating_dx_variable_refrigerant_flow_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict[str, Any]]:
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
    return build_dataframe(
        all_objects_dicts, "Coil:Heating:DX:VRF", sort_by="Name",
        columns=COIL_HEATING_DX_VARIABLE_REFRIGERANT_FLOW_COLUMNS)

# --------------------------------------------------
#  ***** OS:Fan:ConstantVolume *********************
# --------------------------------------------------

FAN_CONSTANT_VOLUME_COLUMNS = (
    'Handle',
    'Name',
    'Availability Schedule Name',
    'Fan Total Efficiency',
    'Pressure Rise {Pa}',
    'Maximum Flow Rate {m3/s}',
    'Motor Efficiency',
    'Motor In Airstream Fraction',
    'Air Inlet Node Name',
    'Air Outlet Node Name',
    'End-Use Subcategory',
)

def get_fan_constant_volume_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: str | None = None, 
    name: str | None = None, 
    _object_ref: openstudio.model.FanConstantVolume | None = None
) -> dict[str, Any]:
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
        'Name': opt(target_object.name()) if target_object.name().is_initialized() else "Unnamed Fan CV",
        'Availability Schedule Name': opt(target_object.availabilitySchedule().name()) if target_object.availabilitySchedule().name().is_initialized() else None,
        'Fan Total Efficiency': target_object.fanTotalEfficiency(),
        'Pressure Rise {Pa}': target_object.pressureRise(),
        'Maximum Flow Rate {m3/s}': opt(target_object.maximumFlowRate()) if target_object.maximumFlowRate().is_initialized() else 'autosize',
        'Motor Efficiency': target_object.motorEfficiency(),
        'Motor In Airstream Fraction': target_object.motorInAirstreamFraction(),
        'Air Inlet Node Name': target_object.inletPort() if hasattr(target_object, 'inletPort') else None,
        'Air Outlet Node Name': target_object.outletPort() if hasattr(target_object, 'outletPort') else None,
        'End-Use Subcategory': target_object.endUseSubcategory()
    }

def get_all_fan_constant_volume_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict[str, Any]]:
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
    return build_dataframe(
        all_objects_dicts, "Fan:ConstantVolume", sort_by="Name",
        columns=FAN_CONSTANT_VOLUME_COLUMNS)

# --------------------------------------------------
#  ***** OS:Fan:OnOff ******************************
# --------------------------------------------------

FAN_ON_OFF_COLUMNS = (
    'Handle',
    'Name',
    'Availability Schedule Name',
    'Fan Total Efficiency',
    'Pressure Rise {Pa}',
    'Maximum Flow Rate {m3/s}',
    'Motor Efficiency',
    'Motor In Airstream Fraction',
    'Air Inlet Node Name',
    'Air Outlet Node Name',
    'Fan Power Ratio Function of Speed Ratio Curve Name',
    'Fan Efficiency Ratio Function of Speed Ratio Curve Name',
    'End-Use Subcategory',
)

def get_fan_on_off_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: str | None = None, 
    name: str | None = None, 
    _object_ref: openstudio.model.FanOnOff | None = None
) -> dict[str, Any]:
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
        'Name': opt(target_object.name()) if target_object.name().is_initialized() else "Unnamed Fan OnOff",
        'Availability Schedule Name': opt(target_object.availabilitySchedule().name()) if target_object.availabilitySchedule().name().is_initialized() else None,
        'Fan Total Efficiency': target_object.fanTotalEfficiency(),
        'Pressure Rise {Pa}': target_object.pressureRise(),
        'Maximum Flow Rate {m3/s}': opt(target_object.maximumFlowRate()) if target_object.maximumFlowRate().is_initialized() else 'autosize',
        'Motor Efficiency': target_object.motorEfficiency(),
        'Motor In Airstream Fraction': opt(target_object.motorInAirstreamFraction()),
        'Air Inlet Node Name': target_object.inletPort() if hasattr(target_object, 'inletPort') else None,
        'Air Outlet Node Name': target_object.outletPort() if hasattr(target_object, 'outletPort') else None,
        'Fan Power Ratio Function of Speed Ratio Curve Name': related_name(target_object, "Fan Power Ratio Function of Speed Ratio Curve Name"),
        'Fan Efficiency Ratio Function of Speed Ratio Curve Name': related_name(target_object, "Fan Efficiency Ratio Function of Speed Ratio Curve Name"),
        'End-Use Subcategory': target_object.endUseSubcategory()
    }

def get_all_fan_on_off_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict[str, Any]]:
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
    return build_dataframe(
        all_objects_dicts, "Fan:OnOff", sort_by="Name", columns=FAN_ON_OFF_COLUMNS)

# --------------------------------------------------
#  ***** OS:HeatExchanger:AirToAir:SensibleAndLatent
# --------------------------------------------------

HX_AIR_TO_AIR_SENSIBLE_AND_LATENT_COLUMNS = (
    'Handle',
    'Name',
    'Availability Schedule Name',
    'Nominal Supply Air Flow Rate {m3/s}',
    'Sensible Effectiveness at 100% Heating Air Flow {dimensionless}',
    'Latent Effectiveness at 100% Heating Air Flow {dimensionless}',
    'Sensible Effectiveness at 100% Cooling Air Flow {dimensionless}',
    'Latent Effectiveness at 100% Cooling Air Flow {dimensionless}',
    'Nominal Electric Power {W}',
    'Supply Air Outlet Temperature Control',
    'Heat Exchanger Type',
    'Frost Control Type',
    'Threshold Temperature {C}',
    'Initial Defrost Time Fraction {dimensionless}',
    'Rate of Defrost Time Fraction Increase {1/K}',
    'Economizer Lockout',
    'Sensible Effectiveness of Heating Air Flow Curve Name',
    'Latent Effectiveness of Heating Air Flow Curve Name',
    'Sensible Effectiveness of Cooling Air Flow Curve Name',
    'Latent Effectiveness of Cooling Air Flow Curve Name',
)

def get_hx_air_to_air_sensible_and_latent_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: str | None = None, 
    name: str | None = None, 
    _object_ref: openstudio.model.HeatExchangerAirToAirSensibleAndLatent | None = None
) -> dict[str, Any]:
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
        'Name': opt(target_object.name()) if target_object.name().is_initialized() else "Unnamed HX",      
        'Availability Schedule Name': related_name(target_object, "Availability Schedule"),
        'Nominal Supply Air Flow Rate {m3/s}': opt(target_object.nominalSupplyAirFlowRate()) if target_object.nominalSupplyAirFlowRate().is_initialized() else 'autosize',
        'Sensible Effectiveness at 100% Heating Air Flow {dimensionless}': target_object.sensibleEffectivenessat100HeatingAirFlow(),
        'Latent Effectiveness at 100% Heating Air Flow {dimensionless}': target_object.latentEffectivenessat100HeatingAirFlow(),
        'Sensible Effectiveness at 100% Cooling Air Flow {dimensionless}': target_object.sensibleEffectivenessat100CoolingAirFlow(),
        'Latent Effectiveness at 100% Cooling Air Flow {dimensionless}': target_object.latentEffectivenessat100CoolingAirFlow(),
        'Nominal Electric Power {W}': target_object.nominalElectricPower(),
        'Supply Air Outlet Temperature Control': target_object.supplyAirOutletTemperatureControl(),
        'Heat Exchanger Type': target_object.heatExchangerType(),
        'Frost Control Type': target_object.frostControlType(),
        'Threshold Temperature {C}': target_object.thresholdTemperature(),
        'Initial Defrost Time Fraction {dimensionless}': target_object.initialDefrostTimeFraction(),
        'Rate of Defrost Time Fraction Increase {1/K}': target_object.rateofDefrostTimeFractionIncrease(),
        'Economizer Lockout': target_object.economizerLockout(),
        'Sensible Effectiveness of Heating Air Flow Curve Name': optional_name(target_object.sensibleEffectivenessofHeatingAirFlowCurve()),
        'Latent Effectiveness of Heating Air Flow Curve Name': optional_name(target_object.latentEffectivenessofHeatingAirFlowCurve()),
        'Sensible Effectiveness of Cooling Air Flow Curve Name': optional_name(target_object.sensibleEffectivenessofCoolingAirFlowCurve()),
        'Latent Effectiveness of Cooling Air Flow Curve Name': optional_name(target_object.latentEffectivenessofCoolingAirFlowCurve())
    }

def get_all_hx_air_to_air_sensible_and_latent_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict[str, Any]]:
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
    return build_dataframe(
        all_objects_dicts, "HeatExchanger:AirToAir:SensibleAndLatent", sort_by="Name",
        columns=HX_AIR_TO_AIR_SENSIBLE_AND_LATENT_COLUMNS)

# --------------------------------------------------
#  ***** OS:AirConditioner:VariableRefrigerantFlow
# --------------------------------------------------

AIR_CONDITIONER_VARIABLE_REFRIGERANT_FLOW_COLUMNS = (
    'Handle',
    'Name',
    'Availability Schedule Name',
    'Gross Rated Total Cooling Capacity {W}',
    'Gross Rated Cooling COP {W/W}',
    'Minimum Outdoor Temperature in Cooling Mode {C}',
    'Maximum Outdoor Temperature in Cooling Mode {C}',
    'Cooling Capacity Ratio Modifier Function of Low Temperature Curve Name',
    'Cooling Capacity Ratio Boundary Curve Name',
    'Cooling Capacity Ratio Modifier Function of High Temperature Curve Name',
    'Cooling Energy Input Ratio Modifier Function of Low Temperature Curve Name',
    'Cooling Energy Input Ratio Boundary Curve Name',
    'Cooling Energy Input Ratio Modifier Function of High Temperature Curve Name',
    'Cooling Energy Input Ratio Modifier Function of Low Part-Load Ratio Curve Name',
    'Cooling Energy Input Ratio Modifier Function of High Part-Load Ratio Curve Name',
    'Cooling Combination Ratio Correction Factor Curve Name',
    'Cooling Part-Load Fraction Correlation Curve Name',
    'Gross Rated Heating Capacity {W}',
    'Rated Heating Capacity Sizing Ratio {W/W}',
    'Rated Heating COP {W/W}',
    'Minimum Outdoor Temperature in Heating Mode {C}',
    'Maximum Outdoor Temperature in Heating Mode {C}',
    'Heating Capacity Ratio Modifier Function of Low Temperature Curve Name',
    'Heating Capacity Ratio Boundary Curve Name',
    'Heating Capacity Ratio Modifier Function of High Temperature Curve Name',
    'Heating Energy Input Ratio Modifier Function of Low Temperature Curve Name',
    'Heating Energy Input Ratio Boundary Curve Name',
    'Heating Energy Input Ratio Modifier Function of High Temperature Curve Name',
    'Heating Performance Curve Outdoor Temperature Type',
    'Heating Energy Input Ratio Modifier Function of Low Part-Load Ratio Curve Name',
    'Heating Energy Input Ratio Modifier Function of High Part-Load Ratio Curve Name',
    'Heating Combination Ratio Correction Factor Curve Name',
    'Heating Part-Load Fraction Correlation Curve Name',
    'Minimum Heat Pump Part-Load Ratio {dimensionless}',
    'Zone Name for Master Thermostat Location',
    'Master Thermostat Priority Control Type',
    'Thermostat Priority Schedule Name',
    'Heat Pump Waste Heat Recovery',
    'Equivalent Piping Length used for Piping Correction Factor in Cooling Mode {m}',
    'Vertical Height used for Piping Correction Factor {m}',
    'Piping Correction Factor for Length in Cooling Mode Curve Name',
    'Piping Correction Factor for Height in Cooling Mode Coefficient {1/m}',
    'Equivalent Piping Length used for Piping Correction Factor in Heating Mode {m}',
    'Piping Correction Factor for Length in Heating Mode Curve Name',
    'Piping Correction Factor for Height in Heating Mode Coefficient {1/m}',
    'Crankcase Heater Power per Compressor {W}',
    'Number of Compressors {dimensionless}',
    'Ratio of Compressor Size to Total Compressor Capacity {W/W}',
    'Maximum Outdoor Dry-bulb Temperature for Crankcase Heater {C}',
    'Defrost Strategy',
    'Defrost Control',
    'Defrost Energy Input Ratio Modifier Function of Temperature Curve Name',
    'Defrost Time Period Fraction {dimensionless}',
    'Resistive Defrost Heater Capacity {W}',
    'Maximum Outdoor Dry-bulb Temperature for Defrost Operation {C}',
    'Condenser Type',
    'Water Condenser Volume Flow Rate {m3/s}',
    'Evaporative Condenser Effectiveness {dimensionless}',
    'Evaporative Condenser Air Flow Rate {m3/s}',
    'Evaporative Condenser Pump Rated Power Consumption {W}',
    'Basin Heater Capacity {W/K}',
    'Basin Heater Setpoint Temperature {C}',
    'Basin Heater Operating Schedule Name',
    'Fuel Type',
    'Minimum Outdoor Temperature in Heat Recovery Mode {C}',
    'Maximum Outdoor Temperature in Heat Recovery Mode {C}',
    'Heat Recovery Cooling Capacity Modifier Curve Name',
    'Initial Heat Recovery Cooling Capacity Fraction {W/W}',
    'Heat Recovery Cooling Capacity Time Constant {hr}',
    'Heat Recovery Cooling Energy Modifier Curve Name',
    'Initial Heat Recovery Cooling Energy Fraction {W/W}',
    'Heat Recovery Cooling Energy Time Constant {hr}',
    'Heat Recovery Heating Capacity Modifier Curve Name',
    'Initial Heat Recovery Heating Capacity Fraction {W/W}',
    'Heat Recovery Heating Capacity Time Constant {hr}',
    'Heat Recovery Heating Energy Modifier Curve Name',
    'Initial Heat Recovery Heating Energy Fraction {W/W}',
    'Heat Recovery Heating Energy Time Constant {hr}',
)

def get_air_conditioner_variable_refrigerant_flow_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: str | None = None, 
    name: str | None = None, 
    _object_ref: openstudio.model.AirConditionerVariableRefrigerantFlow | None = None
) -> dict[str, Any]:
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
        'Name': opt(target_object.name()) if target_object.name().is_initialized() else "Unnamed VRF AC",
        'Availability Schedule Name': related_name(target_object, "Availability Schedule"),
        'Gross Rated Total Cooling Capacity {W}': target_object.grossRatedTotalCoolingCapacity(),
        'Gross Rated Cooling COP {W/W}': target_object.grossRatedCoolingCOP(),
        'Minimum Outdoor Temperature in Cooling Mode {C}': target_object.minimumOutdoorTemperatureinCoolingMode(),
        'Maximum Outdoor Temperature in Cooling Mode {C}': target_object.maximumOutdoorTemperatureinCoolingMode(),
        'Cooling Capacity Ratio Modifier Function of Low Temperature Curve Name': optional_name(target_object.coolingCapacityRatioModifierFunctionofLowTemperatureCurve()),
        'Cooling Capacity Ratio Boundary Curve Name': optional_name(target_object.coolingCapacityRatioBoundaryCurve()),
        'Cooling Capacity Ratio Modifier Function of High Temperature Curve Name': optional_name(target_object.coolingCapacityRatioModifierFunctionofHighTemperatureCurve()),
        'Cooling Energy Input Ratio Modifier Function of Low Temperature Curve Name': optional_name(target_object.coolingEnergyInputRatioModifierFunctionofLowTemperatureCurve()),
        'Cooling Energy Input Ratio Boundary Curve Name': optional_name(target_object.coolingEnergyInputRatioBoundaryCurve()),
        'Cooling Energy Input Ratio Modifier Function of High Temperature Curve Name': optional_name(target_object.coolingEnergyInputRatioModifierFunctionofHighTemperatureCurve()),
        'Cooling Energy Input Ratio Modifier Function of Low Part-Load Ratio Curve Name': optional_name(target_object.coolingEnergyInputRatioModifierFunctionofLowPartLoadRatioCurve()),
        'Cooling Energy Input Ratio Modifier Function of High Part-Load Ratio Curve Name': optional_name(target_object.coolingEnergyInputRatioModifierFunctionofHighPartLoadRatioCurve()),
        'Cooling Combination Ratio Correction Factor Curve Name': optional_name(target_object.coolingCombinationRatioCorrectionFactorCurve()),
        'Cooling Part-Load Fraction Correlation Curve Name': optional_name(target_object.coolingPartLoadFractionCorrelationCurve()),
        'Gross Rated Heating Capacity {W}': target_object.grossRatedHeatingCapacity(),
        'Rated Heating Capacity Sizing Ratio {W/W}': target_object.ratedHeatingCapacitySizingRatio(),
        'Rated Heating COP {W/W}': target_object.ratedHeatingCOP(),
        'Minimum Outdoor Temperature in Heating Mode {C}': target_object.minimumOutdoorTemperatureinHeatingMode(),
        'Maximum Outdoor Temperature in Heating Mode {C}': target_object.maximumOutdoorTemperatureinHeatingMode(),
        'Heating Capacity Ratio Modifier Function of Low Temperature Curve Name': optional_name(target_object.heatingCapacityRatioModifierFunctionofLowTemperatureCurve()),
        'Heating Capacity Ratio Boundary Curve Name': optional_name(target_object.heatingCapacityRatioBoundaryCurve()),
        'Heating Capacity Ratio Modifier Function of High Temperature Curve Name': optional_name(target_object.heatingCapacityRatioModifierFunctionofHighTemperatureCurve()),
        'Heating Energy Input Ratio Modifier Function of Low Temperature Curve Name': optional_name(target_object.heatingEnergyInputRatioModifierFunctionofLowTemperatureCurve()),
        'Heating Energy Input Ratio Boundary Curve Name': optional_name(target_object.heatingEnergyInputRatioBoundaryCurve()),
        'Heating Energy Input Ratio Modifier Function of High Temperature Curve Name': optional_name(target_object.heatingEnergyInputRatioModifierFunctionofHighTemperatureCurve()),
        'Heating Performance Curve Outdoor Temperature Type': target_object.heatingPerformanceCurveOutdoorTemperatureType(),
        'Heating Energy Input Ratio Modifier Function of Low Part-Load Ratio Curve Name': optional_name(target_object.heatingEnergyInputRatioModifierFunctionofLowPartLoadRatioCurve()),
        'Heating Energy Input Ratio Modifier Function of High Part-Load Ratio Curve Name': optional_name(target_object.heatingEnergyInputRatioModifierFunctionofHighPartLoadRatioCurve()),
        'Heating Combination Ratio Correction Factor Curve Name': optional_name(target_object.heatingCombinationRatioCorrectionFactorCurve()),
        'Heating Part-Load Fraction Correlation Curve Name': optional_name(target_object.heatingPartLoadFractionCorrelationCurve()),
        'Minimum Heat Pump Part-Load Ratio {dimensionless}': target_object.minimumHeatPumpPartLoadRatio(),
        'Zone Name for Master Thermostat Location': optional_name(target_object.zoneforMasterThermostatLocation()),
        'Master Thermostat Priority Control Type': target_object.masterThermostatPriorityControlType(),
        'Thermostat Priority Schedule Name': optional_name(target_object.thermostatPrioritySchedule()),
        'Heat Pump Waste Heat Recovery': target_object.heatPumpWasteHeatRecovery(),
        'Equivalent Piping Length used for Piping Correction Factor in Cooling Mode {m}': target_object.equivalentPipingLengthusedforPipingCorrectionFactorinCoolingMode(),
        'Vertical Height used for Piping Correction Factor {m}': target_object.verticalHeightusedforPipingCorrectionFactor(),
        'Piping Correction Factor for Length in Cooling Mode Curve Name': optional_name(target_object.pipingCorrectionFactorforLengthinCoolingModeCurve()),
        'Piping Correction Factor for Height in Cooling Mode Coefficient {1/m}': target_object.pipingCorrectionFactorforHeightinCoolingModeCoefficient(),
        'Equivalent Piping Length used for Piping Correction Factor in Heating Mode {m}': target_object.equivalentPipingLengthusedforPipingCorrectionFactorinHeatingMode(),
        'Piping Correction Factor for Length in Heating Mode Curve Name': optional_name(target_object.pipingCorrectionFactorforLengthinHeatingModeCurve()),
        'Piping Correction Factor for Height in Heating Mode Coefficient {1/m}': target_object.pipingCorrectionFactorforHeightinHeatingModeCoefficient(),
        'Crankcase Heater Power per Compressor {W}': target_object.crankcaseHeaterPowerperCompressor(),
        'Number of Compressors {dimensionless}': target_object.numberofCompressors(),
        'Ratio of Compressor Size to Total Compressor Capacity {W/W}': target_object.ratioofCompressorSizetoTotalCompressorCapacity(),
        'Maximum Outdoor Dry-bulb Temperature for Crankcase Heater {C}': target_object.maximumOutdoorDrybulbTemperatureforCrankcaseHeater(),
        'Defrost Strategy': target_object.defrostStrategy(),
        'Defrost Control': target_object.defrostControl(),
        'Defrost Energy Input Ratio Modifier Function of Temperature Curve Name': optional_name(target_object.defrostEnergyInputRatioModifierFunctionofTemperatureCurve()),
        'Defrost Time Period Fraction {dimensionless}': target_object.defrostTimePeriodFraction(),
        'Resistive Defrost Heater Capacity {W}': target_object.resistiveDefrostHeaterCapacity(),
        'Maximum Outdoor Dry-bulb Temperature for Defrost Operation {C}': target_object.maximumOutdoorDrybulbTemperatureforDefrostOperation(),
        'Condenser Type': target_object.condenserType(),
        'Water Condenser Volume Flow Rate {m3/s}': target_object.waterCondenserVolumeFlowRate(),
        'Evaporative Condenser Effectiveness {dimensionless}': target_object.evaporativeCondenserEffectiveness(),
        'Evaporative Condenser Air Flow Rate {m3/s}': target_object.evaporativeCondenserAirFlowRate(),
        'Evaporative Condenser Pump Rated Power Consumption {W}': target_object.evaporativeCondenserPumpRatedPowerConsumption(),
        'Basin Heater Capacity {W/K}': target_object.basinHeaterCapacity(),
        'Basin Heater Setpoint Temperature {C}': target_object.basinHeaterSetpointTemperature(),
        'Basin Heater Operating Schedule Name': optional_name(target_object.basinHeaterOperatingSchedule()),
        'Fuel Type': target_object.fuelType(),
        'Minimum Outdoor Temperature in Heat Recovery Mode {C}': target_object.minimumOutdoorTemperatureinHeatRecoveryMode(),
        'Maximum Outdoor Temperature in Heat Recovery Mode {C}': target_object.maximumOutdoorTemperatureinHeatRecoveryMode(),
        'Heat Recovery Cooling Capacity Modifier Curve Name': optional_name(target_object.heatRecoveryCoolingCapacityModifierCurve()),
        'Initial Heat Recovery Cooling Capacity Fraction {W/W}': target_object.initialHeatRecoveryCoolingCapacityFraction(),
        'Heat Recovery Cooling Capacity Time Constant {hr}': target_object.heatRecoveryCoolingCapacityTimeConstant(),
        'Heat Recovery Cooling Energy Modifier Curve Name': optional_name(target_object.heatRecoveryCoolingEnergyModifierCurve()),
        'Initial Heat Recovery Cooling Energy Fraction {W/W}': target_object.initialHeatRecoveryCoolingEnergyFraction(),
        'Heat Recovery Cooling Energy Time Constant {hr}': target_object.heatRecoveryCoolingEnergyTimeConstant(),
        'Heat Recovery Heating Capacity Modifier Curve Name': optional_name(target_object.heatRecoveryHeatingCapacityModifierCurve()),
        'Initial Heat Recovery Heating Capacity Fraction {W/W}': target_object.initialHeatRecoveryHeatingCapacityFraction(),
        'Heat Recovery Heating Capacity Time Constant {hr}': target_object.heatRecoveryHeatingCapacityTimeConstant(),
        'Heat Recovery Heating Energy Modifier Curve Name': optional_name(target_object.heatRecoveryHeatingEnergyModifierCurve()),
        'Initial Heat Recovery Heating Energy Fraction {W/W}': target_object.initialHeatRecoveryHeatingEnergyFraction(),
        'Heat Recovery Heating Energy Time Constant {hr}': target_object.heatRecoveryHeatingEnergyTimeConstant()
    }

def get_all_air_conditioner_variable_refrigerant_flow_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict[str, Any]]:
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
    return build_dataframe(
        all_objects_dicts, "AirConditioner:VariableRefrigerantFlow", sort_by="Name",
        columns=AIR_CONDITIONER_VARIABLE_REFRIGERANT_FLOW_COLUMNS)

#-----------------------
#--- OS:Coil:Heating:Gas
#------------------------

# --------------------------------------------------
#  ***** OS:Coil:Heating:Gas ***********************
# --------------------------------------------------

COIL_HEATING_GAS_COLUMNS = (
    'Handle',
    'Name',
    'Availability Schedule Name',
    'Gas Burner Efficiency',
    'Nominal Capacity {W}',
    'On Cycle Parasitic Electric Load {W}',
    'Part Load Fraction Correlation Curve Name',
    'Off Cycle Parasitic Gas Load {W}',
)

def get_coil_heating_gas_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: str | None = None, 
    name: str | None = None, 
    _object_ref: openstudio.model.CoilHeatingGas | None = None
) -> dict[str, Any]:
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
        'Name': opt(target_object.name()) if target_object.name().is_initialized() else "Unnamed Heating Coil Gas",
        'Availability Schedule Name': opt(target_object.availabilitySchedule().name()) if target_object.availabilitySchedule().name().is_initialized() else None,
        'Gas Burner Efficiency': target_object.gasBurnerEfficiency(),
        'Nominal Capacity {W}': opt(target_object.nominalCapacity()) if target_object.nominalCapacity().is_initialized() else 'autosize',
        'On Cycle Parasitic Electric Load {W}': target_object.onCycleParasiticElectricLoad(),
        'Part Load Fraction Correlation Curve Name': optional_name(target_object.partLoadFractionCorrelationCurve()),
        'Off Cycle Parasitic Gas Load {W}': target_object.offCycleParasiticGasLoad()                           
    }

def get_all_coil_heating_gas_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict[str, Any]]:
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
    return build_dataframe(
        all_objects_dicts, "Coil:Heating:Gas", sort_by="Name", columns=COIL_HEATING_GAS_COLUMNS)

#---------------------------
#--- OOS:Coil:Heating:Water
#---------------------------
# --------------------------------------------------
#  ***** OS:Coil:Heating:Water *********************
# --------------------------------------------------

COIL_HEATING_WATER_COLUMNS = (
    'Handle',
    'Name',
    'Availability Schedule Name',
    'U-Factor Times Area Value {W/K}',
    'Maximum Water Flow Rate {m3/s}',
    'Performance Input Method',
    'Rated Capacity {W}',
    'Rated Inlet Water Temperature {C}',
    'Rated Inlet Air Temperature {C}',
    'Rated Outlet Water Temperature {C}',
    'Rated Outlet Air Temperature {C}',
    'Rated Ratio for Air and Water Convection',
)

def get_coil_heating_water_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: str | None = None, 
    name: str | None = None, 
    _object_ref: openstudio.model.CoilHeatingWater | None = None
) -> dict[str, Any]:
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
        'Name': opt(target_object.name()) if target_object.name().is_initialized() else "Unnamed Heating Coil Water",
        'Availability Schedule Name': opt(target_object.availabilitySchedule().name()) if target_object.availabilitySchedule().name().is_initialized() else None,
        'U-Factor Times Area Value {W/K}': opt(target_object.uFactorTimesAreaValue()) if target_object.uFactorTimesAreaValue().is_initialized() else 'autosize',
        'Maximum Water Flow Rate {m3/s}': opt(target_object.maximumWaterFlowRate()) if target_object.maximumWaterFlowRate().is_initialized() else 'autosize',
        'Performance Input Method': target_object.performanceInputMethod(),
        'Rated Capacity {W}': opt(target_object.ratedCapacity()) if target_object.ratedCapacity().is_initialized() else 'autosize',
        'Rated Inlet Water Temperature {C}': target_object.ratedInletWaterTemperature(),
        'Rated Inlet Air Temperature {C}': target_object.ratedInletAirTemperature(),
        'Rated Outlet Water Temperature {C}': target_object.ratedOutletWaterTemperature(),
        'Rated Outlet Air Temperature {C}': target_object.ratedOutletAirTemperature(),
        'Rated Ratio for Air and Water Convection': target_object.ratedRatioForAirAndWaterConvection()
    }

def get_all_coil_heating_water_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict[str, Any]]:
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
    return build_dataframe(
        all_objects_dicts, "Coil:Heating:Water", sort_by="Name", columns=COIL_HEATING_WATER_COLUMNS)

#---------------------------
#--- OOS:Coil:Cooling:Water
#---------------------------

# --------------------------------------------------
#  ***** OS:Coil:Cooling:Water *********************
# --------------------------------------------------

COIL_COOLING_WATER_COLUMNS = (
    'Handle',
    'Name',
    'Availability Schedule Name',
    'Design Water Flow Rate {m3/s}',
    'Design Air Flow Rate {m3/s}',
    'Design Inlet Water Temperature {C}',
    'Design Inlet Air Temperature {C}',
    'Design Outlet Air Temperature {C}',
    'Design Inlet Air Humidity Ratio {kg-H2O/kg-air}',
    'Design Outlet Air Humidity Ratio {kg-H2O/kg-air}',
    'Heat Exchanger Configuration',
)

def get_coil_cooling_water_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: str | None = None, 
    name: str | None = None, 
    _object_ref: openstudio.model.CoilCoolingWater | None = None
) -> dict[str, Any]:
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
        'Name': opt(target_object.name()) if target_object.name().is_initialized() else "Unnamed Cooling Coil Water",
        'Availability Schedule Name': opt(target_object.availabilitySchedule().name()) if target_object.availabilitySchedule().name().is_initialized() else None,
        'Design Water Flow Rate {m3/s}': opt(target_object.designWaterFlowRate()) if target_object.designWaterFlowRate().is_initialized() else 'autosize',
        'Design Air Flow Rate {m3/s}': opt(target_object.designAirFlowRate()) if target_object.designAirFlowRate().is_initialized() else 'autosize',
        'Design Inlet Water Temperature {C}': opt(target_object.designInletWaterTemperature()) if target_object.designInletWaterTemperature().is_initialized() else 'autosize',
        'Design Inlet Air Temperature {C}': opt(target_object.designInletAirTemperature()) if target_object.designInletAirTemperature().is_initialized() else 'autosize',        
        'Design Outlet Air Temperature {C}': opt(target_object.designOutletAirTemperature()) if target_object.designOutletAirTemperature().is_initialized() else 'autosize',
        'Design Inlet Air Humidity Ratio {kg-H2O/kg-air}': opt(target_object.designInletAirHumidityRatio()) if target_object.designInletAirHumidityRatio().is_initialized() else 'autosize',
        'Design Outlet Air Humidity Ratio {kg-H2O/kg-air}': opt(target_object.designOutletAirHumidityRatio()) if target_object.designOutletAirHumidityRatio().is_initialized() else 'autosize',
        'Heat Exchanger Configuration': target_object.heatExchangerConfiguration()        
    }

def get_all_coil_cooling_water_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict[str, Any]]:
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
    return build_dataframe(
        all_objects_dicts, "Coil:Cooling:Water", sort_by="Name", columns=COIL_COOLING_WATER_COLUMNS)


# --------------------------------------------------
#  ***** OS:Pump:VariableSpeed *********************
# --------------------------------------------------


# --------------------------------------------------
#  ***** OS:Pump:VariableSpeed *********************
# --------------------------------------------------

PUMP_VARIABLE_SPEED_COLUMNS = (
    'Handle',
    'Name',
    'Inlet Node Name',
    'Outlet Node Name',
    'Rated Flow Rate {m3/s}',
    'Rated Pump Head {Pa}',
    'Rated Power Consumption {W}',
    'Motor Efficiency',
    'Fraction of Motor Inefficiencies to Fluid Stream',
    'Coefficient 1 of the Part Load Performance Curve',
    'Coefficient 2 of the Part Load Performance Curve',
    'Coefficient 3 of the Part Load Performance Curve',
    'Coefficient 4 of the Part Load Performance Curve',
    'Minimum Flow Rate {m3/s}',
    'Pump Control Type',
    'Pump Flow Rate Schedule Name',
    'Skin Loss Radiative Fraction',
    'Design Power Sizing Method',
    'Design Electric Power per Unit Flow Rate {W/(m3/s)}',
    'Design Shaft Power per Unit Flow Rate per Unit Head {W-s/m3-Pa}',
    'Design Minimum Flow Rate Fraction',
    'End-Use Subcategory',
)

def get_pump_variable_speed_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: str | None = None, 
    name: str | None = None, 
    _object_ref: openstudio.model.PumpVariableSpeed | None = None
) -> dict[str, Any]:
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
        'Name': opt(target_object.name()) if target_object.name().is_initialized() else "Unnamed Pump VS", 
        'Inlet Node Name': target_object.inletPort() if hasattr(target_object, 'inletPort') else None, 
        'Outlet Node Name': target_object.outletPort() if hasattr(target_object, 'outletPort') else None, 
        'Rated Flow Rate {m3/s}': opt(target_object.ratedFlowRate()) if target_object.ratedFlowRate().is_initialized() else 'autosize', 
        'Rated Pump Head {Pa}': target_object.ratedPumpHead(), 
        'Rated Power Consumption {W}': opt(target_object.ratedPowerConsumption()) if target_object.ratedPowerConsumption().is_initialized() else 'autosize',
        'Motor Efficiency': target_object.motorEfficiency(), 
        'Fraction of Motor Inefficiencies to Fluid Stream': target_object.fractionofMotorInefficienciestoFluidStream(), 
        'Coefficient 1 of the Part Load Performance Curve': target_object.coefficient1ofthePartLoadPerformanceCurve(), 
        'Coefficient 2 of the Part Load Performance Curve': target_object.coefficient2ofthePartLoadPerformanceCurve(), 
        'Coefficient 3 of the Part Load Performance Curve': target_object.coefficient3ofthePartLoadPerformanceCurve(), 
        'Coefficient 4 of the Part Load Performance Curve': target_object.coefficient4ofthePartLoadPerformanceCurve(), 
        'Minimum Flow Rate {m3/s}': target_object.minimumFlowRate(), 
        'Pump Control Type': target_object.pumpControlType(), 
        'Pump Flow Rate Schedule Name': optional_name(target_object.pumpFlowRateSchedule()), 
        'Skin Loss Radiative Fraction': target_object.skinLossRadiativeFraction(), 
        'Design Power Sizing Method': target_object.designPowerSizingMethod(), 
        'Design Electric Power per Unit Flow Rate {W/(m3/s)}': target_object.designElectricPowerPerUnitFlowRate(), 
        'Design Shaft Power per Unit Flow Rate per Unit Head {W-s/m3-Pa}': target_object.designShaftPowerPerUnitFlowRatePerUnitHead(), 
        'Design Minimum Flow Rate Fraction': target_object.designMinimumFlowRateFraction(), 
        'End-Use Subcategory': target_object.endUseSubcategory()
    }

def get_all_pump_variable_speed_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict[str, Any]]:
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
    return build_dataframe(
        all_objects_dicts, "Pump:VariableSpeed", sort_by="Name", columns=PUMP_VARIABLE_SPEED_COLUMNS)


# --------------------------------------------------
#  ***** OS:Chiller:Electric:EIR *******************
# --------------------------------------------------


# --------------------------------------------------
#  ***** OS:Chiller:Electric:EIR *******************
# --------------------------------------------------

CHILLER_ELECTRIC_EIR_COLUMNS = (
    'Handle',
    'Name',
    'Reference Capacity {W}',
    'Reference COP {W/W}',
    'Reference Leaving Chilled Water Temperature {C}',
    'Reference Entering Condenser Fluid Temperature {C}',
    'Reference Chilled Water Flow Rate {m3/s}',
    'Reference Condenser Fluid Flow Rate {m3/s}',
    'Cooling Capacity Function of Temperature Curve Name',
    'Electric Input to Cooling Output Ratio Function of Temperature Curve Name',
    'Electric Input to Cooling Output Ratio Function of Part Load Ratio Curve Name',
    'Minimum Part Load Ratio',
    'Maximum Part Load Ratio',
    'Optimum Part Load Ratio',
    'Minimum Unloading Ratio',
    'Condenser Type',
    'Condenser Fan Power Ratio {W/W}',
    'Leaving Chilled Water Lower Temperature Limit {C}',
    'Chiller Flow Mode',
    'Design Heat Recovery Water Flow Rate {m3/s}',
    'Heat Recovery Inlet Node Name',
    'Heat Recovery Outlet Node Name',
    'Sizing Factor',
    'Basin Heater Capacity {W/K}',
    'Basin Heater Setpoint Temperature {C}',
    'Basin Heater Operating Schedule Name',
    'Condenser Heat Recovery Relative Capacity Fraction',
    'Heat Recovery Leaving Temperature Setpoint Node Name',
    'End-Use Subcategory',
)

def get_chiller_electric_eir_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: str | None = None, 
    name: str | None = None, 
    _object_ref: openstudio.model.ChillerElectricEIR | None = None
) -> dict[str, Any]:
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
        'Name': opt(target_object.name()) if target_object.name().is_initialized() else "Unnamed Chiller", 
        'Reference Capacity {W}': opt(target_object.referenceCapacity()) if target_object.referenceCapacity().is_initialized() else 'autosize', 
        'Reference COP {W/W}': target_object.referenceCOP(), 
        'Reference Leaving Chilled Water Temperature {C}': target_object.referenceLeavingChilledWaterTemperature(), 
        'Reference Entering Condenser Fluid Temperature {C}': target_object.referenceEnteringCondenserFluidTemperature(), 
        'Reference Chilled Water Flow Rate {m3/s}': opt(target_object.referenceChilledWaterFlowRate()) if target_object.referenceChilledWaterFlowRate().is_initialized() else 'autosize', 
        'Reference Condenser Fluid Flow Rate {m3/s}': opt(target_object.referenceCondenserFluidFlowRate()) if target_object.referenceCondenserFluidFlowRate().is_initialized() else 'autosize', 
        'Cooling Capacity Function of Temperature Curve Name': related_name(target_object, "Cooling Capacity Function of Temperature Curve Name"), 
        'Electric Input to Cooling Output Ratio Function of Temperature Curve Name': related_name(target_object, "Electric Input to Cooling Output Ratio Function of Temperature Curve Name"),  
        'Electric Input to Cooling Output Ratio Function of Part Load Ratio Curve Name': related_name(target_object, "Electric Input to Cooling Output Ratio Function of Part Load Ratio Curve Name"), 
        'Minimum Part Load Ratio': target_object.minimumPartLoadRatio(), 
        'Maximum Part Load Ratio': target_object.maximumPartLoadRatio(), 
        'Optimum Part Load Ratio': target_object.optimumPartLoadRatio(), 
        'Minimum Unloading Ratio': target_object.minimumUnloadingRatio(), 
        'Condenser Type': target_object.condenserType(), 
        'Condenser Fan Power Ratio {W/W}': target_object.condenserFanPowerRatio(), 
        'Leaving Chilled Water Lower Temperature Limit {C}': target_object.leavingChilledWaterLowerTemperatureLimit(), 
        'Chiller Flow Mode': target_object.chillerFlowMode(), 
        'Design Heat Recovery Water Flow Rate {m3/s}': opt(target_object.designHeatRecoveryWaterFlowRate()) if target_object.designHeatRecoveryWaterFlowRate().is_initialized() else 'autosize', 
        'Heat Recovery Inlet Node Name': optional_name(target_object.heatRecoveryInletNode()), 
        'Heat Recovery Outlet Node Name': optional_name(target_object.heatRecoveryOutletNode()), 
        'Sizing Factor': target_object.sizingFactor(), 
        'Basin Heater Capacity {W/K}': target_object.basinHeaterCapacity(), 
        'Basin Heater Setpoint Temperature {C}': target_object.basinHeaterSetpointTemperature(), 
        'Basin Heater Operating Schedule Name': optional_name(target_object.basinHeaterSchedule()), 
        'Condenser Heat Recovery Relative Capacity Fraction': target_object.condenserHeatRecoveryRelativeCapacityFraction(), 
        'Heat Recovery Leaving Temperature Setpoint Node Name': optional_name(target_object.heatRecoveryLeavingTemperatureSetpointNode()), 
        'End-Use Subcategory': target_object.endUseSubcategory()
    }

def get_all_chiller_electric_eir_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict[str, Any]]:
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
    return build_dataframe(
        all_objects_dicts, "Chiller:Electric:EIR", sort_by="Name", columns=CHILLER_ELECTRIC_EIR_COLUMNS)