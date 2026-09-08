"""Full-detail static transfer, partitioned by zone/role with bounded mesh chunks.

Does not save/change the authoring blend. FBX materials are transfer placeholders;
native shader graphs and packed photographs are exported separately for UE rebuild.
"""
import bpy,sys,json,hashlib,math,array,time
import numpy as np
from pathlib import Path
from mathutils import Matrix,Vector
sys.path.insert(0,str(Path(__file__).parent))
from culture_stages import STAGES
R=Path(__file__).resolve().parents[2];OUT=R/'builds/v043_ue_bundle';OUT.mkdir(parents=True,exist_ok=True)
(OUT/'Meshes').mkdir(exist_ok=True);(OUT/'Textures').mkdir(exist_ok=True)
zone=sys.argv[sys.argv.index('--')+1]
source=R/'models/campus/WZMS_Campus_v043.blend'
source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
sc=bpy.data.scenes['WZMS_Campus'];bpy.context.window.scene=sc
def ident(prefix,name):return prefix+'_'+hashlib.sha256(name.encode()).hexdigest()[:14]
def jsonval(v):
    if isinstance(v,(str,int,float,bool)) or v is None:return v
    try:return [jsonval(x) for x in v]
    except TypeError:return str(v)
geometry_types={'MESH','CURVE','FONT','SURFACE','META'}
used=sorted({m for o in sc.objects if o.type in geometry_types and not o.hide_render for m in o.data.materials if m},key=lambda m:m.name)
images={};materials=[];transfer={}
for m in used:
    matid=ident('M',m.name);nodes=[];photo=[];bs=None
    if m.use_nodes:
        for n in m.node_tree.nodes:
            row={'name':n.name,'type':n.bl_idname,'inputs':{str(i)+':'+s.name:jsonval(s.default_value) for i,s in enumerate(n.inputs) if hasattr(s,'default_value')}}
            for key in ['operation','blend_type','vector_type','noise_dimensions','gradient_type','wave_type','bands_direction','wave_profile','interpolation','extension','projection']:
                if hasattr(n,key):row[key]=jsonval(getattr(n,key))
            if hasattr(n,'color_ramp'):row['ramp']={'interpolation':n.color_ramp.interpolation,'elements':[(e.position,list(e.color)) for e in n.color_ramp.elements]}
            if n.type=='BSDF_PRINCIPLED':bs=n
            if n.type=='TEX_IMAGE' and n.image:
                im=n.image;data=bytes(im.packed_file.data) if im.packed_file else Path(bpy.path.abspath(im.filepath)).read_bytes()
                digest=hashlib.sha256(data).hexdigest();ext='.jpg' if data[:2]==b'\xff\xd8' else '.png'
                file='Textures/T_'+digest[:18]+ext
                if zone=='south' and not (OUT/file).exists():(OUT/file).write_bytes(data)
                # Accessing Blender image.size can decode every 4352-square panorama
                # into retained pixel buffers. Hash/extract packed bytes directly.
                images[digest]={'file':file,'sha256':digest,'bytes':len(data)};row['image_file']=file;photo.append((im,file))
            nodes.append(row)
    linked=[s.name for s in bs.inputs if s.is_linked] if bs else []
    procedural=any(n.type.startswith('TEX_') and n.type not in ['TEX_IMAGE','TEX_COORD'] for n in m.node_tree.nodes) if m.use_nodes else False
    kind='native_procedural_rebuild' if procedural else 'photo_material_review' if photo else 'scalar_material'
    row={'id':matid,'source_name':m.name,'family':m.get('v040_surface_family','other'),'transfer_status':kind,'diffuse_color':list(m.diffuse_color),'nodes':nodes,'links':[(l.from_node.name,l.from_socket.name,l.to_node.name,l.to_socket.name) for l in m.node_tree.links] if m.use_nodes else [],'linked_principled_inputs':linked,'textures':[p[1] for p in photo]}
    materials.append(row)
    tm=bpy.data.materials.new(matid);tm.use_nodes=True;pb=tm.node_tree.nodes.get('Principled BSDF')
    pb.inputs['Base Color'].default_value=m.diffuse_color;tm.diffuse_color=m.diffuse_color
    if bs:
        for key in ['Metallic','Roughness','Alpha','IOR','Transmission Weight']:
            if key in bs.inputs:pb.inputs[key].default_value=bs.inputs[key].default_value
    if photo:
        im,file=photo[0];ni=tm.node_tree.nodes.new('ShaderNodeTexImage');ni.image=im;ni.image.filepath=str(OUT/file)
        tm.node_tree.links.new(ni.outputs['Color'],pb.inputs['Base Color'])
    transfer[m.name]=tm
if zone=='south':
    (OUT/'materials.json').write_text(json.dumps({'source_sha256':source_hash,'materials':materials,'textures':list(images.values()),'warning':'FBX carries placeholder materials and source photos only. Rebuild native procedural shaders and verify transparency/subsurface/water in UE before visual acceptance.'},ensure_ascii=False,indent=2),encoding='utf8')
    (OUT/'scene_reference.json').write_text(json.dumps({'source_sha256':source_hash,'units':'metres','estimated_dimensions_accepted':True,'cameras':[{'name':o.name,'world_matrix':[list(r) for r in o.matrix_world],'lens_mm':o.data.lens,'sensor_width_mm':o.data.sensor_width} for o in sc.objects if o.type=='CAMERA'],'lights':[{'name':o.name,'type':o.data.type,'world_matrix':[list(r) for r in o.matrix_world],'energy_blender_units':o.data.energy,'color':list(o.data.color)} for o in sc.objects if o.type=='LIGHT'],'note':'Lighting values are Blender reference values, not direct UE photometric equivalents.'},indent=2),encoding='utf8')

def object_zone(o):
    if o.get('ue_zone'):return o['ue_zone']
    q=sum((o.matrix_world@Vector(v) for v in o.bound_box),Vector())/8
    return 'south' if q.y<85 else 'north' if q.y>=330 else 'west' if q.x<-15 else 'east' if q.x>100 else 'central'
def object_role(o):
    # Legacy pine shaders predate the master's broadleaf role hints.
    if any('pine needles' in m.name.lower() for m in o.data.materials if m):return 'foliage'
    return o.get('ue_surface_role','solid')
if zone=='south':
    scene_file=OUT/'scene_reference.json';scene_reference=json.loads(scene_file.read_text(encoding='utf8'))
    superseded={r for st in STAGES.values() if st['previous']<43 for r in st.get('supersedes_routes',[])}
    scene_reference['walkthrough_routes']=[{'name':f'v{r}: '+name,'floor_points_m':poly} for r in range(17,44) if r not in superseded for name,poly in STAGES[r]['routes']]
    scene_reference['spawn_reference_foot_position_m']=[-14.5,-30,0]
    scene_reference['route_note']='74 Blender geometric checks; add capsule half-height to floor references and convert coordinates when creating UE actors. Runtime collision remains untested.'
    scene_file.write_text(json.dumps(scene_reference,indent=2),encoding='utf8')
objects=sorted([o for o in sc.objects if o.type in geometry_types and not o.hide_render and object_zone(o)==zone],key=lambda o:(object_role(o),o.name))
assert objects,zone
source_total=sum(o.type in geometry_types and not o.hide_render for o in sc.objects)
deps=bpy.context.evaluated_depsgraph_get()
export_scene=bpy.data.scenes.new('UE_Transfer');export_scene.unit_settings.system='METRIC';export_scene.unit_settings.scale_length=1
records=[];mapping=[];chunk=0;parts=[];size=0;current_role=None
def flush():
    global parts,size,chunk
    if not parts:return
    chunk+=1;name=f'SM_{zone}_{current_role}_{chunk:03}'
    verts=np.concatenate([p['v'] for p in parts]);tri=[];uv=[];norm=[];indices=[];offset=0;slots=[]
    for p in parts:
        tri.append(p['t']+offset);offset+=len(p['v']);uv.append(p['uv']);norm.append(p['n'])
        local=[]
        for mat in p['mats']:
            if mat not in slots:slots.append(mat)
            local.append(slots.index(mat))
        indices.append(np.asarray(local,dtype=np.int32)[p['ids']])
    faces=np.concatenate(tri);uv=np.concatenate(uv);norm=np.concatenate(norm);ids=np.concatenate(indices)
    lo=verts.min(axis=0);hi=verts.max(axis=0);pivot=(lo+hi)/2
    md=bpy.data.meshes.new(name);md.vertices.add(len(verts));md.vertices.foreach_set('co',(verts-pivot).reshape(-1))
    md.loops.add(faces.size);md.loops.foreach_set('vertex_index',faces.reshape(-1));md.polygons.add(len(faces))
    md.polygons.foreach_set('loop_start',np.arange(len(faces),dtype=np.int32)*3);md.polygons.foreach_set('loop_total',np.full(len(faces),3,dtype=np.int32))
    for mat in slots:md.materials.append(transfer[mat])
    md.polygons.foreach_set('material_index',ids);md.update()
    layer=md.uv_layers.new(name='UV0');layer.data.foreach_set('uv',uv.reshape(-1))
    md.polygons.foreach_set('use_smooth',np.ones(len(faces),dtype=bool));md.normals_split_custom_set(norm.tolist())
    obj=bpy.data.objects.new(name,md);export_scene.collection.objects.link(obj);obj.location=pivot.tolist()
    bpy.context.window.scene=export_scene;bpy.context.view_layer.objects.active=obj;obj.select_set(True)
    file='Meshes/'+name+'.fbx'
    bpy.ops.export_scene.fbx(filepath=str(OUT/file),use_selection=True,object_types={'MESH'},use_mesh_modifiers=False,mesh_smooth_type='FACE',use_tspace=False,add_leaf_bones=False,bake_anim=False,path_mode='RELATIVE',embed_textures=False,axis_forward='-Y',axis_up='Z',apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',use_custom_props=False)
    report={'file':file,'name':name,'role':current_role,'source_objects':[p['source'] for p in parts],'vertices':len(verts),'triangles':len(faces),'bounds_m':[lo.tolist(),hi.tolist()],'pivot_blender_m':pivot.tolist(),'materials':[ident('M',mat) for mat in slots],'material_triangle_counts':np.bincount(ids,minlength=len(slots)).tolist(),'sha256':hashlib.sha256((OUT/file).read_bytes()).hexdigest(),'bytes':(OUT/file).stat().st_size,'collision_policy':'none' if current_role in ['foliage','water'] else 'review_static_complex_collision_after_import'}
    records.append(report);print('UE_CHUNK_EXPORTED',name,len(faces),flush=True)
    bpy.data.objects.remove(obj,do_unlink=True);bpy.data.meshes.remove(md);bpy.context.window.scene=sc
    parts=[];size=0

for i,o in enumerate(objects):
    role=object_role(o)
    if role!=current_role:flush();current_role=role
    ev=o.evaluated_get(deps);me=ev.to_mesh(preserve_all_data_layers=True,depsgraph=deps)
    if not me or not len(me.polygons):
        if me:ev.to_mesh_clear()
        mapping.append({'object':o.name,'excluded':'empty mesh'});continue
    me.calc_loop_triangles()
    co=np.empty(len(me.vertices)*3,dtype=np.float32);me.vertices.foreach_get('co',co);co=co.reshape(-1,3)
    mat=np.array(o.matrix_world,dtype=np.float64);co=(co@mat[:3,:3].T+mat[:3,3]).astype(np.float32)
    assert np.isfinite(co).all() and abs(np.linalg.det(mat[:3,:3]))>1e-12,('Invalid transform/vertices',o.name)
    t=np.empty(len(me.loop_triangles)*3,dtype=np.int32);me.loop_triangles.foreach_get('vertices',t);t=t.reshape(-1,3)
    li=np.empty(len(me.loop_triangles)*3,dtype=np.int32);me.loop_triangles.foreach_get('loops',li);li=li.reshape(-1,3)
    if np.linalg.det(mat[:3,:3])<0:t=t[:,::-1].copy();li=li[:,::-1].copy()
    normal=np.empty(len(me.corner_normals)*3,dtype=np.float32);me.corner_normals.foreach_get('vector',normal)
    normal=normal.reshape(-1,3)[li.reshape(-1)]@np.linalg.inv(mat[:3,:3]);normal/=np.maximum(np.linalg.norm(normal,axis=1,keepdims=True),1e-10)
    if me.uv_layers.active:
        u=np.empty(len(me.loops)*2,dtype=np.float32);me.uv_layers.active.data.foreach_get('uv',u);uv=u.reshape(-1,2)[li.reshape(-1)]
    else:
        # UV0 is a metre projection for procedural reconstruction, not lightmap UV.
        xyz=co[t.reshape(-1)];axis=np.abs(normal).argmax(axis=1)
        uv=np.stack([np.where(axis==0,xyz[:,1],xyz[:,0]),np.where(axis==2,xyz[:,1],xyz[:,2])],axis=1)
    ids=np.empty(len(me.loop_triangles),dtype=np.int32);me.loop_triangles.foreach_get('material_index',ids)
    assert len(me.materials) and all(m is not None for m in me.materials),('Unassigned material',o.name)
    mats=[m.name for m in me.materials]
    assert ids.min()>=0 and ids.max()<len(mats),('Invalid material index',o.name)
    if size+len(co)>180000 or len(set(mats)|{m for p in parts for m in p['mats']})>24:flush()
    parts.append({'source':o.name,'v':co,'t':t,'uv':uv,'n':normal,'mats':mats,'ids':ids});size+=len(co)
    mapping.append({'object':o.name,'id':o.get('ue_asset_id',ident('SM',o.name)),'source_type':o.type,'role':role,'evaluated_triangles':len(t),'original_mesh':o.data.name,'uv0':'preserved' if me.uv_layers.active else 'world_metre_projection','negative_transform_baked':bool(np.linalg.det(mat[:3,:3])<0)})
    ev.to_mesh_clear()
flush()
assert hashlib.sha256(source.read_bytes()).hexdigest()==source_hash
(OUT/f'zone_{zone}.json').write_text(json.dumps({'zone':zone,'source_sha256':source_hash,'source_visible_mesh_total':source_total,'source_objects':len(objects),'objects':mapping,'chunks':records,'triangle_decimation':False,'uv0':'Preserved original UV when available; otherwise per-corner dominant-plane world metre projection. No lightmap UV claim.','placement':'Use FBX Scene Import with transforms. Individual static mesh imports must restore saved pivots; inspect handedness in UE.'},ensure_ascii=False,indent=2),encoding='utf8')
print('UE_TRANSFER_ZONE_COMPLETE',zone,flush=True)
