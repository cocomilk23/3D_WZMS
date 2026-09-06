"""v015: Shuinan folded pedestrian bridge, court-side peninsula and utility room.
Source 365 F/B/L and 364 F. Estimated local geometry, not surveyed coordinates.
"""
import bpy,sys,math,random
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).parent))
import campus_common as c
import north_common as n
import north_landscape as l
import south_detail_common as s
sc=bpy.data.scenes['WZMS_Campus'];c.activate(sc);p=n.palette()
# Trim complete procedural leaf strips only where the new island exit is joined.
# This is a documented local adjustment to two v014 planting meshes.
import bmesh
for object_name,group_size in [('Heyu arching variegated strap foliage',56),('Heyu sparse grass blades',3)]:
 obj=bpy.data.objects[object_name];mesh=obj.data;remove=set()
 for start in range(0,len(mesh.vertices),group_size):
  indices=range(start,min(start+group_size,len(mesh.vertices)))
  if any(86.8<=mesh.vertices[i].co.x<=91 and 40.55<=mesh.vertices[i].co.y<=43.45 for i in indices):remove.update(indices)
 bm=bmesh.new();bm.from_mesh(mesh);bm.verts.ensure_lookup_table()
 bmesh.ops.delete(bm,geom=[f for f in bm.faces if any(v.index in remove for v in f.verts)],context='FACES_ONLY')
 bm.to_mesh(mesh);bm.free();mesh.update()
c.collection('120_Shuinan_Continuous_Bridge')
points=[(87,42),(106,42),(106,23),(101,23)]
s.bridge('Shuinan folded waterside bridge',points,2.4,miter=True,open_land_end=True)
c.collection('121_Shuinan_Peninsula_And_Path')
outline=[(101,16),(113,16),(117,21),(116,27),(111,31),(106,31),(102,27),(101,26)]
v=[(x,y,-.04) for x,y in outline]+[(x,y,-1.9) for x,y in outline]
k=len(outline);f=[tuple(range(k)),tuple(reversed(range(k,k*2)))]
for i in range(k):j=(i+1)%k;f.append((i,k+i,k+j,j))
soil=s.mottled('Shuinan irregular earth bank',[(.15,.12,.07),(.32,.27,.14)],6)
c.mesh('Shuinan closed peninsula bank',v,f,soil)
grass=s.mottled('Shuinan peninsula grass',[(.09,.15,.022),(.24,.26,.068)],1.9)
c.mesh('Shuinan peninsula lawn',[(x,y,-.034) for x,y in outline],[tuple(range(k))],grass)
path=n.paving('Waterside fine rectangular granite',(.59,.60,.54),(.6,.30),.004)
s.segment('Shuinan room approach',(106,23),(106,19),2.4,path)
s.segment('Shuinan utility threshold approach',(106,19),(110,19),2.4,path)
# Vertical baluster fence changes from glass to metal on the solid peninsula.
for a,b in [((111,30.8),(116,26.5)),((116,26.5),(116.7,21)),((116.7,21),(113,16.2))]:
 a,b=Vector(a),Vector(b);length=(b-a).length;steps=math.ceil(length/.16)
 s.beam('Shuinan land railing upper rail',(*a,1.05),(*b,1.05),.055,.055,p['steel'])
 s.beam('Shuinan land railing bottom rail',(*a,.15),(*b,.15),.03,.03,p['steel'])
 for j in range(steps+1):
  q=a.lerp(b,j/steps);c.rod('Shuinan land fence vertical',(*q,.15),(*q,1.05),.016,p['steel'],sides=6)
c.collection('122_Shuinan_Grey_Utility_Room')
grey=s.mottled('Shuinan utility light grey panels',[(.43,.45,.42),(.59,.60,.54)],3.3)
joint=c.material('Shuinan utility panel dark joints',(.085,.105,.104))
blue=c.material('Shuinan utility blue door glass',(.035,.20,.28),.20,.3)
c.box('Shuinan utility concrete base',(112,20,.04),(4.2,5.2,.18),p['stone'])
# Walls and roof are separate editable components; unseen interior stays empty.
c.box('Shuinan utility east wall',(114,20,1.67),(.18,5,3.3),grey)
c.box('Shuinan utility south wall',(112,17.5,1.67),(4,.18,3.3),grey)
c.box('Shuinan utility north wall',(112,22.5,1.67),(4,.18,3.3),grey)
c.box('Shuinan utility west lower pier',(110,18.13,1.67),(.18,1.25,3.3),grey)
c.box('Shuinan utility west upper pier',(110,21.63,1.67),(.18,1.75,3.3),grey)
c.box('Shuinan utility door lintel',(110,19.755,2.94),(.18,2.0,.77),grey)
c.box('Shuinan utility flat roof',(112,20,3.34),(4.15,5.15,.16),grey)
c.box('Shuinan utility west door reveal',(109.94,19.755,1.32),(.025,2.0,2.46),p['dark'])
c.box('Shuinan utility blue service door',(109.916,19.7,1.31),(.025,1.34,2.35),blue)
for yy in [19.04,19.7,20.36]:c.box('Shuinan utility door aluminium mullion',(109.89,yy,1.31),(.07,.04,2.40),p['white'])
for z in [.17,1.2,2.49]:c.box('Shuinan utility door cross frame',(109.89,19.7,z),(.07,1.38,.05),p['white'])
c.rod('Shuinan utility door handle',(109.84,19.56,.9),(109.84,19.56,1.18),.014,p['steel'])
for xx in [110.8,111.6,112.4,113.2]:
 c.box('Shuinan utility north panel vertical joint',(xx,22.597,1.67),(.013,.012,3.3),joint)
 c.box('Shuinan utility south panel vertical joint',(xx,17.403,1.67),(.013,.012,3.3),joint)
for yy in [18.3,19.1,19.9,20.7,21.5]:
 c.box('Shuinan utility east panel seam',(114.097,yy,1.67),(.012,.013,3.3),joint)
for z in [1.10,2.19]:
 for yy in [17.401,22.599]:c.box('Shuinan utility horizontal panel seam',(112,yy,z),(4,.012,.012),joint)
c.box('Shuinan utility high vent frame',(110.35,22.61,2.7),(.42,.04,.35),p['dark'])
for z in [2.59,2.66,2.73,2.80]:c.box('Shuinan utility high vent louvre',(110.35,22.65,z),(.37,.08,.025),p['steel'])
c.collection('123_Shuinan_Trees_And_Furniture')
s.tree(113.6,26.5,.94,2.1)
c.tree('Shuinan young supported tree',108.8,27.4,4.5,1.0,1365,False)
for x,y in [(108,30),(104,17.3),(115,24.3)]:s.slit_lamp(x,y)
for x,y in [(111,29.8),(115.4,23.8),(103,17.2)]:l.shrub('Shuinan low shore shrubs',x,y,.42,.7,int(x*y))
for i in range(45):
 a=i*math.tau/45;x=111.6+4.5*math.cos(a);y=24.2+5.8*math.sin(a)
 if x<107.6 or (x<114.5 and y<23.1):continue
 l.ellipsoid('Shuinan shoreline rounded stones',(x,y,-.31),(.28,.22,.22),p['seam'],9,5)
# A loose tennis ball in the archived waterside view; separate removable prop.
l.ellipsoid('Shuinan stray tennis ball',(106.65,34.2,.025),(.033,.033,.033),c.material('Shuinan tennis ball felt',(.53,.68,.025)),16,8)
c.collection('128_Shuinan_And_Southern_Integration_Cameras')
c.camera('58_Shuinan_toward_island',(106,37,1.72),(76,43,2.1),25)
c.camera('59_Shuinan_toward_court_peninsula',(106,39,1.72),(108,22,1.5),27)
c.camera('60_Shuinan_court_and_lotus',(104,42,1.72),(83,22,1.2),24)
c.camera('61_Shuinan_bridge_overview',(135,67,48),(91,32,0),42)
c.camera('62_Southern_four_scene_integration',(195,-150,175),(0,65,0),38)
sc.camera=sc.objects['58_Shuinan_toward_island']
sc['scope']='Southern batch complete as editable exterior initial versions: tennis, Daosi Qian Road, Heyu island, Shuinan waterside bridge. Prior northward campus retained.'
sc['user_acceptance']='Pending user review; strict 1:1 survey calibration and UE walk-through remain future work'
c.save(c.ROOT/'models/campus/WZMS_Campus_v015.blend','v0.0.15',[119232365,119232364,119232359])
print('WZMS_BUILD_COMPLETE v0.0.15',flush=True)
