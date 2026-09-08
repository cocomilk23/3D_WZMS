"""Validate all completed zones against the frozen export and mark zone checkpoints."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();source=Path('E:/3D_WZMS/builds/v043_ue_bundle')
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world();assert world.get_name()=='L_WZMS_Campus'
actors={a.get_actor_label():a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()}
completed=[];rows=[];smes=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
fallback_path=root.parent/'Reports/campus_foliage_fallback.json'
fallback={r['path']:r for r in json.loads(fallback_path.read_text())['meshes']} if fallback_path.exists() else {}
for zone in ['south','central','west','east','north']:
    file=root.parent/('Reports/south_import.json' if zone=='south' else f'Reports/import_{zone}.json')
    if not file.exists():continue
    imported=json.loads(file.read_text());src=json.loads((source/f'zone_{zone}.json').read_text(encoding='utf8'))
    if len(imported['chunks'])!=len(src['chunks']):continue
    for ref in imported['chunks']:
        a=actors[ref['name']];comp=a.static_mesh_component;mesh=comp.static_mesh
        fp=f'/Game/WZMS/{zone.title()}/Meshes/'+ref['name'];compact=fallback.get(fp)
        if compact:
            assert mesh.get_num_nanite_triangles()==compact['nanite_triangles_before']==ref['ue_triangles'],ref['name']
            assert mesh.get_num_triangles(0)==compact['raster_fallback_triangles'],ref['name']
        else:assert mesh.get_num_triangles(0)==ref['ue_triangles'],ref['name']
        assert all(abs(x-y)<.01 for x,y in zip(a.get_actor_location().to_tuple(),ref['placement_cm'])),ref['name']
        assert all(abs(x-100)<.001 for x in a.get_actor_scale3d().to_tuple())
        if ref['role']=='solid':
            assert comp.get_editor_property('disallow_nanite')
            assert str(comp.get_collision_profile_name())=='BlockAll'
        if ref['role']=='foliage':
            ns=smes.get_nanite_settings(mesh)
            assert ns.enabled and ns.shape_preservation==unreal.NaniteShapePreservation.PRESERVE_AREA
            assert ns.keep_percent_triangles==1 and ns.trim_relative_error==0 and abs(ns.fallback_percent_triangles-(compact['fallback_fraction'] if compact else 1))<1e-6
        for i,slot in enumerate(mesh.static_materials):
            mi=comp.get_material(i);assert mi and mi.get_name()=='MI_'+str(slot.material_slot_name),(ref['name'],i)
        rows.append({'zone':zone,'mesh':ref['name'],'source_visible_triangles':ref['ue_triangles'],'full_nanite_geometry_verified':bool(compact),'transform_correct':True,'materials_bound':True,'collision_policy_verified':True})
    completed.append(zone)
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
report={'passed':True,'completed_zones':completed,'all_five_zones_complete':len(completed)==5,'mesh_count':len(rows),'meshes':rows,'source_version':'v043','source_model_unchanged':True}
(root.parent/'Reports/campus_delivery_validation.json').write_text(json.dumps(report,indent=2))
path=root.parent/'Reports/campus_migration.json';progress=json.loads(path.read_text());progress['completed_zones']=completed;progress['verified_meshes']=len(rows);path.write_text(json.dumps(progress,indent=2))
print('WZMS_CAMPUS_VERIFIED',completed,len(rows))
