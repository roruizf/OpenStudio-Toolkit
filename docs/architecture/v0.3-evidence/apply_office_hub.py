# Usage: python apply_office_hub.py <dir with models/>; writes <dir>/models/actual-017-apply-g37.osm (never the sources)
"""Item 4 on Office Hub: G3.7 lighting mapping applied to actual-017 and to reference-011, then compared and diffed."""
import hashlib
import sys
from collections import Counter

import openstudio

from openstudio_toolkit.analysis.compare import compare_to_mapping
from openstudio_toolkit.transforms.apply import ApplyError, apply_mapping
from openstudio_toolkit.views.verification import diff_rows

S = sys.argv[1]
L = lambda p: openstudio.osversion.VersionTranslator().loadModel(p).get()
actual, ref = f"{S}/models/r2f-office-hub-ene01-actual-017.osm", f"{S}/models/r2f-office-hub-ene01-reference-011.osm"
G37 = {"Office": 11.84, "MeetingRoom": 13.99, "Circulations": 5.38, "BreakRoom": 12.92, "Storage": 8.61, "WC": 9.69, "Lobby": 13.99}
ref_model = L(ref)  # keep the model alive while its Spaces are read
mapping = {"lights": {s.nameString(): G37[s.spaceType().get().nameString()] * s.floorArea() for s in ref_model.getSpaces()}}
digest = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
before = digest(actual)
out = f"{S}/models/actual-017-apply-g37.osm"

for label, src, mode in (("actual-017 default", actual, "refuse"), ("reference-011 update", ref, "update")):
    try:
        apply_mapping(src, f"{S}/models/never.osm", mapping, existing=mode)
    except ApplyError as e:
        print(label, "-> refused,", len(e.problems), "problems; first:", e.problems[0])

print(apply_mapping(actual, out, mapping, existing="update"))
child, parent = L(out), L(actual)
c = compare_to_mapping(child, mapping)
d = diff_rows(parent, child, mapping)
print("compare", Counter(c.status), "max |difference|", c.difference.abs().max(), "total", round(c.in_model.sum(), 2))
print("diff", Counter(d.status), Counter(d.field))
print("input unchanged:", digest(actual) == before)
