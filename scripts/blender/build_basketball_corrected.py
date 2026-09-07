"""User-corrected eight basketball courts; four north-south rows by two east-west columns."""
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
def hoop(cx,cy,sign):
    by=cy+sign*12.80;post=cy+sign*14.4;hy=cy+sign*12.425
    c.box('Basketball green weighted steel base',(cx,post,.22),(1.35,.8,.44),steel,.06)
    s.beam('Basketball substantial square upright',(cx,post,.30),(cx,post,3.85),.18,.21,steel)
    s.beam('Basketball cantilever top arm',(cx,post,3.75),(cx,by,3.68),.19,.16,steel)
    s.beam('Basketball diagonal arm brace',(cx,post,2.0),(cx,by,3.39),.11,.12,steel)
    for xx in [cx-.65,cx+.65]:s.beam('Basketball backboard supporting fork',(cx,post,3.6),(xx,by+sign*.06,3.60),.055,.065,steel)
    c.box('Basketball transparent regulation proportion board',(cx,by,3.425),(1.8,.035,1.05),board)
    for xx in [cx-.91,cx+.91]:c.box('Basketball board outer vertical frame',(xx,by,3.425),(.045,.09,1.12),steel)
    for z in [2.88,3.97]:c.box('Basketball board outer horizontal frame',(cx,by,z),(1.86,.09,.045),steel)
    fy=by-sign*.035
    for xx in [cx-.295,cx+.295]:c.box('Basketball backboard target vertical',(xx,fy,3.275),(.035,.008,.45),paint)
    for z in [3.05,3.50]:c.box('Basketball backboard target horizontal',(cx,fy,z),(.59,.008,.035),paint)
    for xx in [cx-.79,cx+.79]:
        for z in [3.02,3.83]:c.rod('Basketball board mounting bolt',(xx,by-sign*.07,z),(xx,by+sign*.065,z),.022,p['steel'],sides=8)
    c.box('Basketball rim wall bracket',(cx,by-sign*.09,3.05),(.18,.22,.10),orange)
    v,f=[],[]
    for j in range(64):
        a=j*math.tau/64;b=(j+1)*math.tau/64
        c.tube_data(v,f,(cx+.225*math.cos(a),hy+.225*math.sin(a),3.05),(cx+.225*math.cos(b),hy+.225*math.sin(b),3.05),.009,.009,8)
    c.mesh('Basketball continuous orange rim',v,f,orange)
    v,f=[],[]
    for level in range(6):
        za=3.025-level*.075;zb=za-.075;ra=.22-level*.014;rb=ra-.014
        for j in range(12):
            a=j*math.tau/12+(level%2)*math.pi/12
            for direction in [-1,1]:
                b=a+direction*math.pi/12
                c.tube_data(v,f,(cx+ra*math.cos(a),hy+ra*math.sin(a),za),(cx+rb*math.cos(b),hy+rb*math.sin(b),zb),.0022,.0022,5)
    c.mesh('Basketball hanging diamond cord net',v,f,netmat)
    c.box('Basketball green upright impact padding',(cx,post-sign*.15,1.02),(.39,.20,1.30),c.material('Basketball dark green safety pad',(.035,.14,.068),.79),.05)

for row,cy in enumerate([222,248,274,300]):
    for col,cx in enumerate([-1,30]):
        c.collection('301_Basketball_8_Court_'+str(row*2+col+1))
        original_cx,original_cy=cx,cy
        cx,cy=0,0
        for yy in [cy-14,cy+14]:q.flat_line('Basketball baseline',[(cx-7.5,yy),(cx+7.5,yy)],.05,paint,.043)
        for xx in [cx-7.5,cx+7.5]:q.flat_line('Basketball sideline',[(xx,cy-14),(xx,cy+14)],.05,paint,.043)
        q.flat_line('Basketball half court line',[(cx-7.5,cy),(cx+7.5,cy)],.05,paint,.043)
        n.disk('Basketball red centre circle',cx,cy,.037,1.8,red,96)
        q.flat_arc('Basketball centre circle white outline',cx,cy,1.8,0,math.tau,paint,.049)
        for sign in [-1,1]:
            ky=cy+sign*11.1
            c.mesh('Basketball photographed red trapezoid key',[(cx-3,cy+sign*14,.04),(cx+3,cy+sign*14,.04),(cx+1.8,cy+sign*8.2,.04),(cx-1.8,cy+sign*8.2,.04)],[(0,1,2,3)] if sign==-1 else [(3,2,1,0)],red)
            for side in [-1,1]:q.flat_line('Basketball photographed tapering key sideline',[(cx+side*3,cy+sign*14),(cx+side*1.8,cy+sign*8.2)],.05,paint,.048)
            q.flat_line('Basketball free throw line',[(cx-1.8,cy+sign*8.2),(cx+1.8,cy+sign*8.2)],.05,paint,.048)
            a0,a1=(math.pi,math.tau) if sign==1 else (0,math.pi)
            q.flat_arc('Basketball free throw semicircle',cx,cy+sign*8.2,1.8,a0,a1,paint,.048)
            delta=math.acos(6.6/6.75)
            a0,a1=(math.pi+delta,math.tau-delta) if sign==1 else (delta,math.pi-delta)
            q.flat_arc('Basketball three point arc',cx,cy+sign*12.425,6.75,a0,a1,paint,.048)
            join=cy+sign*(12.425-math.sqrt(6.75**2-6.6**2))
            for xx in [cx-6.6,cx+6.6]:q.flat_line('Basketball three point corner straight',[(xx,cy+sign*14),(xx,join)],.05,paint,.048)
            for j in range(4):
                w=1.8+1.2*(.8+j)/5.8
                for side in [-1,1]:q.flat_line('Basketball free throw rebound tick',[(cx+side*w,cy+sign*(9.0+j)),(cx+side*(w+.28),cy+sign*(9.0+j))],.05,paint,.048)
            hoop(cx,cy,sign)
        bpy.context.view_layer.update()
        transform=Matrix.Translation((original_cx,original_cy,0))@Matrix.Rotation(math.pi/2,4,'Z')
        for obj in c.COL.objects:obj.matrix_world=transform@obj.matrix_world
        c.COL['court_number']=row*2+col+1
        c.COL['long_axis']='east-west; rotated 90 degrees from v033'
        c.COL['playing_rectangle_m']=[28,15]
        cx,cy=original_cx,original_cy
c.collection('309_Basketball_Corrected_Perimeter')
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
