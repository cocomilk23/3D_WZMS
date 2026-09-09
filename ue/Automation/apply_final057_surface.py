"""Apply one fingerprint-checked surface repair, preserving materials and interpolated UVs."""
import unreal,json,array,hashlib,math
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();ue=root.parent
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
name=json.loads((root/'Saved/Logs/final057_mesh_request.json').read_text())['name']
row=next(r for r in json.loads((ue/'SourceReference/final057_surface_patch.json').read_text()) if r['name']==name)
report=ue/'Reports/final057_surface_applied.json';state=json.loads(report.read_text()) if report.exists() else {'meshes':[]}
assert name not in [r['name'] for r in state['meshes']],'Already repaired; do not repeat'
mesh=unreal.load_asset(row['mesh']);assert mesh;before=mesh.get_num_triangles(0);d=unreal.DynamicMesh()
d,result=unreal.GeometryScript_AssetUtils.copy_mesh_from_static_mesh(mesh,d,unreal.GeometryScriptCopyMeshFromAssetOptions(apply_build_settings=True),unreal.GeometryScriptMeshReadLOD(lod_type=unreal.GeometryScriptLODType.SOURCE_MODEL,lod_index=0));assert result==unreal.GeometryScriptOutcomePins.SUCCESS
_,vs,vg=unreal.GeometryScript_MeshQueries.get_all_vertex_positions(d,False);_,ts,tg=unreal.GeometryScript_MeshQueries.get_all_triangle_indices(d,False);assert not vg and not tg
vb=array.array('d',(x for v in vs.convert_vector_list_to_array() for x in v.to_tuple())).tobytes();tb=array.array('i',(x for t in ts.convert_triangle_list_to_array() for x in t.to_tuple())).tobytes()
assert hashlib.sha256(vb).hexdigest()==row['positions_sha256'],name
assert hashlib.sha256(tb).hexdigest()==row['triangles_sha256'],name
buffers={};ids=set(row['delete_triangles']);added=0;discarded_sliver_area=0.0
def weighted(values,w,n):return [sum(values[j][k]*w[j] for j in range(3)) for k in range(n)]
for change in row.get('clipped_triangles',[]):
 tid=change['triangle'];assert tid not in ids;ids.add(tid)
 ok,*p=unreal.GeometryScript_MeshQueries.get_triangle_positions(d,tid);assert ok
 u1,u2,u3,ok=unreal.GeometryScript_MeshQueries.get_triangle_u_vs(d,0,tid);assert ok
 _,n1,n2,n3,ok=unreal.GeometryScript_MeshQueries.get_triangle_normals(d,tid);assert ok
 mat,ok=unreal.GeometryScript_Materials.get_triangle_material_id(d,tid);assert ok
 buf=buffers.setdefault(mat,{'vertices':[],'triangles':[],'normals':[],'uv0':[]});p=[x.to_tuple() for x in p];uv=[u1.to_tuple(),u2.to_tuple(),u3.to_tuple()];nn=[n1.to_tuple(),n2.to_tuple(),n3.to_tuple()]
 for tri in change['barycentric_triangles']:
  xyz=[weighted(p,w,3) for w in tri]
  a=[xyz[1][i]-xyz[0][i] for i in range(3)];b=[xyz[2][i]-xyz[0][i] for i in range(3)]
  cross=[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];area=math.sqrt(sum(x*x for x in cross))*.5
  shortest=min(math.sqrt(sum((xyz[i][k]-xyz[j][k])**2 for k in range(3))) for i,j in [(0,1),(1,2),(2,0)])
  if area<.000001 or shortest<.0001:
   discarded_sliver_area+=area;continue
  st=len(buf['vertices'])
  for w in tri:
   pos=weighted(p,w,3);normal=weighted(nn,w,3);ln=math.sqrt(sum(x*x for x in normal));normal=[x/ln for x in normal]
   buf['vertices'].append(unreal.Vector(*pos));buf['normals'].append(unreal.Vector(*normal));buf['uv0'].append(unreal.Vector2D(*weighted(uv,w,2)))
  buf['triangles'].append(unreal.IntVector(st,st+1,st+2));added+=1
_,selection=unreal.GeometryScript_MeshSelection.convert_index_array_to_mesh_selection(d,sorted(ids),unreal.GeometryScriptMeshSelectionType.TRIANGLES)
_,deleted=unreal.GeometryScript_MeshEdits.delete_selected_triangles_from_mesh(d,selection);assert deleted==len(ids)
for mat,buf in buffers.items():unreal.GeometryScript_MeshEdits.append_buffers_to_mesh(d,unreal.GeometryScriptSimpleMeshBuffers(**buf),mat)
opts=unreal.GeometryScriptCopyMeshToAssetOptions(enable_recompute_normals=False,enable_recompute_tangents=True,replace_materials=False,apply_nanite_settings=False)
_,result=unreal.GeometryScript_AssetUtils.copy_mesh_to_static_mesh(d,mesh,opts,unreal.GeometryScriptMeshWriteLOD(lod_index=0));assert result==unreal.GeometryScriptOutcomePins.SUCCESS
after=mesh.get_num_triangles(0);assert after==before-deleted+added,(name,before,after,deleted,added)
assert unreal.EditorAssetLibrary.save_loaded_asset(mesh)
state['meshes'].append({'name':name,'mesh':row['mesh'],'triangles_before':before,'deleted':deleted,'added_clipped_triangles':added,'triangles_after':after,'discarded_numerical_sliver_area_m2':discarded_sliver_area,'fingerprints_verified':True,'surface_clips':len(row.get('clipped_triangles',[])),'replacements':row['replacements'],'uv_and_materials_preserved':True})
report.write_text(json.dumps(state,indent=2)+'\n',encoding='utf8')
