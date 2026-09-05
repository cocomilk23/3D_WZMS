"""v0.0.6: south Zhongshan Road and actual cross-water pedestrian bridge.
Build on v0.0.5. North plaza masses are clearly separated pending next delivery.
"""
import sys,math,random
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import bpy
import bmesh
from mathutils import Vector
import campus_common as c
scene=bpy.data.scenes['WZMS_Campus'];c.activate(scene)
# Open the facade cross-route across the previous garden's north edge.
# Trim actual leaves/grass and their soil footprint; do not just cover them.
for obj in list(scene.objects):
    if obj.type=='MESH' and obj.name.startswith(('Lawn individual blades','Garden low border')):
        bm=bmesh.new();bm.from_mesh(obj.data)
        bmesh.ops.delete(bm,geom=[v for v in bm.verts if v.co.y>44.5],context='VERTS')
        bm.to_mesh(obj.data);bm.free();obj.data.update()
    elif obj.name.startswith(('Outer planted lawn soil','Lawn base','Outer garden kerb')):
        obj.scale.y=38.5/42;obj.location.y=25.25
stone=c.material('Plaza pale fine granite',(.58,.57,.51),.84)
edge=c.material('Plaza blue-grey stone bands',(.23,.27,.28),.82)
floor=c.material('South plaza warm ashlar',(.48,.46,.39),.86)
white=c.material('Facade ivory powder coat',(.73,.75,.71),.39,.16)
dark=c.material('Graphite painted metal',(.032,.044,.052),.34,.65)
soil=c.material('Planting soil',(.06,.044,.025),1)
green=c.material('Bridge pale blue-green posts',(.32,.48,.46),.60,.2)
rail=c.material('Bridge silver grey rails',(.40,.49,.49),.34,.55)
water=c.material('Campus lake water',(.11,.16,.085),.17,.1)
scene.objects['South lake water patch'].scale.x=180/110
scene.objects['South lake water patch'].location.z=-1.18
scene.objects['South lake bed'].scale.x=180/110
scene.objects['South lake bed'].location.z=-2.7
c.collection('30_Zhongshan_South_Ground')
c.box('Zhongshan east turn paved ground',(54,59.75,-.16),(10,32.5,.30),floor)
c.box('Zhongshan east bank foundation',(54,59.75,-.65),(10.4,32.9,.67),stone)
for xx in [49.15,58.85]:c.box('Roadside flush stone band',(xx,59.75,-.01),(.30,32.5,.004),edge)
# Bridgeheads meet the inherited facade forewalk, and reserve the northward extension.
c.box('South bridgehead apron',(54,74,-.16),(10,4,.30),floor)
c.box('North bridgehead apron',(54,130,-.16),(14,8,.30),floor)
c.box('North bridgehead base',(54,130,-.69),(14.5,8.5,.80),stone)
for x,y in [(51.0,61),(57,70),(48.5,47)]:
    c.box('Road service cover frame',(x,y,-.015),(.74,.74,.008),edge,.005)
    c.box('Road service cover inset',(x,y,-.008),(.68,.68,.008),stone,.005)
    for dx in [-.21,.21]:c.box('Road cover lifting slot',(x+dx,y,-.003),(.065,.02,.002),dark)
c.collection('31_Zhongshan_Bridge_Structure')
Y0,Y1=76,126;X=54;W=6.8
def deck_z(y):return -.01+.30*math.sin(math.pi*(y-Y0)/(Y1-Y0))
v,f=[],[];segments=100
for i in range(segments+1):
    y=Y0+(Y1-Y0)*i/segments;z=deck_z(y)
    v.extend([(X-W/2,y,z),(X+W/2,y,z),(X-W/2,y,z-.42),(X+W/2,y,z-.42)])
for i in range(segments):
    a=i*4;b=a+4;f.extend([(a,a+1,b+1,b),(a+2,b+2,b+3,a+3),(a,b,b+2,a+2),(a+1,a+3,b+3,b+1)])
f.extend([(0,2,3,1),(400,401,403,402)])
# Fine square non-slip paving, aligned with bridge direction and no UV dependency.
tile=c.material('Bridge small square non-slip pavers',(.59,.58,.50),.87)
n,l=tile.node_tree.nodes,tile.node_tree.links;p=next(q for q in n if q.type=='BSDF_PRINCIPLED')
t=n.new('ShaderNodeTexCoord');b=n.new('ShaderNodeTexBrick');b.offset=0
b.inputs['Scale'].default_value=1;b.inputs['Brick Width'].default_value=.40;b.inputs['Row Height'].default_value=.40
b.inputs['Color1'].default_value=(.63,.62,.54,1);b.inputs['Color2'].default_value=(.48,.50,.45,1)
b.inputs['Mortar'].default_value=(.26,.25,.20,1);b.inputs['Mortar Size'].default_value=.003
l.new(t.outputs['Object'],b.inputs['Vector']);l.new(b.outputs['Color'],p.inputs['Base Color'])
noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=140
mix=n.new('ShaderNodeMath');mix.operation='MULTIPLY_ADD';mix.inputs[1].default_value=.20
l.new(noise.outputs['Fac'],mix.inputs[0]);l.new(b.outputs['Fac'],mix.inputs[2])
bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.28;bump.inputs['Distance'].default_value=.015
l.new(mix.outputs[0],bump.inputs['Height']);l.new(bump.outputs['Normal'],p.inputs['Normal'])
c.mesh('Continuous shallow-camber bridge deck',v,f,tile)
for y in [82,95,108,121]:
    c.box('Bridge cross girder',(54,y,deck_z(y)-.53),(7.6,.70,.40),stone,.03)
    for x in [51.4,56.6]:c.rod('Bridge pier',(x,y,-2.3),(x,y,deck_z(y)-.55),.36,stone,sides=16)
for side in [-1,1]:
    x=X+side*3.55
    for i in range(50):
        y=Y0+i+.5
        c.box('Bridge granite parapet base',(x,y,deck_z(y)+.09),(.34,.992,.22),edge,.012)
        c.box('Bridge green border paver',(X+side*3.12,y,deck_z(y)+.006),(.48,.995,.012),green)
c.collection('32_Zhongshan_Bridge_Railings')
for side in [-1,1]:
    x=X+side*3.55
    count=17;bay=(Y1-Y0)/count
    for k in range(count+1):
        y=Y0+k*bay;z=deck_z(y)
        c.box('Bridge square post shaft',(x,y,z+.70),(.24,.24,1.03),green,.018)
        c.box('Bridge post shoulder',(x,y,z+1.11),(.29,.29,.12),green,.02)
        c.box('Bridge post block cap',(x,y,z+1.28),(.34,.34,.24),green,.025)
        c.box('Bridge post foot',(x,y,z+.22),(.30,.30,.14),green,.025)
    for k in range(count):
        ya=Y0+k*bay;yb=ya+bay
        for h,r in [(1.04,.045),(.81,.022),(.22,.025)]:
            c.rod('Bridge continuous tubular rail',(x,ya,deck_z(ya)+h),(x,yb,deck_z(yb)+h),r,rail,sides=12)
        for j in range(1,16):
            y=ya+j*bay/16;z=deck_z(y)
            c.rod('Bridge vertical baluster',(x,y,z+.22),(x,y,z+.81),.014,rail,sides=8)
        # Three circular ornaments below the handrail, visible in panorama 367.
        for shift in [-.21,0,.21]:
            yc=(ya+yb)/2+shift;zc=deck_z(yc)+.926;rv,rf=[],[]
            for j in range(24):
                a=j*math.tau/24;b=(j+1)*math.tau/24
                c.tube_data(rv,rf,(x,yc+.103*math.cos(a),zc+.103*math.sin(a)),(x,yc+.103*math.cos(b),zc+.103*math.sin(b)),.008,sides=5)
            c.mesh('Bridge three-ring ornament',rv,rf,rail)
print('WZMS_BRIDGE_READY',flush=True)
c.collection('33_Zhongshan_Roadside_Landscape')
grassmat=c.material('Lawn soil green',(.11,.17,.04))
# East shoreline follows the road, retaining free space across the full lane.
c.box('Roadside east planted verge',(60.3,60,-.02),(2.6,30,.1),grassmat)
c.box('Roadside waterfront retaining edge',(61.7,60,-.42),(.30,30,.92),stone,.025)
for j,y in enumerate([49,58,67,74]):
    c.tree('Roadside mature tree',60.2,y,7.4,2.6,1500+j,True)
c.box('West south bridgehead retained shore',(44,79,-.64),(13,14,1.24),stone)
c.box('West north bridgehead retained shore',(45,132,-.64),(8,10,1.24),stone)
c.box('East north bridgehead retained shore',(63,132,-.64),(8,10,1.24),stone)
for x,y in [(47,75),(45,83),(45,129),(62,130)]:
    c.box('Bridgehead tree soil',(x,y,-.01),(4.3,4.3,.10),soil)
    c.tree('Bridgehead broadleaf',x,y,8.5,3.0,int(x*10+y),True)
    c.planting('Bridgehead groundcover',(x,y),(4.2,4.2),.35,int(y*10+x),350)
# Small lotus pond is visible beside the approach in 353/f and 366/r.
# This is local context; the full named island is a later production area.
pondx,pondy=35,36;rx,ry=11.8,8.2
rv=[(pondx,pondy,-.55)];rf=[]
for i in range(97):
    a=i*math.tau/96;rv.append((pondx+rx*math.cos(a),pondy+ry*math.sin(a),-.55))
for i in range(96):rf.append((0,i+1,i+2))
c.mesh('Approach lotus water',rv,rf,water)
c.box('Lotus pond sediment',(pondx,pondy,-1.3),(24,16.5,.15),soil)
# Land around the pond joins the plaza edge and facade road, with an actual
# opening for water. It is not an isolated oval floating in the viewport.
gv,gf=[],[]
for i in range(97):
    a=i*math.tau/96;dx=rx*math.cos(a);dy=ry*math.sin(a)
    tx=((49-pondx) if dx>0 else (22-pondx))/dx if abs(dx)>1e-8 else 1e9
    ty=((45-pondy) if dy>0 else (25-pondy))/dy if abs(dy)>1e-8 else 1e9
    fac=min(tx,ty)
    gv.extend([(pondx+dx,pondy+dy,-.01),(pondx+dx*fac,pondy+dy*fac,-.01)])
for i in range(96):gf.append((2*i,2*i+1,2*i+3,2*i+2))
c.mesh('Lotus garden continuous bank',gv,gf,grassmat)
c.box('East entrance garden ground',(35.5,15,-.17),(27,20,.30),grassmat)
for y in [12,23]:c.tree('East garden broadleaf',43,y,8.0,3.0,1810+y,True)
for i in range(96):
    a=i*math.tau/96;b=(i+1)*math.tau/96
    c.rod('Low curved pond kerb',(pondx+rx*math.cos(a),pondy+ry*math.sin(a),-.08),(pondx+rx*math.cos(b),pondy+ry*math.sin(b),-.08),.15,stone,sides=8)
rng=random.Random(7366);lotus=c.material('Lotus leaf green',(.11,.25,.044),.6)
pink=c.material('Lotus flower pale pink',(.65,.18,.27),.58)
for i in range(145):
    a=rng.uniform(0,math.tau);r=math.sqrt(rng.random())*.85
    x=pondx+rx*r*math.cos(a);y=pondy+ry*r*math.sin(a);z=rng.uniform(-.40,.22);radius=rng.uniform(.22,.48)
    c.rod('Lotus stem',(x,y,-.7),(x,y,z),.011,lotus,sides=5)
    v=[(x,y,z-.045)];f=[]
    for j in range(19):
        t=j*math.tau/18
        v.append((x+radius*math.cos(t),y+radius*math.sin(t),z+.03*math.sin(t*3)))
    for j in range(18):f.append((0,j+1,j+2))
    c.mesh('Lotus cupped leaf',v,f,lotus)
    if i%18==0:
        for j in range(8):
            a=j*math.tau/8;v=[(x,y,z+.05),(x+.08*math.cos(a-.35),y+.08*math.sin(a-.35),z+.12),(x+.18*math.cos(a),y+.18*math.sin(a),z+.22),(x+.08*math.cos(a+.35),y+.08*math.sin(a+.35),z+.12)]
            c.mesh('Lotus pink petal',v,[(0,1,2,3)],pink)
c.collection('34_Zhongshan_Signage_And_Lights')
wood=c.material('Wayfinding warm wood',(.48,.25,.075),.73)
sx,sy=31.5,49.65
c.box('Zhongshan sign base',(sx,sy,.26),(.72,.16,.52),dark,.016)
c.box('Zhongshan sign timber panel',(sx,sy,1.20),(.72,.16,1.38),wood,.014)
c.box('Zhongshan sign dark header',(sx,sy,2.19),(.72,.16,.57),dark,.014)
# Preserve the authentic printed face and map/crest from the already reviewed
# full-resolution source, instead of inventing a simplified sign layout.
photo=bpy.data.images.load(str(c.ROOT/'reference/panoramas/faces/119232366/f.jpg'),check_existing=True);photo.pack()
sm=c.material('Zhongshan original printed wayfinding face',(.48,.35,.22),.8)
sn,sl=sm.node_tree.nodes,sm.node_tree.links;sp=next(n for n in sn if n.type=='BSDF_PRINCIPLED')
tex=sn.new('ShaderNodeTexImage');tex.image=photo;sl.new(tex.outputs['Color'],sp.inputs['Base Color'])
sign=c.mesh('Authentic Zhongshan sign printed face',[(sx-.36,sy-.089,.02),(sx+.36,sy-.089,.02),(sx+.36,sy-.089,2.475),(sx-.36,sy-.089,2.475)],[(0,1,2,3)],sm)
uv=sign.data.uv_layers.new(name='Original panorama printed sign')
coords=[(.151,1-.880),(.254,1-.859),(.250,1-.394),(.1494,1-.381)]
for loop in sign.data.loops:uv.data[loop.index].uv=coords[loop.vertex_index]
sign['reference_scene']='119232366/f';sign['detail_type']='Original print projected onto modeled sign, not relief geometry'
# Road-name stone, distinct from the tall sign in the source photograph.
v=[(sx+1.0,sy-.25,0),(sx+2.0,sy-.25,0),(sx+2.1,sy-.25,.55),(sx+1.7,sy-.25,.79),(sx+1.2,sy-.25,.68),
   (sx+1.0,sy+.03,0),(sx+2.0,sy+.03,0),(sx+2.1,sy+.03,.55),(sx+1.7,sy+.03,.79),(sx+1.2,sy+.03,.68)]
c.mesh('Irregular Zhongshan name stone',v,[(0,1,2,3,4),(5,9,8,7,6),(0,5,6,1),(1,6,7,2),(2,7,8,3),(3,8,9,4),(4,9,5,0)],stone)
c.text('Road stone name','中山路',(sx+1.57,sy-.27,.44),.15,c.material('Road stone red lettering',(.32,.032,.023)))
def solar_light(x,y):
    c.rod('Solar light mast',(x,y,0),(x,y,5.8),.045,white,.025,12)
    c.rod('Solar lamp arm',(x,y,5.0),(x-.65,y,5.35),.032,white)
    c.box('Solar lamp head',(x-.68,y,5.32),(.55,.24,.10),white,.025)
    panel=c.box('Solar panel backing',(x,y,5.7),(.95,.60,.055),dark,.01);panel.rotation_euler[0]=.3
    cells=c.box('Photovoltaic blue cells',(x,y,5.735),(.88,.54,.015),c.material('Photovoltaic cells',(.018,.055,.095),.25,.4));cells.rotation_euler[0]=.3
for x,y in [(58,75),(58,125),(48,133)]:solar_light(x,y)
# Nearest bridgehead rail returns prevent an exposed abrupt end beside the lane.
for side in [-1,1]:
    x=X+side*3.55
    for y in [74.5,127.5]:
        c.rod('Bridgehead return handrail',(x,y-1.5,1.03),(x,y+1.5,1.03),.045,rail,sides=12)
        for j in range(11):
            yy=y-1.5+j*.3;c.rod('Bridgehead return baluster',(x,yy,.12),(x,yy,.99),.015,rail,sides=8)
c.collection('39_North_Context_PENDING_BUQING')
# Context only. The next named scene will replace these masses and its paving.
c.box('Buqing connection reserved paving',(54,141,-.16),(84,14,.30),floor)
for side in [-1,1]:
    x=54+side*26
    c.box('North context building mass',(x,156,10.5),(35,12,21),c.material('Facade pale limestone',(.60,.60,.55)))
    for level in range(5):
        z=2.5+level*3.85
        c.box('North context horizontal window',(x,149.9,z),(33,.10,2.4),c.material('Architectural teal glass 0',(.095,.26,.25),.16,.28))
        c.box('North context floor belt',(x,149.78,z-1.30),(35,.35,.20),white)
        for k in range(17):c.box('North context window mullion',(x-16+k*2,149.76,z),(.12,.12,2.5),white)
for x in [48,60]:c.box('North context portal pier',(x,155,11),(3,10,22),stone)
c.box('North context raised span',(54,155,18.5),(9,10,5),c.material('Architectural teal glass 0',(.095,.26,.25),.16,.28))
c.collection('38_Zhongshan_Cameras')
c.camera('14_Zhongshan_wayfinding',(35,43,1.72),(31.8,49.6,1.2),37)
c.camera('15_Zhongshan_bridge_north',(54,84,1.76),(54,135,3.7),29)
c.camera('16_Zhongshan_bridge_south',(54,116,1.76),(54,71,2.5),29)
c.camera('17_Three_scenes_overview',(145,-38,110),(12,66,6),42)
scene.camera=scene.objects['15_Zhongshan_bridge_north']
scene['scope']='South gate + plaza + Dehan/Guanzhen exteriors + south Zhongshan road/bridge. Buqing context is not delivered as a finished scene.'
scene['next_route_connection']='Bridge north apron at x54 y134 z-0.01; local axes, not surveyed north'
c.save(c.ROOT/'models/campus/WZMS_Campus_v006.blend','v0.0.6',[119232349,119232352,119232353,119232354,119232366,119232367,119232348])
print('WZMS_BUILD_COMPLETE v0.0.6',flush=True)
