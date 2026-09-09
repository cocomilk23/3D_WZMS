"""Run the packaged executable offscreen without taking the owner's foreground window."""
import json,time,subprocess,psutil
from pathlib import Path
ue=Path(__file__).resolve().parents[1];build=Path('E:/WZMS_ValidationBuilds/0.1.0-final.57')
assert json.loads((build/'build-process.json').read_text())['state']=='complete'
user=Path('E:/WZMS_UE_Cache/Final057Smoke');user.mkdir(exist_ok=True)
cmd=[str(build/'Windows/WZMS.exe'),'-RenderOffscreen','-unattended','-nosound','-windowed','-ResX=1280','-ResY=720','-UserDir='+str(user),'-AbsLog='+str(user/'launch.log')]
rows=[];seen={};start=time.time()
with (user/'stdout.log').open('w',encoding='utf8') as log:
 launcher=subprocess.Popen(cmd,cwd=build/'Windows',stdout=log,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
 try:
  while time.time()-start<45:
   current=[]
   for p in psutil.process_iter(['exe','name']):
    try:
     if p.info['exe'] and Path(p.info['exe']).is_relative_to(build/'Windows'):
      seen[p.pid]=p;mem=p.memory_info();cpu=p.cpu_times();current.append({'pid':p.pid,'name':p.info['name'],'private_bytes':getattr(mem,'private',mem.rss),'cpu_seconds':cpu.user+cpu.system})
    except (psutil.NoSuchProcess,psutil.AccessDenied):pass
   rows.append({'elapsed_seconds':round(time.time()-start,2),'processes':current})
   if time.time()-start>15 and not current:break
   time.sleep(1)
  game=[p for p in rows[-1]['processes'] if 'shipping' in p['name'].lower()]
  passed=time.time()-start>=44 and bool(game) and game[0]['private_bytes']>100_000_000
  report={'process_smoke_passed':passed,'complete':True,'duration_seconds':round(time.time()-start,2),'command':cmd,'samples':rows,'visual_menu_clicks_verified':False,'scope':'Standalone Shipping bootstrap and process survival with actual RHI/offscreen rendering. This is not visual/menu-click acceptance or a long-duration GPU stability guarantee.','reference':'https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-command-line-arguments-reference','termination':'Only this isolated smoke-test process is terminated after sampling; user save folder is separate.'}
  (build/'standalone-smoke.json').write_text(json.dumps(report,indent=2));(ue/'Reports/final057_standalone_smoke.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='samples'},indent=2),flush=True)
  assert passed,'Inspect the isolated smoke-test logs before delivery.'
 finally:
  for p in reversed(list(seen.values())):
   try:
    if p.is_running() and Path(p.exe()).is_relative_to(build/'Windows'):p.terminate()
   except (psutil.NoSuchProcess,psutil.AccessDenied):pass
