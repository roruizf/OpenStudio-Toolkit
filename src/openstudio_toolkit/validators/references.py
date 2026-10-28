"""Orphan relations reported as findings instead of crashing the reader.

An empty reference in a field listed in ``FATAL_WHEN_ABSENT`` means a typed OpenStudio accessor
would segfault on that object (e.g. a ``Sizing:Zone`` with no zone). The generic reader reads such
objects safely; this validator turns them into ``integrity.reference.absent`` findings.

A reference to a handle that does not exist cannot be seen here: OpenStudio clears it and logs an
error while loading the model, so after loading it is indistinguishable from an empty reference.
"""

from __future__ import annotations

from typing import Any

from openstudio_toolkit.extractors.generic import ObjectRecord, read_model_objects
from openstudio_toolkit.schemas.findings import Finding, sort_findings
from openstudio_toolkit.validators._fatal_references import FATAL_WHEN_ABSENT


def validate_reference_records(records: list[ObjectRecord]) -> list[Finding]:
    """Return one finding per empty reference that a typed accessor would dereference blindly."""
    findings = []
    for record in records:
        for field in record.fields:
            accessors = FATAL_WHEN_ABSENT.get((record.idd_type, field.name))
            if accessors is None or field.target is not None:
                continue
            findings.append(
                Finding(
                    code="integrity.reference.absent",
                    severity="major",
                    message=f"{record.idd_type} '{record.name or record.handle}' has no '{field.name}'.",
                    object_type="model",
                    object_handle=record.handle,
                    object_name=record.name,
                    evidence={
                        "idd_type": record.idd_type,
                        "field": field.name,
                        "field_index": field.index,
                        "sdk_accessors": list(accessors),
                    },
                    suggested_action="Assign the missing object or remove the orphan from the model.",
                )
            )
    return sort_findings(findings)


def validate_references(model: Any) -> list[Finding]:
    """Read the model with the generic reader and report orphan relations."""
    return validate_reference_records(read_model_objects(model))
