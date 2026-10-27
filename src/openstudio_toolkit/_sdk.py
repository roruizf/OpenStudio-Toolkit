"""Guarded access to OpenStudio SDK values.

An empty OpenStudio Optional does not raise a clean exception on ``.get()``: it raises
``SystemError`` or leaves the interpreter with an exception set that surfaces on a later, unrelated
call. Unwrap Optionals only through :func:`opt`.
"""

from __future__ import annotations

from typing import Any


def opt(value: Any) -> Any:
    """Return the content of an OpenStudio Optional, or None when it is empty."""
    return value.get() if value.is_initialized() else None
