"""Check source route floor contacts against actual imported UE collision."""
import unreal,json,math
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve()
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world();assert world.get_name()=='L_WZMS_Campus'
source=json.loads(Path('E:/3D_WZMS/builds/v043_ue_bundle/scene_reference.json').read_text(encoding='utf8'))
rows=[]
for route in source['walkthrough_routes']:
    points=route['floor_points_m'];samples=[]
    for a,b in zip(points,points[1:]):
        steps=max(1,math.ceil(math.dist(a,b)/2))
        samples.extend([[a[j]+(b[j]-a[j])*t/steps for j in range(3)] for t in range(steps)])
    samples.append(points[-1]);missing=[]
    for p in samples:
        # Tight 0.6 m vertical interval excludes ceilings or an unrelated lower floor.
        start=unreal.Vector(p[0]*100,-p[1]*100,p[2]*100+30)
        end=unreal.Vector(p[0]*100,-p[1]*100,p[2]*100-30)
        hit=unreal.SystemLibrary.line_trace_single(world,start,end,unreal.TraceTypeQuery.ECC_VISIBILITY,True,[],unreal.DrawDebugTrace.NONE)
        if hit is None:missing.append(p)
    rows.append({'route':route['name'],'sample_count':len(samples),'missing_floor_samples_m':missing,'passed':not missing})
(root.parent/'Reports/campus_route_collision.json').write_text(json.dumps({'complete':True,'route_count':len(rows),'sample_count':sum(r['sample_count'] for r in rows),'passed':all(r['passed'] for r in rows),'routes':rows,'limits':'Floor contact test against visible complex collision, not a complete dynamic capsule traversal.'},indent=2))
