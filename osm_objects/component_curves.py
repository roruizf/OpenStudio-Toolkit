import openstudio
import pandas as pd

def get_all_cubic_curves_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all Cubic Curves from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all spaces.
    """

    # Get all spaces in the OpenStudio model.
    all_cubic_curves = osm_model.getCurveCubics()

    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_cubic_curves],
        'Name': [x.name().get() for x in all_cubic_curves],
        'Coefficient1 Constant': [x.coefficient1Constant() for x in all_cubic_curves],
        'Coefficient2 x': [x.coefficient2x() for x in all_cubic_curves],
        'Coefficient3 x**2': [x.coefficient3xPOW2() for x in all_cubic_curves],  
        'Coefficient4 x**3': [x.coefficient4xPOW3() for x in all_cubic_curves],  
        'Minimum Value of x': [x.minimumValueofx() for x in all_cubic_curves],
        'Maximum Value of x': [x.maximumValueofx() for x in all_cubic_curves]
    }

    # Create a DataFrame of all spaces.
    all_cubic_curves_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_cubic_curves_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_cubic_curves_df = all_cubic_curves_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(f"The OSM model contains {all_cubic_curves_df.shape[0]} cubic curves")

    return all_cubic_curves_df


def get_all_quadratic_curves_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all Quadratic Curves from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all spaces.
    """

    # Get all spaces in the OpenStudio model.
    all_quadratic_curves = osm_model.getCurveQuadratics()

    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_quadratic_curves],
        'Name': [x.name().get() for x in all_quadratic_curves],
        'Coefficient1 Constant': [x.coefficient1Constant() for x in all_quadratic_curves],
        'Coefficient2 x': [x.coefficient2x() for x in all_quadratic_curves],
        'Coefficient3 x**2': [x.coefficient3xPOW2() for x in all_quadratic_curves],  
        'Minimum Value of x': [x.minimumValueofx() for x in all_quadratic_curves],
        'Maximum Value of x': [x.maximumValueofx() for x in all_quadratic_curves]
    }

    # Create a DataFrame of all spaces.
    all_quadratic_curves_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_quadratic_curves_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_quadratic_curves_df = all_quadratic_curves_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(f"The OSM model contains {all_quadratic_curves_df.shape[0]} quadratic curves")

    return all_quadratic_curves_df

def get_all_biquadratic_curves_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all Biquadratic Curves from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all spaces.
    """

    # Get all spaces in the OpenStudio model.
    all_biquadratic_curves = osm_model.getCurveBiquadratics()

    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_biquadratic_curves],
        'Name': [x.name().get() for x in all_biquadratic_curves],
        'Coefficient1 Constant': [x.coefficient1Constant() for x in all_biquadratic_curves],
        'Coefficient2 x': [x.coefficient2x() for x in all_biquadratic_curves],
        'Coefficient3 x**2': [x.coefficient3xPOW2() for x in all_biquadratic_curves],  
        'Coefficient4 y': [x.coefficient4y() for x in all_biquadratic_curves],  
        'Coefficient5 y**2': [x.coefficient5yPOW2() for x in all_biquadratic_curves],  
        'Coefficient6 x*y': [x.coefficient6xTIMESY() for x in all_biquadratic_curves],  
        'Minimum Value of x': [x.minimumValueofx() for x in all_biquadratic_curves],
        'Maximum Value of x': [x.maximumValueofx() for x in all_biquadratic_curves],
        'Minimum Value of y': [x.minimumValueofy() for x in all_biquadratic_curves],
        'Maximum Value of y': [x.maximumValueofy() for x in all_biquadratic_curves]
    }

    # Create a DataFrame of all spaces.
    all_biquadratic_curves_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_biquadratic_curves_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_biquadratic_curves_df = all_biquadratic_curves_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(f"The OSM model contains {all_biquadratic_curves_df.shape[0]} biquadratic curves")

    return all_biquadratic_curves_df

def get_all_exponent_curves_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all Exponent Curves from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all spaces.
    """

    # Get all spaces in the OpenStudio model.
    all_exponent_curves = osm_model.getCurveExponents()

    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_exponent_curves],
        'Name': [x.name().get() for x in all_exponent_curves],
        'Coefficient1 Constant': [x.coefficient1Constant() for x in all_exponent_curves],
        'Coefficient2 Constant': [x.coefficient2Constant() for x in all_exponent_curves],
        'Coefficient3 Constant': [x.coefficient3Constant() for x in all_exponent_curves],
        'Minimum Value of x': [x.minimumValueofx() for x in all_exponent_curves],
        'Maximum Value of x': [x.maximumValueofx() for x in all_exponent_curves],
        'Minimum Curve Output': [x.minimumCurveOutput() for x in all_exponent_curves],
        'Maximum Curve Output': [x.maximumCurveOutput() for x in all_exponent_curves],
        'Input Unit Type for X': [x.inputUnitTypeforX() for x in all_exponent_curves],
        'Output Unit Type': [x.outputUnitType() for x in all_exponent_curves]
    }

    # Create a DataFrame of all spaces.
    all_exponent_curves_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_exponent_curves_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_exponent_curves_df = all_exponent_curves_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(f"The OSM model contains {all_exponent_curves_df.shape[0]} exponent curves")

    return all_exponent_curves_df