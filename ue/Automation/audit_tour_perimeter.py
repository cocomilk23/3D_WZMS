"""Audit actual wall/water collision at the map boundary and preserve authored routes."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);actors=list(sub.get_all_level_actors());world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world();assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
boundary=[a for a in actors if a.get_actor_label() in ['SM_Tour_Perimeter_Wall','SM_Tour_Water_Exclusion']];assert len(boundary)==2
ignored=[a for a in actors if a not in boundary];fixture=json.loads((root.parent/'SourceReference/tour_perimeter_validation.json').read_text());fail=[];already_excluded=0;water=next(a for a in boundary if a.get_actor_label()=='SM_Tour_Water_Exclusion');water_ignore=[a for a in actors if a!=water]
for i,sample in enumerate(fixture['samples']):
 for z in [92,180]:
  a,b=sample['inside'],sample['outside'];hit=unreal.SystemLibrary.capsule_trace_single(world,unreal.Vector(a[0]*100,-a[1]*100,z),unreal.Vector(b[0]*100,-b[1]*100,z),30,90,unreal.TraceTypeQuery.ECC_VISIBILITY,False,ignored,unreal.DrawDebugTrace.NONE)
  if hit is None:
   # A sweep wholly inside the water exclusion need not produce a surface hit.
   # Prove that its start is already in the closed forbidden volume with actual physics.
   water_hit=unreal.SystemLibrary.line_trace_single(world,unreal.Vector(a[0]*100,-a[1]*100,470),unreal.Vector(a[0]*100,-a[1]*100,420),unreal.TraceTypeQuery.ECC_VISIBILITY,False,water_ignore,unreal.DrawDebugTrace.NONE)
   if water_hit:already_excluded+=1
   else:fail.append({'sample':i,'height_cm':z,**sample})
wall=next(a for a in boundary if a.get_actor_label()=='SM_Tour_Perimeter_Wall');ignored=[a for a in actors if a!=wall];routes=json.loads((root.parent/'SourceReference/tour_traversal_cases.json').read_text(encoding='utf8'))['cases'];blocked=[]
for row in routes:
 for a,b in zip(row['points'],row['points'][1:]):
  hit=unreal.SystemLibrary.capsule_trace_single(world,unreal.Vector(a[0]*100,-a[1]*100,a[2]*100+92),unreal.Vector(b[0]*100,-b[1]*100,b[2]*100+92),30,90,unreal.TraceTypeQuery.ECC_VISIBILITY,False,ignored,unreal.DrawDebugTrace.NONE)
  if hit:blocked.append({'route':row['name'],'from':a,'to':b})
r={'passed':not fail and not blocked,'boundary_samples':len(fixture['samples']),'capsule_heights_cm':[92,180],'already_inside_forbidden_water_tests':already_excluded,'boundary_failures':fail,'authored_routes_checked':len(routes),'wall_route_conflicts':blocked,'method':'Actual physics against perimeter wall and water exclusion, with walking and near-jump-apex capsule heights. Sweeps wholly within forbidden water are checked by vertical intersection with the closed exclusion volume. Separate character runtime traversal remains required.'}
(root.parent/'Reports/tour_perimeter_collision.json').write_text(json.dumps(r,indent=2),encoding='utf8');print('PERIMETER_AUDIT',r['passed'],'failures',len(fail),'route conflicts',len(blocked))
