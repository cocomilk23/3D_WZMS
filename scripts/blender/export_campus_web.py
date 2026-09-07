"""Export a browser copy of v015. Never save over the editable source .blend."""
import bpy,json,time,hashlib,math
import numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
source=ROOT/'models/campus/WZMS_Campus_v015.blend'
before=hashlib.sha256(source.read_bytes()).hexdigest();start=time.monotonic()
bpy.ops.wm.open_mainfile(filepath=str(source));scene=bpy.data.scenes['WZMS_Campus'];bpy.context.window.scene=scene
items=[o for o in scene.objects if o.type in {'MESH','CURVE','FONT'} and not o.hide_render]
original_faces=sum(len(o.data.polygons) for o in items if o.type=='MESH');reduced=[]
for mesh in list({o.data.name:o.data for o in items if o.type=='MESH'}.values()):
 # Known procedural leaves have five vertices and four triangular faces per leaf.
 if len(mesh.polygons)<4000 or len(mesh.vertices)*4!=len(mesh.polygons)*5:continue
 if not any(any(key in m.name.lower() for key in ['leaf','foliage','groundcover']) for m in mesh.materials if m):continue
 coords=np.empty(len(mesh.vertices)*3,dtype=np.float32);mesh.vertices.foreach_get('co',coords)
 leaves=coords.reshape(-1,5,3)[::4][:,[0,1,3,4],:].copy()
 center=leaves.mean(axis=1,keepdims=True);leaves=center+(leaves-center)*1.6
 ids=np.empty(len(mesh.polygons),dtype=np.int32);mesh.polygons.foreach_get('material_index',ids)
 ids=ids.reshape(-1,4)[::4,0];mats=list(mesh.materials);old_count=len(mesh.polygons)
 mesh.clear_geometry();mesh.from_pydata(leaves.reshape(-1,3).tolist(),[],np.arange(leaves.shape[0]*4).reshape(-1,4).tolist())
 mesh.polygons.foreach_set('material_index',ids);mesh.update()
 reduced.append({'mesh':mesh.name,'original_faces':old_count,'web_faces':len(mesh.polygons)})
print('WEB_FOLIAGE_LOD',len(reduced),flush=True)
# glTF does not carry Blender noise/ramp shaders. Retain photographs, use average
# procedural colours for the interactive copy; original renders remain available.
for mat in bpy.data.materials:
 if not mat.use_nodes:continue
 bs=next((n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
 if not bs:continue
 has_image=any(n.type=='TEX_IMAGE' and n.image for n in mat.node_tree.nodes)
 if not has_image:
  ramps=[n for n in mat.node_tree.nodes if n.type=='VALTORGB']
  if ramps:
   colors=[e.color[:] for e in ramps[0].color_ramp.elements]
   bs.inputs['Base Color'].default_value=[sum(c[i] for c in colors)/len(colors) for i in range(4)]
  for socket in bs.inputs:
   for link in list(socket.links):mat.node_tree.links.remove(link)
for o in scene.objects:o.select_set(False)
for o in items:o.select_set(True)
bpy.context.view_layer.objects.active=items[0]
bpy.ops.object.convert(target='MESH')
for o in bpy.context.selected_objects:
 if o.type=='MESH' and o.data.uv_layers.active:o.data.uv_layers.active.name='UVMap'
print('WEB_JOIN_START',len(items),flush=True)
bpy.ops.object.join();joined=bpy.context.view_layer.objects.active;joined.name='WZMS_Campus_v015_Web'
print('WEB_JOIN_DONE',len(joined.data.polygons),flush=True)
out=ROOT/'web-preview/assets/campus-v015.glb'
bpy.ops.export_scene.gltf(filepath=str(out),export_format='GLB',use_selection=True,
 export_apply=True,export_animations=False,export_cameras=False,export_lights=False,export_extras=False,
 export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,
 export_draco_position_quantization=18,export_draco_normal_quantization=10,export_draco_texcoord_quantization=14)
assert hashlib.sha256(source.read_bytes()).hexdigest()==before
report={'source':source.relative_to(ROOT).as_posix(),'source_sha256':before,'source_unchanged':True,
 'file':out.relative_to(ROOT).as_posix(),'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
 'original_objects':len(items),'original_faces_with_instances':original_faces,'web_faces':len(joined.data.polygons),
 'foliage_lod':reduced,'seconds':round(time.monotonic()-start,2),
 'notes':['Browser foliage uses one enlarged quad for every four procedural leaves.','Buildings, bridges and court geometry retained.','Procedural shader colours approximated; photographs retained.','No walking collision; orbit inspection only.']}
dest=ROOT/'deliverables/v0.0.16';dest.mkdir(parents=True,exist_ok=True)
(dest/'export_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print('WZMS_CAMPUS_WEB_EXPORT_COMPLETE',out.stat().st_size,flush=True)
