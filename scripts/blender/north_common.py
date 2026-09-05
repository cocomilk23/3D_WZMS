"""Shared physical details for the northward campus deliveries.

Local dimensions are estimates from the archived panoramas, not survey data.
"""
import math, random
import bpy
from mathutils import Vector
import campus_common as c

def palette():
    return dict(stone=c.material('North light granite',(.64,.65,.61),.79),
      white=c.material('North ivory frames',(.78,.80,.76),.4,.12),
      seam=c.material('North stone seams',(.30,.32,.30),.88),
      dark=c.material('North dark recess',(.028,.043,.042),.62),
      steel=c.material('North brushed metal',(.43,.48,.47),.31,.78),
      glass=c.material('North blue green glazing',(.075,.23,.23),.18,.32),
      green=c.material('North planted ground',(.095,.15,.026),.95))

def paving(name,color=(.50,.51,.46),brick=(.55,.28),mortar=.008):
    m=c.material(name,color,.84)
    if len(m.node_tree.nodes)>2:return m
    n,l=m.node_tree.nodes,m.node_tree.links
    p=next(n for n in n if n.type=='BSDF_PRINCIPLED')
    co=n.new('ShaderNodeTexCoord');b=n.new('ShaderNodeTexBrick')
    b.inputs['Scale'].default_value=1;b.inputs['Brick Width'].default_value=brick[0]
    b.inputs['Row Height'].default_value=brick[1];b.inputs['Mortar Size'].default_value=mortar
    b.inputs['Color1'].default_value=(*color,1)
    b.inputs['Color2'].default_value=(*(q*.78 for q in color),1)
    b.inputs['Mortar'].default_value=(.30,.31,.27,1)
    l.new(co.outputs['Object'],b.inputs['Vector']);l.new(b.outputs['Color'],p.inputs['Base Color'])
    bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.22;bump.inputs['Distance'].default_value=.012
    l.new(b.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs['Normal'],p.inputs['Normal'])
    return m

def window(x,y,z,w=3.6,h=2.25,out=-1,ac=False):
    p=palette()
    c.box('Window recessed opening',(x,y,z),(w+.10,.14,h+.10),p['dark'])
    c.box('Glazed window',(x,y+out*.082,z),(w,.024,h),p['glass'])
    for dx in [-w/2,-w/4,0,w/4,w/2]:
        c.box('Window vertical sash',(x+dx,y+out*.115,z),(.05,.09,h+.06),p['white'])
    for dz in [-h/2,h*.23,h/2]:c.box('Window horizontal sash',(x,y+out*.12,z+dz),(w+.08,.1,.055),p['white'])
    c.box('Projecting window sill',(x,y+out*.18,z-h/2-.07),(w+.26,.34,.12),p['stone'])
    if ac:
        xx=x+w*.29;zz=z-h/2-.46
        c.box('AC outdoor enclosure',(xx,y+out*.35,zz),(.85,.45,.55),p['white'],.028)
        c.rod('AC dark fan grille',(xx+.17,y+out*.59,zz),(xx+.17,y+out*.607,zz),.20,p['dark'],sides=24)
        for k in range(6):c.box('AC condenser grille',(xx-.24,y+out*.602,zz-.19+k*.075),(.26,.018,.014),p['seam'])
        c.rod('AC service pipe',(xx-.43,y,zz+.4),(xx-.43,y,zz-.45),.017,p['white'])

def railing(a,b,z,height=1.05):
    p=palette();a,b=Vector((*a,z)),Vector((*b,z));n=max(1,math.ceil((b-a).length/1.4))
    for t in [.17,.46,.73,height]:c.rod('Balcony horizontal rail',a+Vector((0,0,t)),b+Vector((0,0,t)),.024,p['steel'],sides=6)
    for i in range(n+1):
        q=a.lerp(b,i/n);c.rod('Balcony upright',q,q+Vector((0,0,height)),.026,p['white'],sides=6)

def academic_wing(name,x,y,width=33,depth=12,floors=6,out=-1,open_corridor=True,open_pilotis=False):
    p=palette();bay=width/7
    for level in range(floors):
        z=level*3.65
        c.box(name+' structural slab',(x,y,z-.14),(width,depth,.26),p['stone'])
        for k in range(8):
            xx=x-width/2+k*bay
            c.box(name+' column',(xx,y+out*(depth/2-.3),z+1.73),(.36,.48,3.5),p['white'])
        fy=y+out*(depth/2-2.35 if open_corridor else depth/2)
        for k in range(7):
            xx=x-width/2+(k+.5)*bay
            if not (open_pilotis and level==0):
                c.box(name+' classroom spandrel',(xx,fy,z+.56),(bay,.22,1.1),p['stone'])
            c.box(name+' classroom lintel',(xx,fy,z+3.36),(bay,.24,.52),p['stone'])
            c.box(name+' window side pier',(xx-bay/2,fy,z+2.02),(.30,.24,2.15),p['white'])
            if not (open_pilotis and level==0):
                window(xx,fy+out*.14,z+2.1,bay-.45,1.93,out,ac=not open_corridor and level>0)
        if open_corridor and level>0:
            c.box(name+' corridor low parapet',(x,y+out*(depth/2-.12),z+.22),(width,.20,.42),p['white'])
            railing((x-width/2,y+out*(depth/2-.13)),(x+width/2,y+out*(depth/2-.13)),z+.23,.88)
        # Rear window wall and hollow rooms rather than a solid monolithic block.
        ry=y-out*depth/2
        c.box(name+' rear lower wall',(x,ry,z+.55),(width,.24,1.1),p['stone'])
        c.box(name+' rear upper wall',(x,ry,z+3.36),(width,.24,.52),p['stone'])
        for k in range(7):
            xx=x-width/2+(k+.5)*bay
            window(xx,ry-out*.14,z+2.1,bay-.5,1.93,-out,ac=level>0)
            c.box(name+' classroom partition',(xx-bay/2,y,z+1.73),(.18,depth-2.8,3.45),p['stone'])
        for xx in [x-width/2,x+width/2]:c.box(name+' end wall',(xx,y,z+1.73),(.26,depth,3.48),p['stone'])
        c.box(name+' front floor fascia',(x,y+out*(depth/2+.12),z-.12),(width+.3,.4,.3),p['white'])
    z=floors*3.65
    c.box(name+' roof',(x,y,z),(width+.5,depth+.6,.26),p['stone'])
    for yy in [y-depth/2,y+depth/2]:
        c.box(name+' roof parapet',(x,yy,z+.43),(width,.22,.7),p['white'])
    if open_corridor:
        yy=y+out*(depth/2-.85)
        c.box(name+' pergola beam',(x,yy,z+1.0),(width+.8,.25,.22),p['white'])
        for k in range(int(width/.5)):
            c.box(name+' pergola tooth',(x-width/2+k*.5,yy,z+.78),(.09,2.4,.35),p['white'])
    c.box(name+' roof service room',(x-width*.25,y,z+1.05),(5,4,2.0),p['stone'])

def stone_joints(x,y,width,height,z0=0):
    p=palette()
    for j in range(int(height/.8)+1):c.box('Cladding horizontal seam',(x,y,z0+j*.8),(width,.008,.009),p['seam'])
    for i in range(1,int(width/.9)):
        c.box('Cladding vertical seam',(x-width/2+i*.9,y,z0+height/2),(.009,.008,height),p['seam'])

def broad_tree(name,x,y,h=9,radius=4,seed=1):
    """Branching broad canopy, leaves clustered on 3D twigs; deterministic mesh."""
    rng=random.Random(seed);v,f,lv,lf,mi=[],[],[],[],[]
    bark=c.material('North avenue bark',(.24,.235,.18),.92)
    if len(bark.node_tree.nodes)<4:c.noise(bark,20,.6,.035)
    c.tube_data(v,f,(0,0,0),(.12,.05,h*.65),.30,.055,10)
    for j in range(12):
        az=j*2.399+rng.uniform(-.35,.35);reach=radius*rng.uniform(.55,1)
        start=Vector((.1,0,h*rng.uniform(.26,.49)));end=Vector((math.cos(az)*reach,math.sin(az)*reach,h*rng.uniform(.61,.89)))
        c.tube_data(v,f,start,end,.14,.022,8)
        for k in range(12):
            a=az+rng.uniform(-1.5,1.5);base=start.lerp(end,rng.uniform(.5,1))
            tip=base+Vector((math.cos(a)*radius*.45,math.sin(a)*radius*.45,h*rng.uniform(.08,.20)))
            c.tube_data(v,f,base,tip,.025,.003,5)
            for n in range(250):
                pt=base.lerp(tip,rng.uniform(.38,1.12))+Vector((rng.gauss(0,.58),rng.gauss(0,.58),rng.gauss(0,.38)))
                c.leaf_data(lv,lf,mi,pt,rng.uniform(.18,.30),rng,rng.randrange(5))
    a=c.mesh(name+' scaffold branches',v,f,bark);a.location=(x,y,0)
    for face in a.data.polygons:face.use_smooth=True
    b=c.mesh(name+' canopy leaves',lv,lf,c.foliage_materials('Avenue leaf ',True),mi);b.location=(x,y,0)
    return [a,b]

def duplicate_tree(prototype,x,y,angle=0,scale=1):
    for orig in prototype:
        o=orig.copy();o.data=orig.data;c.COL.objects.link(o)
        o.location=(x,y,0);o.rotation_euler.z=angle;o.scale=(scale,scale,scale)

def disk(name,x,y,z,r,mat,segments=128,inner=0):
    v,f=[],[]
    for rr in [inner,r]:
        for i in range(segments):a=i*math.tau/segments;v.append((x+rr*math.cos(a),y+rr*math.sin(a),z))
    for i in range(segments):j=(i+1)%segments;f.append((i,j,segments+j,segments+i))
    return c.mesh(name,v,f,mat)

def palm(name,x,y,h=7,seed=1):
    rng=random.Random(seed);v,f,lv,lf,mi=[],[],[],[],[]
    bark=c.material('Palm fibrous bark',(.29,.24,.16),.94)
    c.tube_data(v,f,(x,y,0),(x+.12,y,h),.20,.12,12)
    for j in range(30):
        z=j*h/30;c.tube_data(v,f,(x,y,z),(x,y,z+.035),.205-j*.0025,.205-j*.0025,10)
    for j in range(24):
        az=j*2.399;reach=rng.uniform(2.4,3.7);drop=rng.uniform(.6,2.0)
        last=Vector((x+.12,y,h))
        for k in range(1,21):
            t=k/20;q=Vector((x+.12+math.cos(az)*reach*t,y+math.sin(az)*reach*t,h+1.3*math.sin(math.pi*t)-drop*t))
            c.tube_data(v,f,last,q,.025*(1-t)+.005,.005,5)
            for side in [-1,1]:
                width=.62*math.sin(math.pi*t)**.5
                tip=q+Vector((-math.sin(az)*side*width,math.cos(az)*side*width,-width*.7))
                st=len(lv);lv.extend([q,last,tip]);lf.append((st,st+1,st+2));mi.append(j%5)
            last=q
    c.mesh(name+' ringed trunk and stems',v,f,bark)
    c.mesh(name+' arching pinnate fronds',lv,lf,c.foliage_materials('Palm foliage '),mi)
