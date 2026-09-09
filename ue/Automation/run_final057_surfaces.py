"""Resumable bounded geometry repairs with explicit per-mesh completion records."""
import json,psutil,time
from pathlib import Path
from ue_mcp import UnrealMcpClient
from run_campus_zone import run_job,restart_editor,editor_process
ue=Path(__file__).resolve().parents[1];rows=json.loads((ue/'SourceReference/final057_surface_patch.json').read_text());report=ue/'Reports/final057_surface_applied.json'
done={x['name'] for x in json.loads(report.read_text())['meshes']} if report.exists() else set()
deadline=time.monotonic()+240
while True:
 client=UnrealMcpClient()
 try:client.connect();break
 except OSError:
  if time.monotonic()>deadline:raise
  time.sleep(3)
try:
 run_job(client,'open_transfer_map.py')
 for row in rows:
  if row['name'] in done:continue
  private=editor_process().memory_info().private/2**30
  if private>11:client=restart_editor(client,'/Game/WZMS/Maps/L_WZMS_Transfer')
  (ue/'WZMS/Saved/Logs/final057_mesh_request.json').write_text(json.dumps({'name':row['name']}))
  print('START',row['name'],'editor GiB',round(private,2),flush=True);run_job(client,'apply_final057_surface.py');done.add(row['name']);print('DONE',len(done),'/',len(rows),flush=True)
finally:client.close()
