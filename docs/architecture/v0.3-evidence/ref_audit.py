"""Static reference audit of OSM text. No model load.

Class D (dangling): a field holds {guid} that no object declares as its handle.
Class E (empty ref): a non-extensible field the IDD types as a reference is empty ([req] = IDD-required).

Parsing ignores comments entirely ('!-' and '! ' both appear in real files): fields are
positional, field 0 is the handle. Field semantics for class E come from the installed
OpenStudio IDD (openstudio 3.11.0), not from the comment text.
"""
import json, re, sys
from collections import Counter, defaultdict

GUID = re.compile(r"^\{[0-9a-fA-F-]{36}\}$")


def parse(path):
    objs, cur = [], None
    with open(path, encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            line = raw.split("!", 1)[0].rstrip()
            if not line.strip():
                continue
            if not raw[0].isspace():                   # object type line: "OS:Foo,"
                cur = {"type": line.rstrip(",;").strip(), "fields": []}
                objs.append(cur)
                continue
            # one field per line in OSM; value ends with ',' or ';'
            cur["fields"].append(line.strip().rstrip(",;").strip())
    return objs


def idd_refs():
    import openstudio
    out = {}
    idd = openstudio.IddFactory.instance().getIddFile(openstudio.IddFileType("OpenStudio"))
    for o in idd.objects():
        f = []
        for i, fld in enumerate(o.nonextensibleFields()):
            p = fld.properties()
            is_ref = p.type.valueName() in ("ObjectListType", "HandleType") and i > 0
            f.append((fld.name(), is_ref, p.required))
        ext = []
        for fld in o.extensibleGroup():
            p = fld.properties()
            ext.append((fld.name(), p.type.valueName() in ("ObjectListType", "HandleType"), False))
        out[o.name()] = (f, ext)
    return out


def audit(path, refs):
    objs = parse(path)
    declared = {o["fields"][0] for o in objs if o["fields"] and GUID.match(o["fields"][0])}
    dang, empty = Counter(), Counter()
    dang_ex, empty_ex = {}, {}
    for o in objs:
        spec, ext = refs.get(o["type"], ([], []))
        for i, v in enumerate(o["fields"][1:], start=1):
            if i < len(spec):
                name, is_ref = spec[i][0], spec[i][1]
            elif ext:
                name, is_ref = ext[(i - len(spec)) % len(ext)][:2]
            else:
                name, is_ref = f"field {i}", False
            if GUID.match(v) and v not in declared and is_ref:
                dang[(o["type"], name)] += 1
                dang_ex.setdefault((o["type"], name), o["fields"][0])
            elif v == "" and i < len(spec) and is_ref:
                empty[(o["type"], name + (" [req]" if spec[i][2] else ""))] += 1
                empty_ex.setdefault((o["type"], name), o["fields"][0])
    return {"objects": len(objs), "declared": len(declared),
            "dangling": {f"{t} / {n}": c for (t, n), c in dang.items()},
            "empty_required_ref": {f"{t} / {n}": c for (t, n), c in empty.items()}}


if __name__ == "__main__":
    refs = idd_refs()
    res = {p.rsplit("/", 1)[1]: audit(p, refs) for p in sys.argv[1:]}
    json.dump(res, open("ref_audit.json", "w"), indent=1)
    for k, r in res.items():
        print(f"{k:42} obj {r['objects']:5}  D {sum(r['dangling'].values()):4}  E {sum(r['empty_required_ref'].values()):4}")
