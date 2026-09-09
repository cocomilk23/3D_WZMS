"""Runtime-only photometry probe; restore poses/shadows after isolated diagnostic tests."""
import unreal,json
from pathlib import Path
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert world
root=Path(unreal.Paths.project_dir()).resolve()
baseline={r['ue_label']:r for r in json.loads((root.parent/'Reports/campus_interior_lighting.json').read_text())['lights']}
for name in ['PointLights','SpotLights','RectLights','DirectLighting']:
 unreal.SystemLibrary.execute_console_command(world,'ShowFlag.'+name+' 2')
for a in unreal.GameplayStatics.get_all_actors_of_class(world,unreal.Actor):
 if a.get_actor_label().startswith('InteriorLight_') and 'Canteen' in a.get_actor_label():
  c=a.get_component_by_class(unreal.LocalLightComponent)
  a.set_actor_location(unreal.Vector(*baseline[a.get_actor_label()]['position_cm']),False,True)
  c.set_cast_shadows(True)
  c.set_intensity(150000)
  c.set_light_color(unreal.LinearColor(1,1,1,1))
