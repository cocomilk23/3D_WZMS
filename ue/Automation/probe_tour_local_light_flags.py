"""Runtime diagnostic: explicitly enable local-light show flags."""
import unreal
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert world
for name in ['PointLights','SpotLights','RectLights','DirectLighting']:
 unreal.SystemLibrary.execute_console_command(world,'ShowFlag.'+name+' 1')
