"""Run MRQ with explicit render-only overrides and persistent completion evidence."""
import unreal,json,time
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();ue=root.parent
req=json.loads((root/'Saved/Logs/demo_render_request.json').read_text(encoding='utf8'))
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
sub=unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem);assert not sub.is_rendering()
queue=unreal.MoviePipelineQueue();job=queue.allocate_new_job(unreal.MoviePipelineExecutorJob)
job.job_name=req['name'];job.map=unreal.SoftObjectPath('/Game/WZMS/Maps/L_WZMS_Campus.L_WZMS_Campus')
job.sequence=unreal.SoftObjectPath(req['sequence']);config=job.get_configuration()
output=config.find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting)
output.output_directory=unreal.DirectoryPath(req['directory']);output.file_name_format='frame_{frame_number}'
output.output_resolution=unreal.IntPoint(*req['resolution']);output.zero_pad_frame_numbers=5
output.override_existing_output=False;output.flush_disk_writes_per_shot=True
config.find_or_add_setting_by_class(unreal.MoviePipelineDeferredPassBase)
config.find_or_add_setting_by_class(unreal.MoviePipelineImageSequenceOutput_PNG)
aa=config.find_or_add_setting_by_class(unreal.MoviePipelineAntiAliasingSetting)
aa.spatial_sample_count=1;aa.temporal_sample_count=req.get('samples',4)
aa.engine_warm_up_count=32;aa.render_warm_up_count=24;aa.use_camera_cut_for_warm_up=False
game=config.find_or_add_setting_by_class(unreal.MoviePipelineGameOverrideSetting)
game.game_mode_override=unreal.MoviePipelineGameMode
game.cinematic_quality_settings=False;game.use_lod_zero=False;game.disable_hlods=False
game.use_high_quality_shadows=False;game.override_view_distance_scale=False
game.flush_grass_streaming=False;game.flush_streaming_managers=False
console=config.find_or_add_setting_by_class(unreal.MoviePipelineConsoleVariableSetting)
for name,value in {'r.ScreenPercentage':100.0,'r.Shadow.Virtual.OnePassProjection.MaxLightsPerPixel':32.0,'r.MotionBlurQuality':4.0}.items():
    assert console.add_or_update_console_variable(name,value)
report=ue/'Reports'/req['report'];state={'complete':False,'started_unix':time.time(),'request':req,'errors':[]}
report.write_text(json.dumps(state,indent=2)+'\n')
def finished(executor,success):
    state.update(complete=True,success=bool(success),finished_unix=time.time());report.write_text(json.dumps(state,indent=2)+'\n')
def errored(executor,pipeline,fatal,message):
    state['errors'].append({'fatal':bool(fatal),'message':str(message)});report.write_text(json.dumps(state,indent=2)+'\n')
executor=unreal.MoviePipelinePIEExecutor(sub)
executor.on_executor_finished_delegate.add_callable_unique(finished)
executor.on_executor_errored_delegate.add_callable_unique(errored)
# Keep callbacks, queue and executor alive beyond this bridge job.
unreal._wzms_demo_render=(queue,executor,finished,errored,state)
sub.render_queue_instance_with_executor_instance(queue,executor)
