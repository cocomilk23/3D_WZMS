"""v019 photo-supported mathematics museum gate and courtyard; no exhibit interiors."""
import bpy,sys,math,random
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import campus_common as c,north_common as n,north_landscape as l,culture_common as k,south_detail_common as s
sc=bpy.data.scenes['WZMS_Campus'];c.activate(sc);p=n.palette()
white=c.material('Math white rendered plaster',(.78,.76,.70),.84);c.noise(white,130,.13,.008)
coping=c.material('Math charcoal coping',(.045,.041,.038),.59)
red=c.material('Math reference red carpet',(.56,.018,.024),.95);c.noise(red,200,.3,.005)
stone=n.paving('Math approach grey rectangular pavers',(.41,.43,.41),(.55,.30),.009)
soil=c.material('Math dry courtyard planting soil',(.30,.25,.14),.98)
bronze=c.material('Math bronze lattice metal',(.13,.08,.045),.46,.62)
glass=c.material('Math blue green curtain glazing',(.085,.28,.29),.15,.35)
c.collection('150_Math_Podium_Approach_And_Courtyard')
c.box('Math connected cultural podium',(149.5,116,-.18),(39,42,.34),p['stone'])
c.box('Math approach and courtyard paving',(150,116,-.02),(38,42,.04),stone)
c.box('Math library south connection',(123,136,-.085),(22,4,.15),stone)
c.box('Math west library connecting path',(132,121.5,-.07),(3.8,31,.12),stone)
# Irregular courtyard flagstone surface with Voronoi mortar, in actual world units.
flag=c.material('Math irregular dark grey flagstone',(.25,.27,.26),.82)
nd,lk=flag.node_tree.nodes,flag.node_tree.links;bs=nd.get('Principled BSDF');co=nd.new('ShaderNodeTexCoord');vo=nd.new('ShaderNodeTexVoronoi');vo.feature='DISTANCE_TO_EDGE';vo.inputs['Scale'].default_value=1.6
lk.new(co.outputs['Object'],vo.inputs['Vector']);ramp=nd.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.012;ramp.color_ramp.elements[0].color=(.57,.56,.50,1);ramp.color_ramp.elements[1].position=.025;ramp.color_ramp.elements[1].color=(.21,.24,.24,1);lk.new(vo.outputs['Distance'],ramp.inputs[0]);lk.new(ramp.outputs[0],bs.inputs['Base Color'])
c.box('Math courtyard flagstone surface',(150,124,.002),(29.8,23.6,.014),flag)
c.box('Math entrance red runner',(150,108,.012),(3.5,8,.012),red)
c.box('Math approach red cross runner',(150,104.1,.014),(22,1.8,.012),red)
for x in [143,157]:
 c.box('Math front planting bed',(x,108.1,.014),(8.8,5.8,.02),soil)
 for xx in [x-4.45,x+4.45]:c.box('Math front bed raised kerb',(xx,108.1,.09),(.10,5.9,.18),p['stone'])
for x,y,r in [(143,118,1.8),(157.2,122,2.0),(154,132,2.2)]:
 n.disk('Math clipped planting bed',x,y,.03,r,p['green'],48)
 l.shrub('Math clipped rounded hedge',x,y,.48,r,int(x*y))
c.collection('151_Math_White_Gateway_And_Moon_Lattice')
# Wall around the 2.9m open doorway. Window lattice has an actual circular void.
c.box('Math gate top wall',(151.075,112,3.14),(31.95,.30,.72),white)
c.box('Math gateway west jamb',(147.9,112,1.40),(1.3,.30,2.8),white)
c.box('Math gateway east wall',(159.25,112,1.40),(15.6,.30,2.8),white)
c.box('Math gateway far west pier',(136.8,112,1.4),(3.4,.30,2.8),white)
c.box('Math lattice stone sill',(142.5,112,.30),(8.0,.30,.6),white)
c.box('Math gateway dark coping',(151.075,112,3.54),(32.35,.43,.14),coping)
for xx in [156.4,158.3,160.2]:
 c.box('Math gateway wing tall window dark reveal',(xx,111.825,1.85),(.90,.04,2.70),coping)
 c.box('Math gateway wing tall glazed inset',(xx,111.795,1.85),(.76,.025,2.55),glass)
 for dx in [-.40,.40]:c.box('Math gateway wing tall window stile',(xx+dx,111.77,1.85),(.045,.06,2.61),bronze)
 for z in [.55,1.55,2.5,3.15]:c.box('Math gateway wing tall window transom',(xx,111.77,z),(.82,.06,.045),bronze)
for x in [148.52,151.48]:c.box('Math gate stone door reveal',(x,111.82,1.38),(.10,.08,2.76),p['stone'])
c.box('Math museum title plaque',(150,111.80,3.09),(2.5,.08,.50),coping,.018)
c.text('Math museum name','数 学 馆',(150,111.748,2.93),.41,c.material('Math plaque turquoise calligraphy',(.10,.42,.37),.42,.3))
# Decorative red unveiling ribbon visible in the source, unlettered and removable.
for x,sg in [(148.7,-1),(151.3,1)]:
 o=c.box('Math plaque ribbon tail',(x,111.73,3.01),(.09,.025,.66),red);o.rotation_euler.y=sg*.20
l.ellipsoid('Math plaque ribbon rosette',(150,111.70,3.4),(.14,.07,.12),red,20,12)
cx,cz=142.7,1.72;radius=.90;v,f=[],[]
for ix in range(52):
 for iz in range(15):
  x=138.65+ix*.149;z=.65+iz*.145
  for j in range(10):
   a=j*math.tau/10;b=(j+1)*math.tau/10
   aa=(x+.085*math.cos(a),111.985,z+.085*math.sin(a));bb=(x+.085*math.cos(b),111.985,z+.085*math.sin(b))
   if min(math.hypot(aa[0]-cx,aa[2]-cz),math.hypot(bb[0]-cx,bb[2]-cz))>radius+.02:c.tube_data(v,f,aa,bb,.009,.009,5)
c.mesh('Math small ring lattice with circular opening',v,f,bronze)
v,f=[],[]
for i in range(96):
 a=i*math.tau/96;b=(i+1)*math.tau/96;c.tube_data(v,f,(cx+radius*math.cos(a),111.98,cz+radius*math.sin(a)),(cx+radius*math.cos(b),111.98,cz+radius*math.sin(b)),.055,.055,10)
c.mesh('Math moon window round bronze surround',v,f,bronze)
for x in [138.58,146.42]:c.box('Math lattice vertical frame',(x,111.98,1.72),(.045,.075,2.22),bronze)
for x in [146.6,146.9,147.16]:c.box('Math lattice side vertical accent',(x,111.98,1.72),(.042,.075,2.22),bronze)
c.collection('152_Math_Exhibition_Exterior_Shells')
# Courtyard side wings, using separate walls and roofs with dark sloping profiles.
for x in [137.8,163.0]:
 inner=x+(3.8 if x<150 else -3.8)
 v=[(x,112.4,4.0),(inner,112.4,3.8),(inner,133.3,5.0),(x,133.3,6.8)]
 for j in range(4):
  aa,bb=v[j],v[(j+1)%4]
  c.mesh('Math wing wall following sloping roof',[(aa[0],aa[1],0),(bb[0],bb[1],0),bb,aa],[(0,1,2,3)],white)
 c.mesh('Math sloping dark wing roof',v,[(0,1,2,3)],coping)
 for y in [117,121,125,129]:
  xx=x-.14 if x<150 else x+.14
  c.box('Math tall narrow exterior glass',(xx,y,2.3),(.035,.72,2.6),glass)
  for yy in [y-.38,y+.38]:c.box('Math narrow window reveal',(xx,yy,2.3),(.06,.04,2.67),bronze)
  c.box('Math narrow window transom',(xx,y,2.0),(.06,.78,.04),bronze)
# Circular white room: wall ring and open courtyard doorway (south-facing).
cx,cy=145.5,128;r=4.2;v,f=[],[]
for i in range(96):
 a=i*math.tau/96;b=(i+1)*math.tau/96
 if abs((a+b)/2-math.pi*1.5)<.19:continue
 off=len(v);v.extend([(cx+rr*math.cos(t),cy+rr*math.sin(t),z) for z in [0,4.1] for rr,t in [(r,a),(r,b),(r-.2,b),(r-.2,a)]])
 f.extend([tuple(off+j for j in face) for face in [(0,1,5,4),(3,7,6,2),(4,5,6,7)]])
c.mesh('Math circular white gallery exterior',v,f,white)
c.rod('Math drum flat roof',(cx,cy,4.1),(cx,cy,4.23),r+.13,coping,sides=96)
c.box('Math circular room dark door',(cx,cy-r+.12,1.3),(1.5,.05,2.6),bronze)
for x in [cx-.7,cx+.7]:c.box('Math circular room doorway stone jamb',(x,cy-r-.05,1.4),(.1,.08,2.8),p['stone'])
c.collection('153_Math_Adjacent_Glass_Facade')
# Adjacent curtain-wall building faces the approach; only the visible exterior is detailed.
c.box('Math glass wing roof',(152,98,12.95),(29,8.8,.3),white)
for level in range(3):
 z=level*4.25
 c.box('Math glass wing floor edge',(152,98,z),(29,8,.25),p['stone'])
 for y in [94,102]:
  c.box('Math glass curtain wall',(152,y,z+2.12),(28.5,.05,4.0),glass)
  for x in range(138,168,2):c.box('Math curtain wall silver fin',(x,y+(.12 if y>98 else -.12),z+2.12),(.08,.26,4.23),p['white'])
  for h in [.6,2.1,3.65]:c.box('Math curtain horizontal transom',(152,y,z+h),(28.7,.12,.05),p['steel'])
 for x in [137.5,166.5]:
  c.box('Math curtain end glazing',(x,98,z+2.12),(.045,8,4.0),glass)
  for y in range(94,103,2):c.box('Math curtain end upright',(x,y,z+2.12),(.2,.07,4.2),p['white'])
for x in range(138,168,2):
 c.rod('Math roof angled sunshade rib',(x,102.16,10.8),(x,101.7,12.9),.045,p['white'])
c.collection('154_Math_Bougainvillea_And_Courtyard_Furniture')
def flowers(x,y,scale,seed):
 rng=random.Random(seed);potmat=c.material('Math dark octagonal flower pot',(.055,.036,.024),.46)
 c.rod('Math octagonal planter',(x,y,0),(x,y,.42*scale),.36*scale,potmat,.48*scale,8)
 k.arc('Math flower pot rim',x,y,.46*scale,.4*scale,bronze,width=.026*scale,steps=8)
 c.rod('Math flower woody trunk',(x,y,.3*scale),(x,y,2.8*scale),.055*scale,bronze,.02*scale,10)
 mats=c.foliage_materials('Math bougainvillea green ')+[c.material('Math magenta bracts',(.54,.009,.20),.75),c.material('Math bright pink bracts',(.79,.035,.38),.73)]
 v,f,mi=[],[],[]
 for tier in range(4):
  z=(.85+tier*.65)*scale;r=(.62-tier*.09)*scale
  xx=x+(tier%2-.5)*.40*scale
  for branch in range(5):
   ang=branch*math.tau/5+tier*.7
   c.rod('Math flowering lateral branch',(x,y,z-.30*scale),(xx+math.cos(ang)*r*.72,y+math.sin(ang)*r*.72,z),.020*scale,bronze,.006*scale,7)
  for i in range(950):
   a=rng.random()*math.tau;rr=r*rng.random()**.5;h=z+rng.uniform(-1,1)*math.sqrt(max(.03,1-(rr/r)**2))*.34*scale
   idx=rng.randrange(5) if rng.random()<.28 else rng.randrange(5,7)
   c.leaf_data(v,f,mi,(xx+rr*math.cos(a),y+rr*math.sin(a),h),rng.uniform(.07,.13)*scale,rng,idx)
 c.mesh('Math tiered bougainvillea canopy',v,f,mats,mi)
for i,(x,y,scale) in enumerate([(143.8,105.6,1.05),(143.8,108.6,.83),(156.2,105.6,1.08),(156.2,108.6,.88),(160,106.5,1.15),(139.5,106.5,1.15)]):flowers(x,y,scale,1900+i)
for x,y in [(153.6,115.4),(156,130),(140.3,119)]:k.pot(x,y,0,.80,seed=int(x*y))
for x,y in [(166.8,132.8),(135.4,117),(166.8,108)]:s.slit_lamp(x,y)
l.ellipsoid('Math courtyard scholar rock',(158.8,129.4,.75),(.6,.45,1.0),p['seam'],14,9)
c.collection('158_Math_Exterior_Review_Cameras')
c.camera('72_Math_gate_and_flowers',(149.5,102.5,1.67),(149.8,112.1,1.85),16)
c.camera('73_Math_courtyard_reverse',(152,120,1.7),(146.5,110,1.9),23)
c.camera('74_Math_glass_wing',(171,114,3.6),(150,100,6),30)
c.camera('75_Math_library_overview',(184,77,42),(140,131,4),39)
sc.camera=sc.objects['72_Math_gate_and_flowers'];sc['scope']='Mathematics museum white entrance, moon lattice, courtyard, flowers, red runner and adjacent glass facade; exhibition interiors deferred.'
c.save(c.ROOT/'models/campus/WZMS_Campus_v019.blend','v0.0.19',[119232395,119232396,119232380])
print('WZMS_BUILD_COMPLETE v0.0.19',flush=True)
