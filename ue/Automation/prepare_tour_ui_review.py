"""Use a dedicated play window for real input and 1080p review."""
import unreal
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.LevelEditorPlaySettings'))
settings.set_editor_property('NewWindowWidth',1920)
settings.set_editor_property('NewWindowHeight',1080)
settings.set_editor_property('CenterNewWindow',True)
