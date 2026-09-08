"""Grass leaves remain visible but no longer participate in character collision."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();source=json.loads(Path('E:/3D_WZMS/builds/v043_ue_bundle/materials.json').read_text(encoding='utf8'))
ids={r['id']:r['source_name'] for r in source['materials'] if r['source_name']=='Natural lawn blades'};assert ids
ss=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem);rows=[]
for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors():
 if not isinstance(a,unreal.StaticMeshActor):continue
 mesh=a.static_mesh_component.static_mesh
 if not mesh:continue
 slots={i:str(s.material_slot_name) for i,s in enumerate(mesh.static_materials) if str(s.material_slot_name) in ids}
 if not slots:continue
 before=mesh.get_num_triangles(0)
 for sec in range(mesh.get_num_sections(0)):
  slot=ss.get_lod_material_slot(mesh,0,sec)
  if slot in slots:
   ss.enable_section_collision(mesh,False,0,sec)
   rows.append({'mesh':mesh.get_path_name(),'section':sec,'material':ids[slots[slot]],'collision_enabled':ss.is_section_collision_enabled(mesh,0,sec)})
 unreal.EditorAssetLibrary.save_loaded_asset(mesh);assert mesh.get_num_triangles(0)==before
assert rows and all(not r['collision_enabled'] for r in rows)
(root.parent/'Reports/tour_grass_collision.json').write_text(json.dumps({'sections':rows,'visible_geometry_unchanged':True,'underlying_soil_collision_retained':True},indent=2))
