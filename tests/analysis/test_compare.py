"""Item 5: compare a model against a mapping of requested loads, by Space or Thermal Zone."""

from __future__ import annotations

import math
import tomllib
from pathlib import Path

import openstudio
import pytest

from openstudio_toolkit.analysis.compare import (
    COMPARE_COLUMNS,
    COMPARE_FAMILIES,
    COMPARE_STATUS_VALUES,
    compare_to_mapping,
)
from openstudio_toolkit.dump import dump_view
from openstudio_toolkit.extractors.generic import read_model_objects

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = tomllib.loads((ROOT / "docs" / "contracts" / "v0.3.toml").read_text(encoding="utf-8"))
OFFICE_HUB = ROOT / "examples" / "R2F-Office-Hub.osm"
FIXTURES = {
    "small_office": ROOT / "tests" / "resources" / "small_office.osm",
    "extra_families": ROOT / "tests" / "resources" / "extra_families.osm",
    "office_hub": OFFICE_HUB,
}

M = openstudio.model


def _load(path: Path):
    if not path.exists():
        pytest.skip(f"{path.name} not present")
    return openstudio.osversion.VersionTranslator().loadModel(str(path)).get()


def _row(df, family: str, key: str) -> dict:
    rows = df[(df.family == family) & (df.key == key)].to_dict("records")
    assert len(rows) == 1
    return rows[0]


def test_schema_follows_the_contract() -> None:
    spec = CONTRACT["artifact"]["compare"]

    assert list(COMPARE_COLUMNS) == spec["columns"]
    assert list(COMPARE_STATUS_VALUES) == spec["status_values"]


def test_reads_what_openstudio_resolves_not_what_is_written() -> None:
    """R2F-Office-Hub: 5 W written on the Storage light, plus 10.5 W from the Storage space type."""
    df = compare_to_mapping(_load(OFFICE_HUB), {"lights": {"0.05-Storage": 5.0, "0.01-Lobby": 148.0}})

    assert _row(df, "lights", "0.05-Storage") == {
        "family": "lights",
        "key": "0.05-Storage",
        "field": "Lighting Level {W}",
        "requested": 5.0,
        "in_model": 15.5,
        "difference": 10.5,
        "status": "differs",
    }
    assert _row(df, "lights", "0.01-Lobby")["status"] == "match"


def _expected_totals(model) -> dict[tuple[str, str], float]:
    """Space totals recomputed from the dump views and records, independently of OpenStudio's totals.

    Loads reach a Space from the Space itself and from its space type: its own, or the building's when
    the Space field is empty. Every design method; each load's multiplier.
    """
    view = dump_view(model)
    records = read_model_objects(model)
    by_handle = {r.handle: r for r in records}

    def target_name(record, field: str) -> str | None:
        target = next(f for f in record.fields if f.name == field).target
        return by_handle[target].name if target else None

    building = next((r for r in records if r.idd_type == "OS:Building"), None)  # extra_families has none
    building_type = target_name(building, "Space Type Name") if building is not None else None
    spaces = {r.name: r for r in records if r.idd_type == "OS:Space"}
    area = view["space"].set_index("Name")["Floor Area {m2}"]
    methods = {
        "people": (
            "Number of People Calculation Method",
            {
                "People": ("Number of People {people}", lambda x, a, p: x),
                "People/Area": ("People per Space Floor Area {person/m2}", lambda x, a, p: x * a),
                "Area/Person": ("Space Floor Area per Person {m2/person}", lambda x, a, p: a / x if x else 0.0),
            },
        ),
        "lights": (
            "Design Level Calculation Method",
            {
                "LightingLevel": ("Lighting Level {W}", lambda x, a, p: x),
                "Watts/Area": ("Watts per Space Floor Area {W/m2}", lambda x, a, p: x * a),
                "Watts/Person": ("Watts per Person {W/person}", lambda x, a, p: x * p),
            },
        ),
        "electric_equipment": (
            "Design Level Calculation Method",
            {
                "EquipmentLevel": ("Design Level {W}", lambda x, a, p: x),
                "Watts/Area": ("Watts per Space Floor Area {W/m2}", lambda x, a, p: x * a),
                "Watts/Person": ("Watts per Person {W/person}", lambda x, a, p: x * p),
            },
        ),
    }
    definition_column = {
        "people": "People Definition Name",
        "lights": "Lights Definition Name",
        "electric_equipment": "Electric Equipment Definition Name",
    }
    expected: dict[tuple[str, str], float] = {}
    for family in COMPARE_FAMILIES:  # people first: per-person loads need the Space's people
        method_column, by_method = methods[family]
        definitions = view[f"{family}_definition"].set_index("Name")
        loads = view[family]
        for name, record in spaces.items():
            reach = {name, target_name(record, "Space Type Name") or building_type}
            total = 0.0
            for _, load in loads[loads["Space or SpaceType Name"].isin(reach)].iterrows():
                definition = definitions.loc[load[definition_column[family]]]
                column, value = by_method[definition[method_column]]
                total += value(definition[column], area[name], expected.get(("people", name), 0.0)) * load["Multiplier"]
            expected[(family, name)] = total
    return expected


@pytest.mark.parametrize("fixture", list(FIXTURES))
def test_totals_match_an_independent_recomputation(fixture: str) -> None:
    """Every Space and Thermal Zone total, cell by cell (FPM4 v10 and Office Hub: 1,908 of 1,908 too)."""
    model = _load(FIXTURES[fixture])
    expected = _expected_totals(model)
    by_space = {f: {s: v for (g, s), v in expected.items() if g == f} for f in COMPARE_FAMILIES}
    zones = {z.nameString(): [s.nameString() for s in z.spaces()] for z in model.getThermalZones()}
    by_zone = {f: {z: sum(by_space[f][s] for s in spaces) for z, spaces in zones.items()} for f in COMPARE_FAMILIES}

    for mapping, by in ((by_space, "space"), (by_zone, "thermal_zone")):
        df = compare_to_mapping(model, mapping, by=by)
        assert len(df) == sum(len(v) for v in mapping.values())
        for row in df.itertuples(index=False):
            assert row.status == "match", row
            assert math.isclose(row.in_model, row.requested, rel_tol=1e-12, abs_tol=1e-9), row


def _space(model, x: float, name: str):
    points = [openstudio.Point3d(x, 0, 0), openstudio.Point3d(x, 10, 0)]
    points += [openstudio.Point3d(x + 10, 10, 0), openstudio.Point3d(x + 10, 0, 0)]
    space = M.Space.fromFloorPrint(openstudio.Point3dVector(points), 3, model).get()
    space.setName(name)
    return space


def _lights(model, parent, level: float | None = None, per_area: float | None = None, multiplier: float = 1.0):
    definition = M.LightsDefinition(model)
    if level is not None:
        definition.setLightingLevel(level)
    else:
        definition.setWattsperSpaceFloorArea(per_area)
    lights = M.Lights(definition)
    lights.setMultiplier(multiplier)
    if isinstance(parent, M.Space):
        lights.setSpace(parent)
    else:
        lights.setSpaceType(parent)
    return lights


def test_inheritance_methods_and_multipliers() -> None:
    model = M.Model()
    building_type = M.SpaceType(model)
    _lights(model, building_type, per_area=2.0)
    model.getBuilding().setSpaceType(building_type)
    own_type = M.SpaceType(model)
    per_person = M.LightsDefinition(model)
    per_person.setWattsperPerson(10.0)
    M.Lights(per_person).setSpaceType(own_type)

    inherits = _space(model, 0, "inherits building type")  # 100 m2, no space type of its own
    owns = _space(model, 20, "own type")
    owns.setSpaceType(own_type)
    _lights(model, owns, level=50.0, multiplier=2.0)
    people = M.PeopleDefinition(model)
    people.setNumberofPeople(3.0)
    M.People(people).setSpace(owns)
    zone = M.ThermalZone(model)
    zone.setName("Z")
    zone.setMultiplier(3)
    for space in (inherits, owns):
        space.setThermalZone(zone)

    df = compare_to_mapping(model, {"lights": {"inherits building type": 200.0, "own type": 130.0}})
    # building type only when the Space has none (own type: 50 W x 2 + 10 W/person x 3, no 2 W/m2)
    assert df.status.tolist() == ["match", "match"]

    zone_df = compare_to_mapping(model, {"lights": {"Z": 330.0}}, by="thermal_zone")
    assert _row(zone_df, "lights", "Z")["status"] == "match"  # sum of Spaces, no zone multiplier


def test_missing_and_zero() -> None:
    model = M.Model()
    lit = _space(model, 0, "lit")
    _space(model, 20, "dark")
    _lights(model, lit, level=100.0)

    df = compare_to_mapping(
        model,
        {
            "lights": {"lit": 100.0, "dark": 40.0, "nowhere": 10.0},
            "people": {"dark": 0.0},
        },
    )

    assert df[["key", "status"]].values.tolist() == [
        ["lit", "match"],
        ["dark", "missing"],  # nothing reaches it
        ["nowhere", "missing"],  # no such Space
        ["dark", "match"],  # zero requested, nothing there
    ]
    assert df.in_model.isna().tolist() == [False, True, True, False]
    assert df.in_model[3] == 0.0


def test_orphan_load_is_missing_not_a_crash() -> None:
    """An empty definition field makes OpenStudio's total raise; the row is missing, the rest go on."""
    model = M.Model()
    broken = _space(model, 0, "broken")
    fine = _space(model, 20, "fine")
    _lights(model, broken, level=5.0).setString(2, "")
    _lights(model, fine, level=7.0)

    df = compare_to_mapping(model, {"lights": {"broken": 5.0, "fine": 7.0}})

    assert df.status.tolist() == ["missing", "match"]


@pytest.mark.parametrize(
    ("mapping", "by"),
    [({"lighting": {"x": 1.0}}, "space"), ({"lights": {"x": 1.0}}, "story")],
)
def test_rejects_unknown_family_or_scope(mapping, by) -> None:
    with pytest.raises(ValueError):
        compare_to_mapping(M.Model(), mapping, by=by)
