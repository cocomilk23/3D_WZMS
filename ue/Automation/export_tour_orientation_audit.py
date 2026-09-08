"""Read mesh topology into local analysis buffers; assets are never changed."""
import unreal,json,array
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();out=root/'Saved/OrientationAudit';out.mkdir(exist_ok=True)
request=root/'Saved/Logs/orientation_request.json';paths=json.loads(request.read_text()) if request.exists() else ['/Engine/BasicShapes/Cube','/Game/WZMS/East/Meshes/SM_east_solid_060','/Game/WZMS/East/Meshes/SM_east_solid_058','/Game/WZMS/West/Meshes/SM_west_solid_031']
rows=[]
for path in paths:
 mesh=unreal.load_asset(path);assert mesh;d=unreal.DynamicMesh();d,result=unreal.GeometryScript_AssetUtils.copy_mesh_from_static_mesh(mesh,d,unreal.GeometryScriptCopyMeshFromAssetOptions(apply_build_settings=True),unreal.GeometryScriptMeshReadLOD(lod_type=unreal.GeometryScriptLODType.SOURCE_MODEL,lod_index=0));assert result==unreal.GeometryScriptOutcomePins.SUCCESS
 _,ps,gaps=unreal.GeometryScript_MeshQueries.get_all_vertex_positions(d,False);assert not gaps
 _,ts,gaps=unreal.GeometryScript_MeshQueries.get_all_triangle_indices(d,False);assert not gaps
 positions=ps.convert_vector_list_to_array();triangles=ts.convert_triangle_list_to_array();name=mesh.get_name();vp=out/(name+'.f64');tp=out/(name+'.i32')
 array.array('d',(x for v in positions for x in v.to_tuple())).tofile(vp.open('wb'));array.array('i',(x for t in triangles for x in t.to_tuple())).tofile(tp.open('wb'))
 rows.append({'path':path,'name':name,'vertices':len(positions),'triangles':len(triangles),'positions_file':str(vp),'triangles_file':str(tp)})
(out/'meshes.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
