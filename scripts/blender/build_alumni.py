"""v028 the photographed Alumni glass lobby and display area, not unseen rooms."""
import bpy,sys,math,json
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).parent))
import campus_common as c,north_common as n,south_detail_common as s,island_common as h,west_common as w,west_exhibit as e
sc=bpy.data.scenes['WZMS_Campus'];c.activate(sc);p=n.palette()
old=[]
for o in bpy.data.collections['105_Daosi_Visible_Context_ESTIMATED'].all_objects:
    if o.type!='MESH' or o.name.startswith('Daosi junction roadside palm'):continue
    points=[o.matrix_world@Vector(q) for q in o.bound_box];q=sum(points,Vector())/8
    if -56<q.x<-28 and 150<q.y<163:old.append(o.name)
h.retire('v0.0.28',names=old)
white=c.material('Alumni warm white plaster',(.72,.72,.66),.82)
steel=c.material('Alumni silver column cladding',(.43,.51,.53),.30,.72)
seam=c.material('Alumni charcoal inlay joints',(.032,.038,.034),.74)
floor=n.paving('Alumni polished light granite',(.51,.49,.41),(1.2,1.2),.003)
floor.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.23
glass=c.material('Alumni atrium clear glass',(.74,.86,.84),.07)
bs=glass.node_tree.nodes['Principled BSDF'];bs.inputs['Transmission Weight'].default_value=.96;bs.inputs['IOR'].default_value=1.46
warm=c.material('Alumni warm recessed diffuser',(.93,.61,.22),.40)
bs=warm.node_tree.nodes['Principled BSDF'];bs.inputs['Emission Color'].default_value=(1,.61,.22,1);bs.inputs['Emission Strength'].default_value=3
timber=s.mottled('Alumni oak ceiling slats',[(.17,.105,.038),(.38,.25,.09)],9)
c.collection('240_Alumni_Foundation_And_Approaches')
c.box('Alumni supported precinct plot',(-42,162,-.8),(29,27,1.54),p['stone'])
c.box('Alumni polished lobby floor',(-42,160.5,-.14),(26,19,.28),floor)
s.ribbon('Alumni south entrance apron',[(-42,146),(-42,153)],4.6,floor,0,.2)
s.ribbon('Alumni east path supporting plot',[(-29,160),(-20,160),(-20,146)],5.0,p['green'],-.04,1.5,miter=True)
s.ribbon('Alumni east exit promenade',[(-29,160),(-20,160),(-20,146)],2.8,floor,0,.2,miter=True)
for x in [-52,-47,-42,-37,-32]:c.box('Alumni long dark floor inlay',(x,160.5,.002),(.035,18.5,.008),seam)
for y in [154,158,162,166]:c.box('Alumni transverse dark floor inlay',(-42,y,.002),(25.5,.032,.008),seam)
c.collection('241_Alumni_Glass_Atrium_And_Metal_Columns')
# A tall south-facing glazed lobby in front of the lower exhibit ceiling.
for x in [-54.5,-48,-35.5,-29.5]:
    c.box('Alumni square clad structural column',(x,156,4.6),(.62,.66,9.2),steel,.012)
    for z in [1.5,3,4.5,6,7.5,9]:c.box('Alumni column horizontal panel joint',(x,155.658,z),(.63,.008,.018),seam)
for x0,x1 in [(-55,-43.5),(-40.5,-29)]:
    c.box('Alumni front fixed glass',((x0+x1)/2,151,4),(x1-x0,.018,8),glass)
    for j in range(math.ceil((x1-x0)/1.2)+1):
        xx=min(x1,x0+j*1.2);c.box('Alumni front glazing upright',(xx,150.94,4),(.065,.14,8),p['white'])
    for z in [2.8,4.3,5.8,7.3]:c.box('Alumni front glazing horizontal bar',((x0+x1)/2,150.93,z),(x1-x0,.16,.065),p['white'])
c.box('Alumni clear glass over south door',(-42,151,5.5),(3,.018,5),glass)
for x in [-43.5,-40.5]:c.box('Alumni south door jamb',(x,150.91,1.5),(.06,.13,3),seam)
c.box('Alumni south door lintel',(-42,150.90,3.03),(3.2,.13,.07),seam)
for x in [-43.5,-40.5]:
    c.box('Alumni open south glass leaf',(x,151.65,1.4),(.018,1.25,2.8),glass)
    for yy in [151.02,152.28]:c.box('Alumni open door upright',(x,yy,1.4),(.07,.05,2.8),seam)
    for z in [.04,2.79]:c.box('Alumni open door rail',(x,151.65,z),(.065,1.3,.045),seam)
for x in [-55,-29]:
    c.box('Alumni tall atrium side glass',(x,153.5,4.45),(.018,5,8.9),glass)
    for y in [151,152.25,153.5,154.75,156]:c.box('Alumni side atrium frame',(x,y,4.4),(.12,.075,8.8),p['white'])
# Sloping glass roof grid, a photographed feature of the tall lobby.
for j in range(5):
    ya=151+j;yb=ya+1;za=8+(ya-151)*.24;zb=8+(yb-151)*.24
    c.mesh('Alumni atrium sloping glass roof',[(-55,ya,za),(-29,ya,za),(-29,yb,zb),(-55,yb,zb)],[(0,1,2,3)],glass)
    s.beam('Alumni roof transverse truss',(-55,ya,za),(-29,ya,za),.12,.18,p['white'])
for x in [-55+i*1.3 for i in range(21)]:s.beam('Alumni roof longitudinal glazing bar',(x,151,8),(x,156,9.2),.08,.13,p['white'])
c.collection('242_Alumni_Exhibition_Walls_And_Luminous_Ceiling')
c.box('Alumni rear exhibition wall',(-42,170,2.13),(26,.22,4.26),white)
c.box('Alumni west exhibition wall',(-55,163,2.13),(.22,14,4.26),white)
for y,depth in [(157,2),(165.75,8.5)]:c.box('Alumni east wall beside exit',(-29,y,2.13),(.22,depth,4.26),white)
c.box('Alumni east exit lintel',(-29,160,3.66),(.22,3,1.2),white)
for y in [158.5,161.5]:c.box('Alumni east exit metal jamb',(-29.08,y,1.5),(.16,.085,3),steel)
c.box('Alumni supported exhibit roof',(-42,163,4.34),(26,14,.25),white)
c.box('Alumni dark ceiling recess',(-42,163,4.15),(25.7,13.7,.12),seam)
for x in [-54.7+i*.33 for i in range(78)]:c.box('Alumni individual oak ceiling fin',(x,163,4.03),(.085,13.5,.26),timber)
for x in [-53,-49,-45,-41,-37,-33,-30.5]:
    c.box('Alumni inset warm ceiling line',(x,163,3.98),(.16,12.8,.04),warm)
    data=bpy.data.lights.new('Alumni warm ceiling area','AREA');data.energy=90;data.color=(1,.73,.45);data.shape='RECTANGLE';data.size=.4;data.size_y=10
    obj=bpy.data.objects.new(data.name,data);c.COL.objects.link(obj);obj.location=(x,163,3.8)
# Vertical wood fascia above the low exhibit entrance, leaving the atrium open below.
c.box('Alumni high timber fascia backing',(-42,156.3,6.65),(25.4,.2,5.0),white)
for x in [-54.4+i*.25 for i in range(101)]:c.box('Alumni tall vertical timber slat',(x,156.14,6.65),(.06,.10,4.9),timber)
c.box('Alumni fascia lower white trim',(-42,156.0,4.22),(26,.24,.16),white)
c.text('Alumni founding year luminous ceiling','1902',(-42,161,3.83),1.05,warm,(math.pi,0,0))
c.collection('243_Alumni_Photo_Based_Display_Panels')
blue_quads=[[(905,761),(977,758),(977,935),(905,928)],[(848,764),(902,761),(902,928),(848,922)],[(795,768),(845,765),(845,922),(795,917)],[(744,771),(792,768),(792,916),(744,911)],[(699,773),(741,771),(741,910),(699,906)],[(654,775),(696,773),(696,905),(654,901)]]
red_quads=[[(1125,741),(1221,737),(1221,963),(1125,951)],[(1227,737),(1338,730),(1338,980),(1227,965)],[(1348,731),(1455,722),(1455,1004),(1348,984)],[(1464,722),(1575,712),(1575,1040),(1464,1009)]]
records=[]
for i,quad in enumerate(blue_quads):
    x=-53.3+i*1.32;c.box('Alumni blue panel metal backing',(x,169.73,1.28),(1.24,.065,2.42),steel,.01)
    obj=e.photo_panel('Alumni original blue profile panel',(x,169.69,.09),1.18,2.36,'l',quad)
    records.append({'object':obj.name,'face':'l','quad_pixels_on_1600':quad})
for i,quad in enumerate(red_quads):
    x=-36.4+i*1.45;c.box('Alumni red exhibition panel metal backing',(x,151.35,1.36),(1.37,.065,2.6),steel,.01)
    obj=e.photo_panel('Alumni original red exhibition panel',(x,151.391,.09),1.31,2.53,'f',quad,horizontal=(-1,0,0))
    records.append({'object':obj.name,'face':'f','quad_pixels_on_1600':quad})
screen=c.material('Alumni inactive screen',(.055,.043,.034),.38)
c.box('Alumni mirrored screen frame',(-39,169.73,2.15),(5.0,.09,2.50),steel,.012)
c.box('Alumni dark inactive display',(-39,169.66,2.15),(4.85,.025,2.34),screen)
blue=c.material('Alumni WZHS blue letters',(.015,.22,.46),.36,.15)
c.text('Alumni WZHS dimensional lettering','WZHS',(-39,169.57,.22),.95,blue)
c.collection('244_Alumni_Piano_And_Visible_Lobby_Furniture')
burgundy=c.material('Alumni burgundy piano cloth',(.12,.007,.018),.93)
black=c.material('Alumni polished black piano',(.015,.012,.01),.20)
cx,cy=-51,160.8
shape=[(cx-1.1,cy-.65),(cx+1.1,cy-.65),(cx+1.1,cy+.15),(cx+.8,cy+1.1),(cx,cy+1.5),(cx-.85,cy+1.1),(cx-1.1,cy+.3)]
w.prism('Alumni covered grand piano silhouette',shape,1.0,.73,burgundy)
for x,y in [(cx-.85,cy-.45),(cx+.85,cy-.45),(cx,cy+1.1)]:c.box('Alumni piano leg',(x,y,.38),(.10,.10,.75),black)
c.box('Alumni covered piano cloth front drape',(cx,cy-.65,.81),(2.22,.025,.37),burgundy)
c.box('Alumni piano bench',(cx,cy-1.17,.46),(.85,.37,.09),black,.02)
for dx in [-.34,.34]:
    for dy in [-.12,.12]:c.box('Alumni piano bench leg',(cx+dx,cy-1.17+dy,.22),(.04,.04,.44),black)
for x,y in [(-48,156),(-35.5,156)]:
    c.box('Alumni column extinguisher cabinet',(x,y-.43,.37),(.42,.18,.74),white,.008)
    c.text('Alumni observed fire equipment label','灭火器箱',(x,y-.53,.46),.07,c.material('Alumni red safety text',(.35,.025,.013),.75))
c.collection('248_Alumni_Review_Cameras')
c.camera('110_Alumni_glass_entry',(-42,144,1.7),(-42,160,3.3),24)
c.camera('111_Alumni_exhibition_hall',(-41,154.1,1.7),(-43,169,1.9),24)
c.camera('112_Alumni_atrium_and_panels',(-47,163.5,1.7),(-35,151.7,4),22)
c.camera('113_Alumni_piano_corner',(-44,163.5,1.7),(-51,161,1.5),26)
c.camera('114_Alumni_precinct_overview',(-81,121,48),(-35,148,0),35)
out=c.ROOT/'deliverables/v0.0.28';out.mkdir(parents=True,exist_ok=True)
(out/'exhibit_texture_sources.json').write_text(json.dumps({'source_scene':119232356,'original_faces_packed':True,'panels':records,'text_transcription':'No biographies invented; original photographs mapped projectively.'},ensure_ascii=False,indent=2),encoding='utf8')
h.save(28,'Alumni visible glass lobby and exhibition space from panorama 356. Replaces specifically selected Daosi four-storey context. Photo panels preserve actual source content; full unseen corridors and upper building not claimed. Footprint estimated.',[356,360,376,347,348],'114_Alumni_precinct_overview')
