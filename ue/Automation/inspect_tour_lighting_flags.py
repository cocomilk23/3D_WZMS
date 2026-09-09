import unreal,json
from pathlib import Path
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert world
result={}
for name in ['r.DeferredLighting','ShowFlag.PointLights','ShowFlag.SpotLights','ShowFlag.RectLights','ShowFlag.DirectLighting','r.LightMaxDrawDistanceScale','r.ForwardShading','r.MegaLights.Allow','r.MegaLights.EnableForProject']:
 result[name]=unreal.SystemLibrary.get_console_variable_float_value(name)
Path(unreal.Paths.project_dir()).resolve().joinpath('Saved/Logs/tour_lighting_flags.json').write_text(json.dumps(result,indent=2))
