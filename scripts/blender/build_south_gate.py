"""Build the first WZMS south gate reference sample in Blender 5.1.

Run through Blender MCP using exec(compile(...)). Units are provisional metres.
Only this script's WZMS_SouthGate_Sample scene is rebuilt. Reference photographs
are packed unchanged; wall surface UVs use the photographed inscription/relief.
"""
from pathlib import Path
import bpy
import math
import random
import json
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'models/south_gate'
REPORT = ROOT / 'deliverables/v0.0.2'
OUT.mkdir(parents=True, exist_ok=True)
REPORT.mkdir(parents=True, exist_ok=True)
random.seed(720349)
SCENE_NAME = 'WZMS_SouthGate_Sample'
old = bpy.data.scenes.get(SCENE_NAME)
if old:
    for obj in list(old.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    bpy.data.scenes.remove(old)
scene = bpy.data.scenes.new(SCENE_NAME)
bpy.context.window.scene = scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0
scene['reference_scene_id'] = '119232349'
scene['scale_status'] = 'Estimated from imagery; not surveyed'
scene['scope'] = 'South gate entrance sample; not full campus'
collections = {}
for name in ['01_Ground', '02_NameWall', '03_Gates', '04_Guardhouses',
             '05_Landscape', '06_Background', '07_Lighting', '08_Cameras']:
    c = bpy.data.collections.new(name)
    scene.collection.children.link(c)
    collections[name] = c
COL = collections['01_Ground']

def move(obj, name, mat=None):
    obj.name = name
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    COL.objects.link(obj)
    if mat:
        obj.data.materials.append(mat)
    return obj

def material(name, color, rough=.65, metal=0):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    p = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    p.name = 'Principled BSDF'
    p.inputs['Base Color'].default_value = (*color, 1)
    p.inputs['Roughness'].default_value = rough
    p.inputs['Metallic'].default_value = metal
    return m

def noise_surface(m, scale=45, strength=.14, distance=.035):
    n, l = m.node_tree.nodes, m.node_tree.links
    tex = n.new('ShaderNodeTexNoise')
    tex.inputs['Scale'].default_value = scale
    tex.inputs['Detail'].default_value = 3
    bump = n.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = strength
    bump.inputs['Distance'].default_value = distance
    l.new(tex.outputs['Fac'], bump.inputs['Height'])
    l.new(bump.outputs['Normal'], n.get('Principled BSDF').inputs['Normal'])

stone = material('Warm pale granite', (.66,.64,.58), .83)
noise_surface(stone, 60, .18, .025)
edge = material('Granite curb', (.34,.37,.37), .8)
noise_surface(edge)
dark = material('Graphite painted metal', (.032,.044,.052), .34, .65)
steel = material('Brushed stainless steel', (.46,.5,.51), .29, .85)
white = material('White painted metal', (.8,.8,.72), .43, .15)
blue = material('Gate control blue', (.015,.08,.28), .36)
red = material('Flowers coral red', (.52,.018,.028), .61)
yellow = material('Flowers golden yellow', (.92,.39,.025), .57)
soil = material('Planting soil', (.06,.044,.025), 1)
terracotta = material('Porcelain white pots', (.76,.76,.68), .28)
potblue = material('Porcelain blue bands', (.035,.1,.27), .32)
bark = material('Tree bark', (.13,.09,.05), .92)
noise_surface(bark, 14, .65, .12)
leaves = [material('Leaf green '+str(i), c, .71) for i,c in enumerate([
    (.08,.19,.025), (.14,.28,.038), (.22,.34,.055), (.05,.13,.022), (.31,.38,.08)])]
for m in leaves:
    m.node_tree.nodes.get('Principled BSDF').inputs['Subsurface Weight'].default_value = .07
glass = material('Muted teal glazing', (.10,.26,.25), .2, .38)
glass.node_tree.nodes.get('Principled BSDF').inputs['Coat Weight'].default_value = .35

def cube(name, loc, dims, mat, bevel=0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o=move(bpy.context.object,name,mat)
    o.dimensions=dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        mod=o.modifiers.new('Soft real edges','BEVEL')
        mod.width=bevel; mod.segments=2
    return o

def cyl(name, loc, radius, depth, mat, vertices=16, rtop=None):
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=radius,
        radius2=radius if rtop is None else rtop, depth=depth, location=loc)
    o=move(bpy.context.object,name,mat)
    for p in o.data.polygons:p.use_smooth=True
    return o

def rod(name,a,b,r,mat,r2=None):
    a,b=Vector(a),Vector(b)
    o=cyl(name,(a+b)/2,r,(b-a).length,mat,10,r2)
    o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler()
    return o

def mesh(name,verts,faces,mat):
    d=bpy.data.meshes.new(name)
    d.from_pydata(verts,[],faces); d.update()
    o=bpy.data.objects.new(name,d); COL.objects.link(o)
    if mat:d.materials.append(mat)
    return o

def curve_line(name,coords,r,mat):
    d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D'
    d.bevel_depth=r;d.bevel_resolution=2
    s=d.splines.new('POLY');s.points.add(len(coords)-1)
    for p,co in zip(s.points,coords):p.co=(*co,1)
    o=bpy.data.objects.new(name,d);COL.objects.link(o);d.materials.append(mat)
    return o

# Ground is real geometry; its joints and mineral variation are procedural.
paving = material('Granite rectangular paving', (.42,.44,.41), .86)
n,l=paving.node_tree.nodes,paving.node_tree.links
geo=n.new('ShaderNodeTexCoord'); mapping=n.new('ShaderNodeVectorMath');mapping.operation='SCALE'
mapping.inputs[3].default_value=1
l.new(geo.outputs['Object'],mapping.inputs[0])
brick=n.new('ShaderNodeTexBrick')
brick.inputs['Color1'].default_value=(.46,.46,.41,1)
brick.inputs['Color2'].default_value=(.31,.34,.32,1)
brick.inputs['Mortar'].default_value=(.13,.15,.14,1)
brick.inputs['Scale'].default_value=1
brick.inputs['Mortar Size'].default_value=.008
brick.inputs['Mortar Smooth'].default_value=.003
brick.inputs['Brick Width'].default_value=.85
brick.inputs['Row Height'].default_value=.34
l.new(mapping.outputs['Vector'],brick.inputs['Vector'])
l.new(brick.outputs['Color'],n.get('Principled BSDF').inputs['Base Color'])
bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.3
bump.inputs['Distance'].default_value=.022
l.new(brick.outputs['Fac'],bump.inputs['Height'])
l.new(bump.outputs['Normal'],n.get('Principled BSDF').inputs['Normal'])
cube('Entrance plaza',(0,1,-.16),(70,66,.3),paving,.04)
cube('Outer dark paving band',(0,-12,.005),(64,.42,.035),edge,.008)
for x in [-23,23]:
    cube('Drive edge band',(x,0,.004),(.38,48,.025),edge)
for i in range(70):
    y=-25+i*.54
    cube('Tactile tile',(15.8,y,.015),(.58,.52,.04),stone,.008)
    for j in range(4):cube('Tactile raised rib',(15.59+j*.14,y,.046),(.04,.42,.022),stone,.012)
cover=cyl('Inspection cover',(2.7,-9,.015),.52,.035,dark,64)
for r in [.38,.43,.49]:
    curve_line('Manhole concentric ring',[(2.7+r*math.cos(t*math.tau/80),-9+r*math.sin(t*math.tau/80),.036) for t in range(81)],.009,steel)
for i in range(-5,6):
    x=i*.066
    extent=math.sqrt(max(0,.34**2-x*x))
    cube('Manhole slot',(2.7+x,-9,.039),(.025,2*extent,.01),edge)

# Curved, solid inscription wall. Its photographed calligraphy and relief
# are preserved as a UV-mapped surface, not represented as exact sculpted forms.
COL=collections['02_NameWall']
photo=bpy.data.images.load(str(ROOT/'reference/panoramas/faces/119232349/f.jpg'),check_existing=True)
photo.pack()
wallmat=material('Original wall inscription and relief · photo reference',(.72,.7,.65),.8)
n,l=wallmat.node_tree.nodes,wallmat.node_tree.links
t=n.new('ShaderNodeTexImage');t.image=photo;t.interpolation='Linear'
n.active=t
l.new(t.outputs['Color'],n.get('Principled BSDF').inputs['Base Color'])
noise_surface(wallmat,90,.12,.015)
W,H=18.0,4.85
def wall_y(x):return .38*(x/9)**2
verts=[];faces=[];uvs=[]
segments=72
for i in range(segments+1):
    x=-9+18*i/segments
    verts.extend([(x,wall_y(x),.22),(x,wall_y(x),H+.22)])
for i in range(segments):faces.append((2*i,2*i+2,2*i+3,2*i+1))
wall=mesh('South gate · curved name wall',verts,faces,wallmat)
uv=wall.data.uv_layers.new(name='Reference projection')
for poly in wall.data.polygons:
    for li in poly.loop_indices:
        co=wall.data.vertices[wall.data.loops[li].vertex_index].co
        sx=(co.x+9)/18;sz=(co.z-.22)/H
        # Crop coordinates measured on the original 1600px preview of a 4352px face.
        bow=1-(2*sx-1)**2
        top=.4025+.0105*bow
        bottom=.5695+.008*bow
        uv.data[li].uv=(.1915+sx*.619,1-(bottom-sz*(bottom-top)))
sol=wall.modifiers.new('Stone wall thickness','SOLIDIFY');sol.thickness=.62;sol.offset=-1
wall.data.materials.append(stone);sol.material_offset=1;sol.material_offset_rim=1
bev=wall.modifiers.new('Dressed stone edge','BEVEL');bev.width=.022;bev.segments=2
wall['surface_detail']='Photographic inscription and relief; not sculpted depth'
wall['provisional_width_m']=W;wall['provisional_height_m']=H
cube('Continuous low flower plinth',(0,-.32,.10),(18.3,1.08,.2),stone,.12)
for i in range(72):
    x=-9+(i+.5)*.25
    cube('Wall coping',(x,wall_y(x)+.28,H+.235),(.251,.72,.085),stone,.016)

# Leaf geometry used for both planter foliage and tree crowns.
def leaf_cloud(name, clusters, length=.14, count=150):
    vs=[];fs=[];mi=[]
    for center,spread in clusters:
        for _ in range(count):
            p=Vector(center)+Vector((random.gauss(0,spread[0]),random.gauss(0,spread[1]),random.gauss(0,spread[2])))
            a=random.random()*math.tau
            u=Vector((math.cos(a),math.sin(a),random.uniform(-.6,.6))).normalized()*length*random.uniform(.65,1.3)
            v=Vector((-math.sin(a),math.cos(a),random.uniform(-.3,.3)))*length*.36
            ix=len(vs)
            vs.extend([p-u,p-v,p+Vector((0,0,length*.12)),p+v,p+u])
            fs.extend([(ix,ix+1,ix+2),(ix+1,ix+4,ix+2),(ix+4,ix+3,ix+2),(ix+3,ix,ix+2)])
            mi.extend([random.randrange(len(leaves))]*4)
    o=mesh(name,vs,fs,None)
    for m in leaves:o.data.materials.append(m)
    for p,idx in zip(o.data.polygons,mi):p.material_index=idx
    return o

def flower_cluster(name,center,radius=.13,num=15,mat=red):
    vs=[];fs=[]
    for _ in range(num):
        a=random.random()*math.tau;r=radius*math.sqrt(random.random())
        p=Vector((center[0]+r*math.cos(a),center[1]+r*math.sin(a),center[2]+random.uniform(-.03,.07)))
        for j in range(5):
            th=j*math.tau/5;ix=len(vs);sz=.035
            tip=p+Vector((math.cos(th)*sz,math.sin(th)*sz,.013))
            side=Vector((-math.sin(th)*sz*.55,math.cos(th)*sz*.55,0))
            vs.extend([p,tip+side,tip+Vector((math.cos(th)*sz*.4,math.sin(th)*sz*.4,.005)),tip-side])
            fs.append((ix,ix+1,ix+2,ix+3))
    return mesh(name,vs,fs,mat)

for i in range(65):
    x=-8.78+i*.274;y=-.63+wall_y(x)
    cyl('Blue-white flower pot',(x,y,.31),.105,.24,terracotta,16,.145)
    cyl('Porcelain cobalt rim',(x,y,.419),.145,.026,potblue,16)
    leaf_cloud('Planter leaves',[((x,y,.45),(.09,.08,.05))],.065,35)
    flower_cluster('Red flowering border',(x,y,.52),.105,12)
for x in [-7,-4.2,-1.8,1.5,4.3,7.1]:
    y=-.28+wall_y(x)
    cyl('Raised ceramic vase',(x,y,.54),.12,.65,terracotta,24,.22)
    cyl('Vase blue collar',(x,y,.78),.205,.06,potblue,24)
    leaf_cloud('Vase bouquet foliage',[((x,y,.95),(.2,.18,.15))],.1,100)
    flower_cluster('Tall orange bouquet',(x,y,1.09),.26,42,yellow)

# Retractable stainless gates with real crossing members and wheels.
COL=collections['03_Gates']
for side in [-1,1]:
    start=side*9.35;end=side*15.2
    for k in range(18):
        x=start+(end-start)*k/17
        rod('Gate upright',(x,.15,.18),(x,.15,1.52),.023,steel)
        if k<17:
            x2=start+(end-start)*(k+1)/17
            for yy in [-.03,.33]:
                rod('Gate folding diagonal',(x,yy,.30),(x2,yy,1.35),.018,dark)
                rod('Gate folding diagonal',(x,yy,1.35),(x2,yy,.30),.018,dark)
        wheel=cyl('Gate caster',(x,.13,.11),.083,.11,dark,12)
        wheel.rotation_euler[0]=math.pi/2
    cube('Gate drive pillar',(end,.13,.74),(.43,.57,1.48),dark,.055)
    cube('Gate blue control face',(end,-.162,.92),(.32,.018,.43),blue,.012)
    for z in [.84,.9,.96,1.02]:cube('Control display line',(end,-.177,z),(.22,.008,.009),white)
    cube('Gate warning lens',(end,-.166,1.34),(.18,.025,.08),red,.01)
    for k in range(5):
        x=side*(15.65+k*.44)
        rod('White entrance fence',(x,-.1,.1),(x,-.1,1.2),.026,white)
        cube('Fence amber reflector',(x,-.134,.98),(.053,.01,.095),yellow)
    rod('Fence top rail',(side*15.45,-.1,1.02),(side*17.8,-.1,1.02),.027,white)

# Guard rooms follow the two flanking pale-stone volumes; hidden elevations are inferred.
COL=collections['04_Guardhouses']
for side in [-1,1]:
    x=side*20.8
    cube('Guardhouse stone volume',(x,2.5,1.7),(6.0,4.5,3.4),stone,.055)
    cube('Guardhouse coping',(x,2.5,3.43),(6.16,4.66,.12),stone,.025)
    front=.225
    cube('Guardroom window frame',(x-side*.8,front-.03,1.8),(2.0,.12,1.32),dark,.025)
    cube('Guardroom glass',(x-side*.8,front-.11,1.8),(1.82,.025,1.15),glass)
    for off in [-.32,.32]:cube('Window mullion',(x-side*.8+off,front-.14,1.8),(.035,.035,1.17),steel)
    cube('Guardroom door',(x+side*1.6,front-.04,1.18),(.88,.08,2.32),edge,.025)
    cube('Door upper glazing',(x+side*1.6,front-.09,1.70),(.70,.028,.83),glass)
    rod('Door handle',(x+side*1.88,front-.14,.94),(x+side*1.88,front-.14,1.21),.016,steel)
    for z in [.75,1.5,2.25,3.0]:cube('Stone horizontal joint',(x,front-.012,z),(5.98,.012,.012),edge)
    for off in [-2,-1,0,1,2]:cube('Stone vertical joint',(x+off,front-.013,1.7),(.01,.014,3.36),edge)
    rod('Roof floodlight stand',(x,2.4,3.45),(x,2.4,3.82),.035,dark)
    cube('Roof floodlight',(x,2.33,3.84),(.38,.18,.29),dark,.035)
    cube('Floodlight lens',(x,2.225,3.84),(.3,.022,.2),white)
    for j in range(3):
        xx=x+(j-1)*.75
        cube('Visitor information board',(xx,-1.1,.92),(.64,.08,1.15),steel,.025)
        cube('Blue information panel',(xx,-1.151,.95),(.54,.01,1.0),blue)
        for z in [.62,.77,.92,1.07,1.22]:cube('Information line',(xx,-1.163,z),(.4,.006,.018),white)
        for dx in [-.23,.23]:rod('Board foot',(xx+dx,-1.1,.1),(xx+dx,-1.1,.4),.025,steel)

# Planting beds, branching trees and individual leaf meshes are all editable geometry.
COL=collections['05_Landscape']
def tree(name,loc,height,crown,seed):
    random.seed(seed)
    x,y=loc
    top=Vector((x+.15,y,height*.63))
    rod(name+' trunk',(x,y,0),top,.16,bark,.065)
    clusters=[]
    for j in range(10):
        a=j*2.399;z=height*(.46+.044*j)
        start=Vector((x+.1,y,z))
        reach=crown*(.65+random.random()*.4)*(1-(j/15))
        end=Vector((x+math.cos(a)*reach,y+math.sin(a)*reach,z+height*.15))
        rod(name+' scaffold',start,end,.047,bark,.009)
        for k in range(4):
            aa=a+(k-1.5)*.65
            tip=end+Vector((math.cos(aa)*crown*.37,math.sin(aa)*crown*.37,height*.12))
            rod(name+' twig',end,tip,.012,bark,.002)
            clusters.append((tip,(crown*.25,crown*.25,height*.065)))
    leaf_cloud(name+' foliage',clusters,.12 if height<8 else .16,100)

for side in [-1,1]:
    cube('Planting bed raised border',(side*13.8,7,.1),(7.5,9,.24),edge,.09)
    cube('Planting bed soil',(side*13.8,7,.19),(7.15,8.65,.12),soil,.05)
    for j in range(5):
        x=side*(10.6+j*1.55)
        leaf_cloud('Low hedge',[((x,3.0,.58),(.45,.28,.2))],.085,380)
    tree('Entrance deciduous', (side*11.2,4.8),7.6,1.85,721+side)
    tree('Outer mature tree', (side*19.5,7.2),10.4,3.4,820+side)
    tree('Garden tree',(side*8.5,12.0),9.0,2.5,931+side)
for i in range(9):
    tree('Rear tree belt',(-26+i*6.5,23+random.uniform(-2,2)),10+random.random()*3,3.3,1200+i)

# Forecourt circular planted island visible in the reverse panorama.
cyl('Round forecourt kerb',(0,-23,.14),4.6,.28,edge,96)
cyl('Round forecourt soil',(0,-23,.24),4.32,.1,soil,96)
for j in range(28):
    a=j*math.tau/28
    leaf_cloud('Island border planting',[((4*math.cos(a),-23+4*math.sin(a),.48),(.24,.24,.12))],.08,100)
tree('Forecourt central tree',(0,-23),10.2,2.8,1517)

# Background roof and green glazing seen above the entrance wall; secondary mass only.
COL=collections['06_Background']
cube('Background building mass',(0,36,6),(25,12,12),stone,.06)
cube('Background green glazed facade',(0,29.9,7.4),(23,.16,6.7),glass)
for x in range(-11,12):cube('Glazing vertical mullion',(x,29.78,7.4),(.055,.1,6.75),steel)
for z in [4.1,5.8,7.5,9.2,10.75]:cube('Glazing floor line',(0,29.74,z),(23,.13,.065),steel)
for x in [-7.5,7.5]:cube('Roof support pier',(x,32,12.1),(2.2,5,4.3),stone,.05)
verts=[]
for y in [28.5,40]:
    for i in range(41):
        x=-14+i*.7;z=12.4+.9*(1-(x/14)**2)
        verts.extend([(x,y,z),(x,y,z+.24)])
faces=[]
for i in range(40):
    a=i*2;b=82+i*2
    faces.extend([(a,a+2,b+2,b),(a+1,b+1,b+3,a+3),(a,a+1,a+3,a+2),(b,b+2,b+3,b+1)])
mesh('Broad gently arched roof',verts,faces,stone)

COL=collections['07_Lighting']
world=bpy.data.worlds.new('Clear blue daylight');world.use_nodes=True;scene.world=world
wn=world.node_tree.nodes;wl=world.node_tree.links
next(n for n in wn if n.type=='BACKGROUND').name='Background'
sky=wn.new('ShaderNodeTexSky');sky.sky_type='SINGLE_SCATTERING'
sky.sun_elevation=math.radians(38);sky.sun_rotation=math.radians(140)
sky.sun_disc=False;sky.air_density=1.1;sky.aerosol_density=.55
wl.new(sky.outputs['Color'],wn.get('Background').inputs['Color'])
wn.get('Background').inputs['Strength'].default_value=.28
bpy.ops.object.light_add(type='SUN',location=(-12,-12,18))
sun=move(bpy.context.object,'Late morning sun')
sun.data.energy=2.5;sun.data.angle=.045
sun.rotation_euler=(math.radians(28),math.radians(-25),math.radians(-35))

COL=collections['08_Cameras']
def camera(name,loc,target,lens):
    bpy.ops.object.camera_add(location=loc)
    o=move(bpy.context.object,name);o.data.lens=lens
    o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
    o.data.clip_end=1000
    return o
front=camera('01_Front_reference',(0,-22,2.3),(0,1,3.0),31)
camera('02_Oblique_walkup',(17,-20,3.5),(0,1,2.7),34)
camera('03_Aerial_overview',(37,-43,31),(0,6,1.8),43)
camera('04_Ground_detail',(7,-7,1.72),(1,0,2.1),27)
scene.camera=front
scene.render.engine='CYCLES'
scene.cycles.samples=48
scene.cycles.use_denoising=True
scene.render.resolution_x=1600;scene.render.resolution_y=1000
scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.view_settings.view_transform='AgX'
scene.view_settings.look='AgX - Medium High Contrast'
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':
            area.spaces.active.region_3d.view_perspective='CAMERA'
            area.spaces.active.shading.type='SOLID'
            area.spaces.active.shading.color_type='TEXTURE'
            area.spaces.active.overlay.show_overlays=False
            area.spaces.active.region_3d.view_camera_zoom=10
# No startup scene is removed; it remains separate from the project sample.
polish_path=ROOT/'scripts/blender/polish_south_gate.py'
exec(compile(polish_path.read_text(encoding='utf8'),str(polish_path),'exec'),{'__file__':str(polish_path)})
summary={
    'version':'v0.0.2','scene':scene.name,'objects':len(scene.objects),
    'mesh_objects':sum(o.type=='MESH' for o in scene.objects),
    'mesh_polygons':sum(len(o.data.polygons) for o in scene.objects if o.type=='MESH'),
    'cameras':[o.name for o in scene.objects if o.type=='CAMERA'],
    'packed_images':[im.name for im in bpy.data.images if im.packed_file],
    'reference_scene_ids':['119232349','119232352'],
    'scale_calibrated':False,
    'provisional_name_wall_m':{'width':W,'height':H,'thickness':.62},
    'inferred':['wall back and thickness','guardroom hidden walls','tree crown shapes','background building depth'],
    'surface_limitations':['Inscription and lower relief use the original photograph on a solid wall, not individually sculpted relief geometry.'],
}
(REPORT/'scene_manifest.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'WZMS_SouthGate_v002.blend'))
print(json.dumps(summary,ensure_ascii=False))
