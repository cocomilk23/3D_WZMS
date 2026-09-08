import unreal,json
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()).resolve()
zone=json.loads(Path('E:/3D_WZMS/builds/v043_ue_bundle/zone_south.json').read_text(encoding='utf8'))
assets=unreal.EditorAssetLibrary
actors={a.get_actor_label():a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()}
for ch in zone['chunks']:
    mesh=assets.load_asset('/Game/WZMS/South/Meshes/'+ch['name']);assert mesh,ch['name']
    actor=actors[ch['name']]
    for index,slot in enumerate(mesh.static_materials):
        material=assets.load_asset('/Game/WZMS/Materials/Instances/MI_'+str(slot.material_slot_name));assert material
        actor.static_mesh_component.set_material(index,material)
source=json.loads(Path('E:/3D_WZMS/builds/v043_ue_bundle/materials.json').read_text(encoding='utf8'))
used={m for c in zone['chunks'] for m in c['materials']};rows=[]
for row in source['materials']:
    if row['id'] not in used:continue
    path='/Game/WZMS/Materials/Instances/MI_'+row['id'];mi=assets.load_asset(path);assert mi,path
    rows.append({'id':row['id'],'source_name':row['source_name'],'instance':path,'parent':mi.parent.get_path_name(),'source_photos':row['textures'],'source_transfer_status':row['transfer_status']})
report={'complete':True,'materials':rows,'binding':'StaticMeshComponent overrides; material edits do not rebuild mesh geometry','note':'UE material reconstruction; not shader-identical to Blender.'}
path=ROOT.parent/'Reports/south_materials.json';path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
