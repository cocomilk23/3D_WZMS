"""v022 Taohua island: observed portals, pebble paving, pavilion and twin kiosks."""
import bpy,math,sys,random
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).parent))
import campus_common as c,north_common as n,north_landscape as l,south_detail_common as s,island_common as h,culture_common as k
sc=bpy.data.scenes['WZMS_Campus'];c.activate(sc);p=n.palette()
relocated=[]
for o in sc.objects:
    if o.name.startswith('Jiushan low evergreen bank'):
        q=sum((o.matrix_world@Vector(v) for v in o.bound_box),Vector())/8
        if 209<q.x<213 and 90<q.y<93:relocated.append(o.name)
h.retire('v0.0.22',names=[o.name for o in sc.objects if o.name.startswith(('Jiushan white garden gateway pier','Jiushan white garden gateway lintel'))]+['Jiushan garden landscape stone']+relocated)
c.collection('180_Taohua_Island_And_Shore')
grass=s.mottled('Taohua mixed shaded soil',[(.09,.13,.035),(.24,.24,.10)],2)
bank=h.pebble('Taohua rough water bank',(.32,.34,.29))
outline=h.island('Taohua island',211,74,17,24,grass,bank,hole=(211,60,9.4))
c.box('Taohua southern lake extension',(217.5,47.5,-1.18),(165,25,.06),bpy.data.materials['Heyu green lake water'])
h.chain_edge('Taohua shoreline',outline,gaps=[((211,96),4)])
c.collection('181_Taohua_Coloured_Portals_And_Mosaic')
white=c.material('Taohua white stone portals',(.80,.79,.71),.76);c.noise(white,85,.16,.012)
pink=c.material('Taohua pink portals',(.53,.17,.31),.69);blue=c.material('Taohua pastel blue portals',(.13,.50,.61),.67)
for name,a,b in [('White',(211,96),(211,82)),('Pink',(211,82),(221,73)),('Blue',(211,82),(202,72)),('Pavilion',(211,82),(198,80))]:h.mosaic_path(name+' walk',a,b)
n.disk('Taohua path junction stone inset',211,82,.024,2.15,p['stone'])
h.ring('Taohua junction dark pebble rim',211,82,2.08,2.18,.028,.021,h.pebble('Island black river pebble mosaic',(.23,.24,.215)))
for j in range(4):h.portal('Taohua white peaked frame',(211,94-j*2.8),0,white)
for name,a,b,mat in [('pink',(213,80),(220,73),pink),('blue',(209,80),(203,73),blue)]:
    a,b=Vector(a),Vector(b);d=(b-a).normalized();angle=math.atan2(d.y,d.x)+math.pi/2
    for j in range(4):h.portal('Taohua '+name+' peaked frame',a.lerp(b,j/3),angle,mat)
h.stone_table('Taohua four stone stools',207.3,83.2)
c.collection('182_Taohua_Sunken_Garden_And_Twin_Kiosks')
slab=n.paving('Taohua rose court slabs',(.43,.27,.22),(.65,.38),.007)
n.disk('Taohua sunken circular paving',211,60,-.84,6.3,slab)
for i in range(7):h.ring('Taohua concentric granite terrace',211,60,6.25+i*.45,6.70+i*.45,-.72+i*.12,-1.05,p['stone'])
h.ring('Taohua upper rim',211,60,9.4,10.15,0,-.22,grass)
for j in range(7):
    yy=69.7-j*.45;c.box('Taohua dark step inset',(211,yy,.003-j*.12),(1.1,.30,.018),p['seam'])
# Two octagonal brick structures with arched white sashes; use unknown function honestly.
brick=n.paving('Taohua orange brick kiosk',(.53,.30,.17),(.28,.115),.008)
h.use_facade_uv(brick)
for x,y in [(207,72),(215,72)]:
    kiosk=c.rod('Taohua octagonal brick kiosk',(x,y,0),(x,y,3.5),2.0,brick,sides=8);h.vertical_uv(kiosk)
    c.rod('Taohua kiosk stepped eave',(x,y,3.47),(x,y,3.65),2.12,p['stone'],sides=8)
    c.rod('Taohua kiosk hipped cap',(x,y,3.65),(x,y,4.2),2.02,p['stone'],.40,8)
    l.ellipsoid('Taohua kiosk ball finial',(x,y,4.25),(.18,.18,.18),p['stone'])
    for j in range(8):
        a=(j+.5)*math.tau/8;normal=Vector((math.cos(a),math.sin(a)));u=Vector((-normal.y,normal.x));mid=Vector((x,y))+normal*1.855
        # Glazed inset fronts placed just outside opaque shell; exterior-only structures.
        pts=[mid-u*.54,mid+u*.54];v=[(*pts[0],.60),(*pts[1],.60),(*pts[1],2.3)]
        for z in range(21):
            angle=z*math.pi/20;q=mid+u*(.54*math.cos(angle));v.append((*q,2.3+.54*math.sin(angle)))
        c.mesh('Taohua arched inset glazing',v,[tuple(range(len(v)))],p['glass'])
        for side in [-1,1]:q=mid+u*side*.59;s.beam('Taohua white sash jamb',(*q,.55),(*q,2.3),.095,.075,white)
        for z in [.59,1.03,1.47,1.91,2.3]:s.beam('Taohua horizontal sash',(*(mid-u*.57),z),(*(mid+u*.57),z),.052,.06,white)
        s.beam('Taohua sash centre upright',(*mid,.6),(*mid,2.85),.05,.06,white)
        for j2 in range(24):
            aa=j2*math.pi/24;bb=(j2+1)*math.pi/24;q=mid+u*(.59*math.cos(aa));r=mid+u*(.59*math.cos(bb))
            s.beam('Taohua arch white surround',(*q,2.3+.59*math.sin(aa)),(*r,2.3+.59*math.sin(bb)),.09,.085,white)
c.collection('183_Taohua_Teal_Roof_Pavilion')
teal=c.material('Taohua pavilion teal metal roof',(.025,.32,.31),.43,.2)
x,y=198,80
n.disk('Taohua pavilion floor',x,y,0,3.1,p['stone'],6)
for j in range(6):
    a=(j+.5)*math.tau/6;c.rod('Taohua pavilion pale column',(x+2.65*math.cos(a),y+2.65*math.sin(a),0),(x+2.65*math.cos(a),y+2.65*math.sin(a),2.7),.11,white,sides=12)
c.rod('Taohua pavilion hipped teal roof',(x,y,2.8),(x,y,3.6),3.5,teal,.12,6)
for j in range(6):
    a=j*math.tau/6;s.beam('Taohua pavilion roof ridge',(x,y,3.63),(x+3.5*math.cos(a),y+3.5*math.sin(a),2.82),.055,.06,teal)
h.stone_table('Taohua pavilion table',x,y)
c.collection('184_Taohua_Trees_And_Garden_Furniture')
l.ellipsoid('Taohua relocated entry landscape stone',(208,98.5,.43),(.75,.48,.64),bank,24,12)
l.shrub('Taohua relocated entry shrub',215,92,.5,1.3,13824)
for j,(x,y,scale) in enumerate([(203,91,.83),(217,91,.90),(222,84,.82),(198,87,.74),(223,76,.67),(199,69,.75),(221,64,.71),(205,53,.7),(216,52,.68)]):s.tree(x,y,scale,j*.91)
for x,y in [(218,87),(205,87),(204,78),(219,78),(225,70),(197,75)]:l.shrub('Taohua clipped border',x,y,1.1,1.15,int(x*y))
for x,y in [(223,70),(199,65)]:n.palm('Taohua reference palm',x,y,6.7,int(x*y))
for x,y in [(214,85),(220,76),(203,70)]:l.lamp(x,y)
c.collection('188_Taohua_Review_Cameras')
c.camera('85_Taohua_white_portals',(211,81,1.7),(211,95,2.1),24)
c.camera('86_Taohua_twin_kiosks',(211,59,1.0),(211,72,1.85),25)
c.camera('87_Taohua_coloured_garden',(211,81.5,1.7),(204,73,1.7),22)
c.camera('88_Taohua_island_overview',(246,35,48),(209,77,0),40)
h.save(22,'Taohua island exterior: peaked coloured frames, pebble mosaic, sunken terraces, twin arched kiosks, teal pavilion and planting. Image-estimated layout; kiosk interiors not modelled.',[382,419,420,347],'88_Taohua_island_overview')
