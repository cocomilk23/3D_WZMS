"""Editable components for the library and east cultural precinct; estimated metres."""
import bpy,math,random
from mathutils import Vector
import campus_common as c
import north_common as n
import south_detail_common as s

def arc(name,cx,cy,r,z,mat,a0=0,a1=math.tau,width=.025,steps=96):
 v,f=[],[]
 for i in range(steps):
  a=a0+(a1-a0)*i/steps;b=a0+(a1-a0)*(i+1)/steps
  c.tube_data(v,f,(cx+r*math.cos(a),cy+r*math.sin(a),z),(cx+r*math.cos(b),cy+r*math.sin(b),z),width,width,8)
 return c.mesh(name,v,f,mat)

def rail(name,points,wood=False):
 p=n.palette();top=c.material('Library honey oak handrail',(.34,.18,.066),.4) if wood else p['steel']
 for a,b in zip(points,points[1:]):
  a,b=Vector(a),Vector(b)
  for h in [.22,.43,.64,.85,1.08]:c.rod(name+' horizontal rail',a+Vector((0,0,h)),b+Vector((0,0,h)),.027 if h==1.08 else .012,top if h==1.08 else p['steel'],sides=10)
  steps=max(1,math.ceil((b-a).length/1.2))
  for j in range(steps):
   q=a.lerp(b,j/steps);c.rod(name+' upright',q,q+Vector((0,0,1.08)),.025,p['steel'],sides=10)

def stairs(name,a,b,width,count,mat,rails=True):
 a,b=Vector(a),Vector(b);delta=b-a;tangent=Vector((delta.x,delta.y,0)).normalized();normal=Vector((-tangent.y,tangent.x,0))
 for i in range(count):
  q=a+delta*(i+.5)/count;top=a.z+delta.z*(i+1)/count;depth=Vector((delta.x,delta.y)).length/count
  o=c.box(name+' tread',(q.x,q.y,(top+a.z-.18)/2),(depth+.007,width,top-a.z+.18),mat);o.rotation_euler.z=math.atan2(delta.y,delta.x)
  edge=Vector((q.x,q.y,top+.003))-tangent*(depth*.5-.025)
  c.rod(name+' anti slip nosing',edge+normal*(width/2-.03),edge-normal*(width/2-.03),.009,n.palette()['dark'],sides=6)
 if rails:
  for sign in [-1,1]:rail(name+' side railing',[a+normal*sign*(width/2-.04),b+normal*sign*(width/2-.04)],True)

def area(name,loc,energy,size=5,color=(1,.89,.72),target=None):
 d=bpy.data.lights.new(name,'AREA');d.energy=energy;d.shape='DISK';d.size=size;d.color=color
 o=bpy.data.objects.new(name,d);c.COL.objects.link(o);o.location=loc
 if target:o.rotation_euler=(Vector(target)-Vector(loc)).to_track_quat('-Z','Y').to_euler()
 return o

def pot(x,y,z=0,scale=1,flower=False,seed=0):
 rng=random.Random(seed);ceramic=c.material('Library blue white ceramic',(.63,.70,.71),.22)
 blue=c.material('Library porcelain cobalt',(.026,.073,.22),.25);soil=n.palette()['dark']
 c.rod('Blue white planter',(x,y,z),(x,y,z+.52*scale),.22*scale,ceramic,.34*scale,24)
 arc('Porcelain blue rim',x,y,.33*scale,z+.5*scale,blue,width=.019*scale,steps=32)
 c.rod('Planter soil',(x,y,z+.48*scale),(x,y,z+.5*scale),.3*scale,soil,sides=24)
 v,f,mi=[],[],[];mats=c.foliage_materials('Cultural glossy leaf ')
 if flower:mats=[c.material('Cultural bougainvillea magenta',(.49,.014,.16),.65),c.material('Cultural bougainvillea pink',(.74,.045,.36),.65)]
 for i in range(220):
  a=rng.random()*math.tau;r=rng.random()**.5*.55*scale;h=z+scale*(.9+rng.uniform(-.25,.65))
  c.leaf_data(v,f,mi,(x+math.cos(a)*r,y+math.sin(a)*r,h),rng.uniform(.10,.22)*scale,rng,rng.randrange(len(mats)))
 c.mesh('Potted foliage or flowers',v,f,mats,mi)
 c.rod('Potted plant stem',(x,y,z+.45*scale),(x,y,z+1.2*scale),.02*scale,n.palette()['seam'],sides=8)

def ring_floor(name,z,material,west_open=False):
 """Rectangular shell minus atrium, with a wider opening for the visible upper stairs."""
 v,f=[],[];cx,cy=130,155;steps=160
 for i in range(steps+1):
  a=i*math.tau/steps;dx,dy=math.cos(a),math.sin(a)
  reach=min((142-cx)/dx if dx>1e-7 else (115-cx)/dx if dx< -1e-7 else 1e6,(172-cy)/dy if dy>1e-7 else (138-cy)/dy if dy< -1e-7 else 1e6)
  inner=8.0 if west_open and math.pi*.48<a<math.pi*1.52 else 6.0
  for r,h in [(inner,z),(reach,z),(inner,z-.26),(reach,z-.26)]:v.append((cx+dx*r,cy+dy*r,h))
 for i in range(steps):
  a=i*4;b=a+4;f.extend([(a,b,b+1,a+1),(a+2,a+3,b+3,b+2),(a,a+2,b+2,b),(a+1,b+1,b+3,a+3)])
 return c.mesh(name,v,f,material)
