import logging
from typing import Any

import openstudio
import pandas as pd

from openstudio_toolkit.osm_objects import subsurfaces, surfaces

# Configure logger
logger = logging.getLogger(__name__)

def validator(osm_model: openstudio.model.Model) -> dict[str, Any]:
    """
    Diagnose if the model possesses the necessary geometry components (surfaces/walls) to calculate WWR.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object to validate.

    Returns:
    - Dict[str, Any]: A dictionary containing the validation 'status' ('READY' or 'ERROR') and a list of 'messages'.
    """
    messages = []
    
    # Get all surfaces
    surface_df = surfaces.get_all_surface_objects_as_dataframe(osm_model)
    
    if surface_df.empty:
        msg = "ERROR: Model does not contain any surfaces."
        logger.error(msg)
        messages.append(msg)
        return {"status": "ERROR", "messages": messages}

    # Filter for outdoor-facing walls
    walls_df = surface_df[
        (surface_df['Surface Type'] == 'Wall') & 
        (surface_df['Outside Boundary Condition'] == 'Outdoors')
    ]

    if walls_df.empty:
        msg = "ERROR: Model contains no outdoor-facing 'Wall' surfaces."
        logger.error(msg)
        messages.append(msg)
        return {"status": "ERROR", "messages": messages}

    msg = f"OK: Found {len(walls_df)} outdoor-facing walls."
    logger.info(msg)
    messages.append(msg)
    return {"status": "READY", "messages": messages}

def run(osm_model: openstudio.model.Model) -> pd.DataFrame:
    """
    Calculate the Window-to-Wall Ratio (WWR) for each space in the model.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object to process.

    Returns:
    - pd.DataFrame: A DataFrame with WWR calculations per space, including gross wall area and gross window area.
    """
    logger.info("Starting WWR calculation task...")

    # Fetch geometry dataframes
    all_surfaces_df = surfaces.get_all_surface_objects_as_dataframe(osm_model)
    all_subsurfaces_df = subsurfaces.get_all_subsurface_objects_as_dataframe(osm_model)

    if all_surfaces_df.empty:
        logger.warning("No surfaces found in model. Returning empty DataFrame.")
        return pd.DataFrame()

    # Add gross area to surfaces
    all_surfaces_df['Surface Gross Area'] = all_surfaces_df['Handle'].apply(
        lambda h: osm_model.getSurface(openstudio.toUUID(h)).get().grossArea() if osm_model.getSurface(openstudio.toUUID(h)).is_initialized() else 0.0
    )

    # Add gross area to subsurfaces
    if not all_subsurfaces_df.empty:
        all_subsurfaces_df['Sub Surface Gross Area'] = all_subsurfaces_df['Handle'].apply(
            lambda h: osm_model.getSubSurface(openstudio.toUUID(h)).get().grossArea() if osm_model.getSubSurface(openstudio.toUUID(h)).is_initialized() else 0.0
        )
        
        # Map subsurfaces to space names via their parent surfaces
        # We assume surfaces dataframe already contains 'Space Name' and 'Name'
        surface_to_space_map = all_surfaces_df.set_index('Name')['Space Name'].to_dict()
        all_subsurfaces_df['Space Name'] = all_subsurfaces_df['Surface Name'].map(surface_to_space_map)
    else:
        all_subsurfaces_df = pd.DataFrame(columns=['Space Name', 'Sub Surface Gross Area', 'Sub Surface Type'])

    # Filter for outdoor walls
    walls_df = all_surfaces_df[
        (all_surfaces_df['Surface Type'] == 'Wall') & 
        (all_surfaces_df['Outside Boundary Condition'] == 'Outdoors')
    ]
    
    if walls_df.empty:
        logger.warning("No outdoor-facing walls found. WWR cannot be calculated.")
        return pd.DataFrame()

    walls_by_space = walls_df.groupby('Space Name')['Surface Gross Area'].sum().reset_index()

    # Filter for windows/glass doors
    window_types = ('FixedWindow', 'OperableWindow', 'GlassDoor')
    windows_df = all_subsurfaces_df[all_subsurfaces_df['Sub Surface Type'].isin(window_types)]
    
    if not windows_df.empty:
        windows_by_space = windows_df.groupby('Space Name')['Sub Surface Gross Area'].sum().reset_index()
    else:
        windows_by_space = pd.DataFrame(columns=['Space Name', 'Sub Surface Gross Area'])

    # Merge and calculate WWR
    wwr_df = pd.merge(walls_by_space, windows_by_space, on='Space Name', how='left').fillna(0)
    wwr_df['WWR'] = (wwr_df['Sub Surface Gross Area'] / wwr_df['Surface Gross Area']).where(wwr_df['Surface Gross Area'] > 0, 0)

    logger.info("WWR calculation task finished successfully.")
    return wwr_df
