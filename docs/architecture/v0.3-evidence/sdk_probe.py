"""SDK accessor probe. One worker process per model; the driver restarts the worker after a
crash, skipping the (type, method) pair that killed it.

Worker: for every object, cast to its typed class and call every zero-arg read-looking method.
Before each call it writes "type method handle" to a breadcrumb file (flushed), so a segfault
leaves the culprit on disk. Records each method's return kind: 'optional' (has is_initialized),
'object' (a ModelObject returned directly), or 'other'.
"""
import json, os, subprocess, sys

MUTATING = ("set", "reset", "remove", "add", "clone", "autosize", "create", "apply", "assign",
            "make", "purge", "disconnect", "rename", "erase", "push", "insert", "move", "swap",
            "import", "export", "save", "simulate", "run", "hardsize", "change", "update",
            "translate", "convert", "ensure", "split", "merge", "intersect", "match", "unmatch",
            "combine", "sort", "toggle", "enable", "disable", "zero", "erase", "attach", "detach",
            "applySizingValues", "resize", "fix", "delete", "clear", "unique", "relocate", "rotate",
            "scale", "subtract", "triangulate", "compute", "generate", "search", "assume",
            "this", "thisown", "to", "cast", "pop")


def worker(model_path, crumb, out, skip):
    import openstudio
    m = openstudio.osversion.VersionTranslator().loadModel(model_path).get()
    kinds = {}
    cache = {}
    seen_types = set()
    fh = open(crumb, "w")
    # phase 1: classify every method on the first object of each type
    # phase 2: on every object, call only methods that return an object directly (unguarded)
    objs = list(m.modelObjects())
    work = [(o, 1) for o in objs if not (o.iddObject().name() in seen_types or seen_types.add(o.iddObject().name()))]
    work += [(o, 2) for o in objs]
    for o, phase in work:
        idd = o.iddObject().name()
        cls = cache.get(idd)
        if cls is None:
            cname = idd[3:].replace(":", "").replace("_", "")
            getter = getattr(m, f"get{cname}", None)
            cache[idd] = cls = (cname, getter)
        cname, getter = cls
        if getter is None:
            continue
        try:
            t = getter(o.handle())
        except Exception:
            continue
        if not t.is_initialized():
            continue
        t = t.get()
        for meth in dir(t):
            if meth.startswith("_") or meth.startswith(MUTATING) or f"{idd} {meth}" in skip:
                continue
            if phase == 2 and kinds.get(f"{idd} {meth}") != "object":
                continue
            fn = getattr(t, meth, None)
            if not callable(fn):
                continue
            fh.seek(0); fh.write(f"{idd} {meth} {o.handle()}"); fh.truncate(); fh.flush()
            try:
                r = fn()
            except TypeError:
                continue
            except Exception as e:
                kinds.setdefault(f"{idd} {meth}", f"raises:{type(e).__name__}")
                continue
            k = ("optional" if hasattr(r, "is_initialized") else
                 "object" if hasattr(r, "handle") and hasattr(r, "iddObjectType") else "other")
            kinds.setdefault(f"{idd} {meth}", k)
    json.dump(kinds, open(out, "w"))
    fh.close(); os.remove(crumb)


def driver(model_path, workdir):
    tag = os.path.basename(model_path)
    crumb = os.path.join(workdir, tag + ".crumb")
    out = os.path.join(workdir, tag + ".kinds.json")
    skip, crashes = [], []
    while True:
        p = subprocess.run([sys.executable, "-I", __file__, "worker", model_path, crumb, out, *skip],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if p.returncode == 0:
            break
        site = open(crumb).read().split(" ")
        crashes.append({"type": site[0], "method": site[1], "handle": site[2], "rc": p.returncode})
        skip.append(f"{site[0]} {site[1]}")
        if len(skip) > 200:
            break
    json.dump({"model": tag, "crashes": crashes}, open(os.path.join(workdir, tag + ".crashes.json"), "w"))
    print(tag, "restarts:", len(crashes), [f"{c['type']}.{c['method']}" for c in crashes])


if __name__ == "__main__":
    if sys.argv[1] == "worker":
        worker(sys.argv[2], sys.argv[3], sys.argv[4], set(sys.argv[5:]))
    else:
        os.makedirs(sys.argv[2], exist_ok=True)
        for mp in sys.argv[3:]:
            driver(mp, sys.argv[2])
