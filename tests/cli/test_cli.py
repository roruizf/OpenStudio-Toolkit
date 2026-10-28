"""Item 9: the command line, its outputs and exit codes (0 match, 1 does not match or refused, 2 usage)."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import openstudio
import pandas as pd
import pytest

from openstudio_toolkit.cli import COMMANDS, main

M = openstudio.model


def _space(model, x: float, name: str):
    points = [openstudio.Point3d(x, 0, 0), openstudio.Point3d(x, 10, 0)]
    points += [openstudio.Point3d(x + 10, 10, 0), openstudio.Point3d(x + 10, 0, 0)]
    space = M.Space.fromFloorPrint(openstudio.Point3dVector(points), 3, model).get()
    space.setName(name)
    return space


@pytest.fixture
def files(tmp_path) -> dict[str, Path]:
    """parent.osm: Spaces A (light 100 W) and B (no load); g37.json asks A 120 W, B 50 W."""
    model = M.Model()
    definition = M.LightsDefinition(model)
    definition.setName("LA Definition")
    definition.setLightingLevel(100.0)
    light = M.Lights(definition)
    light.setName("LA")
    light.setSpace(_space(model, 0, "A"))
    _space(model, 20, "B")
    parent = tmp_path / "parent.osm"
    assert model.save(str(parent), True)
    mapping = tmp_path / "g37.json"
    mapping.write_text(json.dumps({"lights": {"A": 120.0, "B": 50.0}}), encoding="utf-8")
    return {"parent": parent, "mapping": mapping, "dir": tmp_path}


def test_commands_are_the_contract() -> None:
    assert COMMANDS == ("dump", "apply", "compare", "diff", "results")


def test_verification_flow(files, capsys) -> None:
    parent, mapping, folder = files["parent"], str(files["mapping"]), files["dir"]
    child = folder / "child.osm"

    assert main(["compare", str(parent), "--mapping", mapping]) == 1  # A has 100 W, B nothing
    assert main(["apply", str(parent), str(child), "--mapping", mapping]) == 1  # A already has a light
    assert "--existing update" in capsys.readouterr().err
    assert not child.exists()

    assert main(["apply", str(parent), str(child), "--mapping", mapping, "--existing", "update"]) == 0
    assert "1 created, 1 updated" in capsys.readouterr().out
    assert main(["compare", str(child), "--mapping", mapping, "--out", str(folder / "c.csv")]) == 0
    assert pd.read_csv(folder / "c.csv").status.tolist() == ["match", "match"]

    report = folder / "report.html"
    code = main(["diff", str(parent), str(child), "--mapping", mapping, "--report", str(report), "--language", "es",
                 "--out", str(folder / "d.csv")])
    out = capsys.readouterr().out
    assert code == 0 and "child vs mapping: 2 match" in out
    assert '<html lang="es">' in report.read_text(encoding="utf-8")
    assert {"changed", "added"} <= set(pd.read_csv(folder / "d.csv").status)


def test_diff_without_mapping_reports_everything_as_not_requested(files, capsys) -> None:
    child = files["dir"] / "child.osm"
    assert main(["apply", str(files["parent"]), str(child), "--mapping", str(files["mapping"]), "--existing",
                 "update"]) == 0
    assert main(["diff", str(files["parent"]), str(child)]) == 0
    assert "not_requested" in capsys.readouterr().out


def test_dump_writes_one_csv_per_family(files) -> None:
    out = files["dir"] / "dump"
    assert main(["dump", str(files["parent"]), "--families", "lights,space", "--out", str(out)]) == 0
    assert sorted(p.name for p in out.iterdir()) == ["lights.csv", "space.csv"]
    assert pd.read_csv(out / "lights.csv").Name.tolist() == ["LA"]


def test_results_with_units(tmp_path, capsys) -> None:
    sql = tmp_path / "eplusout.sql"
    con = sqlite3.connect(sql)
    con.execute(
        "CREATE TABLE TabularDataWithStrings (TabularDataIndex INTEGER PRIMARY KEY, Value TEXT, ReportName TEXT, "
        "ReportForString TEXT, TableName TEXT, RowName TEXT, ColumnName TEXT, Units TEXT)"
    )
    con.execute(
        "INSERT INTO TabularDataWithStrings (Value, ReportName, ReportForString, TableName, RowName, ColumnName, "
        "Units) VALUES ('  3.60', 'AnnualBuildingUtilityPerformanceSummary', 'Entire Facility', 'End Uses', "
        "'Fans', 'Electricity', 'GJ')"
    )
    con.commit()
    con.close()
    assert main(["results", str(sql), "end_uses", "--units", "GJ=kWh"]) == 0
    assert capsys.readouterr().out.splitlines() == ["End Use,Electricity {kWh}", "Fans,1000.0"]
    assert main(["results", str(sql), "end_uses", "--units", "GJ"]) == 2
    assert main(["results", str(sql), "end_uses", "--units", "GJ=cfm"]) == 2


@pytest.mark.parametrize(
    "argv",
    [
        ["compare", "missing.osm", "--mapping", "m.json"],
        ["results", "missing.sql", "end_uses"],
        ["dump", "PARENT", "--families", "lighting", "--out", "x"],
        ["compare", "PARENT", "--mapping", "BAD"],
        ["apply", "PARENT", "PARENT", "--mapping", "MAPPING"],
    ],
)
def test_usage_errors_exit_2(files, argv, capsys) -> None:
    bad = files["dir"] / "bad.json"
    bad.write_text('{"lights": {"A": "120"}}', encoding="utf-8")
    names = {"PARENT": str(files["parent"]), "MAPPING": str(files["mapping"]), "BAD": str(bad)}
    assert main([names.get(a, a) for a in argv]) == 2
    assert capsys.readouterr().err.startswith("openstudio-toolkit ")
