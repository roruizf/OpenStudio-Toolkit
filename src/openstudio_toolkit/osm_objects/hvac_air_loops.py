import logging
from typing import Any

import openstudio
import pandas as pd

from openstudio_toolkit._sdk import connection_node_name, opt, optional_name, related_name
from openstudio_toolkit.osm_objects._base import build_dataframe

# Configure logger
logger = logging.getLogger(__name__)


#-------------------
#--- OS:AirLoopHVAC
#-------------------
AIR_LOOP_HVAC_COLUMNS = (
    'Handle',
    'Name',
    'Controller List Name',
    'Availability Schedule',
    'Availability Manager List Name',
    'Design Supply Air Flow Rate {m3/s}',
    'Design Return Air Flow Fraction of Supply Air Flow',
    'Branch List Name',
    'Connector List Name',
    'Supply Side Inlet Node Name',
    'Demand Side Outlet Node Name',
    'Demand Side Inlet Node A',
    'Supply Side Outlet Node A',
    'Demand Side Inlet Node B',
    'Supply Side Outlet Node B',
    'Return Air Bypass Flow Temperature Setpoint Schedule Name',
    'Demand Mixer Name',
    'Demand Splitter A Name',
    'Demand Splitter B Name',
    'Supply Splitter Name',
)

def get_air_loop_hvac_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: str | None = None, 
    name: str | None = None
) -> dict[str, Any]:
    """
    Retrieve attributes of an OS:AirLoopHVAC object from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.

    Returns:
    - Dict[str, Any]: A dictionary containing AirLoopHVAC attributes.
    """
        
    if handle is not None and name is not None:
        raise ValueError(
            "Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError(
            "Either 'handle' or 'name' must be provided.")

    if handle is not None:
        osm_object = osm_model.getAirLoopHVAC(
            handle)
        if not osm_object:
            logger.warning(
                f"No Air Loop HVAC  object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getAirLoopHVACByName(
            name)
        if not osm_object:
            logger.warning(
                f"No Air Loop HVAC  object found with the name: {name}")
            return {}

    target_object = opt(osm_object)

    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': opt(target_object.name()) if target_object.name().is_initialized() else None,
        'Controller List Name': None,
        'Availability Schedule': opt(target_object.availabilitySchedule().name()) if target_object.availabilitySchedule().name().is_initialized() else None,
        'Availability Manager List Name': None,
        'Design Supply Air Flow Rate {m3/s}': 'Autosize' if target_object.isDesignSupplyAirFlowRateAutosized() else opt(target_object.designSupplyAirFlowRate()),
        'Design Return Air Flow Fraction of Supply Air Flow': target_object.designReturnAirFlowFractionofSupplyAirFlow(),
        'Branch List Name': None,
        'Connector List Name': None,
        'Supply Side Inlet Node Name': connection_node_name(target_object, "Supply Side Inlet Node Name"),
        'Demand Side Outlet Node Name': connection_node_name(target_object, "Demand Side Outlet Node Name"),
        'Demand Side Inlet Node A': connection_node_name(target_object, "Demand Side Inlet Node A"),
        'Supply Side Outlet Node A': connection_node_name(target_object, "Supply Side Outlet Node A"),
        'Demand Side Inlet Node B': None,
        'Supply Side Outlet Node B': None,
        'Return Air Bypass Flow Temperature Setpoint Schedule Name': None,
        'Demand Mixer Name': target_object.demandMixer().nameString(),
        'Demand Splitter A Name': target_object.demandSplitter().nameString(),
        'Demand Splitter B Name': None,
        'Supply Splitter Name': None}
    return object_dict


def get_all_air_loop_hvac_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict[str, Any]]:
    """
    Retrieve attributes for all OS:AirLoopHVAC objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing AirLoopHVAC attributes.
    """

    # Get all spaces in the OpenStudio model.
    all_objects = osm_model.getAirLoopHVACs()

    all_objects_dicts = []

    for target_object in all_objects:
        air_loop_hvac_handle = str(target_object.handle())
        object_dict = get_air_loop_hvac_object_as_dict(
            osm_model, air_loop_hvac_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_air_loop_hvac_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:AirLoopHVAC objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all AirLoopHVAC attributes.
    """

    all_objects_dicts = get_all_air_loop_hvac_objects_as_dicts(osm_model)

    return build_dataframe(
        all_objects_dicts, "Air Loop HVAC", sort_by="Name",
        columns=AIR_LOOP_HVAC_COLUMNS)

#------------------------------------
#--- OS:AirLoopHVAC:OutdoorAirSystem
#------------------------------------

AIR_LOOP_HVAC_OUTDOOR_AIR_SYSTEM_COLUMNS = (
    'Handle',
    'Name',
    'Controller Name',
    'Outdoor Air Equipment List Name',
    'Availability Manager List Name',
    'Mixed Air Node Name',
    'Outdoor Air Stream Node Name',
    'Relief Air Stream Node Name',
    'Return Air Stream Node Name',
)

def get_air_loop_hvac_outdoor_air_system_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: str | None = None, 
    name: str | None = None
) -> dict[str, Any]:
    """
    Retrieve attributes of an OS:AirLoopHVAC:OutdoorAirSystem object from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.

    Returns:
    - Dict[str, Any]: A dictionary containing AirLoopHVAC:OutdoorAirSystem attributes.
    """
    if handle is not None and name is not None:
        raise ValueError(
            "Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError(
            "Either 'handle' or 'name' must be provided.")

    if handle is not None:
        osm_object = osm_model.getAirLoopHVACOutdoorAirSystem(handle)
        if not osm_object:
            logger.warning(
                f"No AirLoopHVAC:OutdoorAirSystem object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getAirLoopHVACOutdoorAirSystemByName(name)
        if not osm_object:
            logger.warning(
                f"No AirLoopHVAC:OutdoorAirSystem object found with the name: {name}")
            return {}

    target_object = opt(osm_object)

    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': opt(target_object.name()) if target_object.name().is_initialized() else None,
        'Controller Name': related_name(target_object, "Controller Name"),
        'Outdoor Air Equipment List Name': None,
        'Availability Manager List Name': None,
        'Mixed Air Node Name': None,
        'Outdoor Air Stream Node Name': None,
        'Relief Air Stream Node Name': None,
        'Return Air Stream Node Name': None
        }

    return object_dict

def get_all_air_loop_hvac_outdoor_air_system_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict[str, Any]]:
    """
    Retrieve attributes for all OS:AirLoopHVAC:OutdoorAirSystem objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing AirLoopHVAC:OutdoorAirSystem attributes.
    """

    # Get all AirLoopHVAC:OutdoorAirSystem objects in the OpenStudio model.
    all_objects = osm_model.getAirLoopHVACOutdoorAirSystems()

    all_objects_dicts = []

    for target_object in all_objects:
        object_handle = str(target_object.handle())
        object_dict = get_air_loop_hvac_outdoor_air_system_object_as_dict(osm_model, object_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts

def get_all_air_loop_hvac_outdoor_air_system_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:AirLoopHVAC:OutdoorAirSystem objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all AirLoopHVAC:OutdoorAirSystem attributes.
    """

    all_objects_dicts = get_all_air_loop_hvac_outdoor_air_system_objects_as_dicts(osm_model)

    return build_dataframe(
        all_objects_dicts, "AirLoopHVAC:OutdoorAirSystem", sort_by="Name",
        columns=AIR_LOOP_HVAC_OUTDOOR_AIR_SYSTEM_COLUMNS)

#---------------------------------
#--- OS:AirLoopHVAC:UnitarySystem
#---------------------------------

AIR_LOOP_HVAC_UNITARY_SYSTEM_COLUMNS = (
    'Handle',
    'Name',
    'Control Type',
    'Controlling Zone or Thermostat Location',
    'Dehumidification Control Type',
    'Availability Schedule Name',
    'Air Inlet Node Name',
    'Air Outlet Node Name',
    'Supply Fan Name',
    'Fan Placement',
    'Supply Air Fan Operating Mode Schedule Name',
    'Heating Coil Name',
    'DX Heating Coil Sizing Ratio',
    'Cooling Coil Name',
    'Use DOAS DX Cooling Coil',
    'DOAS DX Cooling Coil Leaving Minimum Air Temperature {C}',
    'Latent Load Control',
    'Supplemental Heating Coil Name',
    'Supply Air Flow Rate Method During Cooling Operation',
    'Supply Air Flow Rate During Cooling Operation {m3/s}',
    'Supply Air Flow Rate Per Floor Area During Cooling Operation {m3/s-m2}',
    'Fraction of Autosized Design Cooling Supply Air Flow Rate',
    'Design Supply Air Flow Rate Per Unit of Capacity During Cooling Operation {m3/s-W}',
    'Supply Air Flow Rate Method During Heating Operation',
    'Supply Air Flow Rate During Heating Operation {m3/s}',
    'Supply Air Flow Rate Per Floor Area during Heating Operation {m3/s-m2}',
    'Fraction of Autosized Design Heating Supply Air Flow Rate',
    'Design Supply Air Flow Rate Per Unit of Capacity During Heating Operation {m3/s-W}',
    'Supply Air Flow Rate Method When No Cooling or Heating is Required',
    'Supply Air Flow Rate When No Cooling or Heating is Required {m3/s}',
    'Supply Air Flow Rate Per Floor Area When No Cooling or Heating is Required {m3/s-m2}',
    'Fraction of Autosized Design Cooling Supply Air Flow Rate When No Cooling or Heating is Required',
    'Fraction of Autosized Design Heating Supply Air Flow Rate When No Cooling or Heating is Required',
    'Design Supply Air Flow Rate Per Unit of Capacity During Cooling Operation When No Cooling or Heating is Required {m3/s-W}',
    'Design Supply Air Flow Rate Per Unit of Capacity During Heating Operation When No Cooling or Heating is Required {m3/s-W}',
    'Maximum Supply Air Temperature {C}',
    'Maximum Outdoor Dry-Bulb Temperature for Supplemental Heater Operation {C}',
    'Outdoor Dry-Bulb Temperature Sensor Node Name',
    'Ancilliary On-Cycle Electric Power {W}',
    'Ancilliary Off-Cycle Electric Power {W}',
)

def get_air_loop_hvac_unitary_system_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: str | None = None, 
    name: str | None = None
) -> dict[str, Any]:
    """
    Retrieve attributes of an OS:AirLoopHVAC:UnitarySystem object from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.

    Returns:
    - Dict[str, Any]: A dictionary containing AirLoopHVAC:UnitarySystem attributes.
    """
    if handle is not None and name is not None:
        raise ValueError(
            "Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError(
            "Either 'handle' or 'name' must be provided.")

    if handle is not None:
        osm_object = osm_model.getAirLoopHVACUnitarySystem(handle)
        if not osm_object:
            logger.warning(
                f"No AirLoopHVAC:UnitarySystem object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getAirLoopHVACUnitarySystemByName(name)
        if not osm_object:
            logger.warning(
                f"No AirLoopHVAC:UnitarySystem object found with the name: {name}")
            return {}

    target_object = opt(osm_object)

    object_dict = {
    'Handle': str(target_object.handle()),
    'Name': opt(target_object.name()) if target_object.name().is_initialized() else None,
    "Control Type": target_object.controlType(),
    "Controlling Zone or Thermostat Location": opt(target_object.controllingZoneorThermostatLocation()).nameString() if target_object.controllingZoneorThermostatLocation().is_initialized() else None,
    "Dehumidification Control Type": target_object.dehumidificationControlType(),
    'Availability Schedule Name': optional_name(target_object.availabilitySchedule()),
    "Air Inlet Node Name": optional_name(target_object.inletNode()),
    "Air Outlet Node Name": optional_name(target_object.outletNode()),
    "Supply Fan Name": optional_name(target_object.supplyFan()),
    "Fan Placement": opt(target_object.fanPlacement()),
    "Supply Air Fan Operating Mode Schedule Name": optional_name(target_object.supplyAirFanOperatingModeSchedule()),
    "Heating Coil Name": optional_name(target_object.heatingCoil()),
    "DX Heating Coil Sizing Ratio": target_object.dXHeatingCoilSizingRatio(),
    "Cooling Coil Name": optional_name(target_object.coolingCoil()),
    "Use DOAS DX Cooling Coil": target_object.useDOASDXCoolingCoil(),
    "DOAS DX Cooling Coil Leaving Minimum Air Temperature {C}": target_object.useDOASDXCoolingCoil(),
    "Latent Load Control": target_object.latentLoadControl(),
    "Supplemental Heating Coil Name": optional_name(target_object.supplementalHeatingCoil()),
    "Supply Air Flow Rate Method During Cooling Operation": target_object.supplyAirFlowRateMethodDuringCoolingOperation(),
    "Supply Air Flow Rate During Cooling Operation {m3/s}": 'Autosize' if target_object.isSupplyAirFlowRateDuringCoolingOperationAutosized() else opt(target_object.supplyAirFlowRateDuringCoolingOperation()),    
    "Supply Air Flow Rate Per Floor Area During Cooling Operation {m3/s-m2}": opt(target_object.supplyAirFlowRatePerFloorAreaDuringCoolingOperation()) if target_object.supplyAirFlowRatePerFloorAreaDuringCoolingOperation().is_initialized() else None,    
    "Fraction of Autosized Design Cooling Supply Air Flow Rate": None,
    "Design Supply Air Flow Rate Per Unit of Capacity During Cooling Operation {m3/s-W}": None,
    "Supply Air Flow Rate Method During Heating Operation": target_object.supplyAirFlowRateMethodDuringHeatingOperation(),
    "Supply Air Flow Rate During Heating Operation {m3/s}": 'Autosize' if target_object.isSupplyAirFlowRateDuringHeatingOperationAutosized() else opt(target_object.supplyAirFlowRateDuringHeatingOperation()),
    "Supply Air Flow Rate Per Floor Area during Heating Operation {m3/s-m2}": None,
    "Fraction of Autosized Design Heating Supply Air Flow Rate": None,
    "Design Supply Air Flow Rate Per Unit of Capacity During Heating Operation {m3/s-W}": None,
    "Supply Air Flow Rate Method When No Cooling or Heating is Required": None,
    "Supply Air Flow Rate When No Cooling or Heating is Required {m3/s}": None,
    "Supply Air Flow Rate Per Floor Area When No Cooling or Heating is Required {m3/s-m2}": None,
    "Fraction of Autosized Design Cooling Supply Air Flow Rate When No Cooling or Heating is Required": None,
    "Fraction of Autosized Design Heating Supply Air Flow Rate When No Cooling or Heating is Required": None,
    "Design Supply Air Flow Rate Per Unit of Capacity During Cooling Operation When No Cooling or Heating is Required {m3/s-W}": None,
    "Design Supply Air Flow Rate Per Unit of Capacity During Heating Operation When No Cooling or Heating is Required {m3/s-W}": None,
    "Maximum Supply Air Temperature {C}": opt(target_object.maximumSupplyAirTemperature()),
    "Maximum Outdoor Dry-Bulb Temperature for Supplemental Heater Operation {C}": target_object.maximumOutdoorDryBulbTemperatureforSupplementalHeaterOperation(),
    "Outdoor Dry-Bulb Temperature Sensor Node Name": None,
    "Ancilliary On-Cycle Electric Power {W}": target_object.ancilliaryOnCycleElectricPower(),
    "Ancilliary Off-Cycle Electric Power {W}": target_object.ancilliaryOffCycleElectricPower()
}


    return object_dict

def get_all_air_loop_hvac_unitary_system_objects_as_dict(osm_model: openstudio.model.Model) -> list[dict[str, Any]]:
    """
    Retrieve attributes for all OS:AirLoopHVAC:UnitarySystem objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing AirLoopHVAC:UnitarySystem attributes.
    """

    # Get all spaces in the OpenStudio model.
    all_objects = osm_model.getAirLoopHVACUnitarySystems()

    all_objects_dicts = []

    for target_object in all_objects:
        space_handle = str(target_object.handle())
        object_dict = get_air_loop_hvac_unitary_system_object_as_dict(osm_model, space_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts

def get_all_air_loop_hvac_unitary_system_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:AirLoopHVAC:UnitarySystem objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all AirLoopHVAC:UnitarySystem attributes.
    """

    all_objects_dicts = get_all_air_loop_hvac_unitary_system_objects_as_dict(osm_model)

    return build_dataframe(
        all_objects_dicts, "AirLoopHVAC:UnitarySystem", sort_by="Name",
        columns=AIR_LOOP_HVAC_UNITARY_SYSTEM_COLUMNS)