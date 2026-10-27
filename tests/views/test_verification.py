"""Item 7: verification artifact, fixed schema and golden output."""

from __future__ import annotations

import tomllib
from pathlib import Path

import openstudio
import pytest

from openstudio_toolkit.views.verification import (
    COMPARE_COLUMNS,
    DIFF_COLUMNS,
    DIFF_STATUS_VALUES,
    compare_rows,
    diff_rows,
)

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = tomllib.loads((ROOT / "docs" / "contracts" / "v0.3.toml").read_text(encoding="utf-8"))
M = openstudio.model


def _space(model, x: float, name: str):
    points = [openstudio.Point3d(x, 0, 0), openstudio.Point3d(x, 10, 0)]
    points += [openstudio.Point3d(x + 10, 10, 0), openstudio.Point3d(x + 10, 0, 0)]
    space = M.Space.fromFloorPrint(openstudio.Point3dVector(points), 3, model).get()
    space.setName(name)
    return space


def _lights(model, name: str, parent, level: float | None = None, per_area: float | None = None) -> None:
    definition = M.LightsDefinition(model)
    definition.setName(f"{name} Definition")
    if level is not None:
        definition.setLightingLevel(level)
    else:
        definition.setWattsperSpaceFloorArea(per_area)
    lights = M.Lights(definition)
    lights.setName(name)
    if isinstance(parent, M.Space):
        lights.setSpace(parent)
    else:
        lights.setSpaceType(parent)


@pytest.fixture(scope="module")
def pair(tmp_path_factory) -> tuple[Path, Path]:
    """Parent: Spaces A (space type ST) and B; lights on A, on B and on ST; a named schedule.

    Child: every lights level changed, an electric equipment added on A, the schedule removed.
    """
    model = M.Model()
    space_type = M.SpaceType(model)
    space_type.setName("ST")
    a, b = _space(model, 0, "A"), _space(model, 20, "B")
    a.setSpaceType(space_type)
    for space, zone_name in ((a, "ZA"), (b, "ZB")):
        zone = M.ThermalZone(model)
        zone.setName(zone_name)
        space.setThermalZone(zone)
    _lights(model, "LA", a, level=100.0)
    _lights(model, "LB", b, level=50.0)
    _lights(model, "LST", space_type, per_area=2.0)
    M.ScheduleConstant(model).setName("Sched X")

    folder = tmp_path_factory.mktemp("verification")
    parent = folder / "parent.osm"
    assert model.save(str(parent), True)

    model = openstudio.osversion.VersionTranslator().loadModel(str(parent)).get()
    model.getLightsDefinitionByName("LA Definition").get().setLightingLevel(120.0)
    model.getLightsDefinitionByName("LB Definition").get().setLightingLevel(60.0)
    model.getLightsDefinitionByName("LST Definition").get().setWattsperSpaceFloorArea(3.0)
    definition = M.ElectricEquipmentDefinition(model)
    definition.setName("EA Definition")
    equipment = M.ElectricEquipment(definition)
    equipment.setName("EA")
    equipment.setSpace(model.getSpaceByName("A").get())
    model.getScheduleConstantByName("Sched X").get().remove()
    child = folder / "child.osm"
    assert model.save(str(child), True)
    return parent, child


def _load(path: Path):
    return openstudio.osversion.VersionTranslator().loadModel(str(path)).get()


def _rows(df) -> list[tuple]:
    return [tuple(None if v != v else v for v in r) for r in df.itertuples(index=False)]  # NaN -> None


GOLDEN_DIFF = [
    ("OS:Schedule:Constant", "Sched X", "(object removed)", None, None, "not_requested", None),
    ("electric_equipment", "EA", "(object added)", None, None, "not_requested", None),
    ("electric_equipment_definition", "EA Definition", "(object added)", None, None, "not_requested", None),
    ("lights_definition", "LA Definition", "Lighting Level", "100", "120", "changed", "handle"),
    ("lights_definition", "LB Definition", "Lighting Level", "50", "60", "not_requested", "handle"),
    ("lights_definition", "LST Definition", "Watts per Space Floor Area", "2", "3", "changed", "handle"),
]


@pytest.mark.parametrize(("by", "key"), [("space", "A"), ("thermal_zone", "ZA")])
def test_diff_golden_output(pair, by: str, key: str) -> None:
    """Requested: lights reaching A (its own, and its space type's). B's light, the equipment nobody
    asked for and the removed schedule are not_requested; added/removed keep their direction in field."""
    parent, child = pair
    df = diff_rows(_load(parent), _load(child), {"lights": {key: 0.0}}, by=by)

    assert list(df.columns) == list(DIFF_COLUMNS)
    assert sorted(_rows(df), key=lambda r: (r[0], r[1])) == GOLDEN_DIFF


def test_diff_without_the_family_in_the_mapping_is_all_not_requested(pair) -> None:
    parent, child = pair
    df = diff_rows(_load(parent), _load(child), {"people": {"A": 3.0}})

    assert set(df.status) == {"not_requested"}


def test_added_and_removed_requested_rows_keep_their_status(pair) -> None:
    parent, child = pair
    df = diff_rows(_load(parent), _load(child), {"electric_equipment": {"A": 0.0}})

    requested = [(r[0], r[1], r[2], r[5]) for r in _rows(df) if r[5] != "not_requested"]
    assert sorted(requested) == [
        ("electric_equipment", "EA", None, "added"),
        ("electric_equipment_definition", "EA Definition", None, "added"),
    ]


def test_compare_golden_output(pair) -> None:
    df = compare_rows(_load(pair[1]), {"lights": {"A": 420.0, "B": 50.0}})  # A: 120 W + 3 W/m2 x 100 m2

    assert list(df.columns) == list(COMPARE_COLUMNS)
    assert df.values.tolist() == [
        ["lights", "A", "Lighting Level {W}", 420.0, 420.0, 0.0, "match"],
        ["lights", "B", "Lighting Level {W}", 50.0, 60.0, 10.0, "differs"],
    ]


def test_status_values_follow_the_contract() -> None:
    assert list(DIFF_STATUS_VALUES) == CONTRACT["artifact"]["diff"]["status_values"]
