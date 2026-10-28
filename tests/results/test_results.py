"""Item 8: results from eplusout.sql (synthetic SQL with EnergyPlus's own table layout; names invented)."""

from __future__ import annotations

import hashlib
import sqlite3
from pathlib import Path

import polars as pl
import pytest

from openstudio_toolkit.results import UNIT_FACTORS, end_uses, system_sizes, unmet_hours, zone_sizes

ZONE_SIZES = (
    "CREATE TABLE ZoneSizes ( ZoneSizesIndex INTEGER PRIMARY KEY, ZoneName TEXT, LoadType TEXT, CalcDesLoad REAL, "
    "UserDesLoad REAL, CalcDesFlow REAL, UserDesFlow REAL, DesDayName TEXT, PeakHrMin TEXT, PeakTemp REAL, "
    "PeakHumRat REAL, CalcOutsideAirFlow REAL, DOASHeatAddRate REAL)"
)
SYSTEM_SIZES = (
    "CREATE TABLE SystemSizes (SystemSizesIndex INTEGER PRIMARY KEY, SystemName TEXT, LoadType TEXT, "
    "PeakLoadType TEXT, UserDesCap REAL, CalcDesVolFlow REAL, UserDesVolFlow REAL, DesDayName TEXT, PeakHrMin TEXT)"
)
# The real TabularDataWithStrings is a view over TabularData and Strings; its columns are these.
TABULAR = (
    "CREATE TABLE TabularDataWithStrings (TabularDataIndex INTEGER PRIMARY KEY, Value TEXT, ReportName TEXT, "
    "ReportForString TEXT, TableName TEXT, RowName TEXT, ColumnName TEXT, Units TEXT)"
)
FLOW = 30 / 3600  # a zone sized for 30 m3/h; the tabular report prints it as 0.008 m3/s


def _sql(path: Path, energy_unit: str = "GJ") -> Path:
    con = sqlite3.connect(path)
    con.execute(ZONE_SIZES)
    con.execute(SYSTEM_SIZES)
    con.execute(TABULAR)
    con.executemany(
        "INSERT INTO ZoneSizes VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
        [
            (1, "ZONE B", "Cooling", 1500.25, 1725.3, 0.1, FLOW, "CLG DAY", "7/21 15:00:00", 33.1, 0.011, FLOW, 0.0),
            (2, "ZONE B", "Heating", 900.5, 1125.6, 0.05, FLOW, "HTG DAY", "1/21 07:00:00", -2.0, 0.002, FLOW, -12.5),
            (3, "ZONE A", "Cooling", 10.0, 11.5, 0.001, 0.002, "CLG DAY", "7/21 16:00:00", 33.1, 0.011, 0.002, 0.0),
        ],
    )
    con.executemany(
        "INSERT INTO SystemSizes VALUES (?,?,?,?,?,?,?,?,?)",
        [
            (1, "AHU 1", "Cooling", "Sensible", 33592.76, 8.4617, 5.2597222, "CLG DAY", "8/21 15:00:00"),
            (2, "AHU 1", "Heating", "Sensible", 109631.9, 6.9069, 5.2597222, "HTG DAY", "1/21 00:10:00"),
        ],
    )
    cells = []
    unmet = (("ZONE B", "17.33", "2.83"), ("ZONE A", "0.00", "0.50"), ("Facility", "17.33", "3.33"))
    for zone, heating, cooling in unmet:
        cells += [
            ("SystemSummary", "Time Setpoint Not Met", zone, "During Heating", "hr", heating),
            ("SystemSummary", "Time Setpoint Not Met", zone, "During Cooling", "hr", cooling),
        ]
    for fuel in ("Electricity", "Natural Gas"):
        for use, value in (("Heating", "16.88"), ("Fans", "360.82"), ("", ""), ("Total End Uses", "377.70")):
            value = value if fuel == "Electricity" or use in ("Heating", "") else "0.00"
            cells.append(("AnnualBuildingUtilityPerformanceSummary", "End Uses", use, fuel, energy_unit, f"   {value}"))
    cells.append(("AnnualBuildingUtilityPerformanceSummary", "End Uses", "Fans", "Water", "m3", ""))
    con.executemany(
        "INSERT INTO TabularDataWithStrings (Value, ReportName, ReportForString, TableName, RowName, ColumnName, "
        "Units) VALUES (?, ?, 'Entire Facility', ?, ?, ?, ?)",
        [(v, r, t, row, c, u) for r, t, row, c, u, v in cells],
    )
    con.commit()
    con.close()
    return path


@pytest.fixture
def sql(tmp_path) -> Path:
    return _sql(tmp_path / "eplusout.sql")


def test_zone_sizes_keep_full_precision_and_order(sql) -> None:
    df = zone_sizes(sql)
    assert df["Zone"].to_list() == ["ZONE B", "ZONE B", "ZONE A"]  # SQL order, names as EnergyPlus writes them
    assert df["Load Type"].to_list() == ["Cooling", "Heating", "Cooling"]
    assert df["User Design Air Flow {m3/s}"][0] == FLOW
    assert df.schema["Calculated Design Load {W}"] == pl.Float64 and df.schema["Design Day Name"] == pl.String
    in_m3h = zone_sizes(sql, units={"m3/s": "m3/h", "W": "kW"})
    assert in_m3h["User Design Air Flow {m3/h}"][0] == pytest.approx(30.0, abs=1e-12)
    assert in_m3h["Calculated Design Load {kW}"][0] == pytest.approx(1.50025)
    assert "Outdoor Temperature at Peak Load {C}" in in_m3h.columns  # untouched units keep their name


def test_system_sizes(sql) -> None:
    df = system_sizes(sql, units={"m3/s": "L/s"})
    assert df["System"].to_list() == ["AHU 1", "AHU 1"]
    assert df["User Design Air Flow {L/s}"][0] == pytest.approx(5259.7222)
    assert df["User Design Capacity {W}"][1] == 109631.9


def test_unmet_hours_one_row_per_zone_plus_facility(sql) -> None:
    df = unmet_hours(sql)
    assert df.columns == ["Zone", "During Heating {hr}", "During Cooling {hr}"]
    assert df["Zone"].to_list() == ["ZONE B", "ZONE A", "Facility"]
    assert df.filter(pl.col("Zone") == "Facility")["During Cooling {hr}"][0] == 3.33


def test_end_uses_drop_the_separator_row_and_convert(sql) -> None:
    df = end_uses(sql)
    assert df["End Use"].to_list() == ["Heating", "Fans", "Total End Uses"]
    assert df.columns == ["End Use", "Electricity {GJ}", "Natural Gas {GJ}", "Water {m3}"]
    assert df["Water {m3}"].to_list() == [None, None, None]  # empty cells are null, not 0
    kwh = end_uses(sql, units={"GJ": "kWh"})
    assert kwh["Electricity {kWh}"].to_list() == [v * UNIT_FACTORS[("GJ", "kWh")] for v in df["Electricity {GJ}"]]
    assert kwh["Electricity {kWh}"][2] == pytest.approx(104916.67, abs=0.01)


def test_ip_file_keeps_its_units_and_refuses_a_si_conversion(tmp_path) -> None:
    sql = _sql(tmp_path / "ip.sql", energy_unit="kBtu")
    assert "Electricity {kBtu}" in end_uses(sql).columns
    with pytest.raises(ValueError, match="units not in this result: GJ"):
        end_uses(sql, units={"GJ": "kWh"})


def test_bad_conversion_and_missing_file(sql, tmp_path) -> None:
    with pytest.raises(ValueError, match="unsupported conversions: m3/s -> cfm"):
        zone_sizes(sql, units={"m3/s": "cfm"})
    with pytest.raises(FileNotFoundError):
        zone_sizes(tmp_path / "none.sql")


def test_sql_is_opened_read_only(sql) -> None:
    before = hashlib.sha256(sql.read_bytes()).hexdigest()
    for read in (zone_sizes, system_sizes, unmet_hours, end_uses):
        read(sql)
    assert hashlib.sha256(sql.read_bytes()).hexdigest() == before
    con = sqlite3.connect(f"{sql.resolve().as_uri()}?mode=ro", uri=True)
    with pytest.raises(sqlite3.OperationalError, match="readonly"):
        con.execute("DELETE FROM ZoneSizes")
    con.close()
