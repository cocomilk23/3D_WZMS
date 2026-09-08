"""Serial bounded-memory export + full FBX roundtrip; create a hashed LFS delivery ZIP."""
import subprocess,json,hashlib,zipfile,os,argparse
from pathlib import Path
R=Path(__file__).resolve().parents[1];B=Path('D:/Program Files/Blender Foundation/Blender 5.1/blender.exe')
OUT=R/'builds/v043_ue_bundle';D=R/'deliverables/v0.0.43';OUT.mkdir(parents=True,exist_ok=True)
p=argparse.ArgumentParser();p.add_argument('--audit-only',action='store_true');p.add_argument('--zones',nargs='+',default=['south','central','west','east','north']);a=p.parse_args()
def run(script,zone,marker,source=False):
    log=R/'builds'/('v043_'+Path(script).stem+'_'+zone+'.log')
    args=[str(B),'--factory-startup','-b','--threads','6']
    if source:args+=[str(R/'models/campus/WZMS_Campus_v043.blend')]
    args+=['--python',str(R/'scripts/blender'/script),'--',zone]
    env=os.environ.copy();temp=R/'builds/v043_temp';temp.mkdir(exist_ok=True);env['TEMP']=env['TMP']=str(temp)
    with log.open('w',encoding='utf8') as handle:q=subprocess.run(args,cwd=R,stdout=handle,stderr=subprocess.STDOUT,env=env,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    if q.returncode or marker not in log.read_text(encoding='utf8',errors='replace'):raise RuntimeError(str(log))
    print(marker,zone,flush=True)
for zone in a.zones:
    if not a.audit_only:run('export_ue_transfer_v043.py',zone,'UE_TRANSFER_ZONE_COMPLETE',True)
    run('audit_ue_transfer_v043.py',zone,'UE_ROUNDTRIP_ZONE_COMPLETE')
if set(a.zones)!=set(['south','central','west','east','north']):raise SystemExit('Subset checked; run all zones before packaging.')
source=R/'models/campus/WZMS_Campus_v043.blend';source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
zones=[json.loads((OUT/f'zone_{z}.json').read_text(encoding='utf8')) for z in a.zones]
checks=[json.loads((OUT/f'roundtrip_{z}.json').read_text(encoding='utf8')) for z in a.zones]
assert all(z['source_sha256']==source_hash for z in zones+checks) and all(z['all_passed'] for z in checks)
materials=json.loads((OUT/'materials.json').read_text(encoding='utf8'));assert materials['source_sha256']==source_hash
for im in materials['textures']:assert hashlib.sha256((OUT/im['file']).read_bytes()).hexdigest()==im['sha256']
objects=[o['object'] for z in zones for o in z['objects']];assert len(objects)==len(set(objects))
assert all(z['source_visible_mesh_total']==len(objects) for z in zones),'Whole-campus source coverage incomplete'
chunks=[c for z in zones for c in z['chunks']]
assert sum(o.get('evaluated_triangles',0) for z in zones for o in z['objects'])==sum(c['triangles'] for c in chunks)
report={'version':'v0.0.43','source_sha256':source_hash,'zones':len(zones),'source_objects':len(objects),'mesh_files':len(chunks),'evaluated_triangles':sum(c['triangles'] for c in chunks),'textures':len(materials['textures']),'materials':len(materials['materials']),'native_shader_rebuild_count':sum(m['transfer_status']=='native_procedural_rebuild' for m in materials['materials']),'roundtrip_all_passed':True,'decimation_applied':False,'ue_runtime_tested':False,'shader_equivalence_claimed':False,'static_collision':'Roles supplied; collision must be assigned and tested in UE. Foliage/water excluded from intended blocking geometry.','lightmap_uv':'UV0 only; dynamic-lighting handoff. Static lightmap unwrap is not supplied.'}
(OUT/'package_manifest.json').write_text(json.dumps(report,indent=2),encoding='utf8')
readme=R/'docs/UE导入准备_v043.md';assert readme.exists();(OUT/'README.md').write_bytes(readme.read_bytes())
target=D/'ue/WZMS_UE_Transfer_v043.zip';target.parent.mkdir(exist_ok=True)
required=[OUT/'materials.json',OUT/'scene_reference.json',OUT/'package_manifest.json',OUT/'README.md']+[OUT/f'{kind}_{z}.json' for z in a.zones for kind in ['zone','roundtrip']]+[OUT/c['file'] for c in chunks]+[OUT/im['file'] for im in materials['textures']]
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as archive:
    for file in required:archive.write(file,file.relative_to(OUT).as_posix())
with zipfile.ZipFile(target) as archive:assert archive.testzip() is None
report['archive']={'file':target.relative_to(R).as_posix(),'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'crc_verified':True}
(D/'ue_transfer_validation.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print('UE_TRANSFER_PACKAGE_COMPLETE',report['mesh_files'],report['archive']['bytes'],flush=True)
