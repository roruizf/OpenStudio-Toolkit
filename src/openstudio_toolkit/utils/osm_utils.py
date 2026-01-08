import os
import logging
import openstudio
from typing import Optional

# Configure logger
logger = logging.getLogger(__name__)

def load_osm_file_as_model(osm_file_path: str, version_translator: Optional[bool] = True) -> openstudio.model.Model:
    """
    Load an OpenStudio Model (.osm) file from a specified path.

    Parameters:
    - osm_file_path (str): Absolute or relative path to the .osm file.
    - version_translator (bool, optional): If True, uses the VersionTranslator to handle version differences. 
                                           Defaults to True.

    Returns:
    - openstudio.model.Model: The loaded OpenStudio Model object.

    Raises:
    - RuntimeError: If the model fails to load or is uninitialized.
    """
    abs_path = os.path.abspath(osm_file_path)
    
    if version_translator:
        translator = openstudio.osversion.VersionTranslator()
        loaded_model = translator.loadModel(abs_path)
    else:
        loaded_model = openstudio.model.Model.load(abs_path)

    if loaded_model.is_initialized():
        osm_model = loaded_model.get()
        # Log building name if available
        building_name = osm_model.building().get().name().get() if osm_model.building().is_initialized() else "Unnamed Building"
        logger.info(f"Loaded OSM model for building: {building_name}")
        return osm_model
    else:
        err_msg = f"Failed to load OpenStudio model from path: {abs_path}"
        logger.error(err_msg)
        raise RuntimeError(err_msg)

def save_model_as_osm_file(osm_model: openstudio.model.Model, osm_file_path: str, new_file_name: Optional[str] = None) -> None:
    """
    Save an OpenStudio Model object to a file.

    Parameters:
    - osm_model (openstudio.model.Model): The model object to save.
    - osm_file_path (str): The destination directory path or full file path.
    - new_file_name (str, optional): Overriding name for the saved file.

    Returns:
    - None
    """
    # Extract folder and filename
    osm_file_folder = os.path.dirname(os.path.abspath(osm_file_path))
    
    if new_file_name is not None:
        target_name = new_file_name
    else:
        target_name = os.path.basename(osm_file_path)

    save_path = os.path.join(osm_file_folder, target_name)
    osm_model.save(save_path, overwrite=True)
    logger.info(f"Model saved as OSM at: {save_path}")

def convert_osm_to_idf(osm_model: openstudio.model.Model, idf_file_path: str) -> None:
    """
    Convert an OpenStudio Model to an EnergyPlus IDF file using the ForwardTranslator.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model to convert.
    - idf_file_path (str): The path where the generated IDF will be saved.

    Returns:
    - None
    """
    ft = openstudio.energyplus.ForwardTranslator()
    idf_model = ft.translateModel(osm_model)

    save_path = os.path.abspath(idf_file_path)
    idf_model.save(save_path, True)
    logger.info(f"IDF file successfully generated at: {save_path}")
