"""Build estimated district geometry without altering the accepted campus mesh placements."""
import json,sys,math
from pathlib import Path
sys.path.insert(0,'E:/WZMS_UE_Cache/Python')
import shapely
from shapely.geometry import shape,LineString
from tour_mesh_buffers import buffer,box_mesh,flat,quad
root=Path(__file__).resolve().parents[1];plan=json.loads((root/'SourceReference/tour_perimeter_plan.json').read_text(encoding='utf8'));rows=[]
def mesh(name,mats,collision=False):
 row={'name':name,'materials':mats,'buffers':[buffer() for m in mats],'collision':collision};rows.append(row);return row['buffers']
b=mesh('SM_Tour_District_Ground',['Lawn soil green'])[0];flat(b,shape(plan['context_ground']),plan['context_ground_top_m'])
terrain=json.loads((root/'SourceReference/tour_terrain_plan.json').read_text(encoding='utf8'))
band=shape(plan['playable_boundary']).difference(shape(terrain['envelope']).buffer(-.1)).difference(shape(plan['water_surface_footprint']))
b=mesh('SM_Tour_Perimeter_Ground',['Lawn soil green'],True)[0];flat(b,band,-.065)
b=mesh('SM_Tour_District_Road',['North street weathered asphalt','North light granite','White painted metal']);flat(b[0],shape(plan['ring_road']),.015);flat(b[1],shape(plan['outer_sidewalk']),.10)
# Lane markings follow the ring centreline with broken intervals.
line=shape(plan['playable_boundary']).buffer(14).exterior
for i in range(int(line.length/10)):
 a=line.interpolate(i*10);e=line.interpolate(i*10+4)
 if not shape(plan['ring_road']).contains(LineString([a,e]).buffer(.08)):continue
 dx,dy=e.x-a.x,e.y-a.y;box_mesh(b[2],[(a.x+e.x)/2,(a.y+e.y)/2,.027],[math.hypot(dx,dy),.12,.016],math.atan2(dy,dx))
b=mesh('SM_Tour_Perimeter_Wall',['History warm white exterior plaster','Jiushan grey masonry water bank','North light granite'],True)
for line in shapely.get_parts(shape(plan['visible_wall_lines'])):
 points=list(line.coords)
 for a,e in zip(points,points[1:]):
  dx,dy=e[0]-a[0],e[1]-a[1];length=math.hypot(dx,dy)
  if length<.1:continue
  yaw=math.atan2(dy,dx);x,y=(a[0]+e[0])/2,(a[1]+e[1])/2
  box_mesh(b[0],[x,y,1.20],[length,.32,2.4],yaw);box_mesh(b[1],[x,y,.22],[length,.40,.44],yaw);box_mesh(b[2],[x,y,2.43],[length,.44,.10],yaw)
  for k in range(max(1,math.ceil(length/5))+1):
   t=k/max(1,math.ceil(length/5));box_mesh(b[0],[a[0]+dx*t,a[1]+dy*t,1.25],[.50,.50,2.5],yaw);box_mesh(b[2],[a[0]+dx*t,a[1]+dy*t,2.55],[.62,.62,.12],yaw)
for zone in ['West','East','North','South']:
 b=mesh('SM_Tour_District_'+zone,['Alumni warm white plaster','History dark grey metal roof','North ivory frames','North light granite'])
 for item in plan['buildings']:
  x,y=item['centre_m'];w,d,h=item['size_m'];region='West' if x<0 else 'East' if x>220 else 'North' if y>210 else 'South'
  if zone!=region:continue
  flat(b[3],shape(item['plot']),-.02);box_mesh(b[0],[x,y,h/2],[w,d,h]);box_mesh(b[1],[x,y,h+.06],[w+.16,d+.16,.12]);box_mesh(b[0],[x+w*.18,y-d*.15,h+1.4],[w*.35,d*.25,2.8])
  for level in range(item['floors']):
   z=level*3.05+1.5
   for sign in [-1,1]:
    yy=y+sign*(d/2+.025);nx=max(2,int(w/3.2))
    for j in range(nx):
     xx=x-w/2+(j+.5)*w/nx;pts=[[xx-.82,yy,z-.88],[xx+.82,yy,z-.88],[xx+.82,yy,z+.88],[xx-.82,yy,z+.88]]
     if sign>0:pts.reverse()
     quad(b[1],pts,[0,sign,0])
    xx=x+sign*(w/2+.025);ny=max(2,int(d/3.4))
    for j in range(ny):
     yy=y-d/2+(j+.5)*d/ny;pts=[[xx,yy-.72,z-.88],[xx,yy+.72,z-.88],[xx,yy+.72,z+.88],[xx,yy-.72,z+.88]]
     if sign<0:pts.reverse()
     quad(b[1],pts,[sign,0,0])
   if level%3==2 or item['facade_style']==1:
    for sign in [-1,1]:box_mesh(b[2],[x,y+sign*(d/2+.06),(level+1)*3.05-.06],[w+.12,.15,.14])
  for sign in [-1,1]:
   box_mesh(b[0],[x,y+sign*(d/2-.10),h+.45],[w,.20,.90]);box_mesh(b[0],[x+sign*(w/2-.10),y,h+.45],[.20,d,.90])
for row in rows:
 for i,b in enumerate(row['buffers']):b['material']=i
rowdata={'scope':plan['scope'],'context_is_estimated':True,'objects':rows};(root/'SourceReference/tour_perimeter_buffers.json').write_text(json.dumps(rowdata),encoding='utf8')
print([(r['name'],sum(len(b['triangles']) for b in r['buffers'])) for r in rows])
