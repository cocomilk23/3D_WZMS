"""v009: north avenue, red telephone kiosk, bamboo-islet lane and canteen branch.
Photographic evidence: 370 F/L, 371 R, plus cube previews. No surveyed coordinates.
"""
import sys,math
from pathlib import Path
import bpy
from mathutils import Matrix
sys.path.insert(0,str(Path(__file__).parent))
import campus_common as c
import north_common as n
import north_landscape as land
scene=bpy.data.scenes['WZMS_Campus'];c.activate(scene);p=n.palette()
c.collection('60_Zhongshan_North_Road_And_Branches')
c.box('North regional terrain CONTEXT_ESTIMATED',(70,297.5,-.4),(190,185,.60),p['green'])
c.box('Bamboo lane planting support',(84,293,-.17),(48,10,.30),p['green'])
c.box('Canteen branch planting support',(84,353,-.17),(48,10,.30),p['green'])
red=bpy.data.materials['Zhongshan rose granite slabs']
grid=n.paving('North white square tile paving',(.57,.59,.54),(.20,.20),.006)
for node in grid.node_tree.nodes:
    if node.type=='TEX_BRICK':node.offset=0
green=bpy.data.materials['Zhongshan sidepath green border']
c.box('North avenue continuous red paving',(54,325,-.17),(8.6,71,.32),red)
c.box('North west grey strip',(44.2,325,-.17),(4,71,.32),grid)
c.box('North west tree verge',(48,325,-.16),(3.6,71,.30),p['green'])
c.box('North east planted soil',(73,325,-.16),(29,71,.30),p['green'])
c.box('North east white tile path',(83,325,-.17),(3.4,71,.32),grid)
for y in [294,348]:
    c.box('North lateral lane',(80,y,-.145),(55,4.4,.28),grid)
    for yy in [y-1.95,y+1.95]:c.box('Lateral green stone strip',(80,yy,-.002),(55,.26,.016),green)
    for x in range(56,108,4):c.box('Lateral paving green grid',(x,y,-.002),(.18,4.4,.016),green)
for x in [42.1,46.3,49.56,58.44,81.18,84.82]:
    for j in range(71):
        y=289.5+j
        if min(abs(y-294),abs(y-348))<2.8:continue
        c.box('North lane kerbstone',(x,y,.075),(.19,.98,.17),p['stone'],.012)
for y in [305,338,357]:
    n.disk('North road manhole',54.6,y,.002,.38,p['steel'],64)
    for j in range(7):c.box('North cover grate',(54.35+j*.08,y,.013),(.015,.52,.01),p['dark'])
c.box('North building entry forewalk',(86.8,322,-.14),(7.5,11,.28),grid)
for y in [302,333,350]:
    c.box('North road storm drain',(58.1,y,-.006),(.42,.70,.06),p['dark'])
    for j in range(8):c.box('North road drain bar',(58.1,y-.3+j*.086,.013),(.42,.018,.02),p['steel'])

c.collection('61_Zhongshan_North_Tree_Avenue')
proto=[scene.objects['Middle mature avenue tree scaffold branches'],scene.objects['Middle mature avenue tree canopy leaves']]
for side,x in enumerate([48,60.2]):
    for j,y in enumerate([301,310,320,330,340,356]):
        n.duplicate_tree(proto,x,y,j*1.19+side,.96+(j%3)*.04)
        c.rod('North tree whitewash',(x,y,.02),(x,y,.88),.30,p['white'],.28,12)
for x,w in [(48,2.6),(60.2,1.8)]:
    for ya,yb in [(298,344),(352,359)]:c.planting('North liriope border',(x,(ya+yb)/2),(w,yb-ya),.25,int(x+ya),85)
for ya,yb in [(298,343),(352,359)]:c.grass('North garden lawn',(72,(ya+yb)/2),(15,yb-ya),int(ya))
for j,y in enumerate([301,311,330,340,355]):
    land.shrub('North garden shrub',73,y,1.5,.95,370+j)
    land.bench(79.3,y+2,math.pi/2)
    land.lamp(80,y+4)
for j,x in enumerate([70,78,98,104]):
    c.tree('Bamboo-islet lane young tree',x,289,5.7,1.3,370+j)
    c.tree('Canteen branch young tree',x,353,5.9,1.4,410+j)

c.collection('62_Zhongshan_North_Visible_Facade')
c.box('North road building foundation',(96,320,-.26),(15,46,.50),p['stone'])
before=set(scene.objects)
n.academic_wing('North six storey open gallery',96,320,44,11,6,-1,True)
bpy.context.view_layer.update()
rot=Matrix.Translation((96,320,0))@Matrix.Rotation(-math.pi/2,4,'Z')@Matrix.Translation((-96,-320,0))
for o in set(scene.objects)-before:o.matrix_world=rot@o.matrix_world
for yy in [301,339]:
    c.box('North stair tower stone flank',(89.7,yy,11),(3.8,5.8,22),p['stone'])
    c.box('North stair tower glazed front',(87.76,yy,10.6),(.045,5.1,21.2),p['glass'])
    for z in range(27):c.box('North stair tower horizontal fin',(87.58,yy,.3+z*.78),(.43,5.4,.07),p['steel'])
    for dy in [-2.55,0,2.55]:c.box('North stair tower vertical mullion',(87.69,yy+dy,10.6),(.13,.055,21.2),p['white'])
    c.box('North stair tower roof fin',(89.7,yy,22.6),(4.3,6.2,1.0),p['stone'])
    c.box('North stair tower projecting cap',(89,yy,22.3),(5.2,6.8,.28),p['white'])
stepmat=n.paving('North entrance rose granite',(.43,.27,.22),(.75,.45),.003)
for i in range(6):
    a=85.3+i*.36;b=90.8
    c.box('North building entrance step',((a+b)/2,322,(i+1)*.08-.01),(b-a,5,(i+1)*.16),stepmat)
c.box('North building entrance landing',(90.4,322,.47),(1.2,5,.96),stepmat)
c.box('North entrance door recess',(90.34,322,2),(.035,3.2,3.0),p['glass'])
for yy in [320.4,322,323.6]:c.box('North entrance door frame',(90.27,yy,2),(.10,.07,3.1),p['white'])
c.box('North entrance canopy',(88.9,322,3.6),(3.4,5.5,.20),p['white'])
for yy in [319.5,324.5]:
    c.rod('North stair handrail',(85.5,yy,1.1),(88,yy,1.9),.032,p['steel'])
for k,col in enumerate([(.02,.12,.25),(.42,.015,.009),(.015,.22,.06),(.024,.026,.025)]):
    x,y=86.8,306+k*.57;m=c.material('North waste bin '+str(k),col,.54)
    c.box('Four colour waste container',(x,y,.52),(.47,.48,1.04),m,.035)
    c.box('Waste container lid',(x,y,1.07),(.52,.53,.07),p['dark'],.02)
    for yy in [y-.15,y+.15]:c.rod('Waste container wheel',(x+.15,yy,.12),(x+.24,yy,.12),.10,p['dark'],sides=12)

c.collection('63_North_Red_Telephone_Kiosk')
cx,cy=61.8,296.8
kred=c.material('Telephone booth enamel red',(.48,.015,.018),.38,.2)
kg=c.material('Telephone booth clear glazing',(.72,.81,.79),.08)
kp=next(v for v in kg.node_tree.nodes if v.type=='BSDF_PRINCIPLED');kp.inputs['Transmission Weight'].default_value=.90
before=set(scene.objects)
c.box('Telephone kiosk concrete pad',(cx,cy,.07),(1.4,1.25,.14),p['stone'])
for dx in [-.55,.55]:
    for dy in [-.48,.48]:c.box('Telephone kiosk frame post',(cx+dx,cy+dy,1.35),(.075,.075,2.55),kred,.008)
c.box('Telephone kiosk flat cap',(cx,cy,2.67),(1.26,1.12,.16),kred,.025)
c.box('Telephone kiosk red rear panel',(cx,cy+.46,1.36),(1.08,.045,2.45),kred)
for dx in [-.55,.55]:
    c.box('Telephone kiosk side glass',(cx+dx,cy,1.35),(.02,.90,2.1),kg)
    for z in [.2,2.43]:c.box('Telephone side crossbar',(cx+dx,cy,z),(.075,1.0,.075),kred)
c.box('Telephone kiosk header',(cx,cy-.49,2.46),(1.08,.06,.30),kred)
c.text('Telephone kiosk header text','中国电信',(cx,cy-.53,2.43),.13,p['white'])
c.box('Telephone unit',(cx,cy+.34,1.48),(.35,.18,.43),p['steel'],.015)
c.box('Telephone dial panel',(cx+.07,cy+.24,1.42),(.16,.025,.21),p['dark'])
for j in range(4):
    for k in range(3):c.box('Telephone dial key',(cx+.02+k*.05,cy+.22,1.35+j*.047),(.029,.023,.025),p['white'])
c.rod('Telephone handset',(cx-.13,cy+.21,1.3),(cx-.13,cy+.21,1.65),.037,p['dark'])
c.rod('Telephone cord',(cx-.14,cy+.20,1.32),(cx-.04,cy+.22,1.06),.008,p['dark'],sides=5)
bpy.context.view_layer.update()
rot=Matrix.Translation((cx,cy,0))@Matrix.Rotation(-math.pi/2,4,'Z')@Matrix.Translation((-cx,-cy,0))
for o in set(scene.objects)-before:o.matrix_world=rot@o.matrix_world

c.collection('64_North_Bulletin_Boards_And_Utilities')
for y in [307,323,339]:
    for yy in [y-1.7,y+1.7]:c.box('North notice board pedestal',(62.3,yy,1.42),(.23,.23,2.84),p['dark'])
    c.box('North glazed notice board backing',(62.3,y,1.85),(.18,3.6,1.75),p['dark'],.025)
    c.box('North notice board print field',(62.18,y,1.85),(.02,3.28,1.46),p['white'])
    c.box('North notice board blue header',(62.16,y,2.42),(.02,3.28,.30),c.material('North bulletin header blue',(.026,.22,.32),.71))
    for k in range(7):c.box('North bulletin text layout',(62.145,y,1.35+k*.135),(.014,2.92,.021),p['seam'])
    c.box('North notice board top cornice',(62.3,y,2.78),(.38,3.96,.16),p['dark'])
for y in [313,347]:
    hred=c.material('Hydrant weathered red',(.31,.035,.025),.7)
    c.rod('Fire hydrant body',(47.2,y,.05),(47.2,y,.66),.095,hred,sides=12)
    c.rod('Fire hydrant top',(47.2,y,.65),(47.2,y,.72),.13,hred,sides=12)
    c.rod('Fire hydrant side coupling',(47.0,y,.40),(47.4,y,.40),.075,hred,sides=12)
for x,y in [(60.9,345),(61.1,295)]:
    c.rod('Security camera mast',(x,y,0),(x,y,4.1),.042,p['dark'])
    c.box('Security crossarm',(x,y,4.05),(.95,.075,.075),p['steel'])
    for side in [-1,1]:
        c.box('Outdoor security camera',(x+side*.37,y-.12,4.13),(.14,.35,.14),p['white'],.025)
        c.rod('Camera lens',(x+side*.37,y-.30,4.13),(x+side*.37,y-.31,4.13),.045,p['dark'],sides=12)

c.collection('65_North_Court_Visible_Edge')
c.box('North adjacent court extension',(20,325,-.19),(39,71,.34),bpy.data.materials['Middle court blue acrylic'])
land.fence(39.5,290,360,3.0)

c.collection('68_Zhongshan_North_Cameras')
c.camera('28_North_avenue',(54,299,1.72),(54,354,3.2),30)
c.camera('29_Telephone_and_bamboo_lane',(55.5,291,1.72),(64,297,2.0),35)
c.camera('30_North_entry_and_noticeboards',(57,315,1.72),(86.7,322,4.2),30)
c.camera('31_Canteen_branch',(56,345.5,1.72),(101,348,2.7),30)
c.camera('32_North_route_overview',(136,271,76),(59,324,7),42)
scene.camera=scene.objects['28_North_avenue']
scene['scope']='Integrated through north Zhongshan avenue, visible roadside facade, telephone kiosk and canteen branch. Canteen and north gate remain next deliveries.'
scene['next_route_connection']='North gate approach x54 y360 z-0.01; canteen branch extends to x107.5 y348'
c.save(c.ROOT/'models/campus/WZMS_Campus_v009.blend','v0.0.9',[119232349,119232352,119232353,119232354,119232355,119232366,119232367,119232368,119232369,119232370,119232371])
print('WZMS_BUILD_COMPLETE v0.0.9',flush=True)
