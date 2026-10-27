"""Extractors for HVAC Availability Manager objects.

Covers:
    - OS:AvailabilityManager:NightCycle
"""

import logging
from typing import Any

import openstudio
import pandas as pd

from openstudio_toolkit._sdk import opt, related_name
from openstudio_toolkit.osm_objects._base import build_all_dicts, build_dataframe
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
        name = opt(zone.name())
        if name is not None:
            names.append(name)
    return ", ".join(names) if names else None


# ---------------------------------------------------------------------------
#  OS:AvailabilityManager:NightCycle
# ---------------------------------------------------------------------------

AVAILABILITY_MANAGER_NIGHT_CYCLE_COLUMNS = (
    'Handle',
    'Name',
    'Applicability Schedule',
    'Fan Schedule',
    'Control Type',
    'Thermostat Tolerance {deltaC}',
    'Cycling Run Time Control Type',
    'Cycling Run Time {s}',
    'Control Zone or Zone List Name',
    'Cooling Control Zone or Zone List Name',
    'Heating Control Zone or Zone List Name',
    'Heating Zone Fans Only Zone or Zone List Name',
)


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

    # Not a plain field read: fanSchedule() can return a schedule while the Fan Schedule field is empty
    # in the IDF (OpenStudio computes it), so the name comes from the accessor, not related_name().
    fan_schedule = opt(target_object.fanSchedule())

    return {
        'Handle': str(target_object.handle()),
        'Name': opt(target_object.name()),
        'Applicability Schedule': related_name(target_object, "Applicability Schedule"),
        'Fan Schedule': opt(fan_schedule.name()) if fan_schedule is not None else None,
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
    return build_all_dicts(
        osm_model,
        "getAvailabilityManagerNightCycles",
        get_availability_manager_night_cycle_object_as_dict,
    )


def get_all_availability_manager_night_cycle_objects_as_dataframe(
    osm_model: openstudio.model.Model,
) -> pd.DataFrame:
    """Retrieve all OS:AvailabilityManager:NightCycle objects as a DataFrame."""
    return build_dataframe(
        get_all_availability_manager_night_cycle_objects_as_dicts(osm_model),
        "AvailabilityManagerNightCycle", columns=AVAILABILITY_MANAGER_NIGHT_CYCLE_COLUMNS,
    )
