# src/openstudio_toolkit/utils/notebook_setup.py

import sys
import subprocess
import os
import shutil
from typing import Literal

def setup_environment(
    project_folder_path: str,
    openstudio_version: str = "3.7.0",
    install_cli: bool = False,
    toolkit_branch: Literal["main", "dev"] = "main"
):
    """
    Detects the environment (Colab vs. local), installs Python packages,
    and optionally installs the full OpenStudio CLI application in Colab.

    This function prepares a notebook for use with the openstudio-toolkit by
    handling all necessary installations and path configurations.

    Args:
        project_folder_path (str): The absolute path to the project's root folder.
        openstudio_version (str, optional): The version of the openstudio-py package to install.
                                           Defaults to "3.7.0".
        install_cli (bool, optional): If True, will attempt to install the full OpenStudio
                                      Application/CLI. This is required for running Measures
                                      and only works in Google Colab. Defaults to False.
        toolkit_branch (Literal["main", "dev"], optional): The specific GitHub branch of the
                                      openstudio-toolkit to install. Defaults to "main".
    """
    try:
        import google.colab
        IN_COLAB = True
    except ImportError:
        IN_COLAB = False

    print(f"--- Environment Setup ---")
    
    if IN_COLAB:
        print("INFO: Running in Google Colab.")
        
        # 1. Install Python Packages
        print(f"INFO: Installing openstudio-py=={openstudio_version}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", f"openstudio=={openstudio_version}"], stdout=subprocess.DEVNULL)
        
        print(f"INFO: Installing openstudio-toolkit from '{toolkit_branch}' branch...")
        toolkit_url = f"git+https://github.com/roruizf/OpenStudio-Toolkit.git@{toolkit_branch}"
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", toolkit_url], stdout=subprocess.DEVNULL)
        print("INFO: Python packages installed.")
        
        # 2. Install OpenStudio CLI if requested
        if install_cli:
            print("INFO: 'install_cli' is True. Checking for OpenStudio CLI...")
            if shutil.which('openstudio'):
                print("INFO: OpenStudio CLI is already installed.")
                subprocess.run(['openstudio', '--version'])
            else:
                print("INFO: OpenStudio CLI not found. Proceeding with installation...")
                # This logic is specific to the Ubuntu version used by Google Colab
                deb_file = f"OpenStudio-{openstudio_version}+d5269793f1-Ubuntu-22.04-x86_64.deb"
                download_url = f"https://github.com/NREL/OpenStudio/releases/download/v{openstudio_version}/{deb_file}"
                
                subprocess.run(['wget', '-q', '-O', deb_file, download_url])
                subprocess.run(['sudo', 'dpkg', '-i', deb_file])
                subprocess.run(['sudo', 'apt-get', 'install', '-f', '-y']) # Fix dependencies
                if os.path.exists(deb_file):
                    os.remove(deb_file)
                
                if shutil.which('openstudio'):
                    print("INFO: OpenStudio CLI installed successfully.")
                    subprocess.run(['openstudio', '--version'])
                else:
                    print("ERROR: OpenStudio CLI installation failed.")
    else:
        print("INFO: Running in a local environment. Assuming all dependencies are pre-installed.")

    # 3. Add project folder to Python path
    if project_folder_path not in sys.path:
        sys.path.append(project_folder_path)

    print("--- Environment Setup Complete ---")