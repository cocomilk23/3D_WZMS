"""Check actual water collision over the complete planned area and shore boundary."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();fixture=json.loads((root.parent/'SourceReference/tour_water_fixtures.json').read_text(encoding='utf8'));sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);actors=list(sub.get_all_level_actors());water=next(a for a in actors if a.get_actor_label()=='SM_Tour_Water_Exclusion');ignored=[a for a in actors if a!=water];world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
grid_fail=[];sweep_fail=[]
for x,y in fixture['water_grid']:
 hit=unreal.SystemLibrary.line_trace_single(world,unreal.Vector(x*100,-y*100,470),unreal.Vector(x*100,-y*100,420),unreal.TraceTypeQuery.ECC_VISIBILITY,False,ignored,unreal.DrawDebugTrace.NONE)
 if hit is None:grid_fail.append([x,y])
for row in fixture['boundary_sweeps']:
 a=row['outside'];b=row['inside'];hit=unreal.SystemLibrary.capsule_trace_single(world,unreal.Vector(a[0]*100,-a[1]*100,92),unreal.Vector(b[0]*100,-b[1]*100,92),30,90,unreal.TraceTypeQuery.ECC_VISIBILITY,False,ignored,unreal.DrawDebugTrace.NONE)
 if hit is None:sweep_fail.append(row)
r={'passed':not grid_fail and not sweep_fail,'water_grid_samples':len(fixture['water_grid']),'grid_spacing_m':fixture['grid_spacing_m'],'shore_capsule_sweeps':len(fixture['boundary_sweeps']),'grid_failures':grid_fail,'sweep_failures':sweep_fail,'reference_routes_outside_blocked_water':fixture['source_routes_clear'],'method':'Actual editor physics queries against only the hidden water exclusion actor; separate real-character attempts are also required.'}
(root.parent/'Reports/tour_water_collision_audit.json').write_text(json.dumps(r,indent=2));print('WATER_AUDIT',r['passed'],r['water_grid_samples'],r['shore_capsule_sweeps'])
hit=unreal.SystemLibrary.line_trace_single(world,unreal.Vector(-1450,3000,300),unreal.Vector(-1450,3000,-100),unreal.TraceTypeQuery.ECC_VISIBILITY,True,[water],unreal.DrawDebugTrace.NONE)
(root/'Saved/Logs/hit_fields.json').write_text(json.dumps(hit.to_dict(),default=str,indent=2))
