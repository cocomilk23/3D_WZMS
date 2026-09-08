"""Capture final UE review cameras sequentially through the project MCP bridge."""
import json,time
from pathlib import Path
from ue_mcp import UnrealMcpClient
root=Path(__file__).resolve().parents[1]
shots=[('Review_Gate_Exterior','South_Gate.png'),('Review_188_South_gate_registered_axis','South_Plaza.png'),('Review_187_Tennis_registered_school_view','South_Tennis.png'),('Review_186_South_registered_aerial','South_Aerial.png')]
client=UnrealMcpClient();client.connect()
try:
    for camera,filename in shots:
        out=root/'Reviews/South'/filename;start=time.time()
        (root/'WZMS/Saved/Logs/review_request.json').write_text(json.dumps({'camera':camera,'filename':filename}))
        result=client.call_meta('call_tool',{'toolset_name':'wzms_editor_bridge.WZMSProjectTools','tool_name':'run_script','arguments':{'script_name':'render_review_view.py'}})
        job=Path(result['returnValue'])
        while time.time()-start<60:
            try:status=json.loads(job.read_text())
            except json.JSONDecodeError:
                time.sleep(.2);continue
            if status['state']=='failed':raise RuntimeError(status['error'])
            if status['state']=='complete' and out.exists() and out.stat().st_mtime>start:
                from PIL import Image
                try:
                    with Image.open(out) as im:im.verify()
                    break
                except (OSError,SyntaxError):pass
            time.sleep(.5)
        else:raise TimeoutError(filename)
        print(filename,flush=True)
finally:client.close()
