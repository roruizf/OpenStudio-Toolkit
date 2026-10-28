"""Prototype only (scratchpad): r2f contract + 'replace the Space's own loads', on actual-017 with G3.7."""
# Usage: python apply_proto.py <dir with models/>  (writes <dir>/models/actual-017-applied-g37.osm; never the source)
import sys
S = sys.argv[1]
import openstudio
from collections import Counter
from openstudio_toolkit.analysis.compare import compare_to_mapping
from openstudio_toolkit.analysis.diff import diff_models
L = lambda p: openstudio.osversion.VersionTranslator().loadModel(p).get()
src = f"{S}/models/r2f-office-hub-ene01-actual-017.osm"
a = L(src); ref = L(f"{S}/models/r2f-office-hub-ene01-reference-011.osm")
G37 = {"Office": 11.84, "MeetingRoom": 13.99, "Circulations": 5.38, "BreakRoom": 12.92, "Storage": 8.61, "WC": 9.69, "Lobby": 13.99}
mapping = {"lights": {s.nameString(): G37[s.spaceType().get().nameString()] * s.floorArea() for s in ref.getSpaces()}}
m = L(src)
removed = 0
for name, w in mapping["lights"].items():
    sp = m.getSpaceByName(name).get()
    for l in list(sp.lights()):
        d = l.definition(); l.remove(); removed += 1
        if not d.directUseCount(): d.remove()
    d = openstudio.model.LightsDefinition(m); d.setName(f"{name} Lights Definition"); d.setLightingLevel(w)
    i = openstudio.model.Lights(d); i.setName(f"{name} Lights"); i.setSpace(sp)
openstudio.energyplus.ForwardTranslator().translateModel(m)
out = f"{S}/models/actual-017-applied-g37.osm"; m.save(out, True)
m2 = L(out)
c = compare_to_mapping(m2, mapping)
print("removed", removed, "compare", Counter(c.status), "max|diff|", c.difference.abs().max(), "total", round(c.in_model.sum(), 2))
from openstudio_toolkit.views.verification import diff_rows
d = diff_rows(a, m2, mapping)
print("diff", Counter(d.status), Counter(d.family[d.status!="not_requested"]).most_common(4))
print("not_requested sample", d[d.status=="not_requested"].head(5).to_dict("records"))
before = compare_to_mapping(a, mapping); print("actual before: total", round(before.in_model.sum(),2), Counter(before.status))
ex = c[c.key=="1.10-MeetingRoom"].iloc[0]; print("example", ex.key, ex.requested, ex.in_model)
print(Counter(d.field)); print(d[d.key.str.startswith("1.10-Meeting")][["key","field","parent","child","match_method"]].to_string())
