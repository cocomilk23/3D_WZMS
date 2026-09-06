"""Editable southern landscape components; positions are panorama-based estimates."""
import bpy, math, random
from mathutils import Vector
import campus_common as c
import north_common as n

def daylight(scene):
 """Use a physical clear sky in a new world, retaining inherited sun geometry."""
 world=bpy.data.worlds.new('Southern campus physical daylight');world.use_nodes=True
 nd,ln=world.node_tree.nodes,world.node_tree.links;nd.clear()
 sky=nd.new('ShaderNodeTexSky');sky.sky_type='MULTIPLE_SCATTERING';sky.sun_disc=False
 sky.sun_elevation=math.radians(42);sky.sun_rotation=math.radians(145)
 sky.altitude=20;sky.air_density=1;sky.aerosol_density=1.5;sky.ozone_density=1
 bg=nd.new('ShaderNodeBackground');bg.inputs['Strength'].default_value=.25
 out=nd.new('ShaderNodeOutputWorld');ln.new(sky.outputs[0],bg.inputs['Color']);ln.new(bg.outputs[0],out.inputs[0])
 scene.world=world

def beam(name,a,b,width,depth,mat):
 a,b=Vector(a),Vector(b)
 o=c.box(name,(a+b)/2,(width,depth,(b-a).length),mat)
 o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler()
 return o

def segment(name,a,b,width,mat,top=-.01,thickness=.22):
 a,b=Vector(a),Vector(b);d=b-a
 o=c.box(name,((a.x+b.x)/2,(a.y+b.y)/2,top-thickness/2),(d.length,width,thickness),mat)
 o.rotation_euler.z=math.atan2(d.y,d.x)
 return o

def ribbon(name,points,width,mat,z=-.01,thickness=.2):
 pts=[Vector(p) for p in points];v=[]
 for i,p in enumerate(pts):
  direction=pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]
  normal=Vector((-direction.y,direction.x)).normalized()*width/2
  zz=z(p) if callable(z) else z
  v.extend([(p.x-normal.x,p.y-normal.y,zz),(p.x+normal.x,p.y+normal.y,zz),
            (p.x-normal.x,p.y-normal.y,zz-thickness),(p.x+normal.x,p.y+normal.y,zz-thickness)])
 f=[]
 for i in range(len(pts)-1):
  a=i*4;b=a+4;f.extend([(a,a+1,b+1,b),(a+2,b+2,b+3,a+3),(a,b,b+2,a+2),(a+1,a+3,b+3,b+1)])
 k=(len(pts)-1)*4;f.extend([(0,2,3,1),(k,k+1,k+3,k+2)])
 return c.mesh(name,v,f,mat)

def smooth_path(points,steps=12):
 p=[Vector(q) for q in points];result=[]
 for i in range(len(p)-1):
  a,b,d,e=p[max(0,i-1)],p[i],p[i+1],p[min(i+2,len(p)-1)]
  for j in range(steps):
   t=j/steps;q=.5*((2*b)+(-a+d)*t+(2*a-5*b+4*d-e)*t*t+(-a+3*b-3*d+e)*t*t*t)
   result.append(tuple(q))
 return result+[tuple(p[-1])]

def offset(points,distance):
 out=[]
 for i,p in enumerate(points):
  p=Vector(p);a=Vector(points[max(0,i-1)]);b=Vector(points[min(len(points)-1,i+1)])
  t=(b-a).normalized();out.append(tuple(p+Vector((-t.y,t.x))*distance))
 return out

def wire_fence(name,a,b,height=4.0,mat=None,pitch=.11,z=0):
 mat=mat or c.material('Tennis cyan enamel',(.018,.31,.57),.38,.35)
 a,b=Vector(a),Vector(b);direction=(b-a).normalized();length=(b-a).length
 def pt(t,h):q=a+direction*t;return(q.x,q.y,z+h)
 for i in range(math.ceil(length/2.8)+1):
  t=min(length,i*2.8);beam(name+' square upright',pt(t,0),pt(t,height),.10,.10,mat)
 for h in [.045,height/2,height]:beam(name+' horizontal frame',pt(0,h),pt(length,h),.052,.06,mat)
 # One batched mesh per run keeps the editable diamond wires inexpensive.
 v,f=[],[];wire=c.material('Tennis silver diamond wire',(.32,.40,.41),.40,.65)
 for sign in [-1,1]:
  for i in range(math.ceil((length+height)/pitch)+1):
   start=-height+i*pitch
   lo=max(0,-start) if sign==1 else max(0,start+height-length)
   hi=min(height,length-start) if sign==1 else min(height,start+height)
   if hi<=lo:continue
   t0=start+lo if sign==1 else start+height-lo
   t1=start+hi if sign==1 else start+height-hi
   c.tube_data(v,f,pt(t0,lo),pt(t1,hi),.0035,.0035,4)
 c.mesh(name+' diamond mesh',v,f,wire)

def tree(x,y,scale=1,angle=0):
 proto=[bpy.data.objects['Middle mature avenue tree scaffold branches'],bpy.data.objects['Middle mature avenue tree canopy leaves']]
 n.duplicate_tree(proto,x,y,angle,scale)

def slit_lamp(x,y):
 black=c.material('Southern black anodised fittings',(.018,.026,.030),.42,.5)
 diffuser=c.material('Southern warm lamp diffuser',(.74,.74,.59),.42)
 for dx in [-.08,.08]:c.box('Slit lamp tall side',(x+dx,y,1.45),(.038,.10,2.9),black)
 c.box('Slit lamp foot',(x,y,.06),(.24,.20,.12),black)
 c.box('Slit lamp cap',(x,y,2.85),(.20,.13,.24),black)
 c.box('Slit lamp frosted strip',(x,y+.018,1.65),(.032,.035,1.85),diffuser)

def glass_rail(a,b,z=0,name='Waterside bridge'):
 a,b=Vector(a),Vector(b);length=(b-a).length;d=(b-a).normalized();count=max(1,math.ceil(length/1.6))
 steel=c.material('Waterside grey powder coated railing',(.20,.25,.27),.36,.5)
 glass=c.material('Waterside clear laminated glass',(.72,.87,.81),.09)
 bs=glass.node_tree.nodes.get('Principled BSDF');bs.inputs['Transmission Weight'].default_value=1;bs.inputs['IOR'].default_value=1.45
 def pt(t,h):p=a+d*t;return(p.x,p.y,z+h)
 c.rod(name+' rounded top rail',pt(0,1.08),pt(length,1.08),.042,steel,sides=12)
 c.rod(name+' bottom tie',pt(0,.13),pt(length,.13),.018,steel,sides=8)
 for j in range(count+1):beam(name+' upright',pt(j*length/count,.02),pt(j*length/count,1.08),.045,.055,steel)
 for j in range(count):
  lo=j*length/count+.075;hi=(j+1)*length/count-.075
  panel=segment(name+' clear glass panel',a+d*lo,a+d*hi,.014,glass,z+.96,.77)
  for t in [lo+.045,hi-.045]:
   for h in [.24,.89]:
    pos=Vector(pt(t,h));normal=Vector((-d.y,d.x,0))
    c.rod(name+' glass clamp bolt',pos-normal*.019,pos+normal*.019,.019,steel,sides=10)

def bridge(name,points,width=2.4,top=-.01):
 stone=n.paving('Waterside fine rectangular granite',(.59,.60,.54),(.6,.30),.004)
 ribbon(name+' walkable continuous deck',points,width,stone,top,.30)
 for side in [-1,1]:
  edge=offset(points,side*(width/2-.09))
  for a,b in zip(edge,edge[1:]):glass_rail(a,b,top,name)
  inner=offset(points,side*(width/2-.23))
  ribbon(name+' recessed drainage',inner,.105,c.material('Waterside drain recess',(.027,.034,.031)),top+.001,.01)
  for a,b in zip(inner,inner[1:]):
   a,b=Vector(a),Vector(b);d=(b-a).normalized();norm=Vector((-d.y,d.x))
   for j in range(int((b-a).length/.12)):
    q=a+d*(j*.12);segment(name+' drain grate',q-norm*.055,q+norm*.055,.015,n.palette()['steel'],top+.008,.008)
 for a,b in zip(points,points[1:]):
  a,b=Vector(a),Vector(b)
  for j in range(1,max(2,math.ceil((b-a).length/7))):
   q=a.lerp(b,j/max(2,math.ceil((b-a).length/7)))
   c.box(name+' concrete pier',(q.x,q.y,-.75),(width*.70,.45,1.0),n.palette()['stone'])

def mottled(name,colors,scale=2,rough=.86):
 m=c.material(name,colors[0],rough)
 if len(m.node_tree.nodes)>2:return m
 nd,ln=m.node_tree.nodes,m.node_tree.links;p=nd.get('Principled BSDF')
 tex=nd.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=scale
 tex.inputs['Detail'].default_value=4
 co=nd.new('ShaderNodeTexCoord');ln.new(co.outputs['Object'],tex.inputs['Vector'])
 ramp=nd.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(*colors[0],1);ramp.color_ramp.elements[1].color=(*colors[1],1)
 ln.new(tex.outputs['Fac'],ramp.inputs[0]);ln.new(ramp.outputs[0],p.inputs['Base Color']);c.noise(m,140,.2,.009)
 return m
