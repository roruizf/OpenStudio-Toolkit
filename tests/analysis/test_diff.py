"""Item 6: parent -> child diff on the generic reader."""

from __future__ import annotations

import subprocess
import sys
import tomllib
from pathlib import Path

import openstudio
import pytest

from openstudio_toolkit.analysis.diff import (
    DIFF_COLUMNS,
    DIFF_MATCH_METHODS,
    DIFF_STATUS_VALUES,
    TOPOLOGY_TYPES,
    diff_models,
)

ROOT = Path(__file__).resolve().parents[2]
SMALL_OFFICE = ROOT / "tests" / "resources" / "small_office.osm"
ORPHAN_FIXTURE = ROOT / "tests" / "resources" / "orphans_minimal.osm"
CONTRACT = tomllib.loads((ROOT / "docs" / "contracts" / "v0.3.toml").read_text(encoding="utf-8"))


def _translate(path: Path):
    return openstudio.osversion.VersionTranslator().loadModel(str(path)).get()


@pytest.fixture(scope="module")
def translated(tmp_path_factory) -> Path:
    """small_office saved once in the pinned OpenStudio version.

    The fixture is 3.2.0: translating it creates an unnamed OS:WaterHeater:Sizing with a fresh handle
    on every load, which no level of the matching can pair (reported as removed + added).
    """
    path = tmp_path_factory.mktemp("diff") / SMALL_OFFICE.name
    assert _translate(SMALL_OFFICE).save(str(path), True)
    return path


@pytest.fixture
def _load(translated):
    return lambda: _translate(translated)


def _rows(df, status: str) -> list[tuple]:
    return [
        tuple(r) for r in df[df.status == status][["family", "key", "field", "parent", "child"]].itertuples(index=False)
    ]


def test_schema_follows_the_contract() -> None:
    spec = CONTRACT["artifact"]["diff"]

    assert list(DIFF_COLUMNS) == spec["columns"]
    assert set(DIFF_STATUS_VALUES) == set(spec["status_values"]) - {"not_requested"}  # item 7 assigns it
    assert list(DIFF_MATCH_METHODS) == spec["match_methods"]


def test_same_model_has_no_rows(_load) -> None:
    df = diff_models(_load(), _load())

    assert list(df.columns) == list(DIFF_COLUMNS)
    assert df.empty


def test_value_change_is_one_row_matched_by_handle(_load) -> None:
    parent, child = _load(), _load()
    lights = child.getLightsDefinitions()[0]
    old = lights.wattsperSpaceFloorArea().get()
    lights.setWattsperSpaceFloorArea(old + 1)

    df = diff_models(parent, child)

    assert len(df) == 1
    row = df.iloc[0]
    assert (row.family, row.key, row.status, row.match_method) == (
        "lights_definition",
        lights.nameString(),
        "changed",
        "handle",
    )
    assert row.field == "Watts per Space Floor Area"
    assert float(row.parent) == pytest.approx(old) and float(row.child) == pytest.approx(old + 1)


def test_rename_is_one_change_not_one_per_user(_load) -> None:
    """References are compared by matched target: users of a renamed schedule do not change."""
    parent, child = _load(), _load()
    schedule = child.getLightss()[0].schedule().get()
    users = [o for o in child.objects() if any(t.handle() == schedule.handle() for t in o.targets())]
    assert users
    old_name = schedule.nameString()
    schedule.setName("Renamed lighting schedule")

    df = diff_models(parent, child)

    assert _rows(df, "changed") == [
        ("schedule_ruleset", "Renamed lighting schedule", "Name", old_name, "Renamed lighting schedule")
    ]


def test_removed_and_added_objects_are_one_row_each(_load) -> None:
    parent, child = _load(), _load()
    removed = child.getLightss()[0]
    removed_name = removed.nameString()
    removed.remove()
    added = openstudio.model.ScheduleConstant(child)
    added.setName("New constant schedule")

    df = diff_models(parent, child)

    assert ("lights", removed_name, None, None, None) in _rows(df, "removed")
    assert _rows(df, "added") == [("OS:Schedule:Constant", "New constant schedule", None, None, None)]
    assert df[df.status != "changed"].match_method.isna().all()


def test_new_handles_match_by_type_and_unique_name(_load) -> None:
    """A clone has new handles for every object; named objects still match, by type and name.

    Unnamed objects (connections, sizing objects, unique simulation settings) cannot match without
    their handle, so they are removed + added, and every field that points to one of them changes.
    No named object or plain value changes.
    """
    parent = _load()
    child = openstudio.model.toModel(parent.clone())

    df = diff_models(parent, child)

    changed = df[df.status == "changed"]
    assert set(changed.match_method) == {"type_name"}
    assert changed.parent.str.startswith("{").all() and changed.child.str.startswith("{").all()
    unmatched = df[df.status != "changed"]
    assert (unmatched.status == "added").sum() == (unmatched.status == "removed").sum()
    assert len(unmatched) < len(parent.objects()) / 2


def test_unnamed_object_is_keyed_by_its_owner(_load) -> None:
    parent, child = _load(), _load()
    sizing = child.getSizingSystems()[0]
    sizing.setDesignOutdoorAirFlowRate(0.5)

    df = diff_models(parent, child)

    assert df.family.tolist() == ["sizing_system"]
    assert df.key.tolist() == [sizing.airLoopHVAC().nameString()]


def test_topology_is_left_out_unless_asked(_load) -> None:
    parent, child = _load(), _load()
    child.getNodes()[0].setName("Renamed node")

    assert diff_models(parent, child).empty
    with_topology = diff_models(parent, child, include_topology=True)
    assert set(with_topology.family) <= TOPOLOGY_TYPES and not with_topology.empty


def test_family_filter_keeps_rows_but_matches_everything(_load) -> None:
    parent, child = _load(), _load()
    child.getLightsDefinitions()[0].setWattsperSpaceFloorArea(99.0)
    child.getSizingSystems()[0].setDesignOutdoorAirFlowRate(0.5)

    assert diff_models(parent, child, families=["sizing_system"]).family.tolist() == ["sizing_system"]
    assert diff_models(parent, child, families=["OS:Fan:VariableVolume"]).empty
    with pytest.raises(ValueError, match="lightz"):
        diff_models(parent, child, families=["lightz"])


def test_removed_target_shows_as_a_lost_reference(_load) -> None:
    """A reference whose target was removed is a change, even though the child field is empty.

    Real case: East Gate model-basis 001 -> 010, the space type "ChangingRoom" lost its outdoor air.
    """
    parent, child = _load(), _load()
    space_type = child.getSpaceTypes()[0]
    oa = space_type.designSpecificationOutdoorAir()
    if not oa.is_initialized():
        pytest.skip("fixture space type has no outdoor air object")
    oa_name = oa.get().nameString()
    oa.get().remove()

    df = diff_models(parent, child)

    assert (
        "space_type",
        space_type.nameString(),
        "Design Specification Outdoor Air Object Name",
        oa_name,
        None,
    ) in _rows(df, "changed")


def test_translated_model_reports_objects_created_on_load() -> None:
    df = diff_models(_translate(SMALL_OFFICE), _translate(SMALL_OFFICE))

    assert sorted(df.status) == ["added", "removed"]
    assert set(df.family) == {"OS:WaterHeater:Sizing"}


def test_diff_survives_orphan_relations() -> None:
    code = (
        "import sys, openstudio\n"
        "from openstudio_toolkit.analysis.diff import diff_models\n"
        "load = lambda: openstudio.osversion.VersionTranslator().loadModel(sys.argv[1]).get()\n"
        "print(len(diff_models(load(), load())))\n"
    )
    proc = subprocess.run(
        [sys.executable, "-I", "-c", code, str(ORPHAN_FIXTURE)], capture_output=True, text=True, timeout=300
    )

    assert proc.returncode == 0, f"return code {proc.returncode}: {proc.stderr[-2000:]}"
    assert proc.stdout.split()[-1] == "0"
