"""v007: Buqing plaza, architectural frontage and northward through-passage.

355 full cube faces reviewed. 367 establishes the southern bridge connection.
Local +Y follows the route northward; plan dimensions remain image estimates.
"""
import sys, math
from pathlib import Path
import bpy
from mathutils import Matrix,Vector
sys.path.insert(0,str(Path(__file__).parent))
import campus_common as c
import north_common as n
scene=bpy.data.scenes['WZMS_Campus'];c.activate(scene)
old=bpy.data.collections.get('39_North_Context_PENDING_BUQING')
if old:
    for o in list(old.objects):bpy.data.objects.remove(o,do_unlink=True)
    bpy.data.collections.remove(old)
p=n.palette();X=54;Y=181
c.collection('40_Buqing_Paving_And_Routes')
floor=n.paving('Buqing staggered grey granite',(.58,.59,.55),(.6,.30),.006)
c.box('Buqing continuous plaza slab',(54,157.5,-.17),(114,47,.32),floor)
c.box('Buqing through-passage floor',(54,188,-.17),(14,16,.32),floor)
c.box('Buqing north exit apron',(54,200,-.17),(14,11,.32),floor)
for x in [-2,110]:
    c.box('Buqing plaza drainage channel',(x,158,-.015),(.20,46,.08),p['dark'])
    for j in range(230):c.box('Drain grate cross bar',(x,135+j*.2,.007),(.22,.022,.025),p['steel'])
for y in [143,171]:c.box('Paving transverse accent',(54,y,-.002),(111,.32,.014),p['stone'])
for x,y in [(83,147),(23,167)]:
    c.box('Buqing utility cover',(x,y,.004),(.7,.7,.018),p['steel'])
    for j in range(8):c.box('Utility cover groove',(x-.29+j*.08,y,.014),(.009,.6,.004),p['dark'])

c.collection('41_Buqing_Academic_Frontage')
for x in [20.5,87.5]:n.academic_wing('Buqing six storey open gallery',x,187,44,12,6,-1,True)
# The large stone/glass gate is a real open passage at ground level.
c.collection('42_Buqing_Central_Portal')
for x in [45,63]:
    c.box('Buqing monumental stone pier',(x,187,12),(4.5,12,24),p['stone'])
    n.stone_joints(x,180.993,4.5,24)
    c.box('Buqing raised stone crown',(x,187,25.2),(4.5,8,2.4),p['stone'])
    c.box('Buqing cantilever crown roof',(x+(.8 if x<54 else -.8),184.5,24.9),(6.1,7.5,.30),p['white'])
    # Slim vertical glass reveals continue above the upper horizontal screen.
    gx=x+(2.29 if x<54 else -2.29)
    c.box('Buqing vertical teal reveal',(gx,181,12),(.30,.045,24),p['glass'])
    for j in range(30):c.box('Reveal horizontal cap',(gx,180.83,.4+j*.8),(.43,.36,.06),p['steel'])
for lo,hi in [(4.8,10.9),(15.0,23.4)]:
    c.box('Buqing glass bridge floor',(54,186.6,lo),(13.5,11.2,.22),p['stone'])
    c.box('Buqing glass bridge roof',(54,186.6,hi),(13.5,11.2,.22),p['stone'])
    for yy,out in [(180.96,-1),(192.25,1)]:
        c.box('Buqing translucent screen',(54,yy,(lo+hi)/2),(13.4,.028,hi-lo),p['glass'])
        for i in range(10):c.box('Buqing curtain wall vertical frame',(47.3+i*1.49,yy+out*.08,(lo+hi)/2),(.055,.14,hi-lo),p['steel'])
        for j in range(int((hi-lo)/.8)+1):
            c.box('Buqing glass sunshade',(54,yy+out*.15,lo+j*.8),(13.5,.40,.065),p['steel'])
    for j in range(6):c.box('Buqing upper interior circulation floor',(54,184+j*1.35,lo-.13),(13.5,.01,.015),p['seam'])
c.box('Buqing stone middle bridge',(54,187,12.95),(13.5,12,4.0),p['stone'])
n.stone_joints(54,180.989,13.5,4.0,10.95)
for x in [48.8,51.4,56.6,59.2]:
    c.box('Buqing small square dark window',(x,180.97,13.2),(.46,.05,.44),p['dark'])
    for dx in [-.255,.255]:c.box('Square window stone trim',(x+dx,180.93,13.2),(.035,.08,.5),p['white'])
c.box('Buqing recessed middle glass slit',(54,180.90,12.95),(1.3,.07,4.0),p['glass'])
for z in [11,11.8,12.6,13.4,14.2,15]:c.box('Middle slit transom',(54,180.80,z),(1.38,.15,.05),p['steel'])
c.box('Buqing entry canopy',(54,179.7,4.65),(11.8,3.5,.25),p['white'],.02)
for x in [48.5,59.5]:
    c.rod('Buqing round entrance column',(x,179.3,.05),(x,179.3,4.5),.18,p['white'],sides=20)
for x in [50,54,58]:
    for y in [183,187,191]:
        c.box('Buqing soffit recessed luminaire',(x,y,4.66),(.34,.34,.035),p['white'])
for x in [43.1,64.9]:
    c.box('Buqing pier low planting kerb',(x,179.9,.11),(3.7,1.4,.24),p['stone'],.05)
    c.box('Buqing pier soil',(x,179.9,.2),(3.45,1.15,.08),p['green'])
    o=c.planting('Buqing pier groundcover',(x,179.9),(3.4,1.1),.28,int(x*10),180);o.location.z=.19

c.collection('43_Buqing_South_Facade')
n.academic_wing('Buqing south classroom facade',18,138,40,11,6,1,False,True)
for x in [-2.17,38.17]:
    for yy in [133.1,142.9]:
        c.box('South facade narrow stair glazing',(x,yy,10.7),(.025,.55,21.1),p['glass'])
        for j in range(27):c.box('South stair horizontal shade',(x,yy,j*.8+.1),(.30,.73,.065),p['steel'])
# End-wall gold calligraphy appears in 355/r; inscription shape is approximated.
gold=c.material('Buqing weathered gold lettering',(.43,.32,.095),.35,.55)
for col,body in enumerate(['集四海英才','作千秋栋梁']):
    for j,ch in enumerate(body):
        c.text('South wall inscription',ch,(38.18,139.4-col*2.1,17.8-j*1.8),1.0,gold,(math.pi/2,0,math.pi/2))

c.collection('44_Buqing_Library_Entrance_Context')
# Model the actual visible library frontage. Unseen library interiors are later scope.
cx,cy=114,155
c.box('Library podium roof',(cx,cy,4.3),(15,33,.38),p['stone'])
for yy in range(141,171,5):c.box('Library podium column',(107.5,yy,2.1),(.58,.65,4.2),p['stone'])
c.box('Library entrance back wall',(114,155,2),(0.25,30,4),p['stone'])
for yy in [148,151,154,157,160,163]:
    c.box('Library entrance glazing',(113.83,yy,1.85),(.045,2.8,3.3),p['glass'])
    for dy in [-1.4,0,1.4]:c.box('Library entrance mullion',(113.73,yy+dy,1.85),(.12,.05,3.3),p['white'])
for level in range(2):
    z=4.5+level*4.1
    c.box('Library upper floor',(cx+2,cy,z),(15,32,.3),p['stone'])
    c.box('Library upper front lower cladding',(108.45,cy,z+.7),(.28,31,1.4),p['stone'])
    c.box('Library upper front upper cladding',(108.45,cy,z+3.75),(.28,31,.7),p['stone'])
    for yy in range(141,171,3):
        c.box('Library upper ribbon glazing',(108.27,yy,z+2.35),(.035,2.8,1.6),p['glass'])
        c.box('Library front vertical rib',(108.1,yy-1.45,z+2),(.3,.12,3.8),p['white'])
    for xx in [108.5,123.5]:c.box('Library rear side envelope',(xx,cy,z+2),(.25,32,4),p['stone'])
    for yy in [139,171]:c.box('Library end envelope',(116,yy,z+2),(15,.25,4),p['stone'])
c.box('Library roof',(116,155,12.9),(15.8,32.8,.3),p['stone'])
for yy in [139,171]:c.box('Library roof parapet',(116,yy,13.35),(15.8,.25,.65),p['white'])
c.rod('Library round rooftop lantern',(115,155,13),(115,155,15),4.6,p['glass'],sides=64)
c.rod('Library round silver cap',(115,155,15),(115,155,15.22),4.9,p['white'],sides=64)
c.box('Library central stone title panel',(108.0,155,10.55),(.28,14.8,4.05),p['stone'])
c.box('Library central narrow ribbon',(107.84,155,8.98),(.03,13.0,.36),p['glass'])
for j in range(6):c.box('Library stone panel bed joint',(107.851,155,8.56+j*.8),(.008,14.8,.009),p['seam'])
for j in range(13):c.box('Library stone panel upright joint',(107.851,147.8+j*1.2,10.55),(.008,.009,4.0),p['seam'])
c.text('Library title','图 书 馆',(107.80,155,10.5),1.25,gold,(math.pi/2,0,-math.pi/2))
for i in range(25):
    start=134.5+i*.28;end=142
    c.box('Library external stair',(104,(start+end)/2,(i+1)*.085-.01),(5,end-start,(i+1)*.17),p['stone'])
c.box('Library stair connected landing',(105.8,142.2,4.12),(8,2,.24),p['stone'])
for x in [101.6,106.4]:
    c.rod('Library stair handrail',(x,134.5,1.0),(x,141.5,5.25),.035,p['steel'])
    for j in range(10):c.rod('Library stair rail post',(x,134.5+j*.75,j*.455),(x,134.5+j*.75,1+j*.455),.028,p['steel'])
red=c.material('Buqing event poster red',(.54,.013,.009),.8)
c.box('Library event display backing',(106.9,167,1.75),(.14,8.8,3.5),p['stone'])
c.box('Library event red display',(106.8,167,1.77),(.03,8.5,3.22),red)
c.text('Event display visible headline','用青春丈量祖国',(106.77,167,1.65),.63,gold,(math.pi/2,0,-math.pi/2))

c.collection('45_Buqing_Crest_Mosaic')
blue=c.material('Buqing cobalt blue terrazzo',(.018,.055,.30),.54)
c.noise(blue,220,.26,.009)
cream=c.material('Buqing crest white terrazzo',(.82,.84,.81),.67);c.noise(cream,190,.18,.005)
cx,cy=54,157
n.disk('Crest stainless perimeter',cx,cy,.009,8.1,p['steel'],192)
n.disk('Crest outer white trim',cx,cy,.011,8.02,cream,192)
n.disk('Crest blue name ring',cx,cy,.013,7.86,blue,192)
n.disk('Crest white emblem field',cx,cy,.015,5.5,cream,192)
# Reconstructed planar emblem, independent editable polygons rather than a photo plane.
shape=[(-4.4,1.5),(-3.2,2.1),(-1.2,2.8),(0,3.6),(1.2,2.8),(3.2,2.1),(4.4,1.5),(3.7,1.4),(3.1,1.55),(3.45,-.5),(0,-1.3),(-3.45,-.5),(-3.1,1.55),(-3.7,1.4)]
c.mesh('Crest stylised roof and open book',[(cx+x,cy+y,.019) for x,y in shape],[tuple(range(len(shape)))],blue)
for side in [-1,1]:
    pts=[(.23,1.93),(2.73,1.7),(3.00,-.25),(.23,-.87)]
    c.mesh('Crest white book page',[(cx+side*x,cy+y,.021) for x,y in pts],[(0,1,2,3)],cream)
c.text('Crest founding year','1902',(cx,cy-3.95,.024),1.65,p['seam'],(0,0,0))
for body,start,end,size in [('浙江省温州中学',155,25,1.02),('ZHEJIANG WENZHOU HIGH SCHOOL',205,335,.62)]:
    for j,ch in enumerate(body):
        a=math.radians(start+(end-start)*j/max(1,len(body)-1));r=6.48
        # Letters face the same reading side around each semicircle.
        angle=a-math.pi/2 if start<180 else a+math.pi/2
        c.text('Crest perimeter '+ch,ch,(cx+r*math.cos(a),cy+r*math.sin(a),.024),size,p['steel'],(0,0,angle))

c.collection('46_Buqing_Trees_And_Furniture')
c.box('Buqing western planting ground',(-10,158,-.15),(15,49,.30),p['green'])
c.grass('Buqing western lawn',(-10,158),(13,47),355)
c.planting('Buqing western low planting',(-5,158),(3,44),.32,355,85)
proto=n.broad_tree('Buqing mature canopy',-7,140,10,4.1,355)
for j,y in enumerate([149,158,167,176]):n.duplicate_tree(proto,-7,y,j*.85,.94+j*.025)
for x,y in [(99,139),(101,177),(-10,181)]:n.duplicate_tree(proto,x,y,1.7,.78)
for x,y in [(100,174),(100,144),(6,176)]:n.palm('Buqing reference palm',x,y,7.5,int(y))
for y in [145,161,172]:
    c.box('Buqing granite seat',(-1.7,y,.42),(1.0,2.5,.18),p['stone'],.04)
    for dy in [-.8,.8]:c.box('Seat stone support',(-1.7,y+dy,.18),(.75,.3,.36),p['stone'])
    c.box('Buqing litter bin',(-1.7,y+2.2,.48),(.55,.55,.96),p['dark'],.035)
    for k in range(8):c.box('Bin vertical metal slat',(-1.99,y+1.96+k*.067,.47),(.028,.029,.77),p['steel'])
for x,y in [(3,144),(102,173)]:
    c.rod('Buqing lamp mast',(x,y,0),(x,y,5.3),.044,p['dark'])
    c.rod('Buqing lamp curved arm',(x,y,5.15),(x+.65,y,5.50),.025,p['dark'])
    c.box('Buqing LED lamp head',(x+.64,y,5.46),(.50,.24,.075),p['steel'],.02)

c.collection('48_Buqing_Cameras')
c.camera('18_Buqing_arrival',(57,140,1.72),(54,182,10),26)
c.camera('19_Buqing_crest_and_galleries',(88,147,8),(45,174,8),29)
c.camera('20_Buqing_library',(60,162,1.72),(111,155,6),30)
c.camera('21_Buqing_overview',(145,98,90),(50,163,8),43)
c.camera('22_Buqing_portal_passage',(54,179,1.72),(54,201,2.3),28)
scene.camera=scene.objects['18_Buqing_arrival']
scene['scope']='Integrated south scenes plus Buqing plaza, six-storey galleries, portal and visible library frontage. North avenue remains next delivery.'
scene['next_route_connection']='Buqing north apron x54 y205 z-0.01; local image-estimated metres'
c.save(c.ROOT/'models/campus/WZMS_Campus_v007.blend','v0.0.7',[119232349,119232352,119232353,119232354,119232355,119232366,119232367,119232348])
print('WZMS_BUILD_COMPLETE v0.0.7',flush=True)
