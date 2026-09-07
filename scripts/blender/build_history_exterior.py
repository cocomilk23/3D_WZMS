"""v021 school history museum exterior, inferred aerial massing and observed entrance.
The exhibit interiors (405-418) are not furnished in this exterior milestone.
"""
import bpy,sys,math,random
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).parent))
import campus_common as c,north_common as n,north_landscape as l,south_detail_common as s,culture_common as k
sc=bpy.data.scenes['WZMS_Campus'];c.activate(sc);p=n.palette()
white=c.material('History warm white exterior plaster',(.78,.77,.71),.8);c.noise(white,90,.18,.012)
roof=c.material('History dark grey metal roof',(.075,.085,.083),.52,.28)
glass=c.material('History blue green entrance glass',(.51,.75,.72),.12)
bs=glass.node_tree.nodes.get('Principled BSDF');bs.inputs['Transmission Weight'].default_value=.78;bs.inputs['IOR'].default_value=1.45
stone=n.paving('History museum grey forecourt tiles',(.47,.48,.44),(.6,.3),.005)
soil=s.mottled('History island shaded lawn',[(.075,.13,.026),(.25,.25,.065)],1.3)
bank=s.mottled('History island retaining masonry',[(.26,.28,.24),(.49,.49,.40)],3.5)
c.collection('170_History_Museum_Island_And_Approach')
outline=[];count=144
for i in range(count):
 a=i*math.tau/count;outline.append((257+24*(1+.07*math.sin(3*a))*math.cos(a),123+27*(1+.055*math.cos(4*a))*math.sin(a)))
v=[(x,y,-.025) for x,y in outline]+[(x,y,-1.85) for x,y in outline];f=[tuple(range(count)),tuple(reversed(range(count,count*2)))]
for i in range(count):j=(i+1)%count;f.append((i,j,j+count,i+count))
c.mesh('History island closed retaining bank',v,f,bank)
c.mesh('History island grass surface',[(x,y,-.022) for x,y in outline],[tuple(range(count))],soil)
s.ribbon('History bridge to entry approach',[(237,112),(247,112),(247,120),(253,120)],3.6,stone,0,.18,miter=True)
c.box('History entrance forecourt',(247,120,-.09),(10,10,.18),stone)
# A southern garden route provides an exterior inspection loop around the building.
loop=s.smooth_path([(243,112),(248,104),(263,101),(276,110),(278,128),(274,142)],12)
s.ribbon('History waterside garden inspection path',loop,2.2,stone,0,.18)
for side in [-1,1]:s.ribbon('History garden path stone edging',s.offset(loop,side*1.16),.14,p['stone'],.035,.17)
c.collection('171_History_Rectangular_White_Wing')
# Long white volume on the aerial, hollow floor structure with two window tiers.
for level in range(2):
 z=level*4.2
 c.box('History west wing floor',(257,130,z-.13),(14,24,.26),p['stone'])
 for xx in [250,264]:
  if level==0 and xx==250:
   spans=[(118.35,.7),(132.25,19.5)]
  else:spans=[(130,24)]
  for yy,w in spans:
   c.box('History long wing window sill',(xx,yy,z+.45),(.25,w,.9),white)
  c.box('History long wing lintel',(xx,130,z+3.68),(.25,24,1.0),white)
  for yy in [118,122,126,130,134,138,142]:
   c.box('History long wing facade pier',(xx,yy,z+1.98),(.34,.40,3.96),white)
  for yy in [120,124,128,132,136,140]:
   if level==0 and xx==250 and yy==120:continue
   c.box('History tall window glazing',(xx,yy,z+2.07),(.035,3.54,2.32),glass)
   for dy in [-1.8,0,1.8]:c.box('History vertical window sash',(xx,yy+dy,z+2.07),(.10,.045,2.38),p['steel'])
   for zz in [z+.90,z+2.3,z+3.23]:c.box('History window horizontal sash',(xx,yy,zz),(.10,3.6,.045),p['steel'])
 for yy in [118,142]:
  c.box('History west wing end wall',(257,yy,z+2.0),(14,.25,4),white)
  for xx in [253,257,261]:
   # Dark framed inset windows in the end wall are exterior-only detail.
   c.box('History end facade window recess',(xx,yy+(-.14 if yy==118 else .14),z+2.2),(1.65,.025,2.5),p['dark'])
   c.box('History end facade glazing',(xx,yy+(-.17 if yy==118 else .17),z+2.2),(1.50,.025,2.34),glass)
   for dz in [-1.19,0,1.19]:c.box('History end facade transom',(xx,yy+(-.2 if yy==118 else .2),z+2.2+dz),(1.55,.065,.045),p['white'])
# Sloping roof has a closed white wedge and dark roof cap with seams.
v=[(249.7,117.7,8.4),(264.3,117.7,8.4),(264.3,142.3,8.4),(249.7,142.3,8.4),(249.7,117.7,8.75),(264.3,117.7,8.75),(264.3,142.3,10.5),(249.7,142.3,10.5)]
c.mesh('History west wing sloping white roof wedge',v,[(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],white)
c.mesh('History west wing dark sloping roof',v[4:],[(0,1,2,3)],roof)
for j in range(31):
 x=249.7+j*14.6/30;c.rod('History long roof standing seam',(x,117.7,8.765),(x,142.3,10.515),.012,roof,sides=5)
c.collection('172_History_Neighbouring_Cultural_Building_Context')
# A curved lower glass frontage and two unequal dark roof volumes are legible in aerial 347.
cx,cy=264,132;rin,rout=8,12
for z in [0,4.15]:
 v,f=[],[]
 for i in range(49):
  a=math.pi*1.05+math.pi*.75*i/48
  for r in [rin,rout]:v.append((cx+r*math.cos(a),cy+r*math.sin(a),z))
 for i in range(48):f.append((i*2,i*2+1,i*2+3,i*2+2))
 c.mesh('History curved gallery slab' if z==0 else 'History curved gallery roof',v,f,p['stone'] if z==0 else roof)
for i in range(24):
 a=math.pi*1.05+math.pi*.75*i/24;b=math.pi*1.05+math.pi*.75*(i+1)/24
 aa=(cx+rout*math.cos(a),cy+rout*math.sin(a));bb=(cx+rout*math.cos(b),cy+rout*math.sin(b))
 c.mesh('History curved gallery glass panel',[(*aa,.22),(*bb,.22),(*bb,3.94),(*aa,3.94)],[(0,1,2,3)],glass)
 c.rod('History curved white structural mullion',(*aa,0),(*aa,4.15),.067,white,sides=10)
 for h in [.25,1.10,2.60,4.05]:c.rod('History curved facade horizontal band',(*aa,h),(*bb,h),.05,white,sides=10)
# Compact east wing with a gable and glazed end, positioned behind the curved link.
for z in [0,4.1,8.2]:c.box('History east wing floor',(270,135,z-.12),(12,12,.24),p['stone'])
for xx in [264,276]:
 c.box('History east wing white side wall',(xx,135,4.08),(.25,12,8.16),white)
 for y in [131,135,139]:
  for z in [2.1,6.2]:
   c.box('History east wing recessed window',(xx+(.15 if xx==276 else -.15),y,z),(.03,1.8,2.6),p['dark'])
   c.box('History east wing glazed inset',(xx+(.18 if xx==276 else -.18),y,z),(.025,1.64,2.45),glass)
for yy in [129,141]:
 c.box('History east glazed gable facade',(270,yy,4.05),(11.8,.05,8.1),glass)
 for xx in [264,266,268,270,272,274,276]:c.box('History east gable white upright',(xx,yy,4.1),(.13,.20,8.2),white)
 for z in [.15,4.1,8.2]:c.box('History east gable white transom',(270,yy,z),(12.2,.2,.16),white)
 c.mesh('History gable white infill',[(263.8,yy,8.2),(276.2,yy,8.2),(270,yy,11)],[(0,1,2)],white)
for x in [263.7,276.3]:c.mesh('History east dark gable roof',[(x,128.7,8.25),(270,128.7,11.1),(270,141.3,11.1),(x,141.3,8.25)],[(0,1,2,3)],roof)
for j in range(27):
 y=128.7+j*12.6/26
 for x in [263.7,276.3]:c.rod('History east roof standing seam',(x,y,8.27),(270,y,11.12),.012,roof,sides=5)
c.collection('173_History_Entrance_Glass_And_White_Portico')
# Source 405 looks out through clear doors and white rectangular framing.
c.box('History entrance canopy',(248,120,3.74),(5.0,7.8,.24),white)
for yy in [116.3,123.7]:c.box('History white portico pillar',(246,yy,1.8),(.38,.38,3.6),white)
for i in range(9):c.box('History exterior pergola joist',(246.1+i*.49,120,3.56),(.12,7.7,.18),white)
for yy in [118.55,121.45]:
 c.box('History entry door side clear pane',(249.86,yy,1.65),(.035,.75,3.3),glass)
 c.box('History door white side frame',(249.80,yy+(-.40 if yy<120 else .40),1.68),(.14,.10,3.36),white)
 c.box('History door open glass leaf',(250.55,yy+(.37 if yy<120 else -.37),1.61),(1.45,.03,3.20),glass)
 c.rod('History door vertical stainless handle',(250.9,yy+(.29 if yy<120 else -.29),.9),(250.9,yy+(.29 if yy<120 else -.29),1.6),.018,p['steel'])
c.box('History entry glass transom',(249.86,120,3.43),(.04,3.0,.28),glass)
blue=c.material('History entrance blue safety band',(.018,.11,.32),.45)
for yy in [118.6,121.4]:c.box('History glass door blue safety band',(249.82,yy,1.04),(.01,.62,.11),blue)
c.box('History red entrance mat',(250.6,120,.012),(2.8,1.8,.018),c.material('History red door mat',(.39,.012,.026),.95))
c.text('History museum entrance identification','校 史 馆',(245.72,120,3.9),.48,c.material('History dark bronze title',(.08,.11,.09),.43,.5),(math.pi/2,0,-math.pi/2))
# Title placement is an orientation aid inferred for the exterior, documented in delivery.
c.collection('174_History_Waterside_Planting_And_Furniture')
for i,(x,y,size) in enumerate([(239,118,.74),(241,130,.76),(245,141,.78),(254,146,.7),(274,145,.72),(280,133,.68),(276,105,.72),(259,100,.68),(246,104,.72)]):s.tree(x,y,size,i*.63)
for x,y in [(241,124),(243,136),(255,144),(274,143),(278,118),(269,105),(251,104)]:l.shrub('History island low planting',x,y,.55,1.1,int(x*y))
for x,y in [(246,116),(246,124)]:k.pot(x,y,0,.9,seed=int(x*y))
for x,y in [(242,121),(245,133),(264,103),(276,117)]:l.lamp(x,y)
for x,y in [(245,130),(268,105)]:l.bench(x,y,math.pi/2)
# Low granite posts and sagging chains on open water edges, with entry gaps.
v,f=[],[];chain=c.material('History shoreline dark chain',(.07,.09,.085),.45,.60)
for i in range(0,count,4):
 a=outline[i];b=outline[(i+4)%count]
 if a[0]<241 and 107<a[1]<118:continue
 c.box('History shoreline granite post',(*a,.38),(.18,.18,.82),p['stone'],.015)
 aa,bb=Vector(a),Vector(b)
 for j in range(12):
  t=j/12;u=(j+1)/12;pp=aa.lerp(bb,t);qq=aa.lerp(bb,u)
  c.tube_data(v,f,(*pp,.65-.20*math.sin(math.pi*t)),(*qq,.65-.20*math.sin(math.pi*u)),.012,.012,6)
c.mesh('History shoreline chain runs',v,f,chain)
c.collection('178_History_And_Cultural_Integration_Cameras')
c.camera('81_History_entrance',(239.6,115,1.7),(249,120,2.2),26)
c.camera('82_History_waterside',(285,105,5),(262,131,5),32)
c.camera('83_History_courtyard',(249,109,1.7),(264,124,3.5),25)
c.camera('84_Cultural_precinct_overview',(336,35,130),(183,137,3),43)
sc.camera=sc.objects['84_Cultural_precinct_overview'];sc['scope']='Culture batch: library exterior and supported halls, mathematics exterior, Jiushan links, white history museum exterior and adjacent dark-roof cultural-building context. Building attribution, back elevations and exact footprints remain estimated; exhibits and full Meihua island deferred.'
c.save(c.ROOT/'models/campus/WZMS_Campus_v021.blend','v0.0.21',[119232347,119232348,119232405])
print('WZMS_BUILD_COMPLETE v0.0.21',flush=True)
