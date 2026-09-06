"""v014: Heyu island, banyans, variegated banks, lotus beds and entry bridge.
Reference 364 F/B/L and 365 F/B/L. Shoreline and heights remain estimates.
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
p=n.palette();rng=random.Random(1364)
c.collection('110_Heyu_Lake_And_Shore')
# Close the previously reserved ground between the entrance garden and courts.
infill=s.mottled('Heyu connecting bank lawn',[(.09,.15,.023),(.23,.25,.06)],1.5)
c.box('Heyu mainland garden to tennis land infill',(54.3,15,-.50),(10.6,58,.89),infill)
c.box('Heyu court west edge soil infill',(62,8,-.50),(6.0,42,.89),infill)
c.box('Heyu court east edge soil infill',(103.25,8,-.50),(4.9,36,.89),infill)
c.box('Heyu southern court landscape infill',(72,-17,-.50),(75,8,.89),infill)
poly=[(61.9,26),(120,26),(135,60),(135,145),(90,145),(90,71),(61.9,71)]
water=s.mottled('Heyu green lake water',[(.070,.115,.078),(.16,.22,.13)],.15,.19)
bs=water.node_tree.nodes.get('Principled BSDF');bs.inputs['Metallic'].default_value=.18
bs.inputs['Coat Weight'].default_value=.32
c.mesh('Heyu connected east lake surface',[(x,y,-1.15) for x,y in poly],[tuple(range(len(poly)))],water)
c.mesh('Heyu lake bed',[(x,y,-2.7) for x,y in poly],[tuple(range(len(poly)))],p['seam'])
c.box('Heyu mainland retained bank',(62.25,37.5,-.94),(5.5,25,1.8),p['stone'])
# An irregular tapered island, above a genuine closed retaining wall.
outline=[]
for i in range(128):
 a=i*math.tau/128;rx=11*(1+.035*math.sin(3*a));ry=6.5*(1+.12*math.cos(a))
 outline.append((79+rx*math.cos(a),42+ry*math.sin(a)))
v=[(x,y,-.04) for x,y in outline]+[(x,y,-1.85) for x,y in outline]
f=[tuple(range(128)),tuple(reversed(range(128,256)))]
for i in range(128):j=(i+1)%128;f.append((i,128+i,128+j,j))
shore=s.mottled('Heyu rough grey island revetment',[(.22,.24,.19),(.42,.43,.34)],4.5)
c.mesh('Heyu closed island soil and revetment',v,f,shore)
lawn=s.mottled('Heyu patchy dry grass base',[(.10,.14,.025),(.28,.27,.10)],2.2)
c.mesh('Heyu grass island top',[(x,y,-.036) for x,y in outline],[tuple(range(128))],lawn)
c.collection('111_Heyu_Paths_And_Entry_Bridge')
path=[(70,44),(77,42),(87,42)]
stone=n.paving('Waterside fine rectangular granite',(.59,.60,.54),(.6,.3),.004)
s.ribbon('Heyu island continuous stone path',path,2.4,stone,-.01,.17)
s.bridge('Heyu mainland entry bridge',[(63.5,44),(70,44)],2.4)
for side in [-1,1]:s.ribbon('Heyu island flat edge band',s.offset(path,side*1.21),.16,p['stone'],-.004,.16)
def distance_to_path(x,y):
 q=Vector((x,y));d=999
 protected_path=[(63.5,44)]+path
 for a,b in zip(protected_path,protected_path[1:]):
  a,b=Vector(a),Vector(b);v=b-a;t=max(0,min(1,(q-a).dot(v)/v.length_squared));d=min(d,(q-(a+t*v)).length)
 return d
c.collection('112_Heyu_Variegated_Banks_And_Lawn')
mats=[c.material('Heyu strap leaf pale margin',(.46,.49,.25)),c.material('Heyu strap leaf green centre',(.12,.23,.06)),c.material('Heyu strap leaf dry ochre',(.30,.23,.07))]
v,f,ids=[],[],[]
for i in range(220):
 a=i*math.tau/220;x=79+10.5*math.cos(a);y=42+6.0*(1+.12*math.cos(a))*math.sin(a)
 if distance_to_path(x,y)<1.55:continue
 for j in range(22):
  ang=rng.random()*math.tau;reach=rng.uniform(.30,.63);h=rng.uniform(.28,.58)
  for k in range(7):
   t=k/7;u=(k+1)/7
   def point(t,off):
    w=.025*math.sin(math.pi*t)**.6
    return(x+math.cos(ang)*reach*t-math.sin(ang)*w*off,y+math.sin(ang)*reach*t+math.cos(ang)*w*off,-.01+h*math.sin(math.pi*t*.80))
   st=len(v);v.extend([point(t,-1),point(t,-.55),point(t,.55),point(t,1),point(u,-1),point(u,-.55),point(u,.55),point(u,1)])
   for jdx in range(3):f.append((st+jdx,st+jdx+1,st+jdx+5,st+jdx+4));ids.append(1 if jdx==1 else (2 if j%7==0 else 0))
c.mesh('Heyu arching variegated strap foliage',v,f,mats,ids)
v,f=[],[]
for i in range(16000):
 x=rng.uniform(68,90);y=rng.uniform(35,49)
 if ((x-79)/10.5)**2+((y-42)/5.7)**2>1 or distance_to_path(x,y)<1.4:continue
 h=rng.uniform(.035,.15);st=len(v);v.extend([(x-.006,y,-.015),(x+.006,y,-.015),(x+.025,y+.018,h)]);f.append((st,st+1,st+2))
c.mesh('Heyu sparse grass blades',v,f,c.material('Heyu grass blades',(.16,.23,.042)))
c.collection('113_Heyu_Banyans_And_Aerial_Roots')
bark=s.mottled('Heyu banyan grey fibrous bark',[(.18,.17,.12),(.36,.33,.24)],11)
for j,(x,y,scale) in enumerate([(72,38.8,.82),(81.5,46.1,.78),(87,38.7,.62)]):
 s.tree(x,y,scale,j*.8)
 # Buttress roots and multiple trunks preserve the silhouette of the waterside banyans.
 for k in range(9):
  a=k*math.tau/9
  c.rod('Heyu banyan fluted fused trunk',(x+.22*math.cos(a),y+.22*math.sin(a),0),(x+.32*math.cos(a+.25),y+.32*math.sin(a+.25),3.0*scale),.15,bark,.06,9)
  c.rod('Heyu banyan buttress root',(x+1.45*scale*math.cos(a),y+1.45*scale*math.sin(a),-.035),(x+.18*math.cos(a),y+.18*math.sin(a),1.05*scale),.07,bark,.16,8)
 v,f=[],[]
 for k in range(120):
  a=rng.random()*math.tau;r=rng.uniform(.3,2.25)*scale;xx=x+r*math.cos(a);yy=y+r*math.sin(a)
  if distance_to_path(xx,yy)<1.4:continue
  high=rng.uniform(2.8,4.0)*scale;low=rng.uniform(.5,2.0)*scale
  anchor=(x+.06,y+.025,high+.24)
  fork=(x+(xx-x)*.65,y+(yy-y)*.65,high+.12)
  c.tube_data(v,f,anchor,fork,.035,.018,8)
  c.tube_data(v,f,fork,(xx,yy,high),.018,.008,6)
  last=(xx,yy,high)
  for t in range(1,6):
   end=(xx+.05*math.sin(t),yy+.03*math.sin(t*1.7),high+(low-high)*t/5)
   c.tube_data(v,f,last,end,.008,.006,5);last=end
 c.mesh('Heyu hanging banyan aerial roots',v,f,bark)
for obj in c.COL.objects:
 if obj.type=='MESH' and obj.data.materials and obj.data.materials[0]==bark:
  for face in obj.data.polygons:face.use_smooth=True
c.collection('114_Heyu_Lotus_Beds')
lotusm=[c.material('Heyu lotus fresh green',(.11,.25,.11),.63),c.material('Heyu lotus blue green',(.095,.20,.17),.63),c.material('Heyu lotus autumn brown',(.27,.17,.055),.8)]
v,f,ids=[],[],[];stems,stemf=[],[];flowers,flowerf=[],[]
for i in range(620):
 x=rng.uniform(66,100);y=rng.uniform(27.7,53)
 if ((x-79)/12.0)**2+((y-42)/7.3)**2<1 or (y>34 and x>91):continue
 if distance_to_path(x,y)<1.6:continue
 z=rng.uniform(-.87,-.12);r=rng.uniform(.28,.60)
 c.tube_data(stems,stemf,(x,y,-1.6),(x,y,z),.012,.008,5)
 st=len(v);v.append((x,y,z-.055));angle=rng.uniform(0,math.tau)
 for k in range(25):
  a=angle+.13+(math.tau-.26)*k/24
  v.append((x+r*math.cos(a),y+r*math.sin(a),z+.09*math.sin(a*3)+.05))
 for k in range(24):f.append((st,st+k+1,st+k+2));ids.append(i%3 if i%6==0 else i%2)
 if i%31==0:
  for k in range(12):
   a=k*math.tau/12;st=len(flowers);flowers.extend([(x,y,z+.05),(x+.08*math.cos(a-.4),y+.08*math.sin(a-.4),z+.19),(x+.15*math.cos(a),y+.15*math.sin(a),z+.28),(x+.08*math.cos(a+.4),y+.08*math.sin(a+.4),z+.19)]);flowerf.append((st,st+1,st+2,st+3))
c.mesh('Heyu lotus individual cupped leaves',v,f,lotusm,ids)
c.mesh('Heyu lotus stems',stems,stemf,lotusm[0])
c.mesh('Heyu occasional pink lotus petals',flowers,flowerf,c.material('Heyu lotus pink',(.56,.17,.26),.63))
c.collection('115_Heyu_Lights_And_Lifesaving')
for x,y in [(70,46.0),(79,44.0),(88,44)]:s.slit_lamp(x,y)
c.rod('Heyu camera pole',(68,46.5,-.03),(68,46.5,3.5),.040,p['seam'],sides=12)
c.rod('Heyu camera arm',(68,46.5,3.3),(68.45,46.5,3.3),.025,p['seam'])
l.ellipsoid('Heyu security camera housing',(68.46,46.5,3.14),(.105,.10,.15),p['white'],16,8)
# Life ring near the mainland bridgehead, with four distinct white bands.
orange=c.material('Heyu rescue ring orange',(.85,.12,.015),.56)
v,f=[],[]
for i in range(64):
 a=i*math.tau/64;b=(i+1)*math.tau/64
 c.tube_data(v,f,(64.3+.34*math.cos(a),46,.85+.34*math.sin(a)),(64.3+.34*math.cos(b),46,.85+.34*math.sin(b)),.075,.075,8)
c.mesh('Heyu orange lifebuoy',v,f,orange)
for z in [.3,1.2]:c.box('Heyu lifebuoy stand',(64.3,46.15,z),(.06,.07,.60),p['steel'])
c.collection('118_Heyu_Cameras')
c.camera('54_Heyu_island_and_banyans',(68.7,44.0,1.72),(84,42,2.0),26)
c.camera('55_Heyu_bridge_toward_campus',(74,43.5,1.72),(43,55,8),26)
c.camera('56_Heyu_lotus_and_courts',(88,42,1.72),(82,22,1.0),26)
c.camera('57_Heyu_overview',(122,14,44),(76,40,0),42)
sc.camera=sc.objects['54_Heyu_island_and_banyans']
sc['scope']='Existing campus, tennis and Daosi preserved. Added Heyu island and mainland entry bridge. Shuinan eastern bridge is next.'
c.save(c.ROOT/'models/campus/WZMS_Campus_v014.blend','v0.0.14',[119232364,119232365])
print('WZMS_BUILD_COMPLETE v0.0.14',flush=True)
