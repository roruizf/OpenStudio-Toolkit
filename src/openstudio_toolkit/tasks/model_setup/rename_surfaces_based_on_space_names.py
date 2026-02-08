import logging
from typing import Any

import openstudio
import pandas as pd

from openstudio_toolkit.osm_objects import surfaces

# Configure logger
logger = logging.getLogger(__name__)

def _generate_new_surface_names(df: pd.DataFrame) -> pd.Series:
    """
    Generate the initial base names for surfaces based on parent space and boundary conditions.

    Parameters:
    - df (pd.DataFrame): Dataframe containing current surface information.

    Returns:
    - pd.Series: A series of generated 'New Surface Name' strings.
    """
    # Create a map of surface names to their parent space names
    surface_to_space_map = df.set_index('Surface Name')['Space Name'].to_dict()

    # Case 1: Boundary condition is an object (adjacent surface)
    mask_adjacent = df['Outside Boundary Condition Object'].notnull()
    df.loc[mask_adjacent, 'New Surface Name'] = (
        df['Space Name'] + "_" +
        df['Surface Type'] + "_" +
        df['Outside Boundary Condition Object'].map(surface_to_space_map)
    )

    # Case 2: Boundary condition is a simple type (e.g., Outdoors, Ground)
    mask_simple = df['Outside Boundary Condition Object'].isnull()
    df.loc[mask_simple, 'New Surface Name'] = (
        df['Space Name'] + "_" +
        df['Surface Type'] + "_" +
        df['Outside Boundary Condition']
    )
    
    return df['New Surface Name']

def _deduplicate_names(names: pd.Series) -> pd.Series:
    """
    Append incremental suffixes to duplicate names to ensure each name is unique.

    Parameters:
    - names (pd.Series): Series of proposed names.

    Returns:
    - pd.Series: Series of unique names with suffixes.
    """
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

def validator(osm_model: openstudio.model.Model) -> dict[str, Any]:
    """
    Validate that the model has surfaces to be renamed.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object to validate.

    Returns:
    - Dict[str, Any]: A dictionary containing the validation 'status' ('READY' or 'ERROR') and a list of 'messages'.
    """
    count = len(osm_model.getSurfaces())
    if count == 0:
        msg = "ERROR: Model contains no surfaces to rename."
        logger.error(msg)
        return {"status": "ERROR", "messages": [msg]}
    
    msg = f"OK: Found {count} surfaces to process."
    logger.info(msg)
    return {"status": "READY", "messages": [msg]}

def run(osm_model: openstudio.model.Model) -> openstudio.model.Model:
    """
    Rename all surfaces based on their parent space and outside boundary conditions.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object to process.

    Returns:
    - openstudio.model.Model: The updated OpenStudio Model object.
    """
    logger.info("Starting rename surfaces task...")
    
    surfaces_df = surfaces.get_all_surface_objects_as_dataframe(osm_model)
    if surfaces_df.empty:
        logger.info("No surfaces found to rename.")
        return osm_model
            
    surfaces_df = surfaces_df.rename(columns={'Handle': 'Surface Handle', 'Name': 'Surface Name'})

    # 1. Generate base names
    base_names = _generate_new_surface_names(surfaces_df)
    
    # 2. De-duplicate names
    final_names = _deduplicate_names(base_names)
    surfaces_df['New Surface Name'] = final_names

    # 3. Apply changes to the model
    rename_count = 0
    for _, row in surfaces_df.iterrows():
        surface_obj = osm_model.getSurface(openstudio.toUUID(row['Surface Handle']))
        if surface_obj.is_initialized():
            surface = surface_obj.get()
            new_name = row['New Surface Name']
            current_name = surface.name().get() if surface.name().is_initialized() else ""
            
            if current_name != new_name:
                surface.setName(new_name)
                rename_count += 1
            
    logger.info(f"Rename surfaces task finished successfully. {rename_count} surfaces renamed.")
    return osm_model