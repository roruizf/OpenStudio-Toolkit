import logging
from typing import Any

import openstudio
import pandas as pd

from openstudio_toolkit._sdk import connection_node_name, opt, optional_name, related, related_name
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
        'Rated Total Cooling Capacity {W}': opt(target_object.ratedTotalCoolingCapacity()) if target_object.ratedTotalCoolingCapacity().is_initialized() else 'Autosize',
        'Rated Sensible Heat Ratio': opt(target_object.ratedSensibleHeatRatio()) if target_object.ratedSensibleHeatRatio().is_initialized() else 'Autosize',
        'Rated Air Flow Rate {m3/s}': opt(target_object.ratedAirFlowRate()) if target_object.ratedAirFlowRate().is_initialized() else 'Autosize',
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
        'Rated Total Heating Capacity {W}': opt(target_object.ratedTotalHeatingCapacity()) if target_object.ratedTotalHeatingCapacity().is_initialized() else 'Autosize',
        'Rated Air Flow Rate {m3/s}': opt(target_object.ratedAirFlowRate()) if target_object.ratedAirFlowRate().is_initialized() else 'Autosize',
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
        'Maximum Flow Rate {m3/s}': opt(target_object.maximumFlowRate()) if target_object.maximumFlowRate().is_initialized() else 'Autosize',
        'Motor Efficiency': target_object.motorEfficiency(),
        'Motor In Airstream Fraction': target_object.motorInAirstreamFraction(),
        'Air Inlet Node Name': connection_node_name(target_object, "Air Inlet Node Name"),
        'Air Outlet Node Name': connection_node_name(target_object, "Air Outlet Node Name"),
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
        'Maximum Flow Rate {m3/s}': opt(target_object.maximumFlowRate()) if target_object.maximumFlowRate().is_initialized() else 'Autosize',
        'Motor Efficiency': target_object.motorEfficiency(),
        'Motor In Airstream Fraction': opt(target_object.motorInAirstreamFraction()),
        'Air Inlet Node Name': connection_node_name(target_object, "Air Inlet Node Name"),
        'Air Outlet Node Name': connection_node_name(target_object, "Air Outlet Node Name"),
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
        'Nominal Supply Air Flow Rate {m3/s}': opt(target_object.nominalSupplyAirFlowRate()) if target_object.nominalSupplyAirFlowRate().is_initialized() else 'Autosize',
        'Sensible Effectiveness at 100% Heating Air Flow {dimensionless}': target_object.sensibleEffectivenessat100HeatingAirFlow(),
        'Latent Effectiveness at 100% Heating Air Flow {dimensionless}': target_object.latentEffectivenessat100HeatingAirFlow(),
        'Sensible Effectiveness at 100% Cooling Air Flow {dimensionless}': target_object.sensibleEffectivenessat100CoolingAirFlow(),
        'Latent Effectiveness at 100% Cooling Air Flow {dimensionless}': target_object.latentEffectivenessat100CoolingAirFlow(),
        'Nominal Electric Power {W}': target_object.nominalElectricPower(),
        'Supply Air Outlet Temperature Control': target_object.supplyAirOutletTemperatureControl(),
        'Heat Exchanger Type': target_object.heatExchangerType(),
        'Frost Control Type': target_object.frostControlType(),
        'Threshold Temperature {C}': target_object.thresholdTemperature(),
        'Initial Defrost Time Fraction {dimensionless}': opt(target_object.initialDefrostTimeFraction()),
        'Rate of Defrost Time Fraction Increase {1/K}': opt(target_object.rateofDefrostTimeFractionIncrease()),
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

def _vrf_condenser_type(vrf: Any) -> str:
    """Condenser Type as OpenStudio resolves it, without ``condenserType()``.

    When the field is empty, ``condenserType()`` derives the default from ``plantLoop()``, which walks
    every plant loop and segfaults when a loop has orphan relations (seen on the blanked
    ``extra_families.osm``). Same rule through the field: stored value, else ``WaterCooled`` when the
    condenser inlet port is connected to a plant, else ``AirCooled``.
    """
    stored = opt(vrf.getString(opt(vrf.iddObject().getFieldIndex("Condenser Type"))))
    if stored:
        return str(stored)
    return "WaterCooled" if related(vrf, "Condenser Inlet Node") is not None else "AirCooled"


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
        'Gross Rated Total Cooling Capacity {W}': 'Autosize' if target_object.isGrossRatedTotalCoolingCapacityAutosized() else opt(target_object.grossRatedTotalCoolingCapacity()),
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
        'Gross Rated Heating Capacity {W}': 'Autosize' if target_object.isGrossRatedHeatingCapacityAutosized() else opt(target_object.grossRatedHeatingCapacity()),
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
        'Resistive Defrost Heater Capacity {W}': 'Autosize' if target_object.isResistiveDefrostHeaterCapacityAutosized() else opt(target_object.resistiveDefrostHeaterCapacity()),
        'Maximum Outdoor Dry-bulb Temperature for Defrost Operation {C}': target_object.maximumOutdoorDrybulbTemperatureforDefrostOperation(),
        'Condenser Type': _vrf_condenser_type(target_object),
        'Water Condenser Volume Flow Rate {m3/s}': 'Autosize' if target_object.isWaterCondenserVolumeFlowRateAutosized() else opt(target_object.waterCondenserVolumeFlowRate()),
        'Evaporative Condenser Effectiveness {dimensionless}': target_object.evaporativeCondenserEffectiveness(),
        'Evaporative Condenser Air Flow Rate {m3/s}': 'Autosize' if target_object.isEvaporativeCondenserAirFlowRateAutosized() else opt(target_object.evaporativeCondenserAirFlowRate()),
        'Evaporative Condenser Pump Rated Power Consumption {W}': 'Autosize' if target_object.isEvaporativeCondenserPumpRatedPowerConsumptionAutosized() else opt(target_object.evaporativeCondenserPumpRatedPowerConsumption()),
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
        'Nominal Capacity {W}': opt(target_object.nominalCapacity()) if target_object.nominalCapacity().is_initialized() else 'Autosize',
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
        'U-Factor Times Area Value {W/K}': opt(target_object.uFactorTimesAreaValue()) if target_object.uFactorTimesAreaValue().is_initialized() else 'Autosize',
        'Maximum Water Flow Rate {m3/s}': opt(target_object.maximumWaterFlowRate()) if target_object.maximumWaterFlowRate().is_initialized() else 'Autosize',
        'Performance Input Method': target_object.performanceInputMethod(),
        'Rated Capacity {W}': opt(target_object.ratedCapacity()) if target_object.ratedCapacity().is_initialized() else 'Autosize',
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
        'Design Water Flow Rate {m3/s}': opt(target_object.designWaterFlowRate()) if target_object.designWaterFlowRate().is_initialized() else 'Autosize',
        'Design Air Flow Rate {m3/s}': opt(target_object.designAirFlowRate()) if target_object.designAirFlowRate().is_initialized() else 'Autosize',
        'Design Inlet Water Temperature {C}': opt(target_object.designInletWaterTemperature()) if target_object.designInletWaterTemperature().is_initialized() else 'Autosize',
        'Design Inlet Air Temperature {C}': opt(target_object.designInletAirTemperature()) if target_object.designInletAirTemperature().is_initialized() else 'Autosize',        
        'Design Outlet Air Temperature {C}': opt(target_object.designOutletAirTemperature()) if target_object.designOutletAirTemperature().is_initialized() else 'Autosize',
        'Design Inlet Air Humidity Ratio {kg-H2O/kg-air}': opt(target_object.designInletAirHumidityRatio()) if target_object.designInletAirHumidityRatio().is_initialized() else 'Autosize',
        'Design Outlet Air Humidity Ratio {kg-H2O/kg-air}': opt(target_object.designOutletAirHumidityRatio()) if target_object.designOutletAirHumidityRatio().is_initialized() else 'Autosize',
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
        'Inlet Node Name': connection_node_name(target_object, "Inlet Node Name"),
        'Outlet Node Name': connection_node_name(target_object, "Outlet Node Name"),
        'Rated Flow Rate {m3/s}': opt(target_object.ratedFlowRate()) if target_object.ratedFlowRate().is_initialized() else 'Autosize', 
        'Rated Pump Head {Pa}': target_object.ratedPumpHead(), 
        'Rated Power Consumption {W}': opt(target_object.ratedPowerConsumption()) if target_object.ratedPowerConsumption().is_initialized() else 'Autosize',
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
        'Reference Capacity {W}': opt(target_object.referenceCapacity()) if target_object.referenceCapacity().is_initialized() else 'Autosize', 
        'Reference COP {W/W}': target_object.referenceCOP(), 
        'Reference Leaving Chilled Water Temperature {C}': target_object.referenceLeavingChilledWaterTemperature(), 
        'Reference Entering Condenser Fluid Temperature {C}': target_object.referenceEnteringCondenserFluidTemperature(), 
        'Reference Chilled Water Flow Rate {m3/s}': opt(target_object.referenceChilledWaterFlowRate()) if target_object.referenceChilledWaterFlowRate().is_initialized() else 'Autosize', 
        'Reference Condenser Fluid Flow Rate {m3/s}': opt(target_object.referenceCondenserFluidFlowRate()) if target_object.referenceCondenserFluidFlowRate().is_initialized() else 'Autosize', 
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
        'Design Heat Recovery Water Flow Rate {m3/s}': opt(target_object.designHeatRecoveryWaterFlowRate()) if target_object.designHeatRecoveryWaterFlowRate().is_initialized() else 'Autosize', 
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


# --------------------------------------------------
#  ***** OS:Fan:VariableVolume *******************
# --------------------------------------------------

FAN_VARIABLE_VOLUME_COLUMNS = (
    'Handle',
    'Name',
    'Availability Schedule Name',
    'Fan Total Efficiency',
    'Pressure Rise {Pa}',
    'Maximum Flow Rate {m3/s}',
    'Fan Power Minimum Flow Rate Input Method',
    'Fan Power Minimum Flow Fraction',
    'Fan Power Minimum Air Flow Rate {m3/s}',
    'Motor Efficiency',
    'Motor In Airstream Fraction',
    'Fan Power Coefficient 1',
    'Fan Power Coefficient 2',
    'Fan Power Coefficient 3',
    'Fan Power Coefficient 4',
    'Fan Power Coefficient 5',
    'Air Inlet Node Name',
    'Air Outlet Node Name',
    'End-Use Subcategory',
)

def get_fan_variable_volume_object_as_dict(
    osm_model: openstudio.model.Model,
    handle: str | None = None,
    name: str | None = None,
    _object_ref: openstudio.model.FanVariableVolume | None = None
) -> dict[str, Any]:
    """
    Retrieve attributes of an OS:Fan:VariableVolume from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.FanVariableVolume, optional): Direct object reference.

    Returns:
    - Dict[str, Any]: A dictionary with one entry per IDD field (node fields give the node name).
    """
    target_object = helpers.fetch_object(
        osm_model, "FanVariableVolume", handle, name, _object_ref)

    if target_object is None:
        return {}

    return {
        'Handle': str(target_object.handle()),
        'Name': opt(target_object.name()),
        'Availability Schedule Name': related_name(target_object, "Availability Schedule Name"),
        'Fan Total Efficiency': target_object.fanTotalEfficiency(),
        'Pressure Rise {Pa}': target_object.pressureRise(),
        'Maximum Flow Rate {m3/s}': (
            'Autosize' if target_object.isMaximumFlowRateAutosized()
            else opt(target_object.maximumFlowRate())
        ),
        'Fan Power Minimum Flow Rate Input Method': target_object.fanPowerMinimumFlowRateInputMethod(),
        'Fan Power Minimum Flow Fraction': target_object.fanPowerMinimumFlowFraction(),
        'Fan Power Minimum Air Flow Rate {m3/s}': opt(target_object.fanPowerMinimumAirFlowRate()),
        'Motor Efficiency': target_object.motorEfficiency(),
        'Motor In Airstream Fraction': target_object.motorInAirstreamFraction(),
        'Fan Power Coefficient 1': opt(target_object.fanPowerCoefficient1()),
        'Fan Power Coefficient 2': opt(target_object.fanPowerCoefficient2()),
        'Fan Power Coefficient 3': opt(target_object.fanPowerCoefficient3()),
        'Fan Power Coefficient 4': opt(target_object.fanPowerCoefficient4()),
        'Fan Power Coefficient 5': opt(target_object.fanPowerCoefficient5()),
        'Air Inlet Node Name': connection_node_name(target_object, "Air Inlet Node Name"),
        'Air Outlet Node Name': connection_node_name(target_object, "Air Outlet Node Name"),
        'End-Use Subcategory': target_object.endUseSubcategory(),
    }

def get_all_fan_variable_volume_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict[str, Any]]:
    """
    Retrieve attributes for all OS:Fan:VariableVolume objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries, one per object.
    """
    all_objects = osm_model.getFanVariableVolumes()
    return [get_fan_variable_volume_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_fan_variable_volume_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:Fan:VariableVolume objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame with the columns of FAN_VARIABLE_VOLUME_COLUMNS.
    """
    all_objects_dicts = get_all_fan_variable_volume_objects_as_dicts(osm_model)
    return build_dataframe(
        all_objects_dicts, "Fan:VariableVolume", sort_by="Name", columns=FAN_VARIABLE_VOLUME_COLUMNS)

# --------------------------------------------------
#  ***** OS:Pump:ConstantSpeed *******************
# --------------------------------------------------

PUMP_CONSTANT_SPEED_COLUMNS = (
    'Handle',
    'Name',
    'Inlet Node Name',
    'Outlet Node Name',
    'Rated Flow Rate {m3/s}',
    'Rated Pump Head {Pa}',
    'Rated Power Consumption {W}',
    'Motor Efficiency',
    'Fraction of Motor Inefficiencies to Fluid Stream',
    'Pump Control Type',
    'Pump Flow Rate Schedule',
    'Pump Curve',
    'Impeller Diameter {m}',
    'Rotational Speed {rev/min}',
    'Zone',
    'Skin Loss Radiative Fraction',
    'Design Power Sizing Method',
    'Design Electric Power per Unit Flow Rate {W/(m3/s)}',
    'Design Shaft Power per Unit Flow Rate per Unit Head {W-s/m3-Pa}',
    'End-Use Subcategory',
)

def get_pump_constant_speed_object_as_dict(
    osm_model: openstudio.model.Model,
    handle: str | None = None,
    name: str | None = None,
    _object_ref: openstudio.model.PumpConstantSpeed | None = None
) -> dict[str, Any]:
    """
    Retrieve attributes of an OS:Pump:ConstantSpeed from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.PumpConstantSpeed, optional): Direct object reference.

    Returns:
    - Dict[str, Any]: A dictionary with one entry per IDD field (node fields give the node name).
    """
    target_object = helpers.fetch_object(
        osm_model, "PumpConstantSpeed", handle, name, _object_ref)

    if target_object is None:
        return {}

    return {
        'Handle': str(target_object.handle()),
        'Name': opt(target_object.name()),
        'Inlet Node Name': connection_node_name(target_object, "Inlet Node Name"),
        'Outlet Node Name': connection_node_name(target_object, "Outlet Node Name"),
        'Rated Flow Rate {m3/s}': (
            'Autosize' if target_object.isRatedFlowRateAutosized()
            else opt(target_object.ratedFlowRate())
        ),
        'Rated Pump Head {Pa}': target_object.ratedPumpHead(),
        'Rated Power Consumption {W}': (
            'Autosize' if target_object.isRatedPowerConsumptionAutosized()
            else opt(target_object.ratedPowerConsumption())
        ),
        'Motor Efficiency': target_object.motorEfficiency(),
        'Fraction of Motor Inefficiencies to Fluid Stream': target_object.fractionofMotorInefficienciestoFluidStream(),
        'Pump Control Type': target_object.pumpControlType(),
        'Pump Flow Rate Schedule': optional_name(target_object.pumpFlowRateSchedule()),
        'Pump Curve': optional_name(target_object.pumpCurve()),
        'Impeller Diameter {m}': opt(target_object.impellerDiameter()),
        'Rotational Speed {rev/min}': opt(target_object.rotationalSpeed()),
        'Zone': optional_name(target_object.zone()),
        'Skin Loss Radiative Fraction': opt(target_object.skinLossRadiativeFraction()),
        'Design Power Sizing Method': target_object.designPowerSizingMethod(),
        'Design Electric Power per Unit Flow Rate {W/(m3/s)}': target_object.designElectricPowerPerUnitFlowRate(),
        'Design Shaft Power per Unit Flow Rate per Unit Head {W-s/m3-Pa}': (
            target_object.designShaftPowerPerUnitFlowRatePerUnitHead()
        ),
        'End-Use Subcategory': target_object.endUseSubcategory(),
    }

def get_all_pump_constant_speed_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict[str, Any]]:
    """
    Retrieve attributes for all OS:Pump:ConstantSpeed objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries, one per object.
    """
    all_objects = osm_model.getPumpConstantSpeeds()
    return [get_pump_constant_speed_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_pump_constant_speed_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:Pump:ConstantSpeed objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame with the columns of PUMP_CONSTANT_SPEED_COLUMNS.
    """
    all_objects_dicts = get_all_pump_constant_speed_objects_as_dicts(osm_model)
    return build_dataframe(
        all_objects_dicts, "Pump:ConstantSpeed", sort_by="Name", columns=PUMP_CONSTANT_SPEED_COLUMNS)

# --------------------------------------------------
#  ***** OS:CoolingTower:TwoSpeed ****************
# --------------------------------------------------

COOLING_TOWER_TWO_SPEED_COLUMNS = (
    'Handle',
    'Name',
    'Water Inlet Node Name',
    'Water Outlet Node Name',
    'Design Water Flow Rate {m3/s}',
    'High Fan Speed Air Flow Rate {m3/s}',
    'High Fan Speed Fan Power {W}',
    'High Fan Speed U-Factor Times Area Value {W/K}',
    'Low Fan Speed Air Flow Rate {m3/s}',
    'Low Fan Speed Air Flow Rate Sizing Factor',
    'Low Fan Speed Fan Power {W}',
    'Low Fan Speed Fan Power Sizing Factor',
    'Low Fan Speed U-Factor Times Area Value {W/K}',
    'Low Fan Speed U-Factor Times Area Sizing Factor',
    'Free Convection Regime Air Flow Rate {m3/s}',
    'Free Convection Regime Air Flow Rate Sizing Factor',
    'Free Convection Regime U-Factor Times Area Value {W/K}',
    'Free Convection U-Factor Times Area Value Sizing Factor',
    'Performance Input Method',
    'Heat Rejection Capacity and Nominal Capacity Sizing Ratio',
    'High Speed Nominal Capacity {W}',
    'Low Speed Nominal Capacity {W}',
    'Low Speed Nominal Capacity Sizing Factor',
    'Free Convection Nominal Capacity {W}',
    'Free Convection Nominal Capacity Sizing Factor',
    'Basin Heater Capacity {W/K}',
    'Basin Heater Setpoint Temperature {C}',
    'Basin Heater Operating Schedule Name',
    'Evaporation Loss Mode',
    'Evaporation Loss Factor {percent/K}',
    'Drift Loss Percent {percent}',
    'Blowdown Calculation Mode',
    'Blowdown Concentration Ratio',
    'Blowdown Makeup Water Usage Schedule Name',
    'Supply Water Storage Tank Name',
    'Outdoor Air Inlet Node Name',
    'Number of Cells',
    'Cell Control',
    'Cell Minimum  Water Flow Rate Fraction',
    'Cell Maximum Water Flow Rate Fraction',
    'Sizing Factor',
    'Design Inlet Air Dry-Bulb Temperature {C}',
    'Design Inlet Air Wet-Bulb Temperature {C}',
    'Design Approach Temperature {deltaC}',
    'Design Range Temperature {deltaC}',
    'End-Use Subcategory',
)

def get_cooling_tower_two_speed_object_as_dict(
    osm_model: openstudio.model.Model,
    handle: str | None = None,
    name: str | None = None,
    _object_ref: openstudio.model.CoolingTowerTwoSpeed | None = None
) -> dict[str, Any]:
    """
    Retrieve attributes of an OS:CoolingTower:TwoSpeed from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.CoolingTowerTwoSpeed, optional): Direct object reference.

    Returns:
    - Dict[str, Any]: A dictionary with one entry per IDD field (node fields give the node name).
    """
    target_object = helpers.fetch_object(
        osm_model, "CoolingTowerTwoSpeed", handle, name, _object_ref)

    if target_object is None:
        return {}

    return {
        'Handle': str(target_object.handle()),
        'Name': opt(target_object.name()),
        'Water Inlet Node Name': connection_node_name(target_object, "Water Inlet Node Name"),
        'Water Outlet Node Name': connection_node_name(target_object, "Water Outlet Node Name"),
        'Design Water Flow Rate {m3/s}': (
            'Autosize' if target_object.isDesignWaterFlowRateAutosized()
            else opt(target_object.designWaterFlowRate())
        ),
        'High Fan Speed Air Flow Rate {m3/s}': (
            'Autosize' if target_object.isHighFanSpeedAirFlowRateAutosized()
            else opt(target_object.highFanSpeedAirFlowRate())
        ),
        'High Fan Speed Fan Power {W}': (
            'Autosize' if target_object.isHighFanSpeedFanPowerAutosized()
            else opt(target_object.highFanSpeedFanPower())
        ),
        'High Fan Speed U-Factor Times Area Value {W/K}': (
            'Autosize' if target_object.isHighFanSpeedUFactorTimesAreaValueAutosized()
            else opt(target_object.highFanSpeedUFactorTimesAreaValue())
        ),
        'Low Fan Speed Air Flow Rate {m3/s}': (
            'Autosize' if target_object.isLowFanSpeedAirFlowRateAutosized()
            else opt(target_object.lowFanSpeedAirFlowRate())
        ),
        'Low Fan Speed Air Flow Rate Sizing Factor': target_object.lowFanSpeedAirFlowRateSizingFactor(),
        'Low Fan Speed Fan Power {W}': (
            'Autosize' if target_object.isLowFanSpeedFanPowerAutosized()
            else opt(target_object.lowFanSpeedFanPower())
        ),
        'Low Fan Speed Fan Power Sizing Factor': target_object.lowFanSpeedFanPowerSizingFactor(),
        'Low Fan Speed U-Factor Times Area Value {W/K}': (
            'Autosize' if target_object.isLowFanSpeedUFactorTimesAreaValueAutosized()
            else opt(target_object.lowFanSpeedUFactorTimesAreaValue())
        ),
        'Low Fan Speed U-Factor Times Area Sizing Factor': target_object.lowFanSpeedUFactorTimesAreaSizingFactor(),
        'Free Convection Regime Air Flow Rate {m3/s}': (
            'Autosize' if target_object.isFreeConvectionRegimeAirFlowRateAutosized()
            else opt(target_object.freeConvectionRegimeAirFlowRate())
        ),
        'Free Convection Regime Air Flow Rate Sizing Factor': (
            target_object.freeConvectionRegimeAirFlowRateSizingFactor()
        ),
        'Free Convection Regime U-Factor Times Area Value {W/K}': (
            'Autosize' if target_object.isFreeConvectionRegimeUFactorTimesAreaValueAutosized()
            else opt(target_object.freeConvectionRegimeUFactorTimesAreaValue())
        ),
        'Free Convection U-Factor Times Area Value Sizing Factor': (
            target_object.freeConvectionUFactorTimesAreaValueSizingFactor()
        ),
        'Performance Input Method': target_object.performanceInputMethod(),
        'Heat Rejection Capacity and Nominal Capacity Sizing Ratio': (
            target_object.heatRejectionCapacityandNominalCapacitySizingRatio()
        ),
        'High Speed Nominal Capacity {W}': opt(target_object.highSpeedNominalCapacity()),
        'Low Speed Nominal Capacity {W}': (
            'Autosize' if target_object.isLowSpeedNominalCapacityAutosized()
            else opt(target_object.lowSpeedNominalCapacity())
        ),
        'Low Speed Nominal Capacity Sizing Factor': target_object.lowSpeedNominalCapacitySizingFactor(),
        'Free Convection Nominal Capacity {W}': (
            'Autosize' if target_object.isFreeConvectionNominalCapacityAutosized()
            else opt(target_object.freeConvectionNominalCapacity())
        ),
        'Free Convection Nominal Capacity Sizing Factor': target_object.freeConvectionNominalCapacitySizingFactor(),
        'Basin Heater Capacity {W/K}': target_object.basinHeaterCapacity(),
        'Basin Heater Setpoint Temperature {C}': target_object.basinHeaterSetpointTemperature(),
        'Basin Heater Operating Schedule Name': optional_name(target_object.basinHeaterOperatingSchedule()),
        'Evaporation Loss Mode': target_object.evaporationLossMode(),
        'Evaporation Loss Factor {percent/K}': target_object.evaporationLossFactor(),
        'Drift Loss Percent {percent}': target_object.driftLossPercent(),
        'Blowdown Calculation Mode': target_object.blowdownCalculationMode(),
        'Blowdown Concentration Ratio': target_object.blowdownConcentrationRatio(),
        'Blowdown Makeup Water Usage Schedule Name': optional_name(target_object.blowdownMakeupWaterUsageSchedule()),
        'Supply Water Storage Tank Name': related_name(target_object, "Supply Water Storage Tank Name"),
        'Outdoor Air Inlet Node Name': connection_node_name(target_object, "Outdoor Air Inlet Node Name"),
        'Number of Cells': target_object.numberofCells(),
        'Cell Control': target_object.cellControl(),
        'Cell Minimum  Water Flow Rate Fraction': target_object.cellMinimumWaterFlowRateFraction(),
        'Cell Maximum Water Flow Rate Fraction': target_object.cellMaximumWaterFlowRateFraction(),
        'Sizing Factor': target_object.sizingFactor(),
        'Design Inlet Air Dry-Bulb Temperature {C}': target_object.designInletAirDryBulbTemperature(),
        'Design Inlet Air Wet-Bulb Temperature {C}': target_object.designInletAirWetBulbTemperature(),
        'Design Approach Temperature {deltaC}': (
            'Autosize' if target_object.isDesignApproachTemperatureAutosized()
            else opt(target_object.designApproachTemperature())
        ),
        'Design Range Temperature {deltaC}': (
            'Autosize' if target_object.isDesignRangeTemperatureAutosized()
            else opt(target_object.designRangeTemperature())
        ),
        'End-Use Subcategory': target_object.endUseSubcategory(),
    }

def get_all_cooling_tower_two_speed_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict[str, Any]]:
    """
    Retrieve attributes for all OS:CoolingTower:TwoSpeed objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries, one per object.
    """
    all_objects = osm_model.getCoolingTowerTwoSpeeds()
    return [get_cooling_tower_two_speed_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_cooling_tower_two_speed_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:CoolingTower:TwoSpeed objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame with the columns of COOLING_TOWER_TWO_SPEED_COLUMNS.
    """
    all_objects_dicts = get_all_cooling_tower_two_speed_objects_as_dicts(osm_model)
    return build_dataframe(
        all_objects_dicts, "CoolingTower:TwoSpeed", sort_by="Name", columns=COOLING_TOWER_TWO_SPEED_COLUMNS)

# --------------------------------------------------
#  ***** OS:CoolingTower:VariableSpeed ***********
# --------------------------------------------------

COOLING_TOWER_VARIABLE_SPEED_COLUMNS = (
    'Handle',
    'Name',
    'Water Inlet Node',
    'Water Outlet Node',
    'Model Type',
    'Model Coefficient',
    'Design Inlet Air Wet-Bulb Temperature {C}',
    'Design Approach Temperature {deltaC}',
    'Design Range Temperature {deltaC}',
    'Design Water Flow Rate {m3/s}',
    'Design Air Flow Rate {m3/s}',
    'Design Fan Power {W}',
    'Fan Power Ratio Function of Air Flow Rate Ratio Curve',
    'Minimum Air Flow Rate Ratio',
    'Fraction of Tower Capacity in Free Convection Regime',
    'Basin Heater Capacity {W/K}',
    'Basin Heater Setpoint Temperature {C}',
    'Basin Heater Operating Schedule',
    'Evaporation Loss Mode',
    'Evaporation Loss Factor {percent/K}',
    'Drift Loss Percent {percent}',
    'Blowdown Calculation Mode',
    'Blowdown Concentration Ratio',
    'Blowdown Makeup Water Usage Schedule',
    'Supply Water Storage Tank',
    'Outdoor Air Inlet Node',
    'Number of Cells',
    'Cell Control',
    'Cell Minimum  Water Flow Rate Fraction',
    'Cell Maximum Water Flow Rate Fraction',
    'Sizing Factor',
    'End-Use Subcategory',
)

def get_cooling_tower_variable_speed_object_as_dict(
    osm_model: openstudio.model.Model,
    handle: str | None = None,
    name: str | None = None,
    _object_ref: openstudio.model.CoolingTowerVariableSpeed | None = None
) -> dict[str, Any]:
    """
    Retrieve attributes of an OS:CoolingTower:VariableSpeed from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.CoolingTowerVariableSpeed, optional): Direct object reference.

    Returns:
    - Dict[str, Any]: A dictionary with one entry per IDD field (node fields give the node name).
    """
    target_object = helpers.fetch_object(
        osm_model, "CoolingTowerVariableSpeed", handle, name, _object_ref)

    if target_object is None:
        return {}

    return {
        'Handle': str(target_object.handle()),
        'Name': opt(target_object.name()),
        'Water Inlet Node': connection_node_name(target_object, "Water Inlet Node"),
        'Water Outlet Node': connection_node_name(target_object, "Water Outlet Node"),
        'Model Type': opt(target_object.modelType()),
        'Model Coefficient': optional_name(target_object.modelCoefficient()),
        'Design Inlet Air Wet-Bulb Temperature {C}': opt(target_object.designInletAirWetBulbTemperature()),
        'Design Approach Temperature {deltaC}': opt(target_object.designApproachTemperature()),
        'Design Range Temperature {deltaC}': opt(target_object.designRangeTemperature()),
        'Design Water Flow Rate {m3/s}': (
            'Autosize' if target_object.isDesignWaterFlowRateAutosized()
            else opt(target_object.designWaterFlowRate())
        ),
        'Design Air Flow Rate {m3/s}': (
            'Autosize' if target_object.isDesignAirFlowRateAutosized()
            else opt(target_object.designAirFlowRate())
        ),
        'Design Fan Power {W}': (
            'Autosize' if target_object.isDesignFanPowerAutosized()
            else opt(target_object.designFanPower())
        ),
        'Fan Power Ratio Function of Air Flow Rate Ratio Curve': (
            optional_name(target_object.fanPowerRatioFunctionofAirFlowRateRatioCurve())
        ),
        'Minimum Air Flow Rate Ratio': opt(target_object.minimumAirFlowRateRatio()),
        'Fraction of Tower Capacity in Free Convection Regime': (
            opt(target_object.fractionofTowerCapacityinFreeConvectionRegime())
        ),
        'Basin Heater Capacity {W/K}': opt(target_object.basinHeaterCapacity()),
        'Basin Heater Setpoint Temperature {C}': opt(target_object.basinHeaterSetpointTemperature()),
        'Basin Heater Operating Schedule': optional_name(target_object.basinHeaterOperatingSchedule()),
        'Evaporation Loss Mode': target_object.evaporationLossMode(),
        'Evaporation Loss Factor {percent/K}': target_object.evaporationLossFactor(),
        'Drift Loss Percent {percent}': opt(target_object.driftLossPercent()),
        'Blowdown Calculation Mode': target_object.blowdownCalculationMode(),
        'Blowdown Concentration Ratio': opt(target_object.blowdownConcentrationRatio()),
        'Blowdown Makeup Water Usage Schedule': optional_name(target_object.blowdownMakeupWaterUsageSchedule()),
        'Supply Water Storage Tank': related_name(target_object, "Supply Water Storage Tank"),
        'Outdoor Air Inlet Node': connection_node_name(target_object, "Outdoor Air Inlet Node"),
        'Number of Cells': opt(target_object.numberofCells()),
        'Cell Control': target_object.cellControl(),
        'Cell Minimum  Water Flow Rate Fraction': opt(target_object.cellMinimumWaterFlowRateFraction()),
        'Cell Maximum Water Flow Rate Fraction': opt(target_object.cellMaximumWaterFlowRateFraction()),
        'Sizing Factor': opt(target_object.sizingFactor()),
        'End-Use Subcategory': target_object.endUseSubcategory(),
    }

def get_all_cooling_tower_variable_speed_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict[str, Any]]:
    """
    Retrieve attributes for all OS:CoolingTower:VariableSpeed objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries, one per object.
    """
    all_objects = osm_model.getCoolingTowerVariableSpeeds()
    return [get_cooling_tower_variable_speed_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_cooling_tower_variable_speed_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:CoolingTower:VariableSpeed objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame with the columns of COOLING_TOWER_VARIABLE_SPEED_COLUMNS.
    """
    all_objects_dicts = get_all_cooling_tower_variable_speed_objects_as_dicts(osm_model)
    return build_dataframe(
        all_objects_dicts, "CoolingTower:VariableSpeed", sort_by="Name", columns=COOLING_TOWER_VARIABLE_SPEED_COLUMNS)

# --------------------------------------------------
#  ***** OS:Boiler:HotWater **********************
# --------------------------------------------------

BOILER_HOT_WATER_COLUMNS = (
    'Handle',
    'Name',
    'Fuel Type',
    'Nominal Capacity {W}',
    'Nominal Thermal Efficiency',
    'Efficiency Curve Temperature Evaluation Variable',
    'Normalized Boiler Efficiency Curve Name',
    'Design Water Flow Rate {m3/s}',
    'Minimum Part Load Ratio',
    'Maximum Part Load Ratio',
    'Optimum Part Load Ratio',
    'Boiler Water Inlet Node Name',
    'Boiler Water Outlet Node Name',
    'Water Outlet Upper Temperature Limit {C}',
    'Boiler Flow Mode',
    'On Cycle Parasitic Electric Load {W}',
    'Off Cycle Parasitic Fuel Load {W}',
    'Sizing Factor',
    'End-Use Subcategory',
)

def get_boiler_hot_water_object_as_dict(
    osm_model: openstudio.model.Model,
    handle: str | None = None,
    name: str | None = None,
    _object_ref: openstudio.model.BoilerHotWater | None = None
) -> dict[str, Any]:
    """
    Retrieve attributes of an OS:Boiler:HotWater from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.BoilerHotWater, optional): Direct object reference.

    Returns:
    - Dict[str, Any]: A dictionary with one entry per IDD field (node fields give the node name).
    """
    target_object = helpers.fetch_object(
        osm_model, "BoilerHotWater", handle, name, _object_ref)

    if target_object is None:
        return {}

    return {
        'Handle': str(target_object.handle()),
        'Name': opt(target_object.name()),
        'Fuel Type': target_object.fuelType(),
        'Nominal Capacity {W}': (
            'Autosize' if target_object.isNominalCapacityAutosized()
            else opt(target_object.nominalCapacity())
        ),
        'Nominal Thermal Efficiency': target_object.nominalThermalEfficiency(),
        'Efficiency Curve Temperature Evaluation Variable': (
            opt(target_object.efficiencyCurveTemperatureEvaluationVariable())
        ),
        'Normalized Boiler Efficiency Curve Name': optional_name(target_object.normalizedBoilerEfficiencyCurve()),
        'Design Water Flow Rate {m3/s}': (
            'Autosize' if target_object.isDesignWaterFlowRateAutosized()
            else opt(target_object.designWaterFlowRate())
        ),
        'Minimum Part Load Ratio': target_object.minimumPartLoadRatio(),
        'Maximum Part Load Ratio': target_object.maximumPartLoadRatio(),
        'Optimum Part Load Ratio': target_object.optimumPartLoadRatio(),
        'Boiler Water Inlet Node Name': connection_node_name(target_object, "Boiler Water Inlet Node Name"),
        'Boiler Water Outlet Node Name': connection_node_name(target_object, "Boiler Water Outlet Node Name"),
        'Water Outlet Upper Temperature Limit {C}': target_object.waterOutletUpperTemperatureLimit(),
        'Boiler Flow Mode': target_object.boilerFlowMode(),
        'On Cycle Parasitic Electric Load {W}': target_object.onCycleParasiticElectricLoad(),
        'Off Cycle Parasitic Fuel Load {W}': target_object.offCycleParasiticFuelLoad(),
        'Sizing Factor': target_object.sizingFactor(),
        'End-Use Subcategory': target_object.endUseSubcategory(),
    }

def get_all_boiler_hot_water_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict[str, Any]]:
    """
    Retrieve attributes for all OS:Boiler:HotWater objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries, one per object.
    """
    all_objects = osm_model.getBoilerHotWaters()
    return [get_boiler_hot_water_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_boiler_hot_water_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:Boiler:HotWater objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame with the columns of BOILER_HOT_WATER_COLUMNS.
    """
    all_objects_dicts = get_all_boiler_hot_water_objects_as_dicts(osm_model)
    return build_dataframe(
        all_objects_dicts, "Boiler:HotWater", sort_by="Name", columns=BOILER_HOT_WATER_COLUMNS)
