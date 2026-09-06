"""v013: Daosi Qian Road, shaded curve, flower bridge and west-side junction.
Source nodes 372-375. The west gate itself is a separate future asset.
"""
import bpy,sys,math,random
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).parent))
import campus_common as c
import north_common as n
import north_landscape as l
import south_detail_common as s
sc=bpy.data.scenes['WZMS_Campus'];c.activate(sc)
p=n.palette();asphalt=s.mottled('Daosi dark worn asphalt',[(.075,.085,.088),(.17,.18,.17)],2.5)
concrete=s.mottled('Daosi pale bridge concrete',[(.34,.34,.30),(.53,.52,.46)],1.8)
white=c.material('Daosi aged ivory lane paint',(.72,.71,.61),.88)
ground=s.mottled('Daosi dry shaded lawn',[(.055,.10,.018),(.21,.25,.065)],1.2)
curve=s.smooth_path([(-50,47),(-59,48),(-67,59),(-70,72),(-69,86)],18)
north=s.smooth_path([(-69,128),(-69,136),(-58,145),(-30,146),(-20,146)],18)
def deck(p):return -.01+.34*math.sin(math.pi*(p.y-86)/42)
bridge=[(-69,86+j*.5) for j in range(85)]
c.collection('100_Daosi_Road_Surface_And_Banks')
c.box('Daosi southern wooded plot',(-66,64.5,-.24),(31,45,.40),ground)
c.box('Daosi northern junction land',(-48,144,-.30),(66,26,.55),ground)
s.ribbon('Daosi continuous shaded asphalt curve',curve,5.4,asphalt)
s.ribbon('Daosi bridge raised concrete deck',bridge,5.4,concrete,deck,.44)
s.ribbon('Daosi north avenue and Nantian reserved connection',north,5.4,asphalt)
for yy in [86,128]:c.box('Daosi bridgehead overlapping expansion joint',(-69,yy,-.12),(5.4,.24,.22),concrete)
for points in [curve,north]:
 for side in [-1,1]:s.ribbon('Daosi continuous pale kerb',s.offset(points,side*2.8),.20,p['stone'],.025,.18)
 s.ribbon('Daosi continuous pedestrian lane line',s.offset(points,.7),.065,white,-.004,.003)
# White dashed vehicle guidance next to the continuous line on the open bridge.
s.ribbon('Daosi bridge continuous lane line',[(-68.3,y) for _,y in bridge],.065,white,lambda p:deck(p)+.006,.003)
for y in range(88,127,4):
 pts=[(-69.3,y+j*.25) for j in range(9)]
 s.ribbon('Daosi bridge broken centre line',pts,.075,white,lambda p:deck(p)+.006,.003)
tile=n.paving('Daosi ribbed grey transition paving',(.31,.33,.30),(.9,.105),.008)
for yy in [83.5,130.5]:
 c.box('Daosi bridgehead ribbed transition',(-69,yy,-.004),(5.35,4.2,.016),tile)
 s.segment('Daosi bridgehead line',(-68.3,yy-2.1),(-68.3,yy+2.1),.065,white,.008,.003)
for yy in [89,100,113,125]:
 c.box('Daosi underbridge cross girder',(-69,yy,deck(Vector((-69,yy)))-.59),(7.5,.60,.44),p['stone'])
 for xx in [-71,-67]:c.box('Daosi bridge support pier',(xx,yy,-1.30),(.5,.7,1.45),p['stone'])
# West water extension meets the existing lake exactly at x=-90, no coplanar overlay.
water=c.material('Campus lake water',(.11,.16,.085),.17,.1)
c.box('Daosi west channel water',(-98,108,-1.18),(16,74,.06),water)
c.box('Daosi west channel bed',(-98,108,-2.7),(16,74,.14),p['seam'])
c.collection('101_Daosi_Flower_Bridge_Balustrades')
iron=c.material('Daosi dark wrought iron',(.020,.026,.025),.48,.60)
pink=c.material('Daosi pink impatiens',(.58,.065,.25),.65)
cream=c.material('Daosi pale impatiens',(.75,.56,.48),.67)
leaves=c.foliage_materials('Daosi border flowers leaf ')
rng=random.Random(1374)
for side in [-1,1]:
 x=-69+side*3.25
 pts=[(x,y) for _,y in bridge]
 s.ribbon('Daosi weathered flower trough outer wall',s.offset(pts,side*.49),.18,concrete,lambda p:deck(p)+.50,.72)
 s.ribbon('Daosi weathered flower trough inner wall',s.offset(pts,-side*.49),.18,concrete,lambda p:deck(p)+.42,.64)
 s.ribbon('Daosi flower bed soil',pts,.84,c.material('Daosi potting soil',(.047,.034,.018)),lambda p:deck(p)+.36,.08)
 v,f,ids=[],[],[];fv,ff,fi=[],[],[]
 for i in range(5000):
  xx=x+rng.uniform(-.39,.39);yy=rng.uniform(86,128);z=deck(Vector((xx,yy)))+.38+rng.uniform(.03,.22)
  c.leaf_data(v,f,ids,(xx,yy,z),rng.uniform(.06,.12),rng,rng.randrange(5))
  if i%3==0:
   for k in range(5):
    ang=k*math.tau/5;st=len(fv);rad=.055
    fv.extend([(xx,yy,z+.04),(xx+rad*math.cos(ang-.5),yy+rad*math.sin(ang-.5),z+.075),(xx+rad*1.2*math.cos(ang),yy+rad*1.2*math.sin(ang),z+.09),(xx+rad*math.cos(ang+.5),yy+rad*math.sin(ang+.5),z+.075)])
    ff.append((st,st+1,st+2,st+3));fi.append(i%2)
 c.mesh('Daosi dense bridge flower foliage',v,f,leaves,ids);c.mesh('Daosi individual pink white flowers',fv,ff,[pink,cream],fi)
 # Tall pointed arches behind the flowers, batched into one actual metal mesh.
 v,f=[],[];xx=x+side*.36
 for yy in [86+i*.46 for i in range(92)]:
  zz=deck(Vector((xx,yy)))+.42
  points=[(xx,yy-.23+.46*k/12,zz+.70*math.sin(math.pi*k/12)) for k in range(13)]
  for a,b in zip(points,points[1:]):c.tube_data(v,f,a,b,.012,.012,5)
 for yy in range(86,129,3):
  zz=deck(Vector((xx,yy)))+.40;c.tube_data(v,f,(xx,yy,zz),(xx,yy,zz+1.0),.027,.027,8)
 c.mesh('Daosi pointed arch bridge railing',v,f,iron)
c.collection('102_Daosi_Shade_Trees_And_Gardens')
for j,(x,y) in enumerate([(-54,43),(-59,54),(-61,62),(-63,74),(-65,81),(-76,77),(-77,65),(-72,54),(-70,44),(-75,133),(-60,137),(-50,140),(-41,140),(-30,139),(-22,140)]):
 s.tree(x,y,.90+(j%3)*.07,j*.74)
 c.rod('Daosi tree trunk limewash',(x,y,.02),(x+.02,y,1.15),.30*(.90+(j%3)*.07),c.material('Daosi limewash',(.63,.66,.58)),.275,12)
for x,y,w,d in [(-60,63,3,13),(-76,70,3,16),(-55,141,10,2),(-25,140,7,2)]:
 c.planting('Daosi dense garden groundcover',(x,y),(w,d),.27,int(x*x+y),140)
for j,(x,y) in enumerate([(-60,59),(-62,78),(-76,81),(-52,141),(-32,140)]):l.shrub('Daosi sculpted shrub',x,y,1.2,1.0,2200+j)
# Tree-side stones and stainless utility boxes at the southern bridgehead.
rock=s.mottled('Daosi warm rough name stone',[(.28,.21,.12),(.48,.38,.24)],4)
l.ellipsoid('Daosi irregular landscape stone',(-63.1,81,.46),(1.6,.65,.55),rock,9,5)
for x in [-61,-59.8]:
 c.box('Daosi stainless utility cabinet',(x,80,.72),(.75,.45,1.42),p['steel'],.02)
 c.box('Daosi cabinet door seam',(x,79.769,.72),(.69,.009,1.29),p['seam'])
 c.box('Daosi cabinet recessed door',(x,79.759,.72),(.65,.009,1.25),p['steel'])
for x,y in [(-61.4,54),(-73.6,72),(-62.7,83),(-74,131),(-43,141)]:s.slit_lamp(x,y)
c.collection('103_Daosi_White_Parking_Canopy')
c.box('Daosi parking hardstanding',(-84,58,-.15),(13,30,.28),concrete)
for yy in range(45,74,3):s.segment('Daosi parking bay divider',(-89,yy),(-80,yy),.055,white,-.004,.003)
for yy in [46,52,58,64,70]:
 c.box('Daosi carport mast foot',(-79.4,yy,.42),(.50,.50,.84),p['white'])
 c.rod('Daosi carport tall post',(-79.4,yy,0),(-79.4,yy,5.3),.10,p['white'],.075,12)
 s.beam('Daosi carport swept outrigger',(-79.4,yy,2.95),(-88.7,yy,3.5),.18,.34,p['white'])
 c.rod('Daosi carport tension stay',(-79.4,yy,5.1),(-86.5,yy,3.37),.025,p['white'])
 c.rod('Daosi carport diagonal brace',(-79.4,yy,.8),(-82,yy,3.1),.045,p['white'])
roof=c.material('Daosi white tensile roofing',(.70,.70,.62),.78)
v,f=[],[]
for j in range(49):
 yy=45+j*.55
 for i in range(17):
  t=i/16;v.append((-79.2-9.5*t,yy,3.0+.5*t-.12*math.sin(math.pi*t)))
for j in range(48):
 for i in range(16):a=j*17+i;f.append((a,a+1,a+18,a+17))
c.mesh('Daosi continuous gently curved carport membrane',v,f,roof)
c.collection('104_Daosi_Bridgehead_Furniture')
for y in [87,126]:
 x=-72.5;c.rod('Daosi street light mast',(x,y,0),(x,y,6),.055,iron,.036,12)
 c.rod('Daosi street light arm',(x,y,5.4),(x+1,y,5.8),.036,iron)
 c.box('Daosi streetlight LED head',(x+1.05,y,5.79),(.63,.3,.095),p['white'],.025)
 for side,mat in [(-1,c.material('Daosi red banner',(.4,.025,.023))), (1,c.material('Daosi blue banner',(.014,.14,.35)))]:
  c.box('Daosi historic coloured lamp banner',(x+side*.36,y,3.75),(.6,.025,1.25),mat)
for yy in [81,133]:
 c.rod('Daosi round utility cover',(-69.8,yy,-.025),(-69.8,yy,-.007),.29,p['seam'],sides=32)
 for k in range(5):s.segment('Daosi utility cover grooves',(-70.03,yy-.16+k*.08),(-69.57,yy-.16+k*.08),.012,p['steel'],-.003,.003)
# Short lakeside path off the bridgehead with sagging chains.
s.segment('Daosi waterside sidepath',(-66,83),(-53,79),1.6,tile)
for j in range(9):
 x=-66+j*1.5;y=81.8-j*.46
 c.box('Daosi waterfront granite chain post',(x,y,.28),(.18,.18,.56),p['stone'],.012)
 if j<8:
  v,f=[],[]
  for k in range(12):
   t=k/12;u=(k+1)/12
   c.tube_data(v,f,(x+1.5*t,y-.46*t,.44-.15*math.sin(math.pi*t)),(x+1.5*u,y-.46*u,.44-.15*math.sin(math.pi*u)),.012,.012,5)
  c.mesh('Daosi sagging waterfront chain',v,f,iron)
c.collection('105_Daosi_Visible_Context_ESTIMATED')
# Elevated road is visible from 373/374; geometry is environmental context only.
for xx in [-101,-113]:
 c.box('Daosi context elevated road deck',(xx,96,9.0),(9.5,100,.85),p['stone'])
 for yy in range(50,147,24):
  c.box('Daosi context highway pier',(xx,yy,4.1),(1.3,1.8,8.2),p['stone'])
  c.box('Daosi context highway pier cap',(xx,yy,8.3),(8,1.7,.6),p['stone'])
 for side in [-1,1]:
  c.box('Daosi context roadside parapet',(xx+side*4.65,96,9.75),(.22,100,.8),p['white'])
  for yy in range(46,146,3):c.box('Daosi context parapet glazing',(xx+side*4.66,yy,9.88),(.23,2.3,.42),p['glass'])
# Four-storey frontage at 375, limited to the visible road edge, separate scope tag.
n.academic_wing('Daosi junction four storey context',-42,156,26,10,4,-1,False)
for yy in [149.5]:
 for x in [-54,-47,-39,-32]:n.palm('Daosi junction roadside palm',x,yy,7.5,int(x*x))
c.box('Daosi blank outdoor display frame',(-56.5,149,1.9),(4.0,.3,2.4),p['stone'])
c.box('Daosi dark outdoor display',(-56.5,148.83,1.9),(3.65,.025,2.07),p['dark'])
# Reserve a real paved branch for the separately scheduled west gate.
s.segment('Daosi west gate reserved approach',(-69,136),(-81,136),4,asphalt)
c.collection('108_Daosi_Cameras')
c.camera('49_Daosi_shaded_curve',(-65,56,1.72),(-70,78,1.5),27)
c.camera('50_Daosi_flower_bridge',(-69,87,1.76),(-69,126,1.5),30)
c.camera('51_Daosi_lakeside_lookback',(-69,105,1.9),(-24,60,9),29)
c.camera('52_Daosi_north_junction',(-66,139,1.72),(-40,147,3),27)
c.camera('53_Daosi_overview',(-132,19,86),(-54,97,0),39)
sc.camera=sc.objects['49_Daosi_shaded_curve']
sc['scope']='Existing campus and tennis retained; Daosi curve, parking canopy, flower bridge, north junction; west gate is reserved, not delivered.'
c.save(c.ROOT/'models/campus/WZMS_Campus_v013.blend','v0.0.13',[119232372,119232373,119232374,119232375])
print('WZMS_BUILD_COMPLETE v0.0.13',flush=True)
