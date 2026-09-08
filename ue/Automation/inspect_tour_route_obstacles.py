"""Read-only physics probes at failed continuous-route locations."""
import unreal,json,math
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();r=json.loads((root.parent/'Reports/tour_complete_routes_runtime.json').read_text(encoding='utf8'));world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();rows=[]
def desc(hit):
 if not hit:return None
 d=hit.to_dict();c=d['hit_component'];a=c.get_owner() if c else None
 return {'blocking':d['blocking_hit'],'point':list(d['impact_point'].to_tuple()),'normal':list(d['impact_normal'].to_tuple()),'actor':a.get_actor_label() if a else None,'mesh':c.static_mesh.get_path_name() if isinstance(c,unreal.StaticMeshComponent) and c.static_mesh else None,'face_index':d['face_index'],'initial_overlap':d['initial_overlap']}
for case in r['cases']:
 if case['passed']:continue
 pos=unreal.Vector(*case['position_cm']);point=case['route_points_blender_m'][case['waypoint_reached']+1];target=unreal.Vector(point[0]*100,-point[1]*100,point[2]*100+92);dx,dy=target.x-pos.x,target.y-pos.y;length=math.hypot(dx,dy);d=unreal.Vector(dx/max(length,.01),dy/max(length,.01),0);probes=[]
 for lift in [0,5,10,20,50]:
  for complex in [False,True]:
   a=pos-d*40+unreal.Vector(0,0,lift);b=pos+d*220+unreal.Vector(0,0,lift)
   hit=unreal.SystemLibrary.capsule_trace_single(world,a,b,30,90,unreal.TraceTypeQuery.ECC_VISIBILITY,complex,[],unreal.DrawDebugTrace.NONE)
   probes.append({'lift_cm':lift,'complex':complex,'hit':desc(hit)})
 floors=[]
 for step in [-100,-50,0,25,50,100,150,200]:
  p=pos+d*step;hit=unreal.SystemLibrary.line_trace_single(world,unreal.Vector(p.x,p.y,80),unreal.Vector(p.x,p.y,-50),unreal.TraceTypeQuery.ECC_VISIBILITY,True,[],unreal.DrawDebugTrace.NONE);floors.append({'step_cm':step,'hit':desc(hit)})
 rows.append({'route':case['name'],'position_cm':case['position_cm'],'direction':list(d.to_tuple()),'capsules':probes,'floors':floors})
(root/'Saved/Logs/tour_obstacle_probes.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
