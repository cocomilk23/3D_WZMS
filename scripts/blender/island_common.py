"""Reference-led garden components; dimensions remain estimated metres."""
import bpy,math,random,json
from mathutils import Vector
import campus_common as c,north_common as n,north_landscape as l,south_detail_common as s

def retire(version,collections=(),names=()):
    objects=set()
    for name in collections:
        col=bpy.data.collections.get(name)
        if col:objects.update(col.all_objects)
    objects.update(bpy.data.objects[x] for x in names if x in bpy.data.objects)
    out=c.ROOT/'deliverables'/version;out.mkdir(parents=True,exist_ok=True)
    (out/'replacement_scope.json').write_text(json.dumps({'retired_objects':sorted(o.name for o in objects),'reason':'Replace explicitly identified estimated context with this reference-led scene.'},ensure_ascii=False,indent=2),encoding='utf8')
    for o in objects:bpy.data.objects.remove(o,do_unlink=True)

def pebble(name,color=(.30,.32,.28)):
    m=c.material(name,color,.93);nd,ln=m.node_tree.nodes,m.node_tree.links
    if len(nd)>2:return m
    co=nd.new('ShaderNodeTexCoord');v=nd.new('ShaderNodeTexVoronoi');v.inputs['Scale'].default_value=33
    ln.new(co.outputs['Object'],v.inputs['Vector'])
    ramp=nd.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.12;ramp.color_ramp.elements[0].color=(*[x*.38 for x in color],1)
    ramp.color_ramp.elements[1].position=.72;ramp.color_ramp.elements[1].color=(*[min(1,x*1.65) for x in color],1)
    ln.new(v.outputs['Distance'],ramp.inputs[0]);ln.new(ramp.outputs[0],nd.get('Principled BSDF').inputs['Base Color'])
    b=nd.new('ShaderNodeBump');b.inputs['Strength'].default_value=.38;b.inputs['Distance'].default_value=.018
    ln.new(v.outputs['Distance'],b.inputs['Height']);ln.new(b.outputs[0],nd.get('Principled BSDF').inputs['Normal']);return m

def island(name,cx,cy,rx,ry,grass,bank,hole=None):
    outline=[(cx+rx*(1+.045*math.sin(3*a))*math.cos(a),cy+ry*(1+.03*math.cos(4*a))*math.sin(a)) for a in [i*math.tau/144 for i in range(144)]]
    v=[(x,y,-.025) for x,y in outline]+[(x,y,-2.0) for x,y in outline];f=[tuple(reversed(range(144,288)))]
    for i in range(144):j=(i+1)%144;f.append((i,j,j+144,i+144))
    c.mesh(name+' retaining bank',v,f,bank)
    if hole is None:c.mesh(name+' earth surface',[(x,y,-.02) for x,y in outline],[tuple(range(144))],grass)
    else:
        # Radial quads from circular opening to the irregular shore avoid a hidden floor in the amphitheatre.
        hx,hy,hr=hole;v=[]
        for x,y in outline:
            d=Vector((x-hx,y-hy)).normalized();v.extend([(hx+hr*d.x,hy+hr*d.y,-.02),(x,y,-.02)])
        c.mesh(name+' earth outside sunken court',v,[(2*i,2*i+1,2*((i+1)%144)+1,2*((i+1)%144)) for i in range(144)],grass)
    return outline

def ring(name,x,y,ri,ro,top,bottom,mat,steps=128):
    v=[]
    for i in range(steps):
        a=i*math.tau/steps
        for r,z in [(ri,top),(ro,top),(ri,bottom),(ro,bottom)]:v.append((x+r*math.cos(a),y+r*math.sin(a),z))
    f=[]
    for i in range(steps):a=i*4;b=((i+1)%steps)*4;f.extend([(a,a+1,b+1,b),(a+2,b+2,b+3,a+3),(a,b,b+2,a+2),(a+1,a+3,b+3,b+1)])
    return c.mesh(name,v,f,mat)

def portal(name,xy,angle,mat,width=2.7,height=2.8):
    x,y=xy;u=Vector((math.cos(angle),math.sin(angle),0));normal=Vector((-u.y,u.x,0));base=Vector((x,y,0))
    outer=[(-width/2,0),(-width/2,height),(0,height+.85),(width/2,height),(width/2,0)]
    inner=[(-width/2+.20,0),(-width/2+.20,height-.11),(0,height+.61),(width/2-.20,height-.11),(width/2-.20,0)]
    v=[base+u*xx+normal*depth+Vector((0,0,zz)) for depth in [-.16,.16] for row in [outer,inner] for xx,zz in row];f=[]
    for i in range(4):
        f.extend([(i,i+1,i+6,i+5),(i+10,i+15,i+16,i+11),(i,i+10,i+11,i+1),(i+5,i+6,i+16,i+15)])
    f.extend([(0,5,15,10),(4,14,19,9)]);return c.mesh(name+' continuous mitred frame',v,f,mat)

def vertical_uv(obj):
    """Physical local metres along each facade and height for masonry courses."""
    uv=obj.data.uv_layers.new(name='Facade metres')
    for face in obj.data.polygons:
        normal=face.normal;u=Vector((-normal.y,normal.x,0))
        if u.length<.01:u=Vector((1,0,0))
        else:u.normalize()
        for j in face.loop_indices:
            q=obj.data.vertices[obj.data.loops[j].vertex_index].co
            uv.data[j].uv=(q.dot(u),q.z if abs(normal.z)<.7 else q.y)

def use_facade_uv(mat):
    co=next(x for x in mat.node_tree.nodes if x.type=='TEX_COORD');brick=next(x for x in mat.node_tree.nodes if x.type=='TEX_BRICK')
    mat.node_tree.links.new(co.outputs['UV'],brick.inputs['Vector'])

def mosaic_path(name,a,b,width=2.65):
    a,b=Vector(a),Vector(b);d=(b-a).normalized();normal=Vector((-d.y,d.x));length=(b-a).length
    dark=pebble('Island black river pebble mosaic',(.23,.24,.215));light=pebble('Island pale river pebble mosaic',(.51,.50,.43));stone=n.palette()['stone']
    s.ribbon(name+' pebble field',[a,b],width,dark,0,.18)
    for sign in [-1,1]:s.segment(name+' border',a+normal*sign*(width/2-.07),b+normal*sign*(width/2-.07),.11,light,.009,.012)
    for j in range(int(length/1.05)):
        q=a+d*(j*1.05+.525)
        for sign in [-1,1]:
            centre=q+normal*sign*.63
            points=[centre+d*.48,centre+normal*.48,centre-d*.48,centre-normal*.48]
            c.mesh(name+' diamond slab',[(*p,.012) for p in points],[(0,1,2,3)],stone)
        ring(name+' round pebble medallion',q.x,q.y,.18,.26,.016,.009,light,32)

def chain_edge(name,outline,gaps=()):
    p=n.palette();v,f=[],[]
    for i in range(0,len(outline),6):
        a=Vector(outline[i]);b=Vector(outline[(i+6)%len(outline)])
        if any((a-Vector(q)).length<r or (b-Vector(q)).length<r for q,r in gaps):continue
        c.box(name+' post',(*a,.36),(.17,.17,.76),p['seam'],.014)
        for j in range(10):
            t=j/10;u=(j+1)/10;aa=a.lerp(b,t);bb=a.lerp(b,u)
            c.tube_data(v,f,(*aa,.60-.18*math.sin(math.pi*t)),(*bb,.60-.18*math.sin(math.pi*u)),.012,.012,6)
    c.mesh(name+' sagging chain',v,f,p['dark'])

def stone_table(name,x,y):
    stone=pebble('Island carved grey table stone',(.31,.34,.32))
    c.rod(name+' pedestal',(x,y,0),(x,y,.72),.16,stone,sides=16)
    c.rod(name+' circular table',(x,y,.72),(x,y,.80),.65,stone,sides=48)
    for a in [i*math.tau/4 for i in range(4)]:
        xx=x+1.0*math.cos(a);yy=y+1.0*math.sin(a)
        l.ellipsoid(name+' drum seat',(xx,yy,.24),(.22,.22,.27),stone)

def plant_border(name,points,radius=.65):
    for j,(x,y) in enumerate(points):l.shrub(name,x,y,.85,radius,2200+j)

def save(rev,scope,refs,camera):
    sc=c.SCENE;sc.camera=sc.objects[camera];sc['scope']=scope
    c.save(c.ROOT/f'models/campus/WZMS_Campus_v{rev:03}.blend',f'v0.0.{rev}',[119232000+i for i in refs])
    print('WZMS_BUILD_COMPLETE',rev,flush=True)
