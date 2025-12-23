import openstudio
import pandas as pd
import logging
from typing import Dict, Any, List, Optional
from openstudio_toolkit.utils import helpers

# Configure logger
logger = logging.getLogger(__name__)

# --------------------------------------------------
#  ***** OS:Exterior:FuelEquipment:Definition ******
# --------------------------------------------------

def get_exterior_fuel_equipment_definition_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: Optional[str] = None, 
    name: Optional[str] = None, 
    _object_ref: Optional[openstudio.model.ExteriorFuelEquipmentDefinition] = None
) -> Dict[str, Any]:
    """
    Retrieve attributes of an OS:Exterior:FuelEquipment:Definition from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.ExteriorFuelEquipmentDefinition, optional): Direct object reference.

    Returns:
    - Dict[str, Any]: A dictionary containing exterior fuel equipment definition attributes.
    """  
    target_object = helpers.fetch_object(
        osm_model, "ExteriorFuelEquipmentDefinition", handle, name, _object_ref)

    if target_object is None:
        return {}

    return {
        'Handle': str(target_object.handle()), 
        'Name': target_object.name().get() if target_object.name().is_initialized() else "Unnamed Exterior Fuel Equipment Definition", 
        'Design Level {W}': target_object.designLevel()
    }

def get_all_exterior_fuel_equipment_definition_objects_as_dicts(osm_model: openstudio.model.Model) -> List[Dict[str, Any]]:
    """
    Retrieve attributes for all OS:Exterior:FuelEquipment:Definition objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing exterior fuel equipment definition attributes.
    """
    all_objects = osm_model.getExteriorFuelEquipmentDefinitions()
    return [get_exterior_fuel_equipment_definition_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_exterior_fuel_equipment_definition_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:Exterior:FuelEquipment:Definition objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all exterior fuel equipment definition attributes.
    """
    all_objects_dicts = get_all_exterior_fuel_equipment_definition_objects_as_dicts(osm_model)
    df = pd.DataFrame(all_objects_dicts)

    if not df.empty and 'Name' in df.columns:
        df = df.sort_values(by='Name', ascending=True, na_position='first').reset_index(drop=True)

    logger.info(f"Retrieved {len(df)} ExteriorFuelEquipmentDefinition objects from the model.")
    return df

# --------------------------------------------------
#  ***** OS:Exterior:WaterEquipment:Definition *****
# --------------------------------------------------

def get_exterior_water_equipment_definition_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: Optional[str] = None, 
    name: Optional[str] = None, 
    _object_ref: Optional[openstudio.model.ExteriorWaterEquipmentDefinition] = None
) -> Dict[str, Any]:
    """
    Retrieve attributes of an OS:Exterior:WaterEquipment:Definition from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.ExteriorWaterEquipmentDefinition, optional): Direct object reference.

    Returns:
    - Dict[str, Any]: A dictionary containing exterior water equipment definition attributes.
    """  
    target_object = helpers.fetch_object(
        osm_model, "ExteriorWaterEquipmentDefinition", handle, name, _object_ref)

    if target_object is None:
        return {}

    return {
        'Handle': str(target_object.handle()), 
        'Name': target_object.name().get() if target_object.name().is_initialized() else "Unnamed Exterior Water Equipment Definition", 
        'Design Level {m3/s}': target_object.designLevel()
    }

def get_all_exterior_water_equipment_definition_objects_as_dicts(osm_model: openstudio.model.Model) -> List[Dict[str, Any]]:
    """
    Retrieve attributes for all OS:Exterior:WaterEquipment:Definition objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing exterior water equipment definition attributes.
    """
    all_objects = osm_model.getExteriorWaterEquipmentDefinitions()
    return [get_exterior_water_equipment_definition_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_exterior_water_equipment_definition_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:Exterior:WaterEquipment:Definition objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all exterior water equipment definition attributes.
    """
    all_objects_dicts = get_all_exterior_water_equipment_definition_objects_as_dicts(osm_model)
    df = pd.DataFrame(all_objects_dicts)

    if not df.empty and 'Name' in df.columns:
        df = df.sort_values(by='Name', ascending=True, na_position='first').reset_index(drop=True)

    logger.info(f"Retrieved {len(df)} ExteriorWaterEquipmentDefinition objects from the model.")
    return df

# --------------------------------------------------
#  ***** OS:Exterior:Lights:Definition *************
# --------------------------------------------------

def get_exterior_lights_definition_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: Optional[str] = None, 
    name: Optional[str] = None, 
    _object_ref: Optional[openstudio.model.ExteriorLightsDefinition] = None
) -> Dict[str, Any]:
    """
    Retrieve attributes of an OS:Exterior:Lights:Definition from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.ExteriorLightsDefinition, optional): Direct object reference.

    Returns:
    - Dict[str, Any]: A dictionary containing exterior lights definition attributes.
    """  
    target_object = helpers.fetch_object(
        osm_model, "ExteriorLightsDefinition", handle, name, _object_ref)

    if target_object is None:
        return {}

    return {
        'Handle': str(target_object.handle()), 
        'Name': target_object.name().get() if target_object.name().is_initialized() else "Unnamed Exterior Lights Definition", 
        'Design Level {W}': target_object.designLevel()
    }

def get_all_exterior_lights_definition_objects_as_dicts(osm_model: openstudio.model.Model) -> List[Dict[str, Any]]:
    """
    Retrieve attributes for all OS:Exterior:Lights:Definition objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing exterior lights definition attributes.
    """
    all_objects = osm_model.getExteriorLightsDefinitions()
    return [get_exterior_lights_definition_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_exterior_lights_definition_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:Exterior:Lights:Definition objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all exterior lights definition attributes.
    """
    all_objects_dicts = get_all_exterior_lights_definition_objects_as_dicts(osm_model)
    df = pd.DataFrame(all_objects_dicts)

    if not df.empty and 'Name' in df.columns:
        df = df.sort_values(by='Name', ascending=True, na_position='first').reset_index(drop=True)

    logger.info(f"Retrieved {len(df)} ExteriorLightsDefinition objects from the model.")
    return df