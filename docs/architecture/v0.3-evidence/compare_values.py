"""Compare get_all_*_as_dataframe values between the HEAD package (argv[1]) and the working tree."""
import sys, json, importlib, subprocess
def run(pkg_root, mod, fn, path):
    code = f"""
import sys, json; sys.path.insert(0, {pkg_root!r}) if {pkg_root!r} else None
import openstudio, importlib
m = openstudio.osversion.VersionTranslator().loadModel({path!r}).get()
f = getattr(importlib.import_module('openstudio_toolkit.osm_objects.{mod}'), '{fn}')
try:
    df = f(m); print(df.astype(object).where(df.notna(), None).to_json(orient='records', default_handler=str))
except Exception as e:
    print(json.dumps({{'error': type(e).__name__ + ': ' + str(e)[:120]}}))
"""
    p = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True)
    return json.loads(p.stdout.strip().splitlines()[-1]) if p.stdout.strip() else {"error": f"died rc={p.returncode}"}
old_root = sys.argv[1]
for spec in sys.argv[2:]:
    mod, fn = spec.split(".")
    for path in ("tests/resources/small_office.osm", "examples/R2F-Office-Hub.osm", "tests/resources/extra_families.osm"):
        a, b = run(old_root, mod, fn, path), run("", mod, fn, path)
        tag = f"{fn} @ {path.split('/')[-1]}"
        if isinstance(a, dict) or isinstance(b, dict):
            print(tag, "OLD:", a if isinstance(a, dict) else f"{len(a)} rows", "| NEW:", b if isinstance(b, dict) else f"{len(b)} rows"); continue
        diffs = [(i, k, ra.get(k), rb.get(k)) for i, (ra, rb) in enumerate(zip(a, b)) for k in set(ra) | set(rb) if ra.get(k) != rb.get(k)]
        print(tag, f"rows {len(a)}->{len(b)}", "identical" if not diffs and len(a)==len(b) else f"{len(diffs)} diffs e.g. {diffs[:3]}")
