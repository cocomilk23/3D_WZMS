"""v032 gymnasium exterior, open louvred facade and recessed entrance."""
import bpy,math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import campus_common as c,north_common as n,north_landscape as l
import south_detail_common as s,island_common as h,culture_common as u,sports_common as q
sc=bpy.data.scenes['WZMS_Campus'];c.activate(sc);p=n.palette();before=set(bpy.data.objects)
clad=n.paving('Gym ivory panel facade',(.65,.67,.64),(1.2,1.2),.003)
h.use_facade_uv(clad)
white=c.material('Gym pale aluminium frames',(.70,.74,.71),.36,.32)
glass=c.material('Gym upper blue green glazing',(.035,.21,.22),.19,.37)
red=s.mottled('Gym weathered rose granite',[(.25,.10,.078),(.45,.24,.18)],9)
c.noise(red,105,.2,.007)
tile=n.paving('Gym small square grey tiles',(.42,.45,.41),(.115,.115),.004)
green=n.paving('Gym green tile border',(.10,.21,.14),(.115,.115),.004)
soil=s.mottled('Gym planted ground soil',[(.065,.10,.028),(.17,.20,.060)],2)
cx=-76;y0,y1=382,432
c.collection('280_Gym_Forecourt_And_Nantian_Connection')
c.box('Gym continuous ground foundation',(cx,405,-.90),(59,66,1.62),soil)
c.box('Gym small tile entrance forecourt',(cx,376.5,-.07),(56,10.7,.14),tile)
for xx in [cx-17,cx,cx+17]:c.box('Gym green tile longitudinal strip',(xx,376.5,.008),(.35,10.5,.016),green)
for yy in [372.8,378.2]:c.box('Gym green tile crossing strip',(cx,yy,.008),(56,.35,.016),green)
yellow=c.material('Gym faded yellow parking lines',(.61,.46,.075),.91)
for xx in [-98,-90,-62,-54]:
    q.flat_line('Gym observed forecourt yellow bay',[(xx-2,373),(xx-2,378),(xx+2,378)],.055,yellow,.024)
asphalt=s.mottled('Gym shaded road asphalt',[(.06,.07,.060),(.14,.15,.13)],3)
road=[(-43,346),(-29,346),(-29,377),(-48,377)]
s.ribbon('Gym connected road support',road,6.2,soil,-.08,1.5,miter=True)
s.ribbon('Gym connected road surface',road,4.2,asphalt,0,.18,miter=True)
for yy in range(350,375,4):c.box('Gym road broken centre line',(-29,yy,.02),(.09,1.6,.015),p['white'])
c.collection('281_Gym_Editable_Exterior_Shell')
c.box('Gym raised structural floor',(cx,407,.90),(48,50,.36),p['stone'])
# Hollow shell; glazed entrance is closed. This delivery does not claim completed interiors.
for xx in [cx-24,cx+24]:
    c.box('Gym longitudinal lower cladding',(xx,407,5.8),(.25,50,9.44),clad)
    c.box('Gym side sill spandrel closes shell',(xx,407,11.035),(.25,50,1.05),clad)
    c.box('Gym high clerestory glass',(xx,407,13.8),(.035,49.4,4.5),glass)
    c.box('Gym roof edge cladding',(xx,407,17),(.29,50,1.8),clad)
    for yy in range(383,433,4):
        c.box('Gym clerestory structural upright',(xx,yy,13.8),(.32,.20,4.8),white)
    for z in [11.45,12.1,13.45,14.8,16.15]:c.box('Gym clerestory horizontal frame',(xx,407,z),(.10,50,.08),white)
c.box('Gym rear lower wall',(cx,y1,5.8),(48,.25,9.44),clad)
c.box('Gym rear sill spandrel closes shell',(cx,y1,11.035),(48,.25,1.05),clad)
c.box('Gym rear high windows',(cx,y1,13.8),(47.6,.035,4.5),glass)
c.box('Gym rear upper cladding',(cx,y1,17),(48,.25,1.8),clad)
for xx in range(-100,-51,4):c.box('Gym rear clerestory upright',(xx,y1,13.8),(.20,.24,4.8),white)
# Front facade breaks around the wide, photographed open horizontal louvres.
for xx in [cx-19,cx+19]:c.box('Gym front cladding side',(xx,y0,6.15),(10,.25,10.14),clad)
c.box('Gym front entrance lintel',(cx,y0,4.92),(28,.65,.65),clad)
c.box('Gym front clerestory spandrel',(cx,y0,11.05),(28,.28,1.0),clad)
c.box('Gym front clerestory band',(cx,y0,13.8),(47.6,.035,4.5),glass)
c.box('Gym front upper cladding',(cx,y0,17),(48,.28,1.8),clad)
for xx in range(-100,-51,4):c.box('Gym front high window structural pier',(xx,y0-.04,13.8),(.30,.30,4.8),white)
for z in [11.45,12.15,13.45,14.8,16.15]:c.box('Gym front high window transom',(cx,y0-.05,z),(48,.12,.08),white)
for xx in [-90,-83,-76,-69,-62]:c.box('Gym open louvre vertical frame',(xx,y0-.15,7.82),(.17,.32,5.24),white)
for j in range(15):
    o=c.box('Gym photographed horizontal ventilation blade',(cx,y0-.24,5.38+j*.345),(28,.42,.085),white);o.rotation_euler.x=.24
for yy in [383,386,389]:c.box('Gym recessed louvre overhead beam',(cx,yy,10.34),(28,.20,.25),white)
c.box('Gym louvre shaded back plane',(cx,390,7.6),(28,.15,5.6),p['dark'])
c.collection('282_Gym_Entrance_Stairs_And_Doors')
u.stairs('Gym broad rose granite entrance',(-76,377.9,0),(-76,382,1.08),16,6,red,False)
c.box('Gym entrance landing',(-76,384,1.0),(17,4.2,.16),red)
for xx in [-86,-66]:
    c.box('Gym stair planted side wall',(xx,380,.58),(3.8,4.9,1.16),red)
    l.shrub('Gym entry clipped planting',xx,380,.95,1.48,320+int(abs(xx)),base=1.13)
for xx in [-85,-67]:c.box('Gym recessed porch pier',(xx,384,2.95),(.5,4.0,3.75),clad)
c.box('Gym porch soffit',(cx,384,4.65),(18,4.6,.24),clad)
for xx in [-82,-76,-70]:c.box('Gym porch recessed light',(xx,384,4.51),(.22,.22,.035),p['white'])
for xx in [-82,-70]:c.box('Gym entrance glazed sidelight',(xx,386.2,2.62),(3.8,.04,3.08),glass)
for xx in [-78,-74]:c.box('Gym closed entrance glass door',(xx,386.2,2.62),(3.75,.05,3.08),p['dark'])
for xx in [-84,-80,-76,-72,-68]:c.box('Gym door aluminium jamb',(xx,386.13,2.68),(.085,.10,3.2),white)
for z in [1.09,3.7,4.20]:c.box('Gym entrance aluminium transom',(cx,386.12,z),(16,.10,.08),white)
for xx in [-76.23,-75.77]:c.rod('Gym stainless door pull',(xx,386.04,2.0),(xx,386.04,2.65),.019,p['steel'])
c.collection('283_Gym_Roof_And_Facade_Detail')
roof=c.material('Gym pale grey standing seam roof',(.46,.51,.49),.49,.37)
v=[]
for i in range(65):
    x=cx-24.6+49.2*i/64;z=18.0+1.20*math.sin(math.pi*i/64)
    v.extend([(x,y0-.65,z),(x,y1+.65,z)])
c.mesh('Gym gently barrel curved roof ESTIMATED',v,[(2*i,2*i+2,2*i+3,2*i+1) for i in range(64)],roof)
for yy in [y0,y1]:
    gv=[]
    for i in range(65):
        x=cx-24+48*i/64
        z=18+1.20*math.sin(math.pi*(x-(cx-24.6))/49.2)
        gv.extend([(x,yy,17.87),(x,yy,z)])
    c.mesh('Gym curved gable closure under roof ESTIMATED',gv,[(2*i,2*i+2,2*i+3,2*i+1) for i in range(64)],clad)
for xx in [cx-24,cx+24]:
    c.box('Gym continuous eave closure',(xx,407,17.99),(.28,50,.25),clad)
for i in range(65):
    x=cx-24.6+49.2*i/64;z=18+1.2*math.sin(math.pi*i/64)
    c.rod('Gym roof standing seam',(x,y0-.65,z+.025),(x,y1+.65,z+.025),.025,white,sides=6)
for y in [384,394,404,414,424,430]:
    s.beam('Gym upper hall truss lower chord',(-99,y,15.65),(-53,y,15.65),.12,.12,white)
    for i in range(12):
        a=-99+i*46/12;b=a+46/12;z=17.4+1.1*math.sin(math.pi*(i+.5)/12)
        s.beam('Gym clerestory visible diagonal truss',(a,y,15.65),((a+b)/2,y,z),.085,.085,white)
        s.beam('Gym clerestory visible reverse truss',((a+b)/2,y,z),(b,y,15.65),.085,.085,white)
for xx in [-100.3,-51.7]:
    for yy in [385,428]:
        c.rod('Gym external downpipe',(xx,yy,.4),(xx,yy,17.5),.06,white,sides=10)
        for z in [2,6,10,14]:c.box('Gym downpipe bracket',(xx,yy,z),(.19,.16,.045),p['steel'])
for xx in [-94,-58]:
    o=c.box('Gym front security floodlight',(xx,381.73,11.1),(.4,.2,.28),white,.02);o.rotation_euler.x=.3
c.collection('284_Gym_Shaded_Entrance_Landscape')
proto=[sc.objects['Rongyu spreading old banyan connected trunks roots and twigs'],sc.objects['Rongyu spreading old banyan attached broadleaf canopy']]
for xx,yy,scale in [(-91,374.5,.45),(-61,374.5,.45),(-104,391,.75),(-48,400,.72),(-105,419,.75)]:
    n.duplicate_tree(proto,xx,yy,.45,scale)
    c.box('Gym banyan raised square tree pit',(xx,yy,.14),(3.2,3.2,.28),p['stone'])
    c.box('Gym banyan pit soil',(xx,yy,.29),(2.92,2.92,.06),soil)
for xx in [-97,-55]:
    l.bench(xx,373,math.pi/2)
    s.slit_lamp(xx,379)
c.collection('288_Gym_Review_Cameras')
c.camera('129_Gym_entry_forecourt',(-76,365,1.7),(-76,383,8),22)
c.camera('130_Gym_louvres_and_steps',(-69,373,1.7),(-78,384,5.1),24)
c.camera('131_Gym_side_and_roof',(-125,357,42),(-76,405,9),31)
c.camera('132_Gym_track_connection',(-175,365,105),(-68,352,0),34)
for obj in set(bpy.data.objects)-before:
    if obj.type=='MESH' and clad.name in [m.name for m in obj.data.materials]:h.vertical_uv(obj)
h.save(32,'Gym exterior and recessed entrance from 392/357: ivory cladding, green high windows, wide ventilation louvres, rose stairs, small tiled forecourt and trees. Roof depth and unseen side modules estimated. No delivered indoor sports hall.',[392,357,347,348],'129_Gym_entry_forecourt')
