import argparse,json,time
from pathlib import Path
from ue_mcp import UnrealMcpClient
from run_campus_zone import run_job,restart_editor,editor_process
root=Path(__file__).resolve().parents[1];parser=argparse.ArgumentParser();parser.add_argument('--limit',type=int);args=parser.parse_args();paths=[]
for zone in ['south','central','west','east','north']:
    p=root/('Reports/south_import.json' if zone=='south' else f'Reports/import_{zone}.json');r=json.loads(p.read_text())
    paths.extend(f'/Game/WZMS/{zone.title()}/Meshes/'+c['name'] for c in r['chunks'] if c['role']=='foliage')
file=root/'Reports/campus_foliage_fallback.json';done={r['path'] for r in json.loads(file.read_text())['meshes']} if file.exists() else set();pending=[p for p in paths if p not in done]
if args.limit:pending=pending[:args.limit]
c=UnrealMcpClient();c.connect();c=restart_editor(c)
try:
    for i,path in enumerate(pending,1):
        if editor_process().memory_info().private/2**30>14:c=restart_editor(c)
        (root/'WZMS/Saved/Logs/fallback_request.json').write_text(json.dumps({'path':path}))
        t=time.monotonic();run_job(c,'compact_foliage_fallback.py');print(f'{len(done)+i}/{len(paths)} {path.rsplit("/",1)[-1]} {time.monotonic()-t:.1f}s',flush=True)
finally:c.close()
