import unreal,json
from pathlib import Path
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.EditorAssetLibrary.save_directory('/Game/WZMS',only_if_is_dirty=True,recursive=True)
report={'saved':True,'quit_editor':str(getattr(unreal.SystemLibrary,'quit_editor',None)),
 'screenshot_doc':unreal.AutomationLibrary.take_high_res_screenshot.__doc__}
Path(unreal.Paths.project_saved_dir(),'Logs/checkpoint.json').write_text(json.dumps(report,indent=2))
