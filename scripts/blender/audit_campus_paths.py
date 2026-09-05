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
revision=int(version.rsplit('.',1)[1])
routes.append(('plaza central walk',[(0,y) for y in range(3,49)]))
routes.append(('plaza left cross access',[(-x,25) for x in range(12)]))
routes.append(('plaza right cross access',[(x,25) for x in range(12)]))
if revision>=5:
    routes.append(('portal stairs and passage',[(0,48+i*.2) for i in range(100)]))
if revision>=6:
    routes.append(('Zhongshan facade walk',[(x,47) for x in range(0,55)]))
    routes.append(('Zhongshan east turn',[(54,y) for y in range(47,77)]))
    routes.append(('Zhongshan bridge',[(54,76+i*.5) for i in range(101)]))
if revision>=7:
    routes.append(('Buqing bridge arrival and north passage',[(54,126+i*.5) for i in range(159)]))
    routes.append(('Buqing plaza transverse route',[(x,158) for x in range(0,107)]))
    routes.append(('Buqing library external stair',[(104,134.2+i*.1) for i in range(80)]))
if revision>=8:
    for x in [52,54,56]:
        routes.append(('Middle avenue lane x'+str(x),[(x,205+i*.5) for i in range(171)]))
    routes.append(('Middle Jiangkou crosswalk',[(54+i*.25,259) for i in range(117)]))
    routes.append(('Middle garden sidepath',[(83,209+i*.5) for i in range(163)]))
    routes.append(('Zhu Ziqing statue approach',[(59+i*.1,249) for i in range(31)]))
if revision>=9:
    for x in [52,54,56]:
        routes.append(('North avenue lane x'+str(x),[(x,290+i*.5) for i in range(141)]))
    for y in [294,348]:
        routes.append(('North lateral lane y'+str(y),[(54+i*.5,y) for i in range(107)]))
    routes.append(('North garden sidepath',[(83,290+i*.5) for i in range(141)]))
    routes.append(('North building entry stairs',[(83+i*.1,322) for i in range(75)]))
if revision>=10:
    routes.append(('Canteen branch connection',[(101+i*.1,348) for i in range(111)]))
    routes.append(('Canteen long forewalk',[(103,348+i*.25) for i in range(201)]))
    for y in [370,374]:
        routes.append(('Canteen west entry stairs y'+str(y),[(103+i*.1,y) for i in range(76)]))
    routes.append(('Canteen south stairs and open doorway',[(125,346.5+i*.1) for i in range(48)]))
fail=[];reports=[]
for name,points in routes:
    heights=[];hits=[];previous_floor=0.0
    for x,y in points:
        hit,loc,norm,idx,obj,matrix=scene.ray_cast(deps,Vector((x,y,previous_floor+1.4)),Vector((0,0,-1)),distance=4)
        if not hit:
            fail.append({'route':name,'xy':[x,y],'issue':'no walking surface'});continue
        heights.append(loc.z);hits.append(obj.name);previous_floor=loc.z
        up=scene.ray_cast(deps,Vector((x,y,loc.z+.05)),Vector((0,0,1)),distance=1.70)
        if up[0]:fail.append({'route':name,'xy':[x,y],'issue':'headroom obstruction','object':up[4].name})
    steps=[abs(b-a) for a,b in zip(heights,heights[1:])]
    if steps and max(steps)>.20:
        at=steps.index(max(steps))
        fail.append({'route':name,'issue':'floor discontinuity > 20 cm','maximum_m':max(steps),
          'from':{'xy':points[at],'z':heights[at],'object':hits[at]},'to':{'xy':points[at+1],'z':heights[at+1],'object':hits[at+1]}})
    reports.append({'route':name,'samples':len(points),'hits':len(heights),'min_z':min(heights,default=None),'max_z':max(heights,default=None),'largest_step_m':max(steps,default=0)})
    print('WZMS_ROUTE_CHECKED '+name,flush=True)
out=ROOT/'deliverables'/version/'geometry_validation.json';out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps({'opened_saved_blend':bpy.data.filepath,'routes':reports,'failures':fail,'scope':'evaluated geometry; not UE navigation/collision','passed':not fail},ensure_ascii=False,indent=2),encoding='utf8')
print('WZMS_GEOMETRY_AUDIT '+json.dumps({'passed':not fail,'failures':fail},ensure_ascii=False),flush=True)
if fail:raise RuntimeError('Walking geometry failed')
