"""Persist revised camera sequence and close the owned render session."""
import unreal
from pathlib import Path
assert Path(unreal.Paths.project_dir()).resolve()==Path('E:/WZMS_UE/ue/WZMS').resolve()
assert not unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem).is_rendering()
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assert unreal.EditorAssetLibrary.save_asset('/Game/WZMS/Cinematics/LS_Demo059_Campus_r01')
unreal.SystemLibrary.quit_editor()
