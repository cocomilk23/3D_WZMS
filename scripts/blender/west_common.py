"""West precinct components, based on archived panoramas; dimensions estimated."""
import math,random
from mathutils import Vector
import campus_common as c,north_common as n,south_detail_common as s,island_common as h

def tube(v,f,points,radii,sides=12):
    pts=[Vector(q) for q in points];st=len(v)
    for i,q in enumerate(pts):
        tangent=(pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]).normalized()
        u=tangent.cross(Vector((0,0,1)))
        if u.length<.01:u=tangent.cross(Vector((0,1,0)))
        u.normalize();w=tangent.cross(u)
        for j in range(sides):
            a=j*math.tau/sides;v.append(q+radii[i]*(u*math.cos(a)+w*math.sin(a)))
    for i in range(len(pts)-1):
        for j in range(sides):a=st+i*sides+j;b=st+i*sides+(j+1)%sides;f.append((a,b,b+sides,a+sides))
    f.extend([tuple(st+j for j in reversed(range(sides))),tuple(st+(len(pts)-1)*sides+j for j in range(sides))])

def banyan(name,x,y,height=11,radius=7,seed=362):
    rng=random.Random(seed);v,f,lv,lf,mi=[],[],[],[],[]
    bark=s.mottled('West banyan weathered bark',[(.075,.065,.047),(.23,.205,.15)],5)
    if not any(q.type=='BUMP' for q in bark.node_tree.nodes):c.noise(bark,39,.42,.055)
    points=[(.13*math.sin(t*2),.13*math.sin(t),t*height*.48) for t in [j/18 for j in range(19)]]
    tube(v,f,points,[.79*(1-j/24)**1.2+.08 for j in range(19)],18)
    for j in range(10):
        a=j*math.tau/10;points=[];rs=[]
        for q in range(17):
            t=q/16;r=.42+1.85*t;points.append((r*math.cos(a+.13*t),r*math.sin(a+.13*t),.03+1.6*(1-t)**2.6));rs.append(.23*(1-t)+.025)
        tube(v,f,points,rs,12)
    for j in range(12):
        az=j*2.399+rng.uniform(-.20,.20);reach=radius*rng.uniform(.6,.95)
        base=Vector((0,0,height*rng.uniform(.15,.28)))
        elbow=Vector((reach*.44*math.cos(az),reach*.44*math.sin(az),height*rng.uniform(.45,.57)))
        end=Vector((reach*math.cos(az),reach*math.sin(az),height*rng.uniform(.64,.84)))
        pts=[(1-t)**2*base+2*t*(1-t)*elbow+t*t*end for t in [k/18 for k in range(19)]]
        tube(v,f,pts,[.35*(1-k/18)**1.6+.04 for k in range(19)],12)
        for k in range(18):
            a=az+rng.uniform(-1.4,1.4);start=pts[rng.randrange(9,19)]
            tip=start+Vector((math.cos(a)*radius*rng.uniform(.16,.36),math.sin(a)*radius*rng.uniform(.16,.36),rng.uniform(.3,1.6)))
            mid=start.lerp(tip,.48)+Vector((0,0,.25));tube(v,f,[start,mid,tip],[.05,.026,.009],7)
            for q in range(9):
                aa=a+rng.uniform(-1.8,1.8);root=start.lerp(tip,rng.uniform(.45,1))
                twig=root+Vector((math.cos(aa)*rng.uniform(.35,.85),math.sin(aa)*rng.uniform(.35,.85),rng.uniform(-.1,.38)))
                c.tube_data(v,f,root,twig,.007,.0015,5)
                for leaf in range(16):
                    t=.14+.86*(leaf//2)/7;attach=root.lerp(twig,t);angle=aa+(-1 if leaf%2 else 1)*.7
                    length=rng.uniform(.10,.17);u=Vector((math.cos(angle),math.sin(angle),rng.uniform(-.20,.3)))*length
                    side=Vector((-math.sin(angle),math.cos(angle),0))*length*.34
                    st=len(lv);lv.extend([attach,attach+u+side,attach+u*1.88,attach+u-side,attach+u+Vector((0,0,.024))])
                    lf.extend([(st,st+1,st+4),(st+1,st+2,st+4),(st+2,st+3,st+4),(st+3,st,st+4)]);mi.extend([rng.randrange(5)]*4)
        for k in range(9):
            q=pts[rng.randrange(8,17)]+Vector((rng.uniform(-.28,.28),rng.uniform(-.28,.28),0))
            bottom=max(2.5,q.z-rng.uniform(1.2,4.4))
            tube(v,f,[q,q+Vector((.08,-.04,(bottom-q.z)*.5)),Vector((q.x+.13,q.y+.04,bottom))],[.015,.010,.0035],5)
    a=c.mesh(name+' connected trunks roots and twigs',v,f,bark);a.location=(x,y,0)
    for face in a.data.polygons:face.use_smooth=True
    b=c.mesh(name+' attached broadleaf canopy',lv,lf,c.foliage_materials('West banyan leaf ',True),mi);b.location=(x,y,0)
    return [a,b]

def meadow(name,cx,cy,rx,ry,height=.65,seed=1):
    soil=s.mottled('West shaded mound soil',[(.07,.085,.024),(.16,.18,.055)],3)
    def z(x,y):return -.018+height*max(0,1-((x-cx)/rx)**2-((y-cy)/ry)**2)**1.4
    v=[(cx,cy,z(cx,cy))];f=[];steps=96;rings=18
    for j in range(1,rings+1):
        for i in range(steps):a=i*math.tau/steps;x=cx+rx*j/rings*math.cos(a);y=cy+ry*j/rings*math.sin(a);v.append((x,y,z(x,y)))
    for i in range(steps):f.append((0,1+i,1+(i+1)%steps))
    for j in range(rings-1):
        for i in range(steps):a=1+j*steps+i;b=1+j*steps+(i+1)%steps;f.append((a,b,b+steps,a+steps))
    c.mesh(name+' rolling earth',v,f,soil)
    rng=random.Random(seed);v,f,mi=[],[],[]
    for i in range(int(rx*ry*95)):
        a=rng.random()*math.tau;r=rng.random()**.5;x=cx+rx*r*math.cos(a);y=cy+ry*r*math.sin(a)
        for j in range(7):
            az=rng.random()*math.tau;length=rng.uniform(.22,.45);base=Vector((x,y,z(x,y)));side=Vector((-math.sin(az),math.cos(az),0))*.012
            mid=base+Vector((math.cos(az)*length*.34,math.sin(az)*length*.34,length*.72));tip=base+Vector((math.cos(az)*length,math.sin(az)*length,length*.4))
            st=len(v);v.extend([base-side,base+side,mid+side*.7,mid-side*.7,tip]);f.extend([(st,st+1,st+2,st+3),(st+3,st+2,st+4)]);mi.extend([rng.randrange(5)]*2)
    c.mesh(name+' arching groundcover blades',v,f,c.foliage_materials('West groundcover ',True),mi)

def lotus(name,cx,cy,rx,ry,seed=1):
    rng=random.Random(seed);v,f,mi=[],[],[];sv,sf=[],[];stem=c.material('West lotus olive stems',(.10,.18,.045),.74)
    for j in range(60):
        a=rng.random()*math.tau;r=rng.random()**.5;x=cx+rx*r*math.cos(a);y=cy+ry*r*math.sin(a);z=rng.uniform(-.47,.20);rad=rng.uniform(.25,.53)
        c.tube_data(sv,sf,(x-.12,y,-1.1),(x,y,z),.012,.009,6)
        st=len(v);v.append((x,y,z+.045));ph=rng.random()*6
        for k in range(40):
            aa=k*math.tau/40;rr=rad*(1+.06*math.sin(aa*7+ph));v.append((x+rr*math.cos(aa),y+rr*math.sin(aa),z+.10*math.sin(aa+ph)+.04*math.sin(7*aa)))
        for k in range(40):f.append((st,st+1+k,st+1+(k+1)%40));mi.append(j%5)
    c.mesh(name+' radial broad leaves',v,f,c.foliage_materials('West lotus leaf '),mi);c.mesh(name+' rooted stems',sv,sf,stem)

def stone_bridge(name,x,y0,y1,width=2.2):
    stone=s.mottled('Rong weathered carved granite',[(.19,.20,.17),(.38,.38,.32)],24);c.noise(stone,90,.20,.009)
    c.box(name+' continuous deck',(x,(y0+y1)/2,-.15),(width,y1-y0,.30),stone)
    for sign in [-1,1]:
        xx=x+sign*(width/2+.02);count=math.ceil((y1-y0)/1.5)
        for j in range(count+1):
            yy=y0+(y1-y0)*j/count
            c.box(name+' square carved pier',(xx,yy,.41),(.24,.27,.82),stone,.016)
            c.rod(name+' round post crown',(xx,yy,.82),(xx,yy,1.01),.115,stone,sides=16)
        for j in range(count):
            a=y0+(y1-y0)*j/count+.14;b=y0+(y1-y0)*(j+1)/count-.14
            for z,w in [(.18,.14),(.69,.15)]:c.box(name+' open stone railing',(xx,(a+b)/2,z),(.14,b-a,w),stone,.009)
            for yy in [a+.13,b-.13]:c.box(name+' balustrade panel short end',(xx,yy,.41),(.13,.13,.35),stone,.008)
    for yy in [y0+1,y1-1]:c.box(name+' masonry support',(x,yy,-.79),(width*.82,.42,1.25),stone)

def wood_deck(name,poly,width=2.5):
    dark=c.material('West boardwalk dark joints',(.025,.021,.017),.88)
    wood=s.mottled('West boardwalk weathered brown timber',[(.075,.047,.028),(.20,.15,.095)],7)
    if not any(q.type=='BUMP' for q in wood.node_tree.nodes):c.noise(wood,82,.25,.012)
    s.ribbon(name+' supporting continuous deck',poly,width,dark,-.032,.23,miter=True)
    for a,b in zip(poly,poly[1:]):
        a,b=Vector(a),Vector(b);direction=(b-a).normalized();normal=Vector((-direction.y,direction.x));count=math.ceil((b-a).length/.14)
        for j in range(count):
            q=a.lerp(b,(j+.5)/count);s.segment(name+' individual timber board',q-normal*width/2,q+normal*width/2,(b-a).length/count-.004,wood,0,.055)

def prism(name,outline,top,bottom,mat):
    count=len(outline);v=[(*q,z) for z in [bottom,top] for q in outline]
    f=[tuple(reversed(range(count))),tuple(range(count,count*2))]
    for i in range(count):j=(i+1)%count;f.append((i,j,j+count,i+count))
    return c.mesh(name,v,f,mat)

def chain_path(name,poly,gaps=()):
    p=n.palette();v,f=[],[]
    for a,b in zip(poly,poly[1:]):
        a,b=Vector(a),Vector(b)
        if any((a-Vector(q)).length<r or (b-Vector(q)).length<r for q,r in gaps):continue
        c.box(name+' granite post',(*a,.42),(.18,.18,.84),p['stone'],.012)
        for j in range(10):
            t=j/10;u=(j+1)/10;aa=a.lerp(b,t);bb=a.lerp(b,u)
            c.tube_data(v,f,(*aa,.69-.20*math.sin(math.pi*t)),(*bb,.69-.20*math.sin(math.pi*u)),.012,.012,6)
    c.mesh(name+' hanging chain',v,f,p['dark'])
