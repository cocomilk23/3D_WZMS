import unreal
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.EditorAssetLibrary.save_directory('/Game/WZMS',only_if_is_dirty=True,recursive=True)
unreal.SystemLibrary.quit_editor()
