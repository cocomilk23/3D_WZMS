"""Run audits and each review camera in separate, serial Blender processes."""
import argparse,sys,subprocess,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts/blender'))
from culture_stages import STAGES
p=argparse.ArgumentParser();p.add_argument('revision',type=int);p.add_argument('--render-only',action='store_true');p.add_argument('--build',action='store_true');a=p.parse_args()
if a.build and a.render_only:p.error('--build requires the full audits')
rev=a.revision;version=f'v0.0.{rev}';stage=STAGES[rev];out=R/'deliverables'/version
model=R/f'models/campus/WZMS_Campus_v{rev:03}.blend'
blender=Path('D:/Program Files/Blender Foundation/Blender 5.1/blender.exe')
(R/'builds').mkdir(parents=True,exist_ok=True)
def run(label,arguments,marker):
 log=R/'builds'/f'v{rev:03}_{label}.log'
 with log.open('w',encoding='utf8') as handle:
  process=subprocess.run([str(blender),'--factory-startup','-b','--threads','6']+arguments,cwd=R,stdout=handle,stderr=subprocess.STDOUT,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
 text=log.read_text(encoding='utf8',errors='replace')
 if process.returncode or marker not in text:raise RuntimeError(f'{label} failed; inspect {log}')
 print('ISOLATED_STAGE_DONE',label,flush=True)
if a.build:
 previous=R/f'models/campus/WZMS_Campus_v{stage["previous"]:03}.blend'
 run('build',[str(previous),'--python',f'scripts/blender/{stage["builder"]}'],f'WZMS_BUILD_COMPLETE {rev}')
frozen_hash=hashlib.sha256(model.read_bytes()).hexdigest()
if not a.render_only:
 run('geometry',['--python','scripts/blender/audit_culture_delivery.py','--',str(rev)],f'CULTURE_AUDIT_COMPLETE {rev}')
 run('south_wall',['--python','scripts/blender/audit_culture_south_wall.py','--',version],'SOUTH_REVERSE_WALL_PRESERVED True')
merged=None;renders=[]
for camera in stage['cameras']:
 run(camera,[str(model),'--python','scripts/blender/render_campus.py','--',version,camera,'--no-persistent-data'],f'WZMS_RENDER_COMPLETE {version}')
 current=json.loads((out/'render_validation.json').read_text(encoding='utf8'))
 assert current['version']==version and current['samples']==96 and not current['missing_external_images']
 assert current['renders'][0]['camera']==camera
 if merged is None:merged=current
 else:
  assert all(current[k]==merged[k] for k in ['objects','mesh_polygons','metric_units','samples'])
 renders+=current['renders']
assert hashlib.sha256(model.read_bytes()).hexdigest()==frozen_hash,'Model changed during review'
merged['renders']=renders;merged['isolated_process_per_camera']=True;merged['reviewed_model_sha256']=frozen_hash
(out/'render_validation.json').write_text(json.dumps(merged,ensure_ascii=False,indent=2),encoding='utf8')
print('ISOLATED_DELIVERY_REVIEW_READY',version,flush=True)
