"""Resolve named tour starts against actual floor and capsule collision before exposing them."""
import unreal,json,math
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world();assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
raw=[('南大门',[-14.5,-30,0],-90),('南大门广场',[-8.667,21.667,0],-90),('网球场',[51,-15,0],-90),('荷屿',[100,15,0],180),('德涵楼·贯真楼',[18,47,0],-90),('道司前路',[-81,136,0],-90),('榕屿',[-29,106,0],0),('籀园学堂',[-27,130.5,0],180),('校友风采',[-42,162,0],-90),('步青广场',[3,164,0],0),('南田路',[-20,218,0],-90),('西门',[-120,169,0],0),('操场',[-44.23,322.19,0],90),('篮球场',[0,259,0],-90),('体育馆',[-76,392,1.08],-90),('北门',[54,367,0],-90),('食堂',[124.4,351.3,1.04],-90),('竹屿',[143,294,0],0),('图书馆',[116,155,0],0),('数学馆',[147,121,0],0),('校史馆',[247,120,0],0),('桃花岛',[211,82,0],90),('梅花岛',[282,112,0],0),('橘岛',[346,115,0],0)]
rows=[]
for index,(name,point,yaw) in enumerate(raw):
 found=None
 for radius in [0,.6,1.2,1.8]:
  for angle in ([0] if radius==0 else range(0,360,45)):
   x=(point[0]+radius*math.cos(math.radians(angle)))*100;y=-(point[1]+radius*math.sin(math.radians(angle)))*100
   hit=unreal.SystemLibrary.line_trace_single(world,unreal.Vector(x,y,point[2]*100+130),unreal.Vector(x,y,point[2]*100-80),unreal.TraceTypeQuery.ECC_VISIBILITY,False,[],unreal.DrawDebugTrace.NONE)
   if not hit:continue
   h=hit.to_dict();foot=h['impact_point']
   if h['impact_normal'].z<.8 or abs(foot.z-point[2]*100)>55:continue
   centre=foot+unreal.Vector(0,0,94)
   block=unreal.SystemLibrary.capsule_trace_single(world,centre,centre+unreal.Vector(0,0,1),30,90,unreal.TraceTypeQuery.ECC_VISIBILITY,False,[],unreal.DrawDebugTrace.NONE)
   if not block:found=centre;break
  if found:break
 assert found,(name,point)
 rows.append({'index':index,'name':name,'source_floor_point_m':point,'position_cm':list(found.to_tuple()),'yaw_ue':yaw,'map_uv':[(found.x/100+200)/620,(495+found.y/100)/620],'floor_and_capsule_verified':True})
(root.parent/'SourceReference/tour_destinations.json').write_text(json.dumps({'count':len(rows),'method':'Actual floor trace plus a clear standing capsule, within 1.8m of the selected reference location. Continuous access and UI travel are tested separately.','destinations':rows},ensure_ascii=False,indent=2),encoding='utf8')
