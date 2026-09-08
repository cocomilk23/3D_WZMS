"""Place repeated source trees outside campus paths and neighbouring building plots."""
import json,sys,random
from pathlib import Path
sys.path.insert(0,'E:/WZMS_UE_Cache/Python')
import shapely
from shapely.geometry import shape,Point
root=Path(__file__).resolve().parents[1];plan=json.loads((root/'SourceReference/tour_perimeter_plan.json').read_text());terrain=json.loads((root/'SourceReference/tour_terrain_plan.json').read_text());envelope=shape(terrain['envelope']);water=shape(plan['water_surface_footprint']);plots=shapely.union_all([shape(b['plot']) for b in plan['buildings']]);rng=random.Random(478);trees=[]
for offset,spacing in [(11.5,10),(38,12)]:
 line=envelope.buffer(offset).exterior
 for i in range(int(line.length/spacing)):
  p=line.interpolate((i+.5)*spacing)
  if water.distance(p)<4 or plots.distance(p)<4:continue
  trees.append({'xy_m':[p.x,p.y],'scale':rng.uniform(.75,1.05),'yaw_degrees':rng.uniform(0,360)})
(root/'SourceReference/tour_context_planting.json').write_text(json.dumps({'estimated_context':True,'trees':trees,'source_tree_reused':True,'no_gameplay_collision':True},indent=2),encoding='utf8');print('Context trees',len(trees))
