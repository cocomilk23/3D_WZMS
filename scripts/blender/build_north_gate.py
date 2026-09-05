"""v011 north gate, photographic 351 F/R/B/L; all dimensions estimated.
The historic temporary furnishings are isolated. Boom pose is editable, not a UE controller.
"""
import sys,math,random
from pathlib import Path
import bpy
from mathutils import Matrix,Vector
sys.path.insert(0,str(Path(__file__).parent))
import campus_common as c
import north_common as n
import north_landscape as land
scene=bpy.data.scenes['WZMS_Campus'];c.activate(scene);p=n.palette()
front=(math.pi/2,0,math.pi) # text faces north, upright
white=p['white'];steel=p['steel'];dark=p['dark']
red=c.material('North gate enamel red',(.55,.023,.018),.48,.15)
yellow=c.material('North gate worn road yellow',(.65,.44,.055),.88)
navy=c.material('Police fascia midnight blue',(.012,.027,.063),.46)
stone=n.paving('North gate honed granite',(.46,.47,.44),(1.1,.65),.007)
concrete=n.paving('North gate concrete paving',(.43,.44,.40),(1.6,1.6),.005)
asphalt=c.material('North street weathered asphalt',(.17,.18,.17),.94);c.noise(asphalt,90,.65,.017)
glass=c.material('North guardroom clear glass',(.41,.53,.49),.12)
gp=next(q for q in glass.node_tree.nodes if q.type=='BSDF_PRINCIPLED');gp.inputs['Transmission Weight'].default_value=.72

c.collection('80_North_Gate_Approach_And_Street')
c.box('North gate terrain CONTEXT_ESTIMATED',(66,397,-.43),(190,90,.6),p['green'])
c.box('North gate inner paved apron',(54,372.5,-.17),(40,26,.32),concrete)
c.box('North gate red route continuation',(54,372.5,-.158),(8.6,26,.30),bpy.data.materials['Zhongshan rose granite slabs'])
c.box('North gate exterior paved apron',(54,388,-.17),(48,8,.32),concrete)
c.box('North local public street',(54,401,-.21),(142,20,.40),asphalt)
c.box('North opposite sidewalk',(54,414,-.14),(142,6,.26),concrete)
for y in [391,411]:
    for x in range(-16,125):
        if y==391 and 45<=x<=63:continue
        c.box('North street kerbstone',(x,y,.035),(.98,.20,.09),p['stone'],.012)
for x in [49.65,58.35]:
    for y in range(361,385):c.box('North approach stone edging',(x,y,.05),(.18,.98,.12),p['stone'],.01)
for y in [384,389]:
    c.box('North gate storm drain recess',(54,y,-.02),(9,.27,.08),dark)
    for j in range(113):c.box('North gate drain grate',(49.55+j*.08,y,.003),(.02,.27,.02),steel)
for x in [45,63]:c.box('North street yellow box edge',(x,394,-.006),(.14,10,.003),yellow)
for y in [389,399]:c.box('North street yellow box edge',(54,y,-.006),(18,.14,.003),yellow)
for sign in [-1,1]:
    for k in range(-4,11):
        # Clip diagonal paint segments to the actual yellow rectangle.
        pts=[]
        for i in range(401):
            xx=45+i*18/400;yy=sign*(xx-45)+385+k*2
            if 389<=yy<=399:pts.append((xx,yy,-.005))
        if len(pts)>1:
            a,b=Vector(pts[0]),Vector(pts[-1]);d=(b-a).normalized();side=Vector((-d.y,d.x,0))*.045
            c.mesh('North street yellow diagonal hatch',[a-side,a+side,b+side,b-side],[(0,1,2,3)],yellow)
for j in range(46):
    x=43+j*.5
    # Low arched cross section, with distinct bolts and alternating rubber sections.
    verts=[(x+dx,yy,zz) for dx in [-.245,.245] for yy,zz in [(389.6,.01),(389.75,.05),(389.9,.065),(390.05,.05),(390.2,.01)]]
    faces=[(i,i+1,i+6,i+5) for i in range(4)]
    c.mesh('North yellow black rubber speed bump',verts,faces,yellow if j%2 else dark)
    for y in [389.68,390.12]:n.disk('Speed bump fixing bolt',x,y,.035,.023,steel,12)
# White road divider with a gap opposite the campus crossing.
for a,b in [(-14,47),(62,123)]:
    for x in range(a,b,3):
        c.box('Street divider rubber foot',(x,402,.09),(.46,.40,.18),dark,.035)
        c.box('Street divider upright',(x,402,.64),(.075,.075,1.15),white)
    for z in [.26,1.16]:c.rod('Street divider horizontal rail',(a,402,z),(b,402,z),.028,white)
    for j in range(int((b-a)/.22)):c.rod('Street divider vertical picket',(a+j*.22,402,.28),(a+j*.22,402,1.14),.013,white,sides=6)
for x in [46.7,61.3]:
    c.rod('Street red white flexible bollard',(x,402,0),(x,402,1.07),.065,white,sides=16)
    for z in [.3,.65,.95]:c.rod('Street bollard red band',(x,402,z),(x,402,z+.11),.067,red,sides=16)

c.collection('81_North_Guardroom_And_Police_Office')
# From outside facing south, the guardroom is on the viewer's right (local west).
for cx,width in [(44,6),(36,10)]:
    c.box('North guardroom raised floor',(cx,381,.10),(width,10,.22),stone)
    c.box('North guardroom back wall',(cx,376,1.74),(width,.24,3.48),stone)
    for x in [cx-width/2,cx+width/2]:c.box('North guardroom flank wall',(x,381,1.74),(.24,10,3.48),stone)
    c.box('North guardroom front sill',(cx,386,.49),(width,.28,.98),stone)
    c.box('North guardroom front lintel',(cx,386,3.19),(width,.28,.58),stone)
    for x in [cx-width/2+.35,cx+width/2-.35]:c.box('North guardroom stone front pier',(x,386,1.93),(.70,.30,1.91),stone)
    span=width-1.5;left=cx-span/2
    for j in range(4):
        xx=left+(j+.5)*span/4
        c.box('North guardroom front glazing',(xx,386.03,1.95),(span/4-.065,.025,1.86),glass)
    for j in range(5):c.box('North guardroom window stile',(left+j*span/4,386.10,1.96),(.065,.13,1.94),white)
    for z in [1.0,2.26,2.9]:c.box('North guardroom window transom',(cx,386.11,z),(span,.13,.055),white)
    c.box('North guardroom roof slab',(cx,381.15,3.53),(width+.45,11,.30),stone)
    c.box('North guardroom projecting canopy',(cx,386.75,3.47),(width+.45,1.6,.18),white)
    c.box('North guardroom roof fascia',(cx,387.49,3.77),(width+.45,.15,.65),stone)
    # Curtains and immediate work furniture seen through the window.
    curtain=c.material('Guardroom cream curtain',(.57,.53,.43),.95)
    for side in [-1,1]:
        for k in range(7):c.rod('North guardroom curtain fold',(cx+side*(span/2-.12-k*.08),385.82,1.12),(cx+side*(span/2-.12-k*.08),385.82,2.88),.055,curtain,sides=8)
    c.box('North guardroom desk',(cx,384.9,.91),(2.4,.70,.06),p['stone'])
    c.box('North guardroom desktop display',(cx+.45,385.0,1.25),(.6,.09,.4),dark,.01)
    c.box('North guardroom side storage',(cx-1.5,382.8,.69),(.8,1.2,1.38),p['stone'])
# Open working side door facing the campus lane; frame placed within a wall opening.
side=scene.objects.get('North guardroom flank wall.001')
if side and abs(side.location.x-47)<.1:
    bpy.data.objects.remove(side,do_unlink=True)
    c.box('Guardroom lane side rear panel',(47,378.45,1.74),(.24,4.9,3.48),stone)
    c.box('Guardroom lane side front panel',(47,384.55,1.74),(.24,2.9,3.48),stone)
    c.box('Guardroom lane door lintel',(47,382,3.0),(.24,2.2,.96),stone)
    c.box('Guardroom lane door recess',(46.88,382,1.38),(.03,1.9,2.52),glass)
    for y in [381,383]:c.box('Guardroom lane door upright',(47.08,y,1.38),(.12,.065,2.62),white)
    c.rod('Guardroom side door pull',(47.18,381.85,1.1),(47.18,381.85,1.5),.02,steel)
c.box('North police office dark fascia',(36,387.60,3.80),(10.3,.10,.78),navy)
c.text('North police office title','温州中学警务室',(35.5,387.665,3.60),.56,white,front)
# Small sculpted emblem approximation, separately editable from lettering.
gold=c.material('Police emblem warm metal',(.53,.34,.07),.40,.6)
badgeX,badgeY,badgeZ=40.3,387.68,3.82
shield=[(-.27,.33),(.27,.33),(.30,-.03),(.15,-.31),(0,-.41),(-.15,-.31),(-.30,-.03)]
c.mesh('Police badge gold silhouette',[(badgeX+x,badgeY,badgeZ+z) for x,z in shield],[tuple(range(7))],gold)
c.mesh('Police badge blue inset',[(badgeX+x*.8,badgeY+.006,badgeZ+z*.8) for x,z in shield],[tuple(range(7))],navy)
land.ellipsoid('Police badge red roundel',(badgeX,badgeY+.018,badgeZ+.075),(.155,.025,.155),red,32,16)
for i in range(5):
    angle=i*math.tau/5;land.ellipsoid('Police badge gold detail',(badgeX+.073*math.cos(angle),badgeY+.049,badgeZ+.10+.067*math.sin(angle)),(.022,.008,.022),gold,10,6)
c.box('Guardroom blue street number',(46.15,386.18,2.54),(.65,.025,.58),navy)
c.text('Guardroom address street','温中路',(46.15,386.205,2.61),.12,gold,front)
c.text('Guardroom address number','16',(46.15,386.205,2.32),.26,gold,front)
c.box('Guardroom visitor notice',(46.15,386.18,1.78),(.65,.03,.69),white)
for j in range(7):c.box('Guardroom visitor print layout',(46.15,386.203,1.53+j*.072),(.53,.008,.012),navy)

c.collection('82_North_Entrance_Wall_And_Retractable_Gate')
c.box('North east granite entrance wall',(65,383.5,1.96),(11,.55,3.92),stone)
c.box('North east wall side return',(70.4,380.4,1.96),(.55,6.7,3.92),stone)
for x in [60,70]:
    c.rod('North wall floodlight bracket',(x,383.7,3.9),(x,383.6,4.2),.025,steel)
    o=c.box('North wall floodlight',(x,383.55,4.22),(.38,.16,.25),dark,.018);o.rotation_euler.x=.30
    c.box('North floodlight face',(x,383.65,4.22),(.30,.02,.18),white)
# Folded stainless gate remains clear of x=52/54/56 walking lanes.
for j in range(12):
    x=58.7+j*.24
    for y in [383.75,384.65]:
        c.rod('North retractable gate upright',(x,y,.17),(x,y,1.96),.031,steel,sides=10)
        c.rod('North retractable gate crown',(x,y,1.96),(x+.12,384.2,2.12),.027,steel,sides=10)
        if j<11:
            for za,zb in [(.37,1.76),(1.76,.37)]:c.rod('North gate scissor link',(x,y,za),(x+.24,y,zb),.024,steel,sides=8)
        c.rod('North retractable gate wheel',(x,y-.045,.13),(x,y+.045,.13),.105,dark,sides=16)
c.box('North retractable gate motor head',(58.45,384.2,1.08),(.48,1.05,2.1),steel,.035)
c.box('North retractable gate welcome panel',(58.45,384.75,1.06),(.37,.018,1.90),dark)
c.text('North gate welcome vertical','温\n州\n中\n学\n欢\n迎\n您',(58.45,384.772,1.76),.20,white,front)

# Explicit stone panel joints on vertical surfaces, preserving window openings.
c.collection('82_North_Entrance_Wall_And_Retractable_Gate')
panels=[o for o in scene.objects if o.type=='MESH' and o.data.materials and o.data.materials[0]==stone and any(k in o.name for k in ['wall','pier','sill','lintel','fascia'])]
for obj in panels:
    lo=[min(v.co[i] for v in obj.data.vertices)+obj.location[i] for i in range(3)]
    hi=[max(v.co[i] for v in obj.data.vertices)+obj.location[i] for i in range(3)]
    for axis in [0,1]:
        other=1-axis
        for sign in [-1,1]:
            face=(hi[axis] if sign>0 else lo[axis])+sign*.004
            for j in range(math.ceil(lo[2]/.65),math.floor(hi[2]/.65)+1):
                at=[0,0,j*.65];at[axis]=face;at[other]=(lo[other]+hi[other])/2
                size=[.009,.009,.009];size[other]=hi[other]-lo[other]
                c.box('North granite horizontal joint',at,size,p['seam'])
            for j in range(math.ceil(lo[other]/1.10),math.floor(hi[other]/1.10)+1):
                at=[0,0,(lo[2]+hi[2])/2];at[axis]=face;at[other]=j*1.1
                size=[.009,.009,hi[2]-lo[2]]
                c.box('North granite vertical joint',at,size,p['seam'])

c.collection('83_North_Editable_Boom_And_Security')
c.box('North boom concrete island',(48.55,384.4,.11),(1.40,1.80,.22),yellow,.08)
for j in range(5):c.box('North boom base black stripe',(48.04+j*.24,385.305,.12),(.12,.02,.17),dark)
c.box('North boom motor cabinet',(48.55,384.4,.71),(.70,.70,1.18),c.material('Boom motor bronze',(.34,.31,.21),.5,.4),.035)
c.box('North boom display housing',(48.55,384.80,1.40),(.80,.08,.38),dark,.018)
c.text('North boom display','欢迎入校',(48.55,384.85,1.32),.14,yellow,front)
pivot=bpy.data.objects.new('North boom OPEN_POSE rotate Y to 0 for closed reference',None);c.COL.objects.link(pivot);pivot.location=(48.55,384.4,1.27);pivot['closed_y_degrees']=0;pivot['open_y_degrees']=-78
before=set(scene.objects)
c.box('North boom horizontal arm',(53.50,384.4,1.27),(9.9,.12,.16),white)
c.box('North boom lower rail',(53.50,384.4,.31),(9.9,.07,.07),white)
for j in range(24):
    x=48.8+j*.40
    c.box('North boom fence vertical',(x,384.4,.79),(.055,.075,1.03),white)
    c.box('North boom fence red reflector',(x,384.45,1.07),(.057,.02,.15),red)
for j in range(10):c.box('North boom red arm segment',(48.8+j*.95,384.47,1.27),(.43,.018,.14),red)
bpy.context.view_layer.update()
for obj in set(scene.objects)-before:
    mw=obj.matrix_world.copy();obj.parent=pivot;obj.matrix_world=mw
pivot.rotation_euler.y=math.radians(-78)
for x,y in [(48,378),(62,382)]:
    c.rod('North entrance CCTV mast',(x,y,0),(x,y,4.8),.052,steel)
    c.box('North entrance CCTV crossarm',(x,y,4.68),(1.2,.07,.07),steel)
    for dx in [-.42,.42]:
        c.box('North entrance security camera',(x+dx,y+.12,4.75),(.17,.39,.16),white,.025)
        c.rod('North entrance camera lens',(x+dx,y+.32,4.75),(x+dx,y+.33,4.75),.05,dark,sides=14)
    land.ellipsoid('North entrance dome camera',(x,y,4.44),(.15,.15,.13),dark,24,12)
for x in [30.5,37,63,68.5,73]:land.ellipsoid('North spherical granite bollard',(x,388.7,.33),(.36,.36,.36),p['stone'],32,20)

c.collection('84_North_Historic_2022_Temporary_Furnishings_HIDEABLE')
tentblue=c.material('Historic canopy woven blue',(.018,.11,.39),.8);c.noise(tentblue,180,.13,.003)
tentgreen=c.material('Historic emergency tent canvas',(.30,.34,.17),.91);c.noise(tentgreen,130,.15,.003)
def popup(x,y):
    # Four peaked fabric panels, visible frame and accordion bracing.
    c.mesh('Historic blue canopy roof',[(x-2,y-1.8,2.55),(x+2,y-1.8,2.55),(x+2,y+1.8,2.55),(x-2,y+1.8,2.55),(x,y,3.32)],[(0,1,4),(1,2,4),(2,3,4),(3,0,4)],tentblue)
    for dx in [-2,2]:
        for dy in [-1.8,1.8]:c.rod('Historic canopy leg',(x+dx,y+dy,0),(x+dx,y+dy,2.56),.022,white,sides=8)
    for dy in [-1.8,1.8]:
        c.box('Historic blue canopy valance',(x,y+dy,2.44),(4,.018,.25),tentblue)
        for j in range(4):
            a=x-2+j
            c.rod('Historic canopy scissor',(a,y+dy,2.18),(a+1,y+dy,2.52),.012,white,sides=6)
            c.rod('Historic canopy scissor',(a,y+dy,2.52),(a+1,y+dy,2.18),.012,white,sides=6)
    for dx in [-2,2]:c.box('Historic canopy side valance',(x+dx,y,2.44),(.018,3.6,.25),tentblue)
for x in [34.3,38.4]:popup(x,388.8)
# Green temporary tent east of the entrance; opening faces the street.
x,y=68.4,387.6
c.mesh('Historic green tent roof',[(x-1.8,y-1.65,2.1),(x+1.8,y-1.65,2.1),(x+1.8,y+1.65,2.1),(x-1.8,y+1.65,2.1),(x,y-1.65,2.88),(x,y+1.65,2.88)],[(0,3,5,4),(1,4,5,2),(0,4,1),(3,2,5)],tentgreen)
for dx in [-1.8,1.8]:c.box('Historic green tent side',(x+dx,y,1.05),(.024,3.3,2.1),tentgreen)
c.box('Historic green tent back',(x,y-1.65,1.05),(3.6,.024,2.1),tentgreen)
for dx in [-1.29,1.29]:c.box('Historic green tent front flap',(x+dx,y+1.65,1.05),(1.02,.024,2.1),tentgreen)
c.box('Historic green tent raised flap',(x,y+1.65,2.03),(1.56,.04,.18),tentgreen)
c.box('Historic green tent red floor',(x,y,.015),(3.6,3.3,.035),red)
c.box('Historic temporary desk',(x,y+.6,.76),(1.20,.65,.07),p['stone'])
def poster(x,y,title):
    c.box('Historic information board backing',(x,y,1.15),(1.05,.035,1.6),navy)
    for dx in [-.55,.55]:c.rod('Historic information frame',(x+dx,y,.08),(x+dx,y,2.02),.019,steel,sides=8)
    for z in [.32,1.98]:c.rod('Historic information frame rail',(x-.55,y,z),(x+.55,y,z),.019,steel,sides=8)
    for dx in [-.43,.43]:c.rod('Historic information frame foot',(x+dx,y-.25,.07),(x+dx,y+.35,.07),.025,steel,sides=8)
    c.text('Historic poster visible headline',title,(x,y+.025,1.56),.17,white,front)
    for k in range(6):c.box('Historic poster simplified text line',(x,y+.025,.53+k*.12),(.85,.008,.025),white)
for x,title in [(33,'校园防疫'),(34.25,'禁止吸烟'),(35.5,'接送家长\n不聚集'),(64,'进校须知'),(65.25,'护校岗')]:poster(x,390.2,title)
c.box('Historic east wall display frame',(65,383.82,2.58),(6.5,.10,1.80),dark)
c.box('Historic east wall blue display',(65,383.88,2.58),(6.25,.025,1.56),c.material('Historic LED blue',(.013,.10,.33),.6))
c.text('Historic east wall display headline','戴口罩  共防疫',(65,383.905,2.55),.48,white,front)
c.box('Historic inner civilization board',(62.6,372,1.12),(4.5,.16,2.25),yellow)
c.text('Historic inner board headline','全国文明校园',(62.6,372.095,1.26),.42,red,front)

c.collection('85_North_Gate_Trees_And_Planting')
proto=[scene.objects['Middle mature avenue tree scaffold branches'],scene.objects['Middle mature avenue tree canopy leaves']]
for j,(x,y,s) in enumerate([(48,365,1),(60.2,366,1),(60.2,377,.96),(39,369,.9),(30,380,.88),(74,388,1.04),(25,414,.96),(42,414,1),(63,414,.94),(82,414,1)]):
    c.box('North street tree soil',(x,y,-.08),(2.3,2.3,.18),p['green'])
    n.duplicate_tree(proto,x,y,j*.93,s)
    c.rod('North tree trunk whitewash',(x,y,0),(x,y,.88),.30*s,white,.28*s,12)
for x,y in [(39,369),(60.2,366),(60.2,377)]:c.planting('North gate low planted bed',(x,y),(2.0,2.0),.32,int(x+y),125)

c.collection('86_North_Street_Residential_Context')
mint=c.material('Opposite apartment mint facade',(.49,.66,.59),.88);c.noise(mint,35,.12,.01)
awning=c.material('Opposite balcony green canopy',(.06,.30,.18),.56,.08)
shutter=c.material('Opposite shop weathered shutters',(.31,.28,.22),.84);c.noise(shutter,45,.2,.01)
# Street-facing facade reconstructed at contextual detail; interiors unmodelled.
c.box('Opposite residential background envelope',(54,424,9.9),(59,12,19.8),mint)
for j in range(9):
    x=28+j*6.5
    c.box('Opposite shopfront shutter',(x,417.93,1.62),(5.85,.06,3.05),shutter)
    for k in range(43):c.box('Opposite shutter horizontal rib',(x,417.87,.15+k*.07),(5.86,.04,.018),p['seam'])
    c.box('Opposite storefront signboard',(x,417.86,3.53),(6.2,.08,.70),navy if j%3==0 else white)
    c.box('Opposite shop dividing pier',(x-3.15,417.85,1.6),(.25,.35,3.2),p['stone'])
    for level in range(5):
        z=4.15+level*3.12
        c.box('Opposite apartment balcony slab',(x,417.3,z),(5.7,1.5,.18),white)
        n.window(x,417.90,z+1.42,4.6,2.25,-1,True)
        c.box('Opposite balcony white parapet',(x,416.62,z+.23),(5.55,.10,.38),white)
        for zz in [z+.48,z+1.18]:c.rod('Opposite balcony guard rail',(x-2.78,416.54,zz),(x+2.78,416.54,zz),.022,white,sides=8)
        for k in range(22):c.rod('Opposite balcony safety grille',(x-2.65+k*.25,416.52,z+.45),(x-2.65+k*.25,416.52,z+1.19),.010,steel,sides=5)
        if (j+level)%3!=0:
            for k in range(22):c.rod('Opposite enclosed balcony security bars',(x-2.65+k*.25,416.58,z+1.18),(x-2.65+k*.25,416.58,z+2.8),.009,steel,sides=5)
            c.box('Opposite balcony green awning',(x,417.18,z+2.85),(5.7,1.7,.055),awning)
        if (j+level)%7==0:
            cloth=c.material('Street laundry muted red',(.39,.03,.035),.92)
            for k in range(2):c.box('Opposite balcony hanging laundry',(x-.5+k*.7,416.49,z+1.02),(.5,.018,.76),cloth)
for x in [24.4,83.6]:c.box('Opposite residential white end pilaster',(x,423.8,10),(.24,12.2,20),white)
c.box('Opposite residential roof rim',(54,424,20.03),(59.5,12.5,.27),white)
for x in [32,51,72]:
    c.box('Opposite rooftop stair enclosure',(x,425.5,21.0),(6,5,1.8),mint)
    c.box('Opposite rooftop stair canopy',(x,425.5,21.94),(6.4,5.4,.18),white)

c.collection('88_North_Gate_And_Whole_Route_Cameras')
c.camera('38_North_gate_from_street',(54,398,1.72),(54,381,2.1),30)
c.camera('39_North_guardroom_and_police',(54,395,1.72),(39,386,2.0),32)
c.camera('40_North_gate_from_campus',(54,367,1.72),(54,389,2.2),30)
c.camera('41_North_gate_street_context',(59,389,1.72),(53,418,8.0),30)
c.camera('42_North_gate_overview',(104,424,58),(53,381,2),45)
overview=c.camera('43_Complete_route_overview',(255,-185,540),(45,205,0),42)
overview.data.type='ORTHO';overview.data.ortho_scale=720
c.camera('44_Buqing_to_north_integrated',(54,171,1.72),(54,233,6),30)
scene.camera=scene.objects['38_North_gate_from_street']
scene['scope']='Integrated exterior route from south gate through Buqing plaza and Zhongshan avenue to north gate, including canteen exterior. Other campus districts and full interiors remain future scope.'
scene['north_boom_note']='Editable static open pose. Set object North boom OPEN_POSE rotation Y to 0 for the closed photographic state. No gameplay automation.'
c.save(c.ROOT/'models/campus/WZMS_Campus_v011.blend','v0.0.11',[119232349,119232351,119232352,119232353,119232354,119232355,119232366,119232367,119232368,119232369,119232370,119232371,119232425,119232426])
print('WZMS_BUILD_COMPLETE v0.0.11',flush=True)
