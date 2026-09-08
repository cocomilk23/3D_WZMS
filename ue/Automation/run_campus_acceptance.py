"""Repeat actual pawn checks and three viewport profiles; stop PIE even on failure."""
import json,time,subprocess,sys
from pathlib import Path
from ue_mcp import UnrealMcpClient
from run_campus_zone import run_job
root=Path(__file__).resolve().parents[1]
c=UnrealMcpClient();c.connect()
def call(name,args=None):
    return c.call_meta('call_tool',{'toolset_name':'EditorToolset.EditorAppToolset','tool_name':name,'arguments':args or {}})
def completed(script,report,timeout):
    start=time.time();run_job(c,script);file=root/'Reports'/report
    while time.time()-start<timeout:
        try:
            data=json.loads(file.read_text())
            if file.stat().st_mtime>=start and data.get('complete'):
                assert not data.get('error'),data
                if 'passed' in data:assert data['passed'],data
                print('PASS',report,flush=True);return data
        except (json.JSONDecodeError,FileNotFoundError):pass
        time.sleep(1)
    raise TimeoutError(report)
try:
    print(call('StartPIE',{'options':{'bSimulate':False,'playMode':'PlayMode_InViewPort','startTransform':None,'warmupSeconds':2}}),flush=True)
    completed('test_campus_runtime.py','campus_runtime.json',150)
    completed('profile_campus_runtime.py','campus_profile_captures.json',150)
    subprocess.run([sys.executable,str(root/'Automation/capture_view.py'),str(root/'Reviews/Campus/Campus_Runtime_Window.png'),'w1'],check=True)
finally:
    try:call('StopPIE')
    finally:c.close()
