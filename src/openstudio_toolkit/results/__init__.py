"""Simulation results from an EnergyPlus ``eplusout.sql``, as polars DataFrames (item 8).

Approved by Roberto (2026-10-28, "ok 8", then "ok" to the unit option and the full-precision source):

- The SQL is opened read-only (``sqlite3``, ``mode=ro``); nothing in this package can write to it.
- Zone and system sizes come from the SQL tables ``ZoneSizes`` and ``SystemSizes``, which keep full
  precision. The tabular report (the numbers of ``eplustbl.htm``) is rounded: on FPM4 v10 proposed,
  zone ``TZ-FPM4-N00.04-ARRUMOS`` has a user design air flow of 0.008 m3/s there (28.8 m3/h) and
  0.0083333 m3/s in ``ZoneSizes`` (30.0 m3/h). These two tables hold SI values.
- Unmet hours and end uses exist only in the tabular report; their units are read from the SQL's own
  ``Units`` column, so a file written in IP units gets IP column names.
- Names as EnergyPlus writes them (upper case); every unit is in its column name, e.g.
  ``User Design Air Flow {m3/s}``.
- ``units`` converts at extraction, from the full value, with exact factors (``UNIT_FACTORS``), e.g.
  ``{"GJ": "kWh"}`` or ``{"m3/s": "m3/h", "W": "kW"}``. Without it, the numbers are EnergyPlus's. A
  conversion that is not in the table, or a unit that is not in the result (an IP file asked for
  ``GJ``), is an error rather than a guess.

polars is imported only under ``results/`` (contract boundary); model views stay in pandas.
"""

from __future__ import annotations

import re
import sqlite3
from collections.abc import Mapping
from contextlib import closing
from pathlib import Path

import polars as pl

UNIT_FACTORS: Mapping[tuple[str, str], float] = {
    ("GJ", "kWh"): 1e9 / 3.6e6,
    ("GJ", "MWh"): 1e9 / 3.6e9,
    ("GJ", "MJ"): 1e3,
    ("m3/s", "m3/h"): 3600.0,
    ("m3/s", "L/s"): 1e3,
    ("W", "kW"): 1e-3,
}

_ZONE_SIZES = (
    ("ZoneName", "Zone"),
    ("LoadType", "Load Type"),
    ("CalcDesLoad", "Calculated Design Load {W}"),
    ("UserDesLoad", "User Design Load {W}"),
    ("CalcDesFlow", "Calculated Design Air Flow {m3/s}"),
    ("UserDesFlow", "User Design Air Flow {m3/s}"),
    ("DesDayName", "Design Day Name"),
    ("PeakHrMin", "Date/Time Of Peak"),
    ("PeakTemp", "Outdoor Temperature at Peak Load {C}"),
    ("PeakHumRat", "Outdoor Humidity Ratio at Peak Load {kgWater/kgDryAir}"),
    ("CalcOutsideAirFlow", "Minimum Outdoor Air Flow Rate {m3/s}"),
    ("DOASHeatAddRate", "Heat Gain Rate from DOAS {W}"),
)
_SYSTEM_SIZES = (
    ("SystemName", "System"),
    ("LoadType", "Load Type"),
    ("PeakLoadType", "Peak Load Type"),
    ("UserDesCap", "User Design Capacity {W}"),
    ("CalcDesVolFlow", "Calculated Design Air Flow {m3/s}"),
    ("UserDesVolFlow", "User Design Air Flow {m3/s}"),
    ("DesDayName", "Design Day Name"),
    ("PeakHrMin", "Date/Time Of Peak"),
)
_UNIT = re.compile(r"^(.*) \{(.+)\}$")
_TEXT = {"Zone", "System", "Load Type", "Peak Load Type", "Design Day Name", "Date/Time Of Peak"}


def _connect(sql: str | Path) -> sqlite3.Connection:
    path = Path(sql).resolve()
    if not path.is_file():
        raise FileNotFoundError(path)
    return sqlite3.connect(f"{path.as_uri()}?mode=ro", uri=True)


def _convert(df: pl.DataFrame, units: Mapping[str, str] | None) -> pl.DataFrame:
    if not units:
        return df
    unsupported = [f"{a} -> {b}" for a, b in units.items() if (a, b) not in UNIT_FACTORS]
    if unsupported:
        known = ", ".join(f"{a} -> {b}" for a, b in UNIT_FACTORS)
        raise ValueError(f"unsupported conversions: {', '.join(unsupported)} (supported: {known})")
    present = {m.group(2) for c in df.columns if (m := _UNIT.match(c))}
    absent = sorted(set(units) - present)
    if absent:
        raise ValueError(f"units not in this result: {', '.join(absent)} (present: {', '.join(sorted(present))})")
    renamed = {}
    for column in df.columns:
        match = _UNIT.match(column)
        if match and match.group(2) in units:
            target = units[match.group(2)]
            df = df.with_columns(pl.col(column) * UNIT_FACTORS[(match.group(2), target)])
            renamed[column] = f"{match.group(1)} {{{target}}}"
    return df.rename(renamed)


def _sizes(sql: str | Path, table: str, key: str, columns: tuple[tuple[str, str], ...]) -> pl.DataFrame:
    with closing(_connect(sql)) as con:
        rows = con.execute(f"SELECT {', '.join(c for c, _ in columns)} FROM {table} ORDER BY {key}").fetchall()
    schema = {name: (pl.String if name in _TEXT else pl.Float64) for _, name in columns}
    return pl.DataFrame(rows, schema=schema, orient="row")



def _number(value: str) -> float | None:
    text = value.strip()
    return float(text) if text else None


def _tabular(sql: str | Path, report: str, table: str, first: str) -> pl.DataFrame:
    """One row per RowName (in report order), one Float64 column per ColumnName with its SQL unit."""
    with closing(_connect(sql)) as con:
        cells = con.execute(
            "SELECT RowName, ColumnName, Units, Value FROM TabularDataWithStrings "
            "WHERE ReportName = ? AND TableName = ? AND ReportForString = 'Entire Facility' "
            "ORDER BY TabularDataIndex",
            (report, table),
        ).fetchall()
    rows: dict[str, dict[str, float | None]] = {}
    columns: dict[str, None] = {}
    for row, column, unit, value in cells:
        name = f"{column} {{{unit}}}" if unit else column
        columns[name] = None
        rows.setdefault(row, {})[name] = _number(value)
    # EnergyPlus puts an unnamed, empty separator row before the totals.
    rows = {k: v for k, v in rows.items() if k.strip() or any(x is not None for x in v.values())}
    schema = {first: pl.String, **{c: pl.Float64 for c in columns}}
    data = [[name, *(values.get(c) for c in columns)] for name, values in rows.items()]
    return pl.DataFrame(data, schema=schema, orient="row")


def zone_sizes(sql: str | Path, units: Mapping[str, str] | None = None) -> pl.DataFrame:
    """One row per Thermal Zone and load type (Cooling, Heating), from ``ZoneSizes``."""
    return _convert(_sizes(sql, "ZoneSizes", "ZoneSizesIndex", _ZONE_SIZES), units)


def system_sizes(sql: str | Path, units: Mapping[str, str] | None = None) -> pl.DataFrame:
    """One row per air loop and load type (Cooling, Heating), from ``SystemSizes``."""
    return _convert(_sizes(sql, "SystemSizes", "SystemSizesIndex", _SYSTEM_SIZES), units)


def unmet_hours(sql: str | Path, units: Mapping[str, str] | None = None) -> pl.DataFrame:
    """Time setpoint not met, one row per zone plus ``Facility`` (SystemSummary, Time Setpoint Not Met)."""
    return _convert(_tabular(sql, "SystemSummary", "Time Setpoint Not Met", "Zone"), units)


def end_uses(sql: str | Path, units: Mapping[str, str] | None = None) -> pl.DataFrame:
    """One row per end use (``Total End Uses`` last), one column per fuel (AnnualBuildingUtilityPerformanceSummary)."""
    return _convert(_tabular(sql, "AnnualBuildingUtilityPerformanceSummary", "End Uses", "End Use"), units)


__all__ = ["UNIT_FACTORS", "end_uses", "system_sizes", "unmet_hours", "zone_sizes"]
