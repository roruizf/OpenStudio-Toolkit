"""Which inheritance levels reach a Space's loads, and does OpenStudio's total handle every design method."""
import openstudio
from openstudio_toolkit._sdk import opt
M = openstudio.model
m = M.Model()
pts = lambda x: openstudio.Point3dVector([openstudio.Point3d(x,0,0),openstudio.Point3d(x,10,0),openstudio.Point3d(x+10,10,0),openstudio.Point3d(x+10,0,0)])
b = m.getBuilding()
bst = M.SpaceType(m); bst.setName("BuildingST")
ld = M.LightsDefinition(m); ld.setWattsperSpaceFloorArea(2.0); M.Lights(ld).setSpaceType(bst)
pd = M.PeopleDefinition(m); pd.setPeopleperSpaceFloorArea(0.1); M.People(pd).setSpaceType(bst)
b.setSpaceType(bst)
s1 = M.Space.fromFloorPrint(pts(0), 3, m).get(); s1.setName("no own space type")
s2 = M.Space.fromFloorPrint(pts(20), 3, m).get(); s2.setName("own space type")
st = M.SpaceType(m); st.setName("OwnST"); s2.setSpaceType(st)
ld2 = M.LightsDefinition(m); ld2.setWattsperPerson(10); M.Lights(ld2).setSpaceType(st)
pd2 = M.PeopleDefinition(m); pd2.setNumberofPeople(3); M.People(pd2).setSpace(s2)
for s in (s1, s2):
    t = opt(s.spaceType())
    print(f"{s.nameString()}: field={opt(s.getString(2))!r} spaceType()={t.nameString() if t else None} "
          f"defaulted={s.isSpaceTypeDefaulted()} lightingPower={s.lightingPower()} people={s.numberOfPeople()} area={s.floorArea()}")
story = M.BuildingStory(m); s1.setBuildingStory(story)
dss = M.DefaultScheduleSet(m); sch = M.ScheduleRuleset(m); sch.setName("story lighting sch"); dss.setLightingSchedule(sch); story.setDefaultScheduleSet(dss)
l1 = M.Lights(M.LightsDefinition(m)); l1.setSpace(s1)
sc = opt(l1.schedule())
print("light on s1, schedule from story's set:", sc.nameString() if sc else None, "| field:", opt(l1.getString(4)))
