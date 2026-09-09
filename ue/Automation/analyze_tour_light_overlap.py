"""Offline influence-volume audit for the 128 documented source lights; no asset edits."""
import collections,hashlib,json,math,pathlib

ue=pathlib.Path(__file__).resolve().parents[1]
inputs={name:ue/'Reports'/name for name in ['campus_interior_lighting.json','tour_interior_lighting.json','tour_performance.json']}
baseline=json.loads(inputs['campus_interior_lighting.json'].read_text(encoding='utf8'))
additional=json.loads(inputs['tour_interior_lighting.json'].read_text(encoding='utf8'))
performance=json.loads(inputs['tour_performance.json'].read_text(encoding='utf8'))
lights=baseline['lights']
assert len(lights)==baseline['source_local_lights']
source=json.loads(pathlib.Path('E:/3D_WZMS/builds/v043_ue_bundle/scene_reference.json').read_text(encoding='utf8'))
source_by_name={x['name']:x for x in source['lights']}

def distance(a,b):return math.dist(a,b)
def summary(values):
 values=sorted(values)
 return {'min':values[0],'median':values[len(values)//2],'p95':values[math.ceil(len(values)*.95)-1],'max':values[-1]}

areas=[]
for area in sorted({x['source_name'].split()[0] for x in lights}):
 rows=[x for x in lights if x['source_name'].split()[0]==area]
 types=collections.Counter(source_by_name[x['source_name']]['type'] for x in rows)
 pairs=sum(distance(a['position_cm'],b['position_cm'])<a['radius_cm']+b['radius_cm'] for i,a in enumerate(rows) for b in rows[i+1:])
 areas.append({'area':area,'source_light_count':len(rows),'blender_source_types':dict(types),'radius_m':summary([r['radius_cm']/100 for r in rows]),'intersecting_sphere_pairs':pairs,'all_pairs':len(rows)*(len(rows)-1)//2})

# Sample horizontal planes inside the documented building bounds, every 2 metres.
# Floor slabs, light direction, cones, walls, and visibility are deliberately NOT inferred.
planes=[]
for area,height_m in [('Library',1.6),('Library',5.8),('Gym',2.6),('Gym',10.6),('Canteen',2.6)]:
 bounds=next(x['bounds_blender_m'] for x in baseline['bounded_volumes'] if x['name']==area)
 lo,hi=bounds;points=[];counts=[]
 for x in range(math.ceil(lo[0]),math.floor(hi[0])+1,2):
  for y in range(math.ceil(lo[1]),math.floor(hi[1])+1,2):
   p=(x*100,-y*100,height_m*100)
   count=sum(distance(p,l['position_cm'])<l['radius_cm'] for l in lights)
   points.append(p);counts.append(count)
 planes.append({'area':area,'height_blender_m':height_m,'samples':len(points),'sphere_overlap_count':summary(counts),'max_overlap_point_ue_cm':points[counts.index(max(counts))]})

missing=[x['actor'] for x in additional.get('additional_upper_library_lights',[])+additional.get('library_upper_indirect_fill',[])]
report={
 'method':'Offline sphere intersection and 2m grid sampling using authored source-light records; no runtime frame or image claims.',
 'input_sha256':{name:hashlib.sha256(path.read_bytes()).hexdigest() for name,path in inputs.items()},
 'source_light_count':len(lights),'areas':areas,'sample_planes':planes,
 'documented_additional_lights_outside_baseline':missing,
 'previous_clearance_inspector_omitted_prefixes':['Tour_InteriorLight_','Tour_InteriorBounce_'],
 'inspector_scope_fixed_but_not_rerun':True,
 'existing_measured_views':[{'view':v['view'],'average_fps':v['average_fps'],'gpu_ms':v['timings']['GPUTime']['mean']} for v in performance['views']],
 'limitations':['Sphere overlap is only potential influence, not rendered light count or GPU cost.','No occlusion, rect-light hemisphere, spot cone, floor-slab visibility, or shadow-cache reuse is simulated.','Extra lights are explicitly listed, excluded from sphere totals; their current active state needs a fresh editor inventory.','No new performance result, visual improvement, or standalone acceptance is claimed.'],
 'next_measurement':'Fresh editor session after user testing: inventory every authored local light, profile GPU passes at the same library/gym viewpoints, then compare isolated runtime-only lighting/shadow diagnostics with baseline before considering saved changes.'
}
out=ue/'Reports/tour_light_overlap_audit_053.json';out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'areas':areas,'planes':planes,'extra_lights_to_recheck':len(missing)},ensure_ascii=False,indent=2))
