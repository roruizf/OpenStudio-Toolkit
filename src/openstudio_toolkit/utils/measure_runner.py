import os
import json
import tempfile
import subprocess
import shutil
from pathlib import Path
from typing import Dict, Any, Optional


class MeasureRunner:
    """
    Helper class for running OpenStudio measures via CLI.

    Handles temporary directories, OSW file generation, and subprocess execution.
    """

    def __init__(self, openstudio_cli_path: Optional[str] = None):
        """
        Initialize the MeasureRunner.

        Args:
            openstudio_cli_path: Path to openstudio CLI executable. If None, assumes 'openstudio' is in PATH.
        """
        self.openstudio_cli_path = openstudio_cli_path or "openstudio"

    def verify_measure_content(self, measure_dir: str) -> bool:
        """
        Verify that a measure directory contains valid measure content.

        Args:
            measure_dir: Path to the measure directory.

        Returns:
            True if measure.xml exists, False otherwise.
        """
        measure_xml_path = Path(measure_dir) / "measure.xml"
        return measure_xml_path.exists() and measure_xml_path.is_file()

    def run(
        self,
        model_path: str,
        measure_dir: str,
        arguments: Dict[str, Any],
        output_path: Optional[str] = None,
        run_simulation: bool = False
    ) -> Dict[str, Any]:
        """
        Executes the measure workflow.
        CRITICAL: If run_simulation is False, pass '--measures_only' to the CLI.

        Args:
            model_path: Path to input OSM file.
            measure_dir: Path to measure directory.
            arguments: Arguments to pass to the measure.
            output_path: Path for output OSM file. If None, uses a temporary file.
            run_simulation: Whether to run full simulation. If False, uses --measures_only.

        Returns:
            Dict containing 'osm_path' with the path to resulting OSM file.

        Raises:
            RuntimeError: If measure execution fails.
        """
        # Verify measure exists
        if not self.verify_measure_content(measure_dir):
            raise ValueError(f"Invalid measure directory: {measure_dir}")

        # Create temporary directory for workflow
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Copy input OSM to temp directory
            input_osm = temp_path / "input.osm"
            shutil.copy2(model_path, input_osm)

            # Copy measure to temp directory (OpenStudio may have issues accessing measures from site-packages)
            local_measures_dir = temp_path / "measures"
            local_measures_dir.mkdir(exist_ok=True)
            measure_name = Path(measure_dir).name
            local_measure_dir = local_measures_dir / measure_name
            shutil.copytree(measure_dir, local_measure_dir)

            # Generate OSW file with local measure path
            osw_content = self._generate_osw(
                str(input_osm), str(local_measure_dir), arguments)
            osw_path = temp_path / "workflow.osw"
            with open(osw_path, 'w') as f:
                json.dump(osw_content, f, indent=2)

            # Construct Command
            cmd = [self.openstudio_cli_path, "run"]

            if not run_simulation:
                cmd.append("--measures_only")  # <--- THIS IS CRITICAL

            cmd.extend(["-w", str(osw_path)])

            # Run OpenStudio CLI
            result = subprocess.run(
                cmd, cwd=temp_dir, capture_output=True, text=True)

            if result.returncode != 0:
                error_msg = f"Measure execution failed:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
                raise RuntimeError(error_msg)

            # Determine output path
            if output_path:
                final_output_path = output_path
            else:
                # Use a temporary file that will be copied later
                final_output_path = tempfile.mktemp(suffix='.osm')

            # OpenStudio CLI saves the resulting model in run/in.osm
            run_output_osm = temp_path / "run" / "in.osm"
            if run_output_osm.exists():
                source_output = str(run_output_osm)
            else:
                # Fall back to other possible locations
                output_osm = temp_path / "in.osm"
                if output_osm.exists():
                    source_output = str(output_osm)
                else:
                    source_output = str(input_osm)

            # Copy result to final location
            shutil.copy2(source_output, final_output_path)

            return {"osm_path": final_output_path}

    def _generate_osw(self, osm_path: str, measure_dir: str, measure_args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate OSW (OpenStudio Workflow) JSON content.

        Args:
            osm_path: Path to OSM file.
            measure_dir: Path to measure directory.
            measure_args: Measure arguments.

        Returns:
            OSW dictionary.
        """
        measure_name = Path(measure_dir).name

        osw = {
            "seed_file": osm_path,
            "weather_file": "",
            "steps": [
                {
                    "measure_dir_name": measure_name,
                    "arguments": measure_args
                }
            ],
            "file_paths": [
                # Parent directory containing the measure
                str(Path(measure_dir).parent.absolute())
            ]
        }

        return osw
