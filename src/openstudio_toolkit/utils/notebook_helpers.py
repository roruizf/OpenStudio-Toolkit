import os
import logging
from typing import Tuple, Optional

# Configure logger
logger = logging.getLogger(__name__)

def get_osm_path(
    use_gdrive: bool,
    gdrive_path: Optional[str] = None,
    local_path: Optional[str] = None
) -> Tuple[str, str]:
    """
    Coordinate file access for OpenStudio models in both Google Colab and local environments.

    Parameters:
    - use_gdrive (bool): If True and in Colab, mounts Google Drive to access files.
    - gdrive_path (str, optional): The full path to the .osm file within Google Drive.
    - local_path (str, optional): The full path to the .osm file on the local machine.

    Returns:
    - Tuple[str, str]: A tuple containing (absolute_path_to_osm, absolute_path_to_directory).

    Raises:
    - ValueError: If necessary paths are missing for the detected environment.
    - FileNotFoundError: If the specified file cannot be located.
    """
    try:
        from google.colab import drive, files
        in_colab = True
    except ImportError:
        in_colab = False

    if not in_colab:
        # --- Local Environment ---
        logger.info("Running in a local environment.")
        if not local_path:
            raise ValueError("The 'local_path' must be provided when running in a local environment.")
        
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"OSM file not found at local path: {local_path}")
        
        osm_file_path = os.path.abspath(local_path)
        project_folder_path = os.path.dirname(osm_file_path)
    else:
        # --- Google Colab Environment ---
        if use_gdrive:
            if not gdrive_path:
                raise ValueError("The 'gdrive_path' is required when 'use_gdrive' is True.")
            
            logger.info("Mounting Google Drive for file access...")
            drive.mount('/content/drive', force_remount=True)
            
            if not os.path.exists(gdrive_path):
                raise FileNotFoundError(f"OSM file not found in Google Drive: {gdrive_path}")
                
            osm_file_path = gdrive_path
            project_folder_path = os.path.dirname(gdrive_path)
        else:
            logger.info("Requesting file upload in Colab...")
            project_folder_path = '/content'
            uploaded = files.upload()
            
            if not uploaded:
                raise FileNotFoundError("File upload was cancelled or failed.")
                
            file_name = next(iter(uploaded))
            osm_file_path = os.path.join(project_folder_path, file_name)

    logger.info(f"Model path resolved: {osm_file_path}")
    return osm_file_path, project_folder_path