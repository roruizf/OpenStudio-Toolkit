import openstudio
import pandas as pd
import numpy as np
from osm_objects.schedules import *


def get_all_space_types_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all space types objects from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all space types objects.
    """

    # Get all spaces in the OpenStudio model.
    all_space_types = osm_model.getSpaceTypes()

    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_space_types],
        'Name': [x.name().get() for x in all_space_types],
        'Default Construction Set Name': [x.defaultConstructionSet().get().name().get() if not x.defaultConstructionSet().isNull() else None for x in all_space_types],
        'Default Schedule Set Name': [x.defaultScheduleSet().get().name().get() if not x.defaultScheduleSet().isNull() else None for x in all_space_types],
        'Group Rendering Name': [x.renderingColor().get().name().get() if not x.renderingColor().isNull() else None for x in all_space_types],
        'Design Specification Outdoor Air Object Name': [x.designSpecificationOutdoorAir().get().name().get() if not x.designSpecificationOutdoorAir().isNull() else None for x in all_space_types],
        'Standards Template': [x.standardsTemplate().get() if not x.standardsTemplate().isNull() else None for x in all_space_types],
        'Standards Building Type': [x.standardsBuildingType().get() if not x.standardsBuildingType().isNull() else None for x in all_space_types],
        'Standards Space Type': [x.standardsSpaceType().get() if not x.standardsSpaceType().isNull() else None for x in all_space_types]
    }

    # Create a DataFrame of all space types.
    all_space_types_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_space_types_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_space_types_df = all_space_types_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(f"The OSM model contains {all_space_types_df.shape[0]} space types")

    return all_space_types_df


def get_all_space_types_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all space types from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all space types.
    """

    # Get all spaces in the OpenStudio model.
    all_space_types = osm_model.getSpaceTypes()

    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_space_types],
        'Name': [x.nameString() for x in all_space_types],
        'Rendering Color': [x.renderingColor().get().name().get(
        ) if not x.renderingColor().isNull() else None for x in all_space_types],
        'Default Construction Set': [x.defaultConstructionSet().get().name(
        ).get() if not x.defaultConstructionSet().isNull() else None for x in all_space_types],
        'Default Schedule Set': [x.defaultScheduleSet().get().name(
        ).get() if not x.defaultScheduleSet().isNull() else None for x in all_space_types],
        'Design Specification Outdoor Air': [x.designSpecificationOutdoorAir().get(
        ).name().get() if not x.designSpecificationOutdoorAir().isNull() else None for x in all_space_types],
        'Space Infiltration Design Flow Rates': [x.spaceInfiltrationDesignFlowRates(
        )[0].name().get() if x.spaceInfiltrationDesignFlowRates() else None for x in all_space_types],
        'Space Infiltration Effective Leakage Area': [x.spaceInfiltrationEffectiveLeakageAreas(
        )[0].name().get() if x.spaceInfiltrationEffectiveLeakageAreas() else None for x in all_space_types],
        # People
        'People Load Name': [x.people()[0].name().get() if x.people() else None for x in all_space_types],
        'People Definition': [x.people()[0].definition(
        ).name().get() if x.people() else None for x in all_space_types],
        'People Number Of People Schedule': [x.defaultScheduleSet().get().numberofPeopleSchedule().get().name(
        ).get() if not x.defaultScheduleSet().isNull() and not x.defaultScheduleSet().get().numberofPeopleSchedule().isNull() else None for x in all_space_types],
        'People Activity Level Schedule': [x.defaultScheduleSet().get().peopleActivityLevelSchedule().get().name(
        ).get() if not x.defaultScheduleSet().isNull() and not x.defaultScheduleSet().get().numberofPeopleSchedule().isNull() else None for x in all_space_types],
        # Lights
        'Lights Load Name': [x.lights()[0].name().get() if x.lights() else None for x in all_space_types],
        'Lights Definition': [x.lights()[0].definition().name().get() if x.lights() else None for x in all_space_types],
        'Lighting Schedule': [x.defaultScheduleSet().get().lightingSchedule().get().name().get(
        ) if not x.defaultScheduleSet().isNull() and not x.defaultScheduleSet().get().lightingSchedule().isNull() else None for x in all_space_types],
        # Electric Equipment
        'Electric Equipment Load Name': [x.electricEquipment(
        )[0].name().get() if x.electricEquipment() else None for x in all_space_types],
        'Electric Equipment Definition': [x.electricEquipment(
        )[0].definition().name().get() if x.electricEquipment() else None for x in all_space_types],
        'Electric Equipment Schedule': [x.defaultScheduleSet().get().electricEquipmentSchedule().get().name().get(
        ) if not x.defaultScheduleSet().isNull() and not x.defaultScheduleSet().get().electricEquipmentSchedule().isNull() else None for x in all_space_types],
        # Infiltration
        'Infiltration Schedule': [x.defaultScheduleSet().get().infiltrationSchedule().get().name().get(
        ) if not x.defaultScheduleSet().isNull() and not x.defaultScheduleSet().get().infiltrationSchedule().isNull() else None for x in all_space_types]}

    # Create a DataFrame of all space types.
    all_space_types_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_space_types_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_space_types_df = all_space_types_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(f"The OSM model contains {all_space_types_df.shape[0]} space types")

    return all_space_types_df

def create_new_space_types_objects(osm_model: openstudio.model.Model, space_types_to_create_df: pd.DataFrame) -> None:
    """
    Create new space types components based on data from a New Objects DataFrame.

    Parameters:
    - osm_model: The OpenStudio Model object.
    - space_types_to_create_df: DataFrame containing data for new building story components.

    Returns:
    - None
    """
    space_types_to_create_df = space_types_to_create_df.replace(np.nan, None)

    for _, row in space_types_to_create_df.iterrows():
        new_space_type = openstudio.model.SpaceType(osm_model)
        new_space_type.setName(row['Name'])

        # Setting attributes if defined in space_types_to_create_df

        # Default Construction Set Name
        if row['Default Construction Set Name'] is not None:
            new_construction_set = openstudio.model.DefaultConstructionSet(
                osm_model)
            new_space_type.setDefaultConstructionSet(new_construction_set)
        
        # Default Schedule Set Name
        if row['Default Schedule Set Name'] is not None:
            new_schedule_set = openstudio.model.DefaultScheduleSet(osm_model)
            new_space_type.setDefaultScheduleSet(new_schedule_set)
        
        # Group Rendering Name   
        if row['Group Rendering Name'] is not None:
            if osm_model.getRenderingColorByName(row['Group Rendering Name']).isNull():
                rendering_color = openstudio.model.RenderingColor(osm_model)
            else:
                rendering_color = osm_model.getRenderingColorByName(row['Group Rendering Name']).get()

            rendering_color.setName(row['Group Rendering Name'])
            new_space_type.setRenderingColor(rendering_color)
       
        # Design Specification Outdoor Air Object Name
        if row['Design Specification Outdoor Air Object Name'] is not None:
            pass
        
        # Standards Template	
        # Standards Building Type	
        # Standards Space Type
    print(f"{space_types_to_create_df.shape[0]} new space types objects created")

def rename_space_types_components(osm_model: openstudio.model.Model, space_type_name_list: list) -> None:

    # Get all space types
    all_space_types_df = get_all_space_types_as_dataframe(osm_model)
    all_space_types_df = all_space_types_df[all_space_types_df['Name'].isin(space_type_name_list)].reset_index(drop=True)


    for index, row in all_space_types_df.iterrows():

        space_type_name = row['Name']
        space_type_handle = row['Handle']

        # Get Space Type row by row
        space_type = osm_model.getSpaceType(row['Handle']).get()

        print(f"{index + 1}. {space_type_name}:")

        # Rendering Color
        new_name = f"{space_type_name} Rendering Color"
        if row['Rendering Color'] is not None and row['Rendering Color'] != new_name:
            print(
                f"    * Rendering Color Name changed: from {row['Rendering Color']} to {new_name}")
            # Reset Name
            space_type.renderingColor().get().setName(new_name)

        # Default Construction Set
        new_name = f"{space_type_name} Construction Set"
        if row['Default Construction Set'] is not None and row['Default Construction Set'] != new_name:
            print(
                f"    * Construction Set Name changed: from {row['Default Construction Set']} to {new_name}")
            # Reset Name
            space_type.defaultConstructionSet().get().setName(new_name)

        # Rename Default Schedule Set
        new_name = f"{space_type_name} Schedule Set"
        if row['Default Schedule Set'] is not None and row['Default Schedule Set'] != new_name:
            print(
                f"    * Schedule Set Name changed: from {row['Default Schedule Set']} to {new_name}")
            # Reset Name
            space_type.defaultScheduleSet().get().setName(new_name)

        # Rename Design Specification Outdoor Air
        new_name = f"{space_type_name} Ventilation"
        if row['Design Specification Outdoor Air'] is not None and row['Design Specification Outdoor Air'] != new_name:
            print(
                f"    * Design Specification Outdoor Air Name changed: from {row['Design Specification Outdoor Air']} to {new_name}")
            # Reset Name
            space_type.designSpecificationOutdoorAir().get().setName(new_name)

        # Space Infiltration Design Flow Rates
        new_name = f"{space_type_name} Infiltration"
        if row['Space Infiltration Design Flow Rates'] is not None and row['Space Infiltration Design Flow Rates'] != new_name:
            print(
                f"    * Space Infiltration Design Flow Rates Name changed: from {row['Space Infiltration Design Flow Rates']} to {new_name}")
            space_type.spaceInfiltrationDesignFlowRates()[0].setName(new_name)

        # Space Infiltration Effective Leakage Area
        # pass

        # People
        new_name = f"{space_type_name} People"
        if row['People Load Name'] is not None and row['People Load Name'] != new_name:
            print(
                f"    * People Load Name changed: from {row['People Load Name']} to {new_name}")
            space_type.people()[0].setName(new_name)

        # People Definition
        new_name = f"{space_type_name} People Definition"
        if row['People Definition'] is not None and row['People Definition'] != new_name:
            print(
                f"    * People Definition Name changed: from {row['People Definition']} to {new_name}")
            space_type.people()[0].definition().setName(new_name)

        # People Number Of People Schedule
        # pass

        # People Activity Level Schedule
        # pass

        # Lights Load Name
        new_name = f"{space_type_name} Lights"
        if row['Lights Load Name'] is not None and row['Lights Load Name'] != new_name:
            print(
                f"    * Lights Load Name changed: from {row['Lights Load Name']} to {new_name}")
            space_type.lights()[0].setName(new_name)

        # Lights Definition
        new_name = f"{space_type_name} Lights Definition"
        if row['Lights Definition'] is not None and row['Lights Definition'] != new_name:
            print(
                f"    * Lights Definition Name changed: from {row['Lights Definition']} to {new_name}")
            space_type.lights()[0].definition().setName(new_name)

        # Lighting Schedule
        # pass

        # Electric Equipment Load Name
        new_name = f"{space_type_name} Elec Equip"
        if row['Electric Equipment Load Name'] is not None and row['Electric Equipment Load Name'] != new_name:
            print(
                f"    * Electric Equipment Load Name changed: from {row['Electric Equipment Load Name']} to {new_name}")
            space_type.electricEquipment()[0].setName(new_name)

        # Electric Equipment Definition
        new_name = f"{space_type_name} Elec Equip Definition"
        if row['Electric Equipment Definition'] is not None and row['Electric Equipment Definition'] != new_name:
            print(
                f"    * Electric Equipment Definition changed: from {row['Electric Equipment Definition']} to {new_name}")
            space_type.electricEquipment()[0].definition().setName(new_name)

        # Electric Equipment Schedule
        # pass

        # Infiltration Schedule
        # pass


def create_complete_edit_space_types_components(osm_model: openstudio.model.Model, space_type_name_list: list, create_if_none: bool = False) -> None:

    # Rename all space types components
    rename_space_types_components(osm_model, space_type_name_list)

    # Get all space types
    all_space_types_df = get_all_space_types_as_dataframe(osm_model)
    all_space_types_df = all_space_types_df[all_space_types_df['Name'].isin(space_type_name_list)].reset_index(drop=True)

    # Default Schedule Set
    for index, row in all_space_types_df.iterrows():
        new_name = f"{row['Name']} Schedule Set"
        # Create a new object and assig it
        if (create_if_none and row['Default Schedule Set'] == None) or (row['Default Schedule Set'] != None and row['Default Schedule Set'] != new_name):
            # Create new object
            new = openstudio.model.DefaultScheduleSet(osm_model)
            new.setName(new_name)
            print(f"* Default Schedule Set: {new.name()} - created")
            # Assign it to the corresponding space type
            osm_model.getSpaceTypeByName(
                row['Name']).get().setDefaultScheduleSet(new)
            print(f"* Default Schedule Set: {new.name()} - assigned")

    # Design Specification Outdoor Air
    for index, row in all_space_types_df.iterrows():
        new_name = f"{row['Name']} Ventilation"
        # Create a new object and assig it
        if (create_if_none and row['Design Specification Outdoor Air'] == None) or (row['Design Specification Outdoor Air'] != None and row['Design Specification Outdoor Air'] != new_name):
            # Create new object
            new = openstudio.model.DesignSpecificationOutdoorAir(osm_model)
            new.setName(new_name)
            new.setOutdoorAirFlowAirChangesperHour(0)
            print(
                f"* Design Specification Outdoor Air: {new.name()} - created")
            # Assign it to the corresponding space type
            osm_model.getSpaceTypeByName(row['Name']).get(
            ).setDesignSpecificationOutdoorAir(new)
            print(
                f"* Design Specification Outdoor Air: {new.name()} - assigned")

    # Space Infiltration Design Flow Rates
    for index, row in all_space_types_df.iterrows():
        new_name = f"{row['Name']} Infiltration"
        # Create a new object and assig it
        if (create_if_none and row['Space Infiltration Design Flow Rates'] == None) or (row['Space Infiltration Design Flow Rates'] != None and row['Space Infiltration Design Flow Rates'] != new_name):
            new = openstudio.model.SpaceInfiltrationDesignFlowRate(osm_model)
            new.setName(new_name)
            new.setAirChangesperHour(0)
            print(
                f"* Space Infiltration Design Flow Rates: {new.name()} - created")
            # Assign it to the corresponding space type - In this case, space type is assigned to Space Infiltration Design Flow Rate
            new.setSpaceType(osm_model.getSpaceTypeByName(row['Name']).get())
            print(
                f"* Space Infiltration Design Flow Rates: {new.name()} - assigned")
    # Space Infiltration Effective Leakage Area
            # pass

    # People & People Definition
    for index, row in all_space_types_df.iterrows():
        people_new_name = f"{row['Name']} People"
        people_definition_new_name = f"{row['Name']} People Definition"
        # Create a new object and assig it
        if (create_if_none and row['People Load Name'] == None) or (row['People Load Name'] != None and row['People Load Name'] != people_new_name):
            # Create People:Definition object first
            people_definition = openstudio.model.PeopleDefinition(osm_model)
            people_definition.setName(people_definition_new_name)
            people_definition.setNumberofPeople(0)
            print(f"* People Definition: {people_definition.name()} - created")
            # Create People object from People:Definition
            people = openstudio.model.People(people_definition)
            people.setName(people_new_name)
            print(f"* People: {people.name()} - created")
            print(
                f"* People Definition: {people_definition.name()} - assigned")
            # Assign it to the corresponding space type - In this case, space type is assigned to People
            people.setSpaceType(
                osm_model.getSpaceTypeByName(row['Name']).get())
            print(f"* People: {people.name()} - assigned")

    # Lights & Lights Definition
    for index, row in all_space_types_df.iterrows():
        lights_new_name = f"{row['Name']} Lights"
        lights_definition_new_name = f"{row['Name']} Lights Definition"
        # Create a new object and assig it
        if (create_if_none and row['Lights Load Name'] == None) or (row['Lights Load Name'] != None and row['Lights Load Name'] != lights_new_name):
            # Create Lights:Definition object first
            lights_definition = openstudio.model.LightsDefinition(osm_model)
            lights_definition.setName(lights_definition_new_name)
            lights_definition.setLightingLevel(0)
            print(f"* Lights Definition: {lights_definition.name()} - created")
            # Create Lights object from Lights:Definition
            lights = openstudio.model.Lights(lights_definition)
            lights.setName(lights_new_name)
            print(f"* Lights: {lights.name()} - created")
            print(
                f"* Lights Definition: {lights_definition.name()} - assigned")
            # Assign it to the corresponding space type - In this case, space type is assigned to People
            lights.setSpaceType(
                osm_model.getSpaceTypeByName(row['Name']).get())
            print(f"* Lights: {lights.name()} - assigned")

    # Electric Equipment & Electric Equipment Definition
    for index, row in all_space_types_df.iterrows():
        elect_eqp_new_name = f"{row['Name']} Electric Equipment"
        elect_eqp_definition_new_name = f"{row['Name']} Electric Equipment Definition"
        # Create a new object and assig it
        if (create_if_none and row['Electric Equipment Load Name'] == None) or (row['Electric Equipment Load Name'] != None and row['Electric Equipment Load Name'] != elect_eqp_new_name):
            # Create ElectricEquipment:Definition object first
            elect_eqp_definition = openstudio.model.ElectricEquipmentDefinition(
                osm_model)
            elect_eqp_definition.setName(elect_eqp_definition_new_name)
            elect_eqp_definition.setDesignLevel(0)
            print(
                f"* ElectricEquipment Definition: {elect_eqp_definition.name()} - created")
            # Create ElectricEquipment object from ElectricEquipment:Definition
            elect_eqp = openstudio.model.ElectricEquipment(
                elect_eqp_definition)
            elect_eqp.setName(elect_eqp_new_name)
            print(f"* Electric Equipment: {elect_eqp.name()} - created")
            print(
                f"* Electric Equipment Definition: {elect_eqp_definition.name()} - assigned")
            # Assign it to the corresponding space type - In this case, space type is assigned to People
            elect_eqp.setSpaceType(
                osm_model.getSpaceTypeByName(row['Name']).get())
            print(f"* Electric Equipment: {elect_eqp.name()} - assigned")

    # SCHEDULES
    # ----------

    # Get all space types (again)
    all_space_types_df = get_all_space_types_as_dataframe(osm_model)
    all_space_types_df = all_space_types_df[all_space_types_df['Name'].isin(space_type_name_list)].reset_index(drop=True)

    # People Number Of People Schedule
    for index, row in all_space_types_df.iterrows():
        schdle_ruleset_name = f"{row['Name']} Number Of People Schedule"
        schdle_ruleset_type = 'InternalGains'
        # Create a new object and assig it
        if (create_if_none and row['People Number Of People Schedule'] == None) or (row['People Number Of People Schedule'] != None and row['People Number Of People Schedule'] != new_name):
            # Create new object
            create_new_schedule_ruleset(
                osm_model, schdle_ruleset_name, schdle_ruleset_type)
            schdle_ruleset = osm_model.getScheduleByName(schdle_ruleset_name)
            # Assign it to the corresponding Default Schedule Set
            osm_model.getDefaultScheduleSetByName(row['Default Schedule Set']).get(
            ).setNumberofPeopleSchedule(schdle_ruleset.get())
    # People Activity Level Schedule
    for index, row in all_space_types_df.iterrows():
        schdle_ruleset_name = f"{row['Name']} People Activity Level Schedule"
        schdle_ruleset_type = 'ActivityLevel'
        # Create a new object and assig it
        if (create_if_none and row['People Activity Level Schedule'] == None) or (row['People Activity Level Schedule'] != None and row['People Activity Level Schedule'] != new_name):
            # Create new object
            create_new_schedule_ruleset(
                osm_model, schdle_ruleset_name, schdle_ruleset_type)
            schdle_ruleset = osm_model.getScheduleByName(schdle_ruleset_name)
            # Assign it to the corresponding Default Schedule Set
            osm_model.getDefaultScheduleSetByName(row['Default Schedule Set']).get(
            ).setPeopleActivityLevelSchedule(schdle_ruleset.get())
    # Lighting Schedule
    for index, row in all_space_types_df.iterrows():
        schdle_ruleset_name = f"{row['Name']} Lighting Schedule"
        schdle_ruleset_type = 'InternalGains'
        # Create a new object and assig it
        if (create_if_none and row['Lighting Schedule'] == None) or (row['Lighting Schedule'] != None and row['Lighting Schedule'] != new_name):
            # Create new object
            create_new_schedule_ruleset(
                osm_model, schdle_ruleset_name, schdle_ruleset_type)
            schdle_ruleset = osm_model.getScheduleByName(schdle_ruleset_name)
            # Assign it to the corresponding Default Schedule Set
            osm_model.getDefaultScheduleSetByName(
                row['Default Schedule Set']).get().setLightingSchedule(schdle_ruleset.get())

    # Electric Equipment Schedule
    for index, row in all_space_types_df.iterrows():
        schdle_ruleset_name = f"{row['Name']} Electric Equipment Schedule"
        schdle_ruleset_type = 'InternalGains'
        # Create a new object and assig it
        if (create_if_none and row['Electric Equipment Schedule'] == None) or (row['Electric Equipment Schedule'] != None and row['Electric Equipment Schedule'] != new_name):
            # Create new object
            create_new_schedule_ruleset(
                osm_model, schdle_ruleset_name, schdle_ruleset_type)
            schdle_ruleset = osm_model.getScheduleByName(schdle_ruleset_name)
            # Assign it to the corresponding Default Schedule Set
            osm_model.getDefaultScheduleSetByName(row['Default Schedule Set']).get(
            ).setElectricEquipmentSchedule(schdle_ruleset.get())

    # Infiltration Schedule
    for index, row in all_space_types_df.iterrows():
        schdle_ruleset_name = f"{row['Name']} Infiltration Schedule"
        schdle_ruleset_type = 'InternalGains'
        # Create a new object and assig it
        if (create_if_none and row['Infiltration Schedule'] == None) or (row['Infiltration Schedule'] != None and row['Infiltration Schedule'] != new_name):
            # Create new object
            create_new_schedule_ruleset(
                osm_model, schdle_ruleset_name, schdle_ruleset_type)
            schdle_ruleset = osm_model.getScheduleByName(schdle_ruleset_name)
            # Assign it to the corresponding Default Schedule Set
            osm_model.getDefaultScheduleSetByName(row['Default Schedule Set']).get(
            ).setInfiltrationSchedule(schdle_ruleset.get())
