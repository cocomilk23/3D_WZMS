"""Replace primitive furniture and add physically modelled campus construction details."""
import bpy,math,random
from mathutils import Vector,Matrix
import campus_common as c,north_common as n,culture_common as k

def local_box(v,f,loc,size):
    x,y,z=[q/2 for q in size];a,b,d=loc;st=len(v)
    v.extend([(a+xx,b+yy,d+zz) for xx,yy,zz in [(-x,-y,-z),(x,-y,-z),(x,y,-z),(-x,y,-z),(-x,-y,z),(x,-y,z),(x,y,z),(-x,y,z)]])
    f.extend([tuple(st+i for i in face) for face in [(3,2,1,0),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]])

def replace_mesh(obj,verts,faces,changes,modifiers=True):
    md=bpy.data.meshes.new(obj.name+' v040 detailed mesh');md.from_pydata(verts,[],faces);md.update()
    for m in obj.data.materials:md.materials.append(m)
    obj.data=md
    if modifiers:obj.modifiers.clear()
    changes['modified_objects'].append(obj.name)
    return obj

def component_mesh(name,verts,faces,mat,matrix=None):
    obj=c.mesh(name,verts,faces,mat)
    if matrix is not None:obj.matrix_world=matrix
    return obj

def dish_mesh(radius=.2,depth=.04,segments=64):
    # Continuous rolled rim, concave seating surface, solid underside.
    profile=[(0,-.007),(radius*.65,-.004),(radius*.86,.004),(radius*.96,.010),(radius,.004),(radius,-depth),(radius*.9,-depth-.004),(0,-depth-.004)]
    v=[(r*math.cos(a),r*math.sin(a),z) for r,z in profile for a in [j*math.tau/segments for j in range(segments)]]
    f=[]
    for i in range(len(profile)-1):
        for j in range(segments):q=(j+1)%segments;f.append((i*segments+j,i*segments+q,(i+1)*segments+q,(i+1)*segments+j))
    return v,[tuple(reversed(face)) for face in f]

def curved_seat(width=.41,depth=.46,back=False):
    v,f=[],[];steps=12
    for layer in [0,1]:
        for j in range(steps+1):
            for i in range(steps+1):
                u=i/steps*2-1;t=j/steps
                if not back:
                    x=(t-.5)*width;y=u*depth*.5*(.94+.06*math.sin(math.pi*t));z=.022*(u*u)+.016*math.cos(math.pi*t)-layer*.037
                else:
                    x=.03*(u*u)+.025*math.sin(math.pi*t)-layer*.022;y=u*depth*.5*(1-.10*t);z=(t-.5)*.39
                v.append((x,y,z))
    sz=(steps+1)**2
    for layer in [0,1]:
        for j in range(steps):
            for i in range(steps):
                a=layer*sz+j*(steps+1)+i;face=(a,a+1,a+steps+2,a+steps+1);f.append(face if layer==0 else tuple(reversed(face)))
    rim=list(range(steps+1))+[j*(steps+1)+steps for j in range(1,steps+1)]+[steps*(steps+1)+i for i in range(steps-1,-1,-1)]+[j*(steps+1) for j in range(steps-1,0,-1)]
    for a,b in zip(rim,rim[1:]+rim[:1]):f.append((a,a+sz,b+sz,b))
    return v,f if back else [tuple(reversed(face)) for face in f]

def refine_components(scene,changes):
    stats={};p=n.palette();rng=random.Random(4009)
    protected=scene.objects['South name wall reverse photo surface']
    c.collection('370_Refined_Window_Reveals_And_Hardware')
    # Existing recess primitives filled entire openings. Turn each into a real perimeter reveal.
    count=0
    for o in list(scene.objects):
        if o.type!='MESH' or not o.name.startswith(('Window recessed opening','Window dark reveal')):continue
        if len(o.data.vertices)!=8:continue
        xs=[v.co.x for v in o.data.vertices];ys=[v.co.y for v in o.data.vertices];zs=[v.co.z for v in o.data.vertices]
        w,d,h=max(xs)-min(xs),max(ys)-min(ys),max(zs)-min(zs)
        v,f=[],[]
        for x in [-w/2+.04,w/2-.04]:local_box(v,f,(x,0,0),(.08,d,h))
        for z in [-h/2+.04,h/2-.04]:local_box(v,f,(0,0,z),(w,d,.08))
        replace_mesh(o,v,f,changes);count+=1
    stats['hollow_window_reveals']=count
    rubber=c.material('v040 window EPDM seals',(.018,.024,.025),.78)
    handle=c.material('v040 satin window handle alloy',(.47,.5,.49),.27,.80)
    cloth=c.material('v040 warm linen interior curtain',(.50,.46,.37),.88)
    reveal_centres=[o.matrix_world.translation.copy() for o in scene.objects if o.name.startswith('Window recessed opening')]
    count=0
    for o in list(scene.objects):
        if o.type!='MESH' or not o.name.startswith(('Glazed window','Window teal panel')):continue
        w,d,h=o.dimensions
        if d>.2 or h<.4:continue
        v,f=[],[]
        for y in [-d/2-.003,d/2+.003]:
            for x in [-w/2+.012,w/2-.012]:local_box(v,f,(x,y,0),(.022,.015,h))
            for z in [-h/2+.012,h/2-.012]:local_box(v,f,(0,y,z),(w,.015,.022))
        component_mesh('v040 fine window gasket',v,f,rubber,o.matrix_world.copy())
        if o.name.startswith('Glazed window'):
            v,f=[],[]
            for sign in [-1,1]:
                local_box(v,f,(w*.24,sign*.11,-.12),(.020,.032,.15))
                for z in [-.18,-.06]:local_box(v,f,(w*.24,sign*.075,z),(.033,.075,.021))
            component_mesh('v040 opening latch and standoffs',v,f,handle,o.matrix_world.copy())
            if o.matrix_world.translation.z>3 and count%3==0:
                # Inferred partly drawn curtains behind upper academic windows only.
                pos=o.matrix_world.translation;near=min(reveal_centres,key=lambda q:(q-pos).length_squared)
                side=1 if pos.y>near.y else -1
                cv,cf=[],[];span=w*.22
                for j in range(33):
                    x=-w/2+.05+j*span/32;y=-side*(.21+.035*math.sin(j*math.pi/2))
                    cv.extend([(x,y,-h/2+.06),(x,y,h/2-.06)])
                for j in range(32):cf.append((2*j,2*j+2,2*j+3,2*j+1))
                component_mesh('v040 partial pleated linen curtain',cv,cf,cloth,o.matrix_world.copy())
        count+=1
    stats['glazing_hardware_sets']=count
    c.collection('371_Refined_AC_Condensers_And_Mountings')
    dark=c.material('v040 condenser dark fins',(.045,.054,.052),.42,.6)
    for o in list(scene.objects):
        if not o.name.startswith('AC outdoor enclosure'):continue
        # Determine the exposed face from the existing fan disc, not a world-side guess.
        pos=o.matrix_world.translation;fans=[x for x in scene.objects if x.name.startswith('AC dark fan grille')]
        fan=min(fans,key=lambda x:(Vector(sum((x.matrix_world@Vector(v) for v in x.bound_box),Vector())/8)-pos).length_squared)
        centre=sum((fan.matrix_world@Vector(v) for v in fan.bound_box),Vector())/8
        sign=1 if centre.y>pos.y else -1
        v,f=[],[];cy=sign*.267
        for r in [.065,.12,.178,.199]:
            for j in range(48):
                a=j*math.tau/48;b=(j+1)*math.tau/48
                c.tube_data(v,f,(.17+r*math.cos(a),cy,r*math.sin(a)),(.17+r*math.cos(b),cy,r*math.sin(b)),.0035,.0035,5)
        for j in range(12):
            a=j*math.tau/12;c.tube_data(v,f,(.17,cy,0),(.17+.199*math.cos(a),cy,.199*math.sin(a)),.0035,.0035,5)
        for x in [-.30,.30]:
            local_box(v,f,(x,0,-.302),(.055,.51,.038));local_box(v,f,(x,-sign*.20,-.365),(.055,.055,.16))
        obj=component_mesh('v040 condenser grille and mounting feet',v,f,handle,o.matrix_world.copy())
        v,f=[],[]
        for j in range(16):local_box(v,f,(-.28+j*.018,cy-.004*sign,0),(.006,.007,.36))
        component_mesh('v040 condenser radiator fin bank',v,f,dark,o.matrix_world.copy())
    stats['detailed_condensers']=sum(o.name.startswith('AC outdoor enclosure') for o in scene.objects)
    c.collection('372_Refined_Architectural_Edges_And_Roofs')
    count=0
    for o in list(scene.objects):
        if o.type!='MESH' or o==protected or len(o.data.vertices)!=8 or o.modifiers:continue
        name=o.name.lower()
        if not any(t in name for t in ['frame','pier','column','sill','fascia','parapet','tabletop','desk','cabinet','beam','slat','door']):continue
        if any(t in name for t in ['glass','photo','seam','mark','curtain','v040']):continue
        mn=min(o.dimensions)
        if mn<.025:continue
        mod=o.modifiers.new('v040 manufactured edge radius','BEVEL');mod.width=min(.009,mn*.10);mod.segments=3
        mod.affect='EDGES';count+=1;changes['modified_objects'].append(o.name)
    stats['rounded_construction_components']=count
    # Cap existing parapets and add standing roof seam detail only on measured object bounds.
    caps=0
    for o in list(scene.objects):
        if o.type!='MESH' or 'roof parapet' not in o.name.lower() or len(o.data.vertices)!=8:continue
        w,d,h=o.dimensions
        cap=c.box('v040 parapet weathered coping',(0,0,0),(w+.055,d+.055,.055),p['stone'],.01)
        cap.matrix_world=o.matrix_world@Matrix.Translation((0,0,h/2+.025));caps+=1
    stats['parapet_copings']=caps
    c.collection('373_Refined_Contoured_Furniture')
    remove=[];count=0
    for o in list(scene.objects):
        if o.name.startswith('Dining stool concave inset'):remove.append(o)
        if not o.name.startswith('Dining cyan round stool'):continue
        pts=[o.matrix_world@Vector(v) for v in o.bound_box];mid=sum(pts,Vector())/8;top=max(v.z for v in pts)
        v,f=dish_mesh();replace_mesh(o,v,f,changes);o.matrix_world=Matrix.Translation((mid.x,mid.y,top-.005))
        for poly in o.data.polygons:poly.use_smooth=True
        count+=1
    changes['retired_objects'].extend(o.name for o in remove)
    bpy.data.batch_remove(ids=tuple(remove))
    stats['contoured_canteen_stools']=count
    shared={};counts={'seat':0,'back':0}
    for o in list(scene.objects):
        typ='seat' if o.name.startswith('Grandstand seat pan') else 'back' if o.name.startswith('Grandstand curved seat back') else None
        if typ is None:continue
        mat=o.data.materials[0];key=(typ,mat.name)
        if key not in shared:
            v,f=curved_seat(back=typ=='back');md=bpy.data.meshes.new('v040 moulded stadium '+typ+' '+mat.name);md.from_pydata(v,[],f);md.materials.append(mat);md.update()
            for poly in md.polygons:poly.use_smooth=True
            shared[key]=md
        o.data=shared[key];o.modifiers.clear();o.location.z+=.10;changes['modified_objects'].append(o.name);counts[typ]+=1
    for o in list(scene.objects):
        if o.name.startswith('Grandstand seat metal fixing'):
            o.scale.z=.33/.23;o.location.z+=.05;changes['modified_objects'].append(o.name)
    stats['moulded_stadium_seats']=counts
    # Replace long block sofa cushions with separately upholstered seat cushions.
    for o in list(scene.objects):
        if not o.name.startswith('Math rest sofa seat'):continue
        mat=o.data.materials[0];base=o.matrix_world.copy()
        for j in range(3):
            q=c.box('v040 separate upholstered sofa cushion',(0,0,0),(.77,.83,.24),mat,.09)
            q.matrix_world=base@Matrix.Translation((-.79+j*.79,0,-.05))
            # Fine piping around the cushion perimeter.
            points=[]
            for x,y in [(-.32,-.35),(.32,-.35),(.36,-.31),(.36,.31),(.32,.35),(-.32,.35),(-.36,.31),(-.36,-.31),(-.32,-.35)]:points.append(base@Vector((-.79+j*.79+x,y,.05)))
            v,f=[],[]
            for a,b in zip(points,points[1:]):c.tube_data(v,f,a,b,.003,.003,6)
            c.mesh('v040 sofa tailored piping',v,f,mat)
        # Retain the lower supporting upholstered base.
        o.scale.z=.38;o.location.z-=.25;changes['modified_objects'].append(o.name)
    for o in list(scene.objects):
        if o.name.startswith(('Math rest sofa back','Math rest sofa arm')):
            o.location.z-=.25;changes['modified_objects'].append(o.name)
    refine_sofa_finish(scene,changes)
    # School desks: undershelf, apron, joinery and rounded backs replacing flat slabs.
    deskmat=bpy.data.materials['Math classroom aged timber']
    for o in list(scene.objects):
        if o.name.startswith('Math old double school desk'):
            base=o.matrix_world.copy()
            for loc,size in [((0,0,-.19),(1.50,.43,.035)),((0,.22,-.10),(1.58,.025,.17))]:
                q=c.box('v040 school desk shelf and apron',(0,0,0),size,deskmat,.005);q.matrix_world=base@Matrix.Translation(loc)
        elif o.name.startswith('Math classroom chair back'):
            v,f=[],[]
            for side in [0,1]:
                for j in range(17):
                    x=-.19+j*.38/16;y=.06*(x/.19)**2-side*.025
                    v.extend([(x,y,-.20),(x,y,.22-.025*(x/.19)**2)])
            for j in range(16):
                f.extend([(2*j,2*j+2,2*j+3,2*j+1),(34+2*j,35+2*j,37+2*j,36+2*j)])
            f.extend([(0,1,35,34),(32,66,67,33)])
            for j in range(16):f.extend([(2*j,34+2*j,36+2*j,2*j+2),(2*j+1,2*j+3,37+2*j,35+2*j)])
            replace_mesh(o,v,f,changes)
    c.collection('374_Refined_Small_Display_Architecture')
    mini=0
    for o in list(scene.objects):
        if not o.name.startswith('History illustrative miniature school massing'):continue
        w,d,h=o.dimensions;v,f=[],[]
        for side in [-1,1]:
            for row in range(3):
                for col in range(6):local_box(v,f,(-w*.42+col*w*.168,side*(d/2+.001),-h*.3+row*h*.28),(w*.105,.002,h*.15))
        component_mesh('v040 miniature windows and rhythm',v,f,p['dark'],o.matrix_world.copy());mini+=1
    stats['detailed_miniature_buildings']=mini
    return stats

def refine_sofa_finish(scene,changes):
    """Set loose pillows onto the seat and keep upholstery edges smoothly rounded."""
    for o in list(scene.objects):
        if o.type!='MESH':continue
        if o.name.startswith('Math rest mustard cushion'):
            o.location.y=119.19;o.location.z=4.925
            o.rotation_euler.x=math.radians(-14)
        if not o.name.startswith(('Math rest sofa seat','Math rest sofa back','Math rest sofa arm','Math rest mustard cushion','v040 separate upholstered sofa cushion')):continue
        for p in o.data.polygons:p.use_smooth=True
        for m in o.modifiers:
            if m.type=='BEVEL':m.segments=6;m.harden_normals=True
        if not any(m.type=='WEIGHTED_NORMAL' for m in o.modifiers):
            normal=o.modifiers.new('v040 upholstery weighted corner normals','WEIGHTED_NORMAL');normal.keep_sharp=True;normal.weight=50
        if not o.name.startswith('v040'):changes['modified_objects'].append(o.name)
