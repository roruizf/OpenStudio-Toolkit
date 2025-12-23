import openstudio
import pandas as pd
import numpy as np
import datetime
import calendar
import logging
from openstudio_toolkit.utils import helpers

# Configure logger
logger = logging.getLogger(__name__)


def get_default_schedule_set_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None, _object_ref: openstudio.model.DefaultScheduleSet = None) -> dict:
    """
    Retrieve a specified OS:DefaultScheduleSet object from the OpenStudio model by handle, name, or direct reference and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.DefaultScheduleSet, optional): Direct reference to the object.

    Returns:
    - dict: Dictionary containing information about the specified object.
    """
    target_object = helpers.fetch_object(
        osm_model, "DefaultScheduleSet", handle, name, _object_ref)

    if target_object is None:
        return {}

    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Hours of Operation Schedule Name': target_object.hoursofOperationSchedule().get().name().get() if target_object.hoursofOperationSchedule().is_initialized() else None,
        'Number of People Schedule Name': target_object.numberofPeopleSchedule().get().name().get() if target_object.numberofPeopleSchedule().is_initialized() else None,
        'People Activity Level Schedule Name': target_object.peopleActivityLevelSchedule().get().name().get() if target_object.peopleActivityLevelSchedule().is_initialized() else None,
        'Lighting Schedule Name': target_object.lightingSchedule().get().name().get() if target_object.lightingSchedule().is_initialized() else None,
        'Electric Equipment Schedule Name': target_object.electricEquipmentSchedule().get().name().get() if target_object.electricEquipmentSchedule().is_initialized() else None,
        'Gas Equipment Schedule Name': target_object.gasEquipmentSchedule().get().name().get() if target_object.gasEquipmentSchedule().is_initialized() else None,
        'Hot Water Equipment Schedule Name': target_object.hotWaterEquipmentSchedule().get().name().get() if target_object.hotWaterEquipmentSchedule().is_initialized() else None,
        'Infiltration Schedule Name': target_object.infiltrationSchedule().get().name().get() if target_object.infiltrationSchedule().is_initialized() else None,
        'Steam Equipment Schedule Name': target_object.steamEquipmentSchedule().get().name().get() if target_object.steamEquipmentSchedule().is_initialized() else None,
        'Other Equipment Schedule Name': target_object.otherEquipmentSchedule().get().name().get() if target_object.otherEquipmentSchedule().is_initialized() else None
    }

    return object_dict

def get_all_default_schedule_set_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all OS:DefaultScheduleSet objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a default schedule set object.
    """
    all_objects = osm_model.getDefaultScheduleSets()
    return [get_default_schedule_set_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_default_schedule_set_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:DefaultScheduleSet objects from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all default schedule set objects.
    """
    all_objects_dicts = get_all_default_schedule_set_objects_as_dicts(osm_model)
    all_objects_df = pd.DataFrame(all_objects_dicts)

    if not all_objects_df.empty:
        if 'Name' in all_objects_df.columns:
            all_objects_df = all_objects_df.sort_values(
                by='Name', ascending=True, na_position='first').reset_index(drop=True)

    logger.info(f"The OSM model contains {all_objects_df.shape[0]} default schedule sets objects")
    return all_objects_df


def get_schedule_ruleset_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None, _object_ref: openstudio.model.ScheduleRuleset = None) -> dict:
    """
    Retrieve a specified OS:Schedule:Ruleset object from the OpenStudio model by handle, name, or direct reference and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.ScheduleRuleset, optional): Direct reference to the object.

    Returns:
    - dict: Dictionary containing information about the specified object.
    """
    target_object = helpers.fetch_object(
        osm_model, "ScheduleRuleset", handle, name, _object_ref)

    if target_object is None:
        return {}

    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Schedule Type Limits Name': target_object.scheduleTypeLimits().get().name().get() if target_object.scheduleTypeLimits().is_initialized() else None,
        'Default Day Schedule Name': target_object.defaultDaySchedule().name().get() if target_object.defaultDaySchedule().name().is_initialized() else None,
        'Summer Design Day Schedule Name': target_object.summerDesignDaySchedule().name().get() if target_object.summerDesignDaySchedule().name().is_initialized() else None,
        'Winter Design Day Schedule Name': target_object.winterDesignDaySchedule().name().get() if target_object.winterDesignDaySchedule().name().is_initialized() else None
    }

    return object_dict

def get_all_schedule_ruleset_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all OS:Schedule:Ruleset objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a schedule ruleset object.
    """
    all_objects = osm_model.getScheduleRulesets()
    return [get_schedule_ruleset_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_schedule_ruleset_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:Schedule:Ruleset objects from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all schedule ruleset objects.
    """
    all_objects_dicts = get_all_schedule_ruleset_objects_as_dicts(osm_model)
    all_objects_df = pd.DataFrame(all_objects_dicts)

    if not all_objects_df.empty:
        if 'Name' in all_objects_df.columns:
            all_objects_df = all_objects_df.sort_values(
                by='Name', ascending=True, na_position='first').reset_index(drop=True)

    logger.info(f"The OSM model contains {all_objects_df.shape[0]} schedule ruleset objects")
    return all_objects_df


def get_schedule_rule_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None, _object_ref: openstudio.model.ScheduleRule = None) -> dict:
    """
    Retrieve a specified OS:Schedule:Rule object from the OpenStudio model by handle, name, or direct reference and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.ScheduleRule, optional): Direct reference to the object.

    Returns:
    - dict: Dictionary containing information about the specified object.
    """
    target_object = helpers.fetch_object(
        osm_model, "ScheduleRule", handle, name, _object_ref)

    if target_object is None:
        return {}

    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Schedule Ruleset Name': target_object.scheduleRuleset().name().get() if target_object.scheduleRuleset().name().is_initialized() else None,
        'Rule Order': target_object.ruleIndex(),
        'Day Schedule Name': target_object.daySchedule().name().get() if target_object.daySchedule().name().is_initialized() else None,
        'Apply Sunday': target_object.applySunday(),
        'Apply Monday': target_object.applyMonday(),
        'Apply Tuesday': target_object.applyTuesday(),
        'Apply Wednesday': target_object.applyWednesday(),
        'Apply Thursday': target_object.applyThursday(),
        'Apply Friday': target_object.applyFriday(),
        'Apply Saturday': target_object.applySaturday(),
        'Date Specification Type': target_object.dateSpecificationType(),
        'Start Month': target_object.startDate().get().monthOfYear().value() if target_object.startDate().is_initialized() else None,
        'Start Day': target_object.startDate().get().dayOfMonth() if target_object.startDate().is_initialized() else None,
        'End Month': target_object.endDate().get().monthOfYear().value() if target_object.endDate().is_initialized() else None,
        'End Day': target_object.endDate().get().dayOfMonth() if target_object.endDate().is_initialized() else None
    }

    return object_dict

def get_all_schedule_rule_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all OS:Schedule:Rule objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a schedule rule object.
    """
    all_objects = osm_model.getScheduleRules()
    return [get_schedule_rule_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_schedule_rule_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:Schedule:Rule objects from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all schedule rule objects.
    """
    all_objects_dicts = get_all_schedule_rule_objects_as_dicts(osm_model)
    all_objects_df = pd.DataFrame(all_objects_dicts)

    if not all_objects_df.empty:
        if 'Name' in all_objects_df.columns:
            all_objects_df = all_objects_df.sort_values(
                by='Name', ascending=True, na_position='first').reset_index(drop=True)

    logger.info(f"The OSM model contains {all_objects_df.shape[0]} schedule rule objects")
    return all_objects_df


def get_schedule_day_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None, _object_ref: openstudio.model.ScheduleDay = None) -> dict:
    """
    Retrieve a specified OS:Schedule:Day object from the OpenStudio model by handle, name, or direct reference and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.ScheduleDay, optional): Direct reference to the object.

    Returns:
    - dict: Dictionary containing information about the specified object.
    """
    target_object = helpers.fetch_object(
        osm_model, "ScheduleDay", handle, name, _object_ref)

    if target_object is None:
        return {}

    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Schedule Type Limits Name': target_object.scheduleTypeLimits().get().name().get() if target_object.scheduleTypeLimits().is_initialized() else None,
        'Interpolate to Timestep': target_object.interpolatetoTimestep(),
        'Hour': tuple(item.hours() for item in target_object.times()),
        'Minute': tuple(item.minutes() for item in target_object.times()),
        'Values': target_object.values()
    }

    return object_dict

def get_all_schedule_day_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all OS:Schedule:Day objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a schedule day object.
    """
    all_objects = osm_model.getScheduleDays()
    return [get_schedule_day_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_schedule_day_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:Schedule:Day objects from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all schedule day objects.
    """
    all_objects_dicts = get_all_schedule_day_objects_as_dicts(osm_model)
    all_objects_df = pd.DataFrame(all_objects_dicts)

    if not all_objects_df.empty:
        if 'Name' in all_objects_df.columns:
            all_objects_df = all_objects_df.sort_values(
                by='Name', ascending=True, na_position='first').reset_index(drop=True)

    logger.info(f"The OSM model contains {all_objects_df.shape[0]} schedule day objects")
    return all_objects_df


def get_schedule_type_limit_object_as_dict(osm_model: openstudio.model.Model, handle: str = None, name: str = None, _object_ref: openstudio.model.ScheduleTypeLimits = None) -> dict:
    """
    Retrieve a specified OS:ScheduleTypeLimits object from the OpenStudio model by handle, name, or direct reference and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - handle (str, optional): The handle of the object to retrieve.
    - name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.ScheduleTypeLimits, optional): Direct reference to the object.

    Returns:
    - dict: Dictionary containing information about the specified object.
    """
    target_object = helpers.fetch_object(
        osm_model, "ScheduleTypeLimits", handle, name, _object_ref)

    if target_object is None:
        return {}

    object_dict = {
        'Handle': str(target_object.handle()),
        'Name': target_object.name().get() if target_object.name().is_initialized() else None,
        'Lower Limit Value': target_object.lowerLimitValue().get() if target_object.lowerLimitValue().is_initialized() else None,
        'Upper Limit Value': target_object.upperLimitValue().get() if target_object.upperLimitValue().is_initialized() else None,
        'Numeric Type': target_object.numericType().get() if target_object.numericType().is_initialized() else None
    }

    return object_dict

def get_all_schedule_type_limit_objects_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all OS:ScheduleTypeLimits objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a schedule type limits object.
    """
    all_objects = osm_model.getScheduleTypeLimitss()
    return [get_schedule_type_limit_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_schedule_type_limit_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:ScheduleTypeLimits objects from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all schedule type limits objects.
    """
    all_objects_dicts = get_all_schedule_type_limit_objects_as_dicts(osm_model)
    all_objects_df = pd.DataFrame(all_objects_dicts)

    # Replace NaN values with None
    all_objects_df = all_objects_df.replace(np.nan, None)

    if not all_objects_df.empty:
        if 'Name' in all_objects_df.columns:
            all_objects_df = all_objects_df.sort_values(
                by='Name', ascending=True, na_position='first').reset_index(drop=True)

    logger.info(f"The OSM model contains {all_objects_df.shape[0]} schedule type limit objects")
    return all_objects_df


def get_all_default_schedule_set_components_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all default schedule set components from the OpenStudio model and format them into a comprehensive pandas DataFrame, including rules and daily profiles.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: A DataFrame containing all default schedule set components organized by set, ruleset, and day type.
    """
    all_default_schedule_set_df = get_all_default_schedule_set_objects_as_dataframe(osm_model)
    
    if all_default_schedule_set_df.empty:
        logger.warning("No default schedule sets found in the model.")
        return pd.DataFrame()

    columns_to_stack = all_default_schedule_set_df.columns[~all_default_schedule_set_df.columns.isin(['Handle', 'Name'])].tolist()
    default_schedule_ruleset_df = all_default_schedule_set_df.melt(id_vars=['Handle', 'Name'], value_vars=columns_to_stack, var_name='Schedule Ruleset Type', value_name='Schedule Ruleset Name').sort_values(by=['Handle', 'Name']).drop(columns=['Handle'])
    default_schedule_ruleset_df = default_schedule_ruleset_df.rename(columns={'Name': 'Default Schedule Set Name'})
    default_schedule_ruleset_df['Schedule Ruleset Type'] = default_schedule_ruleset_df['Schedule Ruleset Type'].str.replace('Name', '').str.strip()
    default_schedule_ruleset_df = default_schedule_ruleset_df.dropna(subset=['Schedule Ruleset Name']).reset_index(drop=True)

    if default_schedule_ruleset_df.empty:
        logger.info("No schedule rulesets assigned to default schedule sets.")
        return pd.DataFrame()

    all_schedule_ruleset_objects_df = get_all_schedule_ruleset_objects_as_dataframe(osm_model)
    default_schedule_ruleset_df = pd.merge(default_schedule_ruleset_df, all_schedule_ruleset_objects_df, left_on='Schedule Ruleset Name', right_on='Name', how='left')
    default_schedule_ruleset_df = default_schedule_ruleset_df.drop(columns=['Handle', 'Name'])
    default_schedule_ruleset_df = default_schedule_ruleset_df.replace(np.nan, None)
    
    columns_to_stack = default_schedule_ruleset_df.columns[~default_schedule_ruleset_df.columns.isin(['Default Schedule Set Name', 'Schedule Ruleset Type', 'Schedule Ruleset Name', 'Schedule Type Limits Name'])].tolist()
    default_schedule_day_df = default_schedule_ruleset_df.melt(id_vars=['Default Schedule Set Name', 'Schedule Ruleset Type', 'Schedule Ruleset Name', 'Schedule Type Limits Name'], value_vars=columns_to_stack,
                                                                 var_name='Schedule Day Type', value_name='Schedule Day Name').sort_values(by=['Default Schedule Set Name', 'Schedule Ruleset Type', 'Schedule Ruleset Name', 'Schedule Type Limits Name']).reset_index(drop=True)
    default_schedule_day_df['Schedule Day Type'] = default_schedule_day_df['Schedule Day Type'].str.replace('Name', '').str.strip()

    all_schedule_day_objects_df = get_all_schedule_day_objects_as_dataframe(osm_model)
    all_schedule_rule_objects_df = get_all_schedule_rule_objects_as_dataframe(osm_model)
    
    default_schedule_rule_objects_df = all_schedule_rule_objects_df[all_schedule_rule_objects_df['Schedule Ruleset Name'].isin(default_schedule_day_df['Schedule Ruleset Name'].unique())]

    # Stacking priority day schedules and rules
    default_schedule_day_df['Schedule Rule Name'] = None
    default_schedule_day_df['Schedule Rule Order'] = None
    
    for index, row in default_schedule_rule_objects_df.iterrows():
        schedule_ruleset_name = row['Schedule Ruleset Name']
        default_schedule_day_df_i = default_schedule_day_df[default_schedule_day_df['Schedule Ruleset Name'] == schedule_ruleset_name].copy()
        default_schedule_day_df_i = default_schedule_day_df_i.drop_duplicates(['Default Schedule Set Name', 'Schedule Ruleset Type', 'Schedule Ruleset Name',
                                                                                 'Schedule Type Limits Name'], keep='first')
        default_schedule_day_df_i['Schedule Day Name'] = row['Day Schedule Name']
        default_schedule_day_df_i['Schedule Day Type'] = 'Rule Day Schedule'
        default_schedule_day_df_i['Schedule Rule Name'] = row['Name']
        default_schedule_day_df_i['Schedule Rule Order'] = str(row['Rule Order'])
        
        default_schedule_day_df = pd.concat([default_schedule_day_df, default_schedule_day_df_i], ignore_index=True)
    
    default_schedule_day_df = default_schedule_day_df.replace(np.nan, None)
    default_schedule_day_df = default_schedule_day_df.sort_values(by=['Default Schedule Set Name', 'Schedule Ruleset Type', 'Schedule Ruleset Name', 'Schedule Type Limits Name']).reset_index(drop=True)

    logger.info(f"Generated default schedule set components DataFrame with {default_schedule_day_df.shape[0]} rows")
    return default_schedule_day_df


def get_schedule_type_limits_parms(schedule_type_limits_name: str) -> dict:
    """
    Retrieve default parameters for a specified schedule type limit name.

    Parameters:
    - schedule_type_limits_name (str): Name of the schedule type limits (e.g., 'ActivityLevel', 'InternalGains', 'IndoorSetpoint').

    Returns:
    - dict: Dictionary containing default parameters (Lower Limit, Upper Limit, Numeric Type, Unit Type).

    Raises:
    - KeyError: If the provided schedule type limits name is not defined in the internal dictionary.
    """
    # Default parameters for different schedule type limits
    all_possible_schedule_type_limits_parms = {
        'ActivityLevel': {
            'Lower Limit Value': 0,
            'Upper Limit Value': None,
            'Numeric Type': 'Continuous',
            'Unit Type': 'ActivityLevel'
        },
        'InternalGains': {
            'Lower Limit Value': 0,
            'Upper Limit Value': 1,
            'Numeric Type': 'Continuous',
            'Unit Type': 'Dimensionless'
        },
        'IndoorSetpoint': {
            'Lower Limit Value': None,
            'Upper Limit Value': None,
            'Numeric Type': 'Continuous',
            'Unit Type': 'Temperature'
        }
    }

    # Check if the provided schedule type limits name exists in the dictionary
    if schedule_type_limits_name not in all_possible_schedule_type_limits_parms:
        err_msg = f"The key '{schedule_type_limits_name}' needs to be defined in the internal dictionary of 'get_schedule_type_limits_parms'."
        logger.error(err_msg)
        raise KeyError(err_msg)
    
    return all_possible_schedule_type_limits_parms[schedule_type_limits_name]


def create_new_schedule_type_limits(osm_model: openstudio.model.Model, schedule_type_limits_name: str) -> openstudio.model.ScheduleTypeLimits:
    """
    Create a new OS:ScheduleTypeLimits object in the model and configure its properties based on predefined defaults.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - schedule_type_limits_name (str): Name of the schedule type limits to create.

    Returns:
    - openstudio.model.ScheduleTypeLimits: The newly created schedule type limits object.

    Raises:
    - ValueError: If the configured numeric or unit types are invalid.
    """
    # Define sets of possible values (for validation)
    POSSIBLE_NUMERIC_TYPES = {'Continuous', 'Discrete', 'OnOff', 'Control'}
    POSSIBLE_UNIT_TYPES = {'Dimensionless', 'Temperature', 'Power', 'Other', 'ActivityLevel'}

    # Load Schedule Type Limits parameters
    params = get_schedule_type_limits_parms(schedule_type_limits_name)
    lower_limit_value = params['Lower Limit Value']
    upper_limit_value = params['Upper Limit Value']
    numeric_type = params['Numeric Type']
    unit_type = params['Unit Type']

    # Check if input values are valid
    if numeric_type not in POSSIBLE_NUMERIC_TYPES:
        err_msg = f"Invalid numeric_type '{numeric_type}'. Possible values are {POSSIBLE_NUMERIC_TYPES}"
        logger.error(err_msg)
        raise ValueError(err_msg)

    if unit_type not in POSSIBLE_UNIT_TYPES:
        err_msg = f"Invalid unit_type '{unit_type}'. Possible values are {POSSIBLE_UNIT_TYPES}"
        logger.error(err_msg)
        raise ValueError(err_msg)

    # Create ScheduleTypeLimits object
    schedule_type_limits = openstudio.model.ScheduleTypeLimits(osm_model)
    schedule_type_limits.setName(schedule_type_limits_name)

    if lower_limit_value is not None:
        schedule_type_limits.setLowerLimitValue(lower_limit_value)

    if upper_limit_value is not None:
        schedule_type_limits.setUpperLimitValue(upper_limit_value)
    
    schedule_type_limits.setNumericType(numeric_type)
    schedule_type_limits.setUnitType(unit_type)

    logger.info(f"Created new ScheduleTypeLimits: {schedule_type_limits_name}")
    return schedule_type_limits


def create_new_default_schedule_ruleset(osm_model: openstudio.model.Model,
                                        schedule_ruleset_name: str,
                                        schedule_type_limits_name: str
                                        ) -> openstudio.model.ScheduleRuleset:
    """
    Create a new OS:Schedule:Ruleset object with default parameters and design days.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - schedule_ruleset_name (str): Name for the new schedule ruleset.
    - schedule_type_limits_name (str): Name of the schedule type limits to associate.

    Returns:
    - openstudio.model.ScheduleRuleset: The newly created schedule ruleset.
    """
    # Create Schedule RuleSet
    schedule_ruleset = openstudio.model.ScheduleRuleset(osm_model)
    schedule_ruleset.setName(schedule_ruleset_name)
    schedule_ruleset.defaultDaySchedule().setName(f"{schedule_ruleset_name} Default")

    # Assign/Create Schedule Type Limits
    type_limit_obj = osm_model.getScheduleTypeLimitsByName(schedule_type_limits_name)
    if type_limit_obj.is_initialized():
        schedule_type_limits = type_limit_obj.get()
    else:
        schedule_type_limits = create_new_schedule_type_limits(osm_model, schedule_type_limits_name)

    schedule_ruleset.setScheduleTypeLimits(schedule_type_limits)

    # Default parameters for design days
    default_ruleset_params = {
        'ActivityLevel': {
            'Design Day': {
                'Winter Design Day Default Value': 132,
                'Summer Design Day Default Value': 132,
            }
        },
        'InternalGains': {
            'Design Day': {
                'Winter Design Day Default Value': 0,
                'Summer Design Day Default Value': 1,
            }
        },
        'IndoorSetpoint': {
            'Design Day': {
                'Winter Design Day Default Value': 21,
                'Summer Design Day Default Value': 24,
            }
        }
    }

    # Configure Design Days
    if schedule_type_limits_name in default_ruleset_params:
        params = default_ruleset_params[schedule_type_limits_name]['Design Day']

        # Winter Design Day
        winter_design_day = openstudio.model.ScheduleDay(osm_model)
        winter_design_day.setName(f"{schedule_ruleset_name} Winter Design Day")
        winter_design_day.setScheduleTypeLimits(schedule_type_limits)
        winter_val = params['Winter Design Day Default Value']
        # addValue takes Time then value. default time is 24:00 if not specified but let's be explicit if needed
        # OpenStudio default day schedule usually has one value at 24:00
        winter_design_day.addValue(openstudio.Time(0, 24, 0), winter_val)
        schedule_ruleset.setWinterDesignDaySchedule(winter_design_day)

        # Summer Design Day
        summer_design_day = openstudio.model.ScheduleDay(osm_model)
        summer_design_day.setName(f"{schedule_ruleset_name} Summer Design Day")
        summer_design_day.setScheduleTypeLimits(schedule_type_limits)
        summer_val = params['Summer Design Day Default Value']
        summer_design_day.addValue(openstudio.Time(0, 24, 0), summer_val)
        schedule_ruleset.setSummerDesignDaySchedule(summer_design_day)

    logger.info(f"Created new default ScheduleRuleset: {schedule_ruleset_name}")
    return schedule_ruleset


def create_new_schedule_ruleset(
    osm_model: openstudio.model.Model,
    schdle_ruleset_name: str,
    schdle_ruleset_type: str
) -> openstudio.model.ScheduleRuleset:
    """
    Create a new OS:Schedule:Ruleset object and configure its properties based on predefined type-specific defaults.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - schdle_ruleset_name (str): Name for the new schedule ruleset.
    - schdle_ruleset_type (str): Type of the schedule ruleset (e.g., 'ActivityLevel', 'InternalGains', 'IndoorSetpoint').

    Returns:
    - openstudio.model.ScheduleRuleset: The newly created schedule ruleset.

    Raises:
    - ValueError: If the provided schedule ruleset type is invalid.
    """
    # Default parameters
    schdle_ruleset_params = {
        'ActivityLevel': {
            'ScheduleTypeLimits': {
                'Lower Limit Value': 0,
                'Upper Limit Value': None,
                'Numeric Type': 'Continuous',
                'Unit Type': 'ActivityLevel'
            },
            'Design Day': {
                'Winter Design Day Default Value': 132,
                'Summer Design Day Default Value': 132,
            }
        },
        'InternalGains': {
            'ScheduleTypeLimits': {
                'Lower Limit Value': 0,
                'Upper Limit Value': 1,
                'Numeric Type': 'Continuous',
                'Unit Type': 'Dimensionless'
            },
            'Design Day': {
                'Winter Design Day Default Value': 0,
                'Summer Design Day Default Value': 1,
            }
        },
        'IndoorSetpoint': {
            'ScheduleTypeLimits': {
                'Lower Limit Value': None,
                'Upper Limit Value': None,
                'Numeric Type': 'Continuous',
                'Unit Type': 'Temperature'
            },
            'Design Day': None
        }
    }

    # Check if schdle_ruleset_type is in schdle_ruleset_params
    if schdle_ruleset_type not in schdle_ruleset_params:
        err_msg = f"Invalid schdle_ruleset_type '{schdle_ruleset_type}'. Possible values are {list(schdle_ruleset_params.keys())}"
        logger.error(err_msg)
        raise ValueError(err_msg)

    # Assing/Create Schedule Type Limits
    type_limit_name = schdle_ruleset_type
    type_limit_obj = osm_model.getScheduleTypeLimitsByName(type_limit_name)
    if type_limit_obj.is_initialized():
        schdle_type_limit = type_limit_obj.get()
    else:
        schdle_type_limit = create_new_schedule_type_limits(osm_model, type_limit_name)

    schdle_ruleset = openstudio.model.ScheduleRuleset(osm_model)
    schdle_ruleset.setName(schdle_ruleset_name)
    schdle_ruleset.defaultDaySchedule().setName(f"{schdle_ruleset_name} Default")
    schdle_ruleset.setScheduleTypeLimits(schdle_type_limit)

    # Configure Design Days if provided
    design_days_params = schdle_ruleset_params[schdle_ruleset_type]['Design Day']
    if design_days_params is not None:
        # Winter Design Day
        winter_val = design_days_params['Winter Design Day Default Value']
        winter_day = openstudio.model.ScheduleDay(osm_model)
        winter_day.setName(f"{schdle_ruleset_name} Winter Design Day")
        winter_day.setScheduleTypeLimits(schdle_type_limit)
        winter_day.addValue(openstudio.Time(0, 24, 0), winter_val)
        schdle_ruleset.setWinterDesignDaySchedule(winter_day)

        # Summer Design Day
        summer_val = design_days_params['Summer Design Day Default Value']
        summer_day = openstudio.model.ScheduleDay(osm_model)
        summer_day.setName(f"{schdle_ruleset_name} Summer Design Day")
        summer_day.setScheduleTypeLimits(schdle_type_limit)
        summer_day.addValue(openstudio.Time(0, 24, 0), summer_val)
        schdle_ruleset.setSummerDesignDaySchedule(summer_day)

    logger.info(f"Created new ScheduleRuleset: {schdle_ruleset_name} of type {schdle_ruleset_type}")
    return schdle_ruleset


def create_rule_schedule_day(osm_model: openstudio.model.Model,
                             schedule_rule_set_name: str,
                             schedule_day_hours: tuple,
                             schedule_day_minutes: tuple,
                             schedule_day_values: tuple,
                             apply_weekdays: dict,
                             start_date_strftime: str = '2007-01-01',
                             end_date_strftime: str = '2007-12-31'
                             ) -> openstudio.model.ScheduleRule:
    """
    Create a new OS:Schedule:Day and its associated OS:Schedule:Rule, assigning it to a ruleset with specific day application and dates.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - schedule_rule_set_name (str): Name of the existing ruleset to add the rule to.
    - schedule_day_hours (tuple): Tuple of hour values for the daily profile.
    - schedule_day_minutes (tuple): Tuple of minute values for the daily profile.
    - schedule_day_values (tuple): Tuple of values for the daily profile.
    - apply_weekdays (dict): Dictionary indicating which weekdays the rule applies to (e.g., {'Monday': True}).
    - start_date_strftime (str): Start date string (YYYY-MM-DD).
    - end_date_strftime (str): End date string (YYYY-MM-DD).

    Returns:
    - openstudio.model.ScheduleRule: The newly created schedule rule.

    Raises:
    - ValueError: If the target ruleset cannot be found.
    """
    # Get target schedule ruleset
    ruleset_obj = osm_model.getScheduleRulesetByName(schedule_rule_set_name)
    if not ruleset_obj.is_initialized():
        err_msg = f"ScheduleRuleset '{schedule_rule_set_name}' not found."
        logger.error(err_msg)
        raise ValueError(err_msg)
    
    schedule_ruleset = ruleset_obj.get()

    # Create new Schedule Day
    schedule_day = openstudio.model.ScheduleDay(osm_model)
    
    # Set type limit
    if schedule_ruleset.scheduleTypeLimits().is_initialized():
        schedule_day.setScheduleTypeLimits(schedule_ruleset.scheduleTypeLimits().get())
    
    schedule_day_name = schedule_rule_set_name.replace('Schedule', 'Rule Day Schedule')
    schedule_day.setName(schedule_day_name)

    # Add values to the ScheduleDay
    for hour, minute, value in zip(schedule_day_hours, schedule_day_minutes, schedule_day_values):
        until_time = openstudio.Time(0, int(hour), int(minute))
        schedule_day.addValue(until_time, value)

    # Create Schedule Rule
    schedule_rule = openstudio.model.ScheduleRule(schedule_ruleset, schedule_day)
    schedule_rule_name = schedule_rule_set_name.replace('Schedule', 'Rule')
    schedule_rule.setName(schedule_rule_name)

    # Assign weekdays
    if apply_weekdays.get('Monday'): schedule_rule.setApplyMonday(True)
    if apply_weekdays.get('Tuesday'): schedule_rule.setApplyTuesday(True)
    if apply_weekdays.get('Wednesday'): schedule_rule.setApplyWednesday(True)
    if apply_weekdays.get('Thursday'): schedule_rule.setApplyThursday(True)
    if apply_weekdays.get('Friday'): schedule_rule.setApplyFriday(True)
    if apply_weekdays.get('Saturday'): schedule_rule.setApplySaturday(True)
    if apply_weekdays.get('Sunday'): schedule_rule.setApplySunday(True)

    # Assign start and end date
    start_date = openstudio.Date.fromISO8601(start_date_strftime.replace('-', '')) # OpenStudio Date usually prefers ISO or similar
    end_date = openstudio.Date.fromISO8601(end_date_strftime.replace('-', ''))
    schedule_rule.setStartDate(start_date)
    schedule_rule.setEndDate(end_date)

    logger.info(f"Created new ScheduleRule '{schedule_rule_name}' for ruleset '{schedule_rule_set_name}'")
    return schedule_rule


def calculate_equivalent_full_hours(hours: tuple, minutes: tuple, values: tuple, full_load_value: float = 1.0) -> float:
    """
    Calculate the equivalent full-load hours (EFLH) for a given daily schedule profile.

    Parameters:
    - hours (tuple): Tuple of hour values representing the profile (0-24).
    - minutes (tuple): Tuple of minute values corresponding to the hours.
    - values (tuple): Tuple of fraction/value entries for each time period.
    - full_load_value (float, optional): Reference value for "full load". Defaults to 1.0.

    Returns:
    - float: Equivalent full-load hours.
    """
    # Convert input tuples to NumPy arrays for efficient calculations
    # Ensuring the last hour is 24 for the full day coverage
    hours_arr = np.array(list(hours)[:-1] + [24])
    minutes_arr = np.array(minutes)
    values_arr = np.array(values)

    # Calculate the current time in decimal hours
    current_time_in_hours = hours_arr + (minutes_arr / 60.0)

    # Calculate the duration of each interval
    time_differences = np.diff(np.insert(current_time_in_hours, 0, 0.0))

    # Calculate EFLH
    equivalent_full_hours = np.sum(values_arr * time_differences) / full_load_value

    return float(equivalent_full_hours)

def weekday_count(start_date_str: str, end_date_str: str) -> dict:
    """
    Count the occurrences of each weekday within a specified date range.

    Parameters:
    - start_date_str (str): Start date string (YYYY-MM-DD).
    - end_date_str (str): End date string (YYYY-MM-DD).

    Returns:
    - dict: Dictionary mapping weekday names to their respective counts.
    """
    start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')

    counts = {day: 0 for day in calendar.day_name}

    for i in range((end_date - start_date).days + 1):
        current_date = start_date + datetime.timedelta(days=i)
        day_name = calendar.day_name[current_date.weekday()]
        counts[day_name] += 1

    return counts

def convert_schedule_to_daily_profile(hours: tuple, minutes: tuple, values: tuple, timestep: float = 1.0) -> tuple[list[float], list[float]]:
    """
    Interpolate/convert a step-wise schedule into a uniform time-series profile based on a specified timestep.

    Parameters:
    - hours (tuple): Tuple of hour values for the source schedule.
    - minutes (tuple): Tuple of minute values for the source schedule.
    - values (tuple): Tuple of fractional values for the source schedule.
    - timestep (float, optional): Timestep in hours for the output profile. Defaults to 1.0.

    Returns:
    - tuple[list[float], list[float]]: A tuple containing (time_profile, values_profile).
    """
    # Ensure standard ordering and completeness
    source_hours = np.array(list(hours)[:-1] + [24])[::-1]
    source_minutes = np.array(minutes)[::-1]
    source_values = np.array(values)[::-1]

    # Calculate source decimal hours
    source_time_hours = source_hours + (source_minutes / 60.0)

    # Output grid
    daily_time = np.arange(0, 24, timestep)
    daily_values = np.array([source_values[0]] * len(daily_time))

    # Populate grid by looking back at the source steps
    for i in range(len(source_time_hours)):
        index = np.where(daily_time < source_time_hours[i])[0]
        daily_values[index] = source_values[i]

    return daily_time.tolist(), daily_values.tolist()