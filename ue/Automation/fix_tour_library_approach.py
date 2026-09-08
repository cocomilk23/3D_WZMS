"""Reconnect the source library stair foot to the adjacent plaza at the same floor level."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);actors={a.get_actor_label():a for a in sub.get_all_level_actors()}
name='Tour_Library_Stair_Approach';a=actors.get(name) or sub.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(10200,-13225,-30));a.set_actor_label(name);a.set_folder_path('Tour Environment/Ground Repairs');a.set_actor_location(unreal.Vector(10200,-13225,-30),False,True);a.set_actor_scale3d(unreal.Vector(8,4.5,.6))
c=a.static_mesh_component;c.set_static_mesh(unreal.EditorAssetLibrary.load_asset('/Engine/BasicShapes/Cube'));c.set_collision_profile_name('BlockAll');c.set_editor_property('can_ever_affect_navigation',False)
source=json.loads(Path('E:/3D_WZMS/builds/v043_ue_bundle/materials.json').read_text(encoding='utf8'));m=next(r['id'] for r in source['materials'] if r['source_name']=='Library terrace grey tiles');c.set_material(0,unreal.EditorAssetLibrary.load_asset('/Game/WZMS/Materials/Instances/MI_'+m))
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
(root.parent/'Reports/tour_library_approach.json').write_text(json.dumps({'actor':name,'bounds_blender_m':[[98,130,-.6],[106,134.5,0]],'purpose':'Connect plaza to the first exterior stair tread; the original stair begins at y=134.4965 m.'},indent=2))
