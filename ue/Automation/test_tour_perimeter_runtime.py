"""Real-character wall approaches and jump attempts, with grounded final positions."""
import unreal,json,time,math,traceback
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert world
pawn=unreal.GameplayStatics.get_player_pawn(world,0);pc=unreal.GameplayStatics.get_player_controller(world,0);movement=pawn.get_component_by_class(unreal.CharacterMovementComponent)
cases=json.loads((root.parent/'SourceReference/tour_perimeter_runtime_cases.json').read_text())['cases'];out=root.parent/'Reports/tour_perimeter_runtime.json';report={'complete':False,'cases':[],'method':'Real character walking toward perimeter walls, then jumping; no teleport except start of each independent case.'};state={};handle=[None]
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));old=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
def enter(i):
 if pawn.get_editor_property('Flying'):pawn.call_method('ToggleFlight')
 movement.stop_movement_immediately();movement.set_movement_mode(unreal.MovementMode.MOVE_WALKING);p=cases[i]['inside'];pawn.set_actor_location(unreal.Vector(p[0]*100,-p[1]*100,90),False,True);a,b=cases[i]['inside'],cases[i]['outside'];dx,dy=b[0]-a[0],-(b[1]-a[1]);length=math.hypot(dx,dy);direction=unreal.Vector(dx/length,dy/length,0);pc.set_control_rotation(unreal.Rotator(pitch=0,yaw=math.degrees(math.atan2(dy,dx)),roll=0));state.update(i=i,start=time.monotonic(),direction=direction,jumped=False,samples=[],last_sample=0,initial=pawn.get_actor_location())
def tick(dt):
 try:
  t=time.monotonic()-state['start'];pos=pawn.get_actor_location()
  if t>1 and t<5:pawn.add_movement_input(state['direction'],1,False)
  if t>2.5 and not state['jumped']:pawn.jump();state['jumped']=True
  if t-state['last_sample']>.2:state['samples'].append({'t':round(t,2),'position_cm':list(pos.to_tuple()),'mode':str(movement.movement_mode)});state['last_sample']=t
  if t<6:return
  travelled=(pos-state['initial']).dot(state['direction']);escaped=travelled>200;grounded=movement.movement_mode==unreal.MovementMode.MOVE_WALKING and pos.z>60
  passed=not escaped and grounded and travelled>20
  report['cases'].append({'name':cases[state['i']]['name'],'passed':passed,'escaped':escaped,'grounded':grounded,'travelled_toward_wall_cm':travelled,'final_position_cm':list(pos.to_tuple()),'samples':state['samples']});out.write_text(json.dumps(report,indent=2))
  if state['i']+1<len(cases):enter(state['i']+1)
  else:
   report.update(complete=True,passed=all(c['passed'] for c in report['cases']));out.write_text(json.dumps(report,indent=2));pawn.call_method('ReturnToGate');settings.set_editor_property('bThrottleCPUWhenNotForeground',old);unreal.unregister_slate_post_tick_callback(handle[0])
 except Exception:
  report.update(complete=True,passed=False,error=traceback.format_exc());out.write_text(json.dumps(report,indent=2));settings.set_editor_property('bThrottleCPUWhenNotForeground',old);unreal.unregister_slate_post_tick_callback(handle[0])
enter(0);handle[0]=unreal.register_slate_post_tick_callback(tick)
