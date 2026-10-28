"""Item 7, visible form: the HTML report shows the rows as they are, with locations and languages."""

from __future__ import annotations

import re
from html import unescape
from pathlib import Path

import openstudio
import pytest

from openstudio_toolkit.views.verification import ReportPair, compare_rows, diff_rows, write_report

M = openstudio.model


def _load(path: Path):
    return openstudio.osversion.VersionTranslator().loadModel(str(path)).get()


def _space(model, x: float, name: str, zone_name: str):
    points = [openstudio.Point3d(x, 0, 0), openstudio.Point3d(x, 10, 0)]
    points += [openstudio.Point3d(x + 10, 10, 0), openstudio.Point3d(x + 10, 0, 0)]
    space = M.Space.fromFloorPrint(openstudio.Point3dVector(points), 3, model).get()
    space.setName(name)
    zone = M.ThermalZone(model)
    zone.setName(zone_name)
    space.setThermalZone(zone)
    return space, zone


def _lights(model, name: str, space, level: float):
    definition = M.LightsDefinition(model)
    definition.setName(f"{name} Definition")
    definition.setLightingLevel(level)
    lights = M.Lights(definition)
    lights.setName(name)
    lights.setSpace(space)
    return lights


@pytest.fixture(scope="module")
def pair(tmp_path_factory) -> tuple[Path, Path]:
    """Parent: Spaces A (zone ZA) and B (zone ZB), one light each, an air loop with no terminals.

    Child: light A 100 -> 120 W; one schedule "Shared Sched" added and used by both lights; a terminal
    "Terminal ZA" added, serving ZA from the air loop (it belongs to the zone and to the loop).
    """
    model = M.Model()
    a, za = _space(model, 0, "A", "ZA")
    b, _ = _space(model, 20, "B", "ZB")
    _lights(model, "LA", a, 100.0)
    _lights(model, "LB", b, 50.0)
    M.AirLoopHVAC(model).setName("Loop 1")
    folder = tmp_path_factory.mktemp("report")
    parent = folder / "parent.osm"
    assert model.save(str(parent), True)

    model = _load(parent)
    model.getLightsDefinitionByName("LA Definition").get().setLightingLevel(120.0)
    schedule = M.ScheduleConstant(model)
    schedule.setName("Shared Sched")
    for name in ("LA", "LB"):
        model.getLightsByName(name).get().setSchedule(schedule)
    terminal = M.AirTerminalSingleDuctConstantVolumeNoReheat(model, model.alwaysOnDiscreteSchedule())
    terminal.setName("Terminal ZA")
    model.getAirLoopHVACByName("Loop 1").get().addBranchForZone(model.getThermalZoneByName("ZA").get(), terminal)
    child = folder / "child.osm"
    assert model.save(str(child), True)
    return parent, child


@pytest.fixture(scope="module")
def page(pair, tmp_path_factory) -> str:
    parent, child = pair
    report = ReportPair(
        _load(parent),
        _load(child),
        {"lights": {"A": 120.0, "B": 50.4}},
        parent_name="parent.osm",
        child_name="child.osm",
        mapping_name="test mapping",
        tolerance=0.5,
    )
    out = write_report([report], tmp_path_factory.mktemp("html") / "report.html")
    return out.read_text(encoding="utf-8")


def _row(page: str, family: str, key: str) -> list[tuple[str, str]]:
    for tr in re.findall(rf'<tr data-status="[^"]+" data-family="{re.escape(family)}">(.*?)</tr>', page):
        cells = re.findall(r"<td([^>]*)>(.*?)</td>", tr)
        if unescape(re.sub("<[^>]+>", "", cells[1][1])) == key:
            return cells
    raise AssertionError(f"no row {family} {key}")


def _place(cell: tuple[str, str]) -> str:
    found = re.search(r'data-place="([^"]*)"', cell[0])
    return unescape(found.group(1)) if found else ""


def test_every_compare_number_equals_its_row(pair, page: str) -> None:
    """Numbers are checked as numbers (data-v carries the exact float, the text is rounded to 0.01)."""
    rows = compare_rows(_load(pair[1]), {"lights": {"A": 120.0, "B": 50.4}}, tolerance=0.5)
    assert rows.status.tolist() == ["match", "match"]  # B: 50 W in the model, 0.4 W off, within 0.5 W
    for r in rows.itertuples(index=False):
        cells = _row(page, "OS:Lights", r.key)
        for cell, value in zip(cells[3:6], (r.requested, r.in_model, r.difference), strict=True):
            assert float(re.search(r'data-v="([^"]+)"', cell[0]).group(1)) == value
            assert abs(float(cell[1].replace(",", "")) - value) <= 0.005


def test_every_diff_row_is_shown_once(pair, page: str) -> None:
    parent, child = pair
    rows = diff_rows(_load(parent), _load(child), {"lights": {"A": 120.0, "B": 50.4}})
    shown = re.findall(r'<tr data-status="(changed|added|removed|not_requested)"', page)
    assert sorted(shown) == sorted(rows.status)


def test_shared_object_lists_every_place(page: str) -> None:
    cells = _row(page, "OS:Schedule:Constant", "Shared Sched")
    assert [_place(c) for c in cells[7:]] == ["A | B", "ZA | ZB", ""]
    assert "shared (used by 2)" in cells[7][1]


def test_object_with_two_owners_fills_both_columns(page: str) -> None:
    cells = _row(page, "OS:AirTerminal:SingleDuct:ConstantVolume:NoReheat", "Terminal ZA")
    assert [_place(c) for c in cells[7:]] == ["", "ZA", "Loop 1"]


def test_report_header_family_and_sections(page: str) -> None:
    assert "<b>0.5</b>" in page  # tolerance in the header
    assert 'data-family="lights"' not in page  # the OpenStudio type is shown, not the dump name
    assert 'data-t="part.zone"' in page and 'data-t="part.schedules"' in page
    assert "<details open" in page and 'select data-filter="status"' in page


def test_language_is_selectable_and_openstudio_terms_stay_english(pair, tmp_path) -> None:
    parent, child = pair
    report = ReportPair(_load(parent), _load(child), {"lights": {"A": 120.0}})
    page = write_report([report], tmp_path / "es.html", language="es").read_text(encoding="utf-8")
    assert '<html lang="es">' in page
    assert "Informe de verificación" in page and "coincide" in page
    assert "<code>OS:Lights</code>" in page and "<th>Space</th>" in page
    with pytest.raises(ValueError, match="language"):
        write_report([report], tmp_path / "de.html", language="de")
    with pytest.raises(ValueError, match="pairs"):
        write_report([], tmp_path / "none.html")
