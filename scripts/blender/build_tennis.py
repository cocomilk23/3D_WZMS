"""v012: two tennis courts, cyan enclosure, practice wall and entry connection.
Reference: 119232359 F/B/L/R, aerial 348/R. Dimensions are estimates.
"""
import bpy,sys,math,random,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import campus_common as c
import north_common as n
import north_landscape as l
import south_detail_common as s
sc=bpy.data.scenes['WZMS_Campus'];c.activate(sc)
blue=c.material('Tennis cyan enamel',(.018,.31,.57),.38,.35)
white=c.material('Tennis warm white court paint',(.84,.84,.77),.8)
green=s.mottled('Tennis weathered sage surround',[(.18,.33,.23),(.32,.43,.32)],1.9)
violet=s.mottled('Tennis faded violet acrylic',[(.21,.235,.37),(.37,.39,.48)],1.7)
c.collection('90_Tennis_Courts_And_Access')
c.box('Tennis raised aggregate foundation',(83,8,-.28),(36.4,36.4,.52),n.palette()['stone'])
c.box('Tennis two court continuous surround',(83,8,-.028),(36,36,.036),green)
for cy in [-1,17]:
 c.box('Tennis violet doubles playing area',(83,cy,-.007),(23.77,10.97,.004),violet)
 for yy in [cy-5.485,cy-4.115,cy+4.115,cy+5.485]:s.segment('Tennis singles and doubles sideline',(71.115,yy),(94.885,yy),.05,white,-.002,.003)
 for xx in [71.115,94.885]:s.segment('Tennis baseline',(xx,cy-5.485),(xx,cy+5.485),.07,white,-.001,.003)
 for xx in [76.60,89.4]:s.segment('Tennis service line',(xx,cy-4.115),(xx,cy+4.115),.05,white,-.001,.003)
 s.segment('Tennis centre service line',(76.6,cy),(89.4,cy),.05,white,-.001,.003)
 for xx in [71.17,94.83]:s.segment('Tennis baseline centre mark',(xx-.05,cy),(xx+.05,cy),.05,white,0,.003)
pave=n.paving('Tennis exterior grey pavers',(.46,.48,.44),(.3,.3),.004)
s.segment('Tennis access from Zhongshan forewalk',(54,47),(62,47),3,pave)
s.segment('Tennis west entry approach',(62,47),(62,17),3,pave)
s.segment('Tennis west threshold',(62,17),(66,17),2,pave)
c.collection('91_Tennis_Blue_Fencing')
for a,b in [((65,-10),(101,-10)),((65,26),(101,26)),((65,-10),(65,16)),((65,18),(65,26)),((101,-10),(101,22)),((101,24),(101,26))]:s.wire_fence('Tennis perimeter',a,b,4.0,blue)
# Two real door openings, leaves parked along the fence instead of blocking access.
for xx,yy in [(65,16),(101,24)]:
 s.wire_fence('Tennis open gate leaf',(xx,yy),(xx+1.8,yy),2.05,blue)
 for z in [.25,1.7]:c.rod('Tennis gate hinge',(xx,yy,z),(xx,yy,z+.13),.034,n.palette()['steel'])
c.collection('92_Tennis_Nets_And_Practice_Wall')
netmat=c.material('Tennis black woven net',(.018,.021,.022),.83)
posts=c.material('Tennis green net standards',(.016,.16,.09),.4,.45)
for cy in [-1,17]:
 for yy in [cy-6.4,cy+6.4]:
  c.box('Tennis square net post',(83,yy,.535),(.14,.14,1.09),posts,.01)
  c.box('Tennis post top cap',(83,yy,1.1),(.16,.16,.04),posts,.01)
  c.rod('Tennis tension crank',(83.10,yy,.7),(83.22,yy,.7),.013,n.palette()['steel'])
 v,f=[],[]
 def ztop(y):return .914+.156*((y-cy)/6.4)**2
 for j in range(257):
  yy=cy-6.4+j*.05;c.tube_data(v,f,(83,yy,.07),(83,yy,ztop(yy)-.025),.003,.003,4)
 for j in range(20):
  t=j/19
  for k in range(64):
   ya=cy-6.4+k*.2;yb=ya+.2
   c.tube_data(v,f,(83,ya,.07+(ztop(ya)-.10)*t),(83,yb,.07+(ztop(yb)-.10)*t),.003,.003,4)
 c.mesh('Tennis actual woven sagging net',v,f,netmat)
 for k in range(64):
  ya=cy-6.4+k*.2;yb=ya+.2;s.beam('Tennis white top binding',(83,ya,ztop(ya)),(83,yb,ztop(yb)),.035,.05,white)
 c.box('Tennis centre net strap',(82.979,cy,.47),(.015,.045,.91),white)
c.box('Tennis blue practice wall',(100.72,8,1.55),(.25,14,3.1),blue,.02)
c.box('Practice wall white net height line',(100.584,8,.914),(.009,13.85,.055),white)
for yy in [4,12]:
 for zz in [1.45,2.0]:c.box('Practice wall target horizontal',(100.581,yy,zz),(.010,.55,.035),white)
 for dy in [-.275,.275]:c.box('Practice wall target vertical',(100.581,yy+dy,1.725),(.010,.035,.55),white)
c.collection('93_Tennis_Lights_And_Furniture')
for xx in [65.15,100.85]:
 for yy in [-9.5,8,25.5]:
  c.rod('Tennis floodlight pole',(xx,yy,0),(xx,yy,7),.052,blue,.035,12)
  dx=.42 if xx<80 else -.42
  c.rod('Tennis floodlight arm',(xx,yy,6.83),(xx+dx,yy,6.83),.028,blue)
  o=c.box('Tennis rectangular floodlight',(xx+dx,yy,6.79),(.50,.34,.09),n.palette()['dark'],.025);o.rotation_euler.y=.25 if xx<80 else -.25
  c.box('Tennis floodlight diffuser',(xx+dx,yy,6.732),(.43,.27,.014),white)
for yy in [-4,3,10,22]:
 x=66.0;l.bench(x,yy,math.pi/2)
# Long timber flower troughs with upright clipped shrubs seen around the perimeter.
wood=n.paving('Tennis planter vertical timber',(.25,.115,.045),(.10,.48),.003)
for yy in [-8,-3,2,7,12,20,25]:
 for xx in [64.25,101.7]:
  c.box('Tennis timber planter',(xx,yy,.23),(.55,2.3,.46),wood,.025)
  for dy in [-.75,0,.75]:l.shrub('Tennis clipped border',xx,yy+dy,1.2,.24,int(xx*9+yy*5+dy*3),.43)
c.collection('94_Tennis_Adjacent_Planting')
for x,y,w,d in [(62,7,5,44),(83,-12,44,3),(104,8,3,39)]:c.box('Tennis peripheral landscape soil',(x,y,-.20),(w,d,.35),n.palette()['green'])
for j,(x,y) in enumerate([(60,-6),(60,5),(60,29),(60,38),(71,-13),(85,-13),(99,-13)]):s.tree(x,y,.78+(j%3)*.08,j*.7)
c.collection('98_Tennis_Cameras')
c.camera('45_Tennis_ground_toward_wall',(73,12,1.72),(100,8,1.8),25)
c.camera('46_Tennis_net_and_campus',(97,-6,1.72),(61,37,5),24)
c.camera('47_Tennis_entry',(60,17,1.72),(79,17,1.3),27)
c.camera('48_Tennis_overview',(129,-31,47),(82,10,0),40)
sc.camera=sc.objects['45_Tennis_ground_toward_wall']
s.daylight(sc)
sc['scope']='Previous campus retained; v012 adds two tennis courts and their access. He island and Shuinan bridges follow separately.'
sc['south_batch_baseline']='35d1d58; local v011 edits preserved before additions'
c.save(c.ROOT/'models/campus/WZMS_Campus_v012.blend','v0.0.12',[119232359,119232348])
print('WZMS_BUILD_COMPLETE v0.0.12',flush=True)
