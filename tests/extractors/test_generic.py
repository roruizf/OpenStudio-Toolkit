"""Generic reader: every object, every IDD field, safe on orphan relations."""

from __future__ import annotations

from pathlib import Path

import openstudio
import pytest

from openstudio_toolkit.extractors.generic import read_model_objects
from openstudio_toolkit.validators._fatal_references import DERIVED_FOR_OPENSTUDIO
from openstudio_toolkit.validators.references import validate_references

RESOURCES = Path(__file__).resolve().parents[1] / "resources"


def _load(name: str):
    return openstudio.osversion.VersionTranslator().loadModel(str(RESOURCES / name)).get()


@pytest.fixture(scope="module")
def small_office():
    return _load("small_office.osm")


def test_reads_every_object_in_stable_order(small_office) -> None:
    records = read_model_objects(small_office)

    assert len(records) == len(small_office.objects())
    assert records == sorted(records, key=lambda r: (r.idd_type, r.handle))
    assert len({r.handle for r in records}) == len(records)


def test_fields_follow_the_idd_and_resolve_references(small_office) -> None:
    lights = next(r for r in read_model_objects(small_office) if r.idd_type == "OS:Lights")
    definition = next(f for f in lights.fields if f.name == "Lights Definition Name")
    sdk_lights = small_office.getLights(openstudio.toUUID(lights.handle)).get()

    assert [f.index for f in lights.fields] == list(range(1, len(lights.fields) + 1))
    assert definition.is_reference
    assert definition.target == str(sdk_lights.lightsDefinition().handle())


def test_extensible_fields_are_numbered_by_group(small_office) -> None:
    day = next(
        r for r in read_model_objects(small_office) if r.idd_type == "OS:Schedule:Day" and len(r.fields) > 10
    )
    grouped = [f for f in day.fields if f.group is not None]

    assert grouped[0].group == 1
    assert grouped[-1].group == max(f.group for f in grouped)
    assert {f.name for f in grouped if f.group == 1} == {f.name for f in grouped if f.group == grouped[-1].group}


def test_units_come_from_the_idd(small_office) -> None:
    definition = next(r for r in read_model_objects(small_office) if r.idd_type == "OS:Lights:Definition")
    level = next(f for f in definition.fields if f.name == "Lighting Level")

    assert level.units == "W"


def test_orphan_objects_are_read_not_crashed() -> None:
    # Derived from Tribe-Hotel-015 (a third-party model): only its orphan objects, which make the
    # typed accessors Sizing:Zone.thermalZone(), ZoneHVAC:EquipmentList.thermalZone() and
    # StandardsInformation:Material.material() segfault.
    records = read_model_objects(_load("orphans_minimal.osm"))
    sizing = [r for r in records if r.idd_type == "OS:Sizing:Zone"]

    assert len(sizing) == 2
    assert all(r.fields[0].target is None for r in sizing)


def test_orphans_become_findings() -> None:
    findings = validate_references(_load("orphans_minimal.osm"))

    assert {f.code for f in findings} == {"integrity.reference.absent"}
    assert sorted(f.evidence["idd_type"] for f in findings) == [
        "OS:Sizing:Zone",
        "OS:Sizing:Zone",
        "OS:StandardsInformation:Material",
        "OS:ZoneHVAC:EquipmentList",
        "OS:ZoneHVAC:EquipmentList",
    ]
    assert all(f.object_type == "model" and f.severity == "major" for f in findings)


def test_healthy_model_has_no_orphan_findings(small_office) -> None:
    assert validate_references(small_office) == []


def test_fatal_table_matches_the_pinned_openstudio() -> None:
    assert openstudio.openStudioVersion() == DERIVED_FOR_OPENSTUDIO
