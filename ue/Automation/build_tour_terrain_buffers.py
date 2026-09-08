"""Triangulate the reviewed land and water exclusions into small UE construction buffers."""
import sys,json,math
from pathlib import Path
sys.path.insert(0,'E:/WZMS_UE_Cache/Python')
import shapely
from shapely.geometry import shape,LineString
from shapely.ops import unary_union
root=Path(__file__).resolve().parents[1];plan=json.loads((root/'SourceReference/tour_terrain_plan.json').read_text(encoding='utf8'));land=shape(plan['terrain_skin']);water=shape(plan['blocked_water'])
def surfaces(geo,z,up=True):
 verts=[];tris=[];indices={};area=0
 for poly in shapely.get_parts(geo):
  if poly.geom_type!='Polygon' or poly.area<1e-6:continue
  for tri in shapely.get_parts(shapely.constrained_delaunay_triangles(poly)):
   if tri.area<1e-9:continue
   area+=tri.area;v=[[round(x*100,5),round(-y*100,5),round(z*100,5)] for x,y in list(tri.exterior.coords)[:3]]
   cross=(v[1][0]-v[0][0])*(v[2][1]-v[0][1])-(v[1][1]-v[0][1])*(v[2][0]-v[0][0])
   if (cross>0)!=up:v[1],v[2]=v[2],v[1]
   face=[]
   for p in v:
    key=tuple(p)
    if key not in indices:indices[key]=len(verts);verts.append(p)
    face.append(indices[key])
   tris.append(face)
 assert abs(area-geo.area)<max(.01,geo.area*1e-6),(area,geo.area)
 return {'vertices':verts,'triangles':tris,'normals':[[0,0,1 if up else -1]]*len(verts),'uv0':[[v[0]/400,v[1]/400] for v in verts]}
def sides(geo,lo,hi):
 verts=[];tris=[];normals=[]
 for p in shapely.get_parts(geo):
  if p.geom_type!='Polygon':continue
  for ring in [p.exterior,*p.interiors]:
   points=list(ring.coords)
   for a,b in zip(points,points[1:]):
    dx,dy=b[0]-a[0],-(b[1]-a[1]);length=math.hypot(dx,dy)
    if length<1e-8:continue
    n=[dy/length,-dx/length,0];i=len(verts)
    verts.extend([[a[0]*100,-a[1]*100,lo*100],[b[0]*100,-b[1]*100,lo*100],[b[0]*100,-b[1]*100,hi*100],[a[0]*100,-a[1]*100,hi*100]])
    tris.extend([[i,i+1,i+2],[i,i+2,i+3]]);normals.extend([n]*4)
 return {'vertices':verts,'triangles':tris,'normals':normals,'uv0':[[v[0]/400,v[2]/400] for v in verts]}
rows=[{'name':'SM_Tour_Continuous_Ground','visible':True,'materials':['Lawn soil green','Jiushan grey masonry water bank'],'buffers':[dict(surfaces(land,plan['ground_z_m']),material=0),dict(sides(land,-2,plan['ground_z_m']),material=1),dict(surfaces(land,-2,False),material=1)]},{'name':'SM_Tour_Water_Exclusion','visible':False,'materials':['Jiushan grey masonry water bank'],'buffers':[dict(surfaces(water,4.5),material=0),dict(sides(water,-5,4.5),material=0),dict(surfaces(water,-5,False),material=0)]}]
# UE raster front faces use clockwise winding; keep the authored outward normals.
for row in rows:
 for b in row['buffers']:
  b['triangles']=[[t[0],t[2],t[1]] for t in b['triangles']]
(root/'SourceReference/tour_terrain_buffers.json').write_text(json.dumps({'units':'UE centimetres','objects':rows}),encoding='utf8')
print([(r['name'],sum(len(b['triangles']) for b in r['buffers'])) for r in rows],flush=True)
