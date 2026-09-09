"""Read the installed cinematic API before constructing the demo sequence."""
import unreal,json
from pathlib import Path
names=['MoviePipelineAntiAliasingSetting','MoviePipelineGameOverrideSetting','MoviePipelineOutputSetting','MoviePipelinePIEExecutor','MovieSceneScriptingDoubleChannel','MovieSceneBindingProxy','MoviePipelineQueueSubsystem']
out={n:str(getattr(unreal,n).__doc__) for n in names}
out['methods']={n:[x for x in dir(getattr(unreal,n)) if any(k in x for k in ['queue','executor','render','template','binding','key'])] for n in names}
(Path(unreal.Paths.project_dir()).resolve().parent/'Reports/demo_pipeline_api.json').write_text(json.dumps(out,indent=2))
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).load_level('/Game/WZMS/Maps/L_WZMS_Campus')
