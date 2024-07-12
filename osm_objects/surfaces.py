import openstudio
import pandas as pd


def get_all_surface_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:

    # Get all surfaces in the OpenStudio model.
    all_surfaces = osm_model.getSurfaces()
    # Define attributtes to retrieve in a dictionary
    object_attr = {
        'Handle': [str(x.handle()) for x in all_surfaces],
        'Name': [x.name().get() for x in all_surfaces],
        'Surface Type': [x.surfaceType() for x in all_surfaces],
        'Construction Name': [x.construction().get().name().get() if not x.construction().isNull() else None for x in all_surfaces],
        'Space Name': [x.space().get().name().get()
                       for x in all_surfaces],
        'Outside Boundary Condition': [x.outsideBoundaryCondition() for x in all_surfaces],
        'Outside Boundary Condition Object': [x.adjacentSurface().get().name(
        ).get() if not x.adjacentSurface().isNull() else None for x in all_surfaces],
        'Sun Exposure': [x.sunExposure() for x in all_surfaces],
        'Wind Exposure': [x.windExposure() for x in all_surfaces],
        'View Factor to Ground': None,
        'Number of Vertices': None
        # 'X,Y,Z Vertex 1 {m}': None,
        # 'X,Y,Z Vertex 2 {m}': None,
        # 'X,Y,Z Vertex 3 {m}': None,
        # 'X,Y,Z Vertex 4 {m}': None,
        # 'X,Y,Z Vertex 5 {m}': None,
        # 'X,Y,Z Vertex 6 {m}': None
    }
    # Create a DataFrame of all spaces.
    all_surfaces_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_surfaces_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the SpaceName column and reset indexes
    all_surfaces_df = all_surfaces_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(f"The OSM model contains {all_surfaces_df.shape[0]} surfaces")

    return all_surfaces_df
