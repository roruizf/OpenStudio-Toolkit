"""Guarded SDK access: Optionals through opt(), relations through the field target."""

from __future__ import annotations

from pathlib import Path

import openstudio
import pytest

from openstudio_toolkit._sdk import opt, related, related_name

RESOURCES = Path(__file__).resolve().parent / "resources"


def _load(name: str):
    return openstudio.osversion.VersionTranslator().loadModel(str(RESOURCES / name)).get()


def test_opt_unwraps_or_returns_none() -> None:
    assert opt(openstudio.OptionalDouble(2.5)) == 2.5
    assert opt(openstudio.OptionalDouble()) is None


def test_related_resolves_through_the_field(small_office_model) -> None:
    sizing = small_office_model.getSizingZones()[0]
    zone = related(sizing, "Zone or ZoneList Name", cast="ThermalZone")

    assert zone.handle() == sizing.thermalZone().handle()
    assert related_name(sizing, "Zone or ZoneList Name") == zone.nameString()
    assert related(sizing, "Zone or ZoneList Name", cast="Space") is None


def test_related_returns_none_on_orphans() -> None:
    sizing = _load("orphans_minimal.osm").getSizingZones()
    orphans = [s for s in sizing if related(s, "Zone or ZoneList Name") is None]

    assert orphans, "orphans_minimal.osm should carry an orphan Sizing:Zone"
    assert related_name(orphans[0], "Zone or ZoneList Name") is None


def test_related_rejects_unknown_fields(small_office_model) -> None:
    with pytest.raises(KeyError, match="no field"):
        related(small_office_model.getSizingZones()[0], "Not A Field")
