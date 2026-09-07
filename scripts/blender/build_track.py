"""v031 running track, natural dry turf and blue-white covered grandstand."""
import bpy,math,random,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import campus_common as c,north_common as n,north_landscape as l
import south_detail_common as s,island_common as h,sports_common as q,culture_common as u
sc=bpy.data.scenes['WZMS_Campus'];c.activate(sc);p=n.palette()
cx,cy=-85,280;half=(400-2*math.pi*(36.5+.30))/4;inner=36.5
def capsule(r):
    pts=[]
    for i in range(97):
        a=math.pi*i/96;pts.append((cx+r*math.cos(a),cy+half+r*math.sin(a)))
    for i in range(1,41):pts.append((cx-r,cy+half-2*half*i/40))
    for i in range(1,97):
        a=math.pi+math.pi*i/96;pts.append((cx+r*math.cos(a),cy-half+r*math.sin(a)))
    for i in range(1,40):pts.append((cx+r,cy-half+2*half*i/40))
    return pts
def band(name,ri,ro,z,mat):
    a,b=capsule(ri),capsule(ro);v=[(*p,z) for pair in zip(a,b) for p in pair];nn=len(a)
    return c.mesh(name,v,[(2*i,2*i+1,2*((i+1)%nn)+1,2*((i+1)%nn)) for i in range(nn)],mat)
c.collection('270_Track_Field_And_Runoff')
# Replace only the explicitly labelled thin sports-side placeholder ground.
h.retire('v0.0.31',names=['Nantian western athletic verge CONTEXT_ESTIMATED'])
soil=s.mottled('Athletics shaded soil',[(.075,.09,.027),(.20,.22,.08)],2)
c.box('Athletics continuous retained ground',(-92,281,-.80),(136,184,1.5),soil)
c.box('Athletics southern connection infill ESTIMATED',(-50.5,168,-.90),(45,44,1.60),soil)
red=s.mottled('Athletics granular red rubber',[(.21,.055,.038),(.38,.12,.087)],2)
c.noise(red,165,.29,.005)
red2=s.mottled('Athletics alternate rubber lane',[(.235,.063,.044),(.41,.13,.09)],2)
c.noise(red2,165,.29,.005)
white=c.material('Athletics worn white track markings',(.70,.71,.65),.89)
band('Athletics continuous outer grey safety walk',inner+9.85,inner+12.2,.015,n.paving('Athletics perimeter grey paving',(.38,.40,.35),(.6,.4),.006))
for lane in range(8):band('Athletics red running lane '+str(lane+1),inner+lane*1.22,inner+(lane+1)*1.22,.03,red if lane%2 else red2)
for lane in range(9):band('Athletics continuous lane marking '+str(lane),inner+lane*1.22-.025,inner+lane*1.22+.025,.043,white)
band('Athletics inner concrete kerb',inner-.12,inner,.04,p['stone'])
turf=s.mottled('Athletics dry yellow green natural turf',[(.19,.18,.067),(.39,.35,.15)],2.5)
c.noise(turf,145,.24,.012)
# Reuse readable grass patches from the original downward panorama as material
# samples. The original JPEG is packed intact; UV windows avoid the nadir stitch.
im=bpy.data.images.load(str(c.ROOT/'reference/panoramas/faces/119232357/d.jpg'),check_existing=True);im.pack()
nd,ln=turf.node_tree.nodes,turf.node_tree.links;co=nd.new('ShaderNodeTexCoord');samples=[]
for scale,offset,angle in [(1.10,(.75,.36,0),0),(.89,(.73,.08,0),1.03)]:
    rotate=nd.new('ShaderNodeVectorRotate');rotate.rotation_type='AXIS_ANGLE';rotate.inputs['Axis'].default_value=(0,0,1);rotate.inputs['Angle'].default_value=angle;ln.new(co.outputs['Object'],rotate.inputs['Vector'])
    mul=nd.new('ShaderNodeVectorMath');mul.operation='SCALE';mul.inputs['Scale'].default_value=scale;ln.new(rotate.outputs[0],mul.inputs[0])
    frac=nd.new('ShaderNodeVectorMath');frac.operation='FRACTION';ln.new(mul.outputs[0],frac.inputs[0])
    window=nd.new('ShaderNodeVectorMath');window.operation='SCALE';window.inputs['Scale'].default_value=.20;ln.new(frac.outputs[0],window.inputs[0])
    shift=nd.new('ShaderNodeVectorMath');shift.operation='ADD';shift.inputs[1].default_value=offset;ln.new(window.outputs[0],shift.inputs[0])
    tex=nd.new('ShaderNodeTexImage');tex.image=im;tex.extension='EXTEND';ln.new(shift.outputs[0],tex.inputs['Vector']);samples.append(tex.outputs['Color'])
mix=nd.new('ShaderNodeMixRGB');mix.inputs[0].default_value=.5;ln.new(samples[0],mix.inputs[1]);ln.new(samples[1],mix.inputs[2])
tone=nd.new('ShaderNodeMixRGB');tone.blend_type='MULTIPLY';tone.inputs[0].default_value=1;tone.inputs[2].default_value=(.48,.51,.45,1);ln.new(mix.outputs[0],tone.inputs[1]);ln.new(tone.outputs[0],nd['Principled BSDF'].inputs['Base Color'])
bump=nd.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.24;bump.inputs['Distance'].default_value=.008;ln.new(mix.outputs[0],bump.inputs['Height']);ln.new(bump.outputs[0],nd['Principled BSDF'].inputs['Normal'])
c.mesh('Athletics continuous natural grass infield',[(*p,0) for p in capsule(inner-.12)],[tuple(range(len(capsule(inner-.12))))],turf)
rng=random.Random(357);v,f,mi=[],[],[]
mats=[c.material('Athletics cut grass blade '+str(i),col,.93) for i,col in enumerate([(.24,.23,.084),(.34,.31,.11),(.16,.20,.052),(.45,.38,.18)])]
for i in range(650000):
    x=rng.uniform(cx-inner+.3,cx+inner-.3);y=rng.uniform(cy-half-inner+.3,cy+half+inner-.3)
    yy=max(0,abs(y-cy)-half)
    if (x-cx)**2+yy**2>(inner-.22)**2:continue
    ht=rng.uniform(.018,.052);a=rng.random()*math.tau;st=len(v)
    v.extend([(x-.007,y,0),(x+.007,y,0),(x+math.cos(a)*ht*.30,y+math.sin(a)*ht*.3,ht)])
    f.append((st,st+1,st+2));mi.append(rng.randrange(4))
c.mesh('Athletics short natural grass blades',v,f,mats,mi)
# Approximate start/stagger markings, no claim of surveyed track certification.
for lane in range(8):
    rr=inner+(lane+.5)*1.22;y=cy-half+5+lane*.50
    q.flat_line('Athletics lane start bar',[(cx+rr-.58,y),(cx+rr+.58,y)],.05,white,.05)
    obj=c.text('Athletics lane numeral',str(lane+1),(cx+rr,y+1.1,.055),.70,white,(0,0,-math.pi/2))
for y in [cy-half+11,cy+half-11]:q.flat_line('Athletics common finish strip',[(cx+inner,y),(cx+inner+9.76,y)],.06,white,.05)
for name,pts in [('gate one',[(-36,218),(-54,218),(-65,230)]),('gate three',[(-36,318),(-49,318)]),('west stand',[(-131.4,280),(-136,280)])]:
    # Keep connectors under track/turf where they overlap, without hiding painted lanes.
    s.ribbon('Athletics '+name+' continuous support',pts,4.4,p['stone'],-.035,.22)
c.collection('271_Athletics_Blue_White_Grandstand')
blue=c.material('Grandstand bright blue moulded seats',(.008,.29,.58),.38)
blue2=c.material('Grandstand pale cyan seats',(.035,.47,.64),.40)
ivory=c.material('Grandstand weathered ivory concrete',(.64,.68,.65),.81)
metal=c.material('Grandstand pale grey steel',(.42,.49,.48),.34,.67)
roof=c.material('Grandstand pale blue standing seam roof',(.38,.56,.57),.44,.4)
def seat(x,y,z,col):
    c.box('Grandstand seat pan',(x,y,z+.28),(.41,.46,.075),col,.028)
    back=c.box('Grandstand curved seat back',(x-.18,y,z+.48),(.065,.45,.39),col,.028);back.rotation_euler.y=-.10
    c.box('Grandstand seat metal fixing',(x,y,z+.12),(.18,.15,.23),metal)
for centre in [248,310]:
    y0,y1=centre-20,centre+20
    c.box('Grandstand paved toe landing',(-134.2,centre,-.085),(2.6,40,.20),n.paving('Grandstand grey access paving',(.39,.41,.36),(.6,.4),.006))
    for row in range(11):
        xx=-135.3-row*.78;z=(row+1)*.34
        for a,b in [(y0,centre-1.05),(centre+1.05,y1)]:
            c.box('Grandstand concrete stepped terrace',(xx,(a+b)/2,z/2),(.80,b-a,z),ivory)
            for k in range(int((b-a)/.57)):
                yy=a+.32+k*.57;col=blue2 if (row+k)%7==0 else p['white'] if (row//2+k//5)%9==0 else blue
                seat(xx,yy,z,col)
    u.stairs('Grandstand public aisle',(-134.91,centre,0),(-143.49,centre,3.74),1.94,22,ivory,False)
    c.box('Grandstand rear circulation deck',(-145,centre,3.58),(3.0,40,.32),ivory)
    for y in [y0,y0+10,y1-10,y1]:
        s.beam('Grandstand rear column',(-146,y,0),(-146,y,8.45),.20,.20,metal)
        s.beam('Grandstand cantilever rafter',(-147,y,8.30),(-132.5,y,7.66),.18,.22,metal)
        s.beam('Grandstand diagonal roof brace',(-146,y,5.7),(-136,y,7.81),.12,.12,metal)
        s.beam('Grandstand front support',(-134.5,y,0),(-134.5,y,7.74),.14,.14,metal)
    roofobj=c.box('Grandstand sloping roof sheet',(-139.8,centre,8.1),(15.6,42,.11),roof);roofobj.rotation_euler.y=.044
    for yy in [y0-1+i*.33 for i in range(128)]:s.beam('Grandstand standing seam rib',(-147.6,yy,8.49),(-132,yy,7.80),.025,.03,metal)
    for z in [3.96,4.6]:c.rod('Grandstand back safety rail',(-146.5,y0,z),(-146.5,y1,z),.035,p['steel'])
    for yy in range(int(y0),int(y1)+1,2):c.rod('Grandstand back rail upright',(-146.5,yy,3.6),(-146.5,yy,4.7),.029,p['steel'])
    for a,b in [(y0,centre-1.05),(centre+1.05,y1)]:c.box('Grandstand blue front fascia',(-134.80,(a+b)/2,.50),(.10,b-a,.55),blue)
c.collection('272_Athletics_Officials_Pavilion')
c.box('Grandstand officials pavilion floor',(-142,279,1.5),(9,19,.25),ivory)
c.box('Grandstand officials blue base',(-142,279,.67),(9,19,1.34),blue)
for x in [-146.4,-137.6]:
    c.box('Grandstand officials glazing',(x,279,3.3),(.035,18.2,2.6),p['glass'])
    for yy in range(270,289,2):c.box('Grandstand officials glazing mullion',(x,yy,3.3),(.12,.06,2.7),p['white'])
    for z in [2,2.8,4.62]:c.box('Grandstand officials glazing transom',(x,279,z),(.12,18.5,.065),p['white'])
for y in [269.5,288.5]:c.box('Grandstand officials end wall',(-142,y,3.1),(9,.23,3.0),ivory)
c.box('Grandstand officials flat roof',(-142,279,4.88),(9.7,20,.24),ivory)
c.box('Grandstand officials burgundy fascia',(-137.2,279,5.32),(.20,20,.55),c.material('Grandstand burgundy sign band',(.17,.04,.055),.61))
for yy in [270,279,288]:
    s.beam('Grandstand central canopy upright',(-146,yy,4.9),(-146,yy,9.8),.2,.2,metal)
    s.beam('Grandstand central canopy rafter',(-147,yy,9.65),(-133,yy,9.05),.16,.22,metal)
    s.beam('Grandstand central canopy diagonal',(-146,yy,6.5),(-135,yy,9.14),.12,.12,metal)
o=c.box('Grandstand raised centre roof',(-140,279,9.5),(15,21,.13),roof);o.rotation_euler.y=.044
c.collection('273_Athletics_Perimeter_And_Equipment')
for yy in [203,217,342,356]:s.tree(-151,yy,.9,yy*.02)
for xx in [-137,-130,-123]:
    c.rod('Athletics southern flag mast',(xx,205,0),(xx,205,10.5),.055,p['steel'],sides=12)
    l.ellipsoid('Athletics flagpole finial',(xx,205,10.55),(.095,.095,.095),p['steel'])
for yy in [208,352]:
    c.rod('Athletics floodlight mast',(-137,yy,0),(-137,yy,14),.12,p['steel'],.075,12)
    for k in range(4):c.box('Athletics floodlight rectangular head',(-136.7,yy-.9+k*.6,14),(.35,.50,.35),p['white'],.03)
# Source contains portable blue landing pads beside the running field.
pad=c.material('Athletics blue high jump landing mat',(.025,.16,.42),.73)
c.box('Athletics landing mat',(-97,336,.38),(5.5,3.6,.76),pad,.12)
for xx in [-100,-94]:c.rod('Athletics high jump upright',(xx,334,0),(xx,334,2.1),.025,p['steel'])
c.rod('Athletics high jump crossbar',(-100,334,1.55),(-94,334,1.55),.014,white)
c.collection('278_Athletics_Review_Cameras')
c.camera('125_Track_from_field',(-85,270,1.7),(-140,280,4.1),25)
c.camera('126_Track_east_lanes',(-38,248,1.7),(-67,320,1.8),27)
c.camera('127_Track_grandstand',(-128,244,1.7),(-141,252,3.5),25)
c.camera('128_Track_overview',(-207,173,133),(-88,278,0),34)
h.save(31,'Eight-lane oval and dry natural grass with photographed blue-white grandstand, central officials room, canopies and lighting. Standard proportions constrain estimated footprint; actual survey and certification pending. Replaces only labelled Nantian sports verge context.',[357,378,379,347,348],'125_Track_from_field')
