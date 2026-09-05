"""Efficient editable campus geometry. Metres are image-based estimates.

Meshes are built directly: no operator/dependency-graph update per repeated part.
Random generators are local and seeded so deliveries can be rebuilt reproducibly.
"""
from pathlib import Path
import bpy, math, random, json
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
SCENE = None
COL = None
def activate(scene):
    global SCENE
    SCENE = scene
    bpy.context.window.scene = scene
def collection(name):
    global COL
    COL = bpy.data.collections.get(name)
    if COL is None:
        COL = bpy.data.collections.new(name)
        SCENE.collection.children.link(COL)
    return COL
def material(name, color, rough=.7, metal=0):
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name); m.use_nodes=True
    m.diffuse_color=(*color,1)
    p=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
    p.name='Principled BSDF'
    p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Roughness'].default_value=rough
    p.inputs['Metallic'].default_value=metal
    return m
def noise(m, scale=80, amount=.15, distance=.018):
    n,l=m.node_tree.nodes,m.node_tree.links
    p=next(n for n in n if n.type=='BSDF_PRINCIPLED')
    t=n.new('ShaderNodeTexNoise');t.inputs['Scale'].default_value=scale
    t.inputs['Detail'].default_value=3
    b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=amount
    b.inputs['Distance'].default_value=distance
    l.new(t.outputs['Fac'],b.inputs['Height']);l.new(b.outputs['Normal'],p.inputs['Normal'])
def mesh(name, verts, faces, mat=None, indices=None):
    d=bpy.data.meshes.new(name);d.from_pydata(verts,[],faces);d.update()
    o=bpy.data.objects.new(name,d);COL.objects.link(o)
    if mat:
        for m in mat if isinstance(mat,list) else [mat]: d.materials.append(m)
    if indices:
        for p,i in zip(d.polygons,indices):p.material_index=i
    o['component_scope']=COL.name
    return o
def box(name, loc, size, mat, bevel=0):
    x,y,z=[a/2 for a in size]
    v=[(-x,-y,-z),(x,-y,-z),(x,y,-z),(-x,y,-z),(-x,-y,z),(x,-y,z),(x,y,z),(-x,y,z)]
    o=mesh(name,v,[(3,2,1,0),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],mat)
    o.location=loc
    if bevel:
        m=o.modifiers.new('Edge radius','BEVEL');m.width=bevel;m.segments=2
    return o
def tube_data(v,f,a,b,r1,r2=None,sides=8):
    a,b=Vector(a),Vector(b);z=(b-a).normalized()
    x=z.cross(Vector((0,1,0)))
    if x.length<.01:x=z.cross(Vector((1,0,0)))
    x.normalize();y=z.cross(x);r2=r1 if r2 is None else r2;st=len(v)
    for c,r in [(a,r1),(b,r2)]:
        for i in range(sides):
            t=i*math.tau/sides;v.append(c+r*(x*math.cos(t)+y*math.sin(t)))
    f.append(tuple(st+i for i in reversed(range(sides))))
    f.append(tuple(st+sides+i for i in range(sides)))
    for i in range(sides):j=(i+1)%sides;f.append((st+i,st+j,st+sides+j,st+sides+i))
def rod(name,a,b,r,mat,r2=None,sides=10):
    v,f=[],[];tube_data(v,f,a,b,r,r2,sides)
    return mesh(name,v,f,mat)
def text(name, body, loc, size, mat, rotation=(math.pi/2,0,0)):
    d=bpy.data.curves.new(name,'FONT');d.body=body;d.size=size;d.align_x='CENTER';d.extrude=.002
    font=bpy.data.fonts.get('Microsoft YaHei')
    if not font:
        font=bpy.data.fonts.load('C:/Windows/Fonts/msyh.ttc');font.name='Microsoft YaHei'
    d.font=font
    o=bpy.data.objects.new(name,d);COL.objects.link(o);o.location=loc;o.rotation_euler=rotation;d.materials.append(mat)
    # Convert only text object to mesh via evaluated data; no external font dependency.
    bpy.context.view_layer.update()
    deps=bpy.context.evaluated_depsgraph_get()
    md=bpy.data.meshes.new_from_object(o.evaluated_get(deps))
    no=bpy.data.objects.new(name+' lettering',md);COL.objects.link(no);no.matrix_world=o.matrix_world.copy()
    bpy.data.objects.remove(o,do_unlink=True)
    return no
def camera(name,loc,target,lens=32):
    d=bpy.data.cameras.new(name);d.lens=lens;d.clip_end=1500;d.clip_start=.08
    o=bpy.data.objects.new(name,d);COL.objects.link(o);o.location=loc
    o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
    return o
def leaf_data(v,f,ids,p,length,rng,index):
    p=Vector(p);a=rng.uniform(0,math.tau)
    u=Vector((math.cos(a),math.sin(a),rng.uniform(-.65,.65))).normalized()*length
    w=Vector((-math.sin(a),math.cos(a),rng.uniform(-.3,.3)))*length*.36
    st=len(v);v.extend([p-u*.45,p+w,p+Vector((0,0,length*.12)),p+u*.55,p-w])
    f.extend([(st,st+1,st+2),(st+1,st+3,st+2),(st+3,st+4,st+2),(st+4,st,st+2)])
    ids.extend([index]*4)
def foliage_materials(prefix='Campus foliage',dark=False):
    colors=[(.10,.21,.022),(.17,.29,.038),(.23,.34,.055),(.068,.16,.021),(.29,.37,.066)]
    if dark:colors=[tuple(c*.65 for c in a) for a in colors]
    mats=[material(prefix+str(i),c,.64) for i,c in enumerate(colors)]
    for m in mats:
        p=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
        p.inputs['Subsurface Weight'].default_value=.06
    return mats
def tree(name,x,y,height=8,crown=2.0,seed=1,mature=False):
    rng=random.Random(seed);v,f=[],[];lv,lf,mi=[],[],[]
    bark=material('Campus mottled grey bark',(.26,.25,.20),.93)
    if len(bark.node_tree.nodes)<4:noise(bark,22,.7,.04)
    n=28 if mature else 21
    trunk_h=height*.78
    tube_data(v,f,(x,y,0),(x+.12,y+.06,trunk_h),.28 if mature else .115,.035,12)
    for j in range(n):
        az=j*2.399+rng.uniform(-.4,.4);level=j/(n-1)
        z=height*(.34+.5*level)
        reach=crown*(.6+.4*rng.random())*(1-.65*level)
        start=Vector((x+.1,y,z));tip=Vector((x+math.cos(az)*reach,y+math.sin(az)*reach,z+height*.10))
        tube_data(v,f,start,tip,.075*(1-level)+.018 if mature else .035*(1-level)+.009,.007,8)
        for k in range(8):
            a=az+(k%4-1.5)*.5
            base=start.lerp(tip,.32+.085*k)
            end=base+Vector((math.cos(a)*crown*.46,math.sin(a)*crown*.46,height*(.08+.06*rng.random())))
            tube_data(v,f,base,end,.008,.0015,5)
            for t in range(50 if mature else 32):
                q=rng.random();p=base.lerp(end,q)
                p+=Vector((rng.gauss(0,crown*.12),rng.gauss(0,crown*.12),rng.gauss(0,.19)))
                leaf_data(lv,lf,mi,p,rng.uniform(.085,.155) if not mature else rng.uniform(.10,.18),rng,rng.randrange(5))
    branches=mesh(name+' branches',v,f,bark)
    for p in branches.data.polygons:p.use_smooth=True
    mesh(name+' individual leaves',lv,lf,foliage_materials(dark=mature),mi)
    if not mature:
        rod(name+' white trunk paint',(x,y,.05),(x+.03,y+.01,1.25),.117,material('Tree limewash',(.7,.72,.66)),.10,12)
        bamboo=material('Yellow bamboo tree supports',(.48,.28,.06),.81)
        for i in range(3):
            a=i*math.tau/3
            rod(name+' bamboo brace',(x+1.18*math.cos(a),y+1.18*math.sin(a),.1),(x+.12*math.cos(a),y+.12*math.sin(a),2.35),.032,bamboo)
        for z in [1.85,2.24]:
            for i in range(3):
                a=i*math.tau/3;b=(i+1)*math.tau/3
                rod(name+' ties',(x+.18*math.cos(a),y+.18*math.sin(a),z),(x+.18*math.cos(b),y+.18*math.sin(b),z),.022,bamboo)
def planting(name,center,size,height=.32,seed=1,density=500):
    rng=random.Random(seed);v,f,mi=[],[],[];x,y=center;w,d=size
    for i in range(int(w*d*density)):
        p=(x+rng.uniform(-w/2,w/2),y+rng.uniform(-d/2,d/2),rng.uniform(.09,height))
        leaf_data(v,f,mi,p,rng.uniform(.045,.085),rng,rng.randrange(5))
    return mesh(name,v,f,foliage_materials('Groundcover '),mi)
def grass(name,center,size,seed=1):
    rng=random.Random(seed);v,f=[],[];x,y=center;w,d=size
    for i in range(int(w*d*100)):
        px=x+rng.uniform(-w/2,w/2);py=y+rng.uniform(-d/2,d/2);h=rng.uniform(.04,.16);a=rng.random()*math.tau
        st=len(v);v.extend([(px-.008,py,.02),(px+.008,py,.02),(px+math.cos(a)*.04,py+math.sin(a)*.04,h)])
        f.append((st,st+1,st+2))
    return mesh(name,v,f,material('Natural lawn blades',(.085,.16,.032)))
def render_setup(scene):
    scene.render.engine='CYCLES';scene.cycles.samples=48;scene.cycles.use_denoising=True
    scene.render.resolution_x=1600;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG'
    scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast'
def save(path, version, refs):
    SCENE['delivery_version']=version;SCENE['reference_scene_ids']=','.join(map(str,refs))
    SCENE['scale_status']='Image-based estimated metres; no survey calibration'
    SCENE['user_acceptance']='Pending user review'
    SCENE.unit_settings.system='METRIC';SCENE.unit_settings.scale_length=1
    render_setup(SCENE)
    for s in bpy.data.screens:
        for a in s.areas:
            if a.type=='VIEW_3D':
                a.spaces.active.region_3d.view_perspective='CAMERA'
                a.spaces.active.shading.type='MATERIAL'
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(path),compress=True)
