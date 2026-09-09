"""Continuous real-character stair traversal, with stall evidence and no waypoint teleporting."""
import unreal,json,time,math,traceback
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert world
pawn=unreal.GameplayStatics.get_player_pawn(world,0);pc=unreal.GameplayStatics.get_player_controller(world,0);move=pawn.get_component_by_class(unreal.CharacterMovementComponent)
request=root/'Saved/Logs/traversal_request.json';req=json.loads(request.read_text()) if request.exists() else {}
cases=req.get('cases',[{'name':'Library interior ascent and return','points':[[116,155,0],[128.7,155,4.25],[136,155,4.25],[128.7,155,4.25],[119,155,0],[116,155,0]]},{'name':'Library exterior ascent to upper entry','points':[[104,133,0],[104,142.2,4.25],[110,142.4,4.25],[110,155,4.25],[117,155,4.25]]}])
output=root.parent/'Reports'/req.get('report','tour_stair_baseline.json');results={'complete':False,'cases':[],'method':'Actual CharacterMovement following connected waypoints; teleport only at each route start. Segment/stall deadlines use world simulation time so editor loading stalls do not count as blocked walking.'};state={};holder=[None]
def simulation_time():return unreal.GameplayStatics.get_time_seconds(world)
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));old=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
def enter(i):
 if pawn.get_editor_property('Flying'):pawn.call_method('ToggleFlight')
 move.stop_movement_immediately();move.set_movement_mode(unreal.MovementMode.MOVE_WALKING);p=cases[i]['points'][0]
 pawn.set_actor_location(unreal.Vector(p[0]*100,-p[1]*100,p[2]*100+94),False,True)
 state.update(case=i,waypoint=1,start=simulation_time(),phase='settle',samples=[],last_sample=0,anchor=pawn.get_actor_location(),last_progress=simulation_time())
def finish_case(passed,reason):
 pos=pawn.get_actor_location();hit=unreal.SystemLibrary.capsule_trace_single(world,pos,pos+state.get('direction',unreal.Vector(1,0,0))*100,29,88,unreal.TraceTypeQuery.ECC_VISIBILITY,True,[pawn],unreal.DrawDebugTrace.NONE)
 results['cases'].append({'name':cases[state['case']]['name'],'route_points_blender_m':cases[state['case']]['points'],'passed':passed,'reason':reason,'waypoint_reached':state['waypoint']-1,'position_cm':list(pos.to_tuple()),'forward_hit':hit.export_text() if hit else None,'samples':state['samples']})
 output.write_text(json.dumps(results,indent=2))
 if state['case']+1<len(cases):enter(state['case']+1)
 else:
  results['complete']=True;results['passed']=all(c['passed'] for c in results['cases']);output.write_text(json.dumps(results,indent=2));pawn.call_method('ReturnToGate');settings.set_editor_property('bThrottleCPUWhenNotForeground',old);unreal.unregister_slate_post_tick_callback(holder[0])
def tick(dt):
 try:
  now=simulation_time()
  if state['phase']=='settle':
   if now-state['start']<1:return
   state.update(phase='walk',start=now,last_progress=now)
  pos=pawn.get_actor_location();point=cases[state['case']]['points'][state['waypoint']];target=unreal.Vector(point[0]*100,-point[1]*100,point[2]*100+92);delta=target-pos;distance=math.hypot(delta.x,delta.y)
  if distance<45 and abs(delta.z)<50:
   state['waypoint']+=1;state['start']=now;state['last_progress']=now
   if state['waypoint']==len(cases[state['case']]['points']):finish_case(True,'all connected waypoints reached');return
   return
  direction=unreal.Vector(delta.x/max(distance,.001),delta.y/max(distance,.001),0);state['direction']=direction
  pc.set_control_rotation(unreal.Rotator(pitch=0,yaw=math.degrees(math.atan2(direction.y,direction.x)),roll=0));pawn.add_movement_input(direction,.65,False)
  if now-state['last_sample']>.2:
   state['samples'].append({'t':round(now-state['start'],2),'waypoint':state['waypoint'],'position_cm':list(pos.to_tuple()),'mode':str(move.movement_mode)})
   state['last_sample']=now
  if (pos-state['anchor']).length()>15:state['anchor']=pos;state['last_progress']=now
  if now-state['last_progress']>2.5 or now-state['start']>22:finish_case(False,'stalled or segment timed out')
 except Exception:
  results.update(error=traceback.format_exc(),complete=True,passed=False);output.write_text(json.dumps(results,indent=2));settings.set_editor_property('bThrottleCPUWhenNotForeground',old);unreal.unregister_slate_post_tick_callback(holder[0])
enter(0);holder[0]=unreal.register_slate_post_tick_callback(tick)
