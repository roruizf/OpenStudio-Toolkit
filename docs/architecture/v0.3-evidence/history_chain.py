# Usage: python history_chain.py <dir with one model series *.osm>
"""Item 7 follow-up: full history of one model series (consecutive pairs), time and rows per pair."""
import sys, glob, time, openstudio
from openstudio_toolkit.analysis.diff import diff_models
paths = sorted(glob.glob(f"{sys.argv[1]}/*.osm"))
load = lambda p: openstudio.osversion.VersionTranslator().loadModel(p).get()
t0 = time.perf_counter(); prev = load(paths[0]); total = 0; tl = 0
for p in paths[1:]:
    t = time.perf_counter(); cur = load(p); tl += time.perf_counter() - t
    t = time.perf_counter(); df = diff_models(prev, cur); dt = time.perf_counter() - t
    total += len(df)
    print(f"{p.split('ene01-')[-1]:<18} objs {len(cur.objects()):>5}  rows {len(df):>5}  diff {dt:.1f}s  {dict(df.status.value_counts())}")
    prev = cur
print(f"pairs {len(paths)-1}, rows {total}, load {tl:.1f}s, total {time.perf_counter()-t0:.1f}s")
