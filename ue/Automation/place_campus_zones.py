"""Assemble complete staged zones in the shared campus map, preserving accepted assets."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();assets=unreal.EditorAssetLibrary
levels=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
if unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world().get_name()!='L_WZMS_Campus':
    assert levels.load_level('/Game/WZMS/Maps/L_WZMS_Campus')
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);existing={a.get_actor_label():a for a in actors.get_all_level_actors()}
for zone in ['central','west','east','north']:
    path=root.parent/f'Reports/import_{zone}.json'
    if not path.exists():continue
    report=json.loads(path.read_text())
    if not report['complete']:continue
    for ref in report['chunks']:
        if ref['name'] in existing and not ref.get('pending_campus_placement',False):continue
        mesh=assets.load_asset(ref['path']);assert mesh
        loc=unreal.Vector(*ref['placement_cm']);a=existing.get(ref['name']) or actors.spawn_actor_from_class(unreal.StaticMeshActor,loc)
        a.set_actor_label(ref['name']);a.set_actor_location(loc,False,True);a.set_actor_scale3d(unreal.Vector(100,100,100));a.set_folder_path(zone.title()+'/'+ref['role'])
        comp=a.static_mesh_component;comp.set_static_mesh(mesh);comp.set_mobility(unreal.ComponentMobility.STATIC);comp.set_editor_property('disallow_nanite',ref['role']=='solid')
        comp.set_collision_profile_name('BlockAll' if ref['role']=='solid' else 'NoCollision');comp.set_editor_property('cast_shadow',ref['role'] not in ['glass','water'])
        for i,slot in enumerate(mesh.static_materials):
            mi=assets.load_asset('/Game/WZMS/Materials/Instances/MI_'+str(slot.material_slot_name));assert mi;comp.set_material(i,mi)
        ref['pending_campus_placement']=False
    assert levels.save_current_level()
    path.write_text(json.dumps(report,indent=2))
print('WZMS staged zones assembled')
