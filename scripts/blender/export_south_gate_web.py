"""Run on a fresh background load; export an optimized copy without saving over .blend."""
from pathlib import Path
import bpy
import json
import time

ROOT=Path(__file__).resolve().parents[2]
scene=bpy.data.scenes['WZMS_SouthGate_Sample']
bpy.context.window.scene=scene
for o in scene.objects:o.select_set(False)
items=[o for o in scene.objects if o.type in {'MESH','CURVE'}]
for o in items:o.select_set(True)
bpy.context.view_layer.objects.active=items[0]
bpy.ops.object.convert(target='MESH')
for o in bpy.context.selected_objects:
    if o.type=='MESH' and o.data.uv_layers.active:
        o.data.uv_layers.active.name='UVMap'
bpy.ops.object.join()
joined=bpy.context.view_layer.objects.active
joined.name='WZMS_SouthGate_Web'
out=ROOT/'web-preview/assets/south-gate.glb'
out.parent.mkdir(parents=True,exist_ok=True)
start=time.monotonic()
bpy.ops.export_scene.gltf(
    filepath=str(out),export_format='GLB',use_selection=True,
    export_apply=True,export_animations=False,export_cameras=False,
    export_lights=False,export_extras=False,
    export_draco_mesh_compression_enable=True,
    export_draco_mesh_compression_level=6,
    export_draco_position_quantization=16,
    export_draco_normal_quantization=10,
    export_draco_texcoord_quantization=14,
)
report={'source':'models/south_gate/WZMS_SouthGate_v002.blend',
    'file':'web-preview/assets/south-gate.glb','bytes':out.stat().st_size,
    'source_objects':len(items),'joined_meshes':1,
    'geometry_simplified':False,'compression':'Draco',
    'seconds':round(time.monotonic()-start,2),
    'notes':['Original .blend was not overwritten.','Procedural paving recreated in web viewer; render gallery remains the appearance reference.']}
(ROOT/'deliverables/v0.0.3/export_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print('WZMS_WEB_EXPORT '+json.dumps(report,ensure_ascii=False),flush=True)
