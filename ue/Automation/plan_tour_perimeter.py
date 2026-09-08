"""Derive an estimated surrounding district beyond the preserved main-campus footprint."""
import json,sys,random,math
from pathlib import Path
sys.path.insert(0,'E:/WZMS_UE_Cache/Python')
from shapely.geometry import shape,Polygon,Point,box,mapping
from shapely.ops import unary_union
root=Path(__file__).resolve().parents[1];p=json.loads((root/'SourceReference/tour_terrain_plan.json').read_text(encoding='utf8'));source=json.loads((root/'SourceReference/terrain_source.json').read_text(encoding='utf8'));envelope=shape(p['envelope']);lake=unary_union([Polygon(v['xy']) for v in source['water_surfaces']]);rng=random.Random(19020909)
world=box(-900,-800,1100,1300);context_ground=world.difference(lake);boundary=envelope.buffer(8,join_style='mitre');wall=boundary.boundary.difference(lake.buffer(.8));roads=envelope.buffer(29,join_style='round').difference(envelope.buffer(15,join_style='round'));pavement=envelope.buffer(33).difference(envelope.buffer(29));roads=roads.difference(lake.buffer(1));pavement=pavement.difference(lake.buffer(1));buildings=[]
for x in range(-420,681,80):
 for y in range(-310,781,80):
  cx=x+rng.uniform(-10,10);cy=y+rng.uniform(-10,10);w=rng.uniform(18,28);d=rng.uniform(24,40);plot=box(cx-w/2-8,cy-d/2-8,cx+w/2+8,cy+d/2+8)
  distance=plot.distance(envelope)
  if not 48<distance<190 or plot.distance(lake)<12:continue
  floors=rng.randint(5,10) if distance<85 else rng.randint(10,21)
  buildings.append({'id':len(buildings),'centre_m':[cx,cy],'size_m':[w,d,floors*3.05],'floors':floors,'facade_style':rng.randrange(3),'plot':mapping(plot),'source_status':'Estimated surrounding context; not a surveyed neighbouring building.'})
result={'units':'Blender metres; UE (X,-Y,Z)*100','scope':'Estimated surrounding roads, perimeter wall, planting and distant residential blocks. Main-campus buildings stay in their accepted positions.','context_ground':mapping(context_ground),'context_ground_top_m':-.075,'water_surface_footprint':mapping(lake),'visible_wall_lines':mapping(wall),'wall_height_m':2.4,'playable_boundary':mapping(boundary),'ring_road':mapping(roads),'outer_sidewalk':mapping(pavement),'buildings':buildings,'source_routes_inside_boundary':True}
for route in json.loads((root/'SourceReference/tour_traversal_cases.json').read_text(encoding='utf8'))['cases']:
 for pt in route['points']:assert boundary.contains(Point(pt[:2])),(route['name'],pt)
(root/'SourceReference/tour_perimeter_plan.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print('Context buildings',len(buildings),'perimeter metres',round(boundary.length),'wall metres',round(wall.length),'all authored route points within boundary')
