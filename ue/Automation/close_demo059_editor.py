"""Persist revised camera sequence and close the owned render session."""
import unreal,json
from pathlib import Path
assert Path(unreal.Paths.project_dir()).resolve()==Path('E:/WZMS_UE/ue/WZMS').resolve()
assert not unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem).is_rendering()
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
report=Path(unreal.Paths.project_dir()).resolve().parent/'Reports/demo_sequences_059.json'
assert unreal.EditorAssetLibrary.save_asset(json.loads(report.read_text())['final']['sequence'])
unreal.SystemLibrary.quit_editor()
