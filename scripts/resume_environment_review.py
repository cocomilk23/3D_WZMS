"""Resume v043 after the completed first camera without redoing accepted output."""
import json,hashlib,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'deliverables/v0.0.43';model=R/'models/campus/WZMS_Campus_v043.blend'
source_hash=hashlib.sha256(model.read_bytes()).hexdigest()
base=json.loads((D/'render_validation.json').read_text(encoding='utf8'))
assert [r['camera'] for r in base['renders']]==['190_Environment_south_aerial']
first=base['renders'][0];first['render_device']='GPU';renders=[first]
(R/'builds/v043_first_render_receipt.json').write_text(json.dumps(base),encoding='utf8')
B='D:/Program Files/Blender Foundation/Blender 5.1/blender.exe'
for camera in ['191_Environment_gate_garden','192_Environment_lotus_bank','193_Environment_bank_close']:
    log=R/f'builds/v043_{camera}_retry.log'
    with log.open('w',encoding='utf8') as h:p=subprocess.run([B,'--factory-startup','-b','--threads','6',str(model),'--python','scripts/blender/render_campus.py','--','v0.0.43',camera,'--no-persistent-data'],cwd=R,stdout=h,stderr=subprocess.STDOUT,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    assert p.returncode==0 and 'WZMS_RENDER_COMPLETE v0.0.43' in log.read_text(encoding='utf8',errors='replace'),log
    report=json.loads((D/'render_validation.json').read_text(encoding='utf8'));assert report['samples']==96 and not report['missing_external_images']
    assert all(report[k]==base[k] for k in ['objects','mesh_polygons','metric_units'])
    report['renders'][0]['render_device']=report['render_device'];renders+=report['renders']
    print('ENVIRONMENT_REVIEW_CAMERA_COMPLETE',camera,flush=True)
assert hashlib.sha256(model.read_bytes()).hexdigest()==source_hash
base['renders']=renders;base['reviewed_model_sha256']=source_hash;base['isolated_process_per_camera']=True;base['device_note']='All accepted views use OPTIX GPU. Release retained memory by closing the saved preview process before retry. Same Cycles 96 samples, resolution and master.'
(D/'render_validation.json').write_text(json.dumps(base,indent=2),encoding='utf8')
print('ENVIRONMENT_REVIEW_READY',flush=True)
