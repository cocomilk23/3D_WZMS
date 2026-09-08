"""Capture actual PIE timing through Unreal's CSV profiler."""
import unreal,json,time
from pathlib import Path
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert world
assert unreal.GameplayStatics.get_player_pawn(world,0)
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'))
old=settings.get_editor_property('bThrottleCPUWhenNotForeground')
settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
unreal.SystemLibrary.execute_console_command(world,'t.MaxFPS 60')
unreal.SystemLibrary.execute_console_command(world,'stat unit')
unreal.SystemLibrary.execute_console_command(world,'stat fps')
unreal.SystemLibrary.execute_console_command(world,'csvprofile start')
start=time.perf_counter();holder=[None]
def tick(dt):
    if time.perf_counter()-start<12:return
    unreal.SystemLibrary.execute_console_command(world,'csvprofile stop')
    settings.set_editor_property('bThrottleCPUWhenNotForeground',old)
    unreal.unregister_slate_post_tick_callback(holder[0])
    (Path(unreal.Paths.project_dir()).resolve().parent/'Reports/profile_capture.json').write_text(json.dumps({'capture_requested':True,'duration_seconds':time.perf_counter()-start,'fps_cap':60,'mode':'Play In Editor','note':'Inspect the saved CSV and record viewport resolution; this is not a packaged-game benchmark.'},indent=2))
holder[0]=unreal.register_slate_post_tick_callback(tick)
