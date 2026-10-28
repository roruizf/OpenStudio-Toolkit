"""Parent -> child diff of two models, built on the generic reader (item 6).

Matching (V0.3-DECISIONS.md, step B): 1) same handle and IDD type; 2) same IDD type and name, when
the name is unique among the unmatched objects of that type on both sides. Anything else is reported
as removed (parent) and added (child), never guessed. ``CommentOnly`` objects have no persistent
handle and are left out.

Reference fields are compared by the identity of their matched target, not by its name: renaming a
schedule is one change on the schedule, not one on every object that uses it.

Approved by Roberto (2026-10-27): every IDD type is diffed, not only the dump families (``family`` is
the dump family name when there is one, else the IDD type); topology (``OS:Connection``, ``OS:Node``,
``OS:PortList``) is left out of the rows unless asked for, but always takes part in matching; an
unnamed object is keyed by the name of the object it belongs to (its first reference with a target,
e.g. a ``Sizing:System`` by its air loop); an added or removed object is one row with no field.
``not_requested`` is not produced here: it is assigned in item 7, when the diff meets the mapping.

Values are compared as stored text; an empty field and a missing extensible field are both None. In
the three real pairs of step B no change was a number written two ways.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from typing import Any

import pandas as pd

from openstudio_toolkit.dump import families as dump_families
from openstudio_toolkit.extractors.generic import FieldRecord, ObjectRecord, read_model_objects

DIFF_COLUMNS = ("family", "key", "field", "parent", "child", "status", "match_method")
DIFF_STATUS_VALUES = ("changed", "added", "removed")
DIFF_MATCH_METHODS = ("handle", "type_name")

TOPOLOGY_TYPES = frozenset({"OS:Connection", "OS:Node", "OS:PortList"})
EXCLUDED_TYPES = frozenset({"CommentOnly"})


def _match(parent: dict[str, ObjectRecord], child: dict[str, ObjectRecord]) -> dict[str, tuple[str, str]]:
    """Parent handle -> (child handle, match method)."""
    pairs = {h: (h, "handle") for h, r in parent.items() if h in child and child[h].idd_type == r.idd_type}
    matched_child = {c for c, _ in pairs.values()}

    def by_type_name(records: dict[str, ObjectRecord], taken: Iterable[str]) -> dict[tuple[str, str], list[str]]:
        groups: dict[tuple[str, str], list[str]] = defaultdict(list)
        skip = set(taken)
        for handle, record in records.items():
            if handle not in skip and record.name:
                groups[(record.idd_type, record.name)].append(handle)
        return groups

    child_groups = by_type_name(child, matched_child)
    for key, parents in by_type_name(parent, pairs).items():
        children = child_groups.get(key, [])
        if len(parents) == 1 and len(children) == 1:
            pairs[parents[0]] = (children[0], "type_name")
    return pairs


def _key(record: ObjectRecord, records: dict[str, ObjectRecord]) -> str:
    if record.name:
        return record.name
    owner = next((records.get(f.target) for f in record.fields if f.target is not None), None)
    return owner.name if owner is not None and owner.name else record.handle


def _label(field: FieldRecord) -> str:
    return field.name if field.group is None else f"{field.name} #{field.group}"


def _value(field: FieldRecord | None) -> str | None:
    return field.value or None if field is not None else None


def _same(old: FieldRecord | None, new: FieldRecord | None, parent_to_child: dict[str, str]) -> bool:
    if old is not None and new is not None and old.is_reference:
        if old.target is None or new.target is None:
            return old.target is None and new.target is None
        return parent_to_child.get(old.target) == new.target
    return _value(old) == _value(new)


def _selected(families: Iterable[str] | None) -> set[str] | None:
    if families is None:
        return None
    selected = set(families)
    unknown = sorted(name for name in selected if name not in dump_families() and not name.startswith("OS:"))
    if unknown:
        raise ValueError(f"unknown families: {', '.join(unknown)} (use a dump family name or an IDD type)")
    return selected


def diff_models(
    parent: Any,
    child: Any,
    families: Iterable[str] | None = None,
    include_topology: bool = False,
) -> pd.DataFrame:
    """Diff two OpenStudio models, parent -> child, with the columns of ``DIFF_COLUMNS``.

    ``families`` keeps only rows whose ``family`` is listed (dump family names, or IDD types for
    types without a dump family); matching always uses every object of both models.
    """
    selected = _selected(families)
    old = {r.handle: r for r in read_model_objects(parent) if r.idd_type not in EXCLUDED_TYPES}
    new = {r.handle: r for r in read_model_objects(child) if r.idd_type not in EXCLUDED_TYPES}
    pairs = _match(old, new)
    parent_to_child = {p: c for p, (c, _) in pairs.items()}
    names = dump_families()
    family_of = {idd_type: name for name, idd_type in names.items()}

    rows: list[tuple[Any, ...]] = []

    def keep(idd_type: str) -> str | None:
        if idd_type in TOPOLOGY_TYPES and not include_topology:
            return None
        family = family_of.get(idd_type, idd_type)
        return family if selected is None or family in selected else None

    for p, (c, method) in pairs.items():
        family = keep(new[c].idd_type)
        if family is None:
            continue
        key = _key(new[c], new)
        old_fields = {f.index: f for f in old[p].fields}
        new_fields = {f.index: f for f in new[c].fields}
        for index in sorted(old_fields.keys() | new_fields.keys()):
            a, b = old_fields.get(index), new_fields.get(index)
            if not _same(a, b, parent_to_child):
                label = _label(b if b is not None else a)  # type: ignore[arg-type]
                rows.append((family, key, label, _value(a), _value(b), "changed", method, index))

    matched_child = set(parent_to_child.values())
    for status, records, unmatched in (
        ("removed", old, old.keys() - pairs.keys()),
        ("added", new, new.keys() - matched_child),
    ):
        for handle in unmatched:
            family = keep(records[handle].idd_type)
            if family is not None:
                rows.append((family, _key(records[handle], records), None, None, None, status, None, 0))

    df = pd.DataFrame(rows, columns=[*DIFF_COLUMNS, "_index"])
    df = df.sort_values(["family", "key", "status", "_index"], kind="stable", ignore_index=True)
    return df.drop(columns="_index")
