"""Scratchpad only: OpenStudio's own ways to stop sharing loads (copies; sources never saved)."""
import sys
from collections import Counter
import openstudio
from openstudio_toolkit._sdk import opt
from openstudio_toolkit.views.verification import diff_rows
S = sys.argv[1]
L = lambda p: openstudio.osversion.VersionTranslator().loadModel(p).get()
fams = (("lights", "lightingPower"), ("people", "numberOfPeople"), ("electricEquipment", "electricEquipmentPower"))

def shared_defs(m):
    out = Counter()
    for kind, cls in (("lights", "getLightsDefinitions"), ("people", "getPeopleDefinitions"), ("electricEquipment", "getElectricEquipmentDefinitions")):
        out[kind] = sum(1 for d in getattr(m, cls)() if len(d.instances()) > 1)
    return dict(out)

for name in ("models/r2f-office-hub-ene01-actual-017.osm", "models/r2f-office-hub-ene01-reference-011.osm", "fpm4/fpm4-final-proposed.osm", "orph/Tribe-Hotel-015.osm"):
    m = L(f"{S}/{name}")
    st_loads = sum(len(getattr(t, k)()) for t in m.getSpaceTypes() for k, _ in fams)
    print(name.split("/")[-1], "| spaces", len(m.getSpaces()), "| loads on space types", st_loads, "| definitions shared by >1 load", shared_defs(m))

# 1) Space type -> Space: hardApplySpaceType on reference-011 (lights on 7 space types)
src = f"{S}/models/r2f-office-hub-ene01-reference-011.osm"
before = L(src); m = L(src)
totals = {s.nameString(): [getattr(s, t)() for _, t in fams] for s in m.getSpaces()}
for s in m.getSpaces():
    s.hardApplySpaceType(False)  # returns nothing
after = {s.nameString(): [getattr(s, t)() for _, t in fams] for s in m.getSpaces()}
worst = max(abs(a - b) for k in totals for a, b in zip(totals[k], after[k]))
own = sum(len(s.lights()) for s in m.getSpaces()); stl = sum(len(t.lights()) for t in m.getSpaceTypes())
ex = m.getSpaceByName("1.10-MeetingRoom").get()
print("hardApplySpaceType: max change of any Space total", worst, "| own lights now", own, "| lights left on space types", stl,
      "| own space type kept:", opt(ex.spaceType()).nameString() if opt(ex.spaceType()) else None,
      "| example light:", [(l.nameString(), l.definition().nameString(), round(l.lightingLevel() or 0, 2)) for l in ex.lights()])
out = f"{S}/models/reference-011-hard-applied.osm"; m.save(out, True)
d = diff_rows(before, L(out), {})
print("   diff vs reference-011:", Counter(d.status), Counter(d.family).most_common(6))

# 2) Shared definition -> one per load: makeUnique on a synthetic case (two Spaces, one definition)
t = openstudio.model.Model()
pts = lambda x: openstudio.Point3dVector([openstudio.Point3d(x,0,0), openstudio.Point3d(x,10,0), openstudio.Point3d(x+10,10,0), openstudio.Point3d(x+10,0,0)])
a = openstudio.model.Space.fromFloorPrint(pts(0), 3, t).get(); b = openstudio.model.Space.fromFloorPrint(pts(20), 3, t).get()
dfn = openstudio.model.LightsDefinition(t); dfn.setName("Shared 500 W"); dfn.setLightingLevel(500); dfn.setFractionRadiant(0.25)
la = openstudio.model.Lights(dfn); la.setSpace(a); lb = openstudio.model.Lights(dfn); lb.setSpace(b)
print("makeUnique: before, definition used by", len(dfn.instances()))
lb.makeUnique()
nb = lb.definition()
print("   after: original used by", len(dfn.instances()), "| new", nb.nameString(), "used by", len(nb.to_LightsDefinition().get().instances()),
      "| radiant kept", nb.to_LightsDefinition().get().fractionRadiant(), "| level", nb.to_LightsDefinition().get().lightingLevel().get())
