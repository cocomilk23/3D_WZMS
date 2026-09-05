"""Render saved sample cameras, then record structural checks from a fresh load."""
from pathlib import Path
import bpy
import json
import time
import sys

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'deliverables/v0.0.2/previews'
OUT.mkdir(parents=True,exist_ok=True)
scene=bpy.data.scenes['WZMS_SouthGate_Sample']
bpy.context.window.scene=scene
scene.render.engine='CYCLES'
scene.cycles.samples=48
scene.cycles.use_denoising=True
device_info=[]
try:
    prefs=bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type='OPTIX'
    prefs.get_devices()
    for d in prefs.devices:
        d.use=d.type=='OPTIX'
        device_info.append({'name':d.name,'type':d.type,'enabled':bool(d.use)})
    scene.cycles.device='GPU' if any(d['enabled'] for d in device_info) else 'CPU'
except Exception as ex:
    scene.cycles.device='CPU'
    device_info.append({'fallback':str(ex)})
print('WZMS_RENDER_DEVICE '+json.dumps(device_info,ensure_ascii=False),flush=True)
names=['01_Front_reference','02_Oblique_walkup','03_Aerial_overview','04_Ground_detail']
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
if args:names=args
renders=[]
for name in names:
    scene.camera=scene.objects[name]
    scene.render.filepath=str(OUT/(name+'.png'))
    start=time.monotonic()
    bpy.ops.render.render(write_still=True)
    renders.append({'camera':name,'seconds':round(time.monotonic()-start,2),'file':str(Path('previews')/(name+'.png'))})
missing=[]
for im in bpy.data.images:
    if im.source=='FILE' and not im.packed_file and not Path(bpy.path.abspath(im.filepath)).exists():
        missing.append(im.filepath)
checks={
    'opened_saved_blend':bpy.data.filepath,
    'sample_scene':scene.name,
    'render_device':scene.cycles.device,
    'devices':device_info,
    'renders':renders,
    'missing_external_images':missing,
    'name_wall_exists':'South gate · curved name wall' in scene.objects,
    'camera_count':sum(o.type=='CAMERA' for o in scene.objects),
    'metric_units':scene.unit_settings.system=='METRIC',
    'absolute_scale_verified':False,
    'ue_playthrough_verified':False,
}
(OUT.parent/'render_validation.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf8')
print('WZMS_RENDER_VALIDATION '+json.dumps(checks,ensure_ascii=False),flush=True)
if missing:raise RuntimeError('Missing external images')
