"""Capture the actual UE viewport through MCP, with no image alteration."""
import base64,json,sys
from pathlib import Path
from ue_mcp import UnrealMcpClient
client=UnrealMcpClient();client.connect()
try:
    call={'toolset_name':'SlateInspectorToolset.SlateInspectorToolset','tool_name':'Screenshot','arguments':{'ref':sys.argv[2]}} if len(sys.argv)>2 else {'toolset_name':'EditorToolset.EditorAppToolset','tool_name':'CaptureViewport','arguments':{'captureTransform':None,'annotations':None,'bShowUI':False}}
    result=client.rpc('tools/call',{'name':'call_tool','arguments':call})
    if result.get('isError'):raise RuntimeError(str(result))
    def find(obj):
        if isinstance(obj,dict):
            if isinstance(obj.get('data'),str) and (obj.get('mimeType','').startswith('image/') or obj.get('type')=='image'):return obj['data']
            for value in obj.values():
                data=find(value)
                if data:return data
        elif isinstance(obj,list):
            for value in obj:
                data=find(value)
                if data:return data
        elif isinstance(obj,str) and obj.startswith(('{','[')):
            try:return find(json.loads(obj))
            except json.JSONDecodeError:pass
    data=find(result)
    if not data:raise RuntimeError('No screenshot returned: '+str(result)[:500])
    out=Path(sys.argv[1]);out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(base64.b64decode(data));print(out)
finally:client.close()
