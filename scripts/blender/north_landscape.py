"""Road furniture, vegetation and sculptural reference approximations."""
import math,random
from mathutils import Vector
import campus_common as c
import north_common as n

def ellipsoid(name,loc,radii,mat,segments=24,rings=12):
    v,f=[],[]
    for j in range(rings+1):
        t=math.pi*j/rings
        for i in range(segments):
            a=math.tau*i/segments
            v.append((loc[0]+radii[0]*math.sin(t)*math.cos(a),loc[1]+radii[1]*math.sin(t)*math.sin(a),loc[2]+radii[2]*math.cos(t)))
    for j in range(rings):
        for i in range(segments):a=j*segments+i;b=j*segments+(i+1)%segments;f.append((a,b,b+segments,a+segments))
    o=c.mesh(name,v,f,mat)
    for p in o.data.polygons:p.use_smooth=True
    return o

def shrub(name,x,y,h=1.5,radius=.7,seed=1,base=0):
    rng=random.Random(seed);v,f,mi=[],[],[]
    for j in range(2300):
        az=rng.random()*math.tau;r=radius*rng.random()**.5;z=base+h*.55+rng.uniform(-.4,.4)*h
        c.leaf_data(v,f,mi,(x+r*math.cos(az),y+r*math.sin(az),z),rng.uniform(.11,.21),rng,rng.randrange(5))
    c.mesh(name+' leaves',v,f,c.foliage_materials('Shrub glossy leaf '),mi)
    for j in range(5):
        a=j*math.tau/5;c.rod(name+' branch',(x,y,base),(x+radius*.5*math.cos(a),y+radius*.5*math.sin(a),base+h*.85),.024,n.palette()['seam'],.006)

def bench(x,y,angle=0):
    p=n.palette();wood=c.material('Avenue bench warm hardwood',(.29,.12,.034),.76)
    def pt(a,b,z):return (x+a*math.cos(angle)-b*math.sin(angle),y+a*math.sin(angle)+b*math.cos(angle),z)
    for a in [-.69,.69]:
        for b in [-.25,.25]:c.rod('Bench cast iron leg',pt(a,b,.02),pt(a,b,.42),.039,p['dark'])
        c.rod('Bench back support',pt(a,.25,.05),pt(a,.42,.98),.035,p['dark'])
        for b in [-.30,.30]:c.rod('Bench curled armrest support',pt(a,b,.4),pt(a,b,.64),.025,p['dark'])
        c.rod('Bench armrest',pt(a,-.29,.65),pt(a,.35,.65),.035,p['dark'])
    for b in [-.24,-.08,.08,.24]:
        o=c.box('Bench seat timber slat',pt(0,b,.44),(1.8,.13,.055),wood,.012);o.rotation_euler.z=angle
    for z in [.63,.79,.95]:
        o=c.box('Bench back timber slat',pt(0,.30+(z-.6)*.15,z),(1.8,.055,.12),wood,.012);o.rotation_euler.z=angle

def lamp(x,y):
    p=n.palette();glass=c.material('Garden lamp frosted pane',(.63,.65,.48),.48)
    c.rod('Garden lamp flared base',(x,y,0),(x,y,.35),.15,p['dark'],.09,12)
    c.rod('Garden lamp shaft',(x,y,.35),(x,y,3.35),.055,p['dark'],.04,12)
    c.rod('Garden lamp tapered lantern',(x,y,3.15),(x,y,3.70),.10,glass,.35,6)
    c.rod('Garden lamp cap',(x,y,3.70),(x,y,3.75),.38,p['dark'],.37,6)
    for i in range(6):
        a=i*math.tau/6;c.rod('Garden lantern frame',(x+.10*math.cos(a),y+.10*math.sin(a),3.15),(x+.35*math.cos(a),y+.35*math.sin(a),3.70),.015,p['dark'],sides=5)

def fence(x,y0,y1,height=3.2):
    p=n.palette();green=c.material('Court green coated wire',(.014,.19,.10),.43,.38)
    for y in [y0+i*3 for i in range(math.ceil((y1-y0)/3)+1)]:
        y=min(y,y1);c.box('Court fence post',(x,y,height/2),(.095,.095,height),green)
    for z in [.08,height]:c.rod('Court fence continuous tube',(x,y0,z),(x,y1,z),.028,green,sides=6)
    # Single mesh of crossed diagonal wire; geometry remains visible in oblique view.
    v,f=[],[];pitch=.17
    for direction in [-1,1]:
        for i in range(int(((y1-y0)+height)/pitch)+2):
            start=y0-height+i*pitch
            if direction==1:
                lo=max(0,y0-start);hi=min(height,y1-start)
                if hi>lo:c.tube_data(v,f,(x,start+lo,lo),(x,start+hi,hi),.006,.006,4)
            else:
                lo=max(0,start+height-y1);hi=min(height,start+height-y0)
                if hi>lo:c.tube_data(v,f,(x,start+height-lo,lo),(x,start+height-hi,hi),.006,.006,4)
    c.mesh('Court actual chain link mesh',v,f,green)

def standing_statue(x,y,z0=.65):
    """Suit/stance from 369/r; approximate sculpt, not an exact portrait likeness."""
    p=n.palette();bronze=c.material('Statue dark patinated bronze',(.105,.12,.105),.47,.72)
    c.noise(bronze,32,.22,.009)
    v=[(x-.92,y-.65,0),(x+.92,y-.65,0),(x+.92,y+.65,0),(x-.92,y+.65,0),
       (x-.58,y-.43,z0),(x+.58,y-.43,z0),(x+.58,y+.43,z0),(x-.58,y+.43,z0)]
    c.mesh('Statue tapered granite plinth',v,[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],p['seam'])
    c.box('Statue bronze foot platform',(x,y,z0+.045),(1.1,.83,.09),bronze,.012)
    def pt(a,b,z):return(x+a,y+b,z0+z)
    # Trousers, shoes and centre creases, two legs distinctly separated.
    for side in [-1,1]:
        a=side*.155
        ellipsoid('Statue leather shoe',pt(a,-.12,.17),(.13,.25,.095),bronze)
        c.rod('Statue trouser leg',pt(a,0,.23),pt(a*.75,0,1.13),.12,bronze,.15,14)
        c.rod('Statue trouser front crease',pt(a,-.116,.3),pt(a*.75,-.141,1.06),.013,bronze,sides=5)
    # Elliptical cross sections shape the jacket shoulders, waist and hem.
    v,f=[],[];sections=[(.94,.32,.18),(1.04,.33,.19),(1.35,.27,.18),(1.66,.36,.21),(1.77,.29,.18),(1.80,.13,.13)]
    for z,w,d in sections:
        for i in range(24):a=i*math.tau/24;v.append(pt(w*math.cos(a),d*math.sin(a),z))
    for j in range(len(sections)-1):
        for i in range(24):a=j*24+i;b=j*24+(i+1)%24;f.append((a,b,b+24,a+24))
    torso=c.mesh('Statue sculpted jacket',v,f,bronze)
    for face in torso.data.polygons:face.use_smooth=True
    # One arm relaxed and the other bent toward a trouser pocket.
    for a,b,rad in [((.31,0,1.67),(.40,-.025,1.29),.10),((.40,-.025,1.29),(.36,-.08,.99),.085),
                    ((-.31,0,1.67),(-.41,-.06,1.30),.105),((-.41,-.06,1.30),(-.24,-.17,1.10),.086)]:
        c.rod('Statue tailored sleeve',pt(*a),pt(*b),rad,bronze,rad*.82,14)
    ellipsoid('Statue hanging hand',pt(.36,-.09,.94),(.065,.05,.12),bronze)
    ellipsoid('Statue pocket hand',pt(-.23,-.18,1.10),(.07,.045,.08),bronze)
    for side in [-1,1]:
        verts=[pt(side*.07,-.165,1.76),pt(side*.25,-.19,1.61),pt(side*.12,-.215,1.40),pt(side*.035,-.20,1.63)]
        c.mesh('Statue jacket lapel',verts,[(0,1,2,3)],bronze)
    for z in [1.10,1.30,1.48]:ellipsoid('Statue jacket button',pt(.015,-.20,z),(.013,.01,.013),bronze,12,6)
    c.rod('Statue neck',pt(0,0,1.77),pt(0,0,1.93),.085,bronze,sides=16)
    ellipsoid('Statue head',pt(0,-.015,2.055),(.145,.14,.195),bronze,32,20)
    ellipsoid('Statue swept hair',pt(0,.029,2.17),(.143,.116,.075),bronze,32,14)
    ellipsoid('Statue nose bridge',pt(0,-.152,2.04),(.030,.052,.065),bronze,16,10)
    for side in [-1,1]:
        ellipsoid('Statue ear',pt(side*.145,0,2.05),(.028,.038,.063),bronze,16,10)
        c.rod('Statue brow',pt(side*.025,-.144,2.10),pt(side*.106,-.121,2.10),.012,bronze,sides=6)
        ellipsoid('Statue eye relief',pt(side*.063,-.14,2.07),(.026,.013,.012),bronze,16,8)
    c.rod('Statue mouth',pt(-.046,-.146,1.985),pt(.046,-.146,1.985),.009,bronze,sides=6)
    # Plaque text is modeled separately; full biography is not invented.
    gold=c.material('Statue plaque aged brass',(.49,.36,.12),.45,.60)
    angle=math.atan(.22/z0)
    plaque=c.box('Statue brass identification plaque',(x,y-.558,z0*.46),(.86,.018,.38),gold)
    plaque.rotation_euler.x=-angle
    c.text('Statue plaque name','朱自清',(x,y-.557,z0*.52),.115,p['dark'],(math.pi/2-angle,0,0))
    c.text('Statue plaque dates','1898—1948',(x,y-.595,z0*.35),.058,p['dark'],(math.pi/2-angle,0,0))
    for obj in c.COL.objects:
        if obj.type=='MESH' and obj.data.materials and obj.data.materials[0]==bronze:
            for face in obj.data.polygons:face.use_smooth=True
