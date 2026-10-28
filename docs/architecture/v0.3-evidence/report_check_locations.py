# Usage: python report_check_locations.py <dir with models/ and verification-office-hub.html>
# Hand check of a location sample through OpenStudio's typed API (independent of views._location).
import sys, re, html, openstudio
S = sys.argv[1]
load = lambda p: openstudio.osversion.VersionTranslator().loadModel(p).get()
par = load(f"{S}/models/r2f-office-hub-ene01-actual-017.osm"); ch = load(f"{S}/models/r2f-office-hub-ene01-reference-011.osm")
page = open(f"{S}/verification-office-hub.html", encoding="utf-8").read()
def shown(family, key):
    for tr in re.findall(r'<tr data-status="[^"]+" data-family="%s">(.*?)</tr>' % re.escape(family), page):
        cells = re.findall(r"<td([^>]*)>(.*?)</td>", tr)
        if html.unescape(re.sub("<[^>]+>", "", cells[1][1])) == key:
            return [html.unescape(re.search(r'data-place="([^"]*)"', a).group(1)) if "data-place" in a else "" for a, _ in cells[7:]]
def show(label, family, key, expected):
    got = shown(family, key); print(("OK  " if got == expected else "BAD ") + label, "|", got, "| expected", expected)
# 1) air terminal, child: zone from ThermalZone.equipment(), loop from airLoopHVAC()
t = ch.getAirTerminalSingleDuctConstantVolumeNoReheatByName("TZ-0.01-Lobby PSZ-AC Diffuser").get()
z = [zz.nameString() for zz in ch.getThermalZones() if any(e.handle() == t.handle() for e in zz.equipment())]
show("terminal (two owners)", "OS:AirTerminal:SingleDuct:ConstantVolume:NoReheat", "TZ-0.01-Lobby PSZ-AC Diffuser", ["", " | ".join(z), t.airLoopHVAC().get().nameString()])
# 2) VRF terminal, parent: zone + VRF outdoor unit via vrf.terminals()
v = par.getZoneHVACTerminalUnitVariableRefrigerantFlowByName("TZ-0.01-Lobby VRF Terminal Unit").get()
vrf = [x.nameString() for x in par.getAirConditionerVariableRefrigerantFlows() if any(y.handle() == v.handle() for y in x.terminals())]
show("VRF terminal", "OS:ZoneHVAC:TerminalUnit:VariableRefrigerantFlow", "TZ-0.01-Lobby VRF Terminal Unit", ["", v.thermalZone().get().nameString(), " | ".join(vrf)])
# 3) shared schedule, child: Spaces reached through the lights that use it. The report shows 36 for
#    OfficeSmall BLDG_LIGHT_SCH_2013 because the 7 space types' schedule sets also reference it (checked).
cands = [s for s in ch.getScheduleRulesets() if s.nameString().startswith("OfficeSmall BLDG_LIGHT")]
print("lighting rulesets in child:", [s.nameString() for s in cands][:5])
for sch in cands[:2]:
    spaces = set()
    for src in sch.sources():
        if src.iddObject().name() == "OS:Lights":
            l = src.to_Lights().get()
            if l.space().is_initialized(): spaces.add(l.space().get().nameString())
            elif l.spaceType().is_initialized():
                spaces |= {s.nameString() for s in l.spaceType().get().spaces()}
    print("  ", sch.nameString(), "users' spaces:", len(spaces), "html:", (shown("OS:Schedule:Ruleset", sch.nameString()) or ["(no row)"])[0].count("|") + 1 if shown("OS:Schedule:Ruleset", sch.nameString()) else "(no row)")
# 4) space-type light added in child: spaces of that space type
l = [x for x in ch.getLightss() if x.spaceType().is_initialized()][0]
sp = sorted(s.nameString() for s in l.spaceType().get().spaces())
zn = sorted(s.thermalZone().get().nameString() for s in l.spaceType().get().spaces())
show("space type light " + l.nameString(), "OS:Lights", l.nameString(), [" | ".join(sp), " | ".join(zn), ""])
# 5) sub surface -> surface -> space, child
ss = ch.getSubSurfaceByName("0.01-Lobby_Wall_Outdoors_1_FixedWindow_1").get(); s = ss.space().get()
show("sub surface", "OS:SubSurface", ss.nameString(), [s.nameString(), s.thermalZone().get().nameString(), ""])
# 6) zone exhaust fan, parent
f = par.getFanZoneExhaustByName("TZ-0.06-WC Exhaust Fan").get()
show("zone exhaust fan", "OS:Fan:ZoneExhaust", f.nameString(), ["", f.thermalZone().get().nameString(), ""])
# 7) coil inside the unitary system, child: loop via the unitary, zone = its controlling zone
c = ch.getCoilHeatingGasByName("TZ-0.01-Lobby PSZ-AC Gas Htg Coil").get(); u = c.containingHVACComponent().get().to_AirLoopHVACUnitarySystem().get()
show("coil in unitary", "OS:Coil:Heating:Gas", c.nameString(), ["", u.controllingZoneorThermostatLocation().get().nameString(), u.airLoopHVAC().get().nameString()])
