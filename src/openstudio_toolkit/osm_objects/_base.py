"""Shared helpers for osm_objects modules to reduce boilerplate.

Every osm_objects module follows the same triple pattern:
    get_X_as_dict()       -> Dict[str, Any]
    get_all_X_as_dicts()  -> List[Dict[str, Any]]
    get_all_X_as_dataframe() -> pd.DataFrame

The DataFrame conversion and the batch-to-dicts logic are identical across
all modules. This base module provides those shared pieces.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)


def build_dataframe(
    dicts: list[dict[str, Any]],
    object_type_name: str,
    sort_by: str = "Name",
) -> pd.DataFrame:
    """Convert a list of object dicts to a sorted, 0-indexed DataFrame.

    This replaces the 5-line boilerplate found at the end of every
    ``get_all_*_as_dataframe()`` function.

    Args:
        dicts: List of dictionaries from a ``get_all_*_as_dicts()`` call.
        object_type_name: Human-readable type name for the log message
            (e.g. "Space", "ThermalZone").
        sort_by: Column to sort by. Defaults to "Name".

    Returns:
        Sorted DataFrame with reset integer index.
    """
    df = pd.DataFrame(dicts)

    if not df.empty and sort_by in df.columns:
        df = df.sort_values(by=sort_by, ascending=True).reset_index(drop=True)

    logger.info(f"Retrieved {len(df)} {object_type_name} objects from the model.")
    return df


def build_all_dicts(
    osm_model: Any,
    model_getter: str,
    single_dict_fn: Callable,
    **kwargs: Any,
) -> list[dict[str, Any]]:
    """Batch-extract all objects of a type as dicts using the _object_ref shortcut.

    This replaces the 2-line pattern::

        all_objects = osm_model.getSpaces()
        return [get_space_object_as_dict(osm_model, _object_ref=obj) for obj in all_objects]

    Args:
        osm_model: The OpenStudio Model object.
        model_getter: Name of the model's getter method (e.g. "getSpaces").
        single_dict_fn: The ``get_*_object_as_dict`` function for one object.
        **kwargs: Extra keyword arguments forwarded to ``single_dict_fn``
            (e.g. ``enriched_data=True``).

    Returns:
        List of dictionaries, one per object.
    """
    getter = getattr(osm_model, model_getter)
    all_objects = getter()
    return [single_dict_fn(osm_model, _object_ref=obj, **kwargs) for obj in all_objects]
