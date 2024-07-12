import openstudio
import pandas as pd


def get_all_space_objects_into_a_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all spaces from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all spaces.
    """

    # Get all spaces in the OpenStudio model.
    all_spaces = osm_model.getSpaces()

    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_spaces],
        'Name': [x.name().get() for x in all_spaces],
        'Space Type Name': [x.spaceType().get().name().get() if not x.spaceType().isNull() else None for x in all_spaces],
        'Default Construction Set Name': [x.defaultConstructionSet().get().name().get() if not x.defaultConstructionSet().isNull() else None for x in all_spaces],
        'Default Schedule Set Name': [x.defaultScheduleSet().get().name().get() if not x.defaultScheduleSet().isNull() else None for x in all_spaces],
        'Direction of Relative North {deg}': [x.directionofRelativeNorth() for x in all_spaces],
        'X Origin {m}': None,
        'Y Origin {m}': None,
        'Z Origin {m}': None,
        'Building Story Name': [x.buildingStory().get().name().get() if not x.buildingStory().isNull() else None for x in all_spaces],
        'Thermal Zone Name': [x.thermalZone().get().name().get() if not x.thermalZone().isNull() else None for x in all_spaces],
        'Part of Total Floor Area': [x.partofTotalFloorArea() for x in all_spaces],
        'Design Specification Outdoor Air Object Name': None,
        'Building Unit Name': [x.buildingUnit().get().name().get() if not x.buildingUnit().isNull() else None for x in all_spaces],
        'Volume {m3}': [x.volume() for x in all_spaces],
        'Ceiling Height {m}': [x.ceilingHeight() for x in all_spaces],
        'Floor Area {m2}': [x.floorArea() for x in all_spaces]
    }

    # Create a DataFrame of all spaces.
    all_spaces_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_spaces_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_spaces_df = all_spaces_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(f"The OSM model contains {all_spaces_df.shape[0]} spaces")

    return all_spaces_df