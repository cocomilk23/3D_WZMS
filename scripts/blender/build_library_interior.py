"""v018: observed library halls, atrium, straight and paired curved stairs.
No invented reading room plan or attributed portrait identity. Unseen details estimated.
"""
import bpy,sys,math,random
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import campus_common as c,north_common as n,culture_common as k,north_landscape as l
sc=bpy.data.scenes['WZMS_Campus'];c.activate(sc);p=n.palette()
wood=n.paving('Library oak fine vertical panels',(.43,.25,.11),(.18,3.9),.0015)
cream=c.material('Library warm white interior plaster',(.79,.76,.68),.8)
floor=bpy.data.materials['Library polished brown hall tile']
trim=c.material('Library ivory floor border',(.61,.56,.42),.29)
dark=c.material('Library ceiling dark shadow',(.035,.03,.025),.84)
c.collection('140_Library_Interior_Stair_Structure')
k.stairs('Library first floor central staircase',(121,155,0),(127.72,155,4.25),3.6,24,floor)
c.box('Library central second floor bridge',(134.86,155,4.12),(14.28,4,.26),floor)
for yy in [153.02,156.98]:
 k.rail('Library second floor bridge balustrade',[(128.2,yy,4.25),(133.2,yy,4.25)],True)
# A matched pair of quarter-circle stairs, modelled step by step and open above.
for sign in [-1,1]:
 count=26;v,f=[],[];inner,outer=5.9,7.7
 start=math.pi+sign*.16;span=math.pi/2-.16
 for i in range(count):
  a=start+sign*span*i/count;b=start+sign*span*(i+1)/count;z=4.25+4.25*(i+1)/count
  vv=[(130+r*math.cos(t),155+r*math.sin(t),h) for h in [z-.22,z] for r,t in [(inner,a),(outer,a),(outer,b),(inner,b)]]
  off=len(v);v.extend(vv);f.extend([tuple(off+j for j in face) for face in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]])
  k.arc('Library curved step anti slip',130,155,6.8,z+.003,p['dark'],a,b,width=.008,steps=2)
 c.mesh('Library paired curved stair treads',v,f,floor)
 for r in [5.94,7.66]:
  points=[(130+r*math.cos(start+sign*span*i/count),155+r*math.sin(start+sign*span*i/count),4.25+4.25*i/count) for i in range(count+1)]
  k.rail('Library curved oak topped steel handrail',points,True)
 yy=155+(-1 if sign==1 else 1)*7.9
 c.box('Library upper stair radial landing',(130,yy,8.37),(2.0,2.25,.26),floor)
# White fascia and balcony rails; gaps retain stair and central bridge passages.
for z,r in [(4.25,6),(8.5,8)]:
 intervals=[(.09,.84),(1.16,1.91)] if z<8 else [(.13,.44),(.56,.84),(1.16,1.44),(1.56,1.87)]
 for lo,hi in intervals:
  a0,a1=lo*math.pi,hi*math.pi
  pts=[(130+r*math.cos(a0+(a1-a0)*i/48),155+r*math.sin(a0+(a1-a0)*i/48),z) for i in range(49)]
  k.rail('Library atrium perimeter railing',pts,True)
  for h in [.06,.15,.23]:k.arc('Library curved white slab fascia',130,155,r,z-h,cream,a0,a1,.052,96)
c.collection('141_Library_Hall_Finishes_And_Niches')
# Timber-clad structural columns around the light well, outside the stair ribbon.
for i,a in enumerate([.18,.40,.62,.85,1.15,1.38,1.60,1.82]):
 angle=a*math.pi;x=130+8.6*math.cos(angle);y=155+8.6*math.sin(angle)
 c.box('Library tall oak clad atrium column',(x,y,6.22),(.62,.62,12.44),wood,.025)
 for z in [0,4.25,8.5]:c.box('Library timber column dark foot',(x,y,z+.12),(.67,.67,.24),dark)
# Lower hall wall linings, framed display panels and oak ceiling strips.
for base in [0,4.25]:
 for yy in [138.18,171.82]:
  c.box('Library hall wall lining',(128.5,yy,base+.50),(26.7,.025,1.0),cream)
  c.box('Library dark stone skirting',(128.5,yy-.03 if yy>150 else yy+.03,base+.095),(26.7,.04,.19),dark)
 for yy in [139.1,170.9]:c.box('Library floor border long',(128.5,yy,base+.004),(25,.13,.008),trim)
 for xx in [116,141]:c.box('Library floor border cross',(xx,155,base+.004),(.13,31.8,.008),trim)
 for ix in range(98):
  x=115.2+ix*.27
  # Two ceiling strips stop at the actual opening boundary.
  rad=6.12 if base==0 else 8.1;dx=x-130
  gap=math.sqrt(rad*rad-dx*dx) if abs(dx)<rad else 0
  spans=[(138.3,155-gap),(155+gap,171.7)] if gap else [(138.3,171.7)]
  for a,b in spans:
   if b-a>.1:c.box('Library oak slatted ceiling',(x,(a+b)/2,base+3.88),(.19,b-a,.065),wood)
 for x in [118,139]:
  for y in [143,149,161,167]:
   c.rod('Library recessed ceiling bezel',(x,y,base+3.81),(x,y,base+3.86),.13,p['steel'],sides=20)
   em=c.material('Library warm LED diffuser',(1,.81,.55),.35)
   eb=em.node_tree.nodes.get('Principled BSDF');eb.inputs['Emission Color'].default_value=(1,.78,.48,1);eb.inputs['Emission Strength'].default_value=3
   c.rod('Library warm ceiling downlight',(x,y,base+3.795),(x,y,base+3.815),.105,em,sides=20)
 for x,y in [(118,144),(118,166),(139,145),(139,165),(119,155)]:k.area('Library interior diffuse illumination',(x,y,base+3.65),650,4.0)
# Niches visible along the ground stair: open boxes, not fictitious reading rooms.
for yy in [152.65,157.35]:
 side=-1 if yy<155 else 1
 c.box('Library stair flanking timber wall',(120.8,yy,1.88),(4.7,.24,3.76),wood)
 for xx in [119.4,121.1,122.8]:
  for z in [.8,1.75,2.7]:
   c.box('Library open niche dark recess',(xx,yy-side*.135,z),(1.35,.03,.66),dark)
   for zz in [z-.35,z+.35]:c.box('Library niche shelf edge',(xx,yy-side*.23,zz),(1.4,.27,.045),wood)
   for dx in [-.69,.69]:c.box('Library niche vertical reveal',(xx+dx,yy-side*.23,z),(.04,.27,.7),wood)
   if z<2:k.pot(xx,yy-side*.28,z-.32,.20,seed=int(xx*z))
# Freestanding blue exhibition panels visible in the first floor panorama.
c.collection('142_Library_Hall_Display_And_Pots')
blue=c.material('Library display board blue',(.035,.21,.43),.55)
for x,y in [(117.6,141.8),(117.6,145.2),(117.6,165),(117.6,168.3)]:
 c.box('Library display board',(x,y,1.25),(.07,1.48,1.75),cream)
 c.box('Library blue display heading',(x-.041,y,1.88),(.012,1.40,.38),blue)
 for q in range(6):c.box('Library display graphic rules',(x-.042,y,1.52-q*.15),(.014,1.12,.032),p['seam'])
 for yy in [y-.55,y+.55]:
  c.rod('Library display support',(x,yy,.03),(x,yy,.65),.022,p['steel'])
  c.box('Library display foot',(x,yy,.035),(.65,.09,.07),p['steel'])
for base in [0,4.25]:
 for x,y in [(117,150),(117,160),(140,141),(140,169)]:k.pot(x,y,base,seed=int(x*y+base))
for a in [.20,.37,.63,.80,1.2,1.37,1.63,1.80]:
 t=a*math.pi;k.pot(130+8.6*math.cos(t),155+8.6*math.sin(t),4.25,.75,seed=int(a*100))
# Generic dark bust silhouette in the observed location, identity deliberately unassigned.
bronze=c.material('Library reference bust dark patina',(.056,.069,.052),.5,.6)
c.box('Library bust stone pedestal',(136,155,4.85),(.8,.75,1.2),p['dark'],.02)
l.ellipsoid('Library bust shoulder silhouette',(136,155,5.61),(.50,.29,.30),bronze,24,12)
l.ellipsoid('Library bust neck',(136,155,5.91),(.115,.13,.21),bronze,20,10)
l.ellipsoid('Library bust head silhouette',(135.99,155,6.18),(.18,.17,.27),bronze,24,16)
l.ellipsoid('Library bust nose silhouette',(135.8,155,6.16),(.06,.048,.065),bronze,12,8)
for yy in [154.82,155.18]:l.ellipsoid('Library bust ear silhouette',(135.99,yy,6.19),(.044,.035,.070),bronze,12,8)
for x,y in [(135.2,154.55),(136.8,154.55),(135.2,155.45),(136.8,155.45)]:k.pot(x,y,4.25,.52,seed=int(x*y))
c.collection('148_Library_Interior_Review_Cameras')
c.camera('67_Library_ground_hall',(115.6,155,1.65),(126,155,2.1),18)
c.camera('68_Library_atrium_upward',(128,151,5.9),(131,156,11.0),19)
c.camera('69_Library_second_hall',(119.1,155,5.95),(136,155,6.7),21)
c.camera('70_Library_curved_stairs',(138.9,159,6.0),(124,156,7),21)
c.camera('71_Library_hall_reverse',(120.1,154.9,1.65),(111,156,1.7),23)
sc.camera=sc.objects['67_Library_ground_hall']
sc['scope']='Library first and second halls, circular atrium, visible straight and paired curved stairs, radial rooflight; furnishings are restrained approximations, portrait identity unassigned; reading rooms not reconstructed.'
c.save(c.ROOT/'models/campus/WZMS_Campus_v018.blend','v0.0.18',[119232388,119232389,119232391])
print('WZMS_BUILD_COMPLETE v0.0.18',flush=True)
