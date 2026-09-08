"""Use an empty map while building meshes, releasing the assembled campus from memory."""
import unreal
levels=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
assert levels.save_current_level()
path='/Game/WZMS/Maps/L_WZMS_Transfer'
if unreal.EditorAssetLibrary.does_asset_exist(path):assert levels.load_level(path)
else:assert levels.new_level(path)
assert levels.save_current_level()
unreal.SystemLibrary.collect_garbage()
