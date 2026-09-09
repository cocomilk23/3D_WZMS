"""Save completed exterior sequences and close the owned render session."""
import unreal
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assert not unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem).is_rendering()
for revision in ['r01','r02','r03']:
    for kind in ['Campus','Contact']:
        assert unreal.EditorAssetLibrary.save_asset('/Game/WZMS/Cinematics/LS_Demo056_'+kind+'_'+revision)
unreal.SystemLibrary.quit_editor()
