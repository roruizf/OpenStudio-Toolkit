"""Extractors for internal loads objects.

Covers:
    - OS:People
    - OS:People:Definition
    - OS:Lights
    - OS:Lights:Definition
    - OS:ElectricEquipment
    - OS:ElectricEquipment:Definition
    - OS:GasEquipment
    - OS:GasEquipment:Definition
    - OS:SteamEquipment
    - OS:SteamEquipment:Definition
    - OS:OtherEquipment
    - OS:OtherEquipment:Definition
    - OS:WaterUse:Equipment
    - OS:WaterUse:Equipment:Definition
    - OS:SpaceInfiltration:DesignFlowRate
    - OS:DesignSpecification:OutdoorAir
"""

import logging
from typing import Any

import openstudio
import pandas as pd

from openstudio_toolkit.utils import helpers

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
#  OS:People
# ---------------------------------------------------------------------------

def get_people_object_as_dict(
    osm_model: openstudio.model.Model,
    handle: str | None = None,
    name: str | None = None,
    _object_ref: openstudio.model.People | None = None,
) -> dict[str, Any]:
    """Retrieve attributes of a single OS:People object.

    Parameters
    ----------
    osm_model : openstudio.model.Model
        The OpenStudio Model object.
    handle : str, optional
        Handle UUID of the object.
    name : str, optional
        Name of the object.
    _object_ref : People, optional
        Direct object reference (bypasses lookup).

    Returns
    -------
    dict[str, Any]
        Dictionary of object attributes, or empty dict if not found.
    """
    target_object = helpers.fetch_object(
        osm_model, "People", handle, name, _object_ref
    )

    if target_object is None:
        return {}

    # Resolve Space or SpaceType Name
    space_or_spacetype = None
    if target_object.spaceType().is_initialized():
        space_or_spacetype = (
            target_object.spaceType().get().name().get()
            if target_object.spaceType().get().name().is_initialized()
            else None
        )
    elif target_object.space().is_initialized():
        space_or_spacetype = (
            target_object.space().get().name().get()
            if target_object.space().get().name().is_initialized()
            else None
        )

    return {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'People Definition Name': (
            target_object.peopleDefinition().name().get()
            if target_object.peopleDefinition().name().is_initialized()
            else None
        ),
        'Space or SpaceType Name': space_or_spacetype,
        'Number of People Schedule Name': (
            target_object.numberofPeopleSchedule().get().name().get()
            if target_object.numberofPeopleSchedule().is_initialized()
            else None
        ),
        'Activity Level Schedule Name': (
            target_object.activityLevelSchedule().get().name().get()
            if target_object.activityLevelSchedule().is_initialized()
            else None
        ),
        'Surface Name/Angle Factor List Name': None,  # Not accessible via SDK
        'Work Efficiency Schedule Name': (
            target_object.workEfficiencySchedule().get().name().get()
            if target_object.workEfficiencySchedule().is_initialized()
            else None
        ),
        'Clothing Insulation Schedule Name': (
            target_object.clothingInsulationSchedule().get().name().get()
            if target_object.clothingInsulationSchedule().is_initialized()
            else None
        ),
        'Air Velocity Schedule Name': (
            target_object.airVelocitySchedule().get().name().get()
            if target_object.airVelocitySchedule().is_initialized()
            else None
        ),
        'Multiplier': target_object.multiplier(),
    }


def get_all_people_objects_as_dicts(
    osm_model: openstudio.model.Model,
) -> list[dict[str, Any]]:
    """Retrieve attributes for all OS:People objects."""
    from openstudio_toolkit.osm_objects._base import build_all_dicts

    return build_all_dicts(
        osm_model,
        "getPeoples",
        get_people_object_as_dict,
    )


def get_all_people_objects_as_dataframe(
    osm_model: openstudio.model.Model,
) -> pd.DataFrame:
    """Retrieve all OS:People objects as a DataFrame."""
    from openstudio_toolkit.osm_objects._base import build_dataframe

    return build_dataframe(
        get_all_people_objects_as_dicts(osm_model),
        "People",
    )


# ---------------------------------------------------------------------------
#  OS:People:Definition
# ---------------------------------------------------------------------------

def get_people_definition_object_as_dict(
    osm_model: openstudio.model.Model,
    handle: str | None = None,
    name: str | None = None,
    _object_ref: openstudio.model.PeopleDefinition | None = None,
) -> dict[str, Any]:
    """Retrieve attributes of a single OS:People:Definition object.

    Parameters
    ----------
    osm_model : openstudio.model.Model
        The OpenStudio Model object.
    handle : str, optional
        Handle UUID of the object.
    name : str, optional
        Name of the object.
    _object_ref : PeopleDefinition, optional
        Direct object reference (bypasses lookup).

    Returns
    -------
    dict[str, Any]
        Dictionary of object attributes, or empty dict if not found.
    """
    target_object = helpers.fetch_object(
        osm_model, "PeopleDefinition", handle, name, _object_ref
    )

    if target_object is None:
        return {}

    return {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Number of People Calculation Method': target_object.numberofPeopleCalculationMethod(),
        'Number of People {people}': (
            target_object.numberofPeople().get()
            if target_object.numberofPeople().is_initialized()
            else None
        ),
        'People per Space Floor Area {person/m2}': (
            target_object.peopleperSpaceFloorArea().get()
            if target_object.peopleperSpaceFloorArea().is_initialized()
            else None
        ),
        'Space Floor Area per Person {m2/person}': (
            target_object.spaceFloorAreaperPerson().get()
            if target_object.spaceFloorAreaperPerson().is_initialized()
            else None
        ),
        'Fraction Radiant': target_object.fractionRadiant(),
        'Sensible Heat Fraction': (
            target_object.sensibleHeatFraction().get()
            if target_object.sensibleHeatFraction().is_initialized()
            else None
        ),
        'Carbon Dioxide Generation Rate {m3/s-W}': target_object.carbonDioxideGenerationRate(),
    }


def get_all_people_definition_objects_as_dicts(
    osm_model: openstudio.model.Model,
) -> list[dict[str, Any]]:
    """Retrieve attributes for all OS:People:Definition objects."""
    from openstudio_toolkit.osm_objects._base import build_all_dicts

    return build_all_dicts(
        osm_model,
        "getPeopleDefinitions",
        get_people_definition_object_as_dict,
    )


def get_all_people_definition_objects_as_dataframe(
    osm_model: openstudio.model.Model,
) -> pd.DataFrame:
    """Retrieve all OS:People:Definition objects as a DataFrame."""
    from openstudio_toolkit.osm_objects._base import build_dataframe

    return build_dataframe(
        get_all_people_definition_objects_as_dicts(osm_model),
        "PeopleDefinition",
    )


# ---------------------------------------------------------------------------
#  OS:Lights
# ---------------------------------------------------------------------------

def get_lights_object_as_dict(
    osm_model: openstudio.model.Model,
    handle: str | None = None,
    name: str | None = None,
    _object_ref: openstudio.model.Lights | None = None,
) -> dict[str, Any]:
    """Retrieve attributes of a single OS:Lights object.

    Parameters
    ----------
    osm_model : openstudio.model.Model
        The OpenStudio Model object.
    handle : str, optional
        Handle UUID of the object.
    name : str, optional
        Name of the object.
    _object_ref : Lights, optional
        Direct object reference (bypasses lookup).

    Returns
    -------
    dict[str, Any]
        Dictionary of object attributes, or empty dict if not found.
    """
    target_object = helpers.fetch_object(
        osm_model, "Lights", handle, name, _object_ref
    )

    if target_object is None:
        return {}

    # Resolve Space or SpaceType Name
    space_or_spacetype = None
    if target_object.spaceType().is_initialized():
        space_or_spacetype = (
            target_object.spaceType().get().name().get()
            if target_object.spaceType().get().name().is_initialized()
            else None
        )
    elif target_object.space().is_initialized():
        space_or_spacetype = (
            target_object.space().get().name().get()
            if target_object.space().get().name().is_initialized()
            else None
        )

    return {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Lights Definition Name': (
            target_object.lightsDefinition().name().get()
            if target_object.lightsDefinition().name().is_initialized()
            else None
        ),
        'Space or SpaceType Name': space_or_spacetype,
        'Schedule Name': (
            target_object.schedule().get().name().get()
            if target_object.schedule().is_initialized()
            else None
        ),
        'Fraction Replaceable': target_object.fractionReplaceable(),
        'Multiplier': target_object.multiplier(),
        'End-Use Subcategory': target_object.endUseSubcategory(),
    }


def get_all_lights_objects_as_dicts(
    osm_model: openstudio.model.Model,
) -> list[dict[str, Any]]:
    """Retrieve attributes for all OS:Lights objects."""
    from openstudio_toolkit.osm_objects._base import build_all_dicts

    return build_all_dicts(
        osm_model,
        "getLightss",
        get_lights_object_as_dict,
    )


def get_all_lights_objects_as_dataframe(
    osm_model: openstudio.model.Model,
) -> pd.DataFrame:
    """Retrieve all OS:Lights objects as a DataFrame."""
    from openstudio_toolkit.osm_objects._base import build_dataframe

    return build_dataframe(
        get_all_lights_objects_as_dicts(osm_model),
        "Lights",
    )


# ---------------------------------------------------------------------------
#  OS:Lights:Definition
# ---------------------------------------------------------------------------

def get_lights_definition_object_as_dict(
    osm_model: openstudio.model.Model,
    handle: str | None = None,
    name: str | None = None,
    _object_ref: openstudio.model.LightsDefinition | None = None,
) -> dict[str, Any]:
    """Retrieve attributes of a single OS:Lights:Definition object.

    Parameters
    ----------
    osm_model : openstudio.model.Model
        The OpenStudio Model object.
    handle : str, optional
        Handle UUID of the object.
    name : str, optional
        Name of the object.
    _object_ref : LightsDefinition, optional
        Direct object reference (bypasses lookup).

    Returns
    -------
    dict[str, Any]
        Dictionary of object attributes, or empty dict if not found.
    """
    target_object = helpers.fetch_object(
        osm_model, "LightsDefinition", handle, name, _object_ref
    )

    if target_object is None:
        return {}

    return {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Design Level Calculation Method': target_object.designLevelCalculationMethod(),
        'Lighting Level {W}': (
            target_object.lightingLevel().get()
            if target_object.lightingLevel().is_initialized()
            else None
        ),
        'Watts per Space Floor Area {W/m2}': (
            target_object.wattsperSpaceFloorArea().get()
            if target_object.wattsperSpaceFloorArea().is_initialized()
            else None
        ),
        'Watts per Person {W/person}': (
            target_object.wattsperPerson().get()
            if target_object.wattsperPerson().is_initialized()
            else None
        ),
        'Fraction Radiant': target_object.fractionRadiant(),
        'Fraction Visible': target_object.fractionVisible(),
        'Return Air Fraction': target_object.returnAirFraction(),
    }


def get_all_lights_definition_objects_as_dicts(
    osm_model: openstudio.model.Model,
) -> list[dict[str, Any]]:
    """Retrieve attributes for all OS:Lights:Definition objects."""
    from openstudio_toolkit.osm_objects._base import build_all_dicts

    return build_all_dicts(
        osm_model,
        "getLightsDefinitions",
        get_lights_definition_object_as_dict,
    )


def get_all_lights_definition_objects_as_dataframe(
    osm_model: openstudio.model.Model,
) -> pd.DataFrame:
    """Retrieve all OS:Lights:Definition objects as a DataFrame."""
    from openstudio_toolkit.osm_objects._base import build_dataframe

    return build_dataframe(
        get_all_lights_definition_objects_as_dicts(osm_model),
        "LightsDefinition",
    )


# ---------------------------------------------------------------------------
#  OS:ElectricEquipment
# ---------------------------------------------------------------------------

def get_electric_equipment_object_as_dict(
    osm_model: openstudio.model.Model,
    handle: str | None = None,
    name: str | None = None,
    _object_ref: openstudio.model.ElectricEquipment | None = None,
) -> dict[str, Any]:
    """Retrieve attributes of a single OS:ElectricEquipment object.

    Parameters
    ----------
    osm_model : openstudio.model.Model
        The OpenStudio Model object.
    handle : str, optional
        Handle UUID of the object.
    name : str, optional
        Name of the object.
    _object_ref : ElectricEquipment, optional
        Direct object reference (bypasses lookup).

    Returns
    -------
    dict[str, Any]
        Dictionary of object attributes, or empty dict if not found.
    """
    target_object = helpers.fetch_object(
        osm_model, "ElectricEquipment", handle, name, _object_ref
    )

    if target_object is None:
        return {}

    # Resolve Space or SpaceType Name
    space_or_spacetype = None
    if target_object.spaceType().is_initialized():
        space_or_spacetype = (
            target_object.spaceType().get().name().get()
            if target_object.spaceType().get().name().is_initialized()
            else None
        )
    elif target_object.space().is_initialized():
        space_or_spacetype = (
            target_object.space().get().name().get()
            if target_object.space().get().name().is_initialized()
            else None
        )

    return {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Electric Equipment Definition Name': (
            target_object.definition().name().get()
            if target_object.definition().name().is_initialized()
            else None
        ),
        'Space or SpaceType Name': space_or_spacetype,
        'Schedule Name': (
            target_object.schedule().get().name().get()
            if target_object.schedule().is_initialized()
            else None
        ),
        'Multiplier': target_object.multiplier(),
        'End-Use Subcategory': target_object.endUseSubcategory(),
    }


def get_all_electric_equipment_objects_as_dicts(
    osm_model: openstudio.model.Model,
) -> list[dict[str, Any]]:
    """Retrieve attributes for all OS:ElectricEquipment objects."""
    from openstudio_toolkit.osm_objects._base import build_all_dicts

    return build_all_dicts(
        osm_model,
        "getElectricEquipments",
        get_electric_equipment_object_as_dict,
    )


def get_all_electric_equipment_objects_as_dataframe(
    osm_model: openstudio.model.Model,
) -> pd.DataFrame:
    """Retrieve all OS:ElectricEquipment objects as a DataFrame."""
    from openstudio_toolkit.osm_objects._base import build_dataframe

    return build_dataframe(
        get_all_electric_equipment_objects_as_dicts(osm_model),
        "ElectricEquipment",
    )


# ---------------------------------------------------------------------------
#  OS:ElectricEquipment:Definition
# ---------------------------------------------------------------------------

def get_electric_equipment_definition_object_as_dict(
    osm_model: openstudio.model.Model,
    handle: str | None = None,
    name: str | None = None,
    _object_ref: openstudio.model.ElectricEquipmentDefinition | None = None,
) -> dict[str, Any]:
    """Retrieve attributes of a single OS:ElectricEquipment:Definition object.

    Parameters
    ----------
    osm_model : openstudio.model.Model
        The OpenStudio Model object.
    handle : str, optional
        Handle UUID of the object.
    name : str, optional
        Name of the object.
    _object_ref : ElectricEquipmentDefinition, optional
        Direct object reference (bypasses lookup).

    Returns
    -------
    dict[str, Any]
        Dictionary of object attributes, or empty dict if not found.
    """
    target_object = helpers.fetch_object(
        osm_model, "ElectricEquipmentDefinition", handle, name, _object_ref
    )

    if target_object is None:
        return {}

    return {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Design Level Calculation Method': target_object.designLevelCalculationMethod(),
        'Design Level {W}': (
            target_object.designLevel().get()
            if target_object.designLevel().is_initialized()
            else None
        ),
        'Watts per Space Floor Area {W/m2}': (
            target_object.wattsperSpaceFloorArea().get()
            if target_object.wattsperSpaceFloorArea().is_initialized()
            else None
        ),
        'Watts per Person {W/person}': (
            target_object.wattsperPerson().get()
            if target_object.wattsperPerson().is_initialized()
            else None
        ),
        'Fraction Latent': target_object.fractionLatent(),
        'Fraction Radiant': target_object.fractionRadiant(),
        'Fraction Lost': target_object.fractionLost(),
    }


def get_all_electric_equipment_definition_objects_as_dicts(
    osm_model: openstudio.model.Model,
) -> list[dict[str, Any]]:
    """Retrieve attributes for all OS:ElectricEquipment:Definition objects."""
    from openstudio_toolkit.osm_objects._base import build_all_dicts

    return build_all_dicts(
        osm_model,
        "getElectricEquipmentDefinitions",
        get_electric_equipment_definition_object_as_dict,
    )


def get_all_electric_equipment_definition_objects_as_dataframe(
    osm_model: openstudio.model.Model,
) -> pd.DataFrame:
    """Retrieve all OS:ElectricEquipment:Definition objects as a DataFrame."""
    from openstudio_toolkit.osm_objects._base import build_dataframe

    return build_dataframe(
        get_all_electric_equipment_definition_objects_as_dicts(osm_model),
        "ElectricEquipmentDefinition",
    )


# ------------------------------------------------------------------------------------------------
#  ****** LEGACY OBJECTS (NOT REFACTORED) *******************************************************
#  The following objects remain in their original v0.1.0 implementation style
# ------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------
#  ****** Gas Equipment **************************************************************************
# ------------------------------------------------------------------------------------------------

def get_gas_equipment_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None, _object_ref: openstudio.model.GasEquipment = None) -> dict:
    """
    Retrieve a specified OS:GasEquipment object from the OpenStudio model by handle, name, or direct reference and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.GasEquipment, optional): Direct reference to the object.

    Returns:
    - dict: Dictionary containing information about the specified object.
    """
    target_object = helpers.fetch_object(
        osm_model, "GasEquipment", handle, name, _object_ref)

    if target_object is None:
        return {}

    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Gas Equipment Definition Name': target_object.definition().name().get() if target_object.definition().name().is_initialized() else None,
        'Space or SpaceType Name': target_object.spaceType().get().name().get() if target_object.spaceType().is_initialized() else (target_object.space().get().name().get() if target_object.space().is_initialized() else None),
        'Schedule Name': target_object.schedule().get().name().get() if target_object.schedule().is_initialized() else None,
        'Multiplier': target_object.multiplier(),
        'End-Use Subcategory': target_object.endUseSubcategory()
    }

    return object_dict

def get_all_gas_equipment_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all OS:GasEquipment objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a gas equipment object.
    """
    all_objects = osm_model.getGasEquipments()
    return [get_gas_equipment_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_gas_equipment_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:GasEquipment objects from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all gas equipment objects.
    """
    all_objects_dicts = get_all_gas_equipment_objects_as_dicts(osm_model)
    all_objects_df = pd.DataFrame(all_objects_dicts)

    if not all_objects_df.empty:
        if 'Name' in all_objects_df.columns:
            all_objects_df = all_objects_df.sort_values(
                by='Name', ascending=True, na_position='first').reset_index(drop=True)

    logger.info(f"The OSM model contains {all_objects_df.shape[0]} gas equipment objects")
    return all_objects_df


# ------------------------------------------------------------------------------------------------
#  ****** Gas Equipment Definition ***************************************************************
# ------------------------------------------------------------------------------------------------


def get_gas_equipment_definition_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None, _object_ref: openstudio.model.GasEquipmentDefinition = None) -> dict:
    """
    Retrieve a specified OS:GasEquipment:Definition object from the OpenStudio model by handle, name, or direct reference and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.GasEquipmentDefinition, optional): Direct reference to the object.

    Returns:
    - dict: Dictionary containing information about the specified object.
    """
    target_object = helpers.fetch_object(
        osm_model, "GasEquipmentDefinition", handle, name, _object_ref)

    if target_object is None:
        return {}

    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Design Level Calculation Method': target_object.designLevelCalculationMethod(),
        'Design Level {W}': target_object.designLevel().get() if target_object.designLevel().is_initialized() else None,
        'Watts per Space Floor Area {W/m2}': target_object.wattsperSpaceFloorArea().get() if target_object.wattsperSpaceFloorArea().is_initialized() else None,
        'Watts per Person {W/person}': target_object.wattsperPerson().get() if target_object.wattsperPerson().is_initialized() else None,
        'Fraction Latent': target_object.fractionLatent(),
        'Fraction Radiant': target_object.fractionRadiant(),
        'Fraction Lost': target_object.fractionLost(),
    }

    return object_dict

def get_all_gas_equipment_definition_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all OS:GasEquipment:Definition objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a gas equipment definition object.
    """
    all_objects = osm_model.getGasEquipmentDefinitions()
    return [get_gas_equipment_definition_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_gas_equipment_definition_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:GasEquipment:Definition objects from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all gas equipment definition objects.
    """
    all_objects_dicts = get_all_gas_equipment_definition_objects_as_dicts(osm_model)
    all_objects_df = pd.DataFrame(all_objects_dicts)

    if not all_objects_df.empty:
        if 'Name' in all_objects_df.columns:
            all_objects_df = all_objects_df.sort_values(
                by='Name', ascending=True, na_position='first').reset_index(drop=True)

    logger.info(f"The OSM model contains {all_objects_df.shape[0]} gas equipment definition objects")
    return all_objects_df


# ------------------------------------------------------------------------------------------------
#  ****** Steam Equipment ************************************************************************
# ------------------------------------------------------------------------------------------------
def get_steam_equipment_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None, _object_ref: openstudio.model.SteamEquipment = None) -> dict:
    """
    Retrieve a specified OS:SteamEquipment object from the OpenStudio model by handle, name, or direct reference and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.SteamEquipment, optional): Direct reference to the object.

    Returns:
    - dict: Dictionary containing information about the specified object.
    """
    target_object = helpers.fetch_object(
        osm_model, "SteamEquipment", handle, name, _object_ref)

    if target_object is None:
        return {}

    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Steam Equipment Definition Name': target_object.definition().name().get() if target_object.definition().name().is_initialized() else None,
        'Space or SpaceType Name': target_object.spaceType().get().name().get() if target_object.spaceType().is_initialized() else (target_object.space().get().name().get() if target_object.space().is_initialized() else None),
        'Schedule Name': target_object.schedule().get().name().get() if target_object.schedule().is_initialized() else None,
        'Multiplier': target_object.multiplier(),
        'End-Use Subcategory': target_object.endUseSubcategory()
    }

    return object_dict

def get_all_steam_equipment_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all OS:SteamEquipment objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a steam equipment object.
    """
    all_objects = osm_model.getSteamEquipments()
    return [get_steam_equipment_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_steam_equipment_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:SteamEquipment objects from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all steam equipment objects.
    """
    all_objects_dicts = get_all_steam_equipment_objects_as_dicts(osm_model)
    all_objects_df = pd.DataFrame(all_objects_dicts)

    if not all_objects_df.empty:
        if 'Name' in all_objects_df.columns:
            all_objects_df = all_objects_df.sort_values(
                by='Name', ascending=True, na_position='first').reset_index(drop=True)

    logger.info(f"The OSM model contains {all_objects_df.shape[0]} steam equipment objects")
    return all_objects_df


# ------------------------------------------------------------------------------------------------
#  ****** Steam Equipment Definition *************************************************************
# ------------------------------------------------------------------------------------------------

def get_steam_equipment_definition_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None, _object_ref: openstudio.model.SteamEquipmentDefinition = None) -> dict:
    """
    Retrieve a specified OS:SteamEquipment:Definition object from the OpenStudio model by handle, name, or direct reference and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.SteamEquipmentDefinition, optional): Direct reference to the object.

    Returns:
    - dict: Dictionary containing information about the specified object.
    """
    target_object = helpers.fetch_object(
        osm_model, "SteamEquipmentDefinition", handle, name, _object_ref)

    if target_object is None:
        return {}

    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Design Level Calculation Method': target_object.designLevelCalculationMethod(),
        'Design Level {W}': target_object.designLevel().get() if target_object.designLevel().is_initialized() else None,
        'Watts per Space Floor Area {W/m2}': target_object.wattsperSpaceFloorArea().get() if target_object.wattsperSpaceFloorArea().is_initialized() else None,
        'Watts per Person {W/person}': target_object.wattsperPerson().get() if target_object.wattsperPerson().is_initialized() else None,
        'Fraction Latent': target_object.fractionLatent(),
        'Fraction Radiant': target_object.fractionRadiant(),
        'Fraction Lost': target_object.fractionLost(),
    }

    return object_dict

def get_all_steam_equipment_definition_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all OS:SteamEquipment:Definition objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a steam equipment definition object.
    """
    all_objects = osm_model.getSteamEquipmentDefinitions()
    return [get_steam_equipment_definition_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_steam_equipment_definition_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:SteamEquipment:Definition objects from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all steam equipment definition objects.
    """
    all_objects_dicts = get_all_steam_equipment_definition_objects_as_dicts(osm_model)
    all_objects_df = pd.DataFrame(all_objects_dicts)

    if not all_objects_df.empty:
        if 'Name' in all_objects_df.columns:
            all_objects_df = all_objects_df.sort_values(
                by='Name', ascending=True, na_position='first').reset_index(drop=True)

    logger.info(f"The OSM model contains {all_objects_df.shape[0]} steam equipment definition objects")
    return all_objects_df

# ------------------------------------------------------------------------------------------------
#  ****** Other Equipment ************************************************************************
# ------------------------------------------------------------------------------------------------


def get_other_equipment_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None, _object_ref: openstudio.model.OtherEquipment = None) -> dict:
    """
    Retrieve a specified OS:OtherEquipment object from the OpenStudio model by handle, name, or direct reference and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.OtherEquipment, optional): Direct reference to the object.

    Returns:
    - dict: Dictionary containing information about the specified object.
    """
    target_object = helpers.fetch_object(
        osm_model, "OtherEquipment", handle, name, _object_ref)

    if target_object is None:
        return {}

    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Other Equipment Definition Name': target_object.definition().name().get() if target_object.definition().name().is_initialized() else None,
        'Space or SpaceType Name': target_object.spaceType().get().name().get() if target_object.spaceType().is_initialized() else (target_object.space().get().name().get() if target_object.space().is_initialized() else None),
        'Schedule Name': target_object.schedule().get().name().get() if target_object.schedule().is_initialized() else None,
        'Multiplier': target_object.multiplier(),
        'Fuel Type': target_object.fuelType(),
        'End-Use Subcategory': target_object.endUseSubcategory()
    }

    return object_dict

def get_all_other_equipment_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all OS:OtherEquipment objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about an other equipment object.
    """
    all_objects = osm_model.getOtherEquipments()
    return [get_other_equipment_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_other_equipment_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:OtherEquipment objects from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all other equipment objects.
    """
    all_objects_dicts = get_all_other_equipment_objects_as_dicts(osm_model)
    all_objects_df = pd.DataFrame(all_objects_dicts)

    if not all_objects_df.empty:
        if 'Name' in all_objects_df.columns:
            all_objects_df = all_objects_df.sort_values(
                by='Name', ascending=True, na_position='first').reset_index(drop=True)

    logger.info(f"The OSM model contains {all_objects_df.shape[0]} other equipment objects")
    return all_objects_df

# ------------------------------------------------------------------------------------------------
#  ****** Other Equipment Definition *************************************************************
# ------------------------------------------------------------------------------------------------


def get_other_equipment_definition_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None, _object_ref: openstudio.model.OtherEquipmentDefinition = None) -> dict:
    """
    Retrieve a specified OS:OtherEquipment:Definition object from the OpenStudio model by handle, name, or direct reference and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.OtherEquipmentDefinition, optional): Direct reference to the object.

    Returns:
    - dict: Dictionary containing information about the specified object.
    """
    target_object = helpers.fetch_object(
        osm_model, "OtherEquipmentDefinition", handle, name, _object_ref)

    if target_object is None:
        return {}

    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Design Level Calculation Method': target_object.designLevelCalculationMethod(),
        'Design Level {W}': target_object.designLevel().get() if target_object.designLevel().is_initialized() else None,
        'Watts per Space Floor Area {W/m2}': target_object.wattsperSpaceFloorArea().get() if target_object.wattsperSpaceFloorArea().is_initialized() else None,
        'Watts per Person {W/person}': target_object.wattsperPerson().get() if target_object.wattsperPerson().is_initialized() else None,
        'Fraction Latent': target_object.fractionLatent(),
        'Fraction Radiant': target_object.fractionRadiant(),
        'Fraction Lost': target_object.fractionLost(),
    }

    return object_dict

def get_all_other_equipment_definition_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all OS:OtherEquipment:Definition objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about an other equipment definition object.
    """
    all_objects = osm_model.getOtherEquipmentDefinitions()
    return [get_other_equipment_definition_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_other_equipment_definition_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:OtherEquipment:Definition objects from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all other equipment definition objects.
    """
    all_objects_dicts = get_all_other_equipment_definition_objects_as_dicts(osm_model)
    all_objects_df = pd.DataFrame(all_objects_dicts)

    if not all_objects_df.empty:
        if 'Name' in all_objects_df.columns:
            all_objects_df = all_objects_df.sort_values(
                by='Name', ascending=True, na_position='first').reset_index(drop=True)

    logger.info(f"The OSM model contains {all_objects_df.shape[0]} other equipment definition objects")
    return all_objects_df


# ------------------------------------------------------------------------------------------------
#  ****** Water Use Equipment ********************************************************************
# ------------------------------------------------------------------------------------------------


def get_water_use_equipment_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None, _object_ref: openstudio.model.WaterUseEquipment = None) -> dict:
    """
    Retrieve a specified OS:WaterUse:Equipment object from the OpenStudio model by handle, name, or direct reference and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.WaterUseEquipment, optional): Direct reference to the object.

    Returns:
    - dict: Dictionary containing information about the specified object.
    """
    target_object = helpers.fetch_object(
        osm_model, "WaterUseEquipment", handle, name, _object_ref)

    if target_object is None:
        return {}

    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Water Use Equipment Definition Name': target_object.definition().name().get() if target_object.definition().name().is_initialized() else None,
        'Space Name': target_object.space().get().name().get() if target_object.space().is_initialized() else None,
        'Flow Rate Fraction Schedule Name': target_object.flowRateFractionSchedule().get().name().get() if target_object.flowRateFractionSchedule().is_initialized() else None
    }

    return object_dict

def get_all_water_use_equipment_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all OS:WaterUse:Equipment objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a water use equipment object.
    """
    all_objects = osm_model.getWaterUseEquipments()
    return [get_water_use_equipment_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_water_use_equipment_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:WaterUse:Equipment objects from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all water use equipment objects.
    """
    all_objects_dicts = get_all_water_use_equipment_objects_as_dicts(osm_model)
    all_objects_df = pd.DataFrame(all_objects_dicts)

    if not all_objects_df.empty:
        if 'Name' in all_objects_df.columns:
            all_objects_df = all_objects_df.sort_values(
                by='Name', ascending=True, na_position='first').reset_index(drop=True)

    logger.info(f"The OSM model contains {all_objects_df.shape[0]} water use equipment objects")
    return all_objects_df

# ------------------------------------------------------------------------------------------------
#  ****** Water Use Equipment Definition *********************************************************
# ------------------------------------------------------------------------------------------------


def get_water_use_equipment_definition_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None, _object_ref: openstudio.model.WaterUseEquipmentDefinition = None) -> dict:
    """
    Retrieve a specified OS:WaterUse:Equipment:Definition object from the OpenStudio model by handle, name, or direct reference and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.WaterUseEquipmentDefinition, optional): Direct reference to the object.

    Returns:
    - dict: Dictionary containing information about the specified object.
    """
    target_object = helpers.fetch_object(
        osm_model, "WaterUseEquipmentDefinition", handle, name, _object_ref)

    if target_object is None:
        return {}

    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'End-Use Subcategory': target_object.endUseSubcategory(),
        'Peak Flow Rate {m3/s}': target_object.peakFlowRate(),
        'Target Temperature Schedule Name': target_object.targetTemperatureSchedule().get().name().get() if target_object.targetTemperatureSchedule().is_initialized() else None,
        'Sensible Fraction Schedule Name': target_object.sensibleFractionSchedule().get().name().get() if target_object.sensibleFractionSchedule().is_initialized() else None,
        'Latent Fraction Schedule Name': target_object.latentFractionSchedule().get().name().get() if target_object.latentFractionSchedule().is_initialized() else None
    }

    return object_dict

def get_all_water_use_equipment_definition_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all OS:WaterUse:Equipment:Definition objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a water use equipment definition object.
    """
    all_objects = osm_model.getWaterUseEquipmentDefinitions()
    return [get_water_use_equipment_definition_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_water_use_equipment_definition_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:WaterUse:Equipment:Definition objects from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all water use equipment definition objects.
    """
    all_objects_dicts = get_all_water_use_equipment_definition_objects_as_dicts(osm_model)
    all_objects_df = pd.DataFrame(all_objects_dicts)

    if not all_objects_df.empty:
        if 'Name' in all_objects_df.columns:
            all_objects_df = all_objects_df.sort_values(
                by='Name', ascending=True, na_position='first').reset_index(drop=True)

    logger.info(f"The OSM model contains {all_objects_df.shape[0]} water use equipment definition objects")
    return all_objects_df


# ------------------------------------------------------------------------------------------------
#  ****** Space Infiltration Design Flow Rate ****************************************************
# ------------------------------------------------------------------------------------------------


def get_space_infiltration_design_flowrate_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None, _object_ref: openstudio.model.SpaceInfiltrationDesignFlowRate = None) -> dict:
    """
    Retrieve a specified OS:SpaceInfiltration:DesignFlowRate object from the OpenStudio model by handle, name, or direct reference and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.SpaceInfiltrationDesignFlowRate, optional): Direct reference to the object.

    Returns:
    - dict: Dictionary containing information about the specified object.
    """
    target_object = helpers.fetch_object(
        osm_model, "SpaceInfiltrationDesignFlowRate", handle, name, _object_ref)

    if target_object is None:
        return {}

    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Space or SpaceType Name': target_object.spaceType().get().name().get() if target_object.spaceType().is_initialized() else (target_object.space().get().name().get() if target_object.space().is_initialized() else None),
        'Schedule Name': target_object.schedule().get().name().get() if target_object.schedule().is_initialized() else None,
        'Design Flow Rate Calculation Method': target_object.designFlowRateCalculationMethod(),
        'Design Flow Rate {m3/s}': target_object.designFlowRate().get() if target_object.designFlowRate().is_initialized() else None,
        'Flow per Space Floor Area {m3/s-m2}': target_object.flowperSpaceFloorArea().get() if target_object.flowperSpaceFloorArea().is_initialized() else None,
        'Flow per Exterior Surface Area {m3/s-m2}': target_object.flowperExteriorSurfaceArea().get() if target_object.flowperExteriorSurfaceArea().is_initialized()
        else (target_object.flowperExteriorWallArea().get() if target_object.flowperExteriorWallArea().is_initialized() else None),
        'Air Changes per Hour {1/hr}': target_object.airChangesperHour().get() if target_object.airChangesperHour().is_initialized() else None,
        'Constant Term Coefficient': target_object.constantTermCoefficient(),
        'Temperature Term Coefficient': target_object.temperatureTermCoefficient(),
        'Velocity Term Coefficient': target_object.velocityTermCoefficient(),
        'Velocity Squared Term Coefficient': target_object.velocitySquaredTermCoefficient()
    }

    return object_dict

def get_all_space_infiltration_design_flowrate_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all OS:SpaceInfiltration:DesignFlowRate objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a space infiltration object.
    """
    all_objects = osm_model.getSpaceInfiltrationDesignFlowRates()
    return [get_space_infiltration_design_flowrate_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_space_infiltration_design_flowrate_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:SpaceInfiltration:DesignFlowRate objects from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all space infiltration objects.
    """
    all_objects_dicts = get_all_space_infiltration_design_flowrate_objects_as_dicts(osm_model)
    all_objects_df = pd.DataFrame(all_objects_dicts)

    if not all_objects_df.empty:
        if 'Name' in all_objects_df.columns:
            all_objects_df = all_objects_df.sort_values(
                by='Name', ascending=True, na_position='first').reset_index(drop=True)

    logger.info(f"The OSM model contains {all_objects_df.shape[0]} space infiltration design flow rate objects")
    return all_objects_df

# ------------------------------------------------------------------------------------------------
#  ****** Design Specification Outdoor Air *******************************************************
# ------------------------------------------------------------------------------------------------


def get_design_specification_outdoor_air_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None, _object_ref: openstudio.model.DesignSpecificationOutdoorAir = None) -> dict:
    """
    Retrieve a specified OS:DesignSpecification:OutdoorAir object from the OpenStudio model by handle, name, or direct reference and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.DesignSpecificationOutdoorAir, optional): Direct reference to the object.

    Returns:
    - dict: Dictionary containing information about the specified object.
    """
    target_object = helpers.fetch_object(
        osm_model, "DesignSpecificationOutdoorAir", handle, name, _object_ref)

    if target_object is None:
        return {}

    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Outdoor Air Method': target_object.outdoorAirMethod(),
        'Outdoor Air Flow per Person {m3/s-person}': target_object.outdoorAirFlowperPerson(),
        'Outdoor Air Flow per Floor Area {m3/s-m2}': target_object.outdoorAirFlowperFloorArea(),
        'Outdoor Air Flow Rate {m3/s}': target_object.outdoorAirFlowRate(),
        'Outdoor Air Flow Air Changes per Hour {1/hr}': target_object.outdoorAirFlowAirChangesperHour(),
        'Outdoor Air Flow Rate Fraction Schedule Name': target_object.outdoorAirFlowRateFractionSchedule().get().name().get() if target_object.outdoorAirFlowRateFractionSchedule().is_initialized() else None
    }

    return object_dict

def get_all_design_specification_outdoor_air_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all OS:DesignSpecification:OutdoorAir objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a design specification outdoor air object.
    """
    all_objects = osm_model.getDesignSpecificationOutdoorAirs()
    return [get_design_specification_outdoor_air_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_design_specification_outdoor_air_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:DesignSpecification:OutdoorAir objects from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all design specification outdoor air objects.
    """
    all_objects_dicts = get_all_design_specification_outdoor_air_objects_as_dicts(osm_model)
    all_objects_df = pd.DataFrame(all_objects_dicts)

    if not all_objects_df.empty:
        if 'Name' in all_objects_df.columns:
            all_objects_df = all_objects_df.sort_values(
                by='Name', ascending=True, na_position='first').reset_index(drop=True)

    logger.info(f"The OSM model contains {all_objects_df.shape[0]} design specification outdoor air objects")
    return all_objects_df
