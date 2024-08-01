import openstudio
import pandas as pd
import numpy as np


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