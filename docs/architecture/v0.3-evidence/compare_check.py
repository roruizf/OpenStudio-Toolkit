"""Cell-by-cell check: OpenStudio's per-space/zone totals vs an independent recomputation from the dump
views and records (inheritance: space -> own space type, else building space type; every design method;
load multiplier). Then compare_to_mapping on a mapping built from those independent values must be all match."""
import sys, math, openstudio
from openstudio_toolkit.analysis.compare import compare_to_mapping, _FAMILIES as FAMILIES
from openstudio_toolkit.dump import dump_view
from openstudio_toolkit.extractors.generic import read_model_objects

DEF = {"people": ("people_definition", "People Definition Name", "Number of People Calculation Method",
                  {"People": ("Number of People {people}", "abs"), "People/Area": ("People per Space Floor Area {person/m2}", "area"),
                   "Area/Person": ("Space Floor Area per Person {m2/person}", "inv_area")}),
       "lights": ("lights_definition", "Lights Definition Name", "Design Level Calculation Method",
                  {"LightingLevel": ("Lighting Level {W}", "abs"), "Watts/Area": ("Watts per Space Floor Area {W/m2}", "area"),
                   "Watts/Person": ("Watts per Person {W/person}", "person")}),
       "electric_equipment": ("electric_equipment_definition", "Electric Equipment Definition Name", "Design Level Calculation Method",
                  {"EquipmentLevel": ("Design Level {W}", "abs"), "Watts/Area": ("Watts per Space Floor Area {W/m2}", "area"),
                   "Watts/Person": ("Watts per Person {W/person}", "person")})}

for path in sys.argv[1:]:
    m = openstudio.osversion.VersionTranslator().loadModel(path).get()
    v = dump_view(m)
    recs = read_model_objects(m)
    by_handle = {r.handle: r for r in recs}
    building = next(r for r in recs if r.idd_type == "OS:Building")
    bst_field = next(f for f in building.fields if f.name == "Space Type Name")
    building_st = by_handle[bst_field.target].name if bst_field.target else None
    space_rec = {r.name: r for r in recs if r.idd_type == "OS:Space"}
    sp = v["space"].set_index("Name")
    def own_type(name):
        f = next(f for f in space_rec[name].fields if f.name == "Space Type Name")
        return by_handle[f.target].name if f.target else building_st
    expected = {}
    for fam in ("people", "lights", "electric_equipment"):  # people first: W/person needs it
        dview, dfield, mfield, methods = DEF[fam]
        defs = v[dview].set_index("Name")
        inst = v[fam]
        for name in sp.index:
            area, total = sp.at[name, "Floor Area {m2}"], 0.0
            for _, o in inst[inst["Space or SpaceType Name"].isin([name, own_type(name)])].iterrows():
                d = defs.loc[o[dfield]]; col, kind = methods[d[mfield]]; x = d[col]
                per = {"abs": x, "area": x * area, "inv_area": area / x if x else 0.0,
                       "person": x * expected.get(("people", name), 0.0)}[kind]
                total += per * o["Multiplier"]
            expected[(fam, name)] = total
    bad = n = 0
    for (fam, name), exp in expected.items():
        got = getattr(m.getSpaceByName(name).get(), FAMILIES[fam][1])(); n += 1
        if not math.isclose(exp, got, rel_tol=1e-12, abs_tol=1e-9): bad += 1; print("  SPACE MISMATCH", fam, name, exp, got)
    for z in m.getThermalZones():
        for fam in FAMILIES:
            exp = sum(expected[(fam, s.nameString())] for s in z.spaces()); got = getattr(z, FAMILIES[fam][1])(); n += 1
            if not math.isclose(exp, got, rel_tol=1e-12, abs_tol=1e-9): bad += 1; print("  ZONE MISMATCH", fam, z.nameString(), exp, got)
    mapping = {fam: {name: val for (f, name), val in expected.items() if f == fam} for fam in FAMILIES}
    df = compare_to_mapping(m, mapping)
    print(f"{path.split('/')[-1]}: {n} totals checked, {bad} mismatches; compare statuses {df.status.value_counts().to_dict()}")
    print("   missing rows with requested != 0:", int(((df.status == "missing") & (df.requested != 0)).sum()))
