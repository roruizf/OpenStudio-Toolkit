"""Item 3b: every cell of the 8 new views against the stored record, as numbers."""
import re, sys
from collections import Counter
import openstudio
from openstudio_toolkit import dump
from openstudio_toolkit.extractors.generic import read_model_objects
FAMS = ["thermostat_setpoint_dual_setpoint","window_material_simple_glazing_system","fan_variable_volume","pump_constant_speed",
        "cooling_tower_two_speed","cooling_tower_variable_speed","boiler_hot_water","zone_hvac_ideal_loads_air_system","pump_variable_speed",
        "fan_constant_volume","fan_on_off"]
def strip_units(c): return re.sub(r"\s*\{.*\}$", "", c)
for path in sys.argv[1:]:
    m = openstudio.osversion.VersionTranslator().loadModel(path).get()
    recs = {r.handle: r for r in read_model_objects(m)}
    views = dump.dump_view(m, FAMS)
    tally = Counter(); notes = Counter()
    for fam, df in views.items():
        for row in df.to_dict("records"):
            r = recs[row["Handle"]]
            fields = {f.name: f for f in r.fields}
            for col, cell in row.items():
                if col in ("Handle",): continue
                f = fields.get(strip_units(col))
                if f is None: notes[(fam, col, "no IDD field")] += 1; continue
                v = f.value
                if f.target is not None:
                    t = recs.get(f.target)
                    exp = t.name if t else None
                    if t is not None and t.idd_type == "OS:Connection":
                        tf = {g.name: g for g in t.fields}
                        exp = next((recs[tf[h].target].name for h in ("Source Object","Target Object") if tf[h].target in recs and recs[tf[h].target].idd_type=="OS:Node"), None)
                    ok = cell == exp; kind = "relation"
                elif v in (None, ""):
                    ok = None; kind = "empty->default"
                    if cell is not None: notes[(fam, col, f"empty stored, view={cell!r}")] += 1
                elif isinstance(cell, str) and cell == "Autosize":
                    ok = v.lower() in ("autosize", "autocalculate"); kind = "autosize"
                elif isinstance(cell, (int, float)) and not isinstance(cell, bool):
                    ok = float(v) == float(cell); kind = "number"
                else:
                    ok = str(cell) == v or str(cell).lower() == v.lower(); kind = "text"
                    if ok and str(cell) != v: notes[(fam, col, f"case {v!r}->{cell!r}")] += 1
                tally[(kind, ok)] += 1
                if ok is False: print("BAD", fam, row["Name"], col, repr(v), repr(cell), type(cell).__name__)
    print("==", path.split("/")[-1], {k: len(v) for k, v in views.items() if len(v)})
    print("  ", dict(tally))
    for k, n in sorted(notes.items()): print("   note", n, k)
