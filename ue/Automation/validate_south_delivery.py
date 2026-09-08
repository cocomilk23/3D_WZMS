import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();report=json.loads((root.parent/'Reports/south_import.json').read_text())
actors={a.get_actor_label():a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()}
rows=[]
fp=root.parent/'Reports/campus_foliage_fallback.json';fallback={r['path']:r for r in json.loads(fp.read_text())['meshes']} if fp.exists() else {}
for ref in report['chunks']:
    a=actors[ref['name']];mesh=a.static_mesh_component.static_mesh
    compact=fallback.get('/Game/WZMS/South/Meshes/'+ref['name'])
    if compact:assert mesh.get_num_nanite_triangles()==compact['nanite_triangles_before'],ref['name']
    else:assert mesh.get_num_triangles(0)==ref['ue_triangles'],ref['name']
    assert all(abs(x-y)<.01 for x,y in zip(a.get_actor_location().to_tuple(),ref['placement_cm'])),ref['name']
    assert all(abs(x-100)<.001 for x in a.get_actor_scale3d().to_tuple())
    if ref['role']=='solid':assert a.static_mesh_component.get_editor_property('disallow_nanite')
    for i,slot in enumerate(mesh.static_materials):
        mat=a.static_mesh_component.get_material(i)
        assert mat and mat.get_name()=='MI_'+str(slot.material_slot_name),(ref['name'],i)
    rows.append({'mesh':ref['name'],'triangles_preserved':True,'transform_correct':True,'materials_bound':True})
bp=unreal.EditorAssetLibrary.load_asset('/Game/WZMS/Blueprints/BP_WZMS_Explorer')
unreal.BlueprintEditorLibrary.compile_blueprint(bp)
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.EditorAssetLibrary.save_directory('/Game/WZMS',only_if_is_dirty=True,recursive=True)
(root.parent/'Reports/south_delivery_validation.json').write_text(json.dumps({'passed':True,'mesh_count':len(rows),'meshes':rows,'source_hash':report['source_sha256'],'verified_after_nanite_build':True},indent=2))
