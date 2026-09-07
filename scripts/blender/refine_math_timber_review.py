"""Apply final classroom/rest refinements to the unsealed v037; review the affected cameras."""
import ast,bpy,sys,runpy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];S=ROOT/'scripts/blender';sys.path.insert(0,str(S))
rest_only='--rest-only' in sys.argv
import campus_common as c
from mathutils import Vector,Matrix
model=ROOT/'models/campus/WZMS_Campus_v037.blend'
assert not (ROOT/'deliverables/v0.0.37/delivery_validation.json').exists(),'Never change a sealed delivery'
bpy.ops.wm.open_mainfile(filepath=str(model));c.activate(bpy.data.scenes['WZMS_Campus'])
tree=ast.parse((S/'build_math_interior.py').read_text(encoding='utf8'))
functions=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['configure_math_timber','add_math_rest_details']]
exec(compile(ast.Module(body=functions,type_ignores=[]),'builder finish','exec'));configure_math_timber()
scene=bpy.data.scenes['WZMS_Campus']
for obj in list(scene.objects):
 if obj.name.startswith(('Math rest sofa supporting foot','Math rest mustard cushion','Math rest ambient fill')):bpy.data.objects.remove(obj,do_unlink=True)
before=set(scene.objects);add_math_rest_details();bpy.context.view_layer.update()
for obj in set(scene.objects)-before:obj.matrix_world=Matrix.Translation((0,-1,0))@obj.matrix_world
cam=scene.objects['158_Math_upper_rest_corner'];cam.location=(160.5,114,5.9);cam.rotation_euler=(Vector((160.5,119,5.0))-cam.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.wm.save_as_mainfile(filepath=str(model),compress=True)
sys.argv=['audit','--','37'];runpy.run_path(str(S/'audit_culture_delivery.py'),run_name='__main__')
report_path=ROOT/'deliverables/v0.0.37/render_validation.json';previous=json.loads(report_path.read_text(encoding='utf8'))
sys.argv=['render','--','v0.0.37']+(['158_Math_upper_rest_corner'] if rest_only else ['157_Math_traditional_classroom','158_Math_upper_rest_corner']);runpy.run_path(str(S/'render_campus.py'),run_name='__main__')
current=json.loads(report_path.read_text(encoding='utf8'));replacements={x['camera']:x for x in current['renders']}
current['renders']=[replacements.get(x['camera'],x) for x in previous['renders']]
current['selective_review_reason']='Classroom desk/beam shader, upstairs sofa feet/cushions and rest review camera refined. Other scene geometry, materials and review cameras retained.'
report_path.write_text(json.dumps(current,ensure_ascii=False,indent=2),encoding='utf8')
print('CULTURE_STAGE_REVIEW_READY 37',flush=True)
