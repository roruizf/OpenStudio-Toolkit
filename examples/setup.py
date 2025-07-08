import os
import sys
import pandas as pd
from .osm_utils import load_osm_file_as_model

def init_env(use_gdrive, gdrive_path, local_path):
    """
    Initializes the environment for Colab or local execution.
    Returns a tuple containing the project path and a boolean indicating if running in Colab.
    """
    in_colab = 'google.colab' in sys.modules

    if in_colab:
        print("Running in Google Colab.")
        if use_gdrive:
            from google.colab import drive
            drive.mount('/content/drive', force_remount=True)
            print(f"Google Drive mounted. Project path: {gdrive_path}")
            return gdrive_path, True
        else:
            print("Using temporary Colab folder: /content")
            return "/content", True
    else:
        print(f"Running in local environment. Project path: {local_path}")
        return local_path, False

def load_data_file(file_path, in_colab, use_gdrive):
    """
    Loads a data file (e.g., .osm, .xlsx), handling Colab uploads if needed.
    If the file is an .osm, it returns a model object.
    If it's an .xlsx, it returns a pandas DataFrame.
    """
    if not os.path.exists(file_path):
        if in_colab and not use_gdrive:
            print(f"File not found at {file_path}. Please upload the file.")
            from google.colab import files
            uploaded = files.upload()
            if not uploaded:
                print("No file uploaded. Aborting.")
                return None
            file_name = list(uploaded.keys())[0]
            file_path = os.path.join('/content', file_name)
        else:
            print(f"Error: File not found at {file_path}")
            return None

    print(f"Loading data from: {file_path}")
    
    _, file_extension = os.path.splitext(file_path)

    if file_extension.lower() == '.osm':
        return load_osm_file_as_model(file_path)
    elif file_extension.lower() == '.xlsx':
        return pd.read_excel(file_path)
    else:
        print(f"Unsupported file type: {file_extension}. Please load manually.")
        return None
