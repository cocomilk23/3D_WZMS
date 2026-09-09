"""Finish interrupted regression, then render longer stationary checks without overlapping PIE jobs."""
import json,time,subprocess,sys,psutil
from pathlib import Path
from ue_mcp import UnrealMcpClient
from run_campus_zone import run_job
ue=Path(__file__).resolve().parents[1]
deadline=time.time()+1800
while time.time()<deadline:
 running=[]
 for p in psutil.process_iter(['cmdline']):
  try:
   args=p.info['cmdline'] or []
   if any(x.endswith('run_final057_acceptance.py') for x in args) and '--resume' in args:running.append(p.pid)
  except (psutil.NoSuchProcess,psutil.AccessDenied):pass
 if not running:break
 time.sleep(2)
else:raise TimeoutError('Original regression still running')
r=json.loads((ue/'Reports/final057_routes_resumed.json').read_text());assert r['complete'] and not r.get('error')
subprocess.run([sys.executable,str(ue/'Automation/run_final057_acceptance.py'),'--details-only' if '--details-only' in sys.argv else '--retry-routes'],check=True)
c=UnrealMcpClient();c.connect()
try:
 c.call_meta('call_tool',{'toolset_name':'EditorToolset.EditorAppToolset','tool_name':'StopPIE','arguments':{}})
 req={'plan':'final057_hold_shots.json','prefix':'LS_Final057_Hold','revision':'r01','report':'final057_hold_sequences.json','source':'Campus 0.1.0-final.57 after geometry and goal collision corrections; stationary camera review.'}
 (ue/'WZMS/Saved/Logs/demo_build_request.json').write_text(json.dumps(req));run_job(c,'build_demo_sequence.py')
 seq=json.loads((ue/'Reports/final057_hold_sequences.json').read_text())['final']['sequence']
 req={'name':'Final057 extended stationary QA','sequence':seq,'directory':'E:/WZMS_Media/final057/hold-default','resolution':[1280,720],'samples':1,'report':'final057_hold_render.json'}
 (ue/'WZMS/Saved/Logs/demo_render_request.json').write_text(json.dumps(req));run_job(c,'render_demo_sequence.py')
 deadline=time.time()+1200
 while time.time()<deadline:
  r=json.loads((ue/'Reports/final057_hold_render.json').read_text())
  if r.get('complete'):assert r.get('success') and not r['errors'];break
  time.sleep(2)
 else:raise TimeoutError('Stationary render')
 print('REGRESSION AND EXTENDED STATIONARY RENDER COMPLETE',flush=True)
finally:c.close()
