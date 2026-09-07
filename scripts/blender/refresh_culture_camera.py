"""Reframe one unsealed milestone camera; retain and hash-check unaffected views."""
import bpy,sys,json,runpy,hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];S=ROOT/'scripts/blender';sys.path.insert(0,str(S))
from culture_stages import STAGES
args=sys.argv[sys.argv.index('--')+1:];rev=int(args[0]);name=args[1];loc=tuple(map(float,args[2].split(',')));target=Vector(tuple(map(float,args[3].split(','))));lens=float(args[4])
out=ROOT/f'deliverables/v0.0.{rev}';assert not (out/'delivery_validation.json').exists(),'Cannot modify a sealed delivery'
old=json.loads((out/'render_validation.json').read_text(encoding='utf8'));assert [r['camera'] for r in old['renders']]==STAGES[rev]['cameras'] and name in STAGES[rev]['cameras']
retained=[r for r in old['renders'] if r['camera']!=name]
hashes={r['file']:hashlib.sha256((out/r['file']).read_bytes()).hexdigest() for r in retained}
path=ROOT/f'models/campus/WZMS_Campus_v{rev:03}.blend';before=hashlib.sha256(path.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(path));sc=bpy.data.scenes['WZMS_Campus'];bpy.context.window.scene=sc
o=sc.objects[name];o.location=loc;o.rotation_euler=(target-o.location).to_track_quat('-Z','Y').to_euler();o.data.lens=lens
bpy.ops.wm.save_as_mainfile(filepath=str(path),compress=True)
sys.argv=['audit','--',str(rev)];runpy.run_path(str(S/'audit_culture_delivery.py'),run_name='__main__')
sys.argv=['render','--',f'v0.0.{rev}',name];runpy.run_path(str(S/'render_campus.py'),run_name='__main__')
new=json.loads((out/'render_validation.json').read_text(encoding='utf8'));changed=new['renders'][0]
new['renders']=[changed if r['camera']==name else r for r in old['renders']]
assert all(hashlib.sha256((out/f).read_bytes()).hexdigest()==h for f,h in hashes.items())
new['selective_camera_refresh']=old.get('selective_camera_refresh',[])+[{'camera':name,'prior_model_sha256':before,'retained_image_hashes':hashes,'retained_inputs':'Geometry, materials, lights, world and all other camera settings unchanged; retained files hash-checked'}]
(out/'render_validation.json').write_text(json.dumps(new,ensure_ascii=False,indent=2),encoding='utf8')
print('CULTURE_CAMERA_REFRESH_COMPLETE',rev,name,flush=True)
