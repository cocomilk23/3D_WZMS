"""v026 Rongyu: small lotus channel, granite bridge, rolling lawn and banyan."""
import bpy,sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import campus_common as c,north_common as n,south_detail_common as s,island_common as h,west_common as w,north_landscape as l
sc=bpy.data.scenes['WZMS_Campus'];c.activate(sc);p=n.palette()
c.collection('220_Rongyu_Island_And_Entry')
grass=s.mottled('Rongyu shaded green earth',[(.08,.115,.035),(.18,.205,.065)],2)
bank=s.mottled('Rongyu mossy retaining stone',[(.17,.19,.13),(.35,.34,.25)],9);c.noise(bank,45,.32,.018)
outline=h.island('Rongyu irregular low island',-29,101,12,8,grass,bank)
pebble=h.pebble('Rongyu small natural river pebbles',(.38,.37,.29))
approach=[(-20,146),(-20,117),(-29,117)]
s.ribbon('Rongyu mainland supporting earth',approach,5.0,grass,-.025,1.6,miter=True)
s.ribbon('Rongyu approach pebble walk',approach,2.4,pebble,0,.16,miter=True)
loop=[(-29,106),(-22,104),(-20.7,100),(-24,96),(-31,95.6),(-38,98.5),(-38,102),(-34,105),(-29,106)]
s.ribbon('Rongyu continuous island pebble circuit',loop,1.35,pebble,0,.16,miter=True)
s.ribbon('Rongyu bridgehead island approach',[(-29,106),(-29,109)],2.2,pebble,0,.2)
c.collection('221_Rongyu_Stone_Bridge_And_Lotus_Channel')
w.stone_bridge('Rongyu low carved stone bridge',-29,108.5,116,2.2)
w.lotus('Rongyu east lotus patch',-24,112,3.3,1.75,362)
w.lotus('Rongyu west lotus patch',-35,111.2,3.4,1.8,1362)
c.collection('222_Rongyu_Old_Banyan_And_Groundcover')
w.meadow('Rongyu central grass mound',-29,100.5,7.2,3.8,.62,362)
proto=w.banyan('Rongyu spreading old banyan',-29,100.5,10.5,6.6,362)
for obj in proto:obj.location.z=.52
for x,y,height in [(-19,123,6.5),(-40,105,4.1)]:
    n.broad_tree('Rongyu smaller waterside tree',x,y,height,1.5,int(abs(x*y)))
stone=s.mottled('Rongyu natural marker rock',[(.34,.35,.30),(.57,.54,.44)],4)
obj=l.ellipsoid('Rongyu low information stone',(-24.9,102.2,.30),(.55,.45,.34),stone,16,7)
plate=c.box('Rongyu inset bronze marker',(-24.9,102.2,.615),(.43,.30,.018),c.material('Rongyu aged bronze label',(.22,.13,.07),.69,.32))
plate['text_status']='Small inscription unresolved; no invented transcript'
c.collection('223_Rongyu_Mainland_Edge_Furniture')
for x,y in [(-17.9,118),(-18.1,137)]:s.slit_lamp(x,y)
c.collection('228_Rongyu_Review_Cameras')
c.camera('102_Rongyu_stone_bridge',(-29,115.7,1.7),(-29,102,2.4),27)
c.camera('103_Rongyu_lotus_channel',(-35,116,1.7),(-25,110,.35),28)
c.camera('104_Rongyu_banyan_walk',(-22,104,1.7),(-30,100.5,2.7),24)
c.camera('105_Rongyu_island_overview',(1,80,35),(-29,107,1),36)
h.save(26,'Rongyu exterior island and mainland approach. Old banyan, rolling groundcover, lotus channel, granite bridge and pebble loop from panorama 362. Tree form, shoreline and distances are image estimates. Adjacent Zhouyuan building follows in v027.',[362,360,347,348,374],'105_Rongyu_island_overview')
