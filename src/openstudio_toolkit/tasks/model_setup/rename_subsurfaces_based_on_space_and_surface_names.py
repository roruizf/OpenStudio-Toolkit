import logging
from typing import Any

import openstudio
import pandas as pd

from openstudio_toolkit.osm_objects import subsurfaces, surfaces

# Configure logger
logger = logging.getLogger(__name__)

def _get_and_prepare_dataframes(osm_model: openstudio.model.Model) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Extract and prepare the initial dataframes for surfaces and subsurfaces from the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.

    Returns:
    - Tuple[pd.DataFrame, pd.DataFrame]: A tuple containing (subsurfaces_df, surfaces_df).
    """
    # Prepare Subsurfaces DataFrame
    subsurfaces_df = subsurfaces.get_all_subsurface_objects_as_dataframe(osm_model)
    if not subsurfaces_df.empty:
        subsurfaces_df = subsurfaces_df.rename(columns={'Handle': 'Sub Surface Handle', 'Name': 'Sub Surface Name'})
        subsurfaces_df = subsurfaces_df.sort_values(by='Sub Surface Handle', ascending=True).reset_index(drop=True)
    else:
        subsurfaces_df = pd.DataFrame(columns=['Sub Surface Handle', 'Sub Surface Name', 'Surface Name', 'Sub Surface Type'])

    # Prepare Surfaces DataFrame
    surfaces_df = surfaces.get_all_surface_objects_as_dataframe(osm_model)
    if not surfaces_df.empty:
        surfaces_df = surfaces_df.rename(columns={'Handle': 'Surface Handle', 'Name': 'Surface Name'})
        surfaces_df = surfaces_df.sort_values(by='Surface Name', ascending=True).reset_index(drop=True)
    else:
        surfaces_df = pd.DataFrame(columns=['Surface Handle', 'Surface Name', 'Space Name'])

    return subsurfaces_df, surfaces_df

def _generate_and_deduplicate_names(subsurfaces_df: pd.DataFrame, surfaces_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge surface/subsurface data, generate new names based on parents, and ensure uniqueness.

    Parameters:
    - subsurfaces_df (pd.DataFrame): Prepared subsurfaces dataframe.
    - surfaces_df (pd.DataFrame): Prepared surfaces dataframe.

    Returns:
    - pd.DataFrame: Dataframe with generated and deduplicated 'New Sub Surface Name' column.
    """
    if subsurfaces_df.empty:
        return subsurfaces_df

    # Merge to link subsurfaces to their parent surface/space
    merged_df = pd.merge(subsurfaces_df, surfaces_df[['Surface Name', 'Space Name']], on='Surface Name', how='left')

    # Generate the new base name: SurfaceName_SubSurfaceType
    merged_df['New Sub Surface Name'] = merged_df['Surface Name'] + "_" + merged_df['Sub Surface Type']

    # --- De-duplication Logic ---
    # Separate unique and duplicate base names to process them
    duplicates_mask = merged_df.duplicated(subset=['New Sub Surface Name'], keep=False)
    unique_df = merged_df[~duplicates_mask]
    duplicate_df = merged_df[duplicates_mask]

    counter = {}
    
    # Process unique values to add a '_1' suffix
    for idx, row in unique_df.iterrows():
        base_name = row['New Sub Surface Name']
        new_name = f"{base_name}_1"
        merged_df.loc[idx, 'New Sub Surface Name'] = new_name
        counter[base_name] = 1

    # Process duplicate values to add incremental suffixes
    for idx, row in duplicate_df.iterrows():
        base_name = row['New Sub Surface Name']
        if base_name in counter:
            counter[base_name] += 1
        else:
            counter[base_name] = 1
        new_name = f"{base_name}_{counter[base_name]}"
        merged_df.loc[idx, 'New Sub Surface Name'] = new_name
        
    return merged_df

def _apply_names_to_model(osm_model: openstudio.model.Model, final_df: pd.DataFrame) -> None:
    """
    Apply the generated names back to the OpenStudio model objects.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - final_df (pd.DataFrame): Dataframe containing 'Sub Surface Handle' and 'New Sub Surface Name'.
    """
    if final_df.empty:
        return

    for _, row in final_df.iterrows():
        handle_str = row.get('Sub Surface Handle')
        if not handle_str:
            continue
            
        sub_obj = osm_model.getSubSurface(openstudio.toUUID(handle_str))
        if sub_obj.is_initialized():
            subsurface = sub_obj.get()
            new_name = row['New Sub Surface Name']
            current_name = subsurface.name().get() if subsurface.name().is_initialized() else ""
            
            if current_name != new_name:
                subsurface.setName(new_name)

def validator(osm_model: openstudio.model.Model) -> dict[str, Any]:
    """
    Validate that the model possesses subsurfaces to be renamed.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object to validate.

    Returns:
    - Dict[str, Any]: A dictionary containing the validation 'status' ('READY' or 'ERROR') and a list of 'messages'.
    """
    count = len(osm_model.getSubSurfaces())
    if count == 0:
        msg = "ERROR: Model contains no subsurfaces to rename."
        logger.error(msg)
        return {"status": "ERROR", "messages": [msg]}
    
    msg = f"OK: Found {count} subsurfaces to process."
    logger.info(msg)
    return {"status": "READY", "messages": [msg]}

def run(osm_model: openstudio.model.Model) -> openstudio.model.Model:
    """
    Rename all subsurfaces based on their parent surface and space names.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object to process.

    Returns:
    - openstudio.model.Model: The updated OpenStudio Model object.
    """
    logger.info("Starting rename subsurfaces task...")
    
    # 1. Prepare Data
    subsurfaces_df, surfaces_df = _get_and_prepare_dataframes(osm_model)
    
    if subsurfaces_df.empty:
        logger.info("No subsurfaces found to rename.")
        return osm_model

    # 2. Generate and De-duplicate Names
    final_df = _generate_and_deduplicate_names(subsurfaces_df, surfaces_df)
    
    # 3. Apply Names to Model
    _apply_names_to_model(osm_model, final_df)
            
    logger.info("Rename subsurfaces task finished successfully.")
    return osm_model