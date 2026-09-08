"""Small deterministic UE mesh-buffer helpers using source metre coordinates."""
import math
import shapely

def buffer():return {'vertices':[],'triangles':[],'normals':[],'uv0':[]}
def quad(b,points,normal):
 i=len(b['vertices']);b['vertices'].extend([[x*100,-y*100,z*100] for x,y,z in points]);b['normals'].extend([[normal[0],-normal[1],normal[2]]]*4);b['uv0'].extend([[0,0],[1,0],[1,1],[0,1]]);b['triangles'].extend([[i,i+1,i+2],[i,i+2,i+3]])
def box_mesh(b,centre,size,yaw=0):
 x,y,z=centre;w,d,h=[q/2 for q in size];c,s=math.cos(yaw),math.sin(yaw)
 local=[[-w,-d,-h],[w,-d,-h],[w,d,-h],[-w,d,-h],[-w,-d,h],[w,-d,h],[w,d,h],[-w,d,h]];v=[[x+c*a-s*e,y+s*a+c*e,z+k] for a,e,k in local]
 for ids,n in [([0,3,2,1],[0,0,-1]),([4,5,6,7],[0,0,1]),([0,1,5,4],[0,-1,0]),([3,7,6,2],[0,1,0]),([0,4,7,3],[-1,0,0]),([1,2,6,5],[1,0,0])]:quad(b,[v[j] for j in ids],[c*n[0]-s*n[1],s*n[0]+c*n[1],n[2]])
def flat(b,geo,z):
 for poly in shapely.get_parts(geo):
  if poly.geom_type!='Polygon' or poly.area<1e-8:continue
  for tri in shapely.get_parts(shapely.constrained_delaunay_triangles(poly)):
   points=list(tri.exterior.coords)[:3];a,e,k=points
   if (e[0]-a[0])*(k[1]-a[1])-(e[1]-a[1])*(k[0]-a[0])<0:points[1],points[2]=points[2],points[1]
   i=len(b['vertices']);b['vertices'].extend([[x*100,-y*100,z*100] for x,y in points]);b['normals'].extend([[0,0,1]]*3);b['uv0'].extend([[x/4,y/4] for x,y in points]);b['triangles'].append([i,i+1,i+2])
