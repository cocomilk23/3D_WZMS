"""v027 Zhouyuan: curved glazed facade, pergola, timber promenade and entry."""
import bpy,sys,math
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).parent))
import campus_common as c,north_common as n,south_detail_common as s,island_common as h,west_common as w
sc=bpy.data.scenes['WZMS_Campus'];c.activate(sc);p=n.palette()
white=s.mottled('Zhouyuan fine white stucco',[(.68,.685,.62),(.83,.83,.77)],16);c.noise(white,115,.12,.008)
stone=n.paving('Zhouyuan pale large floor tile',(.48,.49,.45),(.9,.9),.004)
frame=c.material('Zhouyuan graphite glazing frame',(.028,.033,.031),.33,.50)
glass=c.material('Zhouyuan clear lake glazing',(.76,.85,.80),.075)
bs=glass.node_tree.nodes.get('Principled BSDF');bs.inputs['Transmission Weight'].default_value=.95;bs.inputs['IOR'].default_value=1.46
def arc(rx,ry,count=48):return [(-37+rx*math.cos(-math.pi+i*math.pi/count),128+ry*math.sin(-math.pi+i*math.pi/count)) for i in range(count+1)]
facade=arc(14,9);outline=[(-51,136),(-51,128)]+facade[1:]+[(-23,136)]
c.collection('230_Zhouyuan_Foundation_And_Curved_Floor')
outer=[(-56,138),(-56,128)]+arc(19,13.5)[1:]+[(-18,138)]
w.prism('Zhouyuan continuous lakeside foundation',outer,-.035,-1.85,p['stone'])
w.prism('Zhouyuan curved hall floor',outline,0,-.25,stone)
grass=s.mottled('Zhouyuan shaded shore earth',[(.085,.115,.035),(.20,.22,.07)],2)
w.prism('Zhouyuan outer bank top',outer,-.025,-.04,grass)
c.collection('231_Zhouyuan_Curved_Glazing_And_White_Walls')
for a,b in zip(facade,facade[1:]):
    s.segment('Zhouyuan curved glazing bottom frame',a,b,.075,frame,.115,.115)
    s.segment('Zhouyuan clear curved glass panel',a,b,.016,glass,3.23,3.08)
    s.segment('Zhouyuan upper glazing frame',a,b,.08,frame,3.29,.065)
    s.segment('Zhouyuan curved white fascia',a,b,.20,white,3.72,.39)
for i in range(0,len(facade),2):
    x,y=facade[i];c.box('Zhouyuan slim full-height mullion',(x,y,1.68),(.062,.065,3.24),frame)
c.box('Zhouyuan quiet north enclosure',(-37,136,1.86),(28,.2,3.72),white)
c.box('Zhouyuan west return wall',(-51,132,1.86),(.20,8,3.72),white)
for lo,hi in [(128,129),(132,134),(134,136)]:
    c.box('Zhouyuan east fixed glass',(-23,(lo+hi)/2,1.68),(.018,hi-lo,3.14),glass)
    for y in [lo,hi]:c.box('Zhouyuan east frame upright',(-23,y,1.68),(.07,.065,3.3),frame)
    c.box('Zhouyuan east frame head',(-23,(lo+hi)/2,3.3),(.09,hi-lo,.065),frame)
for y in [129,132]:
    c.box('Zhouyuan entry white jamb',(-23,y,1.9),(.24,.25,3.8),white)
c.box('Zhouyuan entry lintel',(-23,130.5,3.48),(.24,3.2,.47),white)
# Open glass leaves lie beside the clear three-metre entry.
for y in [129,132]:
    c.box('Zhouyuan open entry leaf',(-22.35,y,1.43),(1.2,.018,2.80),glass)
    for x in [-22.97,-21.73]:c.box('Zhouyuan open door stile',(x,y,1.43),(.045,.055,2.85),frame)
    for z in [.03,2.85]:c.box('Zhouyuan open door rail',(-22.35,y,z),(1.26,.055,.05),frame)
    c.rod('Zhouyuan door pull',(-21.88,y-.07,.9),(-21.88,y-.07,1.4),.018,p['steel'])
w.prism('Zhouyuan curved insulated roof',outline,3.83,3.63,white)
c.collection('232_Zhouyuan_White_Pergola_And_Timber_Promenade')
walk=arc(16.35,11.20,32)
w.wood_deck('Zhouyuan curved waterfront walk',walk,2.50)
w.wood_deck('Zhouyuan west return deck',[(-53.35,128),(-53.35,137)],2.5)
w.wood_deck('Zhouyuan east entrance deck',[(-20.65,128),(-20.65,139)],2.7)
s.ribbon('Zhouyuan level entrance threshold',[(-20,130.5),(-24,130.5)],2.8,stone,0,.20)
for i in range(0,len(facade),2):
    a=Vector(facade[i]);t=-math.pi+i*math.pi/48
    b=Vector((-37+17.6*math.cos(t),128+12.5*math.sin(t)))
    s.beam('Zhouyuan radial white pergola beam',(*a,3.54),(*b,3.54),.15,.25,white)
edge=arc(17.6,12.5)
for a,b in zip(edge,edge[1:]):s.beam('Zhouyuan continuous outer pergola rim',(*a,3.54),(*b,3.54),.16,.27,white)
for y in [128.5+i*.7 for i in range(14)]:s.beam('Zhouyuan east pergola return',(-23,y,3.54),(-19.2,y,3.54),.15,.25,white)
c.box('Zhouyuan east pergola edge',(-19.2,133,3.54),(.16,10,.27),white)
for x,y in [(-22.9,128.0),(-50.7,128.0)]:c.rod('Zhouyuan rounded white entry corner',(x,y,0),(x,y,3.45),.27,white,sides=32)
blue=c.material('Zhouyuan blue hanging nameplate',(.015,.055,.38),.43)
c.box('Zhouyuan hanging nameplate',(-21.8,129.1,2.82),(.94,.042,.48),blue)
c.text('Zhouyuan observed name','籀园学堂',(-21.8,129.073,2.75),.14,p['white'])
c.text('Zhouyuan nameplate reverse','籀园学堂',(-21.8,129.127,2.75),.14,p['white'],(math.pi/2,0,math.pi))
for x in [-22.13,-21.47]:c.rod('Zhouyuan nameplate hanger',(x,129.1,3.06),(x,129.1,3.52),.006,p['steel'],sides=6)
c.collection('233_Zhouyuan_Visible_Entry_Furniture')
wood=c.material('Zhouyuan pale oak furniture',(.46,.30,.13),.64);seat=c.material('Zhouyuan charcoal chair',(.045,.05,.044),.66)
for x,y in [(-27,125),(-33,123),(-40,123),(-46,126)]:
    c.box('Zhouyuan visible table top',(x,y,.74),(1.8,.85,.06),wood,.015)
    for dx in [-.72,.72]:
        for dy in [-.30,.30]:c.box('Zhouyuan table leg',(x+dx,y+dy,.36),(.05,.05,.72),p['dark'])
    for yy in [y-.9,y+.9]:
        c.box('Zhouyuan visible chair seat',(x,yy,.43),(.44,.43,.055),wood,.018)
        for dx in [-.17,.17]:
            for dy in [-.16,.16]:c.box('Zhouyuan chair leg',(x+dx,yy+dy,.21),(.025,.025,.42),p['dark'])
        c.box('Zhouyuan chair back',(x,yy+(.19 if yy>y else -.19),.73),(.43,.04,.5),seat,.02)
# Only the visible entry zone is furnished; the unseen teaching rooms remain unclaimed.
for x in [-45,-40,-35,-30]:
    c.box('Zhouyuan interior track',(x,130,3.59),(.055,7,.04),p['dark'])
    for y in [127,130,133]:
        c.rod('Zhouyuan ceiling spotlight',(x,y,3.55),(x,y,3.41),.075,p['dark'],sides=12)
        lens=c.material('Zhouyuan lit spotlight lens',(.92,.80,.56),.4)
        lens.node_tree.nodes['Principled BSDF'].inputs['Emission Color'].default_value=(1,.84,.63,1)
        lens.node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value=2.4
        c.rod('Zhouyuan spotlight lens',(x,y,3.405),(x,y,3.41),.063,lens,sides=16)
        data=bpy.data.lights.new('Zhouyuan visible entry downlight','SPOT');data.energy=65;data.color=(1,.84,.65);data.spot_size=1.4;data.spot_blend=.65;data.shadow_soft_size=.06
        obj=bpy.data.objects.new(data.name,data);c.COL.objects.link(obj);obj.location=(x,y,3.38)
c.collection('234_Zhouyuan_Lakeside_Trees_And_Shore')
proto=[sc.objects['Rongyu spreading old banyan connected trunks roots and twigs'],sc.objects['Rongyu spreading old banyan attached broadleaf canopy']]
for x,y,scale,angle in [(-45.8,115.8,.70,1.2),(-55.5,131,.70,.6)]:
    h.island('Zhouyuan tree bank projection',x,y,2.2,2.0,grass,p['stone'])
    n.duplicate_tree(proto,x,y,angle,scale)
shore=arc(18.7,13.1,28);w.chain_path('Zhouyuan waterfront chain',shore,gaps=[((-29,116),3.8),((-20,123),4.0)])
c.box('Zhouyuan grey utility cabinet',(-52.2,135.5,.66),(.8,.4,1.32),p['steel'],.015)
c.collection('238_Zhouyuan_Review_Cameras')
c.camera('106_Zhouyuan_entry',(-16,132,1.7),(-28,130.5,1.7),24)
c.camera('107_Zhouyuan_curved_promenade',(-23,117,1.7),(-44,119,2.0),25)
c.camera('108_Zhouyuan_lakeside_facade',(-37,110,1.7),(-37,126,2.1),22)
c.camera('109_Zhouyuan_overview',(-70,97,32),(-36,128,0),35)
h.save(27,'Zhouyuan curved glazed exterior, pergola and wood promenade based on 360. 361 informs only visible entry furniture. Entire roof footprint, back enclosure and dimensions estimated; full classroom interiors not delivered.',[360,361,362,356,347,348],'109_Zhouyuan_overview')
