"""Item 4: apply a per-Space load mapping (contract of r2f-simulation-os base_model_space_loads.py)."""

from __future__ import annotations

import hashlib
from collections import Counter
from pathlib import Path

import openstudio
import pytest

from openstudio_toolkit.analysis.compare import compare_to_mapping
from openstudio_toolkit.transforms.apply import ApplyError, ApplyResult, apply_mapping
from openstudio_toolkit.views.verification import diff_rows

M = openstudio.model


def _load(path: Path):
    return openstudio.osversion.VersionTranslator().loadModel(str(path)).get()


def _space(model, x: float, name: str):
    points = [openstudio.Point3d(x, 0, 0), openstudio.Point3d(x, 10, 0)]
    points += [openstudio.Point3d(x + 10, 10, 0), openstudio.Point3d(x + 10, 0, 0)]
    space = M.Space.fromFloorPrint(openstudio.Point3dVector(points), 3, model).get()
    space.setName(name)
    return space


def _lights(model, name: str, space_or_type, level: float, definition=None):
    if definition is None:
        definition = M.LightsDefinition(model)
        definition.setName(f"{name} Definition")
        definition.setLightingLevel(level)
        definition.setFractionRadiant(0.25)
    lights = M.Lights(definition)
    lights.setName(name)
    if isinstance(space_or_type, M.SpaceType):
        lights.setSpaceType(space_or_type)
    else:
        lights.setSpace(space_or_type)
    return lights


def _save(model, folder: Path, name: str) -> Path:
    path = folder / name
    assert model.save(str(path), True)
    return path


@pytest.fixture
def empty(tmp_path) -> Path:
    """Spaces A and B, no loads."""
    model = M.Model()
    _space(model, 0, "A")
    _space(model, 20, "B")
    return _save(model, tmp_path, "empty.osm")


@pytest.fixture
def with_lights(tmp_path) -> Path:
    """Spaces A and B, one light each (100 W and 50 W per floor area), fraction radiant 0.25, a schedule."""
    model = M.Model()
    schedule = M.ScheduleConstant(model)
    schedule.setName("Light Sched")
    _lights(model, "LA", _space(model, 0, "A"), 100.0).setSchedule(schedule)
    lb = _lights(model, "LB", _space(model, 20, "B"), 0.0)
    lb.lightsDefinition().setWattsperSpaceFloorArea(0.5)
    return _save(model, tmp_path, "lights.osm")


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_creates_loads_and_compare_matches(empty, tmp_path) -> None:
    mapping = {"lights": {"A": 120.0, "B": 0.0}, "people": {"A": 4.0}, "electric_equipment": {"B": 300.0}}
    before = _digest(empty)
    results = apply_mapping(empty, tmp_path / "out.osm", mapping)

    assert results == (
        ApplyResult("lights", 1, 0, 1, 120.0),
        ApplyResult("people", 1, 0, 0, 4.0),
        ApplyResult("electric_equipment", 1, 0, 0, 300.0),
    )
    out = _load(tmp_path / "out.osm")
    assert set(compare_to_mapping(out, mapping).status) == {"match"}
    assert len(out.getSpaceByName("B").get().lights()) == 0  # zero-object rule
    assert [x.nameString() for x in out.getSpaceByName("A").get().lights()] == ["A Lights"]
    assert out.getLightsDefinitionByName("A Lights Definition").is_initialized()
    assert _digest(empty) == before


def test_existing_load_is_refused_by_default_and_nothing_is_written(with_lights, tmp_path) -> None:
    with pytest.raises(ApplyError) as refused:
        apply_mapping(with_lights, tmp_path / "out.osm", {"lights": {"A": 120.0, "B": 60.0, "C": 1.0}})
    assert len(refused.value.problems) == 3
    assert "Space 'C' is not in the model" in refused.value.problems[2]
    assert 'existing="update"' in refused.value.problems[0]
    assert not (tmp_path / "out.osm").exists()


def test_update_sets_only_the_value(with_lights, tmp_path) -> None:
    mapping = {"lights": {"A": 120.0, "B": 60.0}}
    results = apply_mapping(with_lights, tmp_path / "out.osm", mapping, existing="update")
    assert results == (ApplyResult("lights", 0, 2, 0, 180.0),)

    parent, child = _load(with_lights), _load(tmp_path / "out.osm")
    assert set(compare_to_mapping(child, mapping).status) == {"match"}
    rows = diff_rows(parent, child, mapping)
    changed = Counter(zip(rows.key, rows.field, strict=True))
    # A: the level only. B was per floor area: the method switches to an absolute level.
    assert changed == Counter(
        {
            ("LA Definition", "Lighting Level"): 1,
            ("LB Definition", "Design Level Calculation Method"): 1,
            ("LB Definition", "Lighting Level"): 1,
            ("LB Definition", "Watts per Space Floor Area"): 1,
        }
    )
    light = child.getLightsByName("LA").get()
    assert light.lightsDefinition().fractionRadiant() == 0.25
    assert light.schedule().get().nameString() == "Light Sched"


@pytest.mark.parametrize("case", ["two_loads", "shared_definition", "multiplier", "zero"])
def test_update_refuses_what_it_cannot_change_alone(tmp_path, case: str) -> None:
    model = M.Model()
    a, b = _space(model, 0, "A"), _space(model, 20, "B")
    la = _lights(model, "LA", a, 100.0)
    requested = 0.0 if case == "zero" else 120.0
    if case == "two_loads":
        _lights(model, "LA2", a, 10.0)
    elif case == "shared_definition":
        _lights(model, "LB", b, 0.0, definition=la.lightsDefinition())
    elif case == "multiplier":
        la.setMultiplier(2)
    path = _save(model, tmp_path, "in.osm")
    with pytest.raises(ApplyError, match={"two_loads": "exactly one", "shared_definition": "shared by 2",
                                          "multiplier": "multiplier", "zero": "zero-object"}[case]):
        apply_mapping(path, tmp_path / "out.osm", {"lights": {"A": requested}}, existing="update")


@pytest.mark.parametrize("existing", ["refuse", "update"])
@pytest.mark.parametrize("where", ["own_space_type", "building_space_type"])
def test_load_from_a_space_type_is_always_refused(tmp_path, existing: str, where: str) -> None:
    model = M.Model()
    space = _space(model, 0, "A")
    space_type = M.SpaceType(model)
    space_type.setName("Office")
    if where == "own_space_type":
        space.setSpaceType(space_type)
    else:
        model.getBuilding().setSpaceType(space_type)
    _lights(model, "Office Lights", space_type, 0.0).lightsDefinition().setWattsperSpaceFloorArea(10.0)
    path = _save(model, tmp_path, "in.osm")
    with pytest.raises(ApplyError, match="from space type 'Office'"):
        apply_mapping(path, tmp_path / "out.osm", {"lights": {"A": 1000.0}}, existing=existing)


def test_bad_arguments(empty) -> None:
    with pytest.raises(ValueError, match="unknown families"):
        apply_mapping(empty, empty.with_name("o.osm"), {"lighting": {"A": 1.0}})
    with pytest.raises(ValueError, match="existing"):
        apply_mapping(empty, empty.with_name("o.osm"), {"lights": {"A": 1.0}}, existing="replace")
    with pytest.raises(ValueError, match="never modified"):
        apply_mapping(empty, empty, {"lights": {"A": 1.0}})
    with pytest.raises(ValueError, match="requests nothing"):
        apply_mapping(empty, empty.with_name("o.osm"), {"lights": {}})
