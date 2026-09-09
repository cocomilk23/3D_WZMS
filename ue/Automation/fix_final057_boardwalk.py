"""Separate the timber walking surface and its joint bed from the underlying shore path."""
import unreal,json,array,hashlib
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();report=root.parent/'Reports/final057_boardwalk_fix.json';assert not report.exists()
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
mesh=unreal.load_asset('/Game/WZMS/West/Meshes/SM_west_solid_040');before=mesh.get_num_triangles(0)
slots=[str(s.material_slot_name) for s in mesh.static_materials];wanted={'M_8292fae4ec5fce','M_f926dc1ab529aa'};selected=[i for i,x in enumerate(slots) if x in wanted];assert len(selected)==2
d=unreal.DynamicMesh();d,result=unreal.GeometryScript_AssetUtils.copy_mesh_from_static_mesh(mesh,d,unreal.GeometryScriptCopyMeshFromAssetOptions(apply_build_settings=True),unreal.GeometryScriptMeshReadLOD(lod_type=unreal.GeometryScriptLODType.SOURCE_MODEL,lod_index=0));assert result==unreal.GeometryScriptOutcomePins.SUCCESS
_,ts,gaps=unreal.GeometryScript_MeshQueries.get_all_triangle_indices(d,False);assert not gaps;tri=[x.to_tuple() for x in ts.convert_triangle_list_to_array()]
_,vs,gaps=unreal.GeometryScript_MeshQueries.get_all_vertex_positions(d,False);assert not gaps;pos=[x.to_tuple() for x in vs.convert_vector_list_to_array()]
ids=set();face_count=0
for slot in selected:
 _,ls=unreal.GeometryScript_Materials.get_triangles_by_material_id(d,slot);faces=ls.convert_index_list_to_array();face_count+=len(faces)
 for tid in faces:ids.update(tri[tid])
assert ids and face_count>100
_,selection=unreal.GeometryScript_MeshSelection.convert_index_array_to_mesh_selection(d,sorted(ids),unreal.GeometryScriptMeshSelectionType.VERTICES)
unreal.GeometryScript_MeshTransforms.translate_mesh_selection(d,selection,unreal.Vector(0,0,.02))
_,vs,gaps=unreal.GeometryScript_MeshQueries.get_all_vertex_positions(d,False);actual=[x.to_tuple() for x in vs.convert_vector_list_to_array()]
assert all(q==(p[0],p[1],p[2]+.02) if i in ids else q==p for i,(p,q) in enumerate(zip(pos,actual)))
opts=unreal.GeometryScriptCopyMeshToAssetOptions(enable_recompute_normals=False,enable_recompute_tangents=False,replace_materials=False,apply_nanite_settings=False)
_,result=unreal.GeometryScript_AssetUtils.copy_mesh_to_static_mesh(d,mesh,opts,unreal.GeometryScriptMeshWriteLOD(lod_index=0));assert result==unreal.GeometryScriptOutcomePins.SUCCESS
assert mesh.get_num_triangles(0)==before;assert unreal.EditorAssetLibrary.save_loaded_asset(mesh)
report.write_text(json.dumps({'mesh':mesh.get_path_name(),'selected_materials':sorted(wanted),'affected_vertices':len(ids),'affected_triangles':face_count,'surface_raise_m':.02,'triangle_count_unchanged':before,'uv_materials_and_renderer_preserved':True,'old_positions_sha256':hashlib.sha256(array.array('d',(x for p in pos for x in p)).tobytes()).hexdigest(),'visual_and_local_route_review_pending':True},indent=2))
