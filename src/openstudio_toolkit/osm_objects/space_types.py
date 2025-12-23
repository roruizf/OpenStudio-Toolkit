import openstudio
import pandas as pd
import numpy as np
import logging
from openstudio_toolkit.osm_objects.schedules import *
from openstudio_toolkit.utils import helpers

# Configure logger
logger = logging.getLogger(__name__)



def get_space_type_as_dict(osm_model: openstudio.model.Model, space_type_handle: str = None, space_type_name: str = None, _object_ref: openstudio.model.SpaceType = None) -> dict:
    """
    Retrieve a specified OS:SpaceType object from the OpenStudio model by handle, name, or direct reference and return its attributes as a dictionary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - space_type_handle (str, optional): The handle of the object to retrieve.
    - space_type_name (str, optional): The name of the object to retrieve.
    - _object_ref (openstudio.model.SpaceType, optional): Direct reference to the object.

    Returns:
    - dict: Dictionary containing information about the specified space type.
    """
    target_space_type = helpers.fetch_object(
        osm_model, "SpaceType", space_type_handle, space_type_name, _object_ref)

    if target_space_type is None:
        return {}
    
    # Helper to check if a default schedule set exists
    default_sch_set = target_space_type.defaultScheduleSet()
    has_sch_set = default_sch_set.is_initialized()

    space_type_dict = {
        'Handle': str(target_space_type.handle()),
        'Name': target_space_type.name().get() if target_space_type.name().is_initialized() else None,
        'Rendering Color': target_space_type.renderingColor().get().name().get() if target_space_type.renderingColor().is_initialized() else None,
        'Default Construction Set': target_space_type.defaultConstructionSet().get().name().get() if target_space_type.defaultConstructionSet().is_initialized() else None,
        'Default Schedule Set': default_sch_set.get().name().get() if has_sch_set else None,
        
        # Design Specification Outdoor Air
        'Design Specification Outdoor Air': target_space_type.designSpecificationOutdoorAir().get().name().get() if target_space_type.designSpecificationOutdoorAir().is_initialized() else None,
        
        # Standards
        'Standards Template': target_space_type.standardsTemplate().get() if target_space_type.standardsTemplate().is_initialized() else None,
        'Standards Building Type': target_space_type.standardsBuildingType().get() if target_space_type.standardsBuildingType().is_initialized() else None,
        'Standards Space Type': target_space_type.standardsSpaceType().get() if target_space_type.standardsSpaceType().is_initialized() else None,
        
        # Infiltration
        'Space Infiltration Design Flow Rates': target_space_type.spaceInfiltrationDesignFlowRates()[0].name().get() if target_space_type.spaceInfiltrationDesignFlowRates() else None,
        'Space Infiltration Effective Leakage Area': target_space_type.spaceInfiltrationEffectiveLeakageAreas()[0].name().get() if target_space_type.spaceInfiltrationEffectiveLeakageAreas() else None,
        
        # People
        'People Load Name': target_space_type.people()[0].name().get() if target_space_type.people() else None,
        'People Definition': target_space_type.people()[0].definition().name().get() if target_space_type.people() else None,
        'People Number Of People Schedule': default_sch_set.get().numberofPeopleSchedule().get().name().get() if has_sch_set and default_sch_set.get().numberofPeopleSchedule().is_initialized() else None,
        'People Activity Level Schedule': default_sch_set.get().peopleActivityLevelSchedule().get().name().get() if has_sch_set and default_sch_set.get().peopleActivityLevelSchedule().is_initialized() else None,
        
        # Lights
        'Lights Load Name': target_space_type.lights()[0].name().get() if target_space_type.lights() else None,
        'Lights Definition': target_space_type.lights()[0].definition().name().get() if target_space_type.lights() else None,
        'Lighting Schedule': default_sch_set.get().lightingSchedule().get().name().get() if has_sch_set and default_sch_set.get().lightingSchedule().is_initialized() else None,
        
        # Luminaires
        'Luminaires Load Name': target_space_type.luminaires()[0].name().get() if target_space_type.luminaires() else None,
        'Luminaires Definition': target_space_type.luminaires()[0].definition().name().get() if target_space_type.luminaires() else None,
        'Luminaires Schedule': None, # Placeholder
        
        # Electric Equipment
        'Electric Equipment Load Name': target_space_type.electricEquipment()[0].name().get() if target_space_type.electricEquipment() else None,
        'Electric Equipment Definition': target_space_type.electricEquipment()[0].definition().name().get() if target_space_type.electricEquipment() else None,
        'Electric Equipment Schedule': default_sch_set.get().electricEquipmentSchedule().get().name().get() if has_sch_set and default_sch_set.get().electricEquipmentSchedule().is_initialized() else None,
        
        # Gas Equipment        
        'Gas Equipment Load Name': target_space_type.gasEquipment()[0].name().get() if target_space_type.gasEquipment() else None,
        'Gas Equipment Definition': target_space_type.gasEquipment()[0].definition().name().get() if target_space_type.gasEquipment() else None,
        'Gas Equipment Schedule': default_sch_set.get().gasEquipmentSchedule().get().name().get() if has_sch_set and default_sch_set.get().gasEquipmentSchedule().is_initialized() else None,
        
        # Steam Equipment        
        'Steam Equipment Load Name': target_space_type.steamEquipment()[0].name().get() if target_space_type.steamEquipment() else None,
        'Steam Equipment Definition': target_space_type.steamEquipment()[0].definition().name().get() if target_space_type.steamEquipment() else None,
        'Steam Equipment Schedule': default_sch_set.get().steamEquipmentSchedule().get().name().get() if has_sch_set and default_sch_set.get().steamEquipmentSchedule().is_initialized() else None,
        
        # Other Equipment        
        'Other Equipment Load Name': target_space_type.otherEquipment()[0].name().get() if target_space_type.otherEquipment() else None,
        'Other Equipment Definition': target_space_type.otherEquipment()[0].definition().name().get() if target_space_type.otherEquipment() else None,
        'Other Equipment Schedule': default_sch_set.get().otherEquipmentSchedule().get().name().get() if has_sch_set and default_sch_set.get().otherEquipmentSchedule().is_initialized() else None,
        
        # Internal Mass Definitions
        'Internal Mass Name': target_space_type.internalMass()[0].name().get() if target_space_type.internalMass() else None,
        'Internal Mass Definition': target_space_type.internalMass()[0].definition().name().get() if target_space_type.internalMass() else None,
        
        # Infiltration
        'Infiltration Schedule': default_sch_set.get().infiltrationSchedule().get().name().get() if has_sch_set and default_sch_set.get().infiltrationSchedule().is_initialized() else None 
    }
    
    return space_type_dict

def get_all_space_types_as_dicts(osm_model: openstudio.model.Model) -> list[dict]:
    """
    Retrieve all OS:SpaceType objects from the OpenStudio model and return their attributes as a list of dictionaries.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - list[dict]: A list of dictionaries, each containing information about a space type object.
    """
    all_objects = osm_model.getSpaceTypes()
    return [get_space_type_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

def get_all_space_types_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all OS:SpaceType objects from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all space type objects.
    """
    all_objects_dicts = get_all_space_types_as_dicts(osm_model)
    all_objects_df = pd.DataFrame(all_objects_dicts)

    if not all_objects_df.empty:
        if 'Name' in all_objects_df.columns:
            all_objects_df = all_objects_df.sort_values(
                by='Name', ascending=True, na_position='first').reset_index(drop=True)

    logger.info(f"The OSM model contains {all_objects_df.shape[0]} space types")
    return all_objects_df

def create_new_space_types_objects(osm_model: openstudio.model.Model, space_types_to_create_df: pd.DataFrame) -> openstudio.model.Model:
    """
    Create new OS:SpaceType objects in the model based on data from a provided DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - space_types_to_create_df (pd.DataFrame): DataFrame containing data for new space types (Name, Default Construction Set Name, etc.).

    Returns:
    - openstudio.model.Model: The updated OpenStudio Model object.
    """
    space_types_to_create_df = space_types_to_create_df.replace(np.nan, None)

    for _, row in space_types_to_create_df.iterrows():
        name = row.get('Name')
        if not name:
            continue

        # Create new Space Type
        new_space_type = openstudio.model.SpaceType(osm_model)
        new_space_type.setName(name)

        if new_space_type.name().get() != name:
            logger.warning(f"Space type name set as '{new_space_type.name().get()}' which is different than requested: '{name}'")

        # Setting attributes if defined in space_types_to_create_df

        # Default Construction Set Name
        constr_set_name = row.get('Default Construction Set Name')
        if constr_set_name:
            constr_set_obj = osm_model.getDefaultConstructionSetByName(constr_set_name)
            if constr_set_obj.is_initialized():
                new_space_type.setDefaultConstructionSet(constr_set_obj.get())
            else:
                new_construction_set = openstudio.model.DefaultConstructionSet(osm_model)
                new_construction_set.setName(constr_set_name)
                new_space_type.setDefaultConstructionSet(new_construction_set)
        
        # Default Schedule Set Name
        sch_set_name = row.get('Default Schedule Set Name')
        if sch_set_name:
            sch_set_obj = osm_model.getDefaultScheduleSetByName(sch_set_name)
            if sch_set_obj.is_initialized():
                new_space_type.setDefaultScheduleSet(sch_set_obj.get())
            else:
                new_schedule_set = openstudio.model.DefaultScheduleSet(osm_model)
                new_schedule_set.setName(sch_set_name)
                new_space_type.setDefaultScheduleSet(new_schedule_set)
        
        # Group Rendering Name   
        rendering_name = row.get('Group Rendering Name')
        if rendering_name:
            rendering_color_obj = osm_model.getRenderingColorByName(rendering_name)
            if rendering_color_obj.is_initialized():
                rendering_color = rendering_color_obj.get()
            else:
                rendering_color = openstudio.model.RenderingColor(osm_model)
                rendering_color.setName(rendering_name)
            
            new_space_type.setRenderingColor(rendering_color)
       
        # Design Specification Outdoor Air Object Name
        # (Handling can be added as needed)
        
        # Standards Template	
        # Standards Building Type	
        # Standards Space Type

    logger.info(f"Created {space_types_to_create_df.shape[0]} new space types objects")
    return osm_model

def rename_space_types_components(osm_model: openstudio.model.Model, space_type_name_list: list[str]) -> None:
    """
    Rename all associated components of specified space types to a standard naming convention.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - space_type_name_list (list[str]): List of space type names whose components should be renamed.
    """
    # Get all space types
    all_space_types_df = get_all_space_types_objects_as_dataframe(osm_model)
    if all_space_types_df.empty:
        return

    filtered_df = all_space_types_df[all_space_types_df['Name'].isin(space_type_name_list)].reset_index(drop=True)

    for index, row in filtered_df.iterrows():
        space_type_name = row['Name']
        space_type_handle = row['Handle']

        # Get Space Type
        target_obj = osm_model.getSpaceType(openstudio.toUUID(space_type_handle))
        if not target_obj.is_initialized():
            continue
        
        target_space_type = target_obj.get()
        logger.info(f"Processing space type: {space_type_name}")
        
        for column in filtered_df.drop(columns=['Handle', 'Name']).columns: 
            new_name = f"{space_type_name} {column.replace('Name', '').replace('Load', '')}".strip()
            current_val = row[column]
            
            if current_val is not None and current_val != new_name:
                if column == 'Rendering Color' and target_space_type.renderingColor().is_initialized():
                    target_space_type.renderingColor().get().setName(new_name)
                    logger.info(f"    * {column} renamed to {new_name}")
                elif column == 'Default Construction Set' and target_space_type.defaultConstructionSet().is_initialized():
                    target_space_type.defaultConstructionSet().get().setName(new_name)
                    logger.info(f"    * {column} renamed to {new_name}")
                elif column == 'Default Schedule Set' and target_space_type.defaultScheduleSet().is_initialized():
                    target_space_type.defaultScheduleSet().get().setName(new_name)
                    logger.info(f"    * {column} renamed to {new_name}")
                elif column == 'Design Specification Outdoor Air' and target_space_type.designSpecificationOutdoorAir().is_initialized():
                    target_space_type.designSpecificationOutdoorAir().get().setName(new_name)
                    logger.info(f"    * {column} renamed to {new_name}")
                elif column == 'Space Infiltration Design Flow Rates' and target_space_type.spaceInfiltrationDesignFlowRates():
                    target_space_type.spaceInfiltrationDesignFlowRates()[0].setName(new_name)
                    logger.info(f"    * {column} renamed to {new_name}")
                elif column == 'Space Infiltration Effective Leakage Area' and target_space_type.spaceInfiltrationEffectiveLeakageAreas():
                    target_space_type.spaceInfiltrationEffectiveLeakageAreas()[0].setName(new_name)
                    logger.info(f"    * {column} renamed to {new_name}")
                elif column == 'People Load Name' and target_space_type.people():
                    target_space_type.people()[0].setName(new_name)
                    logger.info(f"    * {column} renamed to {new_name}")
                elif column == 'People Definition' and target_space_type.people():
                    target_space_type.people()[0].definition().setName(new_name)
                    logger.info(f"    * {column} renamed to {new_name}")
                elif column == 'People Number Of People Schedule' and target_space_type.defaultScheduleSet().is_initialized():
                    sch_set = target_space_type.defaultScheduleSet().get()
                    if sch_set.numberofPeopleSchedule().is_initialized():
                        sch_set.numberofPeopleSchedule().get().setName(new_name)
                        logger.info(f"    * {column} renamed to {new_name}")
                elif column == 'People Activity Level Schedule' and target_space_type.defaultScheduleSet().is_initialized():
                    sch_set = target_space_type.defaultScheduleSet().get()
                    if sch_set.peopleActivityLevelSchedule().is_initialized():
                        sch_set.peopleActivityLevelSchedule().get().setName(new_name)
                        logger.info(f"    * {column} renamed to {new_name}")
                elif column == 'Lights Load Name' and target_space_type.lights():
                    target_space_type.lights()[0].setName(new_name)
                    logger.info(f"    * {column} renamed to {new_name}")
                elif column == 'Lights Definition' and target_space_type.lights():
                    target_space_type.lights()[0].definition().setName(new_name)
                    logger.info(f"    * {column} renamed to {new_name}")
                elif column == 'Lighting Schedule' and target_space_type.defaultScheduleSet().is_initialized():
                    sch_set = target_space_type.defaultScheduleSet().get()
                    if sch_set.lightingSchedule().is_initialized():
                        sch_set.lightingSchedule().get().setName(new_name)
                        logger.info(f"    * {column} renamed to {new_name}")
                elif column == 'Luminaires Load Name' and target_space_type.luminaires():
                    target_space_type.luminaires()[0].setName(new_name)
                    logger.info(f"    * {column} renamed to {new_name}")
                elif column == 'Luminaires Definition' and target_space_type.luminaires():
                    target_space_type.luminaires()[0].definition().setName(new_name)
                elif column == 'Electric Equipment Load Name' and target_space_type.electricEquipment():
                    target_space_type.electricEquipment()[0].setName(new_name)
                    logger.info(f"    * {column} renamed to {new_name}")
                elif column == 'Electric Equipment Definition' and target_space_type.electricEquipment():
                    target_space_type.electricEquipment()[0].definition().setName(new_name)
                    logger.info(f"    * {column} renamed to {new_name}")
                elif column == 'Electric Equipment Schedule' and target_space_type.defaultScheduleSet().is_initialized():
                    sch_set = target_space_type.defaultScheduleSet().get()
                    if sch_set.electricEquipmentSchedule().is_initialized():
                        sch_set.electricEquipmentSchedule().get().setName(new_name)
                        logger.info(f"    * {column} renamed to {new_name}")
                elif column == 'Gas Equipment Load Name' and target_space_type.gasEquipment():
                    target_space_type.gasEquipment()[0].setName(new_name)
                    logger.info(f"    * {column} renamed to {new_name}")
                elif column == 'Gas Equipment Definition' and target_space_type.gasEquipment():
                    target_space_type.gasEquipment()[0].definition().setName(new_name)
                    logger.info(f"    * {column} renamed to {new_name}")
                elif column == 'Gas Equipment Schedule' and target_space_type.defaultScheduleSet().is_initialized():
                    sch_set = target_space_type.defaultScheduleSet().get()
                    if sch_set.gasEquipmentSchedule().is_initialized():
                        sch_set.gasEquipmentSchedule().get().setName(new_name)
                        logger.info(f"    * {column} renamed to {new_name}")
                elif column == 'Steam Equipment Load Name' and target_space_type.steamEquipment():
                    target_space_type.steamEquipment()[0].setName(new_name)
                    logger.info(f"    * {column} renamed to {new_name}")
                elif column == 'Steam Equipment Definition' and target_space_type.steamEquipment():
                    target_space_type.steamEquipment()[0].definition().setName(new_name)
                    logger.info(f"    * {column} renamed to {new_name}")
                elif column == 'Steam Equipment Schedule' and target_space_type.defaultScheduleSet().is_initialized():
                    sch_set = target_space_type.defaultScheduleSet().get()
                    if sch_set.steamEquipmentSchedule().is_initialized():
                        sch_set.steamEquipmentSchedule().get().setName(new_name)
                        logger.info(f"    * {column} renamed to {new_name}")
                elif column == 'Other Equipment Load Name' and target_space_type.otherEquipment():
                    target_space_type.otherEquipment()[0].setName(new_name)
                    logger.info(f"    * {column} renamed to {new_name}")
                elif column == 'Other Equipment Definition' and target_space_type.otherEquipment():
                    target_space_type.otherEquipment()[0].definition().setName(new_name)
                    logger.info(f"    * {column} renamed to {new_name}")
                elif column == 'Other Equipment Schedule' and target_space_type.defaultScheduleSet().is_initialized():
                    sch_set = target_space_type.defaultScheduleSet().get()
                    if sch_set.otherEquipmentSchedule().is_initialized():
                        sch_set.otherEquipmentSchedule().get().setName(new_name)
                        logger.info(f"    * {column} renamed to {new_name}")
                elif column == 'Internal Mass Name' and target_space_type.internalMass():
                    target_space_type.internalMass()[0].setName(new_name)
                    logger.info(f"    * {column} renamed to {new_name}")
                elif column == 'Internal Mass Definition' and target_space_type.internalMass():
                    target_space_type.internalMass()[0].definition().setName(new_name)   
                elif column == 'Infiltration Schedule' and target_space_type.defaultScheduleSet().is_initialized():
                    sch_set = target_space_type.defaultScheduleSet().get()
                    if sch_set.infiltrationSchedule().is_initialized():
                        sch_set.infiltrationSchedule().get().setName(new_name)
                        logger.info(f"    * {column} renamed to {new_name}")


    


def create_complete_edit_space_types_components(osm_model: openstudio.model.Model, space_type_name_list: list[str], create_if_none: bool = False) -> openstudio.model.Model:
    """
    Ensure all components (Schedules, Loads, Definitions) of specified space types follow standard naming and assignment conventions, creating them if necessary.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - space_type_name_list (list[str]): List of space type names to process.
    - create_if_none (bool, optional): If True, missing components will be created. Defaults to False.

    Returns:
    - openstudio.model.Model: The updated OpenStudio Model object.
    """
    # Rename all space types components
    rename_space_types_components(osm_model, space_type_name_list)

    # Get all space types
    all_space_types_df = get_all_space_types_objects_as_dataframe(osm_model)
    if all_space_types_df.empty:
        return osm_model
    
    filtered_df = all_space_types_df[all_space_types_df['Name'].isin(space_type_name_list)].reset_index(drop=True)

    # Default Schedule Set
    for index, row in filtered_df.iterrows():
        new_name = f"{row['Name']} Schedule Set"
        curr_val = row.get('Default Schedule Set')
        
        # Create a new object and assign it
        if (create_if_none and curr_val is None) or (curr_val is not None and curr_val != new_name):
            # Create new object
            new_sch_set = openstudio.model.DefaultScheduleSet(osm_model)
            new_sch_set.setName(new_name)
            logger.info(f"* Default Schedule Set: {new_name} - created")
            
            # Assign it to the corresponding space type
            st_obj = osm_model.getSpaceTypeByName(row['Name'])
            if st_obj.is_initialized():
                st_obj.get().setDefaultScheduleSet(new_sch_set)
                logger.info(f"* Default Schedule Set: {new_name} - assigned")

    # Design Specification Outdoor Air
    for index, row in filtered_df.iterrows():
        new_name = f"{row['Name']} Ventilation"
        curr_val = row.get('Design Specification Outdoor Air')
        
        if (create_if_none and curr_val is None) or (curr_val is not None and curr_val != new_name):
            new_oa = openstudio.model.DesignSpecificationOutdoorAir(osm_model)
            new_oa.setName(new_name)
            new_oa.setOutdoorAirFlowAirChangesperHour(0)
            logger.info(f"* Design Specification Outdoor Air: {new_name} - created")
            
            st_obj = osm_model.getSpaceTypeByName(row['Name'])
            if st_obj.is_initialized():
                st_obj.get().setDesignSpecificationOutdoorAir(new_oa)
                logger.info(f"* Design Specification Outdoor Air: {new_name} - assigned")

    # Space Infiltration Design Flow Rates
    for index, row in filtered_df.iterrows():
        new_name = f"{row['Name']} Infiltration"
        curr_val = row.get('Space Infiltration Design Flow Rates')
        
        if (create_if_none and curr_val is None) or (curr_val is not None and curr_val != new_name):
            new_inf = openstudio.model.SpaceInfiltrationDesignFlowRate(osm_model)
            new_inf.setName(new_name)
            new_inf.setAirChangesperHour(0)
            logger.info(f"* Space Infiltration Design Flow Rates: {new_name} - created")
            
            st_obj = osm_model.getSpaceTypeByName(row['Name'])
            if st_obj.is_initialized():
                new_inf.setSpaceType(st_obj.get())
                logger.info(f"* Space Infiltration Design Flow Rates: {new_name} - assigned")

    # People & People Definition
    for index, row in filtered_df.iterrows():
        people_new_name = f"{row['Name']} People"
        people_definition_new_name = f"{row['Name']} People Definition"
        curr_val = row.get('People Load Name')
        
        if (create_if_none and curr_val is None) or (curr_val is not None and curr_val != people_new_name):
            # Create People:Definition object first
            people_definition = openstudio.model.PeopleDefinition(osm_model)
            people_definition.setName(people_definition_new_name)
            people_definition.setNumberofPeople(0)
            logger.info(f"* People Definition: {people_definition_new_name} - created")
            
            # Create People object from People:Definition
            people = openstudio.model.People(people_definition)
            people.setName(people_new_name)
            logger.info(f"* People: {people_new_name} - created & assigned definition")
            
            st_obj = osm_model.getSpaceTypeByName(row['Name'])
            if st_obj.is_initialized():
                people.setSpaceType(st_obj.get())
                logger.info(f"* People: {people_new_name} - assigned")

    # Lights & Lights Definition
    for index, row in filtered_df.iterrows():
        lights_new_name = f"{row['Name']} Lights"
        lights_definition_new_name = f"{row['Name']} Lights Definition"
        curr_val = row.get('Lights Load Name')
        
        if (create_if_none and curr_val is None) or (curr_val is not None and curr_val != lights_new_name):
            lights_definition = openstudio.model.LightsDefinition(osm_model)
            lights_definition.setName(lights_definition_new_name)
            lights_definition.setLightingLevel(0)
            logger.info(f"* Lights Definition: {lights_definition_new_name} - created")
            
            lights = openstudio.model.Lights(lights_definition)
            lights.setName(lights_new_name)
            logger.info(f"* Lights: {lights_new_name} - created & assigned definition")
            
            st_obj = osm_model.getSpaceTypeByName(row['Name'])
            if st_obj.is_initialized():
                lights.setSpaceType(st_obj.get())
                logger.info(f"* Lights: {lights_new_name} - assigned")

    # Electric Equipment & Electric Equipment Definition
    for index, row in filtered_df.iterrows():
        elect_eqp_new_name = f"{row['Name']} Electric Equipment"
        elect_eqp_definition_new_name = f"{row['Name']} Electric Equipment Definition"
        curr_val = row.get('Electric Equipment Load Name')
        
        if (create_if_none and curr_val is None) or (curr_val is not None and curr_val != elect_eqp_new_name):
            elect_eqp_definition = openstudio.model.ElectricEquipmentDefinition(osm_model)
            elect_eqp_definition.setName(elect_eqp_definition_new_name)
            elect_eqp_definition.setDesignLevel(0)
            logger.info(f"* ElectricEquipment Definition: {elect_eqp_definition_new_name} - created")
            
            elect_eqp = openstudio.model.ElectricEquipment(elect_eqp_definition)
            elect_eqp.setName(elect_eqp_new_name)
            logger.info(f"* Electric Equipment: {elect_eqp_new_name} - created & assigned definition")
            
            st_obj = osm_model.getSpaceTypeByName(row['Name'])
            if st_obj.is_initialized():
                elect_eqp.setSpaceType(st_obj.get())
                logger.info(f"* Electric Equipment: {elect_eqp_new_name} - assigned")

    # SCHEDULES
    # ----------

    # Refresh DataFrame to pick up new assignments if any
    all_space_types_df = get_all_space_types_objects_as_dataframe(osm_model)
    filtered_df = all_space_types_df[all_space_types_df['Name'].isin(space_type_name_list)].reset_index(drop=True)

    # Helper function for schedule processing
    def process_schedule(row, col_name, suffix, sch_type, setter_func_name):
        new_sch_name = f"{row['Name']} {suffix}"
        curr_val = row.get(col_name)
        if (create_if_none and curr_val is None) or (curr_val is not None and curr_val != new_sch_name):
            create_new_schedule_ruleset(osm_model, new_sch_name, sch_type)
            sch_obj = osm_model.getScheduleByName(new_sch_name)
            if sch_obj.is_initialized():
                dss_name = row.get('Default Schedule Set')
                if dss_name:
                    dss_obj = osm_model.getDefaultScheduleSetByName(dss_name)
                    if dss_obj.is_initialized():
                        getattr(dss_obj.get(), setter_func_name)(sch_obj.get())
                        logger.info(f"* {suffix}: {new_sch_name} - created and assigned to {dss_name}")

    for _, row in filtered_df.iterrows():
        process_schedule(row, 'People Number Of People Schedule', 'Number Of People Schedule', 'InternalGains', 'setNumberofPeopleSchedule')
        process_schedule(row, 'People Activity Level Schedule', 'People Activity Level Schedule', 'ActivityLevel', 'setPeopleActivityLevelSchedule')
        process_schedule(row, 'Lighting Schedule', 'Lighting Schedule', 'InternalGains', 'setLightingSchedule')
        process_schedule(row, 'Electric Equipment Schedule', 'Electric Equipment Schedule', 'InternalGains', 'setElectricEquipmentSchedule')
        process_schedule(row, 'Infiltration Schedule', 'Infiltration Schedule', 'InternalGains', 'setInfiltrationSchedule')
    
    return osm_model
