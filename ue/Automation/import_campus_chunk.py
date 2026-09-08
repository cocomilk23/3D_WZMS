"""Import one checked chunk, save it once, and place it in the campus map."""
import unreal,json,hashlib
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();source=Path('E:/3D_WZMS/builds/v043_ue_bundle')
request=json.loads((root/'Saved/Logs/campus_request.json').read_text());name=request['zone'];assert name in ['central','west','east','north']
zone=json.loads((source/f'zone_{name}.json').read_text(encoding='utf8'))
ch=next(c for c in zone['chunks'] if c['name']==request['chunk'])
ref=next(c for c in json.loads((root.parent/f'Reports/fbx_bounds_{name}.json').read_text()) if c['name']==ch['name'])
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world();assert world.get_name() in ['L_WZMS_Campus','L_WZMS_Transfer'],world.get_name()
staging=world.get_name()=='L_WZMS_Transfer'
assets=unreal.EditorAssetLibrary;smes=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem);actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
src=source/ch['file'];assert hashlib.sha256(src.read_bytes()).hexdigest()==ch['sha256']
path=f'/Game/WZMS/{name.title()}/Meshes/'+ch['name'];mesh=assets.load_asset(path)
if not mesh:
    unreal.SystemLibrary.execute_console_command(None,'Interchange.FeatureFlags.Import.FBX 0')
    ui=unreal.FbxImportUI();ui.automated_import_should_detect_type=False;ui.import_mesh=True;ui.import_as_skeletal=False
    ui.mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH;ui.import_materials=False;ui.import_textures=False;ui.import_animations=False
    d=ui.static_mesh_import_data
    for k,v in dict(combine_meshes=True,auto_generate_collision=False,generate_lightmap_u_vs=False,convert_scene=True,convert_scene_unit=True,force_front_x_axis=False,transform_vertex_to_absolute=False,bake_pivot_in_vertex=False,build_nanite=False,remove_degenerates=False).items():d.set_editor_property(k,v)
    d.normal_import_method=unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS
    task=unreal.AssetImportTask();task.filename=str(src);task.destination_path=f'/Game/WZMS/{name.title()}/Meshes';task.destination_name=ch['name'];task.automated=True;task.save=False;task.options=ui;task.factory=unreal.FbxFactory()
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task]);mesh=assets.load_asset(path);assert mesh,path
if ch['role']=='foliage':
    ns=smes.get_nanite_settings(mesh)
    if not ns.enabled or ns.shape_preservation!=unreal.NaniteShapePreservation.PRESERVE_AREA or ns.fallback_percent_triangles!=1 or ns.fallback_target!=unreal.NaniteFallbackTarget.PERCENT_TRIANGLES:
        ns.enabled=True;ns.shape_preservation=unreal.NaniteShapePreservation.PRESERVE_AREA
        ns.keep_percent_triangles=1;ns.trim_relative_error=0;ns.fallback_percent_triangles=1;ns.fallback_target=unreal.NaniteFallbackTarget.PERCENT_TRIANGLES
        smes.set_nanite_settings(mesh,ns,True)
body=mesh.get_editor_property('body_setup')
if body and ch['role']=='solid':
    body.set_editor_property('collision_trace_flag',unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE);body.set_editor_property('double_sided_geometry',True)
assets.save_loaded_asset(mesh)
lo,hi=ref['used_local_bounds_m'];bounds=mesh.get_bounds();centre=[(lo[j]+hi[j])/2*(1 if j!=1 else -1) for j in range(3)]
error=max(max(abs(bounds.origin.to_tuple()[j]-centre[j])*100 for j in range(3)),max(abs(bounds.box_extent.to_tuple()[j]-(hi[j]-lo[j])/2)*100 for j in range(3)))
assert error<1,(ch['name'],'bounds_error_cm',error)
tris=mesh.get_num_triangles(0);assert tris in [ch['triangles'],ch['triangles']-ref['zero_area_faces']],(ch['name'],'triangles',tris,ref)
slots=[str(s.material_slot_name) for s in mesh.static_materials]
used={m for m,n in zip(ch['materials'],ch['material_triangle_counts']) if n>0};assert used<=set(slots)<=set(ch['materials'])
p=ch['pivot_blender_m'];loc=unreal.Vector(p[0]*100,-p[1]*100,p[2]*100)
a=next((a for a in actors.get_all_level_actors() if a.get_actor_label()==ch['name']),None) or actors.spawn_actor_from_class(unreal.StaticMeshActor,loc)
a.set_actor_label(ch['name']);a.set_folder_path(name.title()+'/'+ch['role']);a.set_actor_location(loc,False,True);a.set_actor_scale3d(unreal.Vector(100,100,100))
comp=a.static_mesh_component;comp.set_static_mesh(mesh);comp.set_mobility(unreal.ComponentMobility.STATIC);comp.set_editor_property('disallow_nanite',ch['role']=='solid')
comp.set_collision_profile_name('BlockAll' if ch['role']=='solid' else 'NoCollision');comp.set_editor_property('cast_shadow',ch['role'] not in ['glass','water'])
for i,mid in enumerate(slots):
    mi=assets.load_asset('/Game/WZMS/Materials/Instances/MI_'+mid);assert mi,mid;comp.set_material(i,mi)
if staging:
    actors.destroy_actor(a)
else:
    assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
report_path=root.parent/f'Reports/import_{name}.json'
report=json.loads(report_path.read_text()) if report_path.exists() else {'zone':name,'source_sha256':zone['source_sha256'],'map':'/Game/WZMS/Maps/L_WZMS_Campus','chunks':[]}
row={'name':ch['name'],'role':ch['role'],'path':path,'source_triangles':ch['triangles'],'ue_triangles':tris,'bounds_error_cm':error,'placement_cm':list(loc.to_tuple()),'materials':slots,'verified':True,'pending_campus_placement':staging}
report['chunks']=[c for c in report['chunks'] if c['name']!=ch['name']]+[row];report['complete']=len(report['chunks'])==len(zone['chunks'])
report_path.write_text(json.dumps(report,indent=2))
unreal.SystemLibrary.collect_garbage()
print('WZMS_CAMPUS_IMPORTED',name,len(report['chunks']),len(zone['chunks']))
