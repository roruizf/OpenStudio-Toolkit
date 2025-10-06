# src/openstudio_toolkit/tasks/model_setup/rename_surfaces_based_on_space_names.py

import openstudio
import pandas as pd
from typing import Dict, List
from openstudio_toolkit.osm_objects import surfaces

def _generate_new_surface_names(df: pd.DataFrame) -> pd.Series:
    """Sub-task: Generates the base names for surfaces."""
    
    # Create a map of surface names to their parent space names
    surface_to_space_map = df.set_index('Surface Name')['Space Name'].to_dict()

    # Case 1: Boundary condition is an object (adjacent surface)
    mask_adjacent = df['Outside Boundary Condition Object'].notnull()
    df.loc[mask_adjacent, 'New Surface Name'] = (
        df['Space Name'] + "_" +
        df['Surface Type'] + "_" +
        df['Outside Boundary Condition Object'].map(surface_to_space_map)
    )

    # Case 2: Boundary condition is a simple type (e.g., Outdoors)
    mask_simple = df['Outside Boundary Condition Object'].isnull()
    df.loc[mask_simple, 'New Surface Name'] = (
        df['Space Name'] + "_" +
        df['Surface Type'] + "_" +
        df['Outside Boundary Condition']
    )
    
    return df['New Surface Name']

def _deduplicate_names(names: pd.Series) -> pd.Series:
    """Sub-task: Appends suffixes to duplicate names to make them unique."""
    counts = {}
    new_names = []
    for name in names:
        if name in counts:
            counts[name] += 1
            new_names.append(f"{name}_{counts[name]}")
        else:
            counts[name] = 1
            new_names.append(f"{name}_1")
    return pd.Series(new_names, index=names.index)

# --- Main Task Functions ---

def validator(osm_model: openstudio.model.Model) -> Dict[str, List[str]]:
    """Validates that the model has surfaces to be renamed."""
    if len(osm_model.getSurfaces()) == 0:
        return {"status": "ERROR", "messages": ["ERROR: Model contains no surfaces to rename."]}
    
    messages = [f"OK: Found {len(osm_model.getSurfaces())} surfaces to process."]
    # Add a 'SKIP' check here in the future if desired
    return {"status": "READY", "messages": messages}

def run(osm_model: openstudio.model.Model) -> openstudio.model.Model:
    """Renames all surfaces based on their space and boundary condition."""
    print("INFO: Starting rename surfaces task...")
    
    # Step 1: Data Collection & Enrichment
    # -------------------------------------
    # Get all surface objects from the model and load them into a pandas DataFrame.
    surfaces_df = surfaces.get_all_surface_objects_as_dataframe(osm_model)
    
    # Create a dictionary mapping each surface's handle to its gross area.
    # This is done once for efficiency instead of querying the model for each row.
    gross_area_map = {
        str(surface.handle()): surface.grossArea() 
        for surface in osm_model.getSurfaces()
    }
    # Add the gross area as a new column to the DataFrame.
    surfaces_df['Gross Area {m2}'] = surfaces_df['Handle'].map(gross_area_map)

    # Create a similar map for the azimuth of each surface.
    azimuth_map = {
        str(surface.handle()): surface.azimuth() 
        for surface in osm_model.getSurfaces()
    }
    # Add the azimuth as a new column.
    surfaces_df['Azimuth'] = surfaces_df['Handle'].map(azimuth_map)

    # Step 2: Sorting for Deterministic Naming
    # ----------------------------------------
    # Sort the DataFrame by multiple criteria. This is a critical step to ensure
    # that the naming convention is consistent and repeatable every time the task is run.
    # Area and Azimuth are sorted in descending order to handle larger surfaces first.
    surfaces_df = surfaces_df.sort_values(
        by=['Space Name', 'Surface Type', 'Outside Boundary Condition', 'Sun Exposure', 'Wind Exposure', 'Gross Area {m2}', 'Azimuth'],
        ascending=[True, True, True, True, True, False, False]
    ).reset_index(drop=True)
    
    # Rename default columns for clarity.
    surfaces_df = surfaces_df.rename(columns={'Handle': 'Surface Handle', 'Name': 'Surface Name'})

    # Step 3: Generate New Names
    # --------------------------
    # Generate a list of new, descriptive names based on the sorted data.
    # These initial names may contain duplicates (e.g., multiple identical windows).
    base_names = _generate_new_surface_names(surfaces_df)
    
    # Process the base names to ensure every name is unique by appending a suffix if needed.
    final_names = _deduplicate_names(base_names)
    
    # Add the final, unique names as a new column to the DataFrame.
    surfaces_df['New Surface Name'] = final_names

    # Step 4: Apply Changes to the OpenStudio Model
    # ---------------------------------------------
    # Iterate through the DataFrame and update each surface in the actual model.
    for index, row in surfaces_df.iterrows():
        # Get the surface object from the model using its handle.
        surface = osm_model.getSurface(row['Surface Handle']).get()
        new_name = row['New Surface Name']
        
        # Only apply the change if the new name is different from the old one.
        if surface.nameString() != new_name:
            surface.setName(new_name)
            
    print("INFO: Rename surfaces task finished successfully.")
    return osm_model