import openstudio
import pandas as pd
import logging
from typing import List, Dict, Any, Optional

from openstudio_toolkit.utils import helpers

# Configure logger
logger = logging.getLogger(__name__)

# --------------------------------------------------
#  ***** OS:ThermalZone ****************************
# --------------------------------------------------

def get_thermal_zone_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: Optional[str] = None, 
    name: Optional[str] = None, 
    _object_ref: Optional[openstudio.model.ThermalZone] = None
) -> Dict[str, Any]:
    """
    Retrieve attributes of an OS:ThermalZone from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.ThermalZone, optional): Direct object reference.

    Returns:
    - Dict[str, Any]: A dictionary containing thermal zone attributes.
    """
    target_object = helpers.fetch_object(
        osm_model, "ThermalZone", handle, name, _object_ref)

    if target_object is None:
        return {}

    return {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else "Unnamed Thermal Zone",
        'Multiplier': target_object.multiplier(),
        'Ceiling Height {m}': target_object.ceilingHeight().get() if target_object.ceilingHeight().is_initialized() else None,
        'Volume {m3}': target_object.airVolume(),
        'Floor Area {m2}': target_object.floorArea(),        
        'Zone Inside Convection Algorithm': target_object.zoneInsideConvectionAlgorithm().get() if target_object.zoneInsideConvectionAlgorithm().is_initialized() else None,
        'Zone Outside Convection Algorithm': target_object.zoneOutsideConvectionAlgorithm().get() if target_object.zoneOutsideConvectionAlgorithm().is_initialized() else None,
        'Zone Conditioning Equipment List Name': target_object.zoneConditioningEquipmentListName(),
        'Zone Air Inlet Port List Handle': str(target_object.inletPortList().handle()) if target_object.inletPortList().handle() else None,
        'Zone Air Exhaust Port List Handle': str(target_object.exhaustPortList().handle()) if target_object.exhaustPortList().handle() else None,
        'Zone Air Node Name': target_object.zoneAirNode().name().get() if target_object.zoneAirNode().name().is_initialized() else None,
        'Zone Return Air Port List Handle': str(target_object.returnPortList().handle()) if target_object.returnPortList().handle() else None,
        'Primary Daylighting Control Name': target_object.primaryDaylightingControl().get().name().get() if (target_object.primaryDaylightingControl().is_initialized() and target_object.primaryDaylightingControl().get().name().is_initialized()) else None,
        'Fraction of Zone Controlled by Primary Daylighting Control': target_object.fractionofZoneControlledbyPrimaryDaylightingControl(),
        'Secondary Daylighting Control Name': target_object.secondaryDaylightingControl().get().name().get() if (target_object.secondaryDaylightingControl().is_initialized() and target_object.secondaryDaylightingControl().get().name().is_initialized()) else None,
        'Fraction of Zone Controlled by Secondary Daylighting Control': target_object.fractionofZoneControlledbySecondaryDaylightingControl(),
        'Illuminance Map Name': target_object.illuminanceMap().get().name().get() if (target_object.illuminanceMap().is_initialized() and target_object.illuminanceMap().get().name().is_initialized()) else None,
        'Group Rendering Name': target_object.renderingColor().get().name().get() if (target_object.renderingColor().is_initialized() and target_object.renderingColor().get().name().is_initialized()) else None,
        'Thermostat Name': target_object.thermostat().get().name().get() if(target_object.thermostat().is_initialized() and target_object.thermostat().get().name().is_initialized()) else None,
        'Use Ideal Air Loads': target_object.useIdealAirLoads(),
        'Humidistat Name': target_object.zoneControlHumidistat().get().name().get() if target_object.zoneControlHumidistat().is_initialized() else None,
        'Daylighting Controls Availability Schedule Name': target_object.daylightingControlsAvailabilitySchedule().get().name().get() if target_object.daylightingControlsAvailabilitySchedule().is_initialized() else None
    }

def get_all_thermal_zones_objects_as_dicts(osm_model: openstudio.model.Model) -> List[Dict[str, Any]]:
    """
    Retrieve attributes for all OS:ThermalZone objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing thermal zone attributes.
    """
    all_objects = osm_model.getThermalZones()
    return [get_thermal_zone_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_thermal_zones_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:ThermalZone objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all ThermalZone attributes.
    """
    all_objects_dicts = get_all_thermal_zones_objects_as_dicts(osm_model)
    df = pd.DataFrame(all_objects_dicts)

    if not df.empty and 'Name' in df.columns:
        df = df.sort_values(by='Name', ascending=True).reset_index(drop=True)

    logger.info(f"Retrieved {len(df)} ThermalZone objects from the model.")
    return df