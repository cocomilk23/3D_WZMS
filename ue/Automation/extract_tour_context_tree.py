"""Read an existing campus tree prototype for instanced district planting; never save Blender."""
import bpy,json
from pathlib import Path
from mathutils import Vector
root=Path('E:/WZMS_UE/ue');names=['Middle mature avenue tree scaffold branches','Middle mature avenue tree canopy leaves'];objects=[bpy.data.objects.get(n) for n in names];assert all(objects),[(n,bool(o)) for n,o in zip(names,objects)]
origin=objects[0].matrix_world.translation.copy();origin.z=min((objects[0].matrix_world@Vector(p)).z for p in objects[0].bound_box)
deps=bpy.context.evaluated_depsgraph_get();rows=[]
for obj in objects:
 evaluated=obj.evaluated_get(deps);mesh=evaluated.to_mesh();mesh.calc_loop_triangles();matrix=obj.matrix_world;normal_matrix=matrix.to_3x3().inverted().transposed();mats=[m.name for m in mesh.materials];buffers=[{'vertices':[],'triangles':[],'normals':[],'uv0':[],'material':i} for i in range(len(mats))];uv=mesh.uv_layers.active
 for tri in mesh.loop_triangles:
  b=buffers[tri.material_index];start=len(b['vertices'])
  for vi,li in zip(tri.vertices,tri.loops):
   p=matrix@mesh.vertices[vi].co-origin;n=(normal_matrix@mesh.corner_normals[li].vector).normalized();b['vertices'].append([p.x*100,-p.y*100,p.z*100]);b['normals'].append([n.x,-n.y,n.z]);b['uv0'].append(list(uv.data[li].uv) if uv else [0,0])
  b['triangles'].append([start,start+1,start+2])
 rows.append({'name':'SM_Tour_Context_Tree_'+('Leaves' if 'leaves' in obj.name else 'Branches'),'source_object':obj.name,'materials':mats,'buffers':buffers,'collision':False,'foliage':'leaves' in obj.name});evaluated.to_mesh_clear()
(root/'SourceReference/tour_context_tree_buffers.json').write_text(json.dumps({'source_file':bpy.data.filepath,'source_origin_m':list(origin),'objects':rows}),encoding='utf8')
print('CONTEXT_TREE',[(r['name'],sum(len(b['triangles']) for b in r['buffers']),r['materials']) for r in rows],flush=True)
