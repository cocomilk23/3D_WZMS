"""v024 Ju island: stepped stone bridge, growing beds and broad tree with pebble seat."""
import bpy,math,sys,random
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).parent))
import campus_common as c,north_common as n,north_landscape as l,south_detail_common as s,island_common as h,culture_common as k
sc=bpy.data.scenes['WZMS_Campus'];c.activate(sc);p=n.palette()
c.collection('200_Ju_Island_And_Garden_Paths')
earth=s.mottled('Ju cultivated brown soil',[(.075,.045,.017),(.25,.18,.085)],4.5);bank=h.pebble('Ju island weathered stone',(.25,.27,.24))
outline=h.island('Ju island',352,117,26,24,earth,bank)
c.box('Ju eastern lake extension',(387.5,125,-1.18),(35,140,.06),bpy.data.materials['Heyu green lake water'])
red=n.paving('Ju garden red brick',(.39,.23,.17),(.22,.11),.005)
grey=n.paving('Ju pale stone path',(.46,.47,.42),(.8,.5),.008)
for name,points in [('Entry',[(338.2,115),(346,115)]),('West garden',[(346,101),(346,132)]),('East garden',[(358,101),(358,132)]),('South cross',[(338,106),(368,106)]),('North cross',[(338,125),(368,125)])]:
    s.ribbon('Ju '+name+' walk',points,2.3,red if name!='Entry' else grey,0,.18,miter=True)
    for side in [-1,1]:s.ribbon('Ju '+name+' stone border',s.offset(points,side*1.16),.12,p['stone'],.012,.15)
c.collection('201_Ju_Stepped_Stone_Bridge')
k.stairs('Ju west stone bridge flight',(325,115,0),(329.2,115,1.68),3.7,14,bank,False)
k.stairs('Ju east stone bridge flight',(338.2,115,0),(334,115,1.68),3.7,14,bank,False)
c.box('Ju bridge raised crown deck',(331.6,115,1.48),(4.82,3.7,.4),bank)
s.ribbon('Ju bridge west approach',[(322,115),(325,115)],3.7,grey,0,.25)
# Masonry arch beneath the deck and curved parapets remain real geometry.
for sign in [-1,1]:
    yy=115+sign*1.78
    points=[(325,yy,0),(329.2,yy,1.68),(334,yy,1.68),(338.2,yy,0)]
    for a,b in zip(points,points[1:]):
        aa,bb=Vector(a),Vector(b);length=(bb-aa).length
        for i in range(math.ceil(length/1.2)+1):
            q=aa.lerp(bb,i/math.ceil(length/1.2));c.box('Ju bridge square granite post',(q.x,q.y,q.z+.56),(.18,.22,1.14),bank,.014)
        s.beam('Ju bridge stone coping',aa+Vector((0,0,1.0)),bb+Vector((0,0,1.0)),.17,.22,bank)
        c.mesh('Ju bridge solid carved parapet',[aa+Vector((0,0,.2)),bb+Vector((0,0,.2)),bb+Vector((0,0,.79)),aa+Vector((0,0,.79))],[(0,1,2,3)],bank)
    v=[]
    for i in range(49):
        t=i/48;x=325+13.2*t;inner=-.95+2.10*math.sin(math.pi*t);outer=inner+.35
        v.extend([(x,yy,inner),(x,yy,outer)])
    c.mesh('Ju bridge side arch stone band',v,[(i*2,i*2+1,i*2+3,i*2+2) for i in range(48)],bank)
c.collection('202_Ju_Mature_Tree_And_Pebble_Seat')
seat=h.pebble('Ju white river pebble tree seat',(.49,.51,.44))
h.ring('Ju large circular pebble tree seat',352,115,2.8,3.4,.53,-.1,seat)
n.disk('Ju tree groundcover soil',352,115,.02,2.79,p['green'])
n.broad_tree('Ju specimen spreading tree',352,115,12.6,6.8,2424)
bark=c.material('Ju exposed root bark',(.14,.10,.06),.94);c.noise(bark,35,.38,.04)
trunk=bpy.data.objects['Ju specimen spreading tree scaffold branches'];trunk.data.materials.clear();trunk.data.materials.append(bark)
for face in trunk.data.polygons:face.use_smooth=True
v,f=[],[]
for j in range(23):
    z=j*.1;r=.30+.62*(1-j/22)**2
    for i in range(36):
        a=i*math.tau/36;rr=r*(1+.07*math.sin(6*a+z))
        v.append((352+rr*math.cos(a),115+rr*math.sin(a),z))
for j in range(22):
    for i in range(36):a=j*36+i;b=j*36+(i+1)%36;f.append((a,b,b+36,a+36))
base=c.mesh('Ju flared continuous old tree base',v,f,bark)
for face in base.data.polygons:face.use_smooth=True
for i in range(12):
    a=i*math.tau/12;v,f=[],[]
    def root(t):
        r=.42+2.04*t;az=a+.14*math.sin(math.pi*t)
        return (352+r*math.cos(az),115+r*math.sin(az),.025+1.40*(1-t)**2.8)
    for j in range(25):
        t=j/24;q=Vector(root(t));tangent=(Vector(root(min(1,t+.005)))-Vector(root(max(0,t-.005)))).normalized()
        u=tangent.cross(Vector((0,0,1))).normalized();w=tangent.cross(u);radius=.21*(1-t)+.015
        for m in range(16):
            angle=m*math.tau/16;v.append(q+radius*(u*math.cos(angle)+w*math.sin(angle)))
    for j in range(24):
        for m in range(16):a0=j*16+m;b0=j*16+(m+1)%16;f.append((a0,b0,b0+16,a0+16))
    obj=c.mesh('Ju curved buttress root',v,f,bark)
    for face in obj.data.polygons:face.use_smooth=True
c.planting('Ju tree liriope groundcover',(352,115),(4.0,4.0),.22,424,450)
c.collection('203_Ju_Cultivated_Beds_And_Labels')
rng=random.Random(2424)
for cx,cy,w,depth in [(340,111,6,5),(340,121,6,5),(352,102,8,4),(352,130,8,6),(363,112,6,7),(363,121,6,5)]:
    c.box('Ju rectangular cultivation bed',(cx,cy,-.015),(w,depth,.08),earth)
    for side in [-1,1]:
        c.box('Ju red brick bed edging',(cx+side*(w/2+.06),cy,.025),(.12,depth+.24,.13),red)
        c.box('Ju red brick bed edging',(cx,cy+side*(depth/2+.06),.025),(w+.24,.12,.13),red)
    for row in range(int(depth/.7)):
        y=cy-depth/2+.40+row*.7
        c.box('Ju low raised growing row',(cx,y,.035),(w-.55,.44,.10),earth)
        c.planting('Ju cultivated green leafy row',(cx,y),(w-.7,.36),.24,24000+int(cx*cy)+row,75)
    c.box('Ju plant label stake',(cx-w/2+.4,cy-depth/2+.3,.4),(.035,.035,.75),p['steel'])
    sign=c.box('Ju green bed information label',(cx-w/2+.4,cy-depth/2+.27,.68),(.4,.035,.22),p['green']);sign['text_status']='Unresolved source text, no invented transcript'
c.collection('204_Ju_Shade_And_Water_Edge_Detail')
for j,(x,y,scale) in enumerate([(337,109,.79),(337,121,.77),(342,133,.85),(356,137,.88),(368,128,.78),(372,116,.84),(365,101,.73),(350,97,.69)]):s.tree(x,y,scale,j*.77)
for x,y in [(339,102),(365,132)]:
    n.broad_tree('Ju young supported fruit tree',x,y,3.6,1.45,int(x*y))
    for a in [0,2.1,4.2]:s.beam('Ju young tree tripod support',(x+1*math.cos(a),y+1*math.sin(a),0),(x,y,2.0),.045,.045,bark)
h.chain_edge('Ju shoreline posts and chains',outline,gaps=[((328,115),7)])
h.stone_table('Ju bridgehead stone seats',340,117.6)
for x,y in [(344,107.5),(360,126.5)]:l.lamp(x,y)
# Distinctive blue campus service post at the entry, visible in 423.
blue=c.material('Ju blue service post enamel',(.025,.18,.38),.41,.15)
c.box('Ju blue service pillar',(342,113,.95),(.28,.30,1.9),blue,.015)
c.box('Ju service pale panel',(342,112.84,1.25),(.19,.024,.85),p['white'])
c.rod('Ju service curved mast',(342,113,1.9),(342,113,4.0),.035,blue)
s.beam('Ju service mast top arm',(342,113,4),(342,112.6,4.1),.06,.05,blue)
c.collection('208_Ju_Review_Cameras')
c.camera('93_Ju_stone_bridge',(342,115,1.7),(328,115,2),25)
c.camera('94_Ju_tree_seat',(345,109,1.65),(352,115,3.1),24)
c.camera('95_Ju_growing_garden',(359,104,1.7),(351,126,1.5),25)
c.camera('96_Ju_island_overview',(384,84,45),(343,119,0),40)
h.save(24,'Ju island exterior: stepped masonry bridge, river-pebble circular tree seat, specimen tree, ordered cultivation beds, red brick paths, service post and water-edge chains. Plant identity and exact plot layout remain estimates.',[421,423,424,347],'96_Ju_island_overview')
