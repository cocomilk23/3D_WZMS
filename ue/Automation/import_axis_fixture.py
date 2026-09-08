import unreal,json
from pathlib import Path
unreal.SystemLibrary.execute_console_command(None,'Interchange.FeatureFlags.Import.FBX 0')
ui=unreal.FbxImportUI()
ui.automated_import_should_detect_type=False
ui.import_mesh=True;ui.import_as_skeletal=False;ui.mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH
ui.import_materials=False;ui.import_textures=False;ui.import_animations=False
d=ui.static_mesh_import_data
d.import_uniform_scale=100.0
for k,v in dict(combine_meshes=True,auto_generate_collision=False,generate_lightmap_u_vs=False,convert_scene=True,convert_scene_unit=True,force_front_x_axis=False,transform_vertex_to_absolute=False,bake_pivot_in_vertex=False).items():
    d.set_editor_property(k,v)
d.normal_import_method=unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS
t=unreal.AssetImportTask();t.filename='E:/WZMS_UE_Cache/AxisFixture.fbx';t.destination_path='/Game/WZMS/QA';t.destination_name='SM_AxisFixture';t.automated=True;t.replace_existing=True;t.replace_existing_settings=True;t.save=True;t.options=ui;t.factory=unreal.FbxFactory()
unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t])
mesh=unreal.load_asset('/Game/WZMS/QA/SM_AxisFixture')
assert mesh, t.imported_object_paths
b=mesh.get_bounds();report={'origin_mesh_units':list(b.origin.to_tuple()),'extent_mesh_units':list(b.box_extent.to_tuple()),'paths':list(t.imported_object_paths),'world_conversion':'Place actor at source pivot (X,-Y,Z)*100 with scale 100; raw local FBX vertices retain metre-sized values.'}
Path('E:/WZMS_UE/ue/Reports/axis_conversion.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print('WZMS_AXIS_FIXTURE',report)
