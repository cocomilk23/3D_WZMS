"""Reframe only camera 67 after a blocked composition, retaining unaffected rendered views.
Geometry, materials and lights do not change. Audit the saved file again, then render 67.
"""
import bpy,sys,json,runpy
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];S=ROOT/'scripts/blender';sys.path.insert(0,str(S))
out=ROOT/'deliverables/v0.0.18';old=json.loads((out/'render_validation.json').read_text(encoding='utf8'))
assert len(old['renders'])==5
path=ROOT/'models/campus/WZMS_Campus_v018.blend';bpy.ops.wm.open_mainfile(filepath=str(path))
sc=bpy.data.scenes['WZMS_Campus'];bpy.context.window.scene=sc;o=sc.objects['67_Library_ground_hall']
o.location=(115.6,155,1.65);o.rotation_euler=(Vector((126,155,2.1))-o.location).to_track_quat('-Z','Y').to_euler();o.data.lens=18;sc.camera=o
bpy.ops.wm.save_as_mainfile(filepath=str(path),compress=True)
sys.argv=['audit','--','18'];runpy.run_path(str(S/'audit_culture_delivery.py'),run_name='__main__')
sys.argv=['render','--','v0.0.18','67_Library_ground_hall'];runpy.run_path(str(S/'render_campus.py'),run_name='__main__')
new=json.loads((out/'render_validation.json').read_text(encoding='utf8'));new['renders']=new['renders']+old['renders'][1:]
new['selective_camera_refresh']={'changed_camera':'67_Library_ground_hall','reason':'Move away from foreground exhibition board; wider central entrance view','retained_views':old['renders'][1:],'unchanged_inputs_for_retained_views':'Geometry, materials, lights, world and the four other camera settings unchanged; only camera67 transform/lens and active scene camera changed'}
(out/'render_validation.json').write_text(json.dumps(new,ensure_ascii=False,indent=2),encoding='utf8')
print('LIBRARY_HALL_CAMERA_REFRESH_COMPLETE',flush=True)
