"""Final saved-scene floor, body width and forward clearance checks.
Ray sampling is geometric evidence only; not a UE capsule/navmesh simulation.
"""
import json,math
from pathlib import Path
import bpy
from mathutils import Vector
scene=bpy.data.scenes['WZMS_Campus'];bpy.context.window.scene=scene
bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get()
routes={
 'south gate to north public street':[(0,3),(0,47),(54,47),(54,76),(54,134),(54,205),(54,290),(54,348),(54,360),(54,398)],
 'main avenue to canteen west exterior landing':[(54,348),(103,348),(103,374),(110.1,374)],
 'main avenue to open canteen south entrance':[(54,348),(115,348),(115,346.5),(125,346.5),(125,351.2)]}
reports=[];fail=[]
for name,waypoints in routes.items():
    samples=[]
    for a,b in zip(waypoints,waypoints[1:]):
        a,b=Vector(a),Vector(b);length=(b-a).length;count=math.ceil(length/.25)
        for i in range(count):samples.append((a.lerp(b,i/count),(b-a).normalized()))
    samples.append((Vector(waypoints[-1]),samples[-1][1]))
    floor=0;maxstep=0
    for sample_index,(pos,d) in enumerate(samples):
        if sample_index%400==0:print('WZMS_CONTINUOUS_SAMPLE '+name+' '+str(sample_index)+'/'+str(len(samples)),flush=True)
        hit,loc,normal,idx,obj,matrix=scene.ray_cast(deps,Vector((pos.x,pos.y,floor+1.4)),Vector((0,0,-1)),distance=4)
        if not hit:fail.append({'route':name,'xy':list(pos),'issue':'missing floor'});continue
        step=abs(loc.z-floor);maxstep=max(maxstep,step);floor=loc.z
        if step>.20:fail.append({'route':name,'xy':list(pos),'issue':'step over 20 cm','height':step,'object':obj.name})
        clear=scene.ray_cast(deps,loc+Vector((0,0,.06)),Vector((0,0,1)),distance=1.70)
        if clear[0]:fail.append({'route':name,'xy':list(pos),'issue':'head clearance','object':clear[4].name})
        # Cast both lateral half-widths and a short forward distance at torso/head heights.
        for z in [.40,.95,1.55]:
            origin=loc+Vector((0,0,z))
            for direction,distance in [(Vector((-d.y,d.x,0)),.35),(Vector((d.y,-d.x,0)),.35),(Vector((d.x,d.y,0)),.25)]:
                h=scene.ray_cast(deps,origin,direction,distance=distance)
                if h[0]:fail.append({'route':name,'xy':list(pos),'issue':'body clearance','z_above_floor':z,'object':h[4].name})
    reports.append({'route':name,'waypoints':waypoints,'samples':len(samples),'maximum_floor_step_m':maxstep,'body_width_m':.70,'headroom_m':1.70})
    print('WZMS_CONTINUOUS_ROUTE_CHECKED '+name,flush=True)
out=Path(__file__).resolve().parents[2]/'deliverables'/scene['delivery_version']/'integrated_route_validation.json'
out.write_text(json.dumps({'opened_saved_blend':bpy.data.filepath,'routes':reports,'failures':fail,'passed':not fail,'scope':'sampled evaluated surfaces and ray clearance; not UE collision/navigation'},ensure_ascii=False,indent=2),encoding='utf8')
print('WZMS_INTEGRATED_ROUTE '+json.dumps({'passed':not fail,'failure_count':len(fail),'examples':fail[:12]},ensure_ascii=False),flush=True)
if fail:raise RuntimeError('Integrated route has geometric obstructions')
