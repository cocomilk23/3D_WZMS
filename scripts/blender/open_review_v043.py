"""Opened with the v043 blend in interactive Blender after memory-heavy delivery work."""
import bpy,json,runpy
from pathlib import Path
R=Path(__file__).resolve().parents[2]
model=R/'models/campus/WZMS_Campus_v043.blend'
if Path(bpy.data.filepath)!=model:
    bpy.ops.wm.open_mainfile(filepath=str(model),load_ui=False)
sc=bpy.data.scenes['WZMS_Campus'];sc.camera=sc.objects['190_Environment_south_aerial']
for window in bpy.context.window_manager.windows:window.scene=sc
sc.cycles.samples=96
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':
            area.spaces.active.shading.type='SOLID';area.spaces.active.shading.color_type='MATERIAL'
            area.spaces.active.region_3d.view_perspective='CAMERA'
            area.spaces.active.region_3d.view_camera_zoom=0
            area.spaces.active.region_3d.view_camera_offset=(0,0)
addon=Path('D:/github项目/blender-mcp-main/addon.py')
if not hasattr(bpy.types.Scene,'blendermcp_port'):runpy.run_path(str(addon),run_name='__main__')
with bpy.context.temp_override(scene=sc):bpy.ops.blendermcp.start_server()
credential_count=sum(bool(scene.get(k)) for scene in bpy.data.scenes for k in scene.keys() if any(t in k.lower() for t in ['secret_id','secret_key','api_key','access_token']))
(R/'builds/v043_open_status.json').write_text(json.dumps({'file':bpy.data.filepath,'camera':sc.camera.name,'mcp_started':bool(getattr(getattr(bpy.types,'blendermcp_server',None),'running',False)),'nonempty_legacy_credential_field_count':credential_count,'ok':True}),encoding='utf8')
# UI state intentionally not written back to the frozen delivery model.
