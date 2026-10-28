"""Item 3 fix: every cell of the 7 touched readers, HEAD package (argv[1]) vs working tree, on the given models.

Raw OpenStudio Optionals are unwrapped for the comparison and reported as "unwrapped" or "autosize"."""
import sys, json, subprocess
FNS=[("hvac_sizing","get_all_sizing_zone_objects_as_dataframe"),("hvac_components","get_all_air_conditioner_variable_refrigerant_flow_objects_as_dataframe"),("hvac_components","get_all_hx_air_to_air_sensible_and_latent_as_dataframe"),("hvac_zone","get_all_air_terminal_single_duct_parallel_piu_reheat_objects_as_dataframe"),("hvac_zone","get_all_zone_hvac_terminal_unit_variant_refrigerant_flow_objects_as_dataframe"),("hvac_zone","get_all_four_pipe_fan_coil_objects_as_dataframe"),("hvac_zone","get_all_zone_hvac_unit_heater_objects_as_dataframe")]
CODE='''
import sys, json; root=sys.argv[1]
if root: sys.path.insert(0, root)
import openstudio, importlib
def cell(v):
    if type(v).__module__.startswith("openstudio"):
        return {"optional": v.get() if v.is_initialized() else None}
    return None if v != v else v
m=openstudio.osversion.VersionTranslator().loadModel(sys.argv[2]).get()
f=getattr(importlib.import_module("openstudio_toolkit.osm_objects."+sys.argv[3]), sys.argv[4])
df=f(m); print(json.dumps([{k: cell(v) for k,v in r.items()} for r in df.to_dict("records")], default=str))
'''
for path in sys.argv[2:]:
    for mod,fn in FNS:
        out=[json.loads(next(l for l in subprocess.run([sys.executable,"-I","-c",CODE,root,path,mod,fn],capture_output=True,text=True).stdout.splitlines() if l.startswith("["))) for root in (sys.argv[1],"")]
        a,b=out; changes={}
        for ra,rb in zip(a,b):
            for k in ra:
                if ra[k]!=rb[k]:
                    kind=("unwrapped" if isinstance(ra[k],dict) and ra[k]["optional"]==rb[k] else
                          "autosize" if isinstance(ra[k],dict) and ra[k]["optional"] is None and rb[k] in ("Autosize","autosize") else f"OTHER {ra[k]!r}->{rb[k]!r}")
                    changes.setdefault((k,kind),0); changes[(k,kind)]+=1
        if changes or len(a)!=len(b):
            print(path.split("/")[-1], fn, f"rows {len(a)}->{len(b)}")
            for (k,kind),n in sorted(changes.items()): print("    ",kind,n,k)
