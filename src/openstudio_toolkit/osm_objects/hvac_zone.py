import logging
from typing import Any

import openstudio
import pandas as pd

from openstudio_toolkit._sdk import opt, optional_name, related_name
from openstudio_toolkit.osm_objects._base import build_dataframe

# Configure logger
logger = logging.getLogger(__name__)

#--
#-- OS:ZoneHVAC:EquipmentList
#--

# Fixed minimum of equipment slots so every model yields the same columns (the most equipment per zone
# seen in 400 local models is 4; OpenStudio sets no limit). A zone with more adds slots instead of
# dropping equipment; unused slots are None.
MIN_ZONE_EQUIPMENT_COLUMNS = 5


def get_all_zone_hvac_equipment_list_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:ZoneHVAC:EquipmentList objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all ZoneHVAC:EquipmentList attributes.
    """
    all_zone_hvac_equipment_lists = osm_model.getZoneHVACEquipmentLists()

    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_zone_hvac_equipment_lists],
        'Name': [opt(x.name()) for x in all_zone_hvac_equipment_lists],
        'Thermal Zone': [related_name(x, "Thermal Zone") for x in all_zone_hvac_equipment_lists],
        'Load Distribution Scheme': [x.loadDistributionScheme() for x in all_zone_hvac_equipment_lists]
        }

    # Create a DataFrame of all thermal zones.
    all_zone_hvac_equipment_lists_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_zone_hvac_equipment_lists_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_zone_hvac_equipment_lists_df = all_zone_hvac_equipment_lists_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    # Equipment columns: at least MIN_ZONE_EQUIPMENT_COLUMNS slots, more if a zone has more equipment
    zone_equipment_max = MIN_ZONE_EQUIPMENT_COLUMNS
    for zone_hvac_equipment_list in all_zone_hvac_equipment_lists:
        num_elements = len(zone_hvac_equipment_list.equipment())
        if num_elements > zone_equipment_max:
            zone_equipment_max = num_elements
    
    for i in range(zone_equipment_max):
      all_zone_hvac_equipment_lists_df[f'Zone Equipment {i+1}'] = None
      all_zone_hvac_equipment_lists_df[f'Zone Equipment Cooling Sequence {i+1}'] = None
      all_zone_hvac_equipment_lists_df[f'Zone Equipment Heating or No-Load Sequence {i+1}'] = None
      all_zone_hvac_equipment_lists_df[f'Zone Equipment Sequential Cooling Fraction Schedule Name {i+1}'] = None
      all_zone_hvac_equipment_lists_df[f'Zone Equipment Sequential Heating Fraction Schedule Name {i+1}'] = None


    for index, row in all_zone_hvac_equipment_lists_df.iterrows():
      # Add columns for each zone HVAC equipment
      zone_hvac_equipment_list = opt(osm_model.getZoneHVACEquipmentListByName(row['Name']))
      if zone_hvac_equipment_list is None:
        continue
      for i in range(len(zone_hvac_equipment_list.equipment())):
        equipment = zone_hvac_equipment_list.equipment()[i]
        all_zone_hvac_equipment_lists_df.loc[index, f'Zone Equipment {i+1}'] = opt(equipment.name())
        all_zone_hvac_equipment_lists_df.loc[index, f'Zone Equipment Cooling Sequence {i+1}'] = zone_hvac_equipment_list.coolingPriority(equipment)
        all_zone_hvac_equipment_lists_df.loc[index, f'Zone Equipment Heating or No-Load Sequence {i+1}'] = zone_hvac_equipment_list.heatingPriority(equipment)
        all_zone_hvac_equipment_lists_df.loc[index, f'Zone Equipment Sequential Cooling Fraction Schedule Name {i+1}'] = optional_name(zone_hvac_equipment_list.sequentialCoolingFractionSchedule(equipment))
        all_zone_hvac_equipment_lists_df.loc[index, f'Zone Equipment Sequential Heating Fraction Schedule Name {i+1}'] = optional_name(zone_hvac_equipment_list.sequentialHeatingFractionSchedule(equipment))

    logger.info(
        f"The OSM model contains {all_zone_hvac_equipment_lists_df.shape[0]} thermal zones")

    return all_zone_hvac_equipment_lists_df



def get_all_zone_hvac_terminal_unit_variant_refrigerant_flow_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:ZoneHVAC:TerminalUnit:VariableRefrigerantFlow objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all VRF terminal unit attributes.
    """

    all_zone_hvac_vrfs = osm_model.getZoneHVACTerminalUnitVariableRefrigerantFlows()

    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_zone_hvac_vrfs],
        'Name': [opt(x.name()) for x in all_zone_hvac_vrfs],
        'Terminal Unit Availability schedule': [related_name(x, "Terminal Unit Availability schedule") for x in all_zone_hvac_vrfs],
        'Terminal Unit Air Inlet Node': None,
        'Terminal Unit Air Outlet Node': None,
        'Supply Air Flow Rate During Cooling Operation {m3/s}': [opt(x.supplyAirFlowRateDuringCoolingOperation()) for x in all_zone_hvac_vrfs],
        'Supply Air Flow Rate When No Cooling is Needed {m3/s}': [opt(x.supplyAirFlowRateWhenNoCoolingisNeeded()) for x in all_zone_hvac_vrfs],
        'Supply Air Flow Rate During Heating Operation {m3/s}': [opt(x.supplyAirFlowRateDuringHeatingOperation()) for x in all_zone_hvac_vrfs],
        'Supply Air Flow Rate When No Heating is Needed {m3/s}': [opt(x.supplyAirFlowRateWhenNoHeatingisNeeded()) for x in all_zone_hvac_vrfs],
        'Outdoor Air Flow Rate During Cooling Operation {m3/s}': [opt(x.outdoorAirFlowRateDuringCoolingOperation()) for x in all_zone_hvac_vrfs],
        'Outdoor Air Flow Rate During Heating Operation {m3/s}': [opt(x.outdoorAirFlowRateDuringHeatingOperation()) for x in all_zone_hvac_vrfs],
        'Outdoor Air Flow Rate When No Cooling or Heating is Needed {m3/s}': [opt(x.outdoorAirFlowRateWhenNoCoolingorHeatingisNeeded()) for x in all_zone_hvac_vrfs],
        'Supply Air Fan Operating Mode Schedule': [related_name(x, "Supply Air Fan Operating Mode Schedule") for x in all_zone_hvac_vrfs],
        'Supply Air Fan Placement': [x.supplyAirFanPlacement() for x in all_zone_hvac_vrfs],
        'Supply Air Fan': [related_name(x, "Supply Air Fan") for x in all_zone_hvac_vrfs],
        'Outside Air Mixer': None,
        'Cooling Coil': [optional_name(x.coolingCoil()) for x in all_zone_hvac_vrfs],
        'Heating Coil': [optional_name(x.heatingCoil()) for x in all_zone_hvac_vrfs],
        'Zone Terminal Unit On Parasitic Electric Energy Use {W}': [x.zoneTerminalUnitOnParasiticElectricEnergyUse() for x in all_zone_hvac_vrfs],
        'Zone Terminal Unit Off Parasitic Electric Energy Use {W}': [x.zoneTerminalUnitOffParasiticElectricEnergyUse() for x in all_zone_hvac_vrfs],
        'Rated Total Heating Capacity Sizing Ratio {W/W}': [x.ratedTotalHeatingCapacitySizingRatio() for x in all_zone_hvac_vrfs],
        'Availability Manager List Name': None,
        'Design Specification ZoneHVAC Sizing Object Name': None,
        'Supplemental Heating Coil Name': [optional_name(x.supplementalHeatingCoil()) for x in all_zone_hvac_vrfs],
        'Maximum Supply Air Temperature from Supplemental Heater {C}': ['Autosize' if x.isMaximumSupplyAirTemperaturefromSupplementalHeaterAutosized() else opt(x.maximumSupplyAirTemperaturefromSupplementalHeater()) for x in all_zone_hvac_vrfs],
        'Maximum Outdoor Dry-Bulb Temperature for Supplemental Heater Operation {C}': [x.maximumOutdoorDryBulbTemperatureforSupplementalHeaterOperation() for x in all_zone_hvac_vrfs]
        }
                       
    # Create a DataFrame of all thermal zones.
    all_zone_hvac_vrfs_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_zone_hvac_vrfs_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_zone_hvac_vrfs_df = all_zone_hvac_vrfs_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    logger.info(
        f"The OSM model contains {all_zone_hvac_vrfs_df.shape[0]} thermal zones")

    return all_zone_hvac_vrfs_df


AIR_TERMINAL_SINGLE_DUCT_PARALLEL_PIU_REHEAT_COLUMNS = (
    'Handle',
    'Name',
    'Availability Schedule Name',
    'Maximum Primary Air Flow Rate {m3/s}',
    'Maximum Secondary Air Flow Rate {m3/s}',
    'Minimum Primary Air Flow Fraction',
    'Fan On Flow Fraction',
    'Supply Air Inlet Node Name',
    'Secondary Air Inlet Node Name',
    'Outlet Node Name',
    'Reheat Coil Air Inlet Node Name',
    'Zone Mixer Name',
    'Fan Name',
    'Reheat Coil Name',
    'Maximum Hot Water or Steam Flow Rate {m3/s}',
    'Minimum Hot Water or Steam Flow Rate {m3/s}',
    'Convergence Tolerance',
)

def get_air_terminal_single_duct_parallel_piu_reheat_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None) -> dict:
    if handle is not None and name is not None:
        raise ValueError(
            "Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError(
            "Either 'handle' or 'name' must be provided.")

    if handle is not None:
        osm_object = osm_model.getAirTerminalSingleDuctParallelPIUReheat(
            handle)
        if not osm_object:
            logger.warning(
                f"No air terminal single duct parallel PIU reheat object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getAirTerminalSingleDuctParallelPIUReheatByName(
            name)
        if not osm_object:
            logger.warning(
                f"No air terminal single duct parallel PIU reheat object found with the name: {name}")
            return {}

    target_object = opt(osm_object)

    object_dict = {
                  'Handle': str(target_object.handle()),
                  'Name': opt(target_object.name()) if target_object.name().is_initialized() else None,
                  'Availability Schedule Name': opt(target_object.availabilitySchedule().name()) if target_object.availabilitySchedule().name().is_initialized() else None,
                  'Maximum Primary Air Flow Rate {m3/s}': opt(target_object.maximumPrimaryAirFlowRate()) if not target_object.isMaximumPrimaryAirFlowRateAutosized() else 'Autosize',
                  'Maximum Secondary Air Flow Rate {m3/s}': opt(target_object.maximumSecondaryAirFlowRate()) if not target_object.isMaximumSecondaryAirFlowRateAutosized() else 'Autosize',
                  'Minimum Primary Air Flow Fraction': opt(target_object.minimumPrimaryAirFlowFraction()) if not target_object.isMinimumPrimaryAirFlowFractionAutosized() else 'Autosize',                  
                  'Fan On Flow Fraction': opt(target_object.fanOnFlowFraction()) if not target_object.isFanOnFlowFractionAutosized() else 'Autosize',
                  'Supply Air Inlet Node Name': opt(target_object.inletModelObject()).nameString() if target_object.inletModelObject().is_initialized() else None,
                  'Secondary Air Inlet Node Name': opt(target_object.secondaryAirInletNode()).nameString() if target_object.secondaryAirInletNode().is_initialized() else None,                  
                  'Outlet Node Name': opt(target_object.outletModelObject()).nameString() if target_object.outletModelObject().is_initialized() else None,                
                  'Reheat Coil Air Inlet Node Name': None,
                  'Zone Mixer Name': None,
                  'Fan Name': target_object.fan().nameString(),
                  'Reheat Coil Name': target_object.reheatCoil().nameString(),
                  'Maximum Hot Water or Steam Flow Rate {m3/s}': opt(target_object.maximumHotWaterorSteamFlowRate()) if not target_object.isMaximumHotWaterorSteamFlowRateAutosized() else 'Autosize',
                  'Minimum Hot Water or Steam Flow Rate {m3/s}': target_object.minimumHotWaterorSteamFlowRate(),
                  'Convergence Tolerance': target_object.convergenceTolerance()
    }

    return object_dict

def get_all_air_terminal_single_duct_parallel_piu_reheat_objects_as_dict(osm_model: openstudio.model.Model) -> list[dict[str, Any]]:
    """
    Retrieve attributes for all OS:AirTerminal:SingleDuct:ParallelPIU:Reheat objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing air terminal attributes.
    """

    # Get all spaces in the OpenStudio model.
    all_objects = osm_model.getAirTerminalSingleDuctParallelPIUReheats()

    all_objects_dicts = []

    for target_object in all_objects:
        space_handle = str(target_object.handle())
        object_dict = get_air_terminal_single_duct_parallel_piu_reheat_object_as_dict(osm_model, space_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_air_terminal_single_duct_parallel_piu_reheat_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:AirTerminal:SingleDuct:ParallelPIU:Reheat objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all air terminal attributes.
    """

    all_objects_dicts = get_all_air_terminal_single_duct_parallel_piu_reheat_objects_as_dict(osm_model)

    return build_dataframe(
        all_objects_dicts, "AirTerminal:SingleDuct:ParallelPIU:Reheat", sort_by="Name",
        columns=AIR_TERMINAL_SINGLE_DUCT_PARALLEL_PIU_REHEAT_COLUMNS)

#------------------------
#--- ZoneHVAC:UnitHeater
#------------------------

ZONE_HVAC_UNIT_HEATER_COLUMNS = (
    'Handle',
    'Name',
    'Availability Schedule Name',
    'Air Inlet Node Name',
    'Air Outlet Node Name',
    'Supply Air Fan Name',
    'Maximum Supply Air Flow Rate {m3/s}',
    'Fan Control Type',
    'Heating Coil Name',
    'Maximum Hot Water Flow Rate {m3/s}',
    'Minimum Hot Water Flow Rate {m3/s}',
    'Heating Convergence Tolerance',
    'Availability Manager List Name',
)

def get_zone_hvac_unit_heater_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: str | None = None, 
    name: str | None = None
) -> dict[str, Any]:
    """
    Retrieve attributes of an OS:ZoneHVAC:UnitHeater object from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.

    Returns:
    - Dict[str, Any]: A dictionary containing unit heater attributes.
    """
    if handle is not None and name is not None:
        raise ValueError(
            "Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError(
            "Either 'handle' or 'name' must be provided.")

    if handle is not None:
        osm_object = osm_model.getZoneHVACUnitHeater(handle)
        if not osm_object:
            logger.warning(
                f"No Zone HVAC Unit Heater object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getZoneHVACUnitHeaterByName(name)
        if not osm_object:
            logger.warning(
                f"No Zone HVAC Unit Heater object found with the name: {name}")
            return {}

    target_object = opt(osm_object)

    object_dict = {
                  'Handle': str(target_object.handle()),
                  'Name': opt(target_object.name()) if target_object.name().is_initialized() else None,
                  'Availability Schedule Name': related_name(target_object, "Availability Schedule Name"),
                  'Air Inlet Node Name': optional_name(target_object.inletNode()),
                  'Air Outlet Node Name': optional_name(target_object.outletNode()),
                  'Supply Air Fan Name': related_name(target_object, "Supply Air Fan Name"),
                  'Maximum Supply Air Flow Rate {m3/s}': opt(target_object.maximumSupplyAirFlowRate()) if not target_object.isMaximumSupplyAirFlowRateAutosized() else 'Autosize',                  
                  'Fan Control Type': target_object.fanControlType(),
                  'Heating Coil Name': related_name(target_object, "Heating Coil Name"),
                  'Maximum Hot Water Flow Rate {m3/s}': opt(target_object.maximumHotWaterFlowRate()) if not target_object.isMaximumHotWaterFlowRateAutosized() else 'Autosize',
                  'Minimum Hot Water Flow Rate {m3/s}': target_object.minimumHotWaterFlowRate(),
                  'Heating Convergence Tolerance': target_object.heatingConvergenceTolerance(),
                  'Availability Manager List Name': None
    }

    return object_dict

def get_all_zone_hvac_unit_heater_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict[str, Any]]:
    """
    Retrieve attributes for all OS:ZoneHVAC:UnitHeater objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing unit heater attributes.
    """

    # Get all spaces in the OpenStudio model.
    all_objects = osm_model.getZoneHVACUnitHeaters()

    all_objects_dicts = []

    for target_object in all_objects:
        space_handle = str(target_object.handle())
        object_dict = get_zone_hvac_unit_heater_object_as_dict(osm_model, space_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts

def get_all_zone_hvac_unit_heater_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:ZoneHVAC:UnitHeater objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all unit heater attributes.
    """

    all_objects_dicts = get_all_zone_hvac_unit_heater_objects_as_dicts(osm_model)

    return build_dataframe(
        all_objects_dicts, "ZoneHVAC:UnitHeater", sort_by="Name",
        columns=ZONE_HVAC_UNIT_HEATER_COLUMNS)

#-------------------------------
#--- OS:ZoneHVAC:FourPipeFanCoil
#-------------------------------

FOUR_PIPE_FAN_COIL_COLUMNS = (
    'Handle',
    'Name',
    'Availability Schedule Name',
    'Capacity Control Method',
    'Maximum Supply Air Flow Rate {m3/s}',
    'Low Speed Supply Air Flow Ratio',
    'Medium Speed Supply Air Flow Ratio',
    'Maximum Outdoor Air Flow Rate {m3/s}',
    'Outdoor Air Schedule Name',
    'Air Inlet Node Name',
    'Air Outlet Node Name',
    'Outdoor Air Mixer Object Type',
    'Outdoor Air Mixer Name',
    'Supply Air Fan Name',
    'Cooling Coil Name',
    'Maximum Cold Water Flow Rate {m3/s}',
    'Minimum Cold Water Flow Rate {m3/s}',
    'Cooling Convergence Tolerance',
    'Heating Coil Name',
    'Maximum Hot Water Flow Rate {m3/s}',
    'Minimum Hot Water Flow Rate {m3/s}',
    'Heating Convergence Tolerance',
    'Supply Air Fan Operating Mode Schedule Name',
    'Minimum Supply Air Temperature in Cooling Mode {C}',
    'Maximum Supply Air Temperature in Heating Mode {C}',
)

def get_four_pipe_fan_coil_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: str | None = None, 
    name: str | None = None
) -> dict[str, Any]:
    """
    Retrieve attributes of an OS:ZoneHVAC:FourPipeFanCoil object from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.

    Returns:
    - Dict[str, Any]: A dictionary containing fan coil attributes.
    """
    if handle is not None and name is not None:
        raise ValueError(
            "Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError(
            "Either 'handle' or 'name' must be provided.")

    if handle is not None:
        osm_object = osm_model.getZoneHVACFourPipeFanCoil(handle)
        if not osm_object:
            logger.warning(
                f"No ZoneHVAC:FourPipeFanCoil object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getZoneHVACFourPipeFanCoilByName(name)
        if not osm_object:
            logger.warning(
                f"No ZoneHVAC:FourPipeFanCoil object found with the name: {name}")
            return {}

    target_object = opt(osm_object)
    object_dict = {
        'Handle': str(target_object.handle()),
                  'Name': opt(target_object.name()) if target_object.name().is_initialized() else None,
                  'Availability Schedule Name': opt(target_object.availabilitySchedule().name()) if target_object.availabilitySchedule().name().is_initialized() else None,
                  'Capacity Control Method': target_object.capacityControlMethod(),
                  'Maximum Supply Air Flow Rate {m3/s}': opt(target_object.maximumSupplyAirFlowRate()) if not target_object.isMaximumSupplyAirFlowRateAutosized() else 'autosize',                  
                  'Low Speed Supply Air Flow Ratio': target_object.lowSpeedSupplyAirFlowRatio(),
                  'Medium Speed Supply Air Flow Ratio': target_object.mediumSpeedSupplyAirFlowRatio(),                  
                  'Maximum Outdoor Air Flow Rate {m3/s}': opt(target_object.maximumOutdoorAirFlowRate()) if not target_object.isMaximumOutdoorAirFlowRateAutosized() else 'autosize',
                  'Outdoor Air Schedule Name': optional_name(target_object.outdoorAirSchedule()),
                  'Air Inlet Node Name': optional_name(target_object.inletNode()),
                  'Air Outlet Node Name': optional_name(target_object.outletNode()),
                  'Outdoor Air Mixer Object Type': target_object.outdoorAirMixerObjectType(),
                  'Outdoor Air Mixer Name': target_object.outdoorAirMixerName(),
                  'Supply Air Fan Name': related_name(target_object, "Supply Air Fan Name"),
                  'Cooling Coil Name': related_name(target_object, "Cooling Coil Name"),
                  'Maximum Cold Water Flow Rate {m3/s}': opt(target_object.maximumColdWaterFlowRate()) if not target_object.isMaximumColdWaterFlowRateAutosized() else 'autosize',
                  'Minimum Cold Water Flow Rate {m3/s}': target_object.minimumColdWaterFlowRate(),
                  'Cooling Convergence Tolerance': target_object.coolingConvergenceTolerance(),
                  'Heating Coil Name': related_name(target_object, "Heating Coil Name"),
                  'Maximum Hot Water Flow Rate {m3/s}': opt(target_object.maximumHotWaterFlowRate()) if not target_object.isMaximumHotWaterFlowRateAutosized() else 'autosize',
                  'Minimum Hot Water Flow Rate {m3/s}': target_object.minimumHotWaterFlowRate(),
                  'Heating Convergence Tolerance': target_object.heatingConvergenceTolerance(),
                  'Supply Air Fan Operating Mode Schedule Name': None,
                  'Minimum Supply Air Temperature in Cooling Mode {C}': opt(target_object.minimumSupplyAirTemperatureInCoolingMode()) if not target_object.isMinimumSupplyAirTemperatureInCoolingModeAutosized() else 'autosize',
                  'Maximum Supply Air Temperature in Heating Mode {C}': opt(target_object.maximumSupplyAirTemperatureInHeatingMode()) if not target_object.isMaximumSupplyAirTemperatureInHeatingModeAutosized() else 'autosize'
              }

    return object_dict

def get_all_four_pipe_fan_coil_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict[str, Any]]:
    """
    Retrieve attributes for all OS:ZoneHVAC:FourPipeFanCoil objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing fan coil attributes.
    """

    # Get all ZoneHVAC:FourPipeFanCoil objects in the OpenStudio model.
    all_objects = osm_model.getZoneHVACFourPipeFanCoils()

    all_objects_dicts = []

    for target_object in all_objects:
        object_handle = str(target_object.handle())
        object_dict = get_four_pipe_fan_coil_object_as_dict(osm_model, object_handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts

def get_all_four_pipe_fan_coil_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:ZoneHVAC:FourPipeFanCoil objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all fan coil attributes.
    """

    all_objects_dicts = get_all_four_pipe_fan_coil_objects_as_dicts(osm_model)

    return build_dataframe(
        all_objects_dicts, "ZoneHVAC:FourPipeFanCoil", sort_by="Name",
        columns=FOUR_PIPE_FAN_COIL_COLUMNS)
