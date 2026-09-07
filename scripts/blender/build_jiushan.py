"""v020 Jiushan Road four-view sequence, blue arches, garden junction, yellow bridge."""
import bpy,sys,math,random
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).parent))
import campus_common as c,north_common as n,north_landscape as l,south_detail_common as s,culture_common as k
sc=bpy.data.scenes['WZMS_Campus'];c.activate(sc);p=n.palette();rng=random.Random(1382)
stone=n.paving('Jiushan fine grey pedestrian paving',(.42,.45,.44),(.60,.32),.006)
yellow=c.material('Jiushan warm yellow lane paint',(.85,.51,.015),.66)
blue=c.material('Jiushan bright blue bridge enamel',(.02,.38,.65),.30,.45)
railyellow=c.material('Jiushan yellow bridge enamel',(.83,.49,.02),.34,.42)
ground=s.mottled('Jiushan shaded grass soil',[(.09,.13,.025),(.27,.28,.09)],1.8)
bank=s.mottled('Jiushan grey masonry water bank',[(.22,.24,.21),(.44,.46,.40)],3.0)
c.collection('160_Jiushan_East_Water_And_Land')
# Meets the existing Heyu water at x135. Ground/structure above masks the seam.
water=bpy.data.materials['Heyu green lake water']
c.box('Jiushan east cultural lake extension',(217.5,130,-1.18),(165,140,.06),water)
c.box('Jiushan east cultural lake bed',(217.5,130,-2.72),(165,140,.08),p['seam'])
main=[(139,136),(172,136),(172,108),(180,100)]
s.ribbon('Jiushan mainland supporting land',main,11.5,ground,-.025,.95,miter=True)
s.ribbon('Jiushan glass facade branch land',[(172,108),(172,93)],12.0,ground,-.025,.95)
outline=[]
for i in range(120):
 a=i*math.tau/120;outline.append((205+10.1*(1+.07*math.sin(3*a))*math.cos(a),106+17*math.sin(a)))
v=[(x,y,-.025) for x,y in outline]+[(x,y,-1.85) for x,y in outline];f=[tuple(range(120)),tuple(reversed(range(120,240)))]
for i in range(120):j=(i+1)%120;f.append((i,j,j+120,i+120))
c.mesh('Jiushan garden junction island revetment',v,f,bank)
c.mesh('Jiushan garden junction island grass',[(x,y,-.02) for x,y in outline],[tuple(range(120))],ground)
c.collection('161_Jiushan_Paved_Links_And_Bridge_Decks')
garden=[(200,100),(207,106),(212,112)]
for name,poly in [('Mainland',main),('Garden junction',garden),('Glass facade branch',[(172,108),(172,93)])]:
 s.ribbon('Jiushan '+name+' paving',poly,5.2,stone,0,.20,miter=True)
 s.ribbon('Jiushan '+name+' yellow centre line',poly,.085,yellow,.008,.005,miter=True)
 for sign in [-1,1]:s.ribbon('Jiushan '+name+' light granite kerb',s.miter_offset(poly,sign*2.68),.16,p['stone'],.045,.20,miter=True)
# Small garden side entrance observed at the junction, with an open rectangular frame.
side=[(207,106),(210,102),(211,96)]
s.ribbon('Jiushan garden side path',side,2.1,stone,.004,.15,miter=True)
s.segment('Jiushan yellow junction branch',(207,106),(208.6,103.9),.085,yellow,.012,.005)
for x in [209.7,212.3]:c.box('Jiushan white garden gateway pier',(x,96,1.65),(.25,.30,3.3),p['white'])
c.box('Jiushan white garden gateway lintel',(211,96,3.26),(3.0,.38,.28),p['white'])
c.box('Jiushan reserved history bridgehead landing',(237.5,112,-.1),(3.1,6,.2),stone)
def bridge(name,a,b,mat,arches=False):
 a,b=Vector(a),Vector(b);d=(b-a).normalized();normal=Vector((-d.y,d.x));length=(b-a).length
 s.ribbon(name+' structural deck',[a,b],5.2,stone,0,.42)
 s.ribbon(name+' yellow centre line',[a,b],.085,yellow,.008,.005)
 for sign in [-1,1]:
  aa=a+normal*sign*2.57;bb=b+normal*sign*2.57
  s.segment(name+' dark raised kerb',aa,bb,.23,p['seam'],.10,.20)
  for h in ([.50,.88] if arches else [.32,.53,.74,1.02,1.22]):
   if arches:c.rod(name+' continuous painted rail',(*aa,h),(*bb,h),.033,mat,sides=10)
   else:s.beam(name+' rectangular yellow horizontal rail',(*aa,h),(*bb,h),.05,.065,mat)
  if arches:
   count=round(length/2.2);span=length/count;v,f=[],[]
   for j in range(count):
    for q in range(24):
     u=q/24;w=(q+1)/24;pp=aa+d*(j*span+span*.5*(1-math.cos(math.pi*u)));rr=aa+d*(j*span+span*.5*(1-math.cos(math.pi*w)))
     c.tube_data(v,f,(*pp,.12+1.10*math.sin(math.pi*u)),(*rr,.12+1.10*math.sin(math.pi*w)),.046,.046,10)
    for fraction in [.25,.5,.75]:
     pp=aa+d*((j+fraction)*span);c.tube_data(v,f,(*pp,.12),(*pp,.12+1.1*math.sqrt(1-(2*fraction-1)**2)),.025,.025,8)
   c.mesh(name+' repeating semicircle blue balustrade',v,f,mat)
  else:
   for j in range(math.ceil(length/1.7)+1):
    pt=aa.lerp(bb,j/math.ceil(length/1.7));c.box(name+' yellow upright',(*pt,.68),(.10,.10,1.2),mat)
  for j in range(int(length/.6)+1):
   pt=aa+d*(j*.6);c.box(name+' deck drainage slot',(*pt,.109),(.14,.06,.01),p['dark'])
 for j in range(1,math.ceil(length/6)):
  pt=a.lerp(b,j/math.ceil(length/6));c.box(name+' concrete pier',(*pt,-1.02),(3.4,.6,1.25),bank)
 for end in [a,b]:s.segment(name+' expansion strip',end-normal*2.5,end+normal*2.5,.07,p['dark'],.003,.008)
bridge('Jiushan blue arch bridge',(180,100),(200,100),blue,True)
bridge('Jiushan yellow rail bridge',(212,112),(237,112),railyellow)
c.collection('162_Jiushan_Shade_Trees_And_Ground_Planting')
# Keep stems, shrubs and low foliage outside the actual pedestrian envelopes.
for i,(x,y,scale) in enumerate([(177.7,133,.82),(177.7,120,.8),(177,111,.75),(200,113,.80),(202,120,.80),(208,119,.72),(199,93,.70),(209,91,.7)]):
 s.tree(x,y,scale,i*.7)
for i,(x,y) in enumerate([(177.1,126),(177,116),(201,118),(208,116.5),(211,91.5),(198.8,91)]):
 l.shrub('Jiushan low evergreen bank',x,y,.50,1.3,13820+i)
for x,y in [(177.5,96),(205,92.5)]:n.palm('Jiushan sago palm',x,y,1.2,int(x*y))
for x,y in [(175.8,131),(175.8,116),(202,115.5),(210,119),(198,94)]:l.lamp(x,y)
for x,y in [(200,118),(175.6,124)]:l.bench(x,y,math.pi/2)
for x,y in [(175.5,119),(203,116)]:
 c.box('Jiushan waste bin body',(x,y,.48),(.45,.45,.9),p['dark'],.04)
 c.box('Jiushan waste bin stainless lid',(x,y,.95),(.52,.52,.06),p['steel'],.025)
 c.box('Jiushan waste bin opening',(x,y-.231,.77),(.31,.014,.18),coping if 'coping' in globals() else p['seam'])
for x,y in [(210,98.5),(201,121),(177.1,128)]:l.ellipsoid('Jiushan garden landscape stone',(x,y,.43),(.75,.48,.64),bank,16,10)
# Narrow permeable strip and service detail along the adjacent glass facade.
for j in range(27):
 y=94+j*.30
 for x in [167.15,167.55,167.95]:
  c.box('Jiushan grass paver concrete',(x,y,-.005),(.33,.25,.07),p['stone'])
  c.box('Jiushan grass paver opening',(x,y,.032),(.19,.13,.004),ground)
for y in [95.5,99.5]:
 c.box('Jiushan facade condenser enclosure',(167.05,y,.48),(.46,.84,.58),p['white'],.015)
 for q in range(9):c.box('Jiushan condenser ventilation louvre',(167.295,y-.32+q*.08,.48),(.015,.018,.44),p['seam'])
k.pot(167.5,101.2,0,.75,seed=380)
c.collection('168_Jiushan_Review_Cameras')
c.camera('76_Jiushan_glass_facade',(172,105,1.7),(165,96,4.2),25)
c.camera('77_Jiushan_blue_bridge',(181,100,1.7),(204,101,1.9),28)
c.camera('78_Jiushan_garden_junction',(202,102,1.7),(214,113,1.8),25)
c.camera('79_Jiushan_yellow_bridge',(217,112,1.7),(237,112,1.7),28)
c.camera('80_Jiushan_network_overview',(261,60,67),(182,117,1),40)
sc.camera=sc.objects['77_Jiushan_blue_bridge'];sc['scope']='Jiushan four-point exterior sequence: paving, yellow guidance line, blue arch bridge, garden junction, yellow bridge; estimated distances and shoreline; museum landing reserved.'
c.save(c.ROOT/'models/campus/WZMS_Campus_v020.blend','v0.0.20',[119232380,119232381,119232382,119232383])
print('WZMS_BUILD_COMPLETE v0.0.20',flush=True)
