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

from openstudio_toolkit._sdk import opt, optional_name, related_name
from openstudio_toolkit.osm_objects._base import build_all_dicts, build_dataframe
from openstudio_toolkit.utils import helpers

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
#  OS:People
# ---------------------------------------------------------------------------

PEOPLE_COLUMNS = (
    'Handle',
    'Name',
    'People Definition Name',
    'Space or SpaceType Name',
    'Number of People Schedule Name',
    'Activity Level Schedule Name',
    'Surface Name/Angle Factor List Name',
    'Work Efficiency Schedule Name',
    'Clothing Insulation Schedule Name',
    'Air Velocity Schedule Name',
    'Multiplier',
)


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

    return {
        'Handle': str(target_object.handle()),
        'Name': opt(target_object.name()),
        'People Definition Name': related_name(target_object, "People Definition Name"),
        'Space or SpaceType Name': related_name(target_object, "Space or SpaceType Name"),
        'Number of People Schedule Name': optional_name(target_object.numberofPeopleSchedule()),
        'Activity Level Schedule Name': optional_name(target_object.activityLevelSchedule()),
        'Surface Name/Angle Factor List Name': None,  # Not accessible via SDK
        'Work Efficiency Schedule Name': optional_name(target_object.workEfficiencySchedule()),
        'Clothing Insulation Schedule Name': optional_name(target_object.clothingInsulationSchedule()),
        'Air Velocity Schedule Name': optional_name(target_object.airVelocitySchedule()),
        'Multiplier': target_object.multiplier(),
    }


def get_all_people_objects_as_dicts(
    osm_model: openstudio.model.Model,
) -> list[dict[str, Any]]:
    """Retrieve attributes for all OS:People objects."""
    return build_all_dicts(
        osm_model,
        "getPeoples",
        get_people_object_as_dict,
    )


def get_all_people_objects_as_dataframe(
    osm_model: openstudio.model.Model,
) -> pd.DataFrame:
    """Retrieve all OS:People objects as a DataFrame."""
    return build_dataframe(
        get_all_people_objects_as_dicts(osm_model),
        "People",
        sort_by="Name", columns=PEOPLE_COLUMNS,
    )


# ---------------------------------------------------------------------------
#  OS:People:Definition
# ---------------------------------------------------------------------------

PEOPLE_DEFINITION_COLUMNS = (
    'Handle',
    'Name',
    'Number of People Calculation Method',
    'Number of People {people}',
    'People per Space Floor Area {person/m2}',
    'Space Floor Area per Person {m2/person}',
    'Fraction Radiant',
    'Sensible Heat Fraction',
    'Carbon Dioxide Generation Rate {m3/s-W}',
)


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
        'Name': opt(target_object.name()),
        'Number of People Calculation Method': target_object.numberofPeopleCalculationMethod(),
        'Number of People {people}': opt(target_object.numberofPeople()),
        'People per Space Floor Area {person/m2}': opt(target_object.peopleperSpaceFloorArea()),
        'Space Floor Area per Person {m2/person}': opt(target_object.spaceFloorAreaperPerson()),
        'Fraction Radiant': target_object.fractionRadiant(),
        'Sensible Heat Fraction': opt(target_object.sensibleHeatFraction()),
        'Carbon Dioxide Generation Rate {m3/s-W}': target_object.carbonDioxideGenerationRate(),
    }


def get_all_people_definition_objects_as_dicts(
    osm_model: openstudio.model.Model,
) -> list[dict[str, Any]]:
    """Retrieve attributes for all OS:People:Definition objects."""
    return build_all_dicts(
        osm_model,
        "getPeopleDefinitions",
        get_people_definition_object_as_dict,
    )


def get_all_people_definition_objects_as_dataframe(
    osm_model: openstudio.model.Model,
) -> pd.DataFrame:
    """Retrieve all OS:People:Definition objects as a DataFrame."""
    return build_dataframe(
        get_all_people_definition_objects_as_dicts(osm_model),
        "PeopleDefinition",
        sort_by="Name", columns=PEOPLE_DEFINITION_COLUMNS,
    )


# ---------------------------------------------------------------------------
#  OS:Lights
# ---------------------------------------------------------------------------

LIGHTS_COLUMNS = (
    'Handle',
    'Name',
    'Lights Definition Name',
    'Space or SpaceType Name',
    'Schedule Name',
    'Fraction Replaceable',
    'Multiplier',
    'End-Use Subcategory',
)


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

    return {
        'Handle': str(target_object.handle()),
        'Name': opt(target_object.name()),
        'Lights Definition Name': related_name(target_object, "Lights Definition Name"),
        'Space or SpaceType Name': related_name(target_object, "Space or SpaceType Name"),
        'Schedule Name': optional_name(target_object.schedule()),
        'Fraction Replaceable': target_object.fractionReplaceable(),
        'Multiplier': target_object.multiplier(),
        'End-Use Subcategory': target_object.endUseSubcategory(),
    }


def get_all_lights_objects_as_dicts(
    osm_model: openstudio.model.Model,
) -> list[dict[str, Any]]:
    """Retrieve attributes for all OS:Lights objects."""
    return build_all_dicts(
        osm_model,
        "getLightss",
        get_lights_object_as_dict,
    )


def get_all_lights_objects_as_dataframe(
    osm_model: openstudio.model.Model,
) -> pd.DataFrame:
    """Retrieve all OS:Lights objects as a DataFrame."""
    return build_dataframe(
        get_all_lights_objects_as_dicts(osm_model),
        "Lights",
        sort_by="Name", columns=LIGHTS_COLUMNS,
    )


# ---------------------------------------------------------------------------
#  OS:Lights:Definition
# ---------------------------------------------------------------------------

LIGHTS_DEFINITION_COLUMNS = (
    'Handle',
    'Name',
    'Design Level Calculation Method',
    'Lighting Level {W}',
    'Watts per Space Floor Area {W/m2}',
    'Watts per Person {W/person}',
    'Fraction Radiant',
    'Fraction Visible',
    'Return Air Fraction',
)


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
        'Name': opt(target_object.name()),
        'Design Level Calculation Method': target_object.designLevelCalculationMethod(),
        'Lighting Level {W}': opt(target_object.lightingLevel()),
        'Watts per Space Floor Area {W/m2}': opt(target_object.wattsperSpaceFloorArea()),
        'Watts per Person {W/person}': opt(target_object.wattsperPerson()),
        'Fraction Radiant': target_object.fractionRadiant(),
        'Fraction Visible': target_object.fractionVisible(),
        'Return Air Fraction': target_object.returnAirFraction(),
    }


def get_all_lights_definition_objects_as_dicts(
    osm_model: openstudio.model.Model,
) -> list[dict[str, Any]]:
    """Retrieve attributes for all OS:Lights:Definition objects."""
    return build_all_dicts(
        osm_model,
        "getLightsDefinitions",
        get_lights_definition_object_as_dict,
    )


def get_all_lights_definition_objects_as_dataframe(
    osm_model: openstudio.model.Model,
) -> pd.DataFrame:
    """Retrieve all OS:Lights:Definition objects as a DataFrame."""
    return build_dataframe(
        get_all_lights_definition_objects_as_dicts(osm_model),
        "LightsDefinition",
        sort_by="Name", columns=LIGHTS_DEFINITION_COLUMNS,
    )


# ---------------------------------------------------------------------------
#  OS:ElectricEquipment
# ---------------------------------------------------------------------------

ELECTRIC_EQUIPMENT_COLUMNS = (
    'Handle',
    'Name',
    'Electric Equipment Definition Name',
    'Space or SpaceType Name',
    'Schedule Name',
    'Multiplier',
    'End-Use Subcategory',
)


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

    return {
        'Handle': str(target_object.handle()),
        'Name': opt(target_object.name()),
        'Electric Equipment Definition Name': related_name(target_object, "Electric Equipment Definition Name"),
        'Space or SpaceType Name': related_name(target_object, "Space or SpaceType Name"),
        'Schedule Name': optional_name(target_object.schedule()),
        'Multiplier': target_object.multiplier(),
        'End-Use Subcategory': target_object.endUseSubcategory(),
    }


def get_all_electric_equipment_objects_as_dicts(
    osm_model: openstudio.model.Model,
) -> list[dict[str, Any]]:
    """Retrieve attributes for all OS:ElectricEquipment objects."""
    return build_all_dicts(
        osm_model,
        "getElectricEquipments",
        get_electric_equipment_object_as_dict,
    )


def get_all_electric_equipment_objects_as_dataframe(
    osm_model: openstudio.model.Model,
) -> pd.DataFrame:
    """Retrieve all OS:ElectricEquipment objects as a DataFrame."""
    return build_dataframe(
        get_all_electric_equipment_objects_as_dicts(osm_model),
        "ElectricEquipment",
        sort_by="Name", columns=ELECTRIC_EQUIPMENT_COLUMNS,
    )


# ---------------------------------------------------------------------------
#  OS:ElectricEquipment:Definition
# ---------------------------------------------------------------------------

ELECTRIC_EQUIPMENT_DEFINITION_COLUMNS = (
    'Handle',
    'Name',
    'Design Level Calculation Method',
    'Design Level {W}',
    'Watts per Space Floor Area {W/m2}',
    'Watts per Person {W/person}',
    'Fraction Latent',
    'Fraction Radiant',
    'Fraction Lost',
)


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
        'Name': opt(target_object.name()),
        'Design Level Calculation Method': target_object.designLevelCalculationMethod(),
        'Design Level {W}': opt(target_object.designLevel()),
        'Watts per Space Floor Area {W/m2}': opt(target_object.wattsperSpaceFloorArea()),
        'Watts per Person {W/person}': opt(target_object.wattsperPerson()),
        'Fraction Latent': target_object.fractionLatent(),
        'Fraction Radiant': target_object.fractionRadiant(),
        'Fraction Lost': target_object.fractionLost(),
    }


def get_all_electric_equipment_definition_objects_as_dicts(
    osm_model: openstudio.model.Model,
) -> list[dict[str, Any]]:
    """Retrieve attributes for all OS:ElectricEquipment:Definition objects."""
    return build_all_dicts(
        osm_model,
        "getElectricEquipmentDefinitions",
        get_electric_equipment_definition_object_as_dict,
    )


def get_all_electric_equipment_definition_objects_as_dataframe(
    osm_model: openstudio.model.Model,
) -> pd.DataFrame:
    """Retrieve all OS:ElectricEquipment:Definition objects as a DataFrame."""
    return build_dataframe(
        get_all_electric_equipment_definition_objects_as_dicts(osm_model),
        "ElectricEquipmentDefinition",
        sort_by="Name", columns=ELECTRIC_EQUIPMENT_DEFINITION_COLUMNS,
    )


# ------------------------------------------------------------------------------------------------
#  ****** LEGACY OBJECTS (NOT REFACTORED) *******************************************************
#  The following objects remain in their original v0.1.0 implementation style
# ------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------
#  ****** Gas Equipment **************************************************************************
# ------------------------------------------------------------------------------------------------

GAS_EQUIPMENT_COLUMNS = (
    'Handle',
    'Name',
    'Gas Equipment Definition Name',
    'Space or SpaceType Name',
    'Schedule Name',
    'Multiplier',
    'End-Use Subcategory',
)


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
        'Name': opt(target_object.name()),
        'Gas Equipment Definition Name': related_name(target_object, "Gas Equipment Definition Name"),
        'Space or SpaceType Name': related_name(target_object, "Space or SpaceType Name"),
        'Schedule Name': optional_name(target_object.schedule()),
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
    return build_dataframe(
        get_all_gas_equipment_objects_as_dicts(osm_model), "GasEquipment",
        sort_by="Name", columns=GAS_EQUIPMENT_COLUMNS)


# ------------------------------------------------------------------------------------------------
#  ****** Gas Equipment Definition ***************************************************************
# ------------------------------------------------------------------------------------------------


GAS_EQUIPMENT_DEFINITION_COLUMNS = (
    'Handle',
    'Name',
    'Design Level Calculation Method',
    'Design Level {W}',
    'Watts per Space Floor Area {W/m2}',
    'Watts per Person {W/person}',
    'Fraction Latent',
    'Fraction Radiant',
    'Fraction Lost',
)


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
        'Name': opt(target_object.name()),
        'Design Level Calculation Method': target_object.designLevelCalculationMethod(),
        'Design Level {W}': opt(target_object.designLevel()),
        'Watts per Space Floor Area {W/m2}': opt(target_object.wattsperSpaceFloorArea()),
        'Watts per Person {W/person}': opt(target_object.wattsperPerson()),
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
    return build_dataframe(
        get_all_gas_equipment_definition_objects_as_dicts(osm_model), "GasEquipmentDefinition",
        sort_by="Name", columns=GAS_EQUIPMENT_DEFINITION_COLUMNS)


# ------------------------------------------------------------------------------------------------
#  ****** Steam Equipment ************************************************************************
# ------------------------------------------------------------------------------------------------
STEAM_EQUIPMENT_COLUMNS = (
    'Handle',
    'Name',
    'Steam Equipment Definition Name',
    'Space or SpaceType Name',
    'Schedule Name',
    'Multiplier',
    'End-Use Subcategory',
)


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
        'Name': opt(target_object.name()),
        'Steam Equipment Definition Name': related_name(target_object, "Steam Equipment Definition Name"),
        'Space or SpaceType Name': related_name(target_object, "Space or SpaceType Name"),
        'Schedule Name': optional_name(target_object.schedule()),
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
    return build_dataframe(
        get_all_steam_equipment_objects_as_dicts(osm_model), "SteamEquipment",
        sort_by="Name", columns=STEAM_EQUIPMENT_COLUMNS)


# ------------------------------------------------------------------------------------------------
#  ****** Steam Equipment Definition *************************************************************
# ------------------------------------------------------------------------------------------------

STEAM_EQUIPMENT_DEFINITION_COLUMNS = (
    'Handle',
    'Name',
    'Design Level Calculation Method',
    'Design Level {W}',
    'Watts per Space Floor Area {W/m2}',
    'Watts per Person {W/person}',
    'Fraction Latent',
    'Fraction Radiant',
    'Fraction Lost',
)


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
        'Name': opt(target_object.name()),
        'Design Level Calculation Method': target_object.designLevelCalculationMethod(),
        'Design Level {W}': opt(target_object.designLevel()),
        'Watts per Space Floor Area {W/m2}': opt(target_object.wattsperSpaceFloorArea()),
        'Watts per Person {W/person}': opt(target_object.wattsperPerson()),
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
    return build_dataframe(
        get_all_steam_equipment_definition_objects_as_dicts(osm_model), "SteamEquipmentDefinition",
        sort_by="Name", columns=STEAM_EQUIPMENT_DEFINITION_COLUMNS)

# ------------------------------------------------------------------------------------------------
#  ****** Other Equipment ************************************************************************
# ------------------------------------------------------------------------------------------------


OTHER_EQUIPMENT_COLUMNS = (
    'Handle',
    'Name',
    'Other Equipment Definition Name',
    'Space or SpaceType Name',
    'Schedule Name',
    'Multiplier',
    'Fuel Type',
    'End-Use Subcategory',
)


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
        'Name': opt(target_object.name()),
        'Other Equipment Definition Name': related_name(target_object, "Other Equipment Definition Name"),
        'Space or SpaceType Name': related_name(target_object, "Space or SpaceType Name"),
        'Schedule Name': optional_name(target_object.schedule()),
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
    return build_dataframe(
        get_all_other_equipment_objects_as_dicts(osm_model), "OtherEquipment",
        sort_by="Name", columns=OTHER_EQUIPMENT_COLUMNS)

# ------------------------------------------------------------------------------------------------
#  ****** Other Equipment Definition *************************************************************
# ------------------------------------------------------------------------------------------------


OTHER_EQUIPMENT_DEFINITION_COLUMNS = (
    'Handle',
    'Name',
    'Design Level Calculation Method',
    'Design Level {W}',
    'Watts per Space Floor Area {W/m2}',
    'Watts per Person {W/person}',
    'Fraction Latent',
    'Fraction Radiant',
    'Fraction Lost',
)


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
        'Name': opt(target_object.name()),
        'Design Level Calculation Method': target_object.designLevelCalculationMethod(),
        'Design Level {W}': opt(target_object.designLevel()),
        'Watts per Space Floor Area {W/m2}': opt(target_object.wattsperSpaceFloorArea()),
        'Watts per Person {W/person}': opt(target_object.wattsperPerson()),
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
    return build_dataframe(
        get_all_other_equipment_definition_objects_as_dicts(osm_model), "OtherEquipmentDefinition",
        sort_by="Name", columns=OTHER_EQUIPMENT_DEFINITION_COLUMNS)


# ------------------------------------------------------------------------------------------------
#  ****** Water Use Equipment ********************************************************************
# ------------------------------------------------------------------------------------------------


WATER_USE_EQUIPMENT_COLUMNS = (
    'Handle',
    'Name',
    'Water Use Equipment Definition Name',
    'Space Name',
    'Flow Rate Fraction Schedule Name',
)


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
        'Name': opt(target_object.name()),
        'Water Use Equipment Definition Name': related_name(target_object, "Water Use Equipment Definition Name"),
        'Space Name': optional_name(target_object.space()),
        'Flow Rate Fraction Schedule Name': optional_name(target_object.flowRateFractionSchedule())
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
    return build_dataframe(
        get_all_water_use_equipment_objects_as_dicts(osm_model), "WaterUseEquipment",
        sort_by="Name", columns=WATER_USE_EQUIPMENT_COLUMNS)

# ------------------------------------------------------------------------------------------------
#  ****** Water Use Equipment Definition *********************************************************
# ------------------------------------------------------------------------------------------------


WATER_USE_EQUIPMENT_DEFINITION_COLUMNS = (
    'Handle',
    'Name',
    'End-Use Subcategory',
    'Peak Flow Rate {m3/s}',
    'Target Temperature Schedule Name',
    'Sensible Fraction Schedule Name',
    'Latent Fraction Schedule Name',
)


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
        'Name': opt(target_object.name()),
        'End-Use Subcategory': target_object.endUseSubcategory(),
        'Peak Flow Rate {m3/s}': target_object.peakFlowRate(),
        'Target Temperature Schedule Name': optional_name(target_object.targetTemperatureSchedule()),
        'Sensible Fraction Schedule Name': optional_name(target_object.sensibleFractionSchedule()),
        'Latent Fraction Schedule Name': optional_name(target_object.latentFractionSchedule())
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
    return build_dataframe(
        get_all_water_use_equipment_definition_objects_as_dicts(osm_model), "WaterUseEquipmentDefinition",
        sort_by="Name", columns=WATER_USE_EQUIPMENT_DEFINITION_COLUMNS)


# ------------------------------------------------------------------------------------------------
#  ****** Space Infiltration Design Flow Rate ****************************************************
# ------------------------------------------------------------------------------------------------


SPACE_INFILTRATION_DESIGN_FLOWRATE_COLUMNS = (
    'Handle',
    'Name',
    'Space or SpaceType Name',
    'Schedule Name',
    'Design Flow Rate Calculation Method',
    'Design Flow Rate {m3/s}',
    'Flow per Space Floor Area {m3/s-m2}',
    'Flow per Exterior Surface Area {m3/s-m2}',
    'Air Changes per Hour {1/hr}',
    'Constant Term Coefficient',
    'Temperature Term Coefficient',
    'Velocity Term Coefficient',
    'Velocity Squared Term Coefficient',
)


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
        'Name': opt(target_object.name()),
        'Space or SpaceType Name': related_name(target_object, "Space or SpaceType Name"),
        'Schedule Name': optional_name(target_object.schedule()),
        'Design Flow Rate Calculation Method': target_object.designFlowRateCalculationMethod(),
        'Design Flow Rate {m3/s}': opt(target_object.designFlowRate()),
        'Flow per Space Floor Area {m3/s-m2}': opt(target_object.flowperSpaceFloorArea()),
        'Flow per Exterior Surface Area {m3/s-m2}': (
            opt(target_object.flowperExteriorSurfaceArea())
            if target_object.flowperExteriorSurfaceArea().is_initialized()
            else opt(target_object.flowperExteriorWallArea())
            if target_object.flowperExteriorWallArea().is_initialized()
            else None
        ),
        'Air Changes per Hour {1/hr}': opt(target_object.airChangesperHour()),
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
    return build_dataframe(
        get_all_space_infiltration_design_flowrate_objects_as_dicts(osm_model), "SpaceInfiltrationDesignFlowRate",
        sort_by="Name", columns=SPACE_INFILTRATION_DESIGN_FLOWRATE_COLUMNS)

# ------------------------------------------------------------------------------------------------
#  ****** Design Specification Outdoor Air *******************************************************
# ------------------------------------------------------------------------------------------------


DESIGN_SPECIFICATION_OUTDOOR_AIR_COLUMNS = (
    'Handle',
    'Name',
    'Outdoor Air Method',
    'Outdoor Air Flow per Person {m3/s-person}',
    'Outdoor Air Flow per Floor Area {m3/s-m2}',
    'Outdoor Air Flow Rate {m3/s}',
    'Outdoor Air Flow Air Changes per Hour {1/hr}',
    'Outdoor Air Flow Rate Fraction Schedule Name',
)


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
        'Name': opt(target_object.name()),
        'Outdoor Air Method': target_object.outdoorAirMethod(),
        'Outdoor Air Flow per Person {m3/s-person}': target_object.outdoorAirFlowperPerson(),
        'Outdoor Air Flow per Floor Area {m3/s-m2}': target_object.outdoorAirFlowperFloorArea(),
        'Outdoor Air Flow Rate {m3/s}': target_object.outdoorAirFlowRate(),
        'Outdoor Air Flow Air Changes per Hour {1/hr}': target_object.outdoorAirFlowAirChangesperHour(),
        'Outdoor Air Flow Rate Fraction Schedule Name': optional_name(target_object.outdoorAirFlowRateFractionSchedule())
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
    return build_dataframe(
        get_all_design_specification_outdoor_air_objects_as_dicts(osm_model), "DesignSpecificationOutdoorAir",
        sort_by="Name", columns=DESIGN_SPECIFICATION_OUTDOOR_AIR_COLUMNS)
