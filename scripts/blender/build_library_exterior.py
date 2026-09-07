"""v017: replace only the old Buqing library context with an editable hollow shell.
Reference 119232387/390 plus atrium 388/389/391. Dimensions are estimates.
"""
import bpy,sys,math,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import campus_common as c, north_common as n, culture_common as k
sc=bpy.data.scenes['WZMS_Campus'];c.activate(sc);p=n.palette()
old=bpy.data.collections.get('44_Buqing_Library_Entrance_Context')
retired=[o.name for o in old.all_objects] if old else []
if old:
 for o in list(old.all_objects):bpy.data.objects.remove(o,do_unlink=True)
 bpy.data.collections.remove(old)
out=c.ROOT/'deliverables/v0.0.17';out.mkdir(parents=True,exist_ok=True)
(out/'replacement_scope.json').write_text(json.dumps({'retired_collection':'44_Buqing_Library_Entrance_Context','retired_objects':retired,'reason':'Replace provisional solid context with photograph-supported exterior and hollow structure'},ensure_ascii=False,indent=2),encoding='utf8')
stone=n.paving('Library cream limestone joints',(.68,.65,.55),(1.0,.52),.003)
floor=n.paving('Library polished brown hall tile',(.12,.095,.070),(.8,.8),.004)
bs=floor.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.24;bs.inputs['Coat Weight'].default_value=.25
tile=n.paving('Library terrace grey tiles',(.44,.45,.42),(.6,.3),.006)
glass=c.material('Library real transmissive glazing',(.67,.85,.83),.09)
bs=glass.node_tree.nodes.get('Principled BSDF');bs.inputs['Transmission Weight'].default_value=.86;bs.inputs['IOR'].default_value=1.45
gold=c.material('Library brushed brass lettering',(.57,.34,.06),.30,.75)
c.collection('130_Library_Structure_And_Exterior')
c.box('Library ground apron',(124,155,-.16),(36,34,.30),tile)
c.box('Library ground hall finished floor',(128.5,155,-.08),(27,34,.16),floor)
k.ring_floor('Library level two atrium slab',4.25,floor)
k.ring_floor('Library level three atrium slab',8.5,floor,True)
k.ring_floor('Library roof with circular light well',12.75,p['white'])
# Side and rear walls with real window openings at every storey.
for level in range(3):
 z=level*4.25
 for yy in [138,172]:
  c.box('Library side stone sill',(128.5,yy,z+.55),(27,.26,1.1),stone)
  c.box('Library side stone lintel',(128.5,yy,z+3.76),(27,.28,.73),stone)
  for xx in [116,120.5,125,129.5,134,138.5,141.8]:
   c.box('Library side masonry pier',(xx,yy,z+2.24),(.42,.30,2.30),stone)
  c.box('Library side west corner return',(115.55,yy,z+2.24),(1.1,.30,2.30),stone)
  for xx in [118.3,122.8,127.3,131.8,136.3,140.2]:
   w=3.8 if xx<139 else 2.6
   c.box('Library side clear glass',(xx,yy,z+2.26),(w,.045,2.25),glass)
   for dx in [-w/2,0,w/2]:c.box('Library side silver sash',(xx+dx,yy,z+2.26),(.045,.11,2.30),p['steel'])
   c.box('Library side glass transom',(xx,yy,z+2.8),(w,.1,.045),p['steel'])
 c.box('Library east sill',(142,155,z+.5),(.28,34,1.0),stone)
 c.box('Library east lintel',(142,155,z+3.8),(.28,34,.65),stone)
 c.box('Library east south corner glazing',(142,139,z+2.18),(.045,1.6,2.35),glass)
 c.box('Library east south corner jamb',(142,138.1,z+2.18),(.30,.25,2.35),stone)
 for yy in range(140,173,4):
  c.box('Library east pier',(142,yy,z+2.18),(.30,.4,2.35),stone)
  if yy<170:
   c.box('Library east glazing',(142,yy+2,z+2.18),(.045,3.6,2.35),glass)
   c.box('Library east vertical sash',(142.04,yy+2,z+2.18),(.08,.04,2.38),p['steel'])
 # Recessed west lobby doors: central 4.8m opening is deliberately open.
 for yy,span in [(144.3,12.6),(165.7,12.6)]:
  c.box('Library west hall glazing',(115,yy,z+1.75),(.045,span,3.50),glass)
  for t in range(7):c.box('Library west lobby mullion',(114.94,yy-span/2+t*span/6,z+1.75),(.09,.05,3.5),p['steel'])
 c.box('Library entrance lintel',(115,155,z+3.83),(.4,34,.65),stone)
 for yy in [152.55,157.45]:
  c.box('Library open entry door folded leaf',(116.1,yy,z+1.55),(2.15,.045,3.1),glass)
  for zz in [z+.1,z+1.1,z+3.06]:c.box('Library open door crossbar',(116.1,yy,zz),(2.15,.06,.04),p['steel'])
  c.rod('Library door stainless pull',(116.6,yy-.06,z+.9),(116.6,yy-.06,z+1.5),.018,p['steel'])
 for yy in [139,144,150,160,166,171]:c.box('Library portico square pier',(108.2,yy,z+2.05),(.62,.62,4.10),stone)
 c.box('Library west balcony slab',(111.5,155,z+4.10),(7,34,.30),stone)
# Large upper title wall and thin blue ribbon, as visible from Buqing Square.
c.box('Library title stone wall',(108,155,10.58),(.36,15,3.96),stone)
c.box('Library title blue green band',(107.80,155,8.73),(.05,15,.17),p['glass'])
c.text('Library facade title','图 书 馆',(107.77,155,10.1),1.05,gold,(math.pi/2,0,-math.pi/2))
for yy in [141.6,170.6]:
 xx0,ww=(112,4) if yy<150 else (108.9,9.5)
 c.box('Library terrace planter parapet',(xx0,yy,4.65),(ww,.7,.8),p['white'])
 c.box('Library terrace dark planter base',(xx0,yy,4.32),(ww+.1,.74,.16),p['dark'])
 for xx in ([111,113] if yy<150 else [105,107,109,111,113]):k.pot(xx,yy,4.95,.48,seed=int(xx+yy))
# Walkable external stair with landing connected to the existing plaza.
c.collection('131_Library_External_Stair_And_Terrace')
k.stairs('Library external granite staircase',(104,134.5,0),(104,141.5,4.25),4.0,25,tile)
c.box('Library external stair top landing',(108.5,142.4,4.12),(13,1.8,.26),tile)
c.box('Library west terrace finished paving',(110.8,156.9,4.255),(8.1,27.0,.01),tile)
k.rail('Library terrace west balustrade',[(106.8,144.0,4.25),(106.8,169.7,4.25)])
for yy in [144,169]:k.pot(113.5,yy,4.26,1.15,seed=int(yy))
# Circular drum and shallow conical radial glass skylight.
c.collection('132_Library_Radial_Skylight')
for z in [12.73,13.52]:k.arc('Library skylight circular curb',130,155,6,z,p['white'],width=.16,steps=96)
for i in range(24):
 a=i*math.tau/24;b=(i+1)*math.tau/24
 q=(130+6*math.cos(a),155+6*math.sin(a),13.52);r=(130+6*math.cos(b),155+6*math.sin(b),13.52)
 c.mesh('Library skylight radial glass panel',[(130,155,15.1),q,r],[(0,1,2)],glass)
 c.rod('Library skylight radial beam',(130,155,15.1),q,.067,p['white'],sides=10)
 c.rod('Library skylight drum upright',(q[0],q[1],12.75),q,.045,p['white'])
 c.mesh('Library clerestory glass',[(q[0],q[1],12.75),(r[0],r[1],12.75),r,q],[(0,1,2,3)],glass)
c.rod('Library skylight crown',(130,155,15.03),(130,155,15.28),.23,p['steel'],sides=24)
c.collection('138_Library_Exterior_Review_Cameras')
c.camera('63_Library_Buqing_front',(76,127,6),(118,155,6),33)
c.camera('64_Library_ground_portico',(102,153,1.7),(119,155,2.2),24)
c.camera('65_Library_upper_terrace',(106.9,145,5.95),(115,161,6.5),24)
c.camera('66_Library_roof_and_connections',(166,119,41),(121,155,5),40)
sc.camera=sc.objects['63_Library_Buqing_front']
sc['scope']='Library exterior replacement; photograph-supported massing, open portico, external staircase, terrace and radial skylight. Interior furnishing in next milestone.'
c.save(c.ROOT/'models/campus/WZMS_Campus_v017.blend','v0.0.17',[119232387,119232388,119232389,119232390,119232391])
print('WZMS_BUILD_COMPLETE v0.0.17',flush=True)
