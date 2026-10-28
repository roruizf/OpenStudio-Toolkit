# Usage: python results_fpm4_check.py <run folder with fpm4-final-{baseline,proposed}/run/eplusout.sql>
"""Item 8 on FPM4 v10: every number of the four results against the SQL, as numbers.

Sizes: each value equals ZoneSizes/SystemSizes exactly, and rounds to the tabular report (eplustbl.htm)
within half its last printed digit. Unmet hours and end uses: each value equals the tabular string as a
float. Units: m3/s -> m3/h and GJ -> kWh are the value times the exact factor. The file is unchanged.
"""
import hashlib
import sqlite3
import sys
from pathlib import Path

from openstudio_toolkit.results import UNIT_FACTORS, end_uses, system_sizes, unmet_hours, zone_sizes

root = Path(sys.argv[1])
for side in ("baseline", "proposed"):
    sql = root / f"fpm4-final-{side}" / "run" / "eplusout.sql"
    digest = hashlib.sha256(sql.read_bytes()).hexdigest()
    con = sqlite3.connect(f"{sql.resolve().as_uri()}?mode=ro", uri=True)
    tab = {}
    for rep, t, r, c, u, v in con.execute("SELECT ReportName, TableName, RowName, ColumnName, Units, Value FROM TabularDataWithStrings WHERE ReportForString='Entire Facility'"):
        tab[(rep, t, r, c)] = v
    bad = checked = 0

    def near(value, text):
        global bad, checked
        text = text.strip()
        decimals = len(text.split(".")[1]) if "." in text else 0
        checked += 1
        if abs(value - float(text)) > 0.5 * 10 ** -decimals + 1e-12:
            bad += 1; print("  BAD", value, text)

    z = zone_sizes(sql)
    raw = con.execute("SELECT ZoneName, LoadType, CalcDesLoad, UserDesLoad, CalcDesFlow, UserDesFlow FROM ZoneSizes ORDER BY ZoneSizesIndex").fetchall()
    assert [tuple(r) for r in z.select(z.columns[:6]).rows()] == raw
    for r in z.iter_rows(named=True):
        t = f"Zone Sensible {r['Load Type']}"
        near(r["Calculated Design Load {W}"], tab[("HVACSizingSummary", t, r["Zone"], "Calculated Design Load")])
        near(r["User Design Air Flow {m3/s}"], tab[("HVACSizingSummary", t, r["Zone"], "User Design Air Flow")])
        near(r["Minimum Outdoor Air Flow Rate {m3/s}"], tab[("HVACSizingSummary", t, r["Zone"], "Minimum Outdoor Air Flow Rate")])
        near(r["Outdoor Temperature at Peak Load {C}"], tab[("HVACSizingSummary", t, r["Zone"], "Outdoor Temperature at Peak Load")])
    s = system_sizes(sql)
    for r in s.iter_rows(named=True):
        mode = r["Load Type"].lower()
        near(r["Calculated Design Air Flow {m3/s}"], tab[("HVACSizingSummary", "System Design Air Flow Rates", r["System"], f"Calculated {mode}")])
        near(r["User Design Air Flow {m3/s}"], tab[("HVACSizingSummary", "System Design Air Flow Rates", r["System"], f"User {mode}")])
    for df, rep, t, first in ((unmet_hours(sql), "SystemSummary", "Time Setpoint Not Met", "Zone"),
                              (end_uses(sql), "AnnualBuildingUtilityPerformanceSummary", "End Uses", "End Use")):
        for r in df.iter_rows(named=True):
            for col, v in r.items():
                if col == first: continue
                text = tab[(rep, t, r[first], col.split(" {")[0])].strip()
                checked += 1
                if (v is None) != (text == "") or (v is not None and v != float(text)):
                    bad += 1; print("  BAD", r[first], col, v, text)
    zh = zone_sizes(sql, units={"m3/s": "m3/h"}); eu = end_uses(sql, units={"GJ": "kWh"}); e = end_uses(sql)
    assert (zh["User Design Air Flow {m3/h}"] == z["User Design Air Flow {m3/s}"] * UNIT_FACTORS[("m3/s", "m3/h")]).all()
    assert (eu["Electricity {kWh}"] == e["Electricity {GJ}"] * UNIT_FACTORS[("GJ", "kWh")]).all()
    arr = zh.filter((zh["Zone"] == "TZ-FPM4-N00.04-ARRUMOS") & (zh["Load Type"] == "Cooling"))["User Design Air Flow {m3/h}"]
    arr = arr[0] if len(arr) else float("nan")  # the zone exists in proposed only
    total = eu.filter(eu["End Use"] == "Total End Uses")["Electricity {kWh}"][0]
    u = unmet_hours(sql)
    facility = u.filter(u["Zone"] == "Facility")
    print(f"{side}: zones {z['Zone'].n_unique()} ({len(z)} rows), systems {s['System'].n_unique()} ({len(s)} rows), "
          f"unmet rows {len(unmet_hours(sql))}, end uses {len(e)}; checked {checked}, bad {bad}; "
          f"ARRUMOS cooling user flow {arr:.4f} m3/h; total electricity {total:,.0f} kWh; "
          f"facility occupied heating/cooling {facility['During Occupied Heating {hr}'][0]}/{facility['During Occupied Cooling {hr}'][0]} h; "
          f"file unchanged {hashlib.sha256(sql.read_bytes()).hexdigest() == digest}")
