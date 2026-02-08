import logging
from typing import Any

import openstudio
import pandas as pd

from openstudio_toolkit.utils import helpers

# Configure logger
logger = logging.getLogger(__name__)

# --------------------------------------------------
#  ***** OS:ThermalZone ****************************
# --------------------------------------------------

def get_thermal_zone_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: str | None = None, 
    name: str | None = None, 
    _object_ref: openstudio.model.ThermalZone | None = None
) -> dict[str, Any]:
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
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Multiplier': target_object.multiplier(),
        'Ceiling Height {m}': target_object.ceilingHeight().get() if target_object.ceilingHeight().is_initialized() else None,
        'Volume {m3}': target_object.airVolume(),
        'Floor Area {m2}': target_object.floorArea(),        
        'Zone Inside Convection Algorithm': target_object.zoneInsideConvectionAlgorithm().get() if target_object.zoneInsideConvectionAlgorithm().is_initialized() else None,
        'Zone Outside Convection Algorithm': target_object.zoneOutsideConvectionAlgorithm().get() if target_object.zoneOutsideConvectionAlgorithm().is_initialized() else None,
        'Zone Conditioning Equipment List Name': target_object.zoneConditioningEquipmentListName(),
        'Zone Air Inlet Port List': str(target_object.inletPortList().handle()) if target_object.inletPortList().handle() else None,
        'Zone Air Exhaust Port List': str(target_object.exhaustPortList().handle()) if target_object.exhaustPortList().handle() else None,
        'Zone Air Node Name': target_object.zoneAirNode().name().get() if target_object.zoneAirNode().name().is_initialized() else None,
        'Zone Return Air Port List': str(target_object.returnPortList().handle()) if target_object.returnPortList().handle() else None,
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

def get_all_thermal_zones_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict[str, Any]]:
    """
    Retrieve attributes for all OS:ThermalZone objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing thermal zone attributes.
    """
    from openstudio_toolkit.osm_objects._base import build_all_dicts
    return build_all_dicts(osm_model, "getThermalZones", get_thermal_zone_object_as_dict)

def get_all_thermal_zones_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:ThermalZone objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all ThermalZone attributes.
    """
    from openstudio_toolkit.osm_objects._base import build_dataframe
    return build_dataframe(get_all_thermal_zones_objects_as_dicts(osm_model), "ThermalZone")


def assign_spaces_to_thermal_zones(osm_model: openstudio.model.Model, 
                                   mapping_data: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Assign Thermal Zones to specific Spaces.
    
    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - mapping_data (List[Dict[str, Any]]): List of dictionaries defining the assignment.
        Each dictionary should contain:
        - 'Space Identifier': Handle (preferred) or Name of the space.
        - 'Thermal Zone Identifier': Handle (preferred) or Name of the zone.
        
        (Backward compatibility: 'Space Handle', 'Space Name', 'Thermal Zone Handle', 'Thermal Zone Name' also accepted)
        
    Returns:
    - Dict[str, Any]: Status dictionary with keys:
        - 'status': 'SUCCESS', 'PARTIAL_SUCCESS', or 'ERROR'
        - 'assigned_count': Number of spaces successfully assigned
        - 'errors': Number of failed assignments
        - 'messages': List of warning/error messages
    """
    assigned_count = 0
    errors = 0
    messages = []
    
    logger.info("Starting task: Assign Spaces to Thermal Zones...")
    
    for entry in mapping_data:
        # 1. Identify Space
        # Check generalized 'Identifier' key first, then fallbacks
        space_id = entry.get('Space Identifier')
        space_handle = space_id if space_id else entry.get('Space Handle')
        space_name = space_id if space_id else entry.get('Space Name')
        
        # When using generic fetch, pass ID to both handle/name args or let fetch handle ambiguity?
        # Helpers.fetch_object tries handle first. If ID is a string, passing it to both is safe
        # IF it's not a UUID, toUUID checks usually fail/return None, then it tries Name.
        
        space_obj = helpers.fetch_object(osm_model, "Space", space_handle, space_name)
        
        if not space_obj:
            identifier = space_handle if space_handle else space_name
            msg = f"Skipping entry: Space '{identifier}' not found."
            logger.warning(msg)
            messages.append(msg)
            errors += 1
            continue
            
        # 2. Identify Thermal Zone
        zone_id = entry.get('Thermal Zone Identifier')
        zone_handle = zone_id if zone_id else entry.get('Thermal Zone Handle')
        zone_name = zone_id if zone_id else entry.get('Thermal Zone Name')
        
        zone_obj = helpers.fetch_object(osm_model, "ThermalZone", zone_handle, zone_name)
        
        if not zone_obj:
            identifier = zone_handle if zone_handle else zone_name
            msg = f"Skipping entry: Thermal Zone '{identifier}' not found for space '{space_obj.nameString()}'."
            logger.warning(msg)
            messages.append(msg)
            errors += 1
            continue
            
        # 3. Assign
        # Note: OpenStudio Space.setThermalZone() takes the zone object
        try:
            success = space_obj.setThermalZone(zone_obj)
            if success:
                assigned_count += 1
            else:
                msg = f"Failed to assign Thermal Zone '{zone_obj.nameString()}' to Space '{space_obj.nameString()}'. Internal OS error."
                logger.warning(msg)
                messages.append(msg)
                errors += 1
        except Exception as e:
            msg = f"Exception assigning Thermal Zone to Space '{space_obj.nameString()}': {str(e)}"
            logger.error(msg)
            messages.append(msg)
            errors += 1
            
    # 4. Determine Status
    if errors == 0 and assigned_count > 0:
        status = "SUCCESS"
    elif errors > 0 and assigned_count > 0:
        status = "PARTIAL_SUCCESS"
    elif errors > 0 and assigned_count == 0:
        status = "ERROR"
    else:
        status = "SUCCESS" # Empty list or no action needed
        
    summary_msg = f"Finished assignment. Assigned: {assigned_count}, Errors: {errors}."
    logger.info(summary_msg)
    
    return {
        "status": status,
        "assigned_count": assigned_count,
        "errors": errors,
        "messages": messages
    }


def update_thermal_zones_data(osm_model: openstudio.model.Model, 
                              zones_data: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Batch update attributes of Thermal Zones.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - zones_data (List[Dict[str, Any]]): List of dictionaries containing data to update.
        Each dictionary should contain:
        - 'Thermal Zone Identifier': Handle (preferred) or Name of the zone.
        
        Optional attributes to update:
        - 'Name': New name.
        - 'Multiplier': Integer values (e.g. 1, 2, 10).        
        - 'Thermostat Name': Name of the Thermostat object to assign.
        - 'Humidistat Name': Name of the Humidistat object to assign.
        - 'Use Ideal Air Loads': Boolean.

    Returns:
    - Dict[str, Any]: Status dictionary.
    """
    updated_count = 0
    errors = 0
    messages = []
    
    logger.info("Starting batch update of Thermal Zones...")

    for entry in zones_data:
        # 1. Identify Zone
        zone_id = entry.get('Thermal Zone Identifier')
        zone_handle = zone_id if zone_id else entry.get('Handle') # Support generic 'Handle' key too
        zone_name = zone_id if zone_id else entry.get('Name')     # Support generic 'Name' key too
        
        if not zone_handle and not zone_name:
             # Try generic 'Thermal Zone Handle' / 'Thermal Zone Name'
             zone_handle = entry.get('Thermal Zone Handle')
             zone_name = entry.get('Thermal Zone Name')

        target_zone = helpers.fetch_object(osm_model, "ThermalZone", zone_handle, zone_name)
        
        if not target_zone:
            identifier = zone_handle if zone_handle else zone_name
            msg = f"Skipping entry: Thermal Zone '{identifier}' not found."
            logger.warning(msg)
            messages.append(msg)
            errors += 1
            continue
            
        changes_made = False
        
        # 2. Update Name
        if 'Name' in entry and entry['Name'] and entry['Name'] != target_zone.name().get():
             target_zone.setName(str(entry['Name']))
             changes_made = True

        # 3. Update Simple Attributes
        if 'Multiplier' in entry and entry['Multiplier'] is not None:
            try:
                target_zone.setMultiplier(int(entry['Multiplier']))
                changes_made = True
            except Exception:
                messages.append(f"Invalid multiplier value for zone {target_zone.nameString()}")        

        if 'Use Ideal Air Loads' in entry and entry['Use Ideal Air Loads'] is not None:
             target_zone.setUseIdealAirLoads(bool(entry['Use Ideal Air Loads']))
             changes_made = True

        # 4. Update Relationships (Thermostat/Humidistat)
        if 'Thermostat Name' in entry:
            tstat_name = entry['Thermostat Name']
            if tstat_name:
                # Need to find the Thermostat object. 
                # Identifying rigid type is hard (could be ZoneControlThermostatStagedDualSetpoint, etc)
                # But 'getThermostatSetpointDualSetpointByName' is specific.
                # Actually, setThermostatSetpointDualSetpoint takes that specific type.
                # Let's try generic 'getObjectByTypeAndName' if possible, or iterate.
                # Simplest way: The model has global thermostats.
                # We'll assume DualSetpoint for now as it's 95% of cases, or search widely?
                # OpenStudio API allows `setThermostatSetpointDualSetpoint`.
                
                # Let's try to find it as a DualSetpoint first
                tstat_opt = osm_model.getThermostatSetpointDualSetpointByName(tstat_name)
                if tstat_opt.is_initialized():
                    target_zone.setThermostatSetpointDualSetpoint(tstat_opt.get())
                    changes_made = True
                else:
                    msg = f"Warning: Thermostat (DualSetpoint) '{tstat_name}' not found for zone '{target_zone.nameString()}'"
                    logger.warning(msg)
                    messages.append(msg)
            else:
                # Reset if explicitly empty/None?
                target_zone.resetThermostatSetpointDualSetpoint()
                changes_made = True

        if 'Humidistat Name' in entry:
            hstat_name = entry['Humidistat Name']
            if hstat_name:
                hstat_opt = osm_model.getZoneControlHumidistatByName(hstat_name)
                if hstat_opt.is_initialized():
                    target_zone.setZoneControlHumidistat(hstat_opt.get())
                    changes_made = True
                else:
                    msg = f"Warning: Humidistat '{hstat_name}' not found for zone '{target_zone.nameString()}'"
                    logger.warning(msg)
                    messages.append(msg)
            else:
                target_zone.resetZoneControlHumidistat()
                changes_made = True

        if changes_made:
            updated_count += 1

    status = "SUCCESS" if updated_count > 0 or (len(zones_data) > 0 and errors == 0) else "ERROR"
    if errors > 0 and updated_count > 0:
        status = "PARTIAL_SUCCESS"
        
    logger.info(f"Finished batch update. Updated: {updated_count}, Errors: {errors}")
    
    return {
        "status": status,
        "updated_count": updated_count,
        "errors": errors,
        "messages": messages
    }