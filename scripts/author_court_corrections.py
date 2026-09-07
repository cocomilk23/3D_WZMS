"""Generate the successor builder from the immutable v033 court details."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
src=(root/'scripts/blender/build_basketball.py').read_text(encoding='utf8')
details=src[src.index('def hoop('):src.index("c.collection('297_")]
details=details.replace('post=cy+sign*15.6','post=cy+sign*14.4').replace('(1.35,1.9,.44)','(1.35,.8,.44)')
details=details.replace('enumerate([226,263,300])','enumerate([222,248,274,300])').replace('enumerate([4,27])','enumerate([-1,30])')
details=details.replace("c.collection('291_Basketball_Court_'+str(row*2+col+1))", "c.collection('301_Basketball_8_Court_'+str(row*2+col+1))\n        original_cx,original_cy=cx,cy\n        cx,cy=0,0")
details+='''        bpy.context.view_layer.update()
        transform=Matrix.Translation((original_cx,original_cy,0))@Matrix.Rotation(math.pi/2,4,'Z')
        for obj in c.COL.objects:obj.matrix_world=transform@obj.matrix_world
        c.COL['court_number']=row*2+col+1
        c.COL['long_axis']='east-west; rotated 90 degrees from v033'
        c.COL['playing_rectangle_m']=[28,15]
        cx,cy=original_cx,original_cy
'''
header='''"""User-corrected eight basketball courts; four north-south rows by two east-west columns."""
import bpy,sys,math,json
from pathlib import Path
from mathutils import Matrix,Vector
sys.path.insert(0,str(Path(__file__).parent))
import campus_common as c,north_common as n,north_landscape as l
import south_detail_common as s,island_common as h,sports_common as q
sc=bpy.data.scenes['WZMS_Campus'];c.activate(sc);p=n.palette()
bpy.context.view_layer.update()
names=[o.name for o in bpy.data.collections['290_Basketball_Red_Green_Surfaces'].objects if not o.name.startswith('Sports integration gym branch')]
# Only the estimated strip displaced by the wider courts is revised. Main roads stay put.
for colname in ['50_Zhongshan_Middle_Road_And_Junctions','60_Zhongshan_North_Road_And_Branches']:
 for o in bpy.data.collections[colname].objects:
  if o.name.startswith(('Middle western grey sidepath','Middle west tree verge','North west grey strip','North west tree verge')):names.append(o.name)
  elif 'kerbstone' in o.name and 41<o.location.x<47:names.append(o.name)
for colname in ['51_Zhongshan_Middle_Shade_Trees','61_Zhongshan_North_Tree_Avenue','252_Nantian_Banyan_Avenue_And_Low_Planting','254_Nantian_Road_Furniture','55_Zhongshan_Middle_Street_Furniture']:
 for o in bpy.data.collections[colname].objects:
  if o.type!='MESH':continue
  bounds=[o.matrix_world@Vector(v) for v in o.bound_box]
  mid=sum(bounds,Vector())/8
  if ((-16.6<mid.x<-11 and 211<mid.y<320) or (45.8<mid.x<49.2 and 209.5<mid.y<361)):
   names.append(o.name)
c.collection('309_Basketball_Corrected_Perimeter')
hydrants=[]
for old in list(sc.objects):
 if old.name.startswith('Fire hydrant'):
  obj=old.copy();c.COL.objects.link(obj);hydrants.append(obj);names.append(old.name)
for obj in hydrants:obj.matrix_world=Matrix.Translation((1.5,0,0))@obj.matrix_world
prototypes=[]
for label in ['Middle mature avenue tree scaffold branches','Middle mature avenue tree canopy leaves']:
 old=sc.objects[label];obj=old.copy();c.COL.objects.link(obj);prototypes.append((obj,label))
h.retire('v0.0.34',collections=['291_Basketball_Court_'+str(i) for i in range(1,7)]+['297_Basketball_Fence_And_Shaded_Edges'],names=names)
for obj,label in prototypes:obj.name=label;obj.location=(-9,324,0);obj.scale=(.66,.66,.66)
green=bpy.data.materials['Basketball weathered green acrylic'];red=bpy.data.materials['Basketball faded terracotta acrylic']
paint=bpy.data.materials['Basketball warm white markings'];steel=bpy.data.materials['Basketball photographed green steel']
board=bpy.data.materials['Basketball clear green tinted backboard'];netmat=bpy.data.materials['Basketball white cord net'];orange=bpy.data.materials['Basketball red orange hoop steel']
soil=bpy.data.materials['Basketball perimeter soil']
c.collection('300_Basketball_Corrected_Site_And_Paths')
c.box('Eight court continuous foundation',(14.5,265,-.7),(62.4,108,1.28),p['stone'])
c.box('Eight court green surround',(14.5,265,-.015),(62.4,108,.08),green)
pave=bpy.data.materials['Basketball shaded entry pavers']
s.ribbon('Eight court north entry',[(-3,330),(14.5,330),(14.5,319)],3.2,pave,0,.20,miter=True)
s.ribbon('Eight court north support',[(-3,330),(14.5,330),(14.5,319)],5.6,soil,-.08,1.5,miter=True)
s.ribbon('Eight court south connection',[(14.5,211),(14.5,205.8),(24.8,205.8),(24.8,200)],3.2,pave,0,.20,miter=True)
s.ribbon('Eight court south support',[(14.5,211),(14.5,205.8),(24.8,205.8),(24.8,200)],5.0,soil,-.08,1.5,miter=True)
# Move the estimated west-side footpath into the former tree strip, retaining both ends.
walk=[(44.2,204.5),(47.5,213),(47.5,350),(44.2,360.5)]
s.ribbon('Zhongshan revised continuous west footpath',walk,3.4,pave,-.01,.24,miter=True)
for y in [235,259,287,313]:s.ribbon('Eight court east gate crossing',[(41.5,y),(49.5,y)],2.8,pave,0,.20)
'''
footer='''c.collection('309_Basketball_Corrected_Perimeter')
for x in [-16.7,45.7]:
 spans=[(211,319)] if x<0 else [(211,233.5),(236.5,257.5),(260.5,285.5),(288.5,311.5),(314.5,319)]
 for a,b in spans:s.wire_fence('Eight court green enclosure',(x,a),(x,b),3.3,steel,.14)
for y in [211,319]:
 for a,b in [(-16.7,12.8),(16.2,45.7)]:s.wire_fence('Eight court north south gate',(a,y),(b,y),3.3,steel,.14)
for x in [-16.2,45.2]:
 for y in [235,261,287,313]:
  c.rod('Eight court floodlight mast',(x,y,0),(x,y,8.7),.065,p['steel'],.045,12)
  for dx in [-.4,.4]:c.box('Eight court paired floodlight',(x+dx,y,8.6),(.52,.24,.34),p['white'],.03)
for x in [2,28,39]:
 s.tree(x,324,.66,x*.04)
 l.bench(x,321.5,0)
c.collection('310_Court_Correction_Cameras')
c.camera('139_Basketball_eight_overview',(93,170,110),(14.5,263,0),38)
c.camera('140_Basketball_rotated_courts',(14.5,235,1.7),(32,250,1.8),25)
c.camera('141_Basketball_shared_aisle',(14.5,320,1.7),(14.5,248,1.7),28)
c.camera('142_Basketball_Zhongshan_connection',(54,259,1.7),(30,260,1.8),27)
c.camera('143_Basketball_top_plan',(14.5,265,210),(14.5,265,0),38)
sc['basketball_count']=8;sc['basketball_grid']='4 north-south rows x 2 east-west columns';sc['basketball_orientation_correction_degrees']=90
bpy.context.view_layer.update()
centres=[]
for number in range(1,9):
 col=bpy.data.collections['301_Basketball_8_Court_'+str(number)]
 obj=next(o for o in col.objects if o.name.startswith('Basketball red centre circle'))
 centre=obj.matrix_world@Vector((0,0,.037));centres.append([round(centre.x,3),round(centre.y,3)])
 expected=[[-1,30][(number-1)%2],[222,248,274,300][(number-1)//2]]
 assert centres[-1]==expected,(number,centres[-1],expected)
 baselines=[o for o in col.objects if o.name.startswith('Basketball baseline')]
 for line in baselines:
  pts=[line.matrix_world@v.co for v in line.data.vertices]
  assert max(v.y for v in pts)-min(v.y for v in pts)>14.9 and max(v.x for v in pts)-min(v.x for v in pts)<.1
assert len(set(tuple(p) for p in centres))==8
(c.ROOT/'deliverables/v0.0.34/layout_validation.json').write_text(json.dumps({'court_centres':centres,'unique_courts':8,'hoops':sum(o.name.startswith('Basketball continuous orange rim') for o in sc.objects),'rotation_degrees':90,'baseline_axis_verified':'Y; playing long axis X','all_passed':True},indent=2),encoding='utf8')
h.save(34,'User correction: eight 28x15m design-proportion basketball courts in a 4x2 grid, each long axis rotated 90 degrees. Compact fixed hoop supports and path/planting reflow are estimated design adaptations, not surveyed dimensions. Xinjiang branch paused; interiors remain scheduled.',[358,379,347,348],'139_Basketball_eight_overview')
'''
(root/'scripts/blender/build_basketball_corrected.py').write_text(header+details+footer,encoding='utf8')
