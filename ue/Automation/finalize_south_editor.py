import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve()
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors=sub.get_all_level_actors()
fixture='/Game/WZMS/QA/SM_AxisFixture'
assert not any(isinstance(a,unreal.StaticMeshActor) and a.static_mesh_component.static_mesh and a.static_mesh_component.static_mesh.get_path_name().startswith(fixture) for a in actors)
if unreal.EditorAssetLibrary.does_asset_exist(fixture):unreal.EditorAssetLibrary.delete_asset(fixture)
for a in actors:
    if a.get_actor_label()=='Review_Plaza_Clear':sub.destroy_actor(a)
camera=next(a for a in sub.get_all_level_actors() if a.get_actor_label()=='Review_Gate_Exterior')
unreal.EditorLevelLibrary.set_level_viewport_camera_info(camera.get_actor_location(),camera.get_actor_rotation())
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.EditorAssetLibrary.save_directory('/Game/WZMS',only_if_is_dirty=True,recursive=True)
report=root.parent/'Reports/explorer_blueprint.json'
data=json.loads(report.read_text());data['runtime_tested']=True;data['runtime_report']='explorer_runtime.json';data['keyboard_reports']=['keyboard_flight.json','keyboard_return.json'];report.write_text(json.dumps(data,indent=2))
reviews=[]
for a in sub.get_all_level_actors():
    if not a.get_actor_label().startswith('Review_'):continue
    reviews.append({'label':a.get_actor_label(),'location_cm':list(a.get_actor_location().to_tuple()),'rotation':str(a.get_actor_rotation()),'fov':a.get_component_by_class(unreal.CameraComponent).field_of_view})
(root.parent/'Reports/review_cameras.json').write_text(json.dumps(reviews,indent=2))
