import openstudio
import pandas as pd


def get_all_thermal_zone_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all thermal zones from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all thermal zones.
    """

    all_thermal_zones = osm_model.getThermalZones()

    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_thermal_zones],
        'Name': [x.name().get() for x in all_thermal_zones],
        'Multiplier': [x.multiplier() for x in all_thermal_zones],
        'Ceiling Height {m}': None,
        'Volume {m3}': [x.airVolume() for x in all_thermal_zones],
        'Floor Area {m2}': [x.floorArea() for x in all_thermal_zones],
        'Zone Inside Convection Algorithm': None,
        'Zone Outside Convection Algorithm': None,
        'Zone Conditioning Equipment List Name': [x.zoneConditioningEquipmentListName() for x in all_thermal_zones],
        'Zone Air Inlet Port List': [str(x.inletPortList().handle()) if not x.inletPortList().handle().isNull() else None for x in all_thermal_zones],
        'Zone Air Exhaust Port List': [str(x.exhaustPortList().handle()) if not x.exhaustPortList().handle().isNull() else None for x in all_thermal_zones],
        'Zone Air Node Name': [x.zoneAirNode().name().get() if not x.zoneAirNode().handle().isNull() else None for x in all_thermal_zones],
        'Zone Return Air Port List': [str(x.returnPortList().handle()) if not x.returnPortList().handle().isNull() else None for x in all_thermal_zones],
        'Primary Daylighting Control Name': [x.primaryDaylightingControl().get().name().get() if not x.primaryDaylightingControl().isNull() else None for x in all_thermal_zones],
        'Fraction of Zone Controlled by Primary Daylighting Control': None,
        'Secondary Daylighting Control Name': None,
        'Fraction of Zone Controlled by Secondary Daylighting Control': None,
        'Illuminance Map Name': None,
        'Group Rendering Name': None,
        'Thermostat Name': [x.thermostat().get().name().get() if not x.thermostat().get().handle().isNull() else None for x in all_thermal_zones],
        'Use Ideal Air Loads': [x.useIdealAirLoads() for x in all_thermal_zones],
        'Humidistat Name': None,
        'Daylighting Controls Availability Schedule Name': None
    }

    # Create a DataFrame of all thermal zones.
    all_thermal_zones_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_thermal_zones_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_thermal_zones_df = all_thermal_zones_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(
        f"The OSM model contains {all_thermal_zones_df.shape[0]} thermal zones")

    return all_thermal_zones_df