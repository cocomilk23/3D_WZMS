"""Editable reference-led interior components; dimensions remain estimates."""
import bpy,math,random
from mathutils import Vector
import campus_common as c,north_common as n,south_detail_common as s,culture_common as k

def glass(name='Interior clear safety glass'):
    m=c.material(name,(.80,.86,.83),.045)
    bs=m.node_tree.nodes['Principled BSDF'];bs.inputs['Transmission Weight'].default_value=.96;bs.inputs['IOR'].default_value=1.46
    return m

def glow(name='Interior neutral LED',color=(.92,.95,1),strength=3):
    m=c.material(name,color,.4);bs=m.node_tree.nodes['Principled BSDF']
    bs.inputs['Emission Color'].default_value=(*color,1);bs.inputs['Emission Strength'].default_value=strength
    return m

def tube_light(name,x,y,z,length=1.2,energy=100):
    p=n.palette();c.box(name+' white fitting',(x,y,z),(.18,length,.08),p['white'],.015)
    for dx in [-.047,.047]:c.rod(name+' fluorescent diffuser',(x+dx,y-length*.46,z-.052),(x+dx,y+length*.46,z-.052),.020,glow(),sides=8)
    d=bpy.data.lights.new(name+' light','AREA');d.energy=energy;d.shape='RECTANGLE';d.size=.25;d.size_y=length;d.color=(.91,.95,1)
    o=bpy.data.objects.new(d.name,d);c.COL.objects.link(o);o.location=(x,y,z-.10)

def photo_panel(name,source,face,vertices,uvs=None,emission=.08):
    """UV sample intact packed source image; no modified raster or generated historical text."""
    path=c.ROOT/f'reference/panoramas/faces/119232{source}/{face}.jpg'
    im=bpy.data.images.load(str(path),check_existing=True)
    if not im.packed_file:im.pack()
    m=c.material(f'{name} source {source}/{face}',(1,1,1),.65);nd,lk=m.node_tree.nodes,m.node_tree.links
    t=next((node for node in nd if node.type=='TEX_IMAGE' and node.image==im),None)
    if t is None:t=nd.new('ShaderNodeTexImage');t.image=im;t.interpolation='Linear'
    bs=nd['Principled BSDF'];lk.new(t.outputs['Color'],bs.inputs['Base Color'])
    if emission:lk.new(t.outputs['Color'],bs.inputs['Emission Color']);bs.inputs['Emission Strength'].default_value=emission
    o=c.mesh(name,vertices,[(0,1,2,3)],m);uv=o.data.uv_layers.new(name='Original source panel corners')
    for loop,q in zip(o.data.loops,uvs or [(0,0),(1,0),(1,1),(0,1)]):uv.data[loop.index].uv=q
    o['reference_image']=path.relative_to(c.ROOT).as_posix();o['reference_surface_scope']='Photographic surface detail, not independently recreated exhibit text'
    return o

def window_y(name,x,y,z,width,height,mat=None):
    mat=mat or glass();frame=n.palette()['white']
    c.box(name+' glazing',(x,y,z),(width,.025,height),mat)
    for xx in [x-width/2,x,x+width/2]:c.box(name+' upright',(xx,y,z),(.055,.10,height+.08),frame)
    for zz in [z-height/2,z,z+height/2]:c.box(name+' transom',(x,y,zz),(width,.10,.055),frame)

def window_x(name,x,y,z,width,height,mat=None):
    mat=mat or glass();frame=n.palette()['white']
    c.box(name+' glazing',(x,y,z),(.025,width,height),mat)
    for yy in [y-width/2,y,y+width/2]:c.box(name+' upright',(x,yy,z),(.10,.055,height+.08),frame)
    for zz in [z-height/2,z,z+height/2]:c.box(name+' transom',(x,y,zz),(.10,width,.055),frame)

def pingpong(x,y,z):
    top=c.material('Gym table tennis violet blue top',(.075,.08,.22),.36)
    steel=c.material('Gym table tennis dark folding steel',(.027,.04,.03),.39,.6);white=n.palette()['white']
    c.box('Gym table tennis regulation proportion top',(x,y,z+.735),(1.525,2.74,.03),top,.008)
    for xx in [x-.748,x+.748]:c.box('Table tennis white long line',(xx,y,z+.753),(.02,2.72,.004),white)
    for yy in [y-1.36,y+1.36]:c.box('Table tennis white end line',(x,yy,z+.753),(1.52,.02,.004),white)
    c.box('Table tennis centre paint',(x,y,z+.753),(.006,2.74,.004),white)
    for xx in [x-.62,x+.62]:
        for yy in [y-.91,y+.91]:
            s.beam('Table tennis folding leg',(xx,yy,z+.07),(xx,y+(yy-y)*.75,z+.70),.032,.035,steel)
            c.rod('Table tennis rubber wheel',(xx-.035,yy,z+.063),(xx+.035,yy,z+.063),.056,steel,sides=14)
        s.beam('Table tennis side underframe',(xx,y-1.18,z+.68),(xx,y+1.18,z+.68),.035,.06,steel)
    for xx in [x-.85,x+.85]:c.rod('Table tennis net clamp',(xx,y,z+.72),(xx,y,z+.91),.015,steel,sides=8)
    c.box('Table tennis net white tape',(x,y,z+.904),(1.72,.011,.012),white)
    v,f=[],[]
    for i in range(86):
        xx=x-.85+i*.02;c.tube_data(v,f,(xx,y,z+.758),(xx,y,z+.898),.0009,.0009,4)
    for j in range(8):c.tube_data(v,f,(x-.85,y,z+.76+j*.019),(x+.85,y,z+.76+j*.019),.0009,.0009,4)
    c.mesh('Table tennis woven net',v,f,steel)

def hoop(name,cx,cy,floor,angle=0):
    """Local board plane Y=0, rim toward negative Y; 3.05m rim above finished floor."""
    before=set(c.COL.objects);steel=c.material('Interior basketball green steel',(.025,.23,.11),.36,.5)
    white=n.palette()['white'];orange=c.material('Interior orange rim',(.68,.10,.014),.35,.4)
    c.box(name+' weighted base',(0,2.5,.2),(1.2,1.7,.4),steel,.035)
    s.beam(name+' upright',(0,2.5,.3),(0,2.5,3.78),.16,.19,steel)
    s.beam(name+' arm',(0,2.5,3.7),(0,.05,3.6),.16,.12,steel)
    s.beam(name+' diagonal brace',(0,2.5,2),(0,.05,3.4),.09,.09,steel)
    c.box(name+' glass backboard',(0,0,3.425),(1.8,.035,1.05),glass())
    for x in [-.9,.9]:c.box(name+' board vertical',(x,0,3.425),(.04,.08,1.10),steel)
    for z in [2.89,3.96]:c.box(name+' board horizontal',(0,0,z),(1.84,.08,.04),steel)
    for x in [-.295,.295]:c.box(name+' target vertical',(x,-.025,3.275),(.03,.008,.45),white)
    for z in [3.05,3.50]:c.box(name+' target horizontal',(0,-.025,z),(.59,.008,.03),white)
    k.arc(name+' orange rim',0,-.375,.225,3.05,orange,width=.009,steps=64)
    c.box(name+' rim bracket',(0,-.10,3.05),(.18,.20,.08),orange)
    v,f=[],[]
    for level in range(6):
        ra=.22-level*.014;rb=ra-.014;za=3.025-level*.075
        for j in range(12):
            a=j*math.tau/12+(level%2)*math.pi/12
            for d in [-1,1]:
                b=a+d*math.pi/12;c.tube_data(v,f,(ra*math.cos(a),-.375+ra*math.sin(a),za),(rb*math.cos(b),-.375+rb*math.sin(b),za-.075),.002,.002,5)
    c.mesh(name+' hanging net',v,f,white)
    from mathutils import Matrix
    m=Matrix.Translation((cx,cy,floor))@Matrix.Rotation(angle,4,'Z')
    bpy.context.view_layer.update()
    for obj in set(c.COL.objects)-before:obj.matrix_world=m@obj.matrix_world

def trophy(x,y,z,scale=1):
    gold=c.material('Gym trophy warm gold',(.56,.31,.065),.24,.78);dark=n.palette()['dark']
    c.box('Trophy dark plinth',(x,y,z+.055*scale),(.22*scale,.17*scale,.11*scale),dark)
    c.rod('Trophy gold stem',(x,y,z+.11*scale),(x,y,z+.30*scale),.025*scale,gold,sides=10)
    c.rod('Trophy cup bowl',(x,y,z+.26*scale),(x,y,z+.48*scale),.045*scale,gold,.13*scale,20)
    for side in [-1,1]:
        c.rod('Trophy curved handle upper',(x+side*.10*scale,y,z+.45*scale),(x+side*.17*scale,y,z+.39*scale),.012*scale,gold,sides=8)
        c.rod('Trophy curved handle lower',(x+side*.17*scale,y,z+.39*scale),(x+side*.085*scale,y,z+.30*scale),.012*scale,gold,sides=8)

def glass_rail(name,points,z):
    steel=n.palette()['steel'];g=glass()
    for a,b in zip(points,points[1:]):
        aa=Vector((*a,z));bb=Vector((*b,z))
        c.rod(name+' top handrail',aa+Vector((0,0,1.1)),bb+Vector((0,0,1.1)),.025,steel,sides=10)
        c.mesh(name+' safety glass',[aa+Vector((0,0,.12)),bb+Vector((0,0,.12)),bb+Vector((0,0,1.03)),aa+Vector((0,0,1.03))],[(0,1,2,3)],g)
        for q in [aa,bb]:c.rod(name+' post',q,q+Vector((0,0,1.1)),.019,steel,sides=8)
