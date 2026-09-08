import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();assets=unreal.EditorAssetLibrary
levels=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
assert levels.save_current_level()
path='/Game/WZMS/Maps/L_WZMS_Campus'
if not assets.does_asset_exist(path):
    world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    assert world.get_name()=='L_WZMS_South'
    assert unreal.EditorLoadingAndSavingUtils.save_map(world,path)
else:
    assert levels.load_level(path)
assert levels.save_current_level()
report_path=root.parent/'Reports/campus_migration.json'
if not report_path.exists():
    report_path.write_text(json.dumps({'source_version':'v0.0.43','map':path,'zones':['south','central','west','east','north'],'south_demo_retained':True,'completed_zones':['south'],'scope':'Existing main campus model; Xinjiang branch remains deferred.'},indent=2))
