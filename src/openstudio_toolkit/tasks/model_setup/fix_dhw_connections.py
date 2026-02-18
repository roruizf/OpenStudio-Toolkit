import logging
import re
from typing import Any, Dict, Tuple

import openstudio

logger = logging.getLogger(__name__)

# Regex to extract a normalizable space name from Honeybee-generated object names.
# Honeybee exports names like: "2019::MidriseApartment::Apartment_SHW..308_32_L2_A44_IS_a1756e43"
# Pattern captures the first segment that starts with digits: "308_32_L2_A44_IS_a1756e43"
_SPACE_NAME_PATTERN = re.compile(r'(\d+_[^.]+)')
_UUID_SUFFIX = re.compile(r'_[0-9a-f]{8}$')


def validator(osm_model: openstudio.model.Model) -> Dict[str, Any]:
    """
    Validate that the model has WaterUseEquipment objects that need connection repair.

    Honeybee-generated models often export WaterUseEquipment objects that are either
    disconnected from their spaces, or have a peakFlowRate of 0 due to floating-point
    truncation during export.

    Parameters:
        osm_model: The OpenStudio Model object to validate.

    Returns:
        Dict with 'status' ('READY', 'SKIP', or 'ERROR') and 'messages'.
    """
    wue_list = model_wue_list = osm_model.getWaterUseEquipments()

    if len(wue_list) == 0:
        msg = "INFO: Model has no WaterUseEquipment objects. Nothing to do."
        logger.info(msg)
        return {"status": "SKIP", "messages": [msg]}

    orphaned = [e for e in wue_list if not e.space().is_initialized()]
    zero_flow = [
        e for e in wue_list
        if e.waterUseEquipmentDefinition().peakFlowRate() == 0.0
    ]

    messages = [f"OK: Found {len(wue_list)} WaterUseEquipment objects."]

    if not orphaned and not zero_flow:
        msg = "INFO: All WaterUseEquipment are linked and have non-zero flow. Nothing to do."
        logger.info(msg)
        messages.append(msg)
        return {"status": "SKIP", "messages": messages}

    if orphaned:
        messages.append(f"WARNING: {len(orphaned)} objects are not linked to a space.")
    if zero_flow:
        messages.append(f"WARNING: {len(zero_flow)} objects have peakFlowRate = 0.")

    logger.info(" | ".join(messages))
    return {"status": "READY", "messages": messages}


def run(
    osm_model: openstudio.model.Model,
) -> Tuple[openstudio.model.Model, list]:
    """
    Re-link WaterUseEquipment to their spaces and normalize DHW object names.

    Extracts the target space name from each WaterUseEquipment object name using
    the Honeybee naming pattern, then:
    - Links the equipment to its space using setSpace()
    - Normalizes equipment names to: DHW_[SpaceName]
    - Normalizes definition names to: DHW_Def_[SpaceName]
    - Normalizes connection names to: DHW_Conn_[SpaceName]

    Parameters:
        osm_model: The OpenStudio Model object to process.

    Returns:
        Tuple of (modified model, audit list of dicts with linking results).
    """
    logger.info("Starting fix_dhw_connections task...")

    spaces_map = {s.nameString(): s for s in osm_model.getSpaces()}
    audit = []

    for equipment in osm_model.getWaterUseEquipments():
        old_name = equipment.nameString()
        definition = equipment.waterUseEquipmentDefinition()

        match = _SPACE_NAME_PATTERN.search(old_name)
        target_space = None

        if match:
            candidate = _UUID_SUFFIX.sub('', match.group(1))
            if candidate in spaces_map:
                target_space = spaces_map[candidate]

                if not equipment.space().is_initialized():
                    equipment.setSpace(target_space)

                equipment.setName(f"DHW_{candidate}")
                definition.setName(f"DHW_Def_{candidate}")

        audit.append({
            "Original Name": old_name,
            "Target Space": target_space.nameString() if target_space else "Not Found",
            "Flow Rate [m3/s]": definition.peakFlowRate(),
            "Linked Successfully": target_space is not None,
        })

    for connection in osm_model.getWaterUseConnectionss():
        match = _SPACE_NAME_PATTERN.search(connection.nameString())
        if match:
            candidate = _UUID_SUFFIX.sub('', match.group(1))
            connection.setName(f"DHW_Conn_{candidate}")

    linked = sum(1 for row in audit if row["Linked Successfully"])
    logger.info(
        f"fix_dhw_connections finished. "
        f"{linked}/{len(audit)} WaterUseEquipment linked to spaces."
    )

    return osm_model, audit
