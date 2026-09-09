"""Validate every named start using native travel functions; UI clicks are tested separately."""
import unreal,json,time,math,traceback
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert world
pc=unreal.GameplayStatics.get_player_controller(world,0);pawn=unreal.GameplayStatics.get_player_pawn(world,0);hud=pc.get_hud();movement=pawn.get_component_by_class(unreal.CharacterMovementComponent)
destinations=json.loads((root.parent/'SourceReference/tour_destinations.json').read_text(encoding='utf8'))['destinations'];report={'complete':False,'hud_class':hud.get_class().get_name(),'initial_menu_open':bool(hud.get_editor_property('MenuOpen')),'initial_paused':unreal.GameplayStatics.is_game_paused(world),'cases':[],'method':'Invoke actual HUD destination-travel function and observe the real pawn settling. This is not a substitute for mouse-click UI testing.'};out=root.parent/'Reports/tour_navigation_runtime.json';state={};handle=[None]
assert report['hud_class']=='BP_WZMS_TourHUD_C'
def enter(i):
 hud.call_method('VisitTourPlace',(i,));state.update(index=i,start=time.monotonic())
def tick(dt):
 try:
  if time.monotonic()-state['start']<1.5:return
  p=destinations[state['index']];position=pawn.get_actor_location();target=unreal.Vector(*p['position_cm']);error=(position-target).length();grounded=movement.movement_mode==unreal.MovementMode.MOVE_WALKING;angle=abs((pc.get_control_rotation().yaw-p['yaw_ue']+180)%360-180);menu=bool(hud.get_editor_property('MenuOpen'));paused=unreal.GameplayStatics.is_game_paused(world)
  passed=error<15 and grounded and angle<2 and not menu and not paused
  report['cases'].append({'name':p['name'],'index':p['index'],'passed':passed,'position_error_cm':error,'grounded':grounded,'heading_error_degrees':angle,'menu_open':menu,'paused':paused});out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
  if state['index']+1<len(destinations):enter(state['index']+1)
  else:
   pawn.call_method('SaveTourProgress');expected={'position_cm':list(pawn.get_editor_property('SafePosition').to_tuple()),'yaw':pawn.get_editor_property('SafeRotation').yaw,'quality':pawn.get_editor_property('QualityPreset'),'volume':pawn.get_editor_property('TourVolume')};(root/'Saved/Logs/tour_restart_expected.json').write_text(json.dumps(expected),encoding='utf8');report.update(complete=True,passed=all(p['passed'] for p in report['cases']) and report['initial_menu_open'] and report['initial_paused']);out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');hud.call_method('SetTourMenu',(True,));unreal.unregister_slate_post_tick_callback(handle[0])
 except Exception:
  report.update(complete=True,passed=False,error=traceback.format_exc());out.write_text(json.dumps(report,indent=2));unreal.unregister_slate_post_tick_callback(handle[0])
enter(0);handle[0]=unreal.register_slate_post_tick_callback(tick)
