"""v036 gym interiors: photographed table tennis hall and upper multi-sport hall."""
import bpy,sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import campus_common as c,north_common as n,south_detail_common as s
import island_common as h,culture_common as k,indoor_common as i,sports_common as q
sc=bpy.data.scenes['WZMS_Campus'];c.activate(sc);p=n.palette()
replace=[]
for o in sc.objects:
 if o.name.startswith(('Gym longitudinal lower cladding','Gym closed entrance glass door','Gym stainless door pull','Gym louvre shaded back plane')):replace.append(o.name)
 elif o.name.startswith('Gym door aluminium jamb') and abs(o.location.x+76)<.1:replace.append(o.name)
glass_sources=[o for o in sc.objects if o.name.startswith(('Gym high clerestory glass','Gym rear high windows','Gym front clerestory band','Gym entrance glazed sidelight'))]
c.collection('320_Gym_Interior_Shell_And_Open_Doors')
# Trim only foliage geometry that crosses the enclosed gym volume.
from mathutils import Vector
import bmesh
bpy.context.view_layer.update()
for old in list(sc.objects):
 if old.type!='MESH' or not old.name.startswith('Rongyu spreading old banyan'):continue
 if not (-112<old.location.x<-40 and 370<old.location.y<440):continue
 inside=lambda v:-99.85<v.x<-52.15 and 386<v.y<431.8 and 1.1<v.z<18
 if not any(inside(old.matrix_world@v.co) for v in old.data.vertices):continue
 obj=old.copy();obj.data=old.data.copy();obj.name='Gym wall-cleared '+old.name;c.COL.objects.link(obj)
 bm=bmesh.new();bm.from_mesh(obj.data)
 verts=[v for v in bm.verts if inside(obj.matrix_world@v.co)]
 bmesh.ops.delete(bm,geom=verts,context='VERTS');bm.to_mesh(obj.data);bm.free();replace.append(old.name)
for old in glass_sources:
 obj=old.copy();obj.data=old.data.copy();obj.name='Interior clear '+old.name;c.COL.objects.link(obj)
 obj.data.materials.clear();obj.data.materials.append(i.glass('Gym daylight clear glazing'));replace.append(old.name)
h.retire('v0.0.36',names=replace)
white=c.material('Gym interior warm white plaster',(.70,.73,.69),.78)
blue=c.material('Gym interior photographed blue wainscot',(.014,.30,.46),.46)
teal=c.material('Gym ground hall worn teal floor',(.055,.28,.245),.31);c.noise(teal,70,.22,.004)
grey=n.paving('Gym foyer polished grey terrazzo',(.39,.43,.40),(.6,.6),.003)
wood=n.paving('Gym upper maple sports floor',(.55,.33,.14),(.12,1.2),.0015)
bs=wood.node_tree.nodes['Principled BSDF'];bs.inputs['Roughness'].default_value=.27
orange=c.material('Gym photographed orange gallery fascia',(.67,.065,.015),.55)
dark=c.material('Gym black rail and skirting',(.025,.035,.035),.50,.3)
for x in [-100,-52]:
 c.box('Gym ground solid sill',(x,407,1.50),(.25,50,.84),white)
 c.box('Gym ground window lintel',(x,407,5.32),(.25,50,1.04),white)
 c.box('Gym upper blue wall',(x,407,8.15),(.25,50,4.14),blue)
 c.box('Gym upper white wall band',(x,407,10.38),(.25,50,.34),white)
 for y in range(384,432,4):i.window_x('Gym ground daylight window',x,y,3.37,3.7,2.88)
 for y in range(382,433,4):c.box('Gym ground window structural pier',(x,y,3.4),(.32,.26,3.05),white)
for x in [-79.5,-72.5]:
 i.window_x('Gym open entrance glass leaf',x,387.6,2.62,2.65,3.08)
 c.rod('Gym open entrance pull',(x+.065,387,2),(x+.065,387,2.65),.019,p['steel'])
c.box('Gym foyer floor',(-76,389.8,1.039),(47.6,7.3,.10),grey)
c.box('Gym teal table tennis floor',(-76,412.5,1.044),(47.6,37,.09),teal)
for x in [-99.4,-52.6]:c.box('Gym black floor edge',(x,412.5,1.089),(.38,37,.014),dark)
for y in [394,430.6]:c.box('Gym black floor end',(-76,y,1.089),(46.8,.38,.014),dark)
for x in [-99.05,-52.95]:c.box('Gym yellow safety edge',(x,412.5,1.098),(.13,36.5,.012),p['yellow'] if 'yellow' in p else c.material('Gym yellow boundary',(.7,.50,.11),.6))
# Upper slab omits the stair opening. Its lower surface forms the real ground ceiling.
for x,y,w,d in [(-76,413.8,47.6,35.8),(-81.8,391,36,10),(-53.8,391,3.6,10)]:
 obj=c.box('Gym upper floor with stair void',(x,y,5.93),(w,d,.30),wood);obj.data.materials.append(white)
 for face in obj.data.polygons:face.material_index=0 if face.normal.z>.5 else 1
for y in [397,405,413,421,429]:
 c.box('Gym ground transverse ceiling beam',(-76,y,5.55),(47.6,.4,.46),white)
 for x in [-90,-80,-70]:
  c.box('Gym table hall white column',(x,y,3.50),(.62,.62,4.84),white)
  c.box('Gym table hall blue column base',(x,y,1.84),(.645,.645,1.52),blue)
for x in [-94,-85,-76,-66,-57]:
 for y in [390,401,409,417,425]:
  if x>-64 and y<397:continue
  i.tube_light('Gym ground fluorescent pair',x,y,5.34,1.7,110)
c.collection('321_Gym_Table_Tennis_And_Trophy_Foyer')
for x in [-94.5,-85.5,-76.5,-66.5,-57]:
 for y in [401,409,417,425]:i.pingpong(x,y,1.08)
for y in [400,414,427]:
 c.box('Gym framed photo timber backing',(-52.2,y,3.4),(.10,8,1.85),c.material('Gym photo board honey timber',(.34,.16,.07),.65))
 # These are original photographed framed pictures, sampled from reference 393/L.
 for j in range(3):
  yy=y-2.5+j*2.5
  c.box('Gym photo frame',(-52.27,yy,3.42),(.06,1.1,.80),p['stone'])
  i.photo_panel('Gym source sports picture',393,'l',[(-52.306,yy+.48,3.08),(-52.306,yy-.48,3.08),(-52.306,yy-.48,3.76),(-52.306,yy+.48,3.76)],[(.921,.594),(.955,.594),(.955,.630),(.921,.630)])
for x in [-95,-91,-87]:
 c.box('Gym trophy cabinet plinth',(x,388.6,1.38),(3.5,.7,.60),p['stone'])
 for z in [1.71,2.35,3.0]:
  c.box('Gym trophy glass shelf',(x,388.6,z),(3.4,.62,.025),i.glass())
  for dx in [-1.2,-.6,0,.6,1.2]:i.trophy(x+dx,388.6,z+.025,.85+abs(dx)*.2)
 i.window_y('Gym trophy cabinet front',x,388.20,2.50,3.5,2.18)
 c.box('Gym trophy cabinet back',(x,389.0,2.50),(3.5,.08,2.2),white)
 i.tube_light('Gym trophy case LED',x,388.6,3.68,2.6,40)
c.collection('322_Gym_Stairs_And_Upper_Gallery')
k.stairs('Gym internal first flight',(-58,388,1.08),(-58,393.6,3.58),2.6,14,grey)
c.box('Gym middle stair landing',(-60,394.6,3.48),(6.6,2.0,.20),grey)
k.stairs('Gym internal return flight',(-62,393.6,3.58),(-62,388,6.08),2.6,14,grey)
c.box('Gym upper stair landing',(-62,387.2,5.98),(4.0,1.6,.20),wood)
k.rail('Gym stair void guard',[(-64,388,6.08),(-64,396,6.08),(-55.6,396,6.08),(-55.6,386.5,6.08)])
# Tiered gallery along the rear, with a dedicated central stair and clear cross-aisle.
for j in range(8):
 y=426.7+j*.52;z=6.08+(j+1)*.32
 for x in [-88.5,-63.5]:
  c.box('Gym rear gallery concrete tier',(x,y,(z+5.88)/2),(21,.52,z-5.88),grey)
  c.box('Gym gallery orange riser',(x,y-.264,z-.15),(21,.018,.30),orange)
k.stairs('Gym rear gallery central aisle',(-76,426.44,6.08),(-76,430.6,8.64),2.0,16,grey)
c.box('Gym gallery upper landing',(-76,431,8.54),(47,1,.20),grey)
k.rail('Gym rear gallery guard',[(-99,431.4,8.64),(-53,431.4,8.64)])
c.collection('323_Gym_Upper_Multi_Sport_Hall')
paint=c.material('Gym indoor court white paint',(.83,.84,.76),.6)
for x in [-90,-62]:q.flat_line('Gym upper basketball baseline',[(x,406.5),(x,421.5)],.05,paint,6.083)
for y in [406.5,421.5]:q.flat_line('Gym upper basketball sideline',[(-90,y),(-62,y)],.05,paint,6.083)
q.flat_line('Gym upper basketball halfway',[(-76,406.5),(-76,421.5)],.05,paint,6.083)
q.flat_arc('Gym upper basketball centre circle',-76,414,1.8,0,math.tau,paint,6.083)
for sign in [-1,1]:
 x=-76+sign*11.1
 c.box('Gym upper blue key',(x,414,6.081),(5.8,4.9,.002),blue)
 q.flat_line('Gym upper free throw',[(-76+sign*8.2,411.55),(-76+sign*8.2,416.45)],.05,paint,6.084)
 for y in [411.55,416.45]:q.flat_line('Gym upper key side',[(-76+sign*14,y),(-76+sign*8.2,y)],.05,paint,6.084)
 i.hoop('Gym upper basketball',-76+sign*12.8,414,6.08,-sign*math.pi/2)
 q.flat_arc('Gym upper free throw circle',-76+sign*8.2,414,1.8,0,math.tau,paint,6.084)
 delta=math.acos(6.6/6.75);a0,a1=(math.pi/2+delta,3*math.pi/2-delta) if sign>0 else (-math.pi/2+delta,math.pi/2-delta)
 q.flat_arc('Gym upper three point arc',-76+sign*12.425,414,6.75,a0,a1,paint,6.084)
 join=-76+sign*(12.425-math.sqrt(6.75**2-6.6**2))
 for y in [407.4,420.6]:q.flat_line('Gym upper three point corner',[(-76+sign*14,y),(join,y)],.05,paint,6.084)
c.text('Gym observed floor school name','温 州 中 学',(-76,404.7,6.084),.67,dark,(0,0,0))
# Two badminton practice rectangles clear of the stair entry.
for x in [-88,-72]:
 for y in [391.5,397.6]:q.flat_line('Gym badminton doubles sidelines',[(x-6.7,y),(x+6.7,y)],.04,paint,6.083)
 for xx in [x-6.7,x+6.7,x-1.98,x+1.98]:q.flat_line('Gym badminton cross lines',[(xx,391.5),(xx,397.6)],.04,paint,6.083)
 for yy in [391.4,397.7]:c.rod('Gym badminton portable upright',(x,yy,6.08),(x,yy,7.63),.025,blue,sides=10)
 v,f=[],[]
 for j in range(127):
  yy=391.4+j*.05;c.tube_data(v,f,(x,yy,6.87),(x,yy,7.61),.0015,.0015,4)
 for j in range(16):c.tube_data(v,f,(x,391.4,6.87+j*.049),(x,397.7,6.87+j*.049),.0015,.0015,4)
 c.mesh('Gym badminton actual black net',v,f,dark)
 c.box('Gym badminton white net tape',(x,394.55,7.625),(.025,6.3,.035),paint)
c.box('Gym photographed dark scoreboard',(-76,431.82,12.4),(10,.16,4),dark)
c.collection('324_Gym_Space_Truss_And_Lighting')
for x in range(-98,-52,4):
 for y in range(386,430,4):
  a=(x,y,15.6);b=(x+4,y,15.6);tip=(x+2,y+2,17.1)
  s.beam('Gym white space truss lower X',a,b,.065,.065,white)
  s.beam('Gym white space truss lower Y',a,(x,y+4,15.6),.065,.065,white)
  for pt in [a,b,(x,y+4,15.6),(x+4,y+4,15.6)]:s.beam('Gym space truss diagonal',pt,tip,.045,.045,white)
for x in [-94,-82,-70,-58]:
 for y in [392,404,416,428]:
  c.rod('Gym industrial pendant suspension',(x,y,15.6),(x,y,14.85),.012,dark,sides=8)
  c.rod('Gym industrial bell shade',(x,y,14.50),(x,y,14.83),.34,white,.13,24)
  c.rod('Gym industrial lamp diffuser',(x,y,14.49),(x,y,14.50),.31,i.glow(strength=6),sides=24)
  k.area('Gym upper industrial light',(x,y,14.45),750,1.0,(.94,.97,1))
c.collection('328_Gym_Indoor_Cameras')
c.camera('148_Gym_table_tennis_hall',(-60,395,2.75),(-86,418,2.8),24)
c.camera('149_Gym_trophy_foyer',(-85,386.9,2.78),(-93,388.6,2.6),25)
c.camera('150_Gym_upper_sports_hall',(-95,424,7.78),(-70,406,10),22)
c.camera('151_Gym_upper_gallery',(-76,430.5,10.34),(-76,405,9.2),23)
c.camera('152_Gym_connected_internal_stair',(-68,388,2.78),(-59,393,4.1),23)
h.save(36,'Gym visible interiors from 393/394: table-tennis hall, trophy foyer, functional estimated two-flight stair, upper wood multi-sport hall, gallery and white space truss. Internal partition positions and floor height estimated. No unseen changing rooms or toilets claimed.',[393,394,392],'150_Gym_upper_sports_hall')
