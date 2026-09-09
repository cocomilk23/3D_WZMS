"""Import exact supplied crest and create editable final sports meshes in the current UE campus."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();ue=root.parent
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assets=unreal.EditorAssetLibrary;at=unreal.AssetToolsHelpers.get_asset_tools();ed=unreal.MaterialEditingLibrary
base='/Game/WZMS/Final057';src=json.loads(Path('E:/3D_WZMS/builds/v043_ue_bundle/materials.json').read_text(encoding='utf8'))
mats={x['source_name']:'/Game/WZMS/Materials/Instances/MI_'+x['id'] for x in src['materials']}
path=base+'/T_WZMS_Crest';assert not assets.does_asset_exist(path)
task=unreal.AssetImportTask();task.filename=str(ue/'SourceTextures/Final057/WZMS_Crest_UserReference.png');task.destination_path=base;task.destination_name='T_WZMS_Crest';task.automated=True;task.save=True;at.import_asset_tasks([task]);tx=unreal.load_asset(path);assert tx
tx.set_editor_property('srgb',True);tx.set_editor_property('power_of_two_mode',unreal.TexturePowerOfTwoSetting.STRETCH_TO_POWER_OF_TWO);tx.set_editor_property('address_x',unreal.TextureAddress.TA_CLAMP);tx.set_editor_property('address_y',unreal.TextureAddress.TA_CLAMP);assets.save_loaded_asset(tx)
mat=at.create_asset('M_Crest',base,unreal.Material,unreal.MaterialFactoryNew());assert mat
tex=ed.create_material_expression(mat,unreal.MaterialExpressionTextureSample,0,0);tex.texture=tx
assert ed.connect_material_property(tex,'RGB',unreal.MaterialProperty.MP_BASE_COLOR)
rough=ed.create_material_expression(mat,unreal.MaterialExpressionConstant,0,150);rough.r=.9;ed.connect_material_property(rough,'',unreal.MaterialProperty.MP_ROUGHNESS)
spec=ed.create_material_expression(mat,unreal.MaterialExpressionConstant,0,250);spec.r=.15;ed.connect_material_property(spec,'',unreal.MaterialProperty.MP_SPECULAR)
ed.recompile_material(mat);assets.save_loaded_asset(mat);mats['Final057_Crest']=mat.get_path_name()
metal=at.create_asset('MI_WhiteGoalFrame',base,unreal.MaterialInstanceConstant,unreal.MaterialInstanceConstantFactoryNew());assert metal
ed.set_material_instance_parent(metal,unreal.load_asset('/Game/WZMS/Materials/M_WZMS_surface'))
for n,col in [('ColorA',(.72,.74,.72)),('ColorB',(.84,.86,.82))]:ed.set_material_instance_vector_parameter_value(metal,n,unreal.LinearColor(*col,1))
for n,v in [('Roughness',.42),('Metallic',.25),('ReliefCm',.004),('DetailSizeCm',50)]:ed.set_material_instance_scalar_parameter_value(metal,n,v)
ed.update_material_instance(metal);assets.save_loaded_asset(metal);mats['Final057_WhiteMetal']=metal.get_path_name()
rows=[];sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
for row in json.loads((ue/'SourceReference/final057_detail_buffers.json').read_text())['objects']:
 name=row['name'];path=base+'/'+name;assert not assets.does_asset_exist(path)
 d=unreal.DynamicMesh();expected=0
 for b in row['buffers']:
  buf=unreal.GeometryScriptSimpleMeshBuffers(vertices=[unreal.Vector(*x) for x in b['vertices']],triangles=[unreal.IntVector(*x) for x in b['triangles']],normals=[unreal.Vector(*x) for x in b['normals']],uv0=[unreal.Vector2D(*x) for x in b['uv0']]);unreal.GeometryScript_MeshEdits.append_buffers_to_mesh(d,buf,b['material']);expected+=len(b['triangles'])
 mesh,result=unreal.GeometryScript_NewAssetUtils.create_new_static_mesh_asset_from_mesh(d,path,unreal.GeometryScriptCreateNewStaticMeshAssetOptions(enable_collision=row['collision'],collision_mode=unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE,enable_nanite=False,enable_recompute_normals=False,enable_recompute_tangents=True));assert result==unreal.GeometryScriptOutcomePins.SUCCESS
 mm=[unreal.load_asset(mats[n]) for n in row['materials']];assert all(mm)
 mesh.set_editor_property('static_materials',[unreal.StaticMaterial(material_interface=m,material_slot_name=unreal.Name('Detail_'+str(i))) for i,m in enumerate(mm)])
 if row['collision']:
  body=mesh.get_editor_property('body_setup');body.set_editor_property('collision_trace_flag',unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE);body.set_editor_property('double_sided_geometry',True)
 assert mesh.get_num_triangles(0)==expected
 assets.save_loaded_asset(mesh);actor=sub.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector());actor.set_actor_label(name);actor.set_folder_path('Final Delivery/057 Corrections');c=actor.static_mesh_component;c.set_static_mesh(mesh);c.set_mobility(unreal.ComponentMobility.STATIC);c.set_collision_profile_name('BlockAll' if row['collision'] else 'NoCollision');c.set_editor_property('can_ever_affect_navigation',False);c.set_editor_property('cast_shadow',row['shadow'])
 for i,m in enumerate(mm):c.set_material(i,m)
 rows.append({'actor':name,'asset':path,'triangles':expected,'collision':row['collision'],'materials':[m.get_path_name() for m in mm]})
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
(ue/'Reports/final057_details_built.json').write_text(json.dumps({'objects':rows,'texture_source_unchanged':True,'texture_mips':'UE power-of-two build stretch for mipmapped viewing','map_saved':True},indent=2)+'\n',encoding='utf8')
