"""Load the campus and read the tested VSM light limit for the focused flicker review."""
import unreal,json
from pathlib import Path
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).load_level('/Game/WZMS/Maps/L_WZMS_Campus')
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
name='r.Shadow.Virtual.OnePassProjection.MaxLightsPerPixel'
before=unreal.SystemLibrary.get_console_variable_int_value(name)
unreal.SystemLibrary.execute_console_command(world,name+' 32')
after=unreal.SystemLibrary.get_console_variable_int_value(name);assert after==32
root=Path(unreal.Paths.project_dir()).resolve()
(root.parent/'Reports/flicker_shadow_capacity.json').write_text(json.dumps({'variable':name,'before_runtime':before,'after_runtime':after,'reason':'Previous actual runtime logs report VSM One Pass Projection max lights overflow. Raise supported capacity without removing lights or shadows.','reference':'https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-console-variables-reference','temporal_visual_validation_pending':True},indent=2)+'\n',encoding='utf8')
