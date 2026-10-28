"""Step B prototype: cascade matching parent -> child.

Levels: 1 handle (same type), 2 type+name, 3 membership (same type, same Space/ThermalZone,
exactly one candidate on each side), 4 unmatched. Never guess: ambiguity stays unmatched.
Membership is the direct reference only: a field of the object pointing to an OS:Space or
OS:ThermalZone (or, for an OS:Space, its zone). Indirect membership is not resolved.
"""
import json, sys
from collections import Counter, defaultdict

import openstudio

HOLDERS = {"OS:Space", "OS:ThermalZone"}


def load(path):
    m = openstudio.osversion.VersionTranslator().loadModel(path)
    if not m.is_initialized():
        sys.exit(f"load failed: {path}")
    m = m.get()
    objs = {}
    for o in m.objects():
        idd = o.iddObject()
        fields, holders = [], set()
        for i in range(o.numFields()):
            v = o.getString(i)
            fields.append(v.get() if v.is_initialized() else None)
            # getString returns the target's NAME for reference fields; resolve the target itself
            t = o.getTarget(i) if i else None
            if t is not None and t.is_initialized() and t.get().iddObject().name() in HOLDERS:
                holders.add(str(t.get().handle()))
        objs[str(o.handle())] = {
            "type": idd.name(),
            "name": o.name().get() if o.name().is_initialized() else None,
            "fields": fields,
            "holders": sorted(holders),
        }
    return objs


def match(P, C):
    lvl = {}                        # parent handle -> (child handle, level)
    up, uc = set(P), set(C)
    # 1. handle
    for h in list(up):
        if h in uc and P[h]["type"] == C[h]["type"]:
            lvl[h] = (h, 1); up.discard(h); uc.discard(h)
    # 2. type + name (unique on both sides)
    def by_tn(objs, pool):
        d = defaultdict(list)
        for h in pool:
            if objs[h]["name"] is not None:
                d[(objs[h]["type"], objs[h]["name"])].append(h)
        return d
    pd_, cd_ = by_tn(P, up), by_tn(C, uc)
    for k, ps in pd_.items():
        cs = cd_.get(k, [])
        if len(ps) == 1 and len(cs) == 1:
            lvl[ps[0]] = (cs[0], 2); up.discard(ps[0]); uc.discard(cs[0])
    # 3. membership: translate child holders into parent handles via matches so far
    c2p = {c: p for p, (c, _) in lvl.items()}
    def by_holder(objs, pool, xl):
        d = defaultdict(list)
        for h in pool:
            hs = objs[h]["holders"]
            if hs:
                key = tuple(sorted(xl(x) for x in hs))
                if None not in key:
                    d[(objs[h]["type"], key)].append(h)
        return d
    pm = by_holder(P, up, lambda x: x)
    cm = by_holder(C, uc, lambda x: c2p.get(x))
    for k, ps in pm.items():
        cs = cm.get(k, [])
        if len(ps) == 1 and len(cs) == 1:
            lvl[ps[0]] = (cs[0], 3); up.discard(ps[0]); uc.discard(cs[0])
    return lvl, up, uc


def report(label, P, C):
    lvl, up, uc = match(P, C)
    fam = defaultdict(Counter)
    for p, (c, l) in lvl.items():
        f = fam[P[p]["type"]]
        f[f"L{l}"] += 1
        if P[p]["fields"][1:] != C[c]["fields"][1:]:
            f["changed"] += 1
        if l == 1 and P[p]["name"] != C[c]["name"]:
            f["renamed"] += 1
    for p in up:
        fam[P[p]["type"]]["unP"] += 1
    for c in uc:
        fam[C[c]["type"]]["unC"] += 1
    tot = Counter()
    for f in fam.values():
        tot.update(f)
    return {"label": label, "parent": len(P), "child": len(C), "total": dict(tot),
            "families": {k: dict(v) for k, v in sorted(fam.items())}}


if __name__ == "__main__":
    out = []
    for pair in sys.argv[1:]:
        label, p, c = pair.split("=", 1)[0], *pair.split("=", 1)[1].split(",")
        out.append(report(label, load(p), load(c)))
    json.dump(out, open(out_path := "match_metrics.json", "w"), indent=1)
    for r in out:
        print(r["label"], r["parent"], "->", r["child"], r["total"])
