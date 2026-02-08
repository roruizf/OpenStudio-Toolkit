import logging
from typing import Any

import openstudio

# Configure logger
logger = logging.getLogger(__name__)

def validate_args(handle: str | None, name: str | None) -> None:
    """
    Validate that exactly one identifier ('handle' or 'name') is provided.

    Parameters:
    - handle (Optional[str]): The unique handle of the object.
    - name (Optional[str]): The name of the object.

    Raises:
    - ValueError: If both or neither identifiers are provided.
    """
    if handle is not None and name is not None:
        raise ValueError("Only one of 'handle' or 'name' should be provided.")
    if handle is None and name is None:
        raise ValueError("Either 'handle' or 'name' must be provided.")

def fetch_object(osm_model: openstudio.model.Model, object_type: str, handle: str | None = None, name: str | None = None, _object_ref: Any | None = None) -> Any | None:
    """
    Retrieve an OpenStudio object from the model using handle, name, or a direct reference.

    Parameters:
    - osm_model (openstudio.model.Model): The OpenStudio Model object.
    - object_type (str): The class name of the object to retrieve (e.g., 'Space', 'ThermalZone').
    - handle (Optional[str]): The handle string for the object.
    - name (Optional[str]): The name string for the object.
    - _object_ref (Optional[Any]): A direct object reference (if provided, bypasses lookup).

    Returns:
    - Optional[Any]: The retrieved OpenStudio object if found and initialized, otherwise None.
    """
    # 1. Performance Priority: Use the direct reference if provided
    if _object_ref is not None:
        return _object_ref

    # 2. Validation: Ensure we have exactly one identifier
    validate_args(handle, name)

    # 3. Determine method names and identifier type
    if handle:
        method_name = f"get{object_type}"
        identifier: Any = openstudio.toUUID(handle)
    else:
        method_name = f"get{object_type}ByName"
        identifier = name

    # 4. Safety Check: Ensure method exists in the model class
    if not hasattr(osm_model, method_name):
        logger.error(f"The method '{method_name}' does not exist in the current OpenStudio model API.")
        return None

    # 5. Dynamic Call to retrieve Optional object
    osm_optional = getattr(osm_model, method_name)(identifier)

    # 6. Safety Check: Only return the object if it is initialized
    if osm_optional.is_initialized():
        return osm_optional.get()
    
    logger.warning(f"No {object_type} found with identifier: {identifier}")
    return None
