"""v039: photographed dining floor, fixed blue stools and white table partitions."""
import bpy,sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import campus_common as c,north_common as n,south_detail_common as s
import island_common as h,culture_common as k,indoor_common as i
sc=bpy.data.scenes['WZMS_Campus'];c.activate(sc);p=n.palette()
ret=[o.name for o in sc.objects if o.name.startswith(('Visible dining','Visible table leg','Canteen queue','Canteen entrance red queue strap'))]
c.collection('350_Canteen_Interior_Finish_And_Daylight')
for old in list(bpy.data.collections['71_Canteen_Ground_Floor_Glazing'].objects):
 if old.name.startswith(('Canteen long window glass','Canteen south glass door and window','Canteen south door sidelight','Canteen south door overlight')):
  obj=old.copy();obj.data=old.data.copy();obj.name='Dining clear '+old.name;c.COL.objects.link(obj)
  obj.data.materials.clear();obj.data.materials.append(i.glass('Canteen indoor daylight glazing'));ret.append(old.name)
h.retire('v0.0.39',names=ret)
white=c.material('Canteen interior clean warm white',(.78,.79,.74),.65)
cream=n.paving('Canteen cream ceramic dining tiles',(.61,.54,.41),(.60,.60),.002)
blue=c.material('Canteen photographed cyan stool plastic',(.013,.32,.51),.30)
steel=c.material('Canteen dark fixed dining frame',(.029,.037,.035),.38,.48)
inox=c.material('Canteen brushed stainless service steel',(.43,.48,.47),.31,.8)
c.box('Canteen complete dining floor',(125,373,1.04),(27.6,43.6,.04),cream)
c.box('Canteen white ceiling finish',(125,373,4.90),(27.6,43.6,.055),white)
for y in [354,362,370,378,386,393]:
 c.box('Canteen white transverse ceiling beam',(125,y,4.63),(27.6,.42,.50),white)
 for x in [121.7,136.3]:
  c.box('Canteen interior structural column',(x,y,2.99),(.48,.48,3.90),white)
  c.box('Canteen cream tiled column base',(x,y,1.68),(.51,.51,1.24),cream)
  c.box('Canteen column dark skirting',(x,y,1.12),(.53,.53,.12),steel)
c.collection('351_Canteen_Blue_Fixed_Stools_And_Partitions')
for x in [115,119.6,129.2,133.8]:
 for y in [357,361,365,369,377,381,385]:
  c.box('Dining four seat white tabletop',(x,y,1.79),(1.80,.78,.055),white,.025)
  c.box('Dining photographed tall white divider',(x,y,2.19),(1.78,.018,.78),white,.012)
  c.box('Dining perpendicular white divider',(x,y,2.0),(.018,.75,.40),white,.012)
  for dx in [-.65,.65]:
   c.box('Dining fixed black table leg',(x+dx,y,1.41),(.055,.12,.72),steel)
   c.box('Dining seat support crossbar',(x+dx,y,1.30),(.055,1.54,.07),steel)
   for dy in [-.69,.69]:
    c.box('Dining fixed stool leg',(x+dx,y+dy,1.28),(.05,.05,.45),steel)
    c.rod('Dining cyan round stool',(x+dx,y+dy,1.50),(x+dx,y+dy,1.545),.20,blue,sides=32)
    c.rod('Dining stool concave inset',(x+dx,y+dy,1.545),(x+dx,y+dy,1.551),.155,blue,sides=32)
c.collection('352_Canteen_Service_And_Dish_Return')
for x in [115.2,119.4,129.5,133.7]:
 c.box('Canteen stainless serving counter',(x,391,1.53),(3.6,1.1,.95),inox,.025)
 c.box('Canteen pale serving fascia',(x,390.44,1.5),(3.5,.028,.75),cream)
 for dx in [-1.4,-.47,.47,1.4]:
  c.box('Canteen recessed tray rim',(x+dx,390.9,2.014),(.80,.73,.025),inox,.035)
  c.box('Canteen recessed dark tray',(x+dx,390.9,2.021),(.66,.59,.024),steel,.04)
 for dx in [-1.6,1.6]:c.rod('Canteen counter glass upright',(x+dx,390.6,2.04),(x+dx,390.6,2.72),.019,inox,sides=10)
 c.box('Canteen counter sneeze screen',(x,390.6,2.50),(3.2,.022,.44),i.glass())
yellow=c.material('Canteen warm service wall',(.62,.47,.12),.78)
c.box('Canteen rear service partition',(125,393.4,2.95),(27.6,.15,3.78),yellow)
c.text('Canteen observed dish return sign','收 残 处',(125,393.30,3.67),.40,c.material('Canteen red interior lettering',(.43,.015,.015),.6))
c.box('Canteen dish return dark recess',(125,393.29,2.29),(3.4,.04,1.7),steel)
c.box('Canteen dish return stainless shelf',(125,392.85,1.94),(3.6,.85,.07),inox,.012)
for y in [361,377]:
 x=124.4
 c.box('Canteen aisle blue spacing floor marker',(x,y,1.066),(1.4,.16,.007),blue)
# Trolley by the side aisle, away from the central route.
for y in [359,383]:
 x=138.45
 for z in [1.25,1.70,2.05]:c.box('Canteen dish trolley shelf',(x,y,z),(.60,.85,.035),inox,.01)
 for xx in [x-.26,x+.26]:
  for yy in [y-.38,y+.38]:
   c.rod('Canteen trolley stainless upright',(xx,yy,1.15),(xx,yy,2.10),.015,inox,sides=8)
   c.rod('Canteen trolley wheel',(xx-.025,yy,1.12),(xx+.025,yy,1.12),.07,steel,sides=12)
c.collection('353_Canteen_Fluorescents_And_Ceiling_Fans')
for x in [115.5,124.4,133]:
 for y in [356,364,372,380,388]:
  i.tube_light('Canteen twin fluorescent',x,y,4.77,1.6,95)
  yy=y+2
  c.rod('Canteen ceiling fan drop',(x,yy,4.85),(x,yy,4.12),.018,white,sides=10)
  c.rod('Canteen ceiling fan motor',(x,yy,4.05),(x,yy,4.15),.15,white,sides=24)
  for a in [0,math.tau/3,2*math.tau/3]:
   verts=[]
   for r,t in [(.12,-.08),(.58,-.07),(.66,.06),(.20,.10)]:verts.append((x+r*math.cos(a)-t*math.sin(a),yy+r*math.sin(a)+t*math.cos(a),4.10))
   c.mesh('Canteen white ceiling fan blade',verts,[(0,1,2,3)],white)
c.collection('358_Canteen_Indoor_And_Batch_Cameras')
c.camera('164_Canteen_dining_hall',(124.4,354,2.74),(124.4,382,2.9),24)
c.camera('165_Canteen_blue_stool_detail',(123,365,2.54),(119.5,367,1.9),28)
c.camera('166_Canteen_service_and_return',(124.4,380,2.74),(125,392.6,2.6),20)
c.camera('167_Canteen_window_and_tables',(116.5,387,2.74),(113,361,2.8),24)
c.camera('168_Campus_integrated_v039',(-265,-140,415),(65,184,0),28)
sc['interior_batch_scope']='gym, mathematics museum, history gallery, photographed canteen dining floor; Xinjiang paused'
h.save(39,'Photographed canteen dining floor 427: 28 fixed four-seat tables, 112 cyan stools, tall white table partitions, cream tiles, white beams/columns, fluorescent fittings, ceiling fans, service counters and dish return. Seating quantity/layout is estimated; kitchen and unobserved upper-floor rooms not claimed. Integrates eight corrected outdoor basketball courts and four tennis courts plus prior indoor milestones.',[427,425,426],'164_Canteen_dining_hall')
