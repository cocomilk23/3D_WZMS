"""Close only this project's completed, camera-only render session."""
import unreal
from pathlib import Path
assert Path(unreal.Paths.project_dir()).resolve()==Path('E:/WZMS_UE/ue/WZMS').resolve()
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assert not unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem).is_rendering()
for revision in ['r01','r02','r03','r04']:
 for kind in ['Campus','Contact']:
  assert unreal.EditorAssetLibrary.save_asset('/Game/WZMS/Cinematics/LS_Demo058_'+kind+'_'+revision)
unreal.SystemLibrary.quit_editor()
