# Usage: python locate_proto.py <dir with data.pkl and models/>
"""Prototype: place each diff row in a base object (Space, Thermal Zone, Air loop, Plant loop) by walking
references forward (what the object points to) and backward (who points to it), nearest first."""
import sys, pickle, collections, openstudio
S = sys.argv[1]
d = pickle.load(open(f"{S}/data.pkl", "rb")); diff = d["diff"]
load = lambda p: openstudio.osversion.VersionTranslator().loadModel(p).get()
models = {"parent": load(f"{S}/models/r2f-office-hub-ene01-actual-017.osm"), "child": load(f"{S}/models/r2f-office-hub-ene01-reference-011.osm")}
BASE = {"OS:Space": "Space", "OS:ThermalZone": "Thermal Zone", "OS:AirLoopHVAC": "Air loop", "OS:PlantLoop": "Plant loop",
        "OS:SpaceType": "Space type", "OS:BuildingStory": "Story"}
def direct(m, o):
    t = o.iddObject().name()
    mo = m.getModelObject(o.handle()).get()
    hc = openstudio.model.toHVACComponent(mo)
    if hc.is_initialized():
        hc = hc.get()
        for acc, lab in (("airLoopHVAC", "Air loop"), ("plantLoop", "Plant loop")):
            x = getattr(hc, acc)()
            if x.is_initialized(): return lab, x.get().nameString()
    return None
def locate(m, o, depth=4):
    seen = {str(o.handle())}; frontier = [o]
    for _ in range(depth):
        nxt = []
        for x in frontier:
            t = x.iddObject().name()
            if t in BASE and x is not o: return BASE[t], x.nameString()
            hit = direct(m, x) if t not in BASE else None
            if hit: return hit
            for y in list(x.targets()) + list(x.sources()):
                if str(y.handle()) not in seen and y.iddObject().name() not in ("OS:Connection", "OS:Node", "OS:PortList"):
                    seen.add(str(y.handle())); nxt.append(y)
        for x in nxt:
            if x.iddObject().name() in BASE: return BASE[x.iddObject().name()], x.nameString()
        frontier = nxt
    return None
# index objects by (family/type, key) via the diff's own keys: look up by name, else via handle-less owner key
res = collections.Counter(); kinds = collections.Counter(); unplaced = collections.Counter(); ex = {}
for r in diff.itertuples():
    side = "parent" if r.status == "removed" or r.field == "(object removed)" else "child"
    m = models[side]
    # find candidates by name across all objects with that name (diff key = name or owner name)
    cands = [o for o in m.objects() if o.nameString() == r.key]
    loc = None
    for o in cands:
        loc = locate(m, o) if o.iddObject().name() not in BASE else (BASE[o.iddObject().name()], o.nameString())
        if loc: break
    if loc: res["placed"] += 1; kinds[loc[0]] += 1; ex.setdefault(r.family, (r.key, loc))
    else: res["unplaced"] += 1; unplaced[r.family] += 1
print(res, kinds); print("unplaced by family:", unplaced.most_common(12))
for k, v in list(ex.items())[:25]: print(" ", k, v)
