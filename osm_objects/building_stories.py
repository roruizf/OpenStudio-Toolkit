import openstudio
import pandas as pd

def get_building_storys_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all building stories from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all building stories.
    """

    # Get all building storeys in the OpenStudio model.
    all_building_stories = osm_model.getBuildingStorys()

    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_building_stories],
        'Name': [x.name().get() for x in all_building_stories],
        'Nominal Z Coordinate {m}': [x.nominalZCoordinate().get() if not x.nominalZCoordinate().isNull() else None for x in all_building_stories],
        'Nominal Floor to Floor Height {m}': [x.nominalFloortoFloorHeight().get() if not x.nominalFloortoFloorHeight().isNull() else None for x in all_building_stories],
        'Default Construction Set Name': [x.defaultConstructionSet().get().name().get() if not x.defaultConstructionSet().isNull() else None for x in all_building_stories],
        'Default Schedule Set Name': [x.defaultScheduleSet().get().name().get() if not x.defaultScheduleSet().isNull() else None for x in all_building_stories],
        'Group Rendering Name': [x.renderingColor().get().name().get() if not x.renderingColor().isNull() else None for x in all_building_stories],
        'Nominal Floor to Ceiling Height {m}': [x.nominalFloortoCeilingHeight().get() if not x.nominalFloortoCeilingHeight().isNull() else None for x in all_building_stories]
    }

    # Create a DataFrame of building.
    all_building_stories_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_building_stories_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_building_stories_df = all_building_stories_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    return all_building_stories_df