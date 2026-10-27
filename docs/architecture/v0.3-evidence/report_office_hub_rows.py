# Usage: python report_office_hub_rows.py <dir with models/r2f-office-hub-ene01-{actual-017,reference-011}.osm>; writes <dir>/data.pkl
"""Office Hub actual-017 -> reference-011, lighting mapping from Table G3.7 (ENE01-REFERENCE-MODEL-SPEC §5) x floor area."""
import sys, openstudio
from openstudio_toolkit.views.verification import compare_rows, diff_rows
S = sys.argv[1]
load = lambda p: openstudio.osversion.VersionTranslator().loadModel(p).get()
actual = load(f"{S}/models/r2f-office-hub-ene01-actual-017.osm")
ref = load(f"{S}/models/r2f-office-hub-ene01-reference-011.osm")
G37 = {"Office": 11.84, "MeetingRoom": 13.99, "Circulations": 5.38, "BreakRoom": 12.92,
       "Storage": 8.61, "WC": 9.69, "Lobby": 13.99}
mapping = {"lights": {s.nameString(): G37[s.spaceType().get().nameString()] * s.floorArea() for s in ref.getSpaces()}}
cmp_ref = compare_rows(ref, mapping)
cmp_act = compare_rows(actual, mapping)
diff = diff_rows(actual, ref, mapping)
import pickle; pickle.dump(dict(mapping=mapping, cmp_ref=cmp_ref, cmp_act=cmp_act, diff=diff), open(f"{S}/data.pkl", "wb"))
print(sum(mapping["lights"].values()))
for n, d in [("cmp_ref", cmp_ref), ("cmp_act", cmp_act)]:
    print(n, d.status.value_counts().to_dict()); print(d.head(3).to_string())
print(diff.status.value_counts().to_dict())
r = diff[diff.status != "not_requested"]
print(r.groupby(["family", "status", "field"]).size())
print(r.head(8).to_string())
print(diff[diff.status == "not_requested"].family.value_counts().head(15))
