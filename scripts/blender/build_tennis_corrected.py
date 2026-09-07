"""v035: four parallel tennis courts, two on either side of a dividing practice wall."""
import bpy,sys,math,json
from pathlib import Path
from mathutils import Vector,Matrix
sys.path.insert(0,str(Path(__file__).parent))
import campus_common as c,north_common as n,north_landscape as l
import south_detail_common as s,island_common as h
sc=bpy.data.scenes['WZMS_Campus'];c.activate(sc);p=n.palette()
bpy.context.view_layer.update()
source=[o for o in bpy.data.collections['90_Tennis_Courts_And_Access'].objects if o.name.startswith(('Tennis violet','Tennis singles','Tennis baseline','Tennis service','Tennis centre'))]
source += [o for o in bpy.data.collections['92_Tennis_Nets_And_Practice_Wall'].objects if not ('wall' in o.name.lower())]
c.collection('311_Tennis_Additional_Two_Courts')
for old in source:
 obj=old.copy();obj.name='East pair '+old.name;c.COL.objects.link(obj)
 obj.matrix_world=Matrix.Translation((36,0,0))@old.matrix_world
 obj['source_component']=old.name;obj['layout_authority']='User correction 2026-09-08'
retired=[o.name for o in bpy.data.collections['92_Tennis_Nets_And_Practice_Wall'].objects if 'wall' in o.name.lower()]
for old in bpy.data.collections['93_Tennis_Lights_And_Furniture'].objects:
 if not old.name.startswith(('Tennis timber planter','Tennis clipped border')):continue
 bounds=[old.matrix_world@Vector(v) for v in old.bound_box];mid=sum(bounds,Vector())/8
 if mid.x>101.1:
  obj=old.copy();obj.name='East outer border '+old.name;c.COL.objects.link(obj)
  obj.matrix_world=Matrix.Translation((36,0,0))@old.matrix_world;retired.append(old.name)
# Replace the old east fence by the solid divider and real end passages.
for o in bpy.data.collections['91_Tennis_Blue_Fencing'].objects:
 bounds=[o.matrix_world@Vector(v) for v in o.bound_box]
 if min(v.x for v in bounds)>100.8:retired.append(o.name)
# The old image-estimated utility peninsula occupied the missing pair's footprint.
# Shift that complete assembly north, preserving its editable details and reconnecting Heyu.
c.collection('315_Tennis_Shuinan_Relocated_Peninsula')
for label in ['121_Shuinan_Peninsula_And_Path','122_Shuinan_Grey_Utility_Room','123_Shuinan_Trees_And_Furniture']:
 for old in bpy.data.collections[label].objects:
  obj=old.copy();obj.name='Reconnected '+old.name;c.COL.objects.link(obj)
  shift=(0,16,0)
  if old.type=='MESH':
   bounds=[old.matrix_world@Vector(v) for v in old.bound_box];mid=sum(bounds,Vector())/8
   if 'Slit lamp' in old.name and abs(mid.x-104)<.4 and abs(mid.y-17.3)<.4:shift=(-2,16,0)
   if old.name.startswith('Shuinan stray tennis ball'):shift=(-2.65,.8,0)
  obj.matrix_world=Matrix.Translation(shift)@old.matrix_world
h.retire('v0.0.35',names=retired,collections=['120_Shuinan_Continuous_Bridge','121_Shuinan_Peninsula_And_Path','122_Shuinan_Grey_Utility_Room','123_Shuinan_Trees_And_Furniture'])
blue=bpy.data.materials['Tennis cyan enamel'];white=bpy.data.materials['Tennis warm white court paint']
green=bpy.data.materials['Tennis weathered sage surround'];pave=bpy.data.materials['Tennis exterior grey pavers']
c.collection('312_Tennis_Extended_Base_And_Divider')
c.box('Tennis estimated southern landscape infill',(94,-23,-.50),(98,26,.90),p['green'])
c.box('Tennis estimated east water continuation',(153,20,-1.20),(36,102,.025),bpy.data.materials['Heyu green lake water'])
c.mesh('Tennis water infill to existing diagonal shore',[(120,26,-1.18),(135,26,-1.18),(135,60,-1.18)],[(0,1,2)],bpy.data.materials['Heyu green lake water'])
c.box('Tennis east retaining bank beneath new courts',(137.25,8,-.77),(.40,36.4,1.50),p['stone'])
c.box('Four tennis east pair foundation',(119,8,-.28),(36.4,36.4,.52),p['stone'])
c.box('Four tennis east continuous green surround',(119,8,-.028),(36,36,.036),green)
c.box('Tennis middle solid dividing practice wall',(100.9,8,1.55),(.30,28,3.1),blue,.02)
c.box('Tennis divider pale concrete coping',(100.9,8,3.12),(.40,28.2,.10),p['stone'],.02)
for x in [100.742,101.058]:
 c.box('Tennis divider white net height line',(x,8,.914),(.009,27.8,.055),white)
 for y in [-1,17]:
  for z in [1.45,2.0]:c.box('Tennis divider target horizontal',(x,y,z),(.01,.55,.035),white)
  for dy in [-.275,.275]:c.box('Tennis divider target vertical',(x,y+dy,1.725),(.01,.035,.55),white)
for y in [-8,24]:s.ribbon('Tennis level passage around wall end',[(97,y),(105,y)],2.6,green,-.012,.12)
for a,b in [((101,-10),(137,-10)),((101,26),(102.6,26)),((105.4,26),(137,26)),((137,-10),(137,26))]:s.wire_fence('Four tennis east blue enclosure',a,b,4,blue)
c.collection('316_Tennis_Heyu_Reconnected_Waterside_Bridge')
s.bridge('Shuinan reconnected water and land deck',[(87,42),(104,42),(104,32)],2.4,miter=True,open_land_end=True)
s.bridge('Shuinan new northern tennis gateway',[(104,32),(104,26)],2.4)
s.ribbon('Shuinan relocated utility branch',[(104,39),(106,39)],2.4,bpy.data.materials['Waterside fine rectangular granite'],-.01,.20)
c.collection('313_Tennis_East_Lights_And_Border')
for y in [-9.5,8,25.5]:
 x=136.85
 c.rod('East tennis floodlight pole',(x,y,0),(x,y,7),.052,blue,.035,12)
 c.rod('East tennis floodlight arm',(x,y,6.83),(x-.42,y,6.83),.028,blue)
 c.box('East tennis floodlight head',(x-.42,y,6.79),(.5,.34,.09),p['dark'],.025)
 c.box('East tennis floodlight diffuser',(x-.42,y,6.732),(.43,.27,.014),white)
for y in [-4,10]:l.bench(135.8,y,math.pi/2)
for x,y,w,d in [(119,-12,37,3),(138.5,8,3,39)]:c.box('Four tennis new landscape border',(x,y,-.22),(w,d,.38),p['green'])
for x,y in [(112,-13),(126,-13),(139,-6),(139,18)]:s.tree(x,y,.72,(x+y)*.1)
c.collection('314_Tennis_Correction_Cameras')
c.camera('144_Tennis_four_overview',(162,-38,67),(101,8,0),40)
c.camera('145_Tennis_divider_end',(95,-8,1.7),(100.9,12,1.8),24)
c.camera('146_Tennis_new_pair_ground',(130,-6,1.7),(108,20,1.6),25)
c.camera('147_Tennis_four_top_plan',(101,8,112),(101,8,0),40)
c.camera('147b_Tennis_Heyu_reconnected',(143,65,43),(105,31,0),37)
sc['tennis_count']=4;sc['tennis_grid']='two parallel pairs separated by a solid wall with end passages'
h.save(35,'User correction: preserve original two parallel tennis courts and add two alongside to the east, same orientation and style. Replace short practice wall by 28m estimated solid divider with north/south passages; retain Heyu island and original entrance. Move the old estimated Shuinan utility peninsula north 16m to clear the added courts and rebuild its connected bridge. Court count and separation user-confirmed; positions, relocated shoreline and wall length remain design estimates.',[359,348,347,364,365],'144_Tennis_four_overview')
