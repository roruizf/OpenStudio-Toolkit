# Usage: python report_office_hub.py <dir with models/> [language]; writes <dir>/verification-office-hub.html
"""Office Hub actual-017 -> reference-011, lighting mapping = Table G3.7 (ENE01-REFERENCE-MODEL-SPEC §5, SI) x floor area."""
import sys, time, openstudio
from openstudio_toolkit.views.verification import ReportPair, write_report
S = sys.argv[1]; lang = sys.argv[2] if len(sys.argv) > 2 else "en"
load = lambda p: openstudio.osversion.VersionTranslator().loadModel(p).get()
actual = load(f"{S}/models/r2f-office-hub-ene01-actual-017.osm")
ref = load(f"{S}/models/r2f-office-hub-ene01-reference-011.osm")
G37 = {"Office": 11.84, "MeetingRoom": 13.99, "Circulations": 5.38, "BreakRoom": 12.92,
       "Storage": 8.61, "WC": 9.69, "Lobby": 13.99}
mapping = {"lights": {s.nameString(): G37[s.spaceType().get().nameString()] * s.floorArea() for s in ref.getSpaces()}}
t = time.time()
pair = ReportPair(actual, ref, mapping, parent_name="r2f-office-hub-ene01-actual-017.osm",
                  child_name="r2f-office-hub-ene01-reference-011.osm",
                  mapping_name="Lighting: Table G3.7 (ENE01-REFERENCE-MODEL-SPEC §5, SI values) × Space floor area, 36 Spaces",
                  tolerance=0.5)
out = write_report([pair], f"{S}/verification-office-hub.html", title="Office Hub ENE01 — actual-017 → reference-011", language=lang)
print(out, f"{time.time()-t:.1f}s", out.stat().st_size // 1024, "KB")
