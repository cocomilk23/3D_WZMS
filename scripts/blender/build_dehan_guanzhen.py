"""v0.0.5: five-storey wings, glazed elevated portal, roofs and lakeside edge.

Image-based exterior reconstruction from 352/353/354/366 and aerial 348.
Unphotographed internal rooms are intentionally unfurnished; envelope is real mesh.
"""
import sys, math, random
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import bpy
import campus_common as c
scene=bpy.data.scenes['WZMS_Campus'];c.activate(scene)
old=bpy.data.collections.get('19_Portal_Context_PENDING_FACADE')
if old:
    for o in list(old.objects):bpy.data.objects.remove(o,do_unlink=True)
    bpy.data.collections.remove(old)
stone=c.material('Facade pale limestone',(.60,.60,.55),.8);c.noise(stone,65,.22,.02)
white=c.material('Facade ivory powder coat',(.73,.75,.71),.39,.16)
grey=c.material('Facade recessed grey spandrel',(.34,.38,.38),.81)
dark=c.material('Graphite painted metal',(.032,.044,.052),.34,.65)
joint=c.material('Facade stone joint',(.17,.20,.19),.9)
steel=c.material('Brushed stainless steel',(.46,.5,.51),.29,.85)
glass=[]
for i,col in enumerate([(.095,.26,.25),(.07,.205,.21),(.15,.30,.28),(.085,.22,.25)]):
    m=c.material('Architectural teal glass '+str(i),col,.16,.28)
    p=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
    p.inputs['Coat Weight'].default_value=.45;p.inputs['Transmission Weight'].default_value=.22
    glass.append(m)
floor=c.material('South plaza warm ashlar',(.48,.46,.39),.86)
roofmat=c.material('Roof standing seam silver',(.44,.47,.46),.39,.45)
inside=c.material('Unfurnished interior shaded wall',(.32,.33,.29),.89)
c.collection('20_Dehan_Guanzhen_Foundations')
c.box('Building plot foundation',(0,59,-.30),(105,26,.56),stone)
c.box('Facade forewalk',(0,48.5,-.10),(105,7,.18),floor)
# Raised passage and seven real 150 mm steps. Front edge y=49.
for i in range(7):
    # Each riser is supported all the way to the landing: no cracks under bevels.
    start=49+i*.4;end=51.8
    c.box('Portal granite step %02d'%i,(0,(start+end)/2,(i+1)*.075-.01),(15,end-start,(i+1)*.15),stone,.009)
c.box('Portal raised through-passage',(0,58.65,.51),(15,14.1,1.06),floor)
for side in [-1,1]:
    c.box('Wing foundation plinth',(side*31.5,59,.41),(35,14,.84),stone,.025)
    c.box('Portal stair side cheek',(side*7.75,50.4,.53),(.45,3.4,1.08),stone,.02)
    c.box('Facade long low planter wall',(side*32,50.25,.35),(32,.26,.72),white,.016)
    c.box('Facade plant soil',(side*32,51.2,.20),(31.7,1.55,.42),c.material('Planting soil',(.06,.044,.025)))
    # Groundcover is copied up to the raised bed without scaling leaf size.
    o=c.planting('Facade low hedge',(side*32,51.2),(31.5,1.5),.38,700+side,250);o.location.z=.40
c.collection('21_Dehan_Guanzhen_Wings')
rng=random.Random(7354)
def windows_y(x,y,z,width=4.8,height=2.18,out=-1):
    """Full window frame and six opening panels on a Y-facing wall."""
    c.box('Window dark reveal',(x,y,z),(width+.14,.12,height+.14),dark)
    c.box('Window sill',(x,y+out*.10,z-height/2-.07),(width+.30,.30,.14),white,.012)
    for dx in [-width/2,width/2]:c.box('Window frame stile',(x+dx,y+out*.1,z),(.065,.11,height),white)
    for zz in [z-height/2,z+height/2,z+height*.19]:c.box('Window horizontal frame',(x,y+out*.105,zz),(width,.12,.055),white)
    step=width/6
    for k in range(6):
        xx=x-width/2+(k+.5)*step
        c.box('Window teal panel',(xx,y+out*.074,z),(step-.06,.025,height-.07),glass[rng.randrange(4)])
        c.box('Opening sash jamb',(xx-step/2,y+out*.12,z),(.038,.13,height-.06),white)
        if k in [1,4]:c.box('Small sash handle',(xx+step*.32,y+out*.19,z-.2),(.018,.06,.16),dark,.003)
def wing(side):
    # Wall segments form openings; no solid wall is placed behind windows.
    a,b=15.7,49.0;center=side*(a+b)/2
    for level in range(5):
        base=.85+level*3.8
        c.box('Wing floor slab',(center,59,base),(b-a,13.3,.24),stone)
        for fy,out in [(52.55,-1),(65.45,1)]:
            c.box('Wing floor spandrel',(center,fy,base+.7),(b-a,.30,1.30),grey)
            c.box('Wing upper fascia',(center,fy,base+3.52),(b-a,.33,.50),stone)
            for k in range(6):
                xx=side*(a+(k+.5)*(b-a)/6)
                windows_y(xx,fy+out*.17,base+2.2,4.75,2.10,out)
            for k in range(7):
                xx=side*(a+k*(b-a)/6)
                c.box('Wing vertical frame pier',(xx,fy+out*.13,base+1.92),(.42,.56,3.8),stone)
                c.box('Paired pier inset',(xx+.10,fy+out*.425,base+1.92),(.055,.018,3.72),grey)
            c.box('Continuous projecting floor belt',(center,fy+out*.27,base+3.65),(b-a+.25,.62,.18),white,.01)
        # Side enclosure and deliberately empty interior floor; external fidelity only.
        for xx in [side*a,side*b]:c.box('Wing end wall',(xx,59,base+1.9),(.25,12.9,3.8),stone)
        for k in range(1,6):
            xx=side*(a+k*(b-a)/6)
            c.box('Interior partition',(xx,59,base+1.85),(.12,12.7,3.45),inside)
    c.box('Wing roof deck',(center,59,20.0),(b-a+.6,14.1,.26),stone)
    # Roof pergola and parapets visible in ground and aerial views.
    for fy in [52.1,65.9]:
        c.box('Wing roof parapet',(center,fy,20.44),(b-a+.7,.24,.76),stone)
        c.box('Wing roof pergola outer beam',(center,fy,22.05),(b-a+1.1,.33,.30),white)
        for k in range(7):c.box('Wing pergola column',(side*(a+k*(b-a)/6),fy,21.1),(.32,.32,1.75),stone)
    for k in range(35):c.box('Wing pergola slat',(side*(a+k*(b-a)/34),59,22.04),(.10,14.2,.18),white)
    c.box('Wing recessed roof plant room',(side*41,59,21.2),(6,5,2.3),stone,.02)
    c.box('Roof plant room cap',(side*41,59,22.41),(6.3,5.3,.16),stone,.01)
    for k in range(4):
        c.box('Roof vent',(side*(38.8+k*1.4),56.47,21.45),(1.05,.05,.8),dark)
        for z in [21.15,21.3,21.45,21.6,21.75]:c.box('Vent louvre',(side*(38.8+k*1.4),56.42,z),(1.07,.09,.035),steel)
for side in [-1,1]:wing(side)
# Rear end returns and open links are visible at both ends in 354/l and 354/r.
# Their exact depth is estimated; openings follow the photographed small transoms.
for side in [-1,1]:
    x=side*43
    c.box('Rear return foundation',(x,76.5,.48),(11,12,1.1),stone)
    for level in range(4):
        base=1.05+level*3.8
        c.box('Rear return floor',(x,76.5,base),(10,11,.22),stone)
        for xx in [x-5,x+5]:c.box('Rear return side wall',(xx,76.5,base+1.85),(.24,11,3.7),white)
        for yy in [71,82]:
            c.box('Return transom lower wall',(x,yy,base+1.20),(10,.24,2.4),white)
            c.box('Return transom upper wall',(x,yy,base+3.37),(10,.24,.65),white)
            for dx in [-3,0,3]:
                c.box('Return high transom',(x+dx,yy+( -.14 if yy==71 else .14),base+2.74),(2,.03,.56),glass[2])
                for dd in [-1,0,1]:c.box('Return transom frame',(x+dx+dd,yy+( -.17 if yy==71 else .17),base+2.74),(.045,.07,.59),white)
        if level>0:
            c.box('Rear open link slab',(x,68.2,base),(4,5.6,.24),stone)
            for xx in [x-1.9,x+1.9]:
                for z in [base+.25,base+.55,base+.85,base+1.05]:c.rod('Rear link handrail',(xx,65.4,z),(xx,71,z),.022,steel)
                for yy in [65.5,67.3,69.1,70.9]:c.rod('Rear link upright',(xx,yy,base),(xx,yy,base+1.08),.023,steel)
    c.box('Rear return flat roof',(x,76.5,16.35),(10.4,11.4,.30),stone)
    c.box('Rear return parapet front',(x,70.95,16.8),(10.4,.25,.65),white)
    c.box('Rear return parapet rear',(x,82.05,16.8),(10.4,.25,.65),white)
print('WZMS_WINGS_READY',flush=True)
c.collection('22_Portal_Stone_Piers')
for side in [-1,1]:
    x=side*9.0
    c.box('Tall portal limestone pier',(x,58,12.0),(3.0,12.0,22.0),stone)
    c.box('Portal pier raised roof fin',(x,58,23.2),(3.0,8.0,2.3),stone)
    # Real narrow recessed panel joints on front/back and opening-facing sides.
    for y in [51.992,64.008]:
        for k in range(28):c.box('Pier horizontal panel seam',(x,y,1.05+k*.80),(3.0,.012,.009),joint)
        for xx in [x-.75,x,x+.75]:c.box('Pier vertical panel seam',(xx,y,12),(.009,.012,21.9),joint)
    for xx in [side*7.493,side*10.507]:
        for k in range(28):c.box('Pier flank horizontal seam',(xx,58,1.05+k*.80),(.012,12,.009),joint)
        for y in range(53,64):c.box('Pier flank vertical seam',(xx,y,12),(.012,.009,21.9),joint)
c.collection('23_Portal_Glazed_Stairs')
for side in [-1,1]:
    x=side*13.25
    c.box('Stair glazed tower dark interior',(x,54.5,9.8),(5,5.4,18),inside)
    # Glazing on three faces with projecting horizontal sunshades.
    for level in range(23):
        z=1.45+level*.76
        c.box('Stair glass horizontal pane',(x,51.64,z),(5.05,.03,.73),glass[level%4])
        c.box('Stair projecting horizontal fin',(x,51.47,z-.39),(5.40,.40,.075),steel)
        for xx in [x-2.56,x+2.56]:
            c.box('Stair side glass',(xx,54.25,z),(.028,5.24,.73),glass[level%4])
            c.box('Stair side horizontal fin',(xx,54.2,z-.39),(.30,5.60,.075),steel)
    for k in range(6):c.box('Stair facade vertical mullion',(x-2.5+k,51.57,9.8),(.045,.12,18.4),steel)
    c.box('Glazed stair projecting canopy',(x,54.1,19.45),(5.7,6.1,.28),white,.015)
c.collection('24_Elevated_Glass_Bridges')
# Front bridge spans two storeys; rear bridge is stepped up as observed from below.
for name,y,depth,bottom,top in [('Front',54.0,4.0,12.4,20.45),('Rear',62.15,3.7,16.15,20.45)]:
    c.box(name+' bridge soffit',(0,y,bottom),(15.0,depth,.26),stone)
    c.box(name+' bridge roof slab',(0,y,top),(15.0,depth,.25),stone)
    for fy in [y-depth/2,y+depth/2]:
        c.box(name+' green curtain wall',(0,fy,(bottom+top)/2),(15,.035,top-bottom),glass[0])
        for k in range(21):c.box(name+' curtain vertical fin',(-7.5+k*.75,fy-.06,(bottom+top)/2),(.052,.19,top-bottom+.1),steel)
        for j in range(int((top-bottom)/1.25)+1):c.box(name+' curtain transom',(0,fy-.03,bottom+j*1.25),(15,.095,.042),steel)
    for x in range(-7,8):c.box(name+' soffit panel joint',(x,y,bottom-.136),(.009,depth,.009),joint)
    for k in range(int(depth)):c.box(name+' soffit transverse seam',(0,y-depth/2+k,bottom-.137),(15,.009,.009),joint)
    if name=='Front':c.box('Front bridge intermediate floor',(0,y,16.22),(15,depth,.20),stone)
# Shallow arched metal roof, with thickness and ribs. Real underside remains visible.
c.collection('25_Portal_Curved_Roof')
v,f=[],[];segments=64
for i in range(segments+1):
    x=-19+i*38/segments;z=22.20+1.10*(1-(x/19)**2)
    v.extend([(x,50.5,z),(x,66.0,z),(x,50.5,z+.19),(x,66.0,z+.19)])
for i in range(segments):
    a=4*i;b=a+4
    f.extend([(a,b,b+1,a+1),(a+2,a+3,b+3,b+2),(a,a+2,b+2,b),(a+1,b+1,b+3,a+3)])
f.extend([(0,1,3,2),(256,258,259,257)])
c.mesh('Broad shallow-arched roof',v,f,roofmat)
for i in range(65):
    x=-19+i*38/64;z=22.20+1.10*(1-(x/19)**2)
    c.rod('Roof standing seam',(x,50.5,z+.20),(x,66,z+.20),.018,roofmat,sides=6)
for y in [51.0,54.7,58.4,62.1,65.7]:
    for i in range(32):
        x=-19+i*38/32;xx=x+38/32
        z=22.16+1.1*(1-(x/19)**2);zz=22.16+1.1*(1-(xx/19)**2)
        c.rod('Exposed roof underside rib',(x,y,z),(xx,y,zz),.045,white,sides=6)
print('WZMS_PORTAL_READY',flush=True)
c.collection('26_Building_Exterior_Details')
# National Civilized Campus sign is legible in 353/l; other invented plaques are omitted.
red=c.material('Campus honour sign red',(.45,.018,.018),.44)
c.box('Honour sign red plinth',(3.6,48.74,.26),(5.8,.52,.50),red,.02)
c.text('Honour sign','全国文明校园',(3.6,48.43,.58),.48,white)
c.text('Honour sign English','NATIONAL CIVILIZED CAMPUS',(3.6,48.43,.23),.135,white)
# Surface-mounted air conditioners on back elevation, as visible from lakeside.
for side in [-1,1]:
    for level in range(1,5):
        for k in [1,3,5]:
            x=side*(16+k*5.5);z=level*3.8+1.9
            c.box('Rear AC housing',(x,66.0,z),(.95,.42,.63),white,.025)
            c.box('AC grille',(x,66.23,z),(.78,.03,.47),grey)
            for j in range(9):c.box('AC grille slat',(x-.34+j*.085,66.252,z),(.02,.019,.45),white)
            for dx in [-.3,.3]:c.box('AC wall bracket',(x+dx,65.86,z-.39),(.04,.72,.05),steel)
    for y in [53.3,64.5]:c.rod('Wing rainwater pipe',(side*48.7,y,.7),(side*48.7,y,20.1),.055,white,sides=10)
    for j in range(4):
        # Trimmed trees keep windows visible and align with the 366 roadside strip.
        x=side*(21+j*7)
        c.tree('Trimmed facade tree',x,49.6,4.2,1.25,960+j+side*20,True)
c.collection('27_Lakeside_Building_Edge')
c.box('Raised lakeside walk',(0,67.9,.50),(102,4.7,1.04),floor)
c.box('Lakeside retaining wall',(0,70.35,.68),(103,.38,1.4),stone,.022)
c.box('Lakeside planting substrate',(0,69.7,.70),(102,.9,.45),c.material('Planting soil',(.06,.044,.025)))
o=c.planting('Lakeside planting strip',(0,69.7),(101,.9),.52,717,650);o.location.z=1.25
for x in range(-48,49,6):
    c.box('Recessed retaining-wall luminaire',(x,70.145,.82),(.26,.025,.13),dark,.012)
    c.box('Wall light lens',(x,70.127,.80),(.18,.01,.034),white)
# Water surface provides actual depth, reflections and a north-side visual context.
water=c.material('Campus lake water',(.11,.16,.085),.17,.1)
pn=next(n for n in water.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
pn.inputs['Transmission Weight'].default_value=.25;pn.inputs['IOR'].default_value=1.333
c.noise(water,4.2,.28,.085)
c.box('South lake water patch',(0,108,-.65),(110,74,.06),water)
c.box('South lake bed',(0,108,-2.0),(110,74,.14),c.material('Lake silt',(.10,.11,.055)))
c.collection('28_Building_Cameras')
c.camera('09_Portal_from_plaza',(-2,18,1.72),(0,54,9.2),27)
c.camera('10_Portal_underside',(0,57,2.76),(0,53.5,19.2),22)
c.camera('11_Building_lakeside',(31,96,8),(0,59,10),31)
c.camera('12_Building_overview',(78,-5,61),(0,49,7.0),42)
c.camera('13_Honour_sign_detail',(3.6,42.5,1.5),(3.6,48.5,.52),48)
scene.camera=scene.objects['09_Portal_from_plaza']
scene['scope']='South gate + inner plaza + Dehan/Guanzhen exterior; north route continues in v0.0.6'
# Correct inherited normalized noise on long slabs: physical object coordinates
# avoid stretched horizontal grain on stair treads and stone seats.
for mat in bpy.data.materials:
    if not mat.use_nodes:continue
    nodes,links=mat.node_tree.nodes,mat.node_tree.links
    for node in list(nodes):
        if node.type=='TEX_NOISE' and not node.inputs['Vector'].is_linked:
            co=nodes.new('ShaderNodeTexCoord');links.new(co.outputs['Object'],node.inputs['Vector'])
c.save(c.ROOT/'models/campus/WZMS_Campus_v005.blend','v0.0.5',[119232349,119232352,119232353,119232354,119232366,119232348])
print('WZMS_BUILD_COMPLETE v0.0.5',flush=True)
