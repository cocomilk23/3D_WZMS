"""Import v043 south geometry; preserve source mesh detail and verify placed bounds."""
import unreal,json,hashlib,time
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()).resolve();REPORT=ROOT.parent/'Reports/south_import.json'
SOURCE=Path('E:/3D_WZMS/builds/v043_ue_bundle')
zone=json.loads((SOURCE/'zone_south.json').read_text(encoding='utf8'))
used_bounds={r['name']:r for r in json.loads((ROOT.parent/'Reports/fbx_used_bounds.json').read_text(encoding='utf8'))}
MAP='/Game/WZMS/Maps/L_WZMS_South'
unreal.SystemLibrary.execute_console_command(None,'Interchange.FeatureFlags.Import.FBX 0')
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
levels=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
assets=unreal.EditorAssetLibrary
if assets.does_asset_exist(MAP):levels.load_level(MAP)
else:
    assets.make_directory('/Game/WZMS/Maps')
    assert levels.new_level(MAP)
existing={a.get_actor_label():a for a in actors.get_all_level_actors()}
rows=[]
report={'source_sha256':zone['source_sha256'],'zone':'south','map':MAP,'coordinate_mapping':'UE world cm = (Blender X, -Blender Y, Blender Z) * 100','mesh_local_units':'FBX local vertices are retained; actor scale 100 converts metres to centimetres. Validated with asymmetric fixture.','chunks':rows,'complete':False}
def checkpoint():REPORT.write_text(json.dumps(report,indent=2),encoding='utf8')
for i,ch in enumerate(sorted(zone['chunks'],key=lambda c:({'solid':0,'glass':1,'water':2,'foliage':3}[c['role']],c['name']))):
    src=SOURCE/ch['file'];assert hashlib.sha256(src.read_bytes()).hexdigest()==ch['sha256']
    path='/Game/WZMS/South/Meshes/'+ch['name'];mesh=assets.load_asset(path)
    if mesh is None:
        ui=unreal.FbxImportUI();ui.automated_import_should_detect_type=False
        ui.import_mesh=True;ui.import_as_skeletal=False;ui.mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH
        ui.import_materials=False;ui.import_textures=False;ui.import_animations=False
        d=ui.static_mesh_import_data
        for k,v in dict(combine_meshes=True,auto_generate_collision=False,generate_lightmap_u_vs=False,convert_scene=True,convert_scene_unit=True,force_front_x_axis=False,transform_vertex_to_absolute=False,bake_pivot_in_vertex=False,build_nanite=ch['role']=='foliage',remove_degenerates=False).items():d.set_editor_property(k,v)
        d.normal_import_method=unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS
        task=unreal.AssetImportTask();task.filename=str(src);task.destination_path='/Game/WZMS/South/Meshes';task.destination_name=ch['name'];task.automated=True;task.save=True;task.options=ui;task.factory=unreal.FbxFactory()
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task]);mesh=assets.load_asset(path)
    assert mesh,path
    if ch['role']=='foliage':
        smes=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
        ns=smes.get_nanite_settings(mesh)
        if ns.fallback_target!=unreal.NaniteFallbackTarget.PERCENT_TRIANGLES or ns.fallback_percent_triangles!=1.0:
            ns.enabled=True;ns.keep_percent_triangles=1.0;ns.trim_relative_error=0
            ns.shape_preservation=unreal.NaniteShapePreservation.PRESERVE_AREA
            ns.fallback_target=unreal.NaniteFallbackTarget.PERCENT_TRIANGLES;ns.fallback_percent_triangles=1.0
            smes.set_nanite_settings(mesh,ns,True)
    slots=list(mesh.static_materials)
    actual=[str(s.material_slot_name) for s in slots]
    used_source={m for m,n in zip(ch['materials'],ch['material_triangle_counts']) if n>0}
    assert used_source <= set(actual) <= set(ch['materials']),('Used material slots',ch['name'],actual,used_source)
    body=mesh.get_editor_property('body_setup')
    if body and ch['role']=='solid':
        if body.get_editor_property('collision_trace_flag')!=unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE:body.set_editor_property('collision_trace_flag',unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE)
        if not body.get_editor_property('double_sided_geometry'):body.set_editor_property('double_sided_geometry',True)
    assets.save_loaded_asset(mesh)
    pivot=ch['pivot_blender_m'];location=unreal.Vector(pivot[0]*100,-pivot[1]*100,pivot[2]*100)
    actor=existing.get(ch['name']) or actors.spawn_actor_from_class(unreal.StaticMeshActor,location)
    actor.set_actor_label(ch['name']);actor.set_folder_path('South/'+ch['role'])
    actor.set_actor_location(location,False,False);actor.set_actor_scale3d(unreal.Vector(100,100,100))
    comp=actor.static_mesh_component;comp.set_static_mesh(mesh);comp.set_mobility(unreal.ComponentMobility.STATIC)
    comp.set_editor_property('disallow_nanite',ch['role']=='solid')
    comp.set_collision_profile_name('BlockAll' if ch['role']=='solid' else 'NoCollision')
    comp.set_editor_property('cast_shadow',ch['role'] not in ['water','glass'])
    reference=used_bounds[ch['name']];lo,hi=reference['used_local_bounds_m']
    b=mesh.get_bounds();expected=[(hi[j]-lo[j])/2 for j in range(3)]
    error=max(abs(b.box_extent.to_tuple()[j]-expected[j])*100 for j in range(3))
    centre=[(lo[j]+hi[j])/2 * (1 if j!=1 else -1) for j in range(3)]
    error=max(error,max(abs(b.origin.to_tuple()[j]-centre[j])*100 for j in range(3)))
    assert error<1.0,('Placed size mismatch cm',ch['name'],error,b.box_extent,expected)
    triangles=mesh.get_num_triangles(0)
    assert triangles in [ch['triangles'],ch['triangles']-reference['zero_area_faces']],('Unexpected triangle loss',ch['name'],triangles,reference)
    rows.append({'name':ch['name'],'role':ch['role'],'mesh':path,'source_triangles':ch['triangles'],'ue_triangles':triangles,'source_zero_area_faces':reference['zero_area_faces'],'material_slots':actual,'placement_cm':list(location.to_tuple()),'scale':100,'bounds_error_cm':error,'collision':'complex_source' if ch['role']=='solid' else 'none','nanite':ch['role']=='foliage'})
    checkpoint();levels.save_current_level();print('WZMS_IMPORTED',i+1,len(zone['chunks']),ch['name'])
report['complete']=len(rows)==len(zone['chunks']);report['source_triangles']=sum(c['triangles'] for c in zone['chunks']);checkpoint()
unreal.EditorLevelLibrary.set_level_viewport_camera_info(unreal.Vector(18000,20000,14000),unreal.Rotator(pitch=-32,yaw=-135,roll=0))
levels.save_current_level()
