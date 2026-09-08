"""Check saved south registration anchors independently of the builder's metadata."""
import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2]
rev=int(Path(bpy.data.filepath).stem.rsplit('_v',1)[1]);assert rev>=42
version=f'v0.0.{rev}'
sc=bpy.data.scenes['WZMS_Campus']
def midpoint(name):
 o=sc.objects[name];pts=[o.matrix_world@Vector(v) for v in o.bound_box]
 return [(min(v[i] for v in pts)+max(v[i] for v in pts))/2 for i in range(3)]
anchors={
 'school_foundation':(midpoint('Building plot foundation'),[0,59]),
 'island':(midpoint('Heyu closed island soil and revetment'),[92,15]),
 'utility_base':(midpoint('Reconnected Shuinan utility concrete base'),[105,-41]),
 'divider':(midpoint('v040 tennis horizontal solid divider'),[48.9,-31])}
for name,(actual,target) in anchors.items():
 assert max(abs(actual[i]-target[i]) for i in range(2))<.1,(name,actual,target)
wall=sc.objects['South name wall reverse photo surface']
assert max(abs(wall.matrix_world.translation[i]-[-26,-25,0][i]) for i in range(3))<1e-5
posts=[midpoint(o.name) for o in bpy.data.collections['03_Gates'].objects if o.name.startswith('Gate upright')]
right=[p for p in posts if p[0]>-17]
assert len(right)==18 and abs(min(p[0] for p in right)+12.4)<.01 and abs(max(p[0] for p in right)+10.8)<.01
assert 'Approach lotus water' not in sc.objects
assert 'v042 continuous lotus bay and east lake' in sc.objects
assert 'v042 three way open bridge landing' in sc.objects
def inside_polygon(q,points):
 hit=False;x,y=q
 for a,b in zip(points,points[1:]+points[:1]):
  if (a.y>y)!=(b.y>y) and x<(b.x-a.x)*(y-a.y)/(b.y-a.y)+a.x:hit=not hit
 return hit
water=sc.objects['v042 southern waterfront water']
water_poly=[water.matrix_world@v.co for v in water.data.vertices]
shore_samples=[(x,-68.05) for x in range(-90,85,5)]
assert all(inside_polygon(q,water_poly) for q in shore_samples),'Gap below south mainland shore'
roundabout=midpoint('Round forecourt kerb')
road=sc.objects['v042 south approach public road']
assert all((Vector((v.x,v.y))-Vector(roundabout[:2])).length>4.7 for v in (road.matrix_world@p.co for p in road.data.vertices)),'Road intersects forecourt island'
report={'version':version,'saved_file':bpy.data.filepath,'anchors':{k:{'measured_mesh_midpoint':a,'adopted_image_estimate_xy':t} for k,(a,t) in anchors.items()},'south_wall_rigid_translation':list(wall.matrix_world.translation),'right_gate_post_count':len(right),'right_gate_retracted_extent_x':[min(p[0] for p in right),max(p[0] for p in right)],'old_isolated_pond_absent':True,'connected_lotus_bay_present':True,'south_coast_water_samples':len(shore_samples),'road_clear_of_forecourt_island':True,'all_passed':True,'survey_accuracy_claimed':False}
(R/'deliverables'/version/'south_registration_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print('SOUTH_REGISTRATION_ANCHORS_VERIFIED',flush=True)
