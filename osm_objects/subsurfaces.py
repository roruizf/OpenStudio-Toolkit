import openstudio
import pandas as pd


def get_all_subsurface_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Retrieve all subsurfaces from the OpenStudio model and organize them into a pandas DataFrame.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - pd.DataFrame: DataFrame containing information about all subsurfaces.
    """

    # Get all subsurfaces in the OpenStudio model.
    all_subsurfaces = osm_model.getSubSurfaces()

    # Define attributes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_subsurfaces],
        'Name': [x.nameString() for x in all_subsurfaces],
        'Sub Surface Type': [x.subSurfaceType() for x in all_subsurfaces],
        'Construction Name': [x.construction().get().name().get() if not x.construction().isNull() else None for x in all_subsurfaces],
        'Surface Name': [x.parent().get().name().get() for x in all_subsurfaces],
        'Outside Boundary Condition Object': [x.outsideBoundaryCondition() for x in all_subsurfaces],
        'View Factor to Ground': None,
        'Frame and Divider Name': [x.windowPropertyFrameAndDivider().get().name().get() if not x.windowPropertyFrameAndDivider().isNull() else None for x in all_subsurfaces],
        'Multiplier': None,
        'Number of Vertices': None
        # 'X,Y,Z Vertex 1 {m}': None,
        # 'X,Y,Z Vertex 2 {m}': None,
        # 'X,Y,Z Vertex 3 {m}': None,
        # 'X,Y,Z Vertex 4 {m}': None
    }

    # Create a DataFrame of all spaces.
    all_subsurfaces_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_subsurfaces_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_subsurfaces_df = all_subsurfaces_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(f"The OSM model contains {all_subsurfaces_df.shape[0]} sub-surfaces")
    return all_subsurfaces_df
