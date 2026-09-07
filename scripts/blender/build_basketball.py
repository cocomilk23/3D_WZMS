"""v033 red-green basketball courts, complete hoops/nets and sports integration."""
import bpy,math,sys
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).parent))
import campus_common as c,north_common as n,north_landscape as l
import south_detail_common as s,island_common as h,sports_common as q
sc=bpy.data.scenes['WZMS_Campus'];c.activate(sc);p=n.palette()
h.retire('v0.0.33',collections=['52_Zhongshan_Middle_Court_Edge','65_North_Court_Visible_Edge'])
green=s.mottled('Basketball weathered green acrylic',[(.10,.19,.075),(.19,.30,.13)],2)
c.noise(green,185,.24,.004)
red=s.mottled('Basketball faded terracotta acrylic',[(.31,.075,.051),(.49,.16,.10)],2)
c.noise(red,185,.24,.004)
paint=c.material('Basketball warm white markings',(.73,.74,.68),.90)
steel=c.material('Basketball photographed green steel',(.024,.24,.115),.38,.45)
board=c.material('Basketball clear green tinted backboard',(.58,.77,.68),.04)
bs=board.node_tree.nodes['Principled BSDF'];bs.inputs['Transmission Weight'].default_value=.95;bs.inputs['IOR'].default_value=1.45
netmat=c.material('Basketball white cord net',(.69,.72,.66),.8)
orange=c.material('Basketball red orange hoop steel',(.65,.11,.018),.37,.45)
soil=s.mottled('Basketball perimeter soil',[(.08,.10,.025),(.18,.22,.07)],2)
c.collection('290_Basketball_Red_Green_Surfaces')
c.box('Sports integration gym branch verge infill ESTIMATED',(-34,366,-.86),(28,44,1.50),soil)
c.box('Basketball continuous court foundation',(16,263,-.7),(51,118,1.28),p['stone'])
c.box('Basketball continuous green acrylic surround',(16,263,-.015),(48,112,.08),green)
s.ribbon('Basketball north access support',[(-3,330),(15.5,330),(15.5,319)],5.8,soil,-.08,1.5,miter=True)
s.ribbon('Basketball north access paving',[(-3,330),(15.5,330),(15.5,319)],3.2,n.paving('Basketball shaded entry pavers',(.38,.40,.35),(.50,.30),.006),0,.17,miter=True)
south_walk=[(15.5,208),(15.5,205.8),(24.8,205.8),(24.8,200)]
s.ribbon('Basketball south access support',south_walk,5.2,soil,-.08,1.5,miter=True)
s.ribbon('Basketball south connection to Jiangkou',south_walk,3.2,n.paving('Basketball shaded entry pavers',(.38,.40,.35),(.50,.30),.006),0,.17,miter=True)

def hoop(cx,cy,sign):
    by=cy+sign*12.80;post=cy+sign*15.6;hy=cy+sign*12.425
    c.box('Basketball green weighted steel base',(cx,post,.22),(1.35,1.9,.44),steel,.06)
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

for row,cy in enumerate([226,263,300]):
    for col,cx in enumerate([4,27]):
        c.collection('291_Basketball_Court_'+str(row*2+col+1))
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
c.collection('297_Basketball_Fence_And_Shaded_Edges')
for x in [-8,40]:
    for lo,hi in [(212 if x==40 else 208,242.5),(247,279.5),(283.5,319)]:s.wire_fence('Basketball green perimeter',(x,lo),(x,hi),3.3,steel,.14)
for y in [208,319]:
    for lo,hi in [(-8,13.5),(17.5,38 if y==208 else 40)]:s.wire_fence('Basketball end perimeter',(lo,y),(hi,y),3.3,steel,.14)
for yy in [244.7,281.5]:
    s.ribbon('Basketball east gate tie to Zhongshan',[(37,yy),(44.2,yy)],2.6,green,.015,.20)
    l.bench(36.6,yy+3.1,math.pi/2)
for x,y in [(-9,220),(-9,274),(39,247.5),(39,282)]:
    c.rod('Basketball slim floodlight mast',(x,y,0),(x,y,8.7),.065,p['steel'],.045,12)
    for dx in [-.4,.4]:
        o=c.box('Basketball paired floodlight head',(x+dx,y,8.6),(.52,.24,.34),p['white'],.03);o.rotation_euler.x=.34
for x,y in [(-8.8,250),(-8.8,288),(37,322)]:s.tree(x,y,.68,y*.02)
c.collection('298_Sports_Batch_Review_Cameras')
c.camera('133_Basketball_ground_view',(14.8,244.6,1.7),(25,282,1.9),27)
c.camera('134_Basketball_hoop_detail',(4,219,1.7),(4,213.0,3.2),32)
c.camera('135_Basketball_north_entry',(15.5,332,1.7),(15.5,286,1.8),26)
c.camera('136_Basketball_overview',(92,179,104),(13,268,0),34)
c.camera('137_West_sports_integrated',(-228,116,198),(-62,284,2),32)
c.camera('138_Campus_integrated_v033',(-265,-140,415),(65,184,0),28)
h.save(33,'Integrated west sports batch with six red-green basketball courts, twelve editable cantilever hoops, backboards, hanging nets, fence gates and Nantian/Zhongshan links. Replaces explicit v008 roadside court and v009 northern extension placeholder collections. Court count/layout and all building placement are image-estimated, not surveyed.',[358,379,347,348],'138_Campus_integrated_v033')
