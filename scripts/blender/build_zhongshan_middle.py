"""v008: shaded Zhongshan avenue, Jiangkou junction and Zhu Ziqing garden.
Reference 368 F/B/L/R and 369 R plus preview overview; estimated local metres.
"""
import sys,math,random
from pathlib import Path
import bpy
from mathutils import Matrix,Vector
sys.path.insert(0,str(Path(__file__).parent))
import campus_common as c
import north_common as n
import north_landscape as land
scene=bpy.data.scenes['WZMS_Campus'];c.activate(scene);p=n.palette()
# Bright diffuse skylight is visible under the canopy in 368/369. Preserve the
# direct sun, and increase the weak inherited sky fill for this integrated version.
for node in scene.world.node_tree.nodes:
    if node.type=='BACKGROUND':node.inputs['Strength'].default_value=.28
c.collection('50_Zhongshan_Middle_Road_And_Junctions')
red=n.paving('Zhongshan rose granite slabs',(.44,.25,.18),(1.1,.62),.0028)
grey=n.paving('Zhongshan sidepath grey flagstone',(.48,.50,.43),(.6,.6),.006)
green=n.paving('Zhongshan sidepath green border',(.095,.17,.105),(.30,.30),.004)
c.box('Middle avenue continuous road',(54,247.5,-.17),(8.6,86,.32),red)
c.box('Middle western grey sidepath',(44.2,247.5,-.17),(4.0,86,.32),grey)
c.box('Middle west tree verge',(48,247.5,-.16),(3.6,85,.30),p['green'])
c.box('Middle eastern garden soil',(73,247.5,-.16),(29,85,.30),p['green'])
c.box('Middle eastern sidepath',(83,247.5,-.17),(3.4,86,.32),grey)
for y,w in [(209,4.5),(259,3.6)]:
    c.box('Jiangkou crossing paved walk',(64,y,-.145),(45,w,.28),grey)
    for yy in [y-w/2+.18,y+w/2-.18]:c.box('Crosswalk green granite border',(64,yy,-.002),(45,.34,.016),green)
for x in [42.1,46.3,49.56,58.44,81.18,84.82]:
    for j in range(85):
        y=205.5+j
        if any(abs(y-yy)<ww/2+.3 for yy,ww in [(209,4.5),(259,3.6)]):continue
        c.box('Middle dressed kerbstone',(x,y,.075),(.19,.98,.17),p['stone'],.013)
for y in [219,271]:
    n.disk('Middle circular manhole',55,y,.004,.41,p['steel'],64)
    for j in range(7):c.box('Manhole inset rib',(55-.26+j*.087,y,.015),(.015,.57,.007),p['dark'])
for y in [214,256,282]:
    c.box('Avenue drainage inlet',(58.1,y,-.012),(.47,.72,.07),p['dark'])
    for j in range(10):c.box('Drain inlet grate',(58.1,y-.32+j*.07,.004),(.46,.016,.018),p['steel'])

c.collection('51_Zhongshan_Middle_Shade_Trees')
proto=n.broad_tree('Middle mature avenue tree',48,214,10.4,4.7,368)
proto2=n.broad_tree('Middle alternate avenue tree',60.2,216,10.8,4.9,369)
for side,x in enumerate([48,60.2]):
    for j,y in enumerate([223,232,241,250,268,278,287]):
        n.duplicate_tree(proto if j%2 else proto2,x,y,j*1.27+side,.92+(j%3)*.055)
        c.rod('Avenue tree whitewash',(x,y,.03),(x,y,1.05),.305,p['white'],.29,12)
for x,y in [(73,221),(73,239),(74,274),(78,286)]:n.duplicate_tree(proto,x,y,y*.14,.65)
# Ground cover is split at crosswalks, with leaf meshes away from walking lanes.
for x,w in [(48,2.6),(60.2,1.8)]:
    spans=[(213,247.5),(250.5,254),(264,289)] if x>50 else [(213,254),(264,289)]
    for ya,yb in spans:
        c.planting('Avenue liriope border',(x,(ya+yb)/2),(w,yb-ya),.25,int(x+ya),90)
for ya,yb in [(214,255),(264,287)]:c.grass('Middle garden lawn',(72,(ya+yb)/2),(15,yb-ya),int(ya))
for j,(x,y) in enumerate([(69,216),(77,218),(71,232),(77,242),(71,267),(77,278),(67,285)]):
    land.shrub('Garden clipped shrub',x,y,1.4,.9,j+368)
for x,y in [(76,228),(71,279)]:n.palm('Middle reference palm',x,y,6.3,int(y))

c.collection('52_Zhongshan_Middle_Court_Edge')
court=c.material('Middle court blue acrylic',(.08,.24,.32),.88)
c.box('Visible adjoining court surface',(20,247.5,-.19),(39,86,.34),court)
land.fence(39.5,205,290,3.0)
line=c.material('Court white painted line',(.75,.77,.72),.85)
for yy in [227,268]:
    for x in [11.5,26.5]:c.box('Court touchline',(x,yy,-.009),(.05,28,.018),line)
    for y in [yy-14,yy+14]:c.box('Court baseline',(19,y,-.009),(15,.05,.018),line)
    c.box('Court centre line',(19,yy,-.009),(15,.05,.018),line)
    n.disk('Court centre circle',19,yy,.002,1.80,line,96,1.75)
    for side in [-1,1]:
        for x in [16.55,21.45]:c.box('Court key lane',(x,yy+side*11.1,-.008),(.05,5.8,.018),line)
        c.box('Court free throw line',(19,yy+side*8.2,-.008),(4.9,.05,.018),line)
        for radius,cy in [(1.8,yy+side*8.2),(6.75,yy+side*12.425)]:
            v,f=[],[]
            for i in range(81):
                a=math.pi*i/80
                for rr in [radius-.025,radius+.025]:v.append((19+rr*math.cos(a),cy-side*rr*math.sin(a),.002))
            for i in range(80):f.append((2*i,2*i+1,2*i+3,2*i+2))
            c.mesh('Court arc marking',v,f,line)
    for y,side in [(yy-12.5,-1),(yy+12.5,1)]:
        c.rod('Basketball stand upright',(19,y+side*1.4,0),(19,y+side*1.4,3.6),.10,p['white'],sides=10)
        c.rod('Basketball stand cantilever',(19,y+side*1.4,3.55),(19,y,3.45),.07,p['white'])
        c.box('Basketball transparent backboard',(19,y,3.43),(1.8,.07,1.05),p['glass'])
        for x in [18.1,19.9]:c.box('Backboard side frame',(x,y-side*.055,3.43),(.055,.12,1.1),p['white'])
        for z in [2.91,3.95]:c.box('Backboard horizontal frame',(19,y-side*.055,z),(1.85,.12,.055),p['white'])
        n.disk('Basketball hoop rim',19,y-side*.38,3.04,.23,c.material('Basketball hoop orange',(.7,.12,.01),.45,.3),48,.208)
for yy in [218,236,275]:
    c.box('Court perimeter bulletin panel',(39.66,yy,1.9),(.065,2.3,1.05),p['white'])
    for k in range(5):c.box('Bulletin display fine rule',(39.71,yy,1.55+k*.14),(.012,2.0,.015),p['seam'])

c.collection('53_Zhongshan_Middle_Visible_Building')
c.box('Middle building foundation',(96,247,-.26),(15,51,.50),p['stone'])
before=set(scene.objects)
n.academic_wing('Middle six storey road facade',96,247,48,11,6,-1,False)
bpy.context.view_layer.update()
rot=Matrix.Translation((96,247,0))@Matrix.Rotation(-math.pi/2,4,'Z')@Matrix.Translation((-96,-247,0))
for o in set(scene.objects)-before:o.matrix_world=rot@o.matrix_world

c.collection('54_Zhu_Ziqing_Statue_Garden')
land.standing_statue(64.4,249,.68)
bpy.context.view_layer.update()
rot=Matrix.Translation((64.4,249,0))@Matrix.Rotation(-math.pi/2,4,'Z')@Matrix.Translation((-64.4,-249,0))
for o in list(c.COL.objects):o.matrix_world=rot@o.matrix_world
c.box('Statue approach pad',(61.6,249,-.14),(4.0,2.2,.28),grey)
for x,y in [(64,247.5),(64,250.5),(65.7,249)]:c.planting('Statue low groundcover',(x,y),(1.0,1.1),.24,int(x*y),150)

c.collection('55_Zhongshan_Middle_Street_Furniture')
for j,y in enumerate([220,238,267,284]):
    land.bench(79.3,y,math.pi/2)
    land.lamp(80.1,y+3.3)
for x,y in [(50.2,212),(57.4,212),(50.4,256.7)]:
    pot=c.material('Avenue glazed brown pot',(.18,.095,.045),.32)
    c.rod('Avenue movable shrub pot',(x,y,0),(x,y,.55),.35,pot,.46,24)
    c.rod('Pot rim',(x,y,.55),(x,y,.59),.48,pot,sides=24)
    land.shrub('Avenue potted shrub',x,y,1.50,.62,int(x*y),.48)
for y in [222,246,276]:
    x=48
    c.box('Tree banner red panel',(x+.37,y,2.7),(.46,.08,1.16),c.material('Avenue anniversary red',(.52,.018,.012),.75))
    c.box('Tree banner blue panel',(x-.17,y,2.7),(.46,.08,1.16),c.material('Avenue anniversary blue',(.018,.16,.32),.75))
    for dx in [-.17,.37]:
        for j in range(7):c.box('Banner lettering suggestion',(x+dx,y-.049,2.28+j*.12),(.11,.012,.040),p['white'])
# Recreate the timber/dark wayfinding family used throughout the source tour.
wood=c.material('North wayfinding timber',(.44,.23,.065),.76)
for x,y,body in [(79.8,212,'江口路'),(61.5,264,'中山路')]:
    c.box('Wayfinding concrete foot',(x,y,.17),(.60,.25,.34),p['stone'])
    c.box('Wayfinding timber upright',(x,y,1.25),(.63,.18,1.82),wood)
    c.box('Wayfinding dark cap',(x,y,2.41),(.63,.19,.5),p['dark'])
    for j,ch in enumerate(body):c.text('Wayfinding road label',ch,(x,y-.11,2.18-j*.27),.22,p['white'])
for x,y in [(47.5,211),(79,260)]:
    for dx,col in [(-.28,(.025,.17,.27)),(.28,(.18,.20,.17))]:
        c.box('Twin waste bin',(x+dx,y,.53),(.51,.46,1.06),p['steel'],.025)
        c.box('Waste classification panel',(x+dx,y-.24,.55),(.37,.025,.6),c.material('Waste classification '+str(col),col))
        c.box('Waste bin opening',(x+dx,y-.25,.93),(.35,.045,.11),p['dark'])

c.collection('58_Zhongshan_Middle_Cameras')
c.camera('23_Middle_avenue_north',(54,213,1.72),(54,274,3.2),30)
c.camera('24_Jiangkou_junction',(58,211,1.72),(75,240,3.8),30)
c.camera('25_Zhu_Ziqing_garden',(55.4,245.2,1.7),(64.4,249,1.62),43)
c.camera('26_Middle_avenue_overview',(137,192,73),(59,243,6),40)
c.camera('27_Middle_court_edge',(54,263,1.72),(36,238,2.0),32)
scene.camera=scene.objects['23_Middle_avenue_north']
scene['scope']='Integrated south scenes, Buqing, Zhongshan middle avenue and visible roadside exteriors; not complete court or building interiors.'
scene['next_route_connection']='Middle avenue north end x54 y290 z-0.01'
c.save(c.ROOT/'models/campus/WZMS_Campus_v008.blend','v0.0.8',[119232349,119232352,119232353,119232354,119232355,119232366,119232367,119232368,119232369])
print('WZMS_BUILD_COMPLETE v0.0.8',flush=True)
