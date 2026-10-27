"""Generic reader: every object in a model, every IDD field, without typed accessors.

The reader touches the model only through ``objects``, ``iddObject``, ``handle``, ``name``,
``numFields``, ``getString`` and ``getTarget`` (enforced by tests/contract). Typed OpenStudio
accessors that return a related object directly segfault when the relation is absent (74
(type, accessor) pairs in OpenStudio 3.11.0); this reader never calls them, so an orphan object is
read like any other and shows up as a reference field with no target.

Field names and units come from the installed OpenStudio IDD, not from the object's comments.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from openstudio_toolkit._sdk import opt

REFERENCE_FIELD_TYPE = "ObjectListType"


@dataclass(frozen=True, slots=True)
class FieldRecord:
    """One field of one object, as stored in the model."""

    index: int
    name: str
    group: int | None
    value: str | None
    units: str | None
    is_reference: bool
    target: str | None


@dataclass(frozen=True, slots=True)
class ObjectRecord:
    """One model object: IDD type, handle, name and all its fields after the handle."""

    idd_type: str
    handle: str
    name: str | None
    fields: tuple[FieldRecord, ...]


@dataclass(frozen=True, slots=True)
class _FieldSpec:
    name: str
    units: str | None
    is_reference: bool


def _field_spec(idd_field: Any) -> _FieldSpec:
    props = idd_field.properties()
    return _FieldSpec(
        name=idd_field.name(),
        units=opt(props.units),
        is_reference=props.type.valueName() == REFERENCE_FIELD_TYPE,
    )


def _specs(idd_object: Any) -> tuple[tuple[_FieldSpec, ...], tuple[_FieldSpec, ...]]:
    fixed = tuple(_field_spec(f) for f in idd_object.nonextensibleFields())
    extensible = tuple(_field_spec(f) for f in idd_object.extensibleGroup())
    return fixed, extensible


def _field(obj: Any, index: int, fixed: tuple[_FieldSpec, ...], extensible: tuple[_FieldSpec, ...]) -> FieldRecord:
    if index < len(fixed):
        spec, group = fixed[index], None
    elif extensible:
        offset = index - len(fixed)
        spec, group = extensible[offset % len(extensible)], offset // len(extensible) + 1
    else:
        spec, group = _FieldSpec(name=f"Field {index}", units=None, is_reference=False), None
    target = opt(obj.getTarget(index)) if spec.is_reference else None
    return FieldRecord(
        index=index,
        name=spec.name,
        group=group,
        value=opt(obj.getString(index)),
        units=spec.units,
        is_reference=spec.is_reference,
        target=str(target.handle()) if target is not None else None,
    )


def read_model_objects(model: Any) -> list[ObjectRecord]:
    """Read every object of an OpenStudio model into records, ordered by IDD type then handle.

    Field 0 (the handle) is carried as ``ObjectRecord.handle``; ``fields`` starts at index 1.
    Extensible fields carry their 1-based group number in ``FieldRecord.group`` and the IDD name of
    the field within the group. For reference fields, ``value`` is what OpenStudio stores for display
    (the target's name when it resolves) and ``target`` is the target's handle, or None when the
    reference is empty.
    """
    cache: dict[str, tuple[tuple[_FieldSpec, ...], tuple[_FieldSpec, ...]]] = {}

    def record(obj: Any) -> ObjectRecord:
        idd_object = obj.iddObject()
        idd_type = idd_object.name()
        if idd_type not in cache:
            cache[idd_type] = _specs(idd_object)
        fixed, extensible = cache[idd_type]
        return ObjectRecord(
            idd_type=idd_type,
            handle=str(obj.handle()),
            name=opt(obj.name()),
            fields=tuple(_field(obj, index, fixed, extensible) for index in range(1, obj.numFields())),
        )

    return sorted((record(obj) for obj in model.objects()), key=lambda r: (r.idd_type, r.handle))
