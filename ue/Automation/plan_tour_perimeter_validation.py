"""Boundary crossing fixtures sampled along the entire playable envelope."""
import json,sys,math
from pathlib import Path
sys.path.insert(0,'E:/WZMS_UE_Cache/Python')
import shapely
from shapely.geometry import shape,Point
root=Path(__file__).resolve().parents[1];p=json.loads((root/'SourceReference/tour_perimeter_plan.json').read_text());boundary=shape(p['playable_boundary']);samples=[]
for ring in shapely.get_parts(boundary.boundary):
 coords=list(ring.coords)
 for a,b in zip(coords,coords[1:]):
  dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy)
  if length<.001:continue
  nx,ny=-dy/length,dx/length
  for i in range(max(1,math.ceil(length/3))):
   t=(i+.5)/max(1,math.ceil(length/3));x,y=a[0]+dx*t,a[1]+dy*t
   if not boundary.contains(Point(x+nx,y+ny)):nx,ny=-nx,-ny
   samples.append({'inside':[x+nx*2,y+ny*2],'outside':[x-nx*2,y-ny*2]})
(root/'SourceReference/tour_perimeter_validation.json').write_text(json.dumps({'spacing_m':3,'samples':samples}),encoding='utf8');print('Boundary crossing samples',len(samples))
