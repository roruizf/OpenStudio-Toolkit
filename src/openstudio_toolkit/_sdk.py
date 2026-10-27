"""Guarded access to OpenStudio SDK values.

An empty OpenStudio Optional does not raise a clean exception on ``.get()``: it raises
``SystemError`` or leaves the interpreter with an exception set that surfaces on a later, unrelated
call. Unwrap Optionals only through :func:`opt`.

Typed accessors that return a related object directly (``SizingZone.thermalZone()``,
``SizingSystem.airLoopHVAC()``, ...) segfault when the reference field is empty; the pairs known for
the pinned OpenStudio are in ``validators/_fatal_references.py``. Read relations through the field
target with :func:`related` or :func:`related_name` instead.
"""

from __future__ import annotations

from typing import Any


def opt(value: Any) -> Any:
    """Return the content of an OpenStudio Optional, or None when it is empty."""
    return value.get() if value.is_initialized() else None


def related(obj: Any, field: str, cast: str | None = None) -> Any:
    """Return the object referenced by the IDD field ``field`` of ``obj``, or None when it is empty.

    The target is resolved through the field (``getTarget``), so an orphan object returns None
    instead of crashing. ``cast`` is an OpenStudio class name (e.g. ``"ThermalZone"``): the target is
    converted with ``to_<cast>()`` and None is returned when it is of another type. Without ``cast``
    the target is a ``WorkspaceObject``.

    Raises:
        KeyError: ``field`` is not a field of the object's IDD type (a programming error).
    """
    idd_object = obj.iddObject()
    index = opt(idd_object.getFieldIndex(field))
    if index is None:
        raise KeyError(f"{idd_object.name()} has no field {field!r}")
    target = opt(obj.getTarget(index))
    if target is None or cast is None:
        return target
    return opt(getattr(target, f"to_{cast}")())


def related_name(obj: Any, field: str) -> str | None:
    """Return the name of the object referenced by ``field``, or None when the reference is empty."""
    target = related(obj, field)
    return opt(target.name()) if target is not None else None


def optional_name(value: Any) -> str | None:
    """Return the name of the object inside an OpenStudio Optional, or None when it is empty.

    Use it with typed accessors that return an Optional (``Lights.schedule()``,
    ``Surface.construction()``): unlike :func:`related_name`, they also return values inherited from
    default sets (schedule sets, construction sets, space types) when the field itself is empty.
    """
    obj = opt(value)
    return opt(obj.name()) if obj is not None else None
