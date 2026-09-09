"""Author one non-overlapping basketball surface, faithful crest UVs, and regulation-sized goal frames."""
import sys,json,math
from pathlib import Path
sys.path.append('E:/WZMS_UE_Cache/Python')
import numpy as np
import shapely
from shapely.geometry import Point,Polygon,LineString,box
from shapely.ops import unary_union
import tour_mesh_buffers as b
ue=Path(__file__).resolve().parents[1];objects=[]
def obj(name,materials,buffers,collision=True,shadow=True):
 objects.append({'name':name,'materials':materials,'buffers':buffers,'collision':collision,'shadow':shadow})
def surface(g,mat,z=.06):
 x=b.buffer();b.flat(x,g,z);x['material']=mat;return x
foot=box(-16.7,211,45.7,319);reds=[];lines=[]
# Shared red pedestrian strips sit inside the existing generous run-off aisles.
for y in [235,261,287,313]:reds.append(box(-16.7,y-1.2,45.7,y+1.2))
reds.append(box(13.2,211,15.8,319))
def line(points):lines.append(LineString(points).buffer(.025,cap_style=2,join_style=2))
def arc(cx,cy,r,a0,a1):line([(cx+r*math.cos(a),cy+r*math.sin(a)) for a in np.linspace(a0,a1,max(16,int(abs(a1-a0)*32)))])
for cy in [222,248,274,300]:
 for cx in [-1,30]:
  # Old local long Y axis was rotated 90 degrees; retain actual court and hoop positions.
  start=len(lines);rstart=len(reds)
  line([(-7.5,-14),(7.5,-14),(7.5,14),(-7.5,14),(-7.5,-14)]);line([(-7.5,0),(7.5,0)])
  reds.append(Point(0,0).buffer(1.8,quad_segs=48));arc(0,0,1.8,0,math.tau)
  for sign in [-1,1]:
   reds.append(Polygon([(-3,sign*14),(3,sign*14),(1.8,sign*8.2),(-1.8,sign*8.2)]))
   line([(-3,sign*14),(-1.8,sign*8.2),(1.8,sign*8.2),(3,sign*14)])
   arc(0,sign*8.2,1.8,math.pi if sign==1 else 0,math.tau if sign==1 else math.pi)
   delta=math.acos(6.6/6.75);arc(0,sign*12.425,6.75,math.pi+delta if sign==1 else delta,math.tau-delta if sign==1 else math.pi-delta)
   join=sign*(12.425-math.sqrt(6.75**2-6.6**2))
   for x in [-6.6,6.6]:line([(x,sign*14),(x,join)])
   for j in range(4):
    w=1.8+1.2*(.8+j)/5.8
    for side in [-1,1]:line([(side*w,sign*(9+j)),(side*(w+.28),sign*(9+j))])
  for group,st in [(lines,start),(reds,rstart)]:
   for i in range(st,len(group)):group[i]=shapely.affinity.affine_transform(group[i],[0,-1,1,0,cx,cy])
white=unary_union(lines).intersection(foot);red=unary_union(reds).intersection(foot).difference(white);green=foot.difference(unary_union([red,white]))
assert abs(green.area+red.area+white.area-foot.area)<1e-5
assert max(green.intersection(red).area,green.intersection(white).area,red.intersection(white).area)<1e-6
obj('SM_Final057_Basketball_Surface',['Basketball weathered green acrylic','Basketball faded terracotta acrylic','Basketball warm white markings'],[surface(green,0),surface(red,1),surface(white,2)],True,False)
# Original image is retained unchanged. Circular mesh UVs use its complete circular emblem.
crest=b.buffer();n=256;crest['vertices']=[[5400,-15700,.5]];crest['normals']=[[0,0,1]];crest['uv0']=[[.5,.5]]
for a in np.linspace(0,math.tau,n,endpoint=False):
 x,y=math.cos(a),math.sin(a);crest['vertices'].append([(54+8.02*x)*100,-(157+8.02*y)*100,.5]);crest['normals'].append([0,0,1]);crest['uv0'].append([.5+.5*x,.5-.5*y])
crest['triangles']=[[0,i+1,(i+1)%n+1] for i in range(n)];crest['material']=0
obj('SM_Final057_Buqing_Crest',['Final057_Crest'],[crest],False,False)
def tube(buf,a,c,r,sides=12):
 a=np.array(a,float);c=np.array(c,float);axis=c-a;axis/=np.linalg.norm(axis);ref=np.array([0,0,1]) if abs(axis[2])<.9 else np.array([1,0,0]);u=np.cross(axis,ref);u/=np.linalg.norm(u);v=np.cross(axis,u)
 for i in range(sides):
  n1=math.cos(i*math.tau/sides)*u+math.sin(i*math.tau/sides)*v;n2=math.cos((i+1)*math.tau/sides)*u+math.sin((i+1)*math.tau/sides)*v
  normal=(n1+n2);normal/=np.linalg.norm(normal)
  b.quad(buf,[a+r*n1,c+r*n1,c+r*n2,a+r*n2],normal)
 # End caps, with explicit outward winding in source coordinates.
 for p,sgn in [(a,-1),(c,1)]:
  for i in range(sides):
   p1=p+r*(math.cos(i*math.tau/sides)*u+math.sin(i*math.tau/sides)*v);p2=p+r*(math.cos((i+1)*math.tau/sides)*u+math.sin((i+1)*math.tau/sides)*v)
   pts=[p,p1,p2] if sgn>0 else [p,p2,p1];st=len(buf['vertices']);buf['vertices'].extend([[float(x*100),float(-y*100),float(z*100)] for x,y,z in pts]);buf['normals'].extend([[float(axis[0]*sgn),float(-axis[1]*sgn),float(axis[2]*sgn)]]*3);buf['uv0'].extend([[0,0],[1,0],[0,1]]);buf['triangles'].append([st,st+1,st+2])
for sign,label in [(-1,'South'),(1,'North')]:
 cx,cy=-85,280+sign*52.5;frame=b.buffer();net=b.buffer()
 # Inner opening exactly 7.32 x 2.44m; 120mm diameter white posts.
 left,right=cx-3.72,cx+3.72;top=2.5
 for x in [left,right]:
  tube(frame,[x,cy,0],[x,cy,top],.06,20)
  tube(frame,[x,cy,.06],[x,cy+sign*2.4,.06],.035)
  tube(frame,[x,cy,top-.1],[x,cy+sign*.95,top-.1],.025)
  tube(frame,[x,cy+sign*.95,top-.1],[x,cy+sign*2.4,.06],.025)
  for yy in [cy+sign*.5,cy+sign*2.25]:b.box_mesh(frame,[x,yy,.018],[.25,.25,.036])
 tube(frame,[left,cy,top],[right,cy,top],.06,20);tube(frame,[left,cy+sign*2.4,.06],[right,cy+sign*2.4,.06],.035)
 # Real net cords; collision is deliberately confined to the solid frame.
 for x in np.linspace(left,right,63):
  tube(net,[x,cy,top-.08],[x,cy+sign*.95,top-.08],.003,4);tube(net,[x,cy+sign*.95,top-.08],[x,cy+sign*2.4,.08],.003,4)
 for z in np.linspace(.08,top-.08,21):
  depth=2.4-(z-.08)/(top-.16)*1.45;tube(net,[left,cy+sign*depth,z],[right,cy+sign*depth,z],.003,4)
  for x in [left,right]:tube(net,[x,cy,z],[x,cy+sign*depth,z],.003,4)
 for d in np.linspace(.12,2.35,20):
  zmax=min(top-.08,.08+(2.4-d)/1.45*(top-.16))
  for x in [left,right]:tube(net,[x,cy+sign*d,.08],[x,cy+sign*d,zmax],.003,4)
 for buf in [frame,net]:buf['material']=0
 obj('SM_Final057_Goal_'+label,['Final057_WhiteMetal'],[frame],True,True)
 obj('SM_Final057_GoalNet_'+label,['Basketball white cord net'],[net],False,False)
(ue/'SourceReference/final057_detail_buffers.json').write_text(json.dumps({'objects':objects},separators=(',',':'))+'\n',encoding='utf8')
(ue/'Reports/final057_detail_design.json').write_text(json.dumps({'basketball':{'courts':8,'grid':'4x2','centres':[[-1,222],[30,222],[-1,248],[30,248],[-1,274],[30,274],[-1,300],[30,300]],'court_size_m':[28,15],'orientation':'existing east-west long axis retained','red_cross_strips_m':2.4,'red_centre_aisle_m':2.6,'centre_circles_red':8,'surface_partition_overlap_m2':0,'existing_dimensions_estimated':True},'crest':{'centre_blender_m':[54,157],'diameter_m':16.04,'original_image_unchanged':True,'single_opaque_surface':True},'goals':{'count':2,'clear_opening_m':[7.32,2.44],'depth_m':2.4,'post_diameter_m':.12,'centres_blender_m':[[-85,227.5],[-85,332.5]],'spacing_m':105},'triangles':{x['name']:sum(len(bb['triangles']) for bb in x['buffers']) for x in objects}},indent=2)+'\n',encoding='utf8')
print('Prepared',len(objects),'detail objects')
