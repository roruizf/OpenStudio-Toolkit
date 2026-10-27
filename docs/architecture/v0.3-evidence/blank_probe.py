"""Synthetic closure of the defect class: for every (type, direct-object accessor) pair seen in
the corpus probe, take one object of that type, blank ONE reference field at a time, and call the
accessor. Records which (type, accessor) dies (segfault) or raises when which field is absent.
In-memory only; nothing is saved. One worker per type, restarted after each crash.
"""
import glob, json, os, subprocess, sys
from collections import defaultdict


def worker(model_path, idd_type, accessors, crumb, out, skip):
    import openstudio
    m = openstudio.osversion.VersionTranslator().loadModel(model_path).get()
    objs = m.getObjectsByType(openstudio.IddObjectType(idd_type))
    o = objs[0]
    cname = idd_type[3:].replace(":", "").replace("_", "")
    idd = o.iddObject()
    ref_fields = [i for i in range(1, o.numFields())
                  if i < len(idd.nonextensibleFields())
                  and idd.getField(i).get().properties().type.valueName() == "ObjectListType"]
    res = json.load(open(out)) if os.path.exists(out) else {}
    fh = open(crumb, "w")
    for i in ref_fields:
        fname = idd.getField(i).get().name()
        for acc in accessors:
            key = f"{acc}|{i}|{fname}"
            if key in skip or key in res:
                continue
            orig = o.getString(i)
            if not orig.is_initialized() or orig.get() == "":
                res[key] = "field already empty"; continue
            orig = orig.get()
            if not o.setString(i, ""):
                res[key] = "blank refused"; continue
            typed = getattr(m, f"get{cname}")(o.handle()).get()
            fh.seek(0); fh.write(key); fh.truncate(); fh.flush()
            try:
                getattr(typed, acc)()
                res[key] = "ok"
            except Exception as e:
                res[key] = f"raises {type(e).__name__}"
            o.setString(i, orig)  # restore in memory; the model is never saved
            json.dump(res, open(out, "w"))
    json.dump(res, open(out, "w"))
    fh.close(); os.remove(crumb)


def driver(workdir, kinds_dir, models):
    os.makedirs(workdir, exist_ok=True)
    pairs = defaultdict(set)
    for f in glob.glob(os.path.join(kinds_dir, "*.kinds.json")):
        for k, v in json.load(open(f)).items():
            if v == "object":
                t, mth = k.split(" ")
                pairs[t].add(mth)
    # smallest model containing each type
    present = defaultdict(list)
    for mp in sorted(models, key=os.path.getsize):
        txt = open(mp, encoding="utf-8", errors="replace").read()
        for t in pairs:
            if f"\n{t},\n" in txt:
                present[t].append(mp)
    summary = {}
    for t, accs in sorted(pairs.items()):
        if not present[t]:
            continue
        tag = t.replace(":", "_")
        crumb, out = os.path.join(workdir, tag + ".crumb"), os.path.join(workdir, tag + ".json")
        skip = []
        while True:
            p = subprocess.run([sys.executable, "-I", __file__, "worker", present[t][0], t, ",".join(sorted(accs)),
                                crumb, out, *skip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if p.returncode == 0:
                break
            key = open(crumb).read()
            r = json.load(open(out)) if os.path.exists(out) else {}
            r[key] = f"SEGFAULT rc={p.returncode}"
            json.dump(r, open(out, "w"))
            skip.append(key)
        summary[t] = json.load(open(out))
    json.dump(summary, open(os.path.join(workdir, "summary.json"), "w"), indent=1)


if __name__ == "__main__":
    if sys.argv[1] == "worker":
        worker(sys.argv[2], sys.argv[3], sys.argv[4].split(","), sys.argv[5], sys.argv[6], set(sys.argv[7:]))
    else:
        driver(sys.argv[2], sys.argv[3], sys.argv[4:])
