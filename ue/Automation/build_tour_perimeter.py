"""Install estimated district context; retain the accepted campus and its water exclusions."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve()
assert unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world() is None,'Stop PIE before editing'
data=json.loads((root.parent/'SourceReference/tour_perimeter_buffers.json').read_text(encoding='utf8'))
materials=json.loads(Path('E:/3D_WZMS/builds/v043_ue_bundle/materials.json').read_text(encoding='utf8'))
matids={r['source_name']:r['id'] for r in materials['materials']}
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);existing={a.get_actor_label():a for a in sub.get_all_level_actors()};rows=[]
for row in data['objects']:
 dynamic=unreal.DynamicMesh();expected=0
 for b in row['buffers']:
  buffers=unreal.GeometryScriptSimpleMeshBuffers(vertices=[unreal.Vector(*v) for v in b['vertices']],triangles=[unreal.IntVector(*t) for t in b['triangles']],normals=[unreal.Vector(*n) for n in b['normals']],uv0=[unreal.Vector2D(*uv) for uv in b['uv0']]);expected+=len(b['triangles'])
  unreal.GeometryScript_MeshEdits.append_buffers_to_mesh(dynamic,buffers,b['material'])
 path='/Game/WZMS/Tour/Meshes/'+row['name'];mesh=unreal.EditorAssetLibrary.load_asset(path)
 if mesh:
  _,outcome=unreal.GeometryScript_AssetUtils.copy_mesh_to_static_mesh(dynamic,mesh,unreal.GeometryScriptCopyMeshToAssetOptions(enable_recompute_normals=False,enable_recompute_tangents=True),unreal.GeometryScriptMeshWriteLOD(lod_index=0))
 else:
  mesh,outcome=unreal.GeometryScript_NewAssetUtils.create_new_static_mesh_asset_from_mesh(dynamic,path,unreal.GeometryScriptCreateNewStaticMeshAssetOptions(enable_collision=row['collision'],collision_mode=unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE,enable_nanite=False,enable_recompute_normals=False,enable_recompute_tangents=True))
 assert outcome==unreal.GeometryScriptOutcomePins.SUCCESS,(path,outcome)
 mats=[unreal.EditorAssetLibrary.load_asset('/Game/WZMS/Materials/Instances/MI_'+matids[n]) for n in row['materials']];assert all(mats)
 mesh.set_editor_property('static_materials',[unreal.StaticMaterial(material_interface=m,material_slot_name=unreal.Name('District_'+str(i))) for i,m in enumerate(mats)])
 if row['collision']:
  body=mesh.get_editor_property('body_setup');body.set_editor_property('collision_trace_flag',unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE);body.set_editor_property('double_sided_geometry',True)
 unreal.EditorAssetLibrary.save_loaded_asset(mesh)
 a=existing.get(row['name']) or sub.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector());a.set_actor_label(row['name']);a.set_actor_location(unreal.Vector(),False,True);a.set_actor_scale3d(unreal.Vector(1,1,1));a.set_folder_path('Tour Environment/Surrounding District')
 c=a.static_mesh_component;c.set_static_mesh(mesh);c.set_collision_profile_name('BlockAll' if row['collision'] else 'NoCollision');c.set_editor_property('can_ever_affect_navigation',False)
 for i,m in enumerate(mats):c.set_material(i,m)
 actual=mesh.get_num_triangles(0);assert actual==expected,(path,actual,expected)
 rows.append({'actor':row['name'],'mesh':path,'triangles':actual,'collision':row['collision']})
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
(root.parent/'Reports/tour_perimeter_build.json').write_text(json.dumps({'context_is_estimated':True,'campus_placements_unchanged':True,'objects':rows,'visual_and_runtime_validation_pending':True},indent=2),encoding='utf8')
