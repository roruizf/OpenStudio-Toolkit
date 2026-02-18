import logging
from typing import Any, Callable, Dict, Tuple

import openstudio

logger = logging.getLogger(__name__)


def _default_zone_name(space_name: str) -> str:
    """
    Default zone-grouping function for Honeybee-generated residential buildings.

    Assumes space names follow the SAC/Honeybee pattern after normalization:
        [CODE]_[PROJECT]_[FLOOR]_[UNIT]_[ROOM_TYPE]
        e.g.: 308_32_L2_A44_IS

    Grouping rules:
    - Apartment units (UNIT starts with 'A' + digits) -> TZ_[FLOOR]_[UNIT]
    - Commercial (ROOM_TYPE contains 'Loja') -> TZ_[FLOOR]_[ROOM_TYPE]
    - Common areas (Escadas, Elevadores, Corredor, etc.) -> TZ_[FLOOR]_Common
    - Utility spaces (Shaft, Plenum, AVAC, etc.) -> TZ_[FLOOR]_Utility
    - Anything else -> TZ_[FLOOR]_[UNIT]

    Parameters:
        space_name: Normalized space name string.

    Returns:
        Target thermal zone name string.
    """
    parts = space_name.split('_')
    if len(parts) < 5:
        return f"TZ_Other_{space_name}"

    floor = parts[2]
    unit = parts[3]
    room_type = parts[4]

    if unit.startswith('A') and unit[1:].isdigit():
        return f"TZ_{floor}_{unit}"
    if "Loja" in room_type:
        return f"TZ_{floor}_{room_type}"

    common_types = ['Escadas', 'Elevadores', 'Nucleo', 'Corredor', 'Circ', 'Atrio', 'CC', 'PN', 'Hall']
    if any(ct in room_type for ct in common_types) or unit == 'CC':
        return f"TZ_{floor}_Common"

    utility_types = ['Shaft', 'Plenum', 'AVAC', 'ETAR', 'Residuos', 'Tecnico', 'Garagem']
    if any(ut in room_type for ut in utility_types):
        return f"TZ_{floor}_Utility"

    return f"TZ_{floor}_{unit}"


def _consolidate_hvac(master_zone, sibling_zones):
    """
    Consolidate HVAC equipment from multiple zones into the master zone.

    Rules:
    - VRF Terminals (ZoneHVACTerminalUnitVariableRefrigerantFlow): keep 1, remove duplicates
    - PTHPs (ZoneHVACPackagedTerminalHeatPump): keep 1, remove duplicates
    - All other zone equipment (e.g. DHW Heat Pumps): move to master, do not remove

    Parameters:
        master_zone: The surviving ThermalZone object.
        sibling_zones: List of ThermalZone objects to be merged into master.
    """
    all_zones = [master_zone] + sibling_zones

    # --- VRF Terminals ---
    vrfs = []
    for zone in all_zones:
        for eq in zone.equipment():
            terminal = eq.to_ZoneHVACTerminalUnitVariableRefrigerantFlow()
            if terminal.is_initialized():
                vrfs.append(terminal.get())

    if len(vrfs) > 1:
        vrfs[0].addToThermalZone(master_zone)
        for duplicate in vrfs[1:]:
            duplicate.remove()

    # --- PTHPs ---
    pthps = []
    for zone in all_zones:
        for eq in zone.equipment():
            pthp = eq.to_ZoneHVACPackagedTerminalHeatPump()
            if pthp.is_initialized():
                pthps.append(pthp.get())

    if len(pthps) > 1:
        pthps[0].addToThermalZone(master_zone)
        for duplicate in pthps[1:]:
            duplicate.remove()

    # --- Other equipment (DHW HPs, etc.) — move to master, preserve all ---
    for zone in sibling_zones:
        for eq in zone.equipment():
            is_vrf = eq.to_ZoneHVACTerminalUnitVariableRefrigerantFlow().is_initialized()
            is_pthp = eq.to_ZoneHVACPackagedTerminalHeatPump().is_initialized()
            if not is_vrf and not is_pthp:
                component = eq.to_ZoneHVACComponent()
                if component.is_initialized():
                    component.get().addToThermalZone(master_zone)


def validator(osm_model: openstudio.model.Model) -> Dict[str, Any]:
    """
    Validate that the model has thermal zones eligible for consolidation.

    Parameters:
        osm_model: The OpenStudio Model object to validate.

    Returns:
        Dict with 'status' ('READY', 'SKIP', or 'ERROR') and 'messages'.
    """
    zones = osm_model.getThermalZones()
    spaces = osm_model.getSpaces()

    if len(zones) == 0:
        msg = "ERROR: Model has no thermal zones."
        logger.error(msg)
        return {"status": "ERROR", "messages": [msg]}

    if len(spaces) == 0:
        msg = "ERROR: Model has no spaces."
        logger.error(msg)
        return {"status": "ERROR", "messages": [msg]}

    spaces_with_zones = [s for s in spaces if s.thermalZone().is_initialized()]

    if len(spaces_with_zones) == 0:
        msg = "ERROR: No spaces are assigned to a thermal zone."
        logger.error(msg)
        return {"status": "ERROR", "messages": [msg]}

    if len(zones) <= 1:
        msg = f"INFO: Model has only {len(zones)} thermal zone(s). Nothing to consolidate."
        logger.info(msg)
        return {"status": "SKIP", "messages": [msg]}

    messages = [
        f"OK: Found {len(spaces_with_zones)} spaces across {len(zones)} thermal zones.",
        "INFO: Ready to consolidate zones and HVAC equipment.",
    ]
    logger.info(" | ".join(messages))
    return {"status": "READY", "messages": messages}


def run(
    osm_model: openstudio.model.Model,
    zone_naming_fn: Callable[[str], str] = _default_zone_name,
) -> Tuple[openstudio.model.Model, Dict[str, int]]:
    """
    Simplify thermal zoning by grouping spaces and consolidating HVAC equipment.

    For each group of spaces that map to the same target zone name:
    1. The first space's thermal zone becomes the "master" zone (renamed to target name).
    2. All other spaces are moved to the master zone.
    3. HVAC equipment is consolidated: one VRF Terminal or PTHP per zone (duplicates removed).
    4. Non-primary equipment (DHW HPs, etc.) is moved to the master zone and preserved.
    5. Empty sibling zones are deleted.

    Parameters:
        osm_model: The OpenStudio Model object to process.
        zone_naming_fn: Function that maps a space name (str) to a target zone name (str).
                        Defaults to _default_zone_name for SAC-style Honeybee buildings.
                        Override this for buildings with different naming conventions.

    Returns:
        Tuple of (modified model, dict with 'initial' and 'final' zone counts).
    """
    logger.info("Starting simplify_thermal_zoning task...")

    initial_zone_count = len(osm_model.getThermalZones())

    # Group spaces by target zone name
    groups: Dict[str, list] = {}
    for space in osm_model.getSpaces():
        if not space.thermalZone().is_initialized():
            continue
        target_name = zone_naming_fn(space.nameString())
        groups.setdefault(target_name, []).append(space)

    final_zone_count = 0
    for target_name, spaces in groups.items():
        master_zone = spaces[0].thermalZone().get()
        master_zone.setName(target_name)

        sibling_zones = []
        for space in spaces[1:]:
            sibling_zone = space.thermalZone().get()
            if sibling_zone.handle() != master_zone.handle():
                if sibling_zone not in sibling_zones:
                    sibling_zones.append(sibling_zone)
                space.setThermalZone(master_zone)

        _consolidate_hvac(master_zone, sibling_zones)

        for zone in sibling_zones:
            zone.remove()

        final_zone_count += 1

    logger.info(
        f"simplify_thermal_zoning finished. "
        f"Zones reduced from {initial_zone_count} to {final_zone_count}."
    )

    return osm_model, {"initial": initial_zone_count, "final": final_zone_count}
