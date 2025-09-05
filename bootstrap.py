# bootstrap.py
import sys, subprocess, os, shutil, argparse

def setup_environment(
    openstudio_version: str = "3.7.0",
    install_cli: bool = False,
    toolkit_branch: str = "main"
):
    try:
        import google.colab
        IN_COLAB = True
    except ImportError:
        IN_COLAB = False

    if not IN_COLAB:
        print("--- INFO: Running in Local Environment. Skipping setup. ---")
        return

    print("--- Setting up Google Colab Environment ---")

    # 1. Install Python Packages
    print(f"INFO: Installing openstudio-py=={openstudio_version}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", f"openstudio=={openstudio_version}"], stdout=subprocess.DEVNULL)

    print(f"INFO: Installing openstudio-toolkit from '{toolkit_branch}' branch...")
    toolkit_url = f"git+https://github.com/roruizf/OpenStudio-Toolkit.git@{toolkit_branch}"
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", toolkit_url], stdout=subprocess.DEVNULL)
    print("INFO: Python packages installed.")

    # 2. Install OpenStudio CLI if requested
    if install_cli:
        # ... (Lógica completa de instalación de la CLI) ...
        pass

    print("\n--- Environment is ready ---")
    print("💥 IMPORTANT: You may need to restart the kernel for the changes to take effect ('Runtime' > 'Restart session').")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Setup environment for OpenStudio Toolkit notebooks.")
    parser.add_argument('--install-cli', action='store_true', help="Install the full OpenStudio CLI.")
    parser.add_argument('--branch', type=str, default='main', help="Specify the toolkit branch to install.")
    args = parser.parse_args()
    setup_environment(install_cli=args.install_cli, toolkit_branch=args.branch)