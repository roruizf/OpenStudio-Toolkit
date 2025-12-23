import openstudio
import logging
from typing import Dict, List, Literal, Any

# Configure logger
logger = logging.getLogger(__name__)

def validator(
    osm_model: openstudio.model.Model,
    variable_names: List[str],
    reporting_frequency: str
) -> Dict[str, Any]:
    """
    Validate that the input parameters for setting output variables are correct and consistent.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - variable_names (List[str]): List of EnergyPlus variable names to request.
    - reporting_frequency (str): The desired reporting frequency (e.g., 'Hourly').

    Returns:
    - Dict[str, Any]: A dictionary containing the validation 'status' and 'messages'.
    """
    messages = []
    
    if not variable_names:
        msg = "ERROR: The 'variable_names' list cannot be empty."
        logger.error(msg)
        return {"status": "ERROR", "messages": [msg]}

    # Valid EnergyPlus frequencies
    valid_frequencies = ["Detailed", "Timestep", "Hourly", "Daily", "Monthly", "RunPeriod", "Annual"]
    if reporting_frequency not in valid_frequencies:
        msg = f"ERROR: '{reporting_frequency}' is not a valid frequency. Choose from: {valid_frequencies}"
        logger.error(msg)
        return {"status": "ERROR", "messages": [msg]}

    msg = f"OK: Validated request for {len(variable_names)} variables at '{reporting_frequency}' frequency."
    logger.info(msg)
    messages.append(msg)
    return {"status": "READY", "messages": messages}

def run(
    osm_model: openstudio.model.Model,
    variable_names: List[str],    
    reporting_frequency: Literal["Detailed", "Timestep", "Hourly", "Daily", "Monthly", "RunPeriod", "Annual"],
    key_value: str = "*",
    remove_existing: bool = False
) -> openstudio.model.Model:
    """
    Configure Output:Variable objects in the OpenStudio model for simulation results.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object to modify.
    - variable_names (List[str]): List of output variable names to add.
    - reporting_frequency (str): The reporting frequency level.
    - key_value (str, optional): The key value filter (e.g., specific object name or '*'). Defaults to "*".
    - remove_existing (bool, optional): If True, all existing Output:Variable objects are removed first. Defaults to False.

    Returns:
    - openstudio.model.Model: The updated OpenStudio Model object.
    """
    logger.info("Starting 'Set Output Variables' task...")
    
    if remove_existing:
        existing_vars = osm_model.getOutputVariables()
        logger.info(f"Removing {len(existing_vars)} existing output variables.")
        for var in existing_vars:
            var.remove()

    added_count = 0
    for var_name in variable_names:
        output_var = openstudio.model.OutputVariable(var_name, osm_model)
        output_var.setKeyValue(key_value)
        output_var.setReportingFrequency(reporting_frequency)
        added_count += 1
        
    logger.info(f"Task finished. {added_count} Output:Variable objects were configured.")
    return osm_model