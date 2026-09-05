"""v010: three-storey canteen exterior, paired windows and tiled forecourt.
Reference 425 F and 426 F, with six-face previews. Interiors remain later scope.
"""
import sys,math
from pathlib import Path
import bpy
sys.path.insert(0,str(Path(__file__).parent))
import campus_common as c
import north_common as n
import north_landscape as land
scene=bpy.data.scenes['WZMS_Campus'];c.activate(scene);p=n.palette()
c.collection('70_Canteen_Forecourt_And_Steps')
grid=bpy.data.materials['North white square tile paving'];green=bpy.data.materials['Zhongshan sidepath green border']
c.box('Canteen tiled forecourt base',(121,372,-.17),(42,57,.32),grid)
for x in range(102,142,4):c.box('Canteen longitudinal green tile band',(x,372,-.002),(.22,57,.016),green)
for y in range(344,402,4):c.box('Canteen transverse green tile band',(121,y,-.002),(42,.22,.016),green)
blue=c.material('Canteen blue tile intersection',(.025,.20,.29),.75)
for x in range(102,142,4):
    for y in range(344,402,4):c.box('Canteen blue tile crossing',(x,y,.008),(.24,.24,.012),blue)
steps=n.paving('Canteen rose granite steps',(.46,.28,.23),(.8,.4),.003)
for node in steps.node_tree.nodes:
    if node.type=='TEX_BRICK':node.inputs['Color2'].default_value=(.43,.26,.22,1)
for i in range(7):
    a=106.5+i*.38;b=111.3
    c.box('Canteen long front stair',((a+b)/2,374,(i+1)*.075-.01),(b-a,32,(i+1)*.15),steps)
    a=347.6+i*.35;b=351.3
    c.box('Canteen south entry stair',(125,(a+b)/2,(i+1)*.075-.01),(15,b-a,(i+1)*.15),steps)
c.box('Canteen main raised floor',(125,373,.51),(28,44,1.06),steps)
for yy in [358,390]:
    c.rod('Canteen stair end handrail',(106.6,yy,1.05),(110,yy,2.03),.033,p['steel'])
    for j in range(5):c.rod('Canteen stair railing upright',(106.6+j*.72,yy,j*.21),(106.6+j*.72,yy,1.05+j*.21),.026,p['steel'])
for y in [355,369,387,397]:
    c.box('Canteen path drain',(103.5,y,-.004),(.5,.8,.06),p['dark'])
    for j in range(10):c.box('Canteen drain grille',(103.5,y-.36+j*.08,.012),(.5,.018,.02),p['steel'])

c.collection('71_Canteen_Ground_Floor_Glazing')
for x in [111,139]:c.box('Canteen granite base skirt',(x,373,1.15),(.30,44,.24),steps)
c.box('Canteen south granite skirt left',(117.25,351,1.15),(12.5,.30,.24),steps)
c.box('Canteen south granite skirt right',(132.25,351,1.15),(13.5,.30,.24),steps)
c.box('Canteen rear ground enclosure',(139,373,2.9),(.28,44,3.72),p['white'])
c.box('Canteen north ground enclosure',(125,395,2.9),(28,.28,3.72),p['white'])
c.box('Canteen long glazing lintel',(111,373,4.68),(.35,44,.28),p['white'])
c.box('Canteen south corner closing pier',(113.36,351,2.9),(.46,.30,3.72),p['white'])
glass=c.material('Canteen green clear glass',(.095,.24,.22),.15,.18)
gp=next(v for v in glass.node_tree.nodes if v.type=='BSDF_PRINCIPLED');gp.inputs['Transmission Weight'].default_value=.35;gp.inputs['Coat Weight'].default_value=.45
for y in range(354,394,3):
    c.box('Canteen long window glass',(110.94,y,2.93),(.028,2.83,3.30),glass)
    for yy in [y-1.44,y+1.44]:c.box('Canteen full height window mullion',(110.83,yy,2.94),(.16,.075,3.39),p['white'])
    for z in [1.25,1.9,3.9,4.62]:c.box('Canteen window transom',(110.82,y,z),(.15,2.93,.07),p['white'])
    c.box('Canteen pale blue glazing safety stripe',(110.80,y,2.08),(.012,2.82,.12),blue)
for x in [115,118,121,124,127,130,133,136]:
    if x==124:
        # A usable entrance opening with a static open leaf, keeping glazing out of the walking line.
        c.box('Canteen south door sidelight',(123.05,350.93,2.93),(.96,.028,3.30),glass)
        c.box('Canteen south door overlight',(124,350.93,4.28),(2.83,.028,.62),glass)
        for xx in [122.56,123.55,125.44]:c.box('Canteen south entry upright',(xx,350.82,2.94),(.065,.16,3.39),p['white'])
        for z in [3.94,4.62]:c.box('Canteen south entry header',(124,350.81,z),(2.93,.15,.07),p['white'])
        for z in [1.25,1.9]:c.box('Canteen south sidelight rail',(123.05,350.81,z),(.97,.15,.07),p['white'])
        c.box('Canteen south door OPEN leaf',(125.49,351.76,2.53),(.028,1.76,2.95),glass)
        for yy in [350.88,352.64]:c.box('Canteen open door stile',(125.49,yy,2.53),(.12,.06,3.02),p['white'])
        for z in [1.04,3.99]:c.box('Canteen open door rail',(125.49,351.76,z),(.12,1.82,.06),p['white'])
        c.rod('Canteen open door handle',(125.39,352.4,2.0),(125.39,352.4,2.45),.019,p['steel'])
        continue
    c.box('Canteen south glass door and window',(x,350.93,2.93),(2.83,.028,3.30),glass)
    for xx in [x-1.44,x+1.44]:c.box('South canteen window stile',(xx,350.82,2.94),(.075,.16,3.39),p['white'])
    for z in [1.25,1.9,3.9,4.62]:c.box('South canteen window transom',(x,350.81,z),(2.93,.15,.07),p['white'])
for y in [357.5,374,390.5]:
    c.box('Canteen ground structural pier',(110.85,y,2.9),(.55,.50,3.72),p['white'])
    for yy in [y-1.0,y+1.0]:c.rod('Canteen door pull handle',(110.67,yy,2.05),(110.67,yy,2.53),.019,p['steel'])
for x,y in [(113,359),(113,388),(136,353)]:
    c.rod('Canteen queue post',(x,y,1.04),(x,y,2.0),.027,p['steel'],sides=12)
    n.disk('Canteen queue post foot',x,y,1.045,.18,p['steel'],40)
c.box('Canteen entrance red queue strap',(113,362,1.86),(.025,6,.055),c.material('Canteen barrier red webbing',(.52,.018,.012),.75))
c.box('Canteen front canopy',(110.8,373,4.85),(1.35,44.5,.25),p['white'])
c.box('Canteen south canopy',(125,350.8,4.85),(28.5,1.35,.25),p['white'])
for y in range(354,394,4):c.rod('Canteen soffit round light',(110.42,y,4.69),(110.42,y,4.73),.16,p['white'],sides=24)
# Only immediate objects visible through glazing, not a completed dining interior.
for y in [363,369,379,385]:
    c.box('Visible dining table',(113.6,y,1.82),(1.3,1.8,.065),p['white'],.025)
    for xx in [113.1,114.1]:
        for yy in [y-.6,y+.6]:c.rod('Visible table leg',(xx,yy,1.04),(xx,yy,1.79),.023,p['steel'])
    for xx in [112.5,114.7]:c.box('Visible dining bench seat',(xx,y,1.48),(.36,1.75,.065),blue,.018)

c.collection('72_Canteen_Upper_White_Facades')
wall=c.material('Canteen aged warm white render',(.72,.74,.70),.86);c.noise(wall,48,.16,.009)
def narrow_x(y,z,x=110.84):
    c.box('Canteen narrow window glass',(x,y,z),(.035,.66,2.32),glass)
    for yy in [y-.36,y+.36]:c.box('Canteen narrow vertical frame',(x-.06,yy,z),(.13,.055,2.44),p['white'])
    for zz in [z-1.18,z+.63,z+1.18]:c.box('Canteen narrow transom',(x-.06,y,zz),(.13,.76,.05),p['white'])
    c.box('Canteen lower narrow centre stile',(x-.06,y,z-.275),(.13,.028,1.81),p['white'])
    c.box('Canteen projecting narrow sill',(x-.14,y,z-1.24),(.4,.88,.13),p['stone'])
def narrow_y(x,y,z,out):
    c.box('Canteen end paired narrow glass',(x,y,z),(.66,.035,2.32),glass)
    for xx in [x-.36,x+.36]:c.box('Canteen end narrow stile',(xx,y+out*.06,z),(.055,.13,2.44),p['white'])
    for zz in [z-1.18,z+.63,z+1.18]:c.box('Canteen end narrow transom',(x,y+out*.06,zz),(.76,.13,.05),p['white'])
    c.box('Canteen end lower centre stile',(x,y+out*.06,z-.275),(.028,.13,1.81),p['white'])
    c.box('Canteen end narrow sill',(x,y+out*.14,z-1.24),(.88,.4,.13),p['stone'])
for level in range(2):
    base=5.05+level*4.25
    c.box('Canteen upper structural floor',(125,373,base),(28,44,.23),p['stone'])
    for j in range(5):
        yy=355.4+j*8.8
        c.box('Canteen upper sill wall',(111,yy,base+.425),(.28,8.8,.85),wall)
        c.box('Canteen upper lintel wall',(111,yy,base+3.72),(.28,8.8,1.06),wall)
        for a,b in [(-4.4,-1.1),(-.42,.42),(1.1,4.4)]:c.box('Canteen paired window side wall',(111,yy+(a+b)/2,base+2.025),(.28,b-a,2.35),wall)
        for dy in [-.76,.76]:narrow_x(yy+dy,base+2.025)
    for y in [351,395]:
        c.box('Canteen end lower wall',(125,y,base+.425),(28,.28,.85),wall)
        c.box('Canteen end upper wall',(125,y,base+3.72),(28,.28,1.06),wall)
        for x in [114.5,121.5,128.5,135.5]:
            for dx in [-.70,.70]:narrow_y(x+dx,y+(-.18 if y==351 else .18),base+2.025,-1 if y==351 else 1)
            for a,b in [(-3.5,-1.03),(-.37,.37),(1.03,3.5)]:c.box('Canteen end narrow window pier',(x+(a+b)/2,y,base+2.025),(b-a,.28,2.35),wall)
    c.box('Canteen rear service envelope',(139,373,base+2.12),(.28,44,4.25),wall)
    for j in range(6):
        c.box('Canteen rear high service window',(139.15,354+j*7.2,base+2.7),(.04,2.0,.85),glass)
    # Sparse large panel seams in the photos, not a dense tile facade.
    for z in [base+.02,base+2.1,base+4.21]:c.box('Canteen long horizontal facade seam',(110.845,373,z),(.01,44,.012),p['seam'])
for y in [351,359.8,368.6,377.4,386.2,395]:c.box('Canteen vertical facade panel seam',(110.84,y,9.3),(.012,.012,8.5),p['seam'])

c.collection('73_Canteen_Corner_Glass_And_Roof')
for j in range(16):
    z=1.35+j*.77
    c.mesh('Canteen corner angled glass closure',[(110.80,351.05,z-.375),(111.05,350.79,z-.375),(111.05,350.79,z+.375),(110.80,351.05,z+.375)],[(0,1,2,3)],glass)
    c.rod('Canteen corner continuous fin',(110.59,351.0,z-.39),(111.0,350.58,z-.39),.035,p['white'],sides=4)
    c.box('Canteen corner glass front',(110.80,352.1,z),(.028,2.1,.75),glass)
    c.box('Canteen corner glass side',(112.1,350.79,z),(2.1,.028,.75),glass)
    c.box('Canteen corner front projecting fin',(110.59,352.1,z-.39),(.47,2.35,.065),p['white'])
    c.box('Canteen corner side projecting fin',(112.1,350.58,z-.39),(2.35,.47,.065),p['white'])
c.box('Canteen main flat roof',(125,373,13.6),(28.5,44.5,.28),p['stone'])
for x in [110.9,139.1]:c.box('Canteen roof parapet long',(x,373,14.07),(.25,44.5,.72),wall)
for y in [350.9,395.1]:c.box('Canteen roof parapet end',(125,y,14.07),(28.5,.25,.72),wall)
for x,y in [(120,360),(132,379)]:
    c.box('Canteen rooftop service enclosure',(x,y,14.4),(4.5,5,1.4),p['stone'])
    for j in range(6):c.box('Canteen service enclosure louver',(x-2.27,y,13.99+j*.14),(.06,4.5,.035),p['seam'])

c.collection('74_Canteen_Signage_And_Street_Furniture')
letter=c.material('Canteen dark wall lettering',(.055,.063,.052),.6)
c.box('Canteen conservation sign white field',(110.70,391,2.84),(.08,4.5,2.8),wall)
c.text('Canteen conservation headline','节约粮食  杜绝浪费',(110.64,391,2.93),.31,letter,(math.pi/2,0,-math.pi/2))
c.text('Canteen conservation subline','文明用餐  珍惜粮食',(110.64,391,2.42),.19,letter,(math.pi/2,0,-math.pi/2))
ornament=c.material('Canteen conservation green ornament',(.025,.30,.12),.67)
verts=[];faces=[]
for j in range(97):
    a=j*math.tau/96
    for r in [.98,1.025]:verts.append((110.635,391+r*math.cos(a),2.84+r*math.sin(a)))
for j in range(96):faces.append((j*2,j*2+1,j*2+3,j*2+2))
c.mesh('Canteen conservation circular motif',verts,faces,ornament)
for j in range(6):
    yy=390.35+j*.25
    c.mesh('Canteen conservation green hills',[(110.63,yy,2.1),(110.63,yy+.15,2.3+(j%3)*.10),(110.63,yy+.30,2.1)],[(0,1,2)],ornament)
for y in [355,394]:
    c.box('Canteen wall notice case',(110.72,y,2.35),(.10,1.4,1.25),p['steel'],.012)
    c.box('Canteen wall notice paper',(110.65,y,2.35),(.02,1.25,1.1),p['white'])
    for j in range(7):c.box('Canteen notice print layout',(110.63,y,1.94+j*.125),(.014,1.08,.016),p['seam'])
for y in [354.5,395]:
    for dy,color in [(-.3,(.02,.20,.30)),(.3,(.03,.26,.14))]:
        c.box('Canteen classified waste bin',(103.8,y+dy,.54),(.6,.53,1.08),p['steel'],.03)
        c.box('Canteen bin classification panel',(103.48,y+dy,.55),(.02,.39,.65),c.material('Canteen bin '+str(color),color))
        c.box('Canteen bin dark opening',(103.47,y+dy,.98),(.025,.39,.10),p['dark'])
for y in [362,382]:
    c.rod('Canteen exterior camera bracket',(110.4,y,4.8),(109.9,y,5.0),.02,p['steel'])
    c.box('Canteen exterior security camera',(109.84,y,5.02),(.32,.14,.14),p['white'],.018)

c.collection('75_Canteen_Court_And_Trees')
c.box('Canteen tree border soil',(99.3,375,-.16),(2.1,42,.30),p['green'])
proto=[scene.objects['Middle mature avenue tree scaffold branches'],scene.objects['Middle mature avenue tree canopy leaves']]
for j,y in enumerate([357,366,375,384,393]):n.duplicate_tree(proto,99.3,y,j*.89,.73)
c.planting('Canteen low hedge',(99.3,375),(1.5,41),.38,425,130)
courtgreen=c.material('Canteen court green acrylic',(.09,.22,.14),.86)
c.box('Canteen adjacent court pad',(87,379,-.19),(22,36,.34),courtgreen)
c.box('Canteen adjacent court red zone',(87,379,-.01),(15,28,.012),c.material('Canteen court warm red',(.32,.11,.08),.87))
line=c.material('Canteen court white paint',(.72,.75,.70),.84)
for x in [79.5,94.5]:c.box('Canteen court sideline',(x,379,.003),(.05,28,.012),line)
for y in [365,379,393]:c.box('Canteen court transverse line',(87,y,.003),(15,.05,.012),line)
n.disk('Canteen court centre circle',87,379,.012,1.8,line,96,1.75)
land.fence(98,361,397,3.0)
for y,side in [(366.5,-1),(391.5,1)]:
    c.rod('Canteen court hoop stand',(87,y+side*1.3,0),(87,y+side*1.3,3.4),.085,p['white'])
    c.rod('Canteen court hoop arm',(87,y+side*1.3,3.4),(87,y,3.4),.06,p['white'])
    c.box('Canteen court backboard',(87,y,3.4),(1.8,.06,1.05),glass)
    n.disk('Canteen court basketball rim',87,y-side*.38,3.04,.23,c.material('Canteen hoop orange',(.62,.10,.014),.45),48,.205)

c.collection('78_Canteen_Cameras')
c.camera('33_Canteen_arrival',(103.5,345,1.72),(113,359,5.2),29)
c.camera('34_Canteen_long_front',(102.8,359,1.72),(111,383,4.6),29)
c.camera('35_Canteen_stair_detail',(102.5,375,1.72),(110.9,374,2.4),33)
c.camera('36_Canteen_court_and_paving',(105,389,1.72),(100,362,2.0),30)
c.camera('37_Canteen_overview',(60,322,55),(113,372,5),38)
c.camera('37b_Canteen_south_entry',(125,343.5,1.72),(125,351.5,2.4),38)
scene.camera=scene.objects['33_Canteen_arrival']
scene['scope']='Integrated northward campus route plus canteen exterior and local forecourt. North gate remains final delivery.'
c.save(c.ROOT/'models/campus/WZMS_Campus_v010.blend','v0.0.10',[119232349,119232352,119232353,119232354,119232355,119232366,119232367,119232368,119232369,119232370,119232371,119232425,119232426])
print('WZMS_BUILD_COMPLETE v0.0.10',flush=True)
