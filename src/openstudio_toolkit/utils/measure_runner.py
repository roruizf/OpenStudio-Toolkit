import os
import json
import tempfile
import subprocess
import shutil
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List

# Configure logger
logger = logging.getLogger(__name__)

class MeasureRunner:
    """
    Helper class for executing OpenStudio measures via the Command Line Interface (CLI).

    This class handles the creation of temporary execution environments, OSW (OpenStudio Workflow) 
    generation, subprocess management, and result extraction.
    """

    def __init__(self, openstudio_cli_path: Optional[str] = None):
        """
        Initialize the MeasureRunner with an optional path to the OpenStudio CLI.

        Parameters:
        - openstudio_cli_path (str, optional): Absolute path to the OpenStudio CLI executable. 
                                               If None, 'openstudio' must be in the system PATH.
        """
        self.openstudio_cli_path = openstudio_cli_path or "openstudio"

    def verify_measure_content(self, measure_dir: str) -> bool:
        """
        Check if a directory contains a valid OpenStudio measure (indicated by measure.xml).

        Parameters:
        - measure_dir (str): Path to the directory to verify.

        Returns:
        - bool: True if the directory is a valid measure, False otherwise.
        """
        measure_xml_path = Path(measure_dir) / "measure.xml"
        return measure_xml_path.exists() and measure_xml_path.is_file()

    def run(
        self,
        model_path: str,
        measure_dir: str,
        arguments: Dict[str, Any],
        output_path: Optional[str] = None,
        run_simulation: bool = False,
        extra_output_files: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Execute an OpenStudio measure on a specified model.

        Parameters:
        - model_path (str): Path to the input .osm file.
        - measure_dir (str): Path to the measure directory to apply.
        - arguments (Dict[str, Any]): Dictionary of arguments for the measure.
        - output_path (str, optional): Path where the resulting .osm file should be saved.
        - run_simulation (bool): If True, runs the full simulation. If False, runs only the measures.
        - extra_output_files (List[str], optional): Paths (relative to run dir) of extra files to retrieve.

        Returns:
        - Dict[str, Any]: Result dictionary containing 'osm_path' and 'extra_files'.

        Raises:
        - ValueError: If the measure directory is invalid.
        - RuntimeError: If the OpenStudio CLI execution fails.
        """
        if not self.verify_measure_content(measure_dir):
            raise ValueError(f"Invalid measure directory: {measure_dir}")

        logger.info(f"Running measure '{Path(measure_dir).name}' on {model_path}")

        # Create temporary directory for workflow execution
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Stage input OSM
            input_osm = temp_path / "input.osm"
            shutil.copy2(model_path, input_osm)

            # Stage measure (copy to temp to avoid permission/path issues in site-packages)
            local_measures_dir = temp_path / "measures"
            local_measures_dir.mkdir(exist_ok=True)
            measure_name = Path(measure_dir).name
            local_measure_dir = local_measures_dir / measure_name
            shutil.copytree(measure_dir, local_measure_dir)

            # Generate OSW workflow file
            osw_content = self._generate_osw(str(input_osm), str(local_measure_dir), arguments)
            osw_path = temp_path / "workflow.osw"
            with open(osw_path, 'w') as f:
                json.dump(osw_content, f, indent=2)

            # Construct CLI command
            cmd = [self.openstudio_cli_path, "run"]
            if not run_simulation:
                cmd.append("--measures_only")
            cmd.extend(["-w", str(osw_path)])

            # Execute subprocess
            logger.debug(f"Executing CLI command: {' '.join(cmd)}")
            result = subprocess.run(cmd, cwd=temp_dir, capture_output=True, text=True)

            if result.returncode != 0:
                logger.error(f"OpenStudio CLI failed with return code {result.returncode}")
                logger.error(f"STDOUT: {result.stdout}")
                logger.error(f"STDERR: {result.stderr}")
                raise RuntimeError(f"Measure execution failed. See logs for details.")

            # Finalize output OSM path
            final_output_path = output_path or tempfile.mktemp(suffix='.osm')

            # Retrieve result model
            run_output_osm = temp_path / "run" / "in.osm"
            source_output = str(run_output_osm) if run_output_osm.exists() else str(input_osm)

            shutil.copy2(source_output, final_output_path)
            logger.info(f"Measure completed. Result saved to {final_output_path}")

            # Collect extra output files if requested
            result_summary = {"osm_path": final_output_path}
            if extra_output_files:
                extra_files_dict = {}
                for file_pattern in extra_output_files:
                    found_file = self._find_file_in_temp(temp_path, file_pattern)
                    if found_file:
                        persistent_path = tempfile.mktemp(suffix=Path(file_pattern).suffix)
                        shutil.copy2(found_file, persistent_path)
                        extra_files_dict[file_pattern] = persistent_path
                result_summary["extra_files"] = extra_files_dict

            return result_summary

    def _find_file_in_temp(self, temp_path: Path, file_pattern: str) -> Optional[Path]:
        """
        Search for a specific file within the temporary run directory.

        Parameters:
        - temp_path (Path): Root path of the temporary directory.
        - file_pattern (str): Relative path or filename pattern to search for.

        Returns:
        - Optional[Path]: Path to the found file, or None if not located.
        """
        exact_path = temp_path / file_pattern
        if exact_path.exists():
            return exact_path

        filename = Path(file_pattern).name
        for found_file in temp_path.rglob(filename):
            return found_file

        return None

    def _generate_osw(self, osm_path: str, measure_dir: str, measure_args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate the content for an OSW (OpenStudio Workflow) JSON file.

        Parameters:
        - osm_path (str): Path to the seed OSM.
        - measure_dir (str): Path to the measure.
        - measure_args (Dict[str, Any]): Measure arguments.

        Returns:
        - Dict[str, Any]: Dictionary representing the OSW structure.
        """
        measure_name = Path(measure_dir).name
        return {
            "seed_file": osm_path,
            "weather_file": "",
            "steps": [
                {
                    "measure_dir_name": measure_name,
                    "arguments": measure_args
                }
            ],
            "file_paths": [str(Path(measure_dir).parent.absolute())]
        }
