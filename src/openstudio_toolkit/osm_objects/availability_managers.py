"""Extractors for HVAC Availability Manager objects.

Covers:
    - OS:AvailabilityManager:NightCycle
"""

import logging
from typing import Any

import openstudio
import pandas as pd

from openstudio_toolkit.utils import helpers

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
#  Private helpers
# ---------------------------------------------------------------------------

def _zone_list_to_name(zones) -> str | None:
    """Convert a tuple/list of ThermalZone objects to comma-separated names.

    Returns None when the collection is empty.
    """
    if not zones:
        return None
    names = []
    for zone in zones:
        if zone.name().is_initialized():
            names.append(zone.name().get())
    return ", ".join(names) if names else None


# ---------------------------------------------------------------------------
#  OS:AvailabilityManager:NightCycle
# ---------------------------------------------------------------------------

def get_availability_manager_night_cycle_object_as_dict(
    osm_model: openstudio.model.Model,
    handle: str | None = None,
    name: str | None = None,
    _object_ref: openstudio.model.AvailabilityManagerNightCycle | None = None,
) -> dict[str, Any]:
    """Retrieve attributes of a single OS:AvailabilityManager:NightCycle.

    Parameters
    ----------
    osm_model : openstudio.model.Model
        The OpenStudio Model object.
    handle : str, optional
        Handle UUID of the object.
    name : str, optional
        Name of the object.
    _object_ref : AvailabilityManagerNightCycle, optional
        Direct object reference (bypasses lookup).

    Returns
    -------
    dict[str, Any]
        Dictionary of object attributes, or empty dict if not found.
    """
    target_object = helpers.fetch_object(
        osm_model, "AvailabilityManagerNightCycle", handle, name, _object_ref
    )

    if target_object is None:
        return {}

    return {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Applicability Schedule': target_object.applicabilitySchedule().name().get() if target_object.applicabilitySchedule().name().is_initialized() else None,
        'Fan Schedule': target_object.fanSchedule().get().name().get() if target_object.fanSchedule().is_initialized() else None,
        'Control Type': target_object.controlType(),
        'Thermostat Tolerance {deltaC}': target_object.thermostatTolerance(),
        'Cycling Run Time Control Type': target_object.cyclingRunTimeControlType(),
        'Cycling Run Time {s}': target_object.cyclingRunTime(),
        'Control Zone or Zone List Name': _zone_list_to_name(target_object.controlThermalZones()),
        'Cooling Control Zone or Zone List Name': _zone_list_to_name(target_object.coolingControlThermalZones()),
        'Heating Control Zone or Zone List Name': _zone_list_to_name(target_object.heatingControlThermalZones()),
        'Heating Zone Fans Only Zone or Zone List Name': _zone_list_to_name(target_object.heatingZoneFansOnlyThermalZones()),
    }


def get_all_availability_manager_night_cycle_objects_as_dicts(
    osm_model: openstudio.model.Model,
) -> list[dict[str, Any]]:
    """Retrieve attributes for all OS:AvailabilityManager:NightCycle objects."""
    from openstudio_toolkit.osm_objects._base import build_all_dicts

    return build_all_dicts(
        osm_model,
        "getAvailabilityManagerNightCycles",
        get_availability_manager_night_cycle_object_as_dict,
    )


def get_all_availability_manager_night_cycle_objects_as_dataframe(
    osm_model: openstudio.model.Model,
) -> pd.DataFrame:
    """Retrieve all OS:AvailabilityManager:NightCycle objects as a DataFrame."""
    from openstudio_toolkit.osm_objects._base import build_dataframe

    return build_dataframe(
        get_all_availability_manager_night_cycle_objects_as_dicts(osm_model),
        "AvailabilityManagerNightCycle",
    )
