"""Correct only proven inward closed components; preserve every vertex and triangle."""
import unreal,json,array,hashlib
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();selection=json.loads((root.parent/'SourceReference/tour_orientation_selection.json').read_text(encoding='utf8'));rows=[]
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world(),'Stop PIE before rebuilding collision'
for row in selection['meshes']:
 ids=row['flip_triangle_ids']
 if not ids:continue
 assert row['path'].startswith('/Game/WZMS/'),row['path']
 mesh=unreal.load_asset(row['path']);assert mesh;before=mesh.get_num_triangles(0);d=unreal.DynamicMesh();d,result=unreal.GeometryScript_AssetUtils.copy_mesh_from_static_mesh(mesh,d,unreal.GeometryScriptCopyMeshFromAssetOptions(apply_build_settings=True),unreal.GeometryScriptMeshReadLOD(lod_type=unreal.GeometryScriptLODType.SOURCE_MODEL,lod_index=0));assert result==unreal.GeometryScriptOutcomePins.SUCCESS
 _,ps,vgaps=unreal.GeometryScript_MeshQueries.get_all_vertex_positions(d,False);_,ts,tgaps=unreal.GeometryScript_MeshQueries.get_all_triangle_indices(d,False);assert not vgaps and not tgaps
 vb=array.array('d',(x for v in ps.convert_vector_list_to_array() for x in v.to_tuple())).tobytes();tb=array.array('i',(x for t in ts.convert_triangle_list_to_array() for x in t.to_tuple())).tobytes()
 assert hashlib.sha256(vb).hexdigest()==row['positions_sha256'],row['name']
 assert hashlib.sha256(tb).hexdigest()==row['triangles_sha256'],row['name']
 _,selected=unreal.GeometryScript_MeshSelection.convert_index_array_to_mesh_selection(d,ids,unreal.GeometryScriptMeshSelectionType.TRIANGLES)
 unreal.GeometryScript_Normals.flip_triangle_selection_normals(d,selected,True,True)
 _,after_positions,gaps=unreal.GeometryScript_MeshQueries.get_all_vertex_positions(d,False);assert not gaps
 assert array.array('d',(x for v in after_positions.convert_vector_list_to_array() for x in v.to_tuple())).tobytes()==vb
 opts=unreal.GeometryScriptCopyMeshToAssetOptions(enable_recompute_normals=False,enable_recompute_tangents=True,replace_materials=False,apply_nanite_settings=False)
 _,result=unreal.GeometryScript_AssetUtils.copy_mesh_to_static_mesh(d,mesh,opts,unreal.GeometryScriptMeshWriteLOD(lod_index=0));assert result==unreal.GeometryScriptOutcomePins.SUCCESS
 assert mesh.get_num_triangles(0)==before==row['triangles'],row['name'];unreal.EditorAssetLibrary.save_loaded_asset(mesh)
 rows.append({'mesh':row['path'],'inward_components_corrected':len(row['inward_closed_components']),'triangles_flipped':len(ids),'triangles_before':before,'triangles_after':mesh.get_num_triangles(0),'vertex_positions_bitwise_unchanged':True,'source_positions_sha256':row['positions_sha256'],'source_triangles_sha256':row['triangles_sha256']})
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
(root.parent/'Reports/tour_orientation_repair.json').write_text(json.dumps({'meshes':rows,'method':selection['method'],'geometry_decimation':False,'runtime_revalidation_pending':True},indent=2),encoding='utf8')
