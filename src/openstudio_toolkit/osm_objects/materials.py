import logging
from typing import Any

import numpy as np
import openstudio
import pandas as pd

from openstudio_toolkit._sdk import opt
from openstudio_toolkit.osm_objects._base import build_dataframe
from openstudio_toolkit.utils import helpers

# Configure logger
logger = logging.getLogger(__name__)

STANDARD_OPAQUE_MATERIAL_COLUMNS = (
    'Handle',
    'Name',
    'Roughness',
    'Thickness {m}',
    'Conductivity {W/m-K}',
    'Density {kg/m3}',
    'Specific Heat {J/kg-K}',
    'Thermal Absorptance',
    'Solar Absorptance',
    'Visible Absorptance',
)


def get_standard_opaque_material_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: str | None = None, 
    name: str | None = None
) -> dict[str, Any]:
    """
    Retrieve attributes of an OS:StandardOpaqueMaterial object from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.

    Returns:
    - Dict[str, Any]: A dictionary containing material attributes.
    """

    if handle is not None and name is not None:
        raise ValueError(
            "Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError(
            "Either 'handle' or 'name' must be provided.")

    # Find the standard opaque material by handle or name
    if handle is not None:
        osm_object = osm_model.getStandardOpaqueMaterial(handle)
        if not osm_object:
            logger.warning(
                f"No standard opaque material found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getStandardOpaqueMaterialByName(name)
        if not osm_object:
            logger.warning(
                f"No standard opaque material found with the name: {name}")
            return {}

    target_object = opt(osm_object)

    # Define attributes to retrieve in a dictionary
    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': opt(target_object.name()),
        'Roughness': target_object.roughness(),
        'Thickness {m}': target_object.thickness(),
        'Conductivity {W/m-K}': target_object.thermalConductivity(),
        'Density {kg/m3}': target_object.density(),
        'Specific Heat {J/kg-K}': target_object.specificHeat(),
        'Thermal Absorptance': target_object.thermalAbsorptance(),
        'Solar Absorptance': target_object.solarAbsorptance(),
        'Visible Absorptance': target_object.visibleAbsorptance(),
        }

    return object_dict

def get_all_standard_opaque_material_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict[str, Any]]:
    """
    Retrieve attributes for all OS:StandardOpaqueMaterial objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing material attributes.
    """

    # Get all standard opaque materials in the OpenStudio model.
    all_objects = osm_model.getStandardOpaqueMaterials()

    all_objects_dicts = []

    for target_object in all_objects:
        handle = str(target_object.handle())
        object_dict = get_standard_opaque_material_object_as_dict(osm_model, handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_standard_opaque_material_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:StandardOpaqueMaterial objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all material attributes.
    """

    return build_dataframe(
        get_all_standard_opaque_material_objects_as_dicts(osm_model), "StandardOpaqueMaterial",
        sort_by="Name", columns=STANDARD_OPAQUE_MATERIAL_COLUMNS)

# --------------------------------------------------
#  ***** OS:Material:NoMass ************************
# --------------------------------------------------

MASSLESS_OPAQUE_MATERIAL_COLUMNS = (
    'Handle',
    'Name',
    'Roughness',
    'Thermal Resistance {m2-K/W}',
    'Thermal Absorptance',
    'Solar Absorptance',
    'Visible Absorptance',
)


def get_massless_opaque_material_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: str | None = None, 
    name: str | None = None
) -> dict[str, Any]:
    """
    Retrieve attributes of an OS:Material:NoMass object from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.

    Returns:
    - Dict[str, Any]: A dictionary containing material attributes.
    """

    if handle is not None and name is not None:
        raise ValueError(
            "Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError(
            "Either 'handle' or 'name' must be provided.")

    # Find the massless opaque material by handle or name
    if handle is not None:
        osm_object = osm_model.getMasslessOpaqueMaterial(handle)
        if not osm_object:
            logger.warning(
                f"No massless opaque material found with the handle: {handle}")
            return {}

    elif name is not None:
        osm_object = osm_model.getMasslessOpaqueMaterialByName(name)
        if not osm_object:
            logger.warning(
                f"No massless opaque material found with the name: {name}")
            return {}

    target_object = opt(osm_object)

    # Define attributes to retrieve in a dictionary
    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': opt(target_object.name()),
        'Roughness': target_object.roughness(),
        'Thermal Resistance {m2-K/W}': target_object.thermalResistance(),
        'Thermal Absorptance': opt(target_object.thermalAbsorptance()),
        'Solar Absorptance': opt(target_object.solarAbsorptance()),
        'Visible Absorptance': opt(target_object.visibleAbsorptance())
    }

    return object_dict

def get_all_massless_opaque_material_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict[str, Any]]:
    """
    Retrieve attributes for all OS:Material:NoMass objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing material attributes.
    """

    # Get all massless opaque materials in the OpenStudio model.
    all_objects = osm_model.getMasslessOpaqueMaterials()

    all_objects_dicts = []

    for target_object in all_objects:
        handle = str(target_object.handle())
        object_dict = get_massless_opaque_material_object_as_dict(osm_model, handle)
        all_objects_dicts.append(object_dict)

    return all_objects_dicts


def get_all_massless_opaque_material_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:Material:NoMass objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all material attributes.
    """

    return build_dataframe(
        get_all_massless_opaque_material_objects_as_dicts(osm_model), "Material:NoMass",
        sort_by="Name", columns=MASSLESS_OPAQUE_MATERIAL_COLUMNS)

# --------------------------------------------------


def get_all_opaque_material_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all opaque material objects from an OpenStudio model as a DataFrame.

    Args:
        osm_model (openstudio.model.Model): The OpenStudio model to extract materials from.

    Returns:
        pd.DataFrame: DataFrame containing all opaque materials with their properties.
    """
    # Get all standard opaque materials and massless opaque materials
    all_standard_opaque_materials_df = get_all_standard_opaque_material_objects_as_dataframe(osm_model)
    get_all_massless_opaque_materials_df = get_all_massless_opaque_material_objects_as_dataframe(osm_model)

    # Add 'Material Type' column to each DataFrame
    all_standard_opaque_materials_df['Material Type'] = 'Standard'
    get_all_massless_opaque_materials_df['Material Type'] = 'NoMass'

    # Calculate Thermal Resistance {m2-K/W}
    all_standard_opaque_materials_df['Thermal Resistance {m2-K/W}'] = all_standard_opaque_materials_df['Thickness {m}'] / all_standard_opaque_materials_df['Conductivity {W/m-K}']

    # Concatenate vertically
    all_opaque_materials_df = pd.concat(
        [all_standard_opaque_materials_df, get_all_massless_opaque_materials_df],
        ignore_index=True,
        sort=False
    )

    # Move 'Material Type' to the third position (index 2)
    cols = list(all_opaque_materials_df.columns)
    cols.remove('Material Type')  # Remove from current position
    cols.insert(1, 'Material Type')  # Insert at position 2 (third position)
    all_opaque_materials_df = all_opaque_materials_df[cols]

    # Replace NaN with None if desired
    all_opaque_materials_df = all_opaque_materials_df.replace({np.nan: None})

    return all_opaque_materials_df


# --------------------------------------------------
#  ***** OS:WindowMaterial:SimpleGlazingSystem ***
# --------------------------------------------------

WINDOW_MATERIAL_SIMPLE_GLAZING_SYSTEM_COLUMNS = (
    'Handle',
    'Name',
    'U-Factor {W/m2-K}',
    'Solar Heat Gain Coefficient',
    'Visible Transmittance',
)

def get_window_material_simple_glazing_system_object_as_dict(
    osm_model: openstudio.model.Model,
    handle: str | None = None,
    name: str | None = None,
    _object_ref: openstudio.model.SimpleGlazing | None = None
) -> dict[str, Any]:
    """
    Retrieve attributes of an OS:WindowMaterial:SimpleGlazingSystem from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.SimpleGlazing, optional): Direct object reference.

    Returns:
    - Dict[str, Any]: A dictionary with one entry per IDD field (node fields give the node name).
    """
    target_object = helpers.fetch_object(
        osm_model, "SimpleGlazing", handle, name, _object_ref)

    if target_object is None:
        return {}

    return {
        'Handle': str(target_object.handle()),
        'Name': opt(target_object.name()),
        'U-Factor {W/m2-K}': target_object.uFactor(),
        'Solar Heat Gain Coefficient': target_object.solarHeatGainCoefficient(),
        'Visible Transmittance': opt(target_object.visibleTransmittance()),
    }

def get_all_window_material_simple_glazing_system_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict[str, Any]]:
    """
    Retrieve attributes for all OS:WindowMaterial:SimpleGlazingSystem objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries, one per object.
    """
    all_objects = osm_model.getSimpleGlazings()
    return [get_window_material_simple_glazing_system_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_window_material_simple_glazing_system_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:WindowMaterial:SimpleGlazingSystem objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame with the columns of WINDOW_MATERIAL_SIMPLE_GLAZING_SYSTEM_COLUMNS.
    """
    all_objects_dicts = get_all_window_material_simple_glazing_system_objects_as_dicts(osm_model)
    return build_dataframe(
        all_objects_dicts, "WindowMaterial:SimpleGlazingSystem", sort_by="Name", columns=WINDOW_MATERIAL_SIMPLE_GLAZING_SYSTEM_COLUMNS)
