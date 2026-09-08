"""Refine approved estimated layout and attach reversible UE handoff metadata."""
import bpy,sys,json,math,random,hashlib
import numpy as np
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).parent))
import campus_common as c,island_common as h,south_detail_common as s
sc=bpy.data.scenes['WZMS_Campus'];c.activate(sc)
out=c.ROOT/'deliverables/v0.0.43';out.mkdir(parents=True,exist_ok=True)
changes=dict(retired_objects=[],transformed_objects=[],modified_objects=[],reason='User accepts image-estimated dimensions and current layout; environmental detail and pre-UE preparation only.')
stats={};rng=random.Random(43043)

# Keep branch positions, make individual leaves less uniformly small and flat.
# Only the thirteen south precinct trees are changed; no generic whole-campus scale.
trees=[o for o in sc.objects if o.type=='MESH' and o.name.startswith(('Garden broadleaf','v042 bank broadleaf')) and 'individual leaves' in o.name]
for o in trees:
    o.data=o.data.copy();m=o.data
    v=np.empty(len(m.vertices)*3,dtype=np.float32);m.vertices.foreach_get('co',v);v=v.reshape(-1,5,3)
    centre=v[:,2:3,:].copy();rand=np.random.default_rng(int(hashlib.sha256(o.name.encode()).hexdigest()[:8],16))
    scale=rand.uniform(1.22,1.65,(len(v),1,1));v[:]=centre+(v-centre)*scale
    m.vertices.foreach_set('co',v.reshape(-1));m.update();changes['modified_objects'].append(o.name)
stats['refined_south_tree_canopies']=len(trees)

# These materials deliberately remain native master shaders. UE gets explicit
# material recipes, and a separate FBX transfer set, not a false baked-equivalence claim.
modified_materials=[]
for m in bpy.data.materials:
    if not m.use_nodes or any(n.type=='TEX_IMAGE' for n in m.node_tree.nodes):continue
    family=m.get('v040_surface_family');name=m.name.lower()
    if not (family=='soil' and any(k in name for k in ['lawn','grass soil','shaded verge'])) and 'bark' not in name:continue
    nd,lk=m.node_tree.nodes,m.node_tree.links;bs=next((n for n in nd if n.type=='BSDF_PRINCIPLED'),None)
    if not bs:continue
    co=nd.new('ShaderNodeTexCoord');co.name='v043 surface coordinates'
    noise=nd.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=2.2 if 'bark' not in name else 4
    noise.inputs['Detail'].default_value=4
    if 'bark' in name:
        stretch=nd.new('ShaderNodeVectorMath');stretch.operation='MULTIPLY';stretch.inputs[1].default_value=(8,8,.55)
        lk.new(co.outputs['Object'],stretch.inputs[0]);lk.new(stretch.outputs[0],noise.inputs['Vector'])
    else:lk.new(co.outputs['Object'],noise.inputs['Vector'])
    ramp=nd.new('ShaderNodeValToRGB');base=tuple(m.diffuse_color[:3])
    ramp.color_ramp.elements[0].position=.18;ramp.color_ramp.elements[1].position=.82
    ramp.color_ramp.elements[0].color=(*(v*.65 for v in base),1)
    ramp.color_ramp.elements[1].color=(*(v*1.25 for v in base),1)
    lk.new(noise.outputs['Fac'],ramp.inputs[0]);lk.new(ramp.outputs[0],bs.inputs['Base Color'])
    bump=nd.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.32;bump.inputs['Distance'].default_value=.012 if 'bark' in name else .005
    if bs.inputs['Normal'].is_linked:lk.new(bs.inputs['Normal'].links[0].from_socket,bump.inputs['Normal'])
    lk.new(noise.outputs['Fac'],bump.inputs['Height']);lk.new(bump.outputs[0],bs.inputs['Normal'])
    m['v043_environment_refinement']=True;modified_materials.append(m.name)

c.collection('390_Environment_Stone_Coping')
stones=[c.material('v043 sawn granite tone '+str(i),color,.79) for i,color in enumerate([(.36,.38,.34),(.40,.41,.37),(.43,.44,.40),(.38,.395,.36)])]
for m in stones:c.noise(m,95,.2,.0015)
shorelines=[([(13,-13),(13,21),(25,29),(50,32),(61.5,28.5)],.37),([(-94,-68),(92,-68),(115,-57),(110,-51),(85,-51)],.52)]
count=0
for poly,width in shorelines:
    for a,b in zip(poly,poly[1:]):
        a,b=Vector(a),Vector(b);length=(b-a).length;steps=math.ceil(length/1.15);direction=(b-a).normalized()
        for j in range(steps):
            aa=a+direction*(length*j/steps+.008);bb=a+direction*(length*(j+1)/steps-.008)
            ob=s.segment('v043 jointed bank coping',aa,bb,width,stones[rng.randrange(4)],.035,.105)
            mod=ob.modifiers.new('Sawn stone eased arris','BEVEL');mod.width=.006;mod.segments=2;count+=1
stats['individual_coping_stones']=count

# Sediment/wet mineral band is below the walkway and just above water level.
c.collection('391_Environment_Wet_Bank_And_Fittings')
wet=c.material('v043 damp shoreline mineral',(.13,.16,.105),.88);c.noise(wet,35,.3,.003)
for name in ['v042 lotus bay mainland retaining edge','v042 south granite shoreline']:
    old=sc.objects[name];ob=old.copy();ob.data=old.data.copy();ob.name='v043 shoreline water stain';c.COL.objects.link(ob)
    for v in ob.data.vertices:v.co.z=-.93 if v.co.z>-.1 else -1.23
    ob.data.materials.clear();ob.data.materials.append(wet)
    # A thin coating outside each retaining wall, away from coplanar faces.
    for k in range(0,len(ob.data.vertices),4):
        a,b=ob.data.vertices[k].co,ob.data.vertices[k+1].co;d=(b-a).normalized()*.006
        for j in [0,2]:ob.data.vertices[k+j].co-=d
        for j in [1,3]:ob.data.vertices[k+j].co+=d
metal=c.material('v043 cast iron drainage',(.035,.042,.041),.65,.55)
concrete=c.material('v043 weathered drain surround',(.25,.27,.25),.86);c.noise(concrete,90,.22,.001)
for x,y,angle in [(8.4,-28,0),(8.4,-43,0),(27,-53.4,math.pi/2),(64,-53.4,math.pi/2),(55.3,40,0)]:
    # Grates occupy planted margins beside paths; no new vertical obstructions.
    frame=c.box('v043 drain outer rim',(x,y,-.016),(.44,.70,.052),metal,.006);frame.rotation_euler.z=angle
    base=c.box('v043 drain sump shadow',(x,y,-.042),(.39,.65,.04),metal)
    for j in range(10):
        dx,dy=0,-.285+j*.063
        o=c.box('v043 drain grate rib',(x+dx*math.cos(angle)-dy*math.sin(angle),y+dx*math.sin(angle)+dy*math.cos(angle),.012),(.37,.018,.025),concrete,.003);o.rotation_euler.z=angle
stats['drain_grates']=5

c.collection('392_Environment_Instanced_Underplanting')
# Three authored reusable grass clumps: true folded blades, no alpha cards.
grassm=[c.material('v043 sedge green '+str(i),co,.71) for i,co in enumerate([(.09,.16,.032),(.14,.23,.052),(.23,.29,.085)])]
protos=[]
for k in range(3):
    v=[];f=[];ids=[]
    for j in range(44):
        az=rng.random()*math.tau;r=rng.uniform(0,.15);x,y=r*math.cos(az),r*math.sin(az)
        ht=rng.uniform(.14,.34);bend=rng.uniform(.10,.23);w=rng.uniform(.008,.016);st=len(v)
        side=Vector((-math.sin(az)*w,math.cos(az)*w,0));a=Vector((x,y,0));b=a+Vector((math.cos(az)*bend*.35,math.sin(az)*bend*.35,ht*.7));tip=a+Vector((math.cos(az)*bend,math.sin(az)*bend,ht))
        v.extend([a-side,a+side,b-side*.6,b+side*.6,b+Vector((0,0,.006)),tip]);f.extend([(st,st+1,st+4),(st,st+4,st+2),(st+1,st+3,st+4),(st+2,st+4,st+5),(st+4,st+3,st+5)]);ids.extend([j%3]*5)
    proto=c.mesh('v043 sedge reusable clump '+str(k),v,f,grassm,ids);protos.append(proto)
positions=[]
for a,b in [((11.4,-10),(11.4,17)),((17.8,27.0),(25,31.2)),((27,33.5),(48,36.0)),((5,-50),(7,-26))]:
    a,b=Vector(a),Vector(b)
    for j in range(math.ceil((b-a).length/.35)):
        q=a.lerp(b,rng.random());positions.append((q.x+rng.uniform(-.25,.25),q.y+rng.uniform(-.25,.25)))
for i,(x,y) in enumerate(positions):
    p=protos[i%3];o=p if i<3 else p.copy()
    if i>=3:c.COL.objects.link(o)
    o.location=(x,y,-.04);scale=rng.uniform(.7,1.2);o.scale=(scale,scale,scale);o.rotation_euler.z=rng.random()*math.tau
stats['grass_clump_instances']=len(positions);stats['grass_unique_meshes']=3

c.collection('393_Environment_Canopy_Litter')
v=[];f=[];idx=[]
leafm=[c.material('v043 dry fallen leaf '+str(i),co,.92) for i,co in enumerate([(.14,.095,.031),(.21,.155,.052),(.25,.20,.081)])]
for branch in [o for o in sc.objects if o.type=='MESH' and o.name.startswith(('Garden broadleaf','v042 bank broadleaf')) and 'branches' in o.name]:
    # Trunk first ring identifies the actual tree base, including gate-plaza shear.
    base=sum((branch.matrix_world@branch.data.vertices[j].co for j in range(12)),Vector())/12
    for j in range(50):
        az=rng.random()*math.tau;r=rng.uniform(.25,.80);p=base+Vector((math.cos(az)*r,math.sin(az)*r,.012))
        c.leaf_data(v,f,idx,p,rng.uniform(.035,.08),rng,j%3)
c.mesh('v043 sparse leaf litter under tree bases',v,f,leafm,idx)

# Metadata is separate from user-facing object names. It supports deterministic,
# partitioned transfer without collapsing the editable master or changing placement.
for o in sc.objects:
    if o.type!='MESH':continue
    q=o.matrix_world@Vector(o.bound_box[0]);bounds=[o.matrix_world@Vector(v) for v in o.bound_box]
    mid=sum(bounds,Vector())/8
    o['ue_zone']=('south' if mid.y<85 else 'north' if mid.y>=330 else 'west' if mid.x<-15 else 'east' if mid.x>100 else 'central')
    names=' '.join(m.name.lower() for m in o.data.materials if m)
    o['ue_surface_role']='foliage' if any(k in names for k in ['leaf','foliage','grass blade','sedge','groundcover']) else 'water' if any(k in names for k in ['lake water','green water']) else 'glass' if any(k in names for k in ['glazing','glass']) else 'solid'
    o['ue_asset_id']='SM_'+hashlib.sha256(o.name.encode()).hexdigest()[:14]
    o['ue_collision_policy']='none' if o['ue_surface_role'] in ['foliage','water'] else 'static_surface_review'
sc['dimension_policy']='User accepted image-estimated dimensions on 2026-09-08; retain current layout.'
sc['ue_handoff_status']='Prepared master; FBX roundtrip and material migration manifest accompany delivery. Runtime not yet verified.'
sc['render_review_samples']=96
c.collection('394_Environment_Review_Cameras')
for name,source in [('190_Environment_south_aerial','186_South_registered_aerial'),('191_Environment_gate_garden','188_South_gate_registered_axis'),('192_Environment_lotus_bank','189_Heyu_registered_shore')]:
    old=sc.objects[source];o=old.copy();o.data=old.data.copy();o.name=name;c.COL.objects.link(o)
c.camera('193_Environment_bank_close',(10.0,-1.5,1.72),(18,13,-.35),30)
stats['refined_materials']=modified_materials
(out/'replacement_scope.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf8')
(out/'environment_refinement.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf8')
h.save(43,'Environmental refinement on accepted v042 estimated layout: south canopy leaves, jointed granite coping, damp bank band, drainage fittings, instanced sedges, sparse leaf litter and campus lawn/bark shaders. Stable UE identifiers, zones and surface roles attached without renaming or moving the editable source. Preserve source-photo wall. Unknown rooms and Xinjiang remain excluded.',[347,348,349,352,353,354,359,364,365,366],'190_Environment_south_aerial')
