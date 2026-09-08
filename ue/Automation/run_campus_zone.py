"""Resumable one-chunk MCP jobs; never abandon or overlap a running editor mutation."""
import argparse,json,time
from pathlib import Path
from ue_mcp import UnrealMcpClient
root=Path(__file__).resolve().parents[1]

def run_job(client,script):
    result=client.call_meta('call_tool',{'toolset_name':'wzms_editor_bridge.WZMSProjectTools','tool_name':'run_script','arguments':{'script_name':script}})
    job=Path(result['returnValue']);started=time.monotonic()
    while time.monotonic()-started<1800:
        try:state=json.loads(job.read_text(encoding='utf8'))
        except (json.JSONDecodeError,FileNotFoundError):time.sleep(.2);continue
        if state['state']=='failed':raise RuntimeError(json.dumps(state))
        if state['state']=='complete':return state
        time.sleep(.5)
    raise TimeoutError(f'Job may still be running; inspect {job} before retrying')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('zone',choices=['central','west','east','north']);parser.add_argument('--limit',type=int);args=parser.parse_args()
    zone=json.loads(Path(f'E:/3D_WZMS/builds/v043_ue_bundle/zone_{args.zone}.json').read_text(encoding='utf8'))
    report=root/f'Reports/import_{args.zone}.json'
    done={r['name'] for r in json.loads(report.read_text())['chunks'] if r['verified']} if report.exists() else set()
    chunks=sorted(zone['chunks'],key=lambda c:({'solid':0,'glass':1,'water':2,'foliage':3}[c['role']],c['name']))
    pending=[c for c in chunks if c['name'] not in done]
    if args.limit:pending=pending[:args.limit]
    client=UnrealMcpClient();client.connect();started=time.monotonic()
    try:
        for i,ch in enumerate(pending,1):
            (root/'WZMS/Saved/Logs/campus_request.json').write_text(json.dumps({'zone':args.zone,'chunk':ch['name']}))
            t=time.monotonic();print(f'START {args.zone} {len(done)+i}/{len(chunks)} {ch["name"]}',flush=True)
            run_job(client,'import_campus_chunk.py')
            print(f'DONE {ch["name"]} {time.monotonic()-t:.1f}s; batch elapsed {time.monotonic()-started:.1f}s',flush=True)
    finally:client.close()
if __name__=='__main__':main()
