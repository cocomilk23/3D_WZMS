"""Separate three proven overlapping slabs, preserving topology, materials and UVs."""
import array,hashlib,json,unreal
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve()
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
plan=json.loads((root.parent/'SourceReference/buqing_surface_separation.json').read_text(encoding='utf8'))
rows=[]
for row in plan['meshes']:
 mesh=unreal.load_asset(row['mesh']);assert mesh
 d=unreal.DynamicMesh();d,result=unreal.GeometryScript_AssetUtils.copy_mesh_from_static_mesh(mesh,d,unreal.GeometryScriptCopyMeshFromAssetOptions(apply_build_settings=True),unreal.GeometryScriptMeshReadLOD(lod_type=unreal.GeometryScriptLODType.SOURCE_MODEL,lod_index=0));assert result==unreal.GeometryScriptOutcomePins.SUCCESS
 _,vs,gaps=unreal.GeometryScript_MeshQueries.get_all_vertex_positions(d,False);assert not gaps
 _,ts,gaps=unreal.GeometryScript_MeshQueries.get_all_triangle_indices(d,False);assert not gaps
 original=[v.to_tuple() for v in vs.convert_vector_list_to_array()]
 triangles=array.array('i',(x for t in ts.convert_triangle_list_to_array() for x in t.to_tuple())).tobytes()
 assert hashlib.sha256(array.array('d',(x for p in original for x in p)).tobytes()).hexdigest()==row['positions_sha256']
 assert hashlib.sha256(triangles).hexdigest()==row['triangles_sha256']
 expected=list(original)
 for change in row['changes']:
  ids=change['vertex_ids'];shift=change['translation_local']
  _,selection=unreal.GeometryScript_MeshSelection.convert_index_array_to_mesh_selection(d,ids,unreal.GeometryScriptMeshSelectionType.VERTICES)
  unreal.GeometryScript_MeshTransforms.translate_mesh_selection(d,selection,unreal.Vector(*shift))
  for i in ids:expected[i]=tuple(original[i][k]+shift[k] for k in range(3))
 _,vs,gaps=unreal.GeometryScript_MeshQueries.get_all_vertex_positions(d,False);assert not gaps
 actual=[v.to_tuple() for v in vs.convert_vector_list_to_array()]
 assert actual==expected,'Unexpected vertex changes'
 _,ts,gaps=unreal.GeometryScript_MeshQueries.get_all_triangle_indices(d,False);assert not gaps
 assert array.array('i',(x for t in ts.convert_triangle_list_to_array() for x in t.to_tuple())).tobytes()==triangles
 opts=unreal.GeometryScriptCopyMeshToAssetOptions(enable_recompute_normals=False,enable_recompute_tangents=False,replace_materials=False,apply_nanite_settings=False)
 _,result=unreal.GeometryScript_AssetUtils.copy_mesh_to_static_mesh(d,mesh,opts,unreal.GeometryScriptMeshWriteLOD(lod_index=0));assert result==unreal.GeometryScriptOutcomePins.SUCCESS
 unreal.EditorAssetLibrary.save_loaded_asset(mesh)
 rows.append({'mesh':row['mesh'],'changes':row['changes'],'triangles_unchanged':True,'only_selected_vertices_changed':True,'new_positions_sha256':hashlib.sha256(array.array('d',(x for p in actual for x in p)).tobytes()).hexdigest()})
(root.parent/'Reports/buqing_surface_separation_applied.json').write_text(json.dumps({'meshes':rows,'runtime_validation_pending':True},indent=2)+'\n',encoding='utf8')
