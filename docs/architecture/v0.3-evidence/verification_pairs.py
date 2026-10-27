"""Item 7: diff rows crossed with a mapping on real parent -> child pairs.

Mapping = every Space of the child with its OpenStudio lighting total (a "lighting was requested
everywhere" mapping). Prints status counts and, per status, the families involved.
"""
import sys, time, collections, openstudio
from openstudio_toolkit.views.verification import diff_rows

load = lambda p: openstudio.osversion.VersionTranslator().loadModel(p).get()
for parent_path, child_path in zip(sys.argv[1::2], sys.argv[2::2]):
    parent, child = load(parent_path), load(child_path)
    for family in ("lights", "people"):
        accessor = {"lights": "lightingPower", "people": "numberOfPeople"}[family]
        mapping = {family: {s.nameString(): getattr(s, accessor)() for s in child.getSpaces()}}
        t = time.perf_counter(); df = diff_rows(parent, child, mapping); dt = time.perf_counter() - t
        print(f"{parent_path.split('/')[-1]} -> {child_path.split('/')[-1]} [{family} mapping]: {len(df)} rows, {dt:.1f}s")
        for status, group in df.groupby("status"):
            print(f"   {status}: {len(group)}  {dict(collections.Counter(group.family).most_common(6))}")
