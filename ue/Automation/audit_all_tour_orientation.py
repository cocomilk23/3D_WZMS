"""Audit all currently placed solid chunks in bounded read-only editor batches."""
import json
from pathlib import Path
from ue_mcp import UnrealMcpClient
from run_campus_zone import run_job
root=Path(__file__).resolve().parents[1];validation=json.loads((root/'Reports/campus_delivery_validation.json').read_text(encoding='utf8'));paths=['/Engine/BasicShapes/Cube']
for row in validation['meshes']:
 if '_solid_' not in row['mesh']:continue
 variant=row.get('tour_geometry_variant');paths.append(variant['replacement'] if variant else '/Game/WZMS/'+row['zone'].title()+'/Meshes/'+row['mesh'])
client=UnrealMcpClient();client.connect();all_rows=[]
try:
 for i in range(0,len(paths),4):
  (root/'WZMS/Saved/Logs/orientation_request.json').write_text(json.dumps(paths[i:i+4]),encoding='utf8');run_job(client,'export_tour_orientation_audit.py')
  all_rows.extend(json.loads((root/'WZMS/Saved/OrientationAudit/meshes.json').read_text(encoding='utf8')));print('Audited',len(all_rows),'of',len(paths),'meshes',flush=True)
 (root/'WZMS/Saved/OrientationAudit/meshes.json').write_text(json.dumps(all_rows,indent=2),encoding='utf8')
finally:client.close()
