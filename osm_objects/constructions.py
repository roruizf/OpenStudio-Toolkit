import openstudio
import pandas as pd


def get_all_default_construction_set_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    # Get all spaces in the OpenStudio model.
    all_default_construction_sets = osm_model.getDefaultConstructionSets()

    # Define attributtes to retrieve in a dictionary
    object_attr = {'Handle': [str(x.handle()) for x in all_default_construction_sets],
                   'Name': [x.name().get() for x in all_default_construction_sets],
                   'Default Exterior Surface Constructions Name': [x.defaultExteriorSurfaceConstructions().get().name().get() if not x.defaultExteriorSurfaceConstructions().isNull() else None for x in all_default_construction_sets],
                   'Default Interior Surface Constructions Name': [x.defaultInteriorSurfaceConstructions().get().name().get() if not x.defaultInteriorSurfaceConstructions().isNull() else None for x in all_default_construction_sets],
                   'Default Ground Contact Surface Constructions Name': [x.defaultGroundContactSurfaceConstructions().get().name().get() if not x.defaultGroundContactSurfaceConstructions().isNull() else None for x in all_default_construction_sets],
                   'Default Exterior SubSurface Constructions Name': [x.defaultExteriorSubSurfaceConstructions().get().name().get() if not x.defaultExteriorSubSurfaceConstructions().isNull() else None for x in all_default_construction_sets],
                   'Default Interior SubSurface Constructions Name': [x.defaultInteriorSubSurfaceConstructions().get().name().get() if not x.defaultInteriorSubSurfaceConstructions().isNull() else None for x in all_default_construction_sets],
                   'Interior Partition Construction Name': [x.interiorPartitionConstruction().get().name().get() if not x.interiorPartitionConstruction().isNull() else None for x in all_default_construction_sets],
                   'Space Shading Construction Name': [x.spaceShadingConstruction().get().name().get() if not x.spaceShadingConstruction().isNull() else None for x in all_default_construction_sets],
                   'Building Shading Construction Name': [x.buildingShadingConstruction().get().name().get() if not x.buildingShadingConstruction().isNull() else None for x in all_default_construction_sets],
                   'Site Shading Construction Name': [x.siteShadingConstruction().get().name().get() if not x.siteShadingConstruction().isNull() else None for x in all_default_construction_sets],
                   'Adiabatic Surface Construction Name': [x.adiabaticSurfaceConstruction().get().name().get() if not x.adiabaticSurfaceConstruction().isNull() else None for x in all_default_construction_sets]
                   }

    # Create a DataFrame of all spaces.
    all_default_construction_sets_df = pd.DataFrame(columns=object_attr.keys())
    for key in object_attr.keys():
        all_default_construction_sets_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_default_construction_sets_df = all_default_construction_sets_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(
        f"The OSM model contains {all_default_construction_sets_df.shape[0]} default construction sets")

    return all_default_construction_sets_df


def get_all_default_surface_construction_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    # Get all spaces in the OpenStudio model.
    all_default_surface_constructions = osm_model.getDefaultSurfaceConstructionss()

    # Define attributtes to retrieve in a dictionary
    object_attr = {'Handle': [str(x.handle()) for x in all_default_surface_constructions],
                   'Name': [x.name().get() for x in all_default_surface_constructions],
                   'Floor Construction Name': [x.floorConstruction().get().name().get() if not x.floorConstruction().isNull() else None for x in all_default_surface_constructions],
                   'Wall Construction Name': [x.wallConstruction().get().name().get() if not x.wallConstruction().isNull() else None for x in all_default_surface_constructions],
                   'Roof Ceiling Construction Name': [x.roofCeilingConstruction().get().name().get() if not x.roofCeilingConstruction().isNull() else None for x in all_default_surface_constructions]
                   }

    # Create a DataFrame of all spaces.
    all_default_surface_constructions_df = pd.DataFrame(
        columns=object_attr.keys())
    for key in object_attr.keys():
        all_default_surface_constructions_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_default_surface_constructions_df = all_default_surface_constructions_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(
        f"The OSM model contains {all_default_surface_constructions_df.shape[0]} default surface constructions")

    return all_default_surface_constructions_df


def get_all_default_subsurface_construction_objects_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:
    # Get all spaces in the OpenStudio model.
    all_default_subsurface_constructions = osm_model.getDefaultSubSurfaceConstructionss()

    # Define attributtes to retrieve in a dictionary
    object_attr = {'Handle': [str(x.handle()) for x in all_default_subsurface_constructions],
                   'Name': [x.name().get() for x in all_default_subsurface_constructions],
                   'Fixed Window Construction Name': [x.fixedWindowConstruction().get().name().get() if not x.fixedWindowConstruction().isNull() else None for x in all_default_subsurface_constructions],
                   'Operable Window Construction Name': [x.operableWindowConstruction().get().name().get() if not x.operableWindowConstruction().isNull() else None for x in all_default_subsurface_constructions],
                   'Door Construction Name': [x.doorConstruction().get().name().get() if not x.doorConstruction().isNull() else None for x in all_default_subsurface_constructions],
                   'Glass Door Construction Name': [x.glassDoorConstruction().get().name().get() if not x.glassDoorConstruction().isNull() else None for x in all_default_subsurface_constructions],
                   'Overhead Door Construction Name': [x.overheadDoorConstruction().get().name().get() if not x.overheadDoorConstruction().isNull() else None for x in all_default_subsurface_constructions],
                   'Skylight Construction Name': [x.skylightConstruction().get().name().get() if not x.skylightConstruction().isNull() else None for x in all_default_subsurface_constructions],
                   'Tubular Daylight Dome Construction Name': [x.tubularDaylightDomeConstruction().get().name().get() if not x.tubularDaylightDomeConstruction().isNull() else None for x in all_default_subsurface_constructions],
                   'Tubular Daylight Diffuser Construction Name': [x.tubularDaylightDiffuserConstruction().get().name().get() if not x.tubularDaylightDiffuserConstruction().isNull() else None for x in all_default_subsurface_constructions]
                   }

    # Create a DataFrame of all spaces.
    all_default_subsurface_constructions_df = pd.DataFrame(
        columns=object_attr.keys())
    for key in object_attr.keys():
        all_default_subsurface_constructions_df[key] = object_attr[key]

    # Sort the DataFrame alphabetically by the Name column and reset indexes
    all_default_subsurface_constructions_df = all_default_subsurface_constructions_df.sort_values(
        by='Name', ascending=True).reset_index(drop=True)

    print(
        f"The OSM model contains {all_default_subsurface_constructions_df.shape[0]} default subsurface constructions")
    return all_default_subsurface_constructions_df


def get_all_default_construction_set_component_as_dataframe(osm_model: openstudio.model.Model) -> pd.DataFrame:

    # Load required Data Frames
    all_default_construction_sets_df = get_all_default_construction_set_objects_as_dataframe(
        osm_model)
    all_default_surface_constructions_df = get_all_default_surface_construction_objects_as_dataframe(
        osm_model)
    all_default_subsurface_constructions_df = get_all_default_subsurface_construction_objects_as_dataframe(
        osm_model)

    # Define required dictionaries
    ext_surf_constr_dict = {'Exterior Surface Construction Walls': 'Wall Construction Name',
                            'Exterior Surface Construction Floors': 'Floor Construction Name',
                            'Exterior Surface Construction Roofs': 'Roof Ceiling Construction Name'
                            }
    int_surf_constr_dict = {
        'Interior Surface Construction Walls': 'Wall Construction Name',
        'Interior Surface Construction Floors': 'Floor Construction Name',
        'Interior Surface Construction Ceilings': 'Roof Ceiling Construction Name'
    }
    ground_surf_constr_dict = {
        'Ground Contact Surface Construction Walls': 'Wall Construction Name',
        'Ground Contact Surface Construction Floors': 'Floor Construction Name',
        'Ground Contact Surface Construction Ceilings': 'Roof Ceiling Construction Name'
    }
    ext_subsurf_constr_dict = {
        'Exterior SubSurface Construction Fixed Windows': 'Fixed Window Construction Name',
        'Exterior SubSurface Construction Operable Windows': 'Operable Window Construction Name',
        'Exterior SubSurface Construction Doors': 'Door Construction Name',
        'Exterior SubSurface Construction Glass Doors': 'Glass Door Construction Name',
        'Exterior SubSurface Construction Overhead Doors': 'Overhead Door Construction Name',
        'Exterior SubSurface Construction Skylights': 'Skylight Construction Name',
        'Exterior SubSurface Construction Tubular Daylight Domes': 'Tubular Daylight Dome Construction Name',
        'Exterior SubSurface Construction Tubular Daylight Diffusers': 'Tubular Daylight Diffuser Construction Name'
    }

    int_subsurf_constr_dict = {
        'Interior SubSurface Construction Fixed Windows': 'Fixed Window Construction Name',
        'Interior SubSurface Construction Operable Windows': 'Operable Window Construction Name',
        'Interior SubSurface Construction Doors': 'Door Construction Name'
    }

    all_default_construction_sets_components_df = all_default_construction_sets_df[[
        'Handle', 'Name']].copy()
    # Default Exterior Surface Constructions
    for index, row in all_default_construction_sets_components_df.iterrows():
        for key, value in ext_surf_constr_dict.items():
            name = all_default_construction_sets_df.loc[index,
                                                        'Default Exterior Surface Constructions Name']
            all_default_construction_sets_components_df.loc[index, key] = all_default_surface_constructions_df.loc[
                all_default_surface_constructions_df['Name'] == name, value].values[0]
    # Default Interior Surface Constructions
    for index, row in all_default_construction_sets_components_df.iterrows():
        for key, value in int_surf_constr_dict.items():
            name = all_default_construction_sets_df.loc[index,
                                                        'Default Interior Surface Constructions Name']
            all_default_construction_sets_components_df.loc[index, key] = all_default_surface_constructions_df.loc[
                all_default_surface_constructions_df['Name'] == name, value].values[0]

    # Default Ground Contact Surface Constructions
    for index, row in all_default_construction_sets_components_df.iterrows():
        for key, value in ground_surf_constr_dict.items():
            name = all_default_construction_sets_df.loc[index,
                                                        'Default Ground Contact Surface Constructions Name']
            all_default_construction_sets_components_df.loc[index, key] = all_default_surface_constructions_df.loc[
                all_default_surface_constructions_df['Name'] == name, value].values[0]

    # Default Exterior SubSurface Constructions Name
    for index, row in all_default_construction_sets_components_df.iterrows():
        for key, value in ext_subsurf_constr_dict.items():
            name = all_default_construction_sets_df.loc[index,
                                                        'Default Exterior SubSurface Constructions Name']
            all_default_construction_sets_components_df.loc[index, key] = all_default_subsurface_constructions_df.loc[
                all_default_subsurface_constructions_df['Name'] == name, value].values[0]

    # Default Interior SubSurface Constructions Name
    for index, row in all_default_construction_sets_components_df.iterrows():
        for key, value in int_subsurf_constr_dict.items():
            name = all_default_construction_sets_df.loc[index,
                                                        'Default Interior SubSurface Constructions Name']
            all_default_construction_sets_components_df.loc[index, key] = all_default_subsurface_constructions_df.loc[
                all_default_subsurface_constructions_df['Name'] == name, value].values[0]

    # Other Constructions
    cols = ['Space Shading Construction Name', 'Building Shading Construction Name',
            'Site Shading Construction Name', 'Interior Partition Construction Name', 'Adiabatic Surface Construction Name']
    all_default_construction_sets_components_df[cols] = all_default_construction_sets_df[cols].copy(
    )
    return all_default_construction_sets_components_df
