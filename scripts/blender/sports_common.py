"""Reference-led west gate and sports components; editable, estimated metres."""
import math, random
from mathutils import Vector
import campus_common as c, north_common as n, north_landscape as l
import south_detail_common as s, island_common as h

def arch_x(name,x,y,spring,radius,depth,thick,mat,a0=0,a1=math.pi,steps=48):
    v=[]
    for i in range(steps+1):
        a=a0+(a1-a0)*i/steps
        for xx,r in [(x-depth/2,radius),(x-depth/2,radius+thick),(x+depth/2,radius),(x+depth/2,radius+thick)]:
            v.append((xx,y+r*math.cos(a),spring+r*math.sin(a)))
    f=[(0,2,3,1),(steps*4,steps*4+1,steps*4+3,steps*4+2)]
    for i in range(steps):
        a=i*4;b=a+4;f.extend([(a,b,b+1,a+1),(a+2,a+3,b+3,b+2),(a,a+2,b+2,b),(a+1,b+1,b+3,a+3)])
    return c.mesh(name,v,f,mat)

def arched_bay(name,x,y,r,spring,top,depth,pier,mat):
    for sign in [-1,1]:
        c.box(name+' masonry jamb',(x,y+sign*(r+pier/2),spring/2),(depth,pier,spring),mat)
    arch_x(name+' deep vault',x,y,spring,r,depth,.28,mat)
    v=[]
    for i in range(49):
        yy=-r-pier+(r+pier)*2*i/48
        bottom=spring+math.sqrt(max(0,(r+.28)**2-yy*yy)) if abs(yy)<r+.28 else spring
        for xx,z in [(x-depth/2,bottom),(x-depth/2,top),(x+depth/2,bottom),(x+depth/2,top)]:v.append((xx,y+yy,z))
    f=[]
    for i in range(48):
        a=i*4;b=a+4;f.extend([(a,b,b+1,a+1),(a+2,a+3,b+3,b+2),(a+1,b+1,b+3,a+3)])
    c.mesh(name+' brick spandrel',v,f,mat)

def radial_bricks(name,x,y,z,r,width,mat,full=False):
    count=60 if full else 36
    for i in range(count):
        a=i*(math.tau if full else math.pi)/count+.006
        b=(i+1)*(math.tau if full else math.pi)/count-.006
        arch_x(name+' individual voussoir',x,y,z,r,.12,width,mat,a,b,2)

def clipped_pine(name,x,y):
    rng=random.Random(350);v,f,lv,lf,ids=[],[],[],[],[]
    bark=c.material('West gate pine bark',(.15,.12,.085),.9)
    c.tube_data(v,f,(x,y,.25),(x+.2,y,6.6),.27,.045,14)
    for j in range(17):
        z=.9+j*.30;az=j*2.399;reach=(3.8-z*.43)*rng.uniform(.65,1)
        tip=Vector((x+reach*math.cos(az),y+reach*math.sin(az),z+.5))
        c.tube_data(v,f,(x,y,z),tip,.10,.025,10)
        for k in range(1800):
            a=rng.random()*math.tau;r=rng.random()**.5
            q=tip+Vector((math.cos(a)*r*.85,math.sin(a)*r*.65,rng.uniform(-.16,.24)))
            c.leaf_data(lv,lf,ids,q,.15,rng,rng.randrange(5))
    c.mesh(name+' layered branch structure',v,f,bark)
    c.mesh(name+' clipped needle clusters',lv,lf,c.foliage_materials('West gate pine needles ',True),ids)

def flat_line(name,points,width,mat,z=.055):
    return s.ribbon(name,points,width,mat,z,.008,miter=True)

def flat_arc(name,x,y,r,a0,a1,mat,z=.055,width=.05,steps=100):
    v=[]
    for i in range(steps+1):
        a=a0+(a1-a0)*i/steps
        for rr in [r-width/2,r+width/2]:v.append((x+rr*math.cos(a),y+rr*math.sin(a),z))
    return c.mesh(name,v,[(2*i,2*i+1,2*i+3,2*i+2) for i in range(steps)],mat)
