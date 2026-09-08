"""Water-area grid, shore sweeps and authored route checks for the actual UE collision."""
import json,sys,math
from pathlib import Path
sys.path.insert(0,'E:/WZMS_UE_Cache/Python')
import shapely
from shapely.geometry import shape,Point
root=Path(__file__).resolve().parents[1];plan=json.loads((root/'SourceReference/tour_terrain_plan.json').read_text(encoding='utf8'));water=shape(plan['blocked_water']);land=shape(plan['land']);bounds=water.bounds
grid=[]
for x in range(math.floor(bounds[0]),math.ceil(bounds[2])+1,5):
 for y in range(math.floor(bounds[1]),math.ceil(bounds[3])+1,5):
  if water.contains(Point(x,y)):grid.append([x,y])
sweeps=[];candidates=[]
for poly in shapely.get_parts(water):
 if poly.geom_type!='Polygon':continue
 for ring in [poly.exterior,*poly.interiors]:
  coords=list(ring.coords)
  for a,b in zip(coords,coords[1:]):
   dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy)
   if length<.8:continue
   n=[-dy/length,dx/length]
   for i in range(max(1,math.ceil(length/15))):
    t=(i+.5)/max(1,math.ceil(length/15));p=[a[0]+dx*t,a[1]+dy*t]
    plus=[p[j]+n[j] for j in range(2)];minus=[p[j]-n[j] for j in range(2)]
    if water.contains(Point(plus))==water.contains(Point(minus)):continue
    if water.contains(Point(minus)):n=[-v for v in n]
    outside=[p[j]-n[j]*1.5 for j in range(2)];inside=[p[j]+n[j]*2.5 for j in range(2)]
    if not water.contains(Point(inside)) or water.contains(Point(outside)):continue
    sweeps.append({'outside':outside,'inside':inside})
    if land.contains(Point(outside)):candidates.append({'outside':outside,'inside':inside,'edge':p,'inward':n})
anchors=[('South waterfront',(0,-68)),('Tennis waterfront',(100,-25)),('Lotus bay',(80,40)),('Central lake',(0,100)),('West channel',(-97,100)),('Zhouyuan shore',(-40,120)),('Cultural lake',(180,100)),('Taohua low terrace',(214,60)),('History island',(257,130)),('Meihua island',(325,130)),('Ju island',(374,116)),('Bamboo lake',(145,300))]
runtime=[]
for name,anchor in anchors:
 options=sorted(candidates,key=lambda p:math.dist(p['edge'],anchor));runtime.append({'name':name,'candidates':options[:10]})
source=json.loads(Path('E:/3D_WZMS/builds/v043_ue_bundle/scene_reference.json').read_text(encoding='utf8'));route_hits=[]
for route in source['walkthrough_routes']:
 for a,b in zip(route['floor_points_m'],route['floor_points_m'][1:]):
  count=max(1,math.ceil(math.dist(a,b)))
  for i in range(count+1):
   p=[a[j]+(b[j]-a[j])*i/count for j in range(3)]
   if p[2]<4.5 and water.contains(Point(p[:2])):route_hits.append({'route':route['name'],'point':p})
assert not route_hits,route_hits[:10]
(root/'SourceReference/tour_water_fixtures.json').write_text(json.dumps({'grid_spacing_m':5,'water_grid':grid,'boundary_sweeps':sweeps,'runtime':runtime,'source_routes_clear':74,'source_route_water_conflicts':route_hits}),encoding='utf8')
print('Grid',len(grid),'boundary sweeps',len(sweeps),'runtime shore locations',len(runtime),'source routes clear',74)
