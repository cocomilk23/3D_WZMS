"""Drive the actual tour pawn toward twelve shoreline areas and verify exclusion."""
import unreal,json,time,math,traceback
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert world
pawn=unreal.GameplayStatics.get_player_pawn(world,0);pc=unreal.GameplayStatics.get_player_controller(world,0);move=pawn.get_component_by_class(unreal.CharacterMovementComponent);actors=unreal.GameplayStatics.get_all_actors_of_class(world,unreal.StaticMeshActor);water=next(a for a in actors if a.get_actor_label()=='SM_Tour_Water_Exclusion')
fixture=json.loads((root.parent/'SourceReference/tour_water_fixtures.json').read_text());geometry=json.loads((root.parent/'SourceReference/tour_terrain_plan.json').read_text())['blocked_water'];polys=geometry['coordinates'] if geometry['type']=='MultiPolygon' else [geometry['coordinates']]
output=root.parent/'Reports/tour_water_runtime.json';results={'complete':False,'tests':[],'method':'Actual pawn movement toward the water for three seconds at each of twelve shore areas, after finding a clear standing location.'};state={};holder=[None]
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));old=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
def ring_contains(x,y,ring):
 inside=False
 for a,b in zip(ring,ring[1:]):
  if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:inside=not inside
 return inside
def is_water(v):
 x,y=v.x/100,-v.y/100
 return any(ring_contains(x,y,p[0]) and not any(ring_contains(x,y,h) for h in p[1:]) for p in polys)
def finish():
 results.update(complete=True,passed=all(r['passed'] for r in results['tests']) and len(results['tests'])==len(fixture['runtime']));output.write_text(json.dumps(results,indent=2));pawn.call_method('ReturnToGate');settings.set_editor_property('bThrottleCPUWhenNotForeground',old);unreal.unregister_slate_post_tick_callback(holder[0])
def enter(i):
 row=fixture['runtime'][i];chosen=None
 for c in row['candidates']:
  x,y=c['outside'];hit=unreal.SystemLibrary.line_trace_single(world,unreal.Vector(x*100,-y*100,200),unreal.Vector(x*100,-y*100,-110),unreal.TraceTypeQuery.ECC_VISIBILITY,False,[pawn,water],unreal.DrawDebugTrace.NONE)
  if hit is None:continue
  h=hit.to_dict();foot=h['impact_point']
  if h['impact_normal'].z<.85 or not -105<foot.z<40:continue
  centre=foot+unreal.Vector(0,0,94);obstacle=unreal.SystemLibrary.capsule_trace_single(world,centre,centre+unreal.Vector(0,0,1),30,90,unreal.TraceTypeQuery.ECC_VISIBILITY,False,[pawn],unreal.DrawDebugTrace.NONE)
  if obstacle:continue
  chosen=(c,centre);break
 if chosen is None:
  results['tests'].append({'location':row['name'],'passed':False,'reason':'No clear standing candidate; this area needs inspection.'})
  if i+1<len(fixture['runtime']):enter(i+1)
  else:finish()
  return
 c,centre=chosen
 if pawn.get_editor_property('Flying'):pawn.call_method('ToggleFlight')
 move.stop_movement_immediately();move.set_movement_mode(unreal.MovementMode.MOVE_WALKING);pawn.set_actor_location(centre,False,True);n=c['inward'];direction=unreal.Vector(n[0],-n[1],0);pc.set_control_rotation(unreal.Rotator(pitch=0,yaw=math.degrees(math.atan2(direction.y,direction.x)),roll=0))
 state.update(index=i,start=time.monotonic(),phase='settle',origin=centre,direction=direction,samples=[],entered_water=False,max_distance_cm=0)
def tick(dt):
 try:
  now=time.monotonic();elapsed=now-state['start']
  if state['phase']=='settle':
   if elapsed<1:return
   state.update(phase='walk',start=now);return
  pos=pawn.get_actor_location();state['entered_water']|=is_water(pos);state['max_distance_cm']=max(state['max_distance_cm'],(pos-state['origin']).length());pawn.add_movement_input(state['direction'],.65,False)
  if len(state['samples'])==0 or elapsed>len(state['samples'])*.15:state['samples'].append(list(pos.to_tuple()))
  if elapsed<3:return
  on_floor=move.movement_mode==unreal.MovementMode.MOVE_WALKING;passed=not state['entered_water'] and state['max_distance_cm']<180 and on_floor
  results['tests'].append({'location':fixture['runtime'][state['index']]['name'],'passed':passed,'entered_blocked_water':state['entered_water'],'walking_on_floor':on_floor,'maximum_travel_cm':state['max_distance_cm'],'start_position_cm':list(state['origin'].to_tuple()),'end_position_cm':list(pos.to_tuple()),'trajectory_cm':state['samples']});output.write_text(json.dumps(results,indent=2))
  if state['index']+1<len(fixture['runtime']):enter(state['index']+1)
  else:finish()
 except Exception:
  results.update(error=traceback.format_exc(),passed=False,complete=True);output.write_text(json.dumps(results,indent=2));settings.set_editor_property('bThrottleCPUWhenNotForeground',old);unreal.unregister_slate_post_tick_callback(holder[0])
holder[0]=unreal.register_slate_post_tick_callback(tick);enter(0)
