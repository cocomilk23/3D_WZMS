"""Fresh-load delivery rendering and dependency/scale inspection.
Usage: blender -b FILE --python render_campus.py -- VERSION CAMERA ...
"""
import bpy, sys, time, json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import campus_common as c
args=sys.argv[sys.argv.index('--')+1:];version=args[0];names=args[1:]
scene=bpy.data.scenes['WZMS_Campus'];c.activate(scene);c.render_setup(scene)
if scene.get('render_review_samples'):
    scene.cycles.samples=int(scene['render_review_samples'])
prefs=bpy.context.preferences.addons['cycles'].preferences
prefs.compute_device_type='OPTIX';prefs.get_devices()
devices=[]
for d in prefs.devices:
    d.use=d.type=='OPTIX';devices.append({'name':d.name,'type':d.type,'use':bool(d.use)})
scene.cycles.device='GPU' if any(d['use'] for d in devices) else 'CPU'
# Reuse the same scene's acceleration data across review cameras. Image size,
# sample count and material settings are unchanged; cache dies with this process.
scene.render.use_persistent_data=True
out=c.ROOT/'deliverables'/version/'previews';out.mkdir(parents=True,exist_ok=True)
r=[]
for name in names:
    scene.camera=scene.objects[name];scene.render.filepath=str(out/(name+'.png'))
    st=time.monotonic();bpy.ops.render.render(write_still=True)
    r.append({'camera':name,'seconds':round(time.monotonic()-st,2),'file':'previews/'+name+'.png'})
    print('WZMS_CAMERA_DONE '+name,flush=True)
missing=[im.filepath for im in bpy.data.images if im.source=='FILE' and not im.packed_file and not Path(bpy.path.abspath(im.filepath)).exists()]
report={'opened_saved_blend':bpy.data.filepath,'version':scene.get('delivery_version'),
 'objects':len(scene.objects),'mesh_polygons':sum(len(o.data.polygons) for o in scene.objects if o.type=='MESH'),
 'collections':[c.name for c in scene.collection.children],
 'metric_units':scene.unit_settings.system=='METRIC','missing_external_images':missing,
 'devices':devices,'persistent_render_data':bool(scene.render.use_persistent_data),'samples':scene.cycles.samples,'renders':r,'absolute_scale_verified':False,'user_acceptance':'pending','ue_playthrough_verified':False}
(out.parent/'render_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
if missing:raise RuntimeError(missing)
print('WZMS_RENDER_COMPLETE '+version,flush=True)
