"""Item 6: analysis.diff vs diff_proto.py on real pairs (argv[1] = dir holding diff_proto.py, then parent,child ...)."""
import openstudio
sys.path.insert(0, sys.argv[1]); import diff_proto
from openstudio_toolkit.analysis.diff import diff_models, TOPOLOGY_TYPES
for spec in sys.argv[2:]:
    p, c = spec.split(",")
    pm, cm = diff_proto.load(p), diff_proto.load(c)
    t = time.perf_counter(); df = diff_models(pm, cm, include_topology=True); dt = time.perf_counter() - t
    proto = diff_proto.diff(pm, cm); proto = proto[proto.family != "CommentOnly"]
    norm = lambda d: collections.Counter(zip(d.family, d.field.fillna(""), d.parent.fillna(""), d.child.fillna(""), d.status, d.match_method.fillna("")))
    a, b = norm(df), norm(proto)
    print(p.split("/")[-1], f"{dt:.1f}s rows {len(df)} proto {len(proto)} same-ignoring-key {a == b}",
          "handle-keys", int(df.key.str.startswith("{").sum()), "default rows", len(diff_models(pm, cm)))
