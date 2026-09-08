"""South precinct registration to aerial ground landmarks; dimensions remain estimates."""
import bpy,sys,math,json,random,re
from pathlib import Path
from mathutils import Matrix,Vector
sys.path.insert(0,str(Path(__file__).parent))
import campus_common as c, island_common as h, south_detail_common as s, north_common as n
sc=bpy.data.scenes['WZMS_Campus'];c.activate(sc)
out=c.ROOT/'deliverables/v0.0.42';out.mkdir(parents=True,exist_ok=True)
changes=dict(retired_objects=[],transformed_objects=[],modified_objects=[],reason='User approved aerial registration of the south gate, courts, lotus bay, Heyu and shoreline. Preserve existing school and northern campus, and preserve south wall content during whole-gate translation.')
def centre(o):return sum((o.matrix_world@Vector(v) for v in o.bound_box),Vector())/8
def shift(objects,xyz):
 for o in set(objects):
  o.matrix_world=Matrix.Translation(xyz)@o.matrix_world
  changes['transformed_objects'].append(o.name)
def objects_in(names):return [o for name in names for o in bpy.data.collections[name].objects]
def retire(objects):
 objects=set(objects);changes['retired_objects'].extend(o.name for o in objects)
 bpy.data.batch_remove(ids=tuple(objects))
def warp_plaza_point(v):
 t=max(0,min(1,(45-v.y)/45));return Vector((v.x-26*t,v.y-25*t,v.z))
def warp_mesh(o):
 # Only planar paving, ground and planted strips are stretched. Furniture/trees stay rigid.
 old=o.matrix_world.copy();inv=old.inverted();o.data=o.data.copy()
 for v in o.data.vertices:v.co=inv@warp_plaza_point(old@v.co)
 o.data.update();changes['modified_objects'].append(o.name)

# The gate, its stonework and both photographs move as one rigid assembly.
shift(objects_in(['01_Ground','02_NameWall','03_Gates','04_Guardhouses','05_Landscape','14_Plaza_Wall_Reverse']),(-26,-25,0))
# Retract the right accordion gate into its drive end, keeping posts/wheels rigid.
right_diagonals=[]
for o in bpy.data.collections['03_Gates'].objects:
 q=centre(o)
 if q.x<=-17:continue
 if o.name.startswith('Gate folding diagonal'):right_diagonals.append(o)
 elif o.name.startswith(('Gate upright','Gate caster')):
  k=max(0,min(17,round((q.x+26-9.35)/5.85*17)))
  shift([o],(13.6+1.6*k/17-26-q.x,0,0))
retire(right_diagonals)
c.collection('386_South_Gate_Open_Accordion')
gate_dark=bpy.data.materials['Graphite painted metal']
height=math.sqrt(1.05**2+(5.85/17)**2-(1.6/17)**2)
for k in range(17):
 x=13.6+1.6*k/17-26;x2=13.6+1.6*(k+1)/17-26
 for y in [-25.03,-24.67]:
  c.rod('v042 retracted gate folding bar',(x,y,.30),(x2,y,.30+height),.018,gate_dark,sides=10)
  c.rod('v042 retracted gate folding bar',(x,y,.30+height),(x2,y,.30),.018,gate_dark,sides=10)
for o in bpy.data.collections['10_Plaza_Paving'].objects:warp_mesh(o)
for name in ['11_Plaza_Tree_Islands','12_Plaza_Furniture','13_Plaza_Mature_Gardens']:
 for o in bpy.data.collections[name].objects:
  if o.name.startswith('Garden low border'):warp_mesh(o);continue
  q=centre(o)
  if o.name.startswith('Garden broadleaf'):
   anchor=[11,27,43][int(re.search(r'Garden broadleaf -?1 (\d)',o.name).group(1))]
  elif o.name.startswith('Notice'):
   anchor=min([9+j*4.9 for j in range(5)],key=lambda y:abs(y-q.y))
  elif o.name.startswith(('Garden display','Display stand')):anchor=17
  else:anchor=min([10,20,30,40],key=lambda y:abs(y-q.y))
  a=Vector((0,anchor,0));shift([o],warp_plaza_point(a)-a)

# Keep every court/net dimension and its confirmed orientation; change position only.
shift(objects_in(['360_Refined_Tennis_Four_Rotated_Courts','361_Refined_Tennis_Enclosure_And_Divider']),(-52,-39,0))
col=bpy.data.collections['379_Tennis_Aerial_Corrected_Shore_And_Access']
shift([o for o in col.objects if o.name.startswith(('v041 tennis blue boundary','v041 east court retaining bank'))],(-52,-39,0))
retire([o for o in list(col.objects) if not o.name.startswith(('v041 tennis blue boundary','v041 east court retaining bank'))])
retire(objects_in(['90_Tennis_Courts_And_Access']))
island=objects_in(['111_Heyu_Paths_And_Entry_Bridge','112_Heyu_Variegated_Banks_And_Lawn','113_Heyu_Banyans_And_Aerial_Roots','114_Heyu_Lotus_Beds','115_Heyu_Lights_And_Lifesaving'])
old_entry=[o for o in island if o.name.startswith('Heyu mainland entry bridge')]
island=[o for o in island if o not in old_entry]
island += [bpy.data.objects[name] for name in ['Heyu closed island soil and revetment','Heyu grass island top']]
shift(island,(13,-27,0));retire(old_entry)
shift([o for o in bpy.data.collections['115_Heyu_Lights_And_Lifesaving'].objects if o.name.startswith(('Heyu orange lifebuoy','Heyu lifebuoy stand'))],(-16.3,13,0))
shift(objects_in(['315_Tennis_Shuinan_Relocated_Peninsula']),(-7,-77,0))

# Remove inherited infill rectangles and the isolated oval pond, not just cover them.
retire([o for o in bpy.data.collections['110_Heyu_Lake_And_Shore'].objects if o.name not in ['Heyu closed island soil and revetment','Heyu grass island top']])
retire(objects_in(['362_Refined_Tennis_Heyu_Connections']))
old_pond=[o for o in bpy.data.collections['33_Zhongshan_Roadside_Landscape'].objects if o.name.startswith(('Approach lotus','Lotus pond','Lotus garden','East entrance garden','East garden broadleaf','Low curved pond','Lotus stem','Lotus cupped','Lotus pink'))]
retire(old_pond)
if 'Tennis estimated southern landscape infill' in bpy.data.objects:retire([bpy.data.objects['Tennis estimated southern landscape infill']])

p=n.palette();pave=bpy.data.materials['Waterside fine rectangular granite'];lawn=bpy.data.materials['Heyu connecting bank lawn'];water=bpy.data.materials['Heyu green lake water']
c.collection('381_South_Registered_Mainland_And_Lotus_Bay')
def solid_polygon(name,outline,top,bottom,mat):
 count=len(outline);v=[(x,y,top) for x,y in outline]+[(x,y,bottom) for x,y in outline]
 faces=[tuple(range(count)),tuple(reversed(range(count,2*count)))]+[(i,count+i,count+(i+1)%count,(i+1)%count) for i in range(count)]
 return c.mesh(name,v,faces,mat)
land=[(-94,-68),(92,-68),(115,-57),(110,-51),(85,-51),(85,-13),(13,-13),(13,21),(25,29),(50,32),(61.5,28.5),(63,32),(61.9,43),(61.9,71),(-90,71)]
solid_polygon('v042 continuous south mainland',land,-.06,-2.1,lawn)
bay=[(13,-13),(85,-13),(85,-55),(118,-55),(130,-70),(171,-70),(171,71),(135,71),(135,145),(90,145),(90,71),(61.9,71),(61.9,43),(63,32),(61.5,28.5),(50,32),(25,29),(13,21)]
c.mesh('v042 continuous lotus bay and east lake',[(x,y,-1.15) for x,y in bay],[tuple(range(len(bay)))],water)
c.mesh('v042 continuous lotus bay lake bed',[(x,y,-2.7) for x,y in bay],[tuple(range(len(bay)))],p['seam'])
south_water=[(-94,-106),(171,-106),(171,-70),(130,-70),(118,-55),(85,-55),(85,-68),(-94,-68)]
c.mesh('v042 southern waterfront water',[(x,y,-1.15) for x,y in south_water],[tuple(range(len(south_water)))],water)
c.mesh('v042 southern waterfront lake bed',[(x,y,-2.7) for x,y in south_water],[tuple(range(len(south_water)))],p['seam'])
# Connect the mainland coast to the existing utility peninsula without empty water gaps.
shore=[(-94,-68),(92,-68),(115,-57),(110,-51),(85,-51)]
s.ribbon('v042 south granite shoreline',shore,.45,p['stone'],-.02,1.6,miter=True)
s.ribbon('v042 lotus bay mainland retaining edge',[(13,-13),(13,21),(25,29),(50,32),(61.5,28.5),(63,32),(61.9,43)],.28,p['stone'],-.025,1.5,miter=True)

c.collection('382_South_Registered_Walks_And_Bridges')
solid_polygon('v042 gate inner threshold paving',[(-48,-22),(-4,-22),(-2.266,-20.333),(-46.266,-20.333)],-.01,-.22,pave)
# A planted-side public access reaches the west court gate without cutting a court.
s.ribbon('v042 plaza to tennis west gate',[(-12,-19),(10,-19),(10,-22),(14,-22)],3,pave,-.01,.18,miter=True)
s.ribbon('v042 southern court perimeter path',[(10,-22),(10,-52),(88,-52)],2.4,pave,-.01,.18,miter=True)
# Bay-side promenade connects the school forewalk to the relocated island.
s.ribbon('v042 school to bay promenade',[(54,47),(57,41),(60,30)],3,pave,-.01,.22,miter=True)
s.bridge('v042 mainland to Heyu',[(60,30),(69,27),(78,17),(81.5,17),(83,17)],2.4,miter=True,open_land_end=True)
s.bridge('v042 Heyu eastern folded walkway',[(100,15),(110,15),(110,-8),(91.5,-8)],2.4,miter=True)
s.bridge('v042 court north gateway bridge',[(88.5,-8),(52,-8),(52,-13)],2.4,miter=True)
s.bridge('v042 utility waterside walk',[(90,-9.5),(90,-36),(90,-38)],2.4,miter=True,open_land_end=True)
c.box('v042 three way open bridge landing',(90,-8,-.16),(3,3,.30),pave)
s.glass_rail((88.5,-6.5),(91.5,-6.5),name='v042 junction outside guard')
s.ribbon('v042 utility connection apron',[(90,-38),(99,-38),(99,-42)],2.4,pave,-.01,.20,miter=True)
solid_polygon('v042 utility apron earth support',[(88,-43),(102,-43),(102,-35),(88,-35)],-.08,-2.0,lawn)
# Connect west-side circulation to the relocated gate and preserve the existing Daosi road.
s.ribbon('v042 gate west garden connection',[(-42,-22),(-49,-7),(-50,20),(-50,47)],3,pave,-.01,.20,miter=True)

c.collection('383_South_Lotus_Bay_Vegetation')
rng=random.Random(420347);v=[];f=[];ids=[];stems=[];sf=[]
lotus=[bpy.data.materials[name] for name in ['Heyu lotus leaf dark','Heyu lotus leaf middle','Heyu lotus leaf pale'] if name in bpy.data.materials]
if not lotus:lotus=[bpy.data.materials['Lotus leaf green']]
# Dense broad bed, matching the aerial bay silhouette. Keep bridge corridors clear.
leaf_regions=[(44,7,28,15),(68,-1,12,10)]
for i in range(2600):
 cx,cy,rx,ry=leaf_regions[i%2];a=rng.random()*math.tau;r=math.sqrt(rng.random());x=cx+rx*r*math.cos(a);y=cy+ry*r*math.sin(a)
 if x<15 or y<-11 or y>26 or (y>20 and x<27) or (x>52 and y>23):continue
 z=rng.uniform(-.46,-.10);rad=rng.uniform(.23,.53);start=len(v);v.append((x,y,z-.06))
 for j in range(17):
  theta=.15+j*(math.tau-.3)/16;v.append((x+rad*math.cos(theta),y+rad*math.sin(theta),z+.035*math.sin(theta*3)))
 for j in range(16):f.append((start,start+j+1,start+j+2));ids.append(i%len(lotus))
 c.tube_data(stems,sf,(x,y,-1.7),(x,y,z-.06),.008,.008,5)
c.mesh('v042 broad lotus bay leaves',v,f,lotus,ids);c.mesh('v042 lotus bay stems',stems,sf,lotus[0])
# Low planting defines the bank without obscuring the corrected spatial layout.
for i,(x,y) in enumerate([(7,-5),(8,10),(18,27),(31,34),(44,37),(-39,-4),(-44,17)]):
 c.tree('v042 bank broadleaf',x,y,7.2,2.5,4200+i,True)

c.collection('384_South_Registered_Street')
road=s.smooth_path([(-80,-61),(-52,-61),(-36,-62),(-26,-62),(-12,-62),(6,-59),(36,-59),(68,-59),(89,-60)],12)
asphalt=bpy.data.materials['Daosi dark worn asphalt']
s.ribbon('v042 south approach public road',road,7.0,asphalt,-.012,.20)
for side in [-1,1]:s.ribbon('v042 south road kerb',s.offset(road,side*3.6),.22,p['stone'],.035,.20)
s.ribbon('v042 south road centre marking',road,.09,bpy.data.materials['Daosi aged ivory lane paint'],-.006,.004)
c.box('v042 public road to gate forecourt apron',(-26,-57.5,-.10),(24,5,.184),pave)

c.collection('385_South_Layout_Review_Cameras')
c.camera('186_South_registered_aerial',(166,-174,162),(18,0,0),43)
c.camera('187_Tennis_registered_school_view',(31,-42,1.72),(0,54,8.5),22)
c.camera('188_South_gate_registered_axis',(-24,-18,1.72),(0,48,7),25)
c.camera('189_Heyu_registered_shore',(119,-36,29),(69,10,0),32)
sc['tennis_grid']='Four courts in one X row: (22,-31),(40,-31),(58,-31),(76,-31), long axis Y; divider (48.9,-31)'
sc['south_layout_revision']='v042 image-ground registration, rounded estimates; school fixed, no survey claim'
sc['render_review_samples']=96
for key in ['retired_objects','transformed_objects','modified_objects']:changes[key]=sorted(set(changes[key]))
(out/'replacement_scope.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf8')
h.save(42,'South precinct aerial layout correction: rigid gate/court/island/utility moves around fixed school, connected plaza, broad lotus bay, shore and pedestrian routes. Preserve existing court dimensions and main-campus refinements. Ground image registration remains an estimate; deferred south wall content unchanged inside translated gate.',[347,348,349,352,353,354,359,364,365,366],'186_South_registered_aerial')
