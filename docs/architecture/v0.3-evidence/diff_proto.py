"""Item 6 prototype: diff_models on read_model_objects, cascade handle -> type+name (unique both sides)."""
import sys, time, collections
import openstudio, pandas as pd
from openstudio_toolkit.extractors.generic import read_model_objects
from openstudio_toolkit import dump
TOPOLOGY = {"OS:Connection", "OS:Node", "OS:PortList"}
FAM = {v: k for k, v in dump.families().items()}

def load(p): return openstudio.osversion.VersionTranslator().loadModel(p).get()

def match(P, C):
    pairs, up, uc = {}, dict(P), dict(C)
    for h in list(up):
        if h in uc and up[h].idd_type == uc[h].idd_type:
            pairs[h] = (h, "handle"); del up[h]; del uc[h]
    def by(pool):
        d = collections.defaultdict(list)
        for h, r in pool.items():
            if r.name: d[(r.idd_type, r.name)].append(h)
        return d
    bp, bc = by(up), by(uc)
    for k, ps in bp.items():
        cs = bc.get(k, [])
        if len(ps) == 1 and len(cs) == 1:
            pairs[ps[0]] = (cs[0], "type_name"); del up[ps[0]]; del uc[cs[0]]
    return pairs, up, uc

def label(f): return f.name if f.group is None else f"{f.name} #{f.group}"

def diff(pm, cm):
    P = {r.handle: r for r in read_model_objects(pm) if r.idd_type != "OS:CommentOnly"}
    C = {r.handle: r for r in read_model_objects(cm) if r.idd_type != "OS:CommentOnly"}
    pairs, up, uc = match(P, C)
    p2c = {p: c for p, (c, _) in pairs.items()}
    rows = []
    fam = lambda t: FAM.get(t, t)
    for p, (c, how) in pairs.items():
        a, b = P[p], C[c]
        fa, fb = {f.index: f for f in a.fields}, {f.index: f for f in b.fields}
        for i in sorted(set(fa) | set(fb)):
            x, y = fa.get(i), fb.get(i)
            if x is not None and y is not None and x.is_reference:
                same = (x.target is None and y.target is None) or (x.target is not None and p2c.get(x.target) == y.target)
            else:
                same = (x.value if x else None) or None
                same = same == ((y.value if y else None) or None)
            if not same:
                rows.append((fam(b.idd_type), b.name or b.handle, label(y or x), x.value if x else None, y.value if y else None, "changed", how))
    rows += [(fam(r.idd_type), r.name or r.handle, None, None, None, "removed", None) for r in up.values()]
    rows += [(fam(r.idd_type), r.name or r.handle, None, None, None, "added", None) for r in uc.values()]
    return pd.DataFrame(rows, columns=["family", "key", "field", "parent", "child", "status", "match_method"])

if __name__ == "__main__":
    for spec in sys.argv[1:]:
        p, c = spec.split(",")
        t = time.perf_counter(); df = diff(load(p), load(c)); dt = time.perf_counter() - t
        topo = df.family.isin(TOPOLOGY)
        print(f"\n== {p.split('/')[-1]} -> {c.split('/')[-1]}  ({dt:.1f}s)  rows {len(df)}, topology {topo.sum()}")
        print(df[~topo].groupby("status").size().to_dict())
        print(df[~topo].groupby(["family","status"]).size().sort_values(ascending=False).head(12).to_string())
        df.to_csv(spec.replace(",", "__").replace("/", "_")[-80:] + ".csv", index=False)
