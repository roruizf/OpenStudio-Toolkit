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

def get_all_zone_hvac_equipment_list_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all zone HVAC Equipment List from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all thermal zones.
    """
    all_zone_hvac_equipment_lists = osm_model.getZoneHVACEquipmentLists()

    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_zone_hvac_equipment_lists],
        'Name': [x.name().get() for x in all_zone_hvac_equipment_lists],
        'Thermal Zone': [x.thermalZone().name().get() for x in all_zone_hvac_equipment_lists],
        'Load Distribution Scheme': [x.loadDistributionScheme() for x in all_zone_hvac_equipment_lists]
        }

    # Create a DataFrame of all thermal zones.
    all_zone_hvac_equipment_lists_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_zone_hvac_equipment_lists_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_zone_hvac_equipment_lists_df = all_zone_hvac_equipment_lists_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    # Get maximum number of zoneHVAC equipments
    zone_equipment_max = 0
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
      zone_hvac_equipment_list = osm_model.getZoneHVACEquipmentListByName(row['Name']).get()
      for i in range(len(zone_hvac_equipment_list.equipment())):
        all_zone_hvac_equipment_lists_df.loc[index, f'Zone Equipment {i+1}'] = zone_hvac_equipment_list.equipment()[i].name().get()
        all_zone_hvac_equipment_lists_df.loc[index, f'Zone Equipment Cooling Sequence {i+1}'] = zone_hvac_equipment_list.coolingPriority(zone_hvac_equipment_list.equipment()[i])
        all_zone_hvac_equipment_lists_df.loc[index, f'Zone Equipment Heating or No-Load Sequence {i+1}'] = zone_hvac_equipment_list.heatingPriority(zone_hvac_equipment_list.equipment()[i])
        all_zone_hvac_equipment_lists_df.loc[index, f'Zone Equipment Sequential Cooling Fraction Schedule Name {i+1}'] = zone_hvac_equipment_list.sequentialCoolingFractionSchedule(zone_hvac_equipment_list.equipment()[i]).get().name().get() if not zone_hvac_equipment_list.sequentialCoolingFractionSchedule(zone_hvac_equipment_list.equipment()[i]).isNull() else None
        all_zone_hvac_equipment_lists_df.loc[index, f'Zone Equipment Sequential Heating Fraction Schedule Name {i+1}'] = zone_hvac_equipment_list.sequentialHeatingFractionSchedule(zone_hvac_equipment_list.equipment()[i]).get().name().get() if not zone_hvac_equipment_list.sequentialHeatingFractionSchedule(zone_hvac_equipment_list.equipment()[i]).isNull() else None

    print(
        f"The OSM model contains {all_zone_hvac_equipment_lists_df.shape[0]} thermal zones")

    return all_zone_hvac_equipment_lists_df



def get_all_zone_hvac_terminal_unit_variant_refrigerant_flow_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all zone HVAC Variant Refrigerant Flow from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all thermal zones.
    """

    all_zone_hvac_vrfs = osm_model.getZoneHVACTerminalUnitVariableRefrigerantFlows()

    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_zone_hvac_vrfs],
        'Name': [x.name().get() for x in all_zone_hvac_vrfs],
        'Terminal Unit Availability schedule': [x.terminalUnitAvailabilityschedule().name() for x in all_zone_hvac_vrfs],
        'Terminal Unit Air Inlet Node': None,
        'Terminal Unit Air Outlet Node': None,
        'Supply Air Flow Rate During Cooling Operation {m3/s}': [x.supplyAirFlowRateDuringCoolingOperation().get() if not x.supplyAirFlowRateDuringCoolingOperation().isNull() else None for x in all_zone_hvac_vrfs],
        'Supply Air Flow Rate When No Cooling is Needed {m3/s}': [x.supplyAirFlowRateWhenNoCoolingisNeeded().get() if not x.supplyAirFlowRateWhenNoCoolingisNeeded().isNull() else None for x in all_zone_hvac_vrfs],
        'Supply Air Flow Rate During Heating Operation {m3/s}': [x.supplyAirFlowRateDuringHeatingOperation().get() if not x.supplyAirFlowRateDuringHeatingOperation().isNull() else None for x in all_zone_hvac_vrfs],
        'Supply Air Flow Rate When No Heating is Needed {m3/s}': [x.supplyAirFlowRateWhenNoHeatingisNeeded().get() if not x.supplyAirFlowRateWhenNoHeatingisNeeded().isNull() else None for x in all_zone_hvac_vrfs],
        'Outdoor Air Flow Rate During Cooling Operation {m3/s}': [x.outdoorAirFlowRateDuringCoolingOperation().get() if not x.outdoorAirFlowRateDuringCoolingOperation().isNull() else None for x in all_zone_hvac_vrfs],
        'Outdoor Air Flow Rate During Heating Operation {m3/s}': [x.outdoorAirFlowRateDuringHeatingOperation().get() if not x.outdoorAirFlowRateDuringHeatingOperation().isNull() else None for x in all_zone_hvac_vrfs],
        'Outdoor Air Flow Rate When No Cooling or Heating is Needed {m3/s}': [x.outdoorAirFlowRateWhenNoCoolingorHeatingisNeeded().get() if not x.outdoorAirFlowRateWhenNoCoolingorHeatingisNeeded().isNull() else None for x in all_zone_hvac_vrfs],
        'Supply Air Fan Operating Mode Schedule': [x.supplyAirFanOperatingModeSchedule().name() if not x.supplyAirFanOperatingModeSchedule().name().isNull() else None for x in all_zone_hvac_vrfs],
        'Supply Air Fan Placement': [x.supplyAirFanPlacement() for x in all_zone_hvac_vrfs],
        'Supply Air Fan': [x.supplyAirFan().name().get() if not x.supplyAirFan().name().isNull() else None for x in all_zone_hvac_vrfs],
        'Outside Air Mixer': None,
        'Cooling Coil': [x.coolingCoil().get().name().get() if not x.coolingCoil().get().name().isNull() else None for x in all_zone_hvac_vrfs],
        'Heating Coil': [x.heatingCoil().get().name().get() if not x.heatingCoil().get().name().isNull() else None for x in all_zone_hvac_vrfs],
        'Zone Terminal Unit On Parasitic Electric Energy Use {W}': [x.zoneTerminalUnitOnParasiticElectricEnergyUse() for x in all_zone_hvac_vrfs],
        'Zone Terminal Unit Off Parasitic Electric Energy Use {W}': [x.zoneTerminalUnitOffParasiticElectricEnergyUse() for x in all_zone_hvac_vrfs],
        'Rated Total Heating Capacity Sizing Ratio {W/W}': [x.ratedTotalHeatingCapacitySizingRatio() for x in all_zone_hvac_vrfs],
        'Availability Manager List Name': None,
        'Design Specification ZoneHVAC Sizing Object Name': None,
        'Supplemental Heating Coil Name': [x.supplementalHeatingCoil().get().name() if not x.supplementalHeatingCoil().isNull() else None for x in all_zone_hvac_vrfs],
        'Maximum Supply Air Temperature from Supplemental Heater {C}': [x.maximumSupplyAirTemperaturefromSupplementalHeater() for x in all_zone_hvac_vrfs],
        'Maximum Outdoor Dry-Bulb Temperature for Supplemental Heater Operation {C}': [x.maximumOutdoorDryBulbTemperatureforSupplementalHeaterOperation() for x in all_zone_hvac_vrfs]
        }
                       
    # Create a DataFrame of all thermal zones.
    all_zone_hvac_vrfs_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_zone_hvac_vrfs_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_zone_hvac_vrfs_df = all_zone_hvac_vrfs_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(
        f"The OSM model contains {all_zone_hvac_vrfs_df.shape[0]} thermal zones")

    return all_zone_hvac_vrfs_df


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
        if osm_object is None:
            print(
                f"No air terminal single duct parallel PIU reheat object found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getAirTerminalSingleDuctParallelPIUReheatByName(
            name)
        if not osm_object:
            print(
                f"No air terminal single duct parallel PIU reheat object found with the name: {name}")
            return {}

    target_object = osm_object.get()

    object_dict = {
                  'Handle': str(target_object.handle()),
                  'Name': target_object.name().get() if target_object.name().is_initialized() else None,
                  'Availability Schedule Name': target_object.availabilitySchedule().name().get() if target_object.availabilitySchedule().name().is_initialized() else None,
                  'Maximum Primary Air Flow Rate {m3/s}': target_object.maximumPrimaryAirFlowRate().get() if not target_object.isMaximumPrimaryAirFlowRateAutosized() else 'Autosize',
                  'Maximum Secondary Air Flow Rate {m3/s}': target_object.maximumSecondaryAirFlowRate().get() if not target_object.isMaximumPrimaryAirFlowRateAutosized() else 'Autosize',
                  'Minimum Primary Air Flow Fraction': target_object.minimumPrimaryAirFlowFraction().get() if not target_object.isMinimumPrimaryAirFlowFractionAutosized() else 'Autosize',                  
                  'Fan On Flow Fraction': target_object.fanOnFlowFraction().get() if not target_object.isFanOnFlowFractionAutosized() else 'Autosize',
                  'Supply Air Inlet Node Name': target_object.inletModelObject().get().nameString() if target_object.inletModelObject().is_initialized() else None,
                  'Secondary Air Inlet Node Name': target_object.secondaryAirInletNode().get().nameString() if target_object.secondaryAirInletNode().is_initialized() else None,                  
                  'Outlet Node Name': target_object.outletModelObject().get().nameString() if target_object.outletModelObject().is_initialized() else None,                
                  'Reheat Coil Air Inlet Node Name': None,
                  'Zone Mixer Name': None,
                  'Fan Name': target_object.fan().nameString(),
                  'Reheat Coil Name': target_object.reheatCoil().nameString(),
                  'Maximum Hot Water or Steam Flow Rate {m3/s}': target_object.maximumHotWaterorSteamFlowRate() if not target_object.isMaximumHotWaterorSteamFlowRateAutosized() else 'Autosize',
                  'Minimum Hot Water or Steam Flow Rate {m3/s}': target_object.minimumHotWaterorSteamFlowRate(),
                  'Convergence Tolerance': target_object.convergenceTolerance()
    }

    return object_dict

def get_all_air_terminal_single_duct_parallel_piu_reheat_objects_as_dict(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all air terminal single duct parallel PIU reheat objects from the OpenStudio model 
    and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about an air terminal single duct parallel PIU reheat object.
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
    Retrieve all air terminal single duct parallel PIU reheat objects from the OpenStudio model 
    and return their attributes as a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all air terminal single duct parallel PIU reheat objects.
    """

    all_objects_dicts = get_all_air_terminal_single_duct_parallel_piu_reheat_objects_as_dict(osm_model)

    # Create a DataFrame of all air terminal single duct parallel PIU reheat objects.
    all_air_terminals_df = pd.DataFrame(all_objects_dicts)

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_air_terminals_df = all_air_terminals_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(f"The OSM model contains {all_air_terminals_df.shape[0]} air terminal single duct parallel PIU reheat objects")

    return all_air_terminals_df