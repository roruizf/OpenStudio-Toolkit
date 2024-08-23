import openstudio
import pandas as pd


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
    # Get maximum number of zoneHVAC equipments
    zone_equipment_max = 0
    for zone_hvac_equipment_list in all_zone_hvac_equipment_lists:
        num_elements = len(zone_hvac_equipment_list.equipment())
        if num_elements > zone_equipment_max:
            zone_equipment_max = num_elements

    # Add columns for each zone HVAC equipment
    for i in range(zone_equipment_max):
      object_attr[f'Zone Equipment {i+1}'] = [x.equipment()[i].name().get() for x in all_zone_hvac_equipment_lists]
      object_attr[f'Zone Equipment Cooling Sequence {i+1}'] = [x.coolingPriority(x.equipment()[i]) for x in all_zone_hvac_equipment_lists]
      object_attr[f'Zone Equipment Heating or No-Load Sequence {i+1}'] = [x.heatingPriority(x.equipment()[i]) for x in all_zone_hvac_equipment_lists]
      object_attr[f'Zone Equipment Sequential Cooling Fraction Schedule Name {i+1}'] = [x.sequentialCoolingFractionSchedule(x.equipment()[i]).get().name().get() if not x.sequentialCoolingFractionSchedule(x.equipment()[i]).isNull() else None for x in all_zone_hvac_equipment_lists]
      object_attr[f'Zone Equipment Sequential Heating Fraction Schedule Name {i+1}'] = [x.sequentialHeatingFractionSchedule(x.equipment()[i]).get().name().get() if not x.sequentialHeatingFractionSchedule(x.equipment()[i]).isNull() else None for x in all_zone_hvac_equipment_lists]

    # Create a DataFrame of all thermal zones.
    all_zone_hvac_equipment_lists_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_zone_hvac_equipment_lists_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_zone_hvac_equipment_lists_df = all_zone_hvac_equipment_lists_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

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
        'Terminal Unit Availability schedule': None,
        'Terminal Unit Air Inlet Node': None,
        'Terminal Unit Air Outlet Node': None,
        'Supply Air Flow Rate During Cooling Operation {m3/s}': [x.supplyAirFlowRateDuringCoolingOperation().get() if not x.supplyAirFlowRateDuringCoolingOperation().isNull() else None for x in all_zone_hvac_vrfs],
        'Supply Air Flow Rate When No Cooling is Needed {m3/s}': [x.supplyAirFlowRateWhenNoCoolingisNeeded().get() if not x.supplyAirFlowRateWhenNoCoolingisNeeded().isNull() else None for x in all_zone_hvac_vrfs],
        'Supply Air Flow Rate During Heating Operation {m3/s}': [x.supplyAirFlowRateDuringHeatingOperation().get() if not x.supplyAirFlowRateDuringHeatingOperation().isNull() else None for x in all_zone_hvac_vrfs],
        'Supply Air Flow Rate When No Heating is Needed {m3/s}': [x.supplyAirFlowRateWhenNoHeatingisNeeded().get() if not x.supplyAirFlowRateWhenNoHeatingisNeeded().isNull() else None for x in all_zone_hvac_vrfs],
        'Outdoor Air Flow Rate During Cooling Operation {m3/s}': [x.outdoorAirFlowRateDuringCoolingOperation().get() if not x.outdoorAirFlowRateDuringCoolingOperation().isNull() else None for x in all_zone_hvac_vrfs],
        'Outdoor Air Flow Rate During Heating Operation {m3/s}': [x.outdoorAirFlowRateDuringHeatingOperation().get() if not x.outdoorAirFlowRateDuringHeatingOperation().isNull() else None for x in all_zone_hvac_vrfs],
        'Outdoor Air Flow Rate When No Cooling or Heating is Needed {m3/s}': [x.outdoorAirFlowRateWhenNoCoolingorHeatingisNeeded().get() if not x.outdoorAirFlowRateWhenNoCoolingorHeatingisNeeded().isNull() else None for x in all_zone_hvac_vrfs],
        'Supply Air Fan Operating Mode Schedule': None,
        'Supply Air Fan Placement': None,
        'Supply Air Fan': [x.supplyAirFan().name().get() if not x.supplyAirFan().name().isNull() else None for x in all_zone_hvac_vrfs],
        'Outside Air Mixer': None,
        'Cooling Coil': [x.coolingCoil().get().name().get() if not x.coolingCoil().get().name().isNull() else None for x in all_zone_hvac_vrfs],
        'Heating Coil': [x.heatingCoil().get().name().get() if not x.heatingCoil().get().name().isNull() else None for x in all_zone_hvac_vrfs],
        'Zone Terminal Unit On Parasitic Electric Energy Use {W}': None,
        'Zone Terminal Unit Off Parasitic Electric Energy Use {W}': None,
        'Rated Total Heating Capacity Sizing Ratio {W/W}': None,
        'Availability Manager List Name': None,
        'Design Specification ZoneHVAC Sizing Object Name': None,
        'Supplemental Heating Coil Name': None,
        'Maximum Supply Air Temperature from Supplemental Heater {C}': None,
        'Maximum Outdoor Dry-Bulb Temperature for Supplemental Heater Operation {C}': None
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