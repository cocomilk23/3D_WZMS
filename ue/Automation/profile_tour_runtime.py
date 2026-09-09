"""Record current tour performance with its HUD, measured viewport size, and five views."""
import unreal,json,time,traceback
from pathlib import Path
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert world
pawn=unreal.GameplayStatics.get_player_pawn(world,0);pc=unreal.GameplayStatics.get_player_controller(world,0);assert pawn
root=Path(unreal.Paths.project_dir()).resolve();dest=root.parent/'Reports/tour_profile_captures.json'
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));old=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
source=json.loads(Path('E:/3D_WZMS/builds/v043_ue_bundle/scene_reference.json').read_text(encoding='utf8'))
import math
cases=[('SouthGate',0),('Aerial','182_Refined_whole_campus'),('Library',18),('GymUpper','150_Gym_upper_sports_hall'),('Canteen',16)]
results={'complete':False,'captures':[],'fps_cap':60,'gameplay_fov':80,'mode':'UE 5.8 PIE; current complete campus, tour HUD, refined local lighting; not standalone certification'};holder=[None];state={}
unreal.SystemLibrary.execute_console_command(world,'t.MaxFPS 60')
hud=pc.get_hud();hud.set_editor_property('show_hud',True);hud.call_method('SetTourMenu',(False,));pc.set_view_target_with_blend(pawn,0)
results['quality']=pawn.get_editor_property('QualityPreset')
results['resolution_scale']=list(unreal.GameUserSettings.get_game_user_settings().get_resolution_scale_information_ex())
def enter(index):
    name,camera=cases[index]
    if isinstance(camera,int):hud.call_method('VisitTourPlace',(camera,))
    else:
        if not pawn.get_editor_property('Flying'):pawn.call_method('ToggleFlight')
        row=next(c for c in source['cameras'] if c['name']==camera);m=row['world_matrix'];d=(-m[0][2],m[1][2],-m[2][2])
        pawn.set_actor_location(unreal.Vector(m[0][3]*100,-m[1][3]*100,m[2][3]*100-80),False,True)
        pc.set_control_rotation(unreal.Rotator(pitch=math.degrees(math.atan2(d[2],math.hypot(d[0],d[1]))),yaw=math.degrees(math.atan2(d[1],d[0])),roll=0))
    state.update(index=index,start=time.perf_counter(),phase='warmup')
def finish():
    settings.set_editor_property('bThrottleCPUWhenNotForeground',old);hud.call_method('VisitTourPlace',(0,));hud.call_method('SetTourMenu',(True,));unreal.unregister_slate_post_tick_callback(holder[0]);dest.write_text(json.dumps(results,indent=2))
def tick(dt):
    try:
        elapsed=time.perf_counter()-state['start'];name,_=cases[state['index']]
        results['viewport_pixels']=[hud.get_editor_property('UIWidth'),hud.get_editor_property('UIHeight')]
        if state['phase']=='warmup' and elapsed>=5:
            state['before']={p.name for p in (root/'Saved/Profiling/CSV').glob('*.csv')}
            unreal.SystemLibrary.execute_console_command(world,'csvprofile start');state.update(start=time.perf_counter(),phase='capture')
        elif state['phase']=='capture' and elapsed>=20:
            unreal.SystemLibrary.execute_console_command(world,'csvprofile stop');state.update(start=time.perf_counter(),phase='flush')
        elif state['phase']=='flush' and elapsed>=3:
            files=[p for p in (root/'Saved/Profiling/CSV').glob('*.csv') if p.name not in state['before']];assert files
            latest=max(files,key=lambda p:p.stat().st_mtime);results['captures'].append({'view':name,'csv':str(latest),'warmup_seconds':5,'capture_seconds':20})
            if state['index']+1<len(cases):enter(state['index']+1)
            else:results['complete']=True;finish()
    except Exception:
        results['error']=traceback.format_exc();finish()
enter(0);holder[0]=unreal.register_slate_post_tick_callback(tick)
