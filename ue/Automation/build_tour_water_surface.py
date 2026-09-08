"""Replace overlapping translucent surfaces with one continuous animated pond surface."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();assets=unreal.EditorAssetLibrary;ed=unreal.MaterialEditingLibrary
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
data=json.loads((root.parent/'SourceReference/tour_water_surface_buffers.json').read_text(encoding='utf8'))
parent='/Game/WZMS/Tour/Materials/M_Tour_Lake'
if not assets.does_asset_exist(parent):assert assets.duplicate_asset('/Game/WZMS/Materials/M_WZMS_water',parent)
mat=assets.load_asset(parent);mat.set_editor_property('blend_mode',unreal.BlendMode.BLEND_OPAQUE);ed.recompile_material(mat);assets.save_loaded_asset(mat)
name='MI_Tour_Lake';path='/Game/WZMS/Tour/Materials/'+name;mi=assets.load_asset(path)
if not mi:mi=unreal.AssetToolsHelpers.get_asset_tools().create_asset(name,'/Game/WZMS/Tour/Materials',unreal.MaterialInstanceConstant,unreal.MaterialInstanceConstantFactoryNew())
ed.set_material_instance_parent(mi,mat)
for key,value in [('ColorA',[.035,.080,.066]),('ColorB',[.050,.115,.088])]:ed.set_material_instance_vector_parameter_value(mi,key,unreal.LinearColor(*value,1))
for key,value in [('Roughness',.23),('Metallic',0),('DetailSizeCm',90),('ReliefCm',.6),('Flow',.012)]:ed.set_material_instance_scalar_parameter_value(mi,key,value)
ed.update_material_instance(mi);assets.save_loaded_asset(mi)
d=unreal.DynamicMesh()
for b in data['buffers']:
 buffers=unreal.GeometryScriptSimpleMeshBuffers(vertices=[unreal.Vector(*v) for v in b['vertices']],triangles=[unreal.IntVector(*t) for t in b['triangles']],normals=[unreal.Vector(*n) for n in b['normals']],uv0=[unreal.Vector2D(*v) for v in b['uv0']]);unreal.GeometryScript_MeshEdits.append_buffers_to_mesh(d,buffers,0)
path='/Game/WZMS/Tour/Meshes/SM_Tour_Lake_Surface';mesh=assets.load_asset(path)
if mesh:_,outcome=unreal.GeometryScript_AssetUtils.copy_mesh_to_static_mesh(d,mesh,unreal.GeometryScriptCopyMeshToAssetOptions(enable_recompute_normals=False,enable_recompute_tangents=True),unreal.GeometryScriptMeshWriteLOD(lod_index=0))
else:mesh,outcome=unreal.GeometryScript_NewAssetUtils.create_new_static_mesh_asset_from_mesh(d,path,unreal.GeometryScriptCreateNewStaticMeshAssetOptions(enable_collision=False,enable_nanite=False,enable_recompute_normals=False,enable_recompute_tangents=True))
assert outcome==unreal.GeometryScriptOutcomePins.SUCCESS
mesh.set_editor_property('static_materials',[unreal.StaticMaterial(material_interface=mi,material_slot_name='Lake')]);assets.save_loaded_asset(mesh)
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);actors={a.get_actor_label():a for a in sub.get_all_level_actors()};hidden=[]
for zone in ['south','central','west','east','north']:
 source=json.loads(Path(f'E:/3D_WZMS/builds/v043_ue_bundle/zone_{zone}.json').read_text(encoding='utf8'))
 for row in source['chunks']:
  if row['role']!='water':continue
  a=actors[row['name']];a.set_actor_hidden_in_game(True);a.set_is_temporarily_hidden_in_editor(True);hidden.append(row['name'])
a=actors.get('SM_Tour_Lake_Surface') or sub.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector());a.set_actor_label('SM_Tour_Lake_Surface');a.set_folder_path('Tour Environment/Water');a.set_actor_scale3d(unreal.Vector(1,1,1));c=a.static_mesh_component;c.set_static_mesh(mesh);c.set_material(0,mi);c.set_collision_profile_name('NoCollision');c.set_editor_property('cast_shadow',False)
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
(root.parent/'Reports/tour_water_surface.json').write_text(json.dumps({'source_water_assets_preserved':True,'hidden_source_actors':hidden,'replacement_actor':a.get_actor_label(),'area_m2':data['area_m2'],'level_m':data['level_m'],'collision':'NoCollision; water exclusion remains separately active','visual_validation_pending':True},indent=2),encoding='utf8')
