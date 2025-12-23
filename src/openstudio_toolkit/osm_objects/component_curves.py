from openstudio_toolkit.utils import helpers
import openstudio
import pandas as pd
import logging
from typing import Dict, Any, List, Optional

# Configure logger
logger = logging.getLogger(__name__)

# --------------------------------------------------
#  ***** OS:Curve:Cubic ****************************
# --------------------------------------------------

def get_curve_cubic_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: Optional[str] = None, 
    name: Optional[str] = None, 
    _object_ref: Optional[openstudio.model.CurveCubic] = None
) -> Dict[str, Any]:
    """
    Retrieve attributes of an OS:Curve:Cubic object from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.CurveCubic, optional): Direct object reference.

    Returns:
    - Dict[str, Any]: A dictionary containing curve cubic attributes.
    """  
    target_object = helpers.fetch_object(
        osm_model, "CurveCubic", handle, name, _object_ref)

    if target_object is None:
        return {}

    return {
        'Handle': str(target_object.handle()), 
        'Name': target_object.name().get() if target_object.name().is_initialized() else "Unnamed Cubic Curve", 
        'Coefficient1 Constant': target_object.coefficient1Constant(), 
        'Coefficient2 x': target_object.coefficient2x(), 
        'Coefficient3 x**2': target_object.coefficient3xPOW2(), 
        'Coefficient4 x**3': target_object.coefficient4xPOW3(), 
        'Minimum Value of x': target_object.minimumValueofx(), 
        'Maximum Value of x': target_object.maximumValueofx()
    }

def get_all_curve_cubic_objects_as_dicts(osm_model: openstudio.model.Model) -> List[Dict[str, Any]]:
    """
    Retrieve attributes for all OS:Curve:Cubic objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing cubic curve attributes.
    """
    all_objects = osm_model.getCurveCubics()
    return [get_curve_cubic_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_curve_cubic_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:Curve:Cubic objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all curve cubic attributes.
    """
    all_objects_dicts = get_all_curve_cubic_objects_as_dicts(osm_model)
    df = pd.DataFrame(all_objects_dicts)

    if not df.empty and 'Name' in df.columns:
        df = df.sort_values(by='Name', ascending=True, na_position='first').reset_index(drop=True)

    logger.info(f"Retrieved {len(df)} Curve:Cubic objects from the model.")
    return df

# --------------------------------------------------
#  ***** OS:Curve:Biquadratic **********************
# --------------------------------------------------

def get_curve_biquadratic_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: Optional[str] = None, 
    name: Optional[str] = None, 
    _object_ref: Optional[openstudio.model.CurveBiquadratic] = None
) -> Dict[str, Any]:
    """
    Retrieve attributes of an OS:Curve:Biquadratic object from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.CurveBiquadratic, optional): Direct object reference.

    Returns:
    - Dict[str, Any]: A dictionary containing biquadratic curve attributes.
    """  
    target_object = helpers.fetch_object(
        osm_model, "CurveBiquadratic", handle, name, _object_ref)

    if target_object is None:
        return {}

    return {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else "Unnamed Biquadratic Curve",
        'Coefficient1 Constant': target_object.coefficient1Constant(),
        'Coefficient2 x': target_object.coefficient2x(),
        'Coefficient3 x**2': target_object.coefficient3xPOW2(),  
        'Coefficient4 y': target_object.coefficient4y(),  
        'Coefficient5 y**2': target_object.coefficient5yPOW2(),  
        'Coefficient6 x*y': target_object.coefficient6xTIMESY(),  
        'Minimum Value of x': target_object.minimumValueofx(),
        'Maximum Value of x': target_object.maximumValueofx(),
        'Minimum Value of y': target_object.minimumValueofy(),
        'Maximum Value of y': target_object.maximumValueofy()
    }

def get_all_curve_biquadratic_objects_as_dicts(osm_model: openstudio.model.Model) -> List[Dict[str, Any]]:
    """
    Retrieve attributes for all OS:Curve:Biquadratic objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing biquadratic curve attributes.
    """
    all_objects = osm_model.getCurveBiquadratics()
    return [get_curve_biquadratic_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_curve_biquadratic_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:Curve:Biquadratic objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all curve biquadratic attributes.
    """
    all_objects_dicts = get_all_curve_biquadratic_objects_as_dicts(osm_model)
    df = pd.DataFrame(all_objects_dicts)

    if not df.empty and 'Name' in df.columns:
        df = df.sort_values(by='Name', ascending=True, na_position='first').reset_index(drop=True)

    logger.info(f"Retrieved {len(df)} Curve:Biquadratic objects from the model.")
    return df

# --------------------------------------------------
#  ***** OS:Curve:Exponent *************************
# --------------------------------------------------

def get_curve_exponent_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: Optional[str] = None, 
    name: Optional[str] = None, 
    _object_ref: Optional[openstudio.model.CurveExponent] = None
) -> Dict[str, Any]:
    """
    Retrieve attributes of an OS:Curve:Exponent object from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.CurveExponent, optional): Direct object reference.

    Returns:
    - Dict[str, Any]: A dictionary containing curve exponent attributes.
    """  
    target_object = helpers.fetch_object(
        osm_model, "CurveExponent", handle, name, _object_ref)

    if target_object is None:
        return {}

    return {
        'Handle': str(target_object.handle()), 
        'Name': target_object.name().get() if target_object.name().is_initialized() else "Unnamed Exponent Curve", 
        'Coefficient1 Constant': target_object.coefficient1Constant(), 
        'Coefficient2 Constant': target_object.coefficient2Constant(), 
        'Coefficient3 Constant': target_object.coefficient3Constant(), 
        'Minimum Value of x': target_object.minimumValueofx(), 
        'Maximum Value of x': target_object.maximumValueofx(), 
        'Minimum Curve Output': target_object.minimumCurveOutput().get() if target_object.minimumCurveOutput().is_initialized() else None, 
        'Maximum Curve Output': target_object.maximumCurveOutput().get() if target_object.maximumCurveOutput().is_initialized() else None, 
        'Input Unit Type for X': target_object.inputUnitTypeforX(), 
        'Output Unit Type': target_object.outputUnitType()
    }

def get_all_curve_exponent_objects_as_dicts(osm_model: openstudio.model.Model) -> List[Dict[str, Any]]:
    """
    Retrieve attributes for all OS:Curve:Exponent objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing exponent curve attributes.
    """
    all_objects = osm_model.getCurveExponents()
    return [get_curve_exponent_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_curve_exponent_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:Curve:Exponent objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all curve exponent attributes.
    """
    all_objects_dicts = get_all_curve_exponent_objects_as_dicts(osm_model)
    df = pd.DataFrame(all_objects_dicts)

    if not df.empty and 'Name' in df.columns:
        df = df.sort_values(by='Name', ascending=True, na_position='first').reset_index(drop=True)

    logger.info(f"Retrieved {len(df)} Curve:Exponent objects from the model.")
    return df

# --------------------------------------------------
#  ***** OS:Curve:Quadratic ************************
# --------------------------------------------------

def get_curve_quadratic_object_as_dict(
    osm_model: openstudio.model.Model, 
    handle: Optional[str] = None, 
    name: Optional[str] = None, 
    _object_ref: Optional[openstudio.model.CurveQuadratic] = None
) -> Dict[str, Any]:
    """
    Retrieve attributes of an OS:Curve:Quadratic object from the OpenStudio Model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.CurveQuadratic, optional): Direct object reference.

    Returns:
    - Dict[str, Any]: A dictionary containing quadratic curve attributes.
    """
    target_object = helpers.fetch_object(
        osm_model, "CurveQuadratic", handle, name, _object_ref)

    if target_object is None:
        return {}

    return {
        'Handle': str(target_object.handle()), 
        'Name': target_object.name().get() if target_object.name().is_initialized() else "Unnamed Quadratic Curve", 
        'Coefficient1 Constant': target_object.coefficient1Constant(), 
        'Coefficient2 x': target_object.coefficient2x(), 
        'Coefficient3 x**2': target_object.coefficient3xPOW2(), 
        'Minimum Value of x': target_object.minimumValueofx(), 
        'Maximum Value of x': target_object.maximumValueofx()
    }

def get_all_curve_quadratic_objects_as_dicts(osm_model: openstudio.model.Model) -> List[Dict[str, Any]]:
    """
    Retrieve attributes for all OS:Curve:Quadratic objects in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - List[Dict[str, Any]]: A list of dictionaries containing quadratic curve attributes.
    """
    all_objects = osm_model.getCurveQuadratics()
    return [get_curve_quadratic_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_curve_quadratic_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:Curve:Quadratic objects and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all curve quadratic attributes.
    """
    all_objects_dicts = get_all_curve_quadratic_objects_as_dicts(osm_model)
    df = pd.DataFrame(all_objects_dicts)

    if not df.empty and 'Name' in df.columns:
        df = df.sort_values(by='Name', ascending=True, na_position='first').reset_index(drop=True)

    logger.info(f"Retrieved {len(df)} Curve:Quadratic objects from the model.")
    return df