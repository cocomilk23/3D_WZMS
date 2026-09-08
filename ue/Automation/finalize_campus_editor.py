"""Set the verified campus as the startup map and leave a useful gate view."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();reports=root.parent/'Reports'
previous=root/'Saved/Logs/build_throttle_previous.json'
if previous.exists():
    performance=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'))
    performance.set_editor_property('bThrottleCPUWhenNotForeground',json.loads(previous.read_text())['value'])
delivery=json.loads((reports/'campus_delivery_validation.json').read_text());assert delivery['passed'] and delivery['mesh_count']==249
runtime=json.loads((reports/'campus_runtime.json').read_text());assert runtime['complete'] and runtime['passed']
source=json.loads(Path('E:/3D_WZMS/builds/v043_ue_bundle/materials.json').read_text(encoding='utf8'))
for row in source['materials']:
    assert unreal.EditorAssetLibrary.does_asset_exist('/Game/WZMS/Materials/Instances/MI_'+row['id']),row['id']
    for texture in row['textures']:assert unreal.EditorAssetLibrary.does_asset_exist('/Game/WZMS/Textures/'+Path(texture).stem),texture
config=root/'Config/DefaultEngine.ini';text=config.read_text();text=text.replace('EditorStartupMap=/Game/WZMS/Maps/L_WZMS_South','EditorStartupMap=/Game/WZMS/Maps/L_WZMS_Campus').replace('GameDefaultMap=/Game/WZMS/Maps/L_WZMS_South','GameDefaultMap=/Game/WZMS/Maps/L_WZMS_Campus');config.write_text(text)
unreal.EditorLevelLibrary.set_level_viewport_camera_info(unreal.Vector(-2500,9000,750),unreal.Rotator(pitch=-2,yaw=-90,roll=0))
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.EditorAssetLibrary.save_directory('/Game/WZMS',only_if_is_dirty=True,recursive=True)
path=reports/'campus_migration.json';progress=json.loads(path.read_text());progress.update(geometry_migration_complete=True,materials_verified=len(source['materials']),default_map='/Game/WZMS/Maps/L_WZMS_Campus',interactive_runtime_verified=True,source_dimensions='User-approved estimates; no survey dimensions supplied',delivery_scope='All existing v043 main-campus model content; not newly modelled unseen interiors');path.write_text(json.dumps(progress,indent=2))
