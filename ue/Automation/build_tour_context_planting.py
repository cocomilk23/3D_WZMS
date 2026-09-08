"""Share two native meshes for a district tree belt; preserve full Nanite foliage source."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();assets=unreal.EditorAssetLibrary;sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);smes=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
source=json.loads((root.parent/'SourceReference/tour_context_tree_buffers.json').read_text(encoding='utf8'));plan=json.loads((root.parent/'SourceReference/tour_context_planting.json').read_text());mats=json.loads(Path('E:/3D_WZMS/builds/v043_ue_bundle/materials.json').read_text(encoding='utf8'));ids={m['source_name']:m['id'] for m in mats['materials']};meshes=[]
for row in source['objects']:
 path='/Game/WZMS/Tour/Meshes/'+row['name'];mesh=assets.load_asset(path)
 if not mesh:
  d=unreal.DynamicMesh()
  for b in row['buffers']:
   bs=unreal.GeometryScriptSimpleMeshBuffers(vertices=[unreal.Vector(*v) for v in b['vertices']],triangles=[unreal.IntVector(*t) for t in b['triangles']],normals=[unreal.Vector(*n) for n in b['normals']],uv0=[unreal.Vector2D(*u) for u in b['uv0']]);unreal.GeometryScript_MeshEdits.append_buffers_to_mesh(d,bs,b['material'])
  mesh,outcome=unreal.GeometryScript_NewAssetUtils.create_new_static_mesh_asset_from_mesh(d,path,unreal.GeometryScriptCreateNewStaticMeshAssetOptions(enable_collision=False,enable_nanite=row['foliage'],enable_recompute_normals=False,enable_recompute_tangents=True));assert outcome==unreal.GeometryScriptOutcomePins.SUCCESS
  materials=[assets.load_asset('/Game/WZMS/Materials/Instances/MI_'+ids[m]) for m in row['materials']];assert all(materials);mesh.set_editor_property('static_materials',[unreal.StaticMaterial(material_interface=m,material_slot_name=unreal.Name(str(i))) for i,m in enumerate(materials)])
  if row['foliage']:
   ns=smes.get_nanite_settings(mesh);ns.enabled=True;ns.shape_preservation=unreal.NaniteShapePreservation.PRESERVE_AREA;ns.keep_percent_triangles=1;ns.trim_relative_error=0;ns.fallback_target=unreal.NaniteFallbackTarget.PERCENT_TRIANGLES;ns.fallback_percent_triangles=.02;smes.set_nanite_settings(mesh,ns,True)
  assets.save_loaded_asset(mesh)
 meshes.append(mesh)
existing={a.get_actor_label():a for a in sub.get_all_level_actors()};active=set()
for i,p in enumerate(plan['trees']):
 for j,mesh in enumerate(meshes):
  name=f'Tour_ContextTree_{i:03d}_{j}';active.add(name);loc=unreal.Vector(p['xy_m'][0]*100,-p['xy_m'][1]*100,-6.5);a=existing.get(name) or sub.spawn_actor_from_class(unreal.StaticMeshActor,loc);a.set_actor_label(name);a.set_folder_path('Tour Environment/Context Trees');a.set_actor_location(loc,False,True);a.set_actor_rotation(unreal.Rotator(pitch=0,yaw=p['yaw_degrees'],roll=0),False);s=p['scale'];a.set_actor_scale3d(unreal.Vector(s,s,s));c=a.static_mesh_component;c.set_static_mesh(mesh);c.set_collision_profile_name('NoCollision');c.set_editor_property('can_ever_affect_navigation',False)
for name,a in existing.items():
 if name.startswith('Tour_ContextTree_') and name not in active:sub.destroy_actor(a)
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
(root.parent/'Reports/tour_context_planting.json').write_text(json.dumps({'trees':len(plan['trees']),'actors':len(active),'shared_meshes':[m.get_path_name() for m in meshes],'collision':'None; outside original campus','source_foliage_triangles_retained':True,'visual_and_performance_validation_pending':True},indent=2),encoding='utf8')
