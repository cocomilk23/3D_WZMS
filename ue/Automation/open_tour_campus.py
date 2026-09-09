"""Open the delivered campus for runtime review, away from the map-capture camera."""
import unreal
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
levels=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
assert levels.load_level('/Game/WZMS/Maps/L_WZMS_Campus')
unreal.EditorLevelLibrary.set_level_viewport_camera_info(unreal.Vector(-2500,9000,750),unreal.Rotator(pitch=-2,yaw=-90,roll=0))
