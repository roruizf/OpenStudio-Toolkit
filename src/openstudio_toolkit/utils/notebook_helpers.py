"""
Notebook helper utilities for local/WSL2 development.

This module provides utilities for resolving file paths in Jupyter notebooks,
replacing the legacy Colab-specific logic with robust local file handling.
"""

import logging
from pathlib import Path
from typing import Tuple

# Configure logger
logger = logging.getLogger(__name__)


def get_osm_path(
    use_gdrive: bool = False,  # Deprecated, kept for backward compatibility
    gdrive_path: str | None = None,  # Deprecated
    local_path: str | None = None,
) -> Tuple[str, str]:
    """
    Resolve file path for OpenStudio models in local/WSL2 environments.

    This function replaces the legacy Colab-specific logic with robust local
    file path resolution using pathlib. It supports both absolute and relative
    paths, resolving them correctly from the notebook's execution context.

    Parameters
    ----------
    use_gdrive : bool, optional
        Deprecated parameter kept for backward compatibility. Ignored in WSL2.
    gdrive_path : str, optional
        Deprecated parameter kept for backward compatibility. Ignored in WSL2.
    local_path : str, optional
        Path to the .osm file. Can be absolute or relative to notebook location.
        If relative, it will be resolved from the current working directory.

    Returns
    -------
    Tuple[str, str]
        A tuple containing:
        - absolute_path_to_osm (str): Resolved absolute path to the .osm file
        - absolute_path_to_directory (str): Resolved absolute path to parent directory

    Raises
    ------
    ValueError
        If local_path is not provided or is empty.
    FileNotFoundError
        If the specified file does not exist at the resolved path.

    Examples
    --------
    >>> # From a notebook in notebooks/1_Model_Setup/
    >>> osm_path, project_dir = get_osm_path(local_path='../../examples/model.osm')
    >>> # Returns absolute paths to model.osm and examples/ directory

    >>> # Using absolute path
    >>> osm_path, project_dir = get_osm_path(
    ...     local_path='/mnt/g/My Drive/R2F-EES/Development/project/model.osm'
    ... )

    Notes
    -----
    - This function is designed for local/WSL2 development only
    - Google Colab parameters (use_gdrive, gdrive_path) are ignored
    - Relative paths are resolved from the current working directory (os.getcwd())
    - All returned paths are absolute strings for compatibility with OpenStudio SDK
    """
    # Validate input
    if not local_path:
        raise ValueError(
            "The 'local_path' parameter is required for local/WSL2 development. "
            "Provide either an absolute path or a path relative to the notebook location."
        )

    # Resolve path using pathlib
    osm_path = Path(local_path)

    # If relative, resolve from current working directory
    if not osm_path.is_absolute():
        osm_path = Path.cwd() / osm_path

    # Resolve to absolute path (handles .. and . components)
    osm_path = osm_path.resolve()

    # Verify file exists
    if not osm_path.exists():
        raise FileNotFoundError(
            f"OSM file not found at resolved path: {osm_path}\n"
            f"Original input: {local_path}\n"
            f"Current working directory: {Path.cwd()}"
        )

    # Verify it's a file, not a directory
    if not osm_path.is_file():
        raise ValueError(f"Path exists but is not a file: {osm_path}")

    # Get parent directory
    project_folder = osm_path.parent

    logger.info(f"Model path resolved: {osm_path}")
    logger.info(f"Project folder: {project_folder}")

    # Return as strings for compatibility with OpenStudio SDK
    return str(osm_path), str(project_folder)


def resolve_output_path(
    input_osm_path: str,
    output_suffix: str = "_modified",
    output_dir: str | None = None,
) -> str:
    """
    Generate output file path for modified OSM models.

    Parameters
    ----------
    input_osm_path : str
        Path to the input .osm file (from get_osm_path).
    output_suffix : str, optional
        Suffix to append to the filename before extension. Default: "_modified"
    output_dir : str, optional
        Directory for output file. If None, uses current working directory.

    Returns
    -------
    str
        Absolute path to the output file.

    Examples
    --------
    >>> input_path = '/path/to/model.osm'
    >>> output_path = resolve_output_path(input_path, suffix='_normalized')
    >>> # Returns: '/current/dir/model_normalized.osm'
    """
    input_path = Path(input_osm_path)
    stem = input_path.stem  # Filename without extension
    extension = input_path.suffix  # .osm

    # Construct output filename
    output_filename = f"{stem}{output_suffix}{extension}"

    # Determine output directory
    if output_dir:
        output_path = Path(output_dir) / output_filename
    else:
        output_path = Path.cwd() / output_filename

    # Resolve to absolute path
    output_path = output_path.resolve()

    logger.info(f"Output path resolved: {output_path}")

    return str(output_path)
