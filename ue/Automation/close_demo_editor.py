"""Close this owned rendering session after saving only its completed cinematic assets."""
import unreal
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assert not unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem).is_rendering()
for name in ['LS_Demo055_Campus_r01','LS_Demo055_Campus_r02','LS_Demo055_Contact_r01','LS_Demo055_Contact_r02']:
    assert unreal.EditorAssetLibrary.save_asset('/Game/WZMS/Cinematics/'+name)
# The incomplete initial API probe has never been part of a delivered sequence.
if unreal.EditorAssetLibrary.does_asset_exist('/Game/WZMS/Cinematics/LS_Demo055_Contact'):
    assert unreal.EditorAssetLibrary.delete_asset('/Game/WZMS/Cinematics/LS_Demo055_Contact')
unreal.SystemLibrary.quit_editor()
