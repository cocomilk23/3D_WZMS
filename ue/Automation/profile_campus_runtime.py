"""Record separate ground, aerial and indoor CSV captures in the assembled PIE map."""
import unreal,json,time,traceback
from pathlib import Path
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert world
pawn=unreal.GameplayStatics.get_player_pawn(world,0);pc=unreal.GameplayStatics.get_player_controller(world,0);assert pawn
root=Path(unreal.Paths.project_dir()).resolve();dest=root.parent/'Reports/campus_profile_captures.json'
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));old=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
source=json.loads(Path('E:/3D_WZMS/builds/v043_ue_bundle/scene_reference.json').read_text(encoding='utf8'))
import math
cases=[('Ground',None),('Aerial','182_Refined_whole_campus'),('Interior','164_Canteen_dining_hall')]
results={'complete':False,'captures':[],'fps_cap':60,'gameplay_fov':80,'mode':'UE 5.8 PIE; full campus loaded'};holder=[None];state={}
unreal.SystemLibrary.execute_console_command(world,'t.MaxFPS 60')
def enter(index):
    name,camera=cases[index]
    if camera is None:pawn.call_method('ReturnToGate')
    else:
        if not pawn.get_editor_property('Flying'):pawn.call_method('ToggleFlight')
        row=next(c for c in source['cameras'] if c['name']==camera);m=row['world_matrix'];d=(-m[0][2],m[1][2],-m[2][2])
        pawn.set_actor_location(unreal.Vector(m[0][3]*100,-m[1][3]*100,m[2][3]*100-80),False,True)
        pc.set_control_rotation(unreal.Rotator(pitch=math.degrees(math.atan2(d[2],math.hypot(d[0],d[1]))),yaw=math.degrees(math.atan2(d[1],d[0])),roll=0))
    state.update(index=index,start=time.perf_counter(),phase='warmup')
def finish():
    settings.set_editor_property('bThrottleCPUWhenNotForeground',old);pawn.call_method('ReturnToGate');unreal.unregister_slate_post_tick_callback(holder[0]);dest.write_text(json.dumps(results,indent=2))
def tick(dt):
    try:
        elapsed=time.perf_counter()-state['start'];name,_=cases[state['index']]
        if state['phase']=='warmup' and elapsed>=5:
            state['before']={p.name for p in (root/'Saved/Profiling/CSV').glob('*.csv')}
            unreal.SystemLibrary.execute_console_command(world,'csvprofile start');state.update(start=time.perf_counter(),phase='capture')
        elif state['phase']=='capture' and elapsed>=12:
            unreal.SystemLibrary.execute_console_command(world,'csvprofile stop');state.update(start=time.perf_counter(),phase='flush')
        elif state['phase']=='flush' and elapsed>=3:
            files=[p for p in (root/'Saved/Profiling/CSV').glob('*.csv') if p.name not in state['before']];assert files
            latest=max(files,key=lambda p:p.stat().st_mtime);results['captures'].append({'view':name,'csv':str(latest),'warmup_seconds':5,'capture_seconds':12})
            if state['index']+1<len(cases):enter(state['index']+1)
            else:results['complete']=True;finish()
    except Exception:
        results['error']=traceback.format_exc();finish()
enter(0);holder[0]=unreal.register_slate_post_tick_callback(tick)
