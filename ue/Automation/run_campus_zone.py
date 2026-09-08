"""Resumable one-chunk MCP jobs; never abandon or overlap a running editor mutation."""
import argparse,json,time,subprocess,psutil
from pathlib import Path
from ue_mcp import UnrealMcpClient
root=Path(__file__).resolve().parents[1]

def editor_process():
    return psutil.Process(int((root/'WZMS/Saved/Logs/editor_pid.txt').read_text().strip()))

def restart_editor(client,map_path='/Game/WZMS/Maps/L_WZMS_Transfer'):
    proc=editor_process();print(f'CHECKPOINT restarting owned editor {proc.pid} to release build memory',flush=True)
    try:run_job(client,'close_saved_editor.py')
    except (OSError,RuntimeError):
        if proc.is_running():raise
    proc.wait(timeout=120)
    try:client.close()
    except OSError:pass
    subprocess.Popen(['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',str(root/'Automation/Start-WZMS.ps1'),'-WaitForExit','-Map',map_path],creationflags=subprocess.CREATE_NO_WINDOW)
    deadline=time.monotonic()+300
    while time.monotonic()<deadline:
        time.sleep(3)
        fresh=UnrealMcpClient()
        try:fresh.connect();return fresh
        except OSError:pass
    raise TimeoutError('Editor restart did not expose MCP within five minutes')

def run_job(client,script):
    result=client.call_meta('call_tool',{'toolset_name':'wzms_editor_bridge.WZMSProjectTools','tool_name':'run_script','arguments':{'script_name':script}})
    job=Path(result['returnValue']);started=time.monotonic();last_probe=started
    while time.monotonic()-started<1800:
        try:state=json.loads(job.read_text(encoding='utf8'))
        except (json.JSONDecodeError,FileNotFoundError):time.sleep(.2);continue
        if state['state']=='failed':raise RuntimeError(json.dumps(state))
        if state['state']=='complete':return state
        if time.monotonic()-last_probe>10:
            if not editor_process().is_running():raise RuntimeError(f'Editor stopped during {job}; inspect logs before resuming')
            last_probe=time.monotonic()
        time.sleep(.5)
    raise TimeoutError(f'Job may still be running; inspect {job} before retrying')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('zone',choices=['central','west','east','north']);parser.add_argument('--limit',type=int);parser.add_argument('--fresh',action='store_true');args=parser.parse_args()
    zone=json.loads(Path(f'E:/3D_WZMS/builds/v043_ue_bundle/zone_{args.zone}.json').read_text(encoding='utf8'))
    report=root/f'Reports/import_{args.zone}.json'
    done={r['name'] for r in json.loads(report.read_text())['chunks'] if r['verified']} if report.exists() else set()
    chunks=sorted(zone['chunks'],key=lambda c:({'solid':0,'glass':1,'water':2,'foliage':3}[c['role']],c['name']))
    pending=[c for c in chunks if c['name'] not in done]
    if args.limit:pending=pending[:args.limit]
    client=UnrealMcpClient();client.connect();started=time.monotonic()
    if args.fresh:client=restart_editor(client)
    try:
        for i,ch in enumerate(pending,1):
            mem=editor_process().memory_info().private/2**30
            if mem>14:client=restart_editor(client)
            (root/'WZMS/Saved/Logs/campus_request.json').write_text(json.dumps({'zone':args.zone,'chunk':ch['name']}))
            t=time.monotonic();print(f'START {args.zone} {len(done)+i}/{len(chunks)} {ch["name"]}',flush=True)
            run_job(client,'import_campus_chunk.py')
            print(f'DONE {ch["name"]} {time.monotonic()-t:.1f}s; batch elapsed {time.monotonic()-started:.1f}s; private {editor_process().memory_info().private/2**30:.1f} GiB',flush=True)
    finally:client.close()
if __name__=='__main__':main()
