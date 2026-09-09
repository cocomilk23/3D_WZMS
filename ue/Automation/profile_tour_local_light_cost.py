"""PIE-only temporary local-light/shadow cost experiment; never saves scene assets.

Run in a fresh editor session after the standalone owner test has ended. Variants
intentionally change lighting for diagnosis, and are NOT proposed visual settings.
Baseline is repeated between variants to expose temporal/streaming drift.
"""
import builtins,json,math,time,traceback,unreal
from pathlib import Path

assert not getattr(builtins,'_wzms_light_cost_running',False),'A lighting experiment is already active'
root=Path(unreal.Paths.project_dir()).resolve()
sub=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
world=sub.get_game_world();assert world,'Requires an actual PIE game world'
assert world != sub.get_editor_world(),'Never mutate the saved editor world'
pc=unreal.GameplayStatics.get_player_controller(world,0)
pawn=unreal.GameplayStatics.get_player_pawn(world,0);hud=pc.get_hud()
assert hud.get_class().get_name()=='BP_WZMS_TourHUD_C'
assert not pawn.get_editor_property('Flying'),'Start from walking mode'
performance_settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'))
previous_throttle=performance_settings.get_editor_property('bThrottleCPUWhenNotForeground')
previous={'position':pawn.get_actor_location(),'rotation':pc.get_control_rotation(),'menu':bool(hud.get_editor_property('MenuOpen')),'view_target':pc.get_view_target()}
movement=pawn.get_component_by_class(unreal.CharacterMovementComponent)
previous['movement_mode']=movement.movement_mode
lights=[]
for actor in unreal.GameplayStatics.get_all_actors_of_class(world,unreal.Actor):
 if not actor.get_actor_label().startswith(('InteriorLight_','Tour_InteriorLight_','Tour_InteriorBounce_')):continue
 component=actor.get_component_by_class(unreal.LocalLightComponent)
 if component:
  lights.append({'component':component,'name':actor.get_actor_label(),'visible':bool(component.get_editor_property('visible')),'cast_shadows':bool(component.get_editor_property('cast_shadows')),'radius_cm':float(component.get_editor_property('attenuation_radius'))})
assert lights,'No authored local lights found'
source=json.loads(Path('E:/3D_WZMS/builds/v043_ue_bundle/scene_reference.json').read_text(encoding='utf8'))
destinations=json.loads((root.parent/'SourceReference/tour_destinations.json').read_text(encoding='utf8'))['destinations']
points=[]
library=next(p for p in destinations if p['index']==18)
points.append(('Library',unreal.Vector(*library['position_cm']),unreal.Rotator(pitch=0,yaw=library['yaw_ue'],roll=0)))
camera=next(c for c in source['cameras'] if c['name']=='150_Gym_upper_sports_hall')
m=camera['world_matrix'];direction=(-m[0][2],m[1][2],-m[2][2])
points.append(('GymUpper',unreal.Vector(m[0][3]*100,-m[1][3]*100,m[2][3]*100-80),unreal.Rotator(pitch=math.degrees(math.atan2(direction[2],math.hypot(direction[0],direction[1]))),yaw=math.degrees(math.atan2(direction[1],direction[0])),roll=0)))
variants=['baseline_before','local_shadows_off','baseline_middle','local_lights_off','baseline_after']
steps=[(point,variant) for point in points for variant in variants]
stamp=time.strftime('%Y%m%d_%H%M%S');output=root.parent/'Reports'/f'tour_local_light_cost_{stamp}.json'
report={'complete':False,'diagnostic_only':True,'scene_saved':False,'warmup_seconds':8,'capture_seconds':15,'quality':pawn.get_editor_property('QualityPreset'),'resolution_scale':list(unreal.GameUserSettings.get_game_user_settings().get_resolution_scale_information_ex()),'fps_cap':unreal.SystemLibrary.get_console_variable_float_value('t.MaxFPS'),'lights':[{k:v for k,v in row.items() if k!='component'} for row in lights],'captures':[],'limitations':['Light-off and shadow-off views intentionally differ visually; neither is a delivery setting.','Total GPU deltas include secondary effects and do not identify an individual renderer pass.','Repeated baselines must be compared before interpreting variant differences.']}
state={};handle=[None]

def record():output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def restore_lights():
 for row in lights:
  row['component'].set_visibility(row['visible'])
  row['component'].set_cast_shadows(row['cast_shadows'])
def enter(index):
 restore_lights()
 (name,position,rotation),variant=steps[index]
 if variant=='local_shadows_off':
  for row in lights:row['component'].set_cast_shadows(False)
 elif variant=='local_lights_off':
  for row in lights:row['component'].set_visibility(False)
 pawn.set_actor_location(position,False,True);pc.set_control_rotation(rotation)
 state.update(index=index,start=time.monotonic(),phase='warmup',csv_running=False)
 report['current']={'view':name,'variant':variant};record()
def finish(error=None):
 try:
  if state.get('csv_running'):unreal.SystemLibrary.execute_console_command(world,'csvprofile stop')
  restore_lights()
  report['restored_lights']=all(bool(r['component'].get_editor_property('visible'))==r['visible'] and bool(r['component'].get_editor_property('cast_shadows'))==r['cast_shadows'] for r in lights)
  pawn.set_actor_location(previous['position'],False,True);pc.set_control_rotation(previous['rotation'])
  movement.set_movement_mode(previous['movement_mode']);pc.set_view_target_with_blend(previous['view_target'],0)
  hud.call_method('SetTourMenu',(previous['menu'],))
 except Exception:
  report['restoration_error']=traceback.format_exc()
 finally:
  performance_settings.set_editor_property('bThrottleCPUWhenNotForeground',previous_throttle)
  if handle[0] is not None:unreal.unregister_slate_post_tick_callback(handle[0])
  builtins._wzms_light_cost_running=False
  report.update(complete=True,error=error,measurement_completed=error is None and len(report['captures'])==len(steps));record()
def tick(dt):
 try:
  assert sub.get_game_world()==world,'PIE ended during measurement'
  elapsed=time.monotonic()-state['start']
  report['viewport_pixels']=[hud.get_editor_property('UIWidth'),hud.get_editor_property('UIHeight')]
  if state['phase']=='warmup' and elapsed>=8:
   state['csv_before']={p for p in (root/'Saved/Profiling/CSV').glob('*.csv')}
   unreal.SystemLibrary.execute_console_command(world,'csvprofile start')
   state.update(phase='capture',start=time.monotonic(),csv_running=True)
  elif state['phase']=='capture' and elapsed>=15:
   unreal.SystemLibrary.execute_console_command(world,'csvprofile stop')
   state.update(phase='flush',start=time.monotonic(),csv_running=False)
  elif state['phase']=='flush' and elapsed>=3:
   files=[p for p in (root/'Saved/Profiling/CSV').glob('*.csv') if p not in state['csv_before']]
   if not files:
    assert elapsed<30,'CSV did not flush within 30 seconds'
    return
   newest=max(files,key=lambda p:p.stat().st_mtime)
   report['captures'].append({**report['current'],'csv':str(newest)})
   if state['index']+1<len(steps):enter(state['index']+1)
   else:finish()
 except Exception:finish(traceback.format_exc())

builtins._wzms_light_cost_running=True
try:
 performance_settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
 hud.call_method('SetTourMenu',(False,));pc.set_view_target_with_blend(pawn,0)
 movement.set_movement_mode(unreal.MovementMode.MOVE_FLYING)
 enter(0);handle[0]=unreal.register_slate_post_tick_callback(tick)
 print('Temporary lighting experiment started; inspect complete and restoration fields:',output)
except Exception:
 finish(traceback.format_exc());raise
