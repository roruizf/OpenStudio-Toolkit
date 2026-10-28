"""Where do loads live in real models, and how far is 'stored on the space' from 'what OpenStudio resolves'."""
import sys, collections, openstudio
from openstudio_toolkit._sdk import opt
for path in sys.argv[1:]:
    m = openstudio.osversion.VersionTranslator().loadModel(path).get()
    spaces = list(m.getSpaces()); zones = list(m.getThermalZones())
    print(f"\n== {path.split('/')[-1]}: {len(spaces)} spaces, {len(zones)} zones, "
          f"zones with >1 space: {sum(len(z.spaces())>1 for z in zones)}, max multiplier {max((z.multiplier() for z in zones), default=0)}")
    fams = [("people", m.getPeoples, lambda s: s.numberOfPeople(), lambda o: o.peopleDefinition().numberofPeople()),
            ("lights", m.getLightss, lambda s: s.lightingPower(), lambda o: o.lightsDefinition().lightingLevel()),
            ("elec_eq", m.getElectricEquipments, lambda s: s.electricEquipmentPower(), lambda o: o.electricEquipmentDefinition().designLevel())]
    for name, getter, resolved, level in fams:
        objs = list(getter())
        at_space = collections.Counter(); at_st = 0; no_parent = 0; methods = collections.Counter(); sched_empty_field = 0
        stored = collections.defaultdict(float)
        for o in objs:
            if o.getString(2 if name!="people" else 2).get() == "":
                pass
            sp = opt(o.space()); st = opt(o.spaceType())
            if sp is not None: at_space[sp.nameString()] += 1
            elif st is not None: at_st += 1
            else: no_parent += 1
            lv = opt(level(o))
            if sp is not None and lv is not None: stored[sp.nameString()] += lv * o.multiplier()
            methods[o.definition().getString(2).get()] += 1
        multi = sum(c > 1 for c in at_space.values())
        differ = [(s.nameString(), stored.get(s.nameString(), 0.0), resolved(s)) for s in spaces
                  if abs(stored.get(s.nameString(), 0.0) - resolved(s)) > 1e-6]
        print(f"  {name}: {len(objs)} objs, on space {sum(at_space.values())}, on spacetype {at_st}, none {no_parent}, "
              f"spaces with >1 obj {multi}, methods {dict(methods)}; spaces where stored-on-space != resolved: {len(differ)}")
        for d in differ[:3]: print("     e.g.", d)
    # outdoor air: space field vs resolved (spacetype inheritance)
    oa_field = sum(1 for s in spaces if s.getString(12).get() != "")
    oa_res = sum(1 for s in spaces if opt(s.designSpecificationOutdoorAir()) is not None)
    print(f"  outdoor air object: written on space {oa_field}, resolved (incl. space type) {oa_res}")
