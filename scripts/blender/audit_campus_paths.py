"""Check actual evaluated surfaces along delivery routes, independent of names.

This verifies geometric floor continuity and 1.7 m headroom, not UE collision.
"""
import sys,json,math
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
scene=bpy.data.scenes['WZMS_Campus'];bpy.context.window.scene=scene
bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get()
version=scene['delivery_version'];routes=[]
routes.append(('plaza central walk',[(0,y) for y in range(3,49)]))
routes.append(('plaza left cross access',[(-x,25) for x in range(12)]))
routes.append(('plaza right cross access',[(x,25) for x in range(12)]))
if version in ['v0.0.5','v0.0.6']:
    routes.append(('portal stairs and passage',[(0,48+i*.2) for i in range(100)]))
if version=='v0.0.6':
    routes.append(('Zhongshan facade walk',[(x,47) for x in range(0,55)]))
    routes.append(('Zhongshan east turn',[(54,y) for y in range(47,77)]))
    routes.append(('Zhongshan bridge',[(54,76+i*.5) for i in range(101)]))
fail=[];reports=[]
for name,points in routes:
    heights=[];hits=[]
    for x,y in points:
        hit,loc,norm,idx,obj,matrix=scene.ray_cast(deps,Vector((x,y,1.4)),Vector((0,0,-1)),distance=4)
        if not hit:
            fail.append({'route':name,'xy':[x,y],'issue':'no walking surface'});continue
        heights.append(loc.z);hits.append(obj.name)
        up=scene.ray_cast(deps,Vector((x,y,loc.z+.05)),Vector((0,0,1)),distance=1.70)
        if up[0]:fail.append({'route':name,'xy':[x,y],'issue':'headroom obstruction','object':up[4].name})
    steps=[abs(b-a) for a,b in zip(heights,heights[1:])]
    if steps and max(steps)>.20:fail.append({'route':name,'issue':'floor discontinuity > 20 cm','maximum_m':max(steps)})
    reports.append({'route':name,'samples':len(points),'hits':len(heights),'min_z':min(heights,default=None),'max_z':max(heights,default=None),'largest_step_m':max(steps,default=0)})
out=ROOT/'deliverables'/version/'geometry_validation.json';out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps({'opened_saved_blend':bpy.data.filepath,'routes':reports,'failures':fail,'scope':'evaluated geometry; not UE navigation/collision','passed':not fail},ensure_ascii=False,indent=2),encoding='utf8')
print('WZMS_GEOMETRY_AUDIT '+json.dumps({'passed':not fail,'failures':fail},ensure_ascii=False),flush=True)
if fail:raise RuntimeError('Walking geometry failed')
