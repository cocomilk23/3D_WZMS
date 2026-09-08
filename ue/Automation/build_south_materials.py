"""Rebuild UE surface materials using source colours, photos and physical parameters."""
import unreal,json
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()).resolve();SOURCE=Path('E:/3D_WZMS/builds/v043_ue_bundle')
src=json.loads((SOURCE/'materials.json').read_text(encoding='utf8'))
zone=json.loads((SOURCE/'zone_south.json').read_text(encoding='utf8'))
used={m for c in zone['chunks'] for m in c['materials']}
rows=[m for m in src['materials'] if m['id'] in used]
assets=unreal.EditorAssetLibrary;at=unreal.AssetToolsHelpers.get_asset_tools();ed=unreal.MaterialEditingLibrary
BASE='/Game/WZMS/Materials';reports=[]
def texture(file,name,srgb=True):
    path='/Game/WZMS/Textures/'+name;tx=assets.load_asset(path)
    if not tx:
        t=unreal.AssetImportTask();t.filename=str(file);t.destination_path='/Game/WZMS/Textures';t.destination_name=name;t.automated=True;t.save=True
        at.import_asset_tasks([t]);tx=assets.load_asset(path)
    assert tx,path
    tx.set_editor_property('srgb',srgb);assets.save_loaded_asset(tx);return tx
noise=texture(ROOT.parent/'SourceTextures/T_SurfaceDetail.png','T_SurfaceDetail',False)
photo_default=texture(ROOT.parent/'SourceTextures/T_SurfaceDetail.png','T_PhotoPlaceholder',True)
def expr(mat,cls,**props):
    node=ed.create_material_expression(mat,getattr(unreal,'MaterialExpression'+cls),0,0)
    for k,v in props.items():node.set_editor_property(k,v)
    return node
def connect(a,b,pin='',out=''):
    assert ed.connect_material_expressions(a,out,b,pin),(a,b,pin,out)
def output(a,prop,out=''):
    assert ed.connect_material_property(a,out,getattr(unreal.MaterialProperty,'MP_'+prop)),prop
def scalar(mat,name,value):return expr(mat,'ScalarParameter',parameter_name=name,default_value=float(value))
def vector(mat,name,col):return expr(mat,'VectorParameter',parameter_name=name,default_value=unreal.LinearColor(*col[:3],1))
def custom(mat,code,inputs,kind):
    node=expr(mat,'Custom',code=code,output_type=getattr(unreal.CustomMaterialOutputType,kind))
    items=[]
    for name in inputs:
        item=unreal.CustomInput();item.set_editor_property('input_name',name);items.append(item)
    node.set_editor_property('inputs',items)
    for name,source in inputs.items():connect(source,node,name)
    return node
masters={}
for family in ['surface','foliage','glass','water','photo']:
    name='M_WZMS_'+family;mat=assets.load_asset(BASE+'/'+name)
    if not mat:mat=at.create_asset(name,BASE,unreal.Material,unreal.MaterialFactoryNew())
    ed.delete_all_material_expressions(mat)
    mat.set_editor_property('two_sided',family in ['foliage','glass','water'])
    mat.set_editor_property('tangent_space_normal',False)
    if family=='foliage':mat.set_editor_property('shading_model',unreal.MaterialShadingModel.MSM_TWO_SIDED_FOLIAGE)
    if family in ['glass','water']:
        mat.set_editor_property('blend_mode',unreal.BlendMode.BLEND_TRANSLUCENT)
        mat.set_editor_property('translucency_lighting_mode',unreal.TranslucencyLightingMode.TLM_SURFACE)
        output(scalar(mat,'Opacity',.28 if family=='glass' else .78),'OPACITY')
    rough=scalar(mat,'Roughness',.65);metal=scalar(mat,'Metallic',0)
    output(rough,'ROUGHNESS');output(metal,'METALLIC')
    color_a=vector(mat,'ColorA',[.2,.2,.2]);color_b=vector(mat,'ColorB',[.3,.3,.3])
    normal=expr(mat,'VertexNormalWS')
    if family=='photo':
        sample=expr(mat,'TextureSampleParameter2D',parameter_name='Photo',texture=photo_default)
        output(sample,'BASE_COLOR','RGB')
    else:
        pos=expr(mat,'WorldPosition');scale=scalar(mat,'DetailSizeCm',100)
        tex=expr(mat,'TextureObjectParameter',parameter_name='SurfaceDetail',texture=noise)
        timer=expr(mat,'Time');speed=scalar(mat,'Flow',.018 if family=='water' else 0)
        pattern=custom(mat,'''float3 p=Pos/max(Size,0.01)+float3(Time*Flow,Time*Flow*0.6,0);
float3 w=pow(abs(N),4);w/=max(w.x+w.y+w.z,0.0001);
float3 a=Texture2DSample(Detail,DetailSampler,p.yz).rgb;
float3 b=Texture2DSample(Detail,DetailSampler,p.xz).rgb;
float3 c=Texture2DSample(Detail,DetailSampler,p.xy).rgb;
return dot(a*w.x+b*w.y+c*w.z,float3(.48,.32,.20));''',{'Pos':pos,'N':normal,'Size':scale,'Detail':tex,'Time':timer,'Flow':speed},'CMOT_FLOAT1')
        mix=expr(mat,'LinearInterpolate');connect(color_a,mix,'A');connect(color_b,mix,'B');connect(pattern,mix,'Alpha');output(mix,'BASE_COLOR')
        bump=scalar(mat,'ReliefCm',.04)
        perturbed=custom(mat,'''float3 n=normalize(N);float3 px=ddx(P),py=ddy(P);
float3 r1=cross(py,n),r2=cross(n,px);float d=dot(px,r1);
float3 g=sign(d)*(ddx(H)*r1+ddy(H)*r2)*Strength;
return normalize(n-g/max(abs(d),0.000001));''',{'N':normal,'P':pos,'H':pattern,'Strength':bump},'CMOT_FLOAT3')
        output(perturbed,'NORMAL')
        if family=='foliage':
            sub=expr(mat,'Multiply');connect(mix,sub,'A');connect(scalar(mat,'LeafTransmission',.35),sub,'B');output(sub,'SUBSURFACE_COLOR')
    ed.layout_material_expressions(mat);ed.recompile_material(mat);assets.save_loaded_asset(mat);masters[family]=mat

import runpy
base_parameters=runpy.run_path(str(Path(__file__).with_name('source_material_values.py')))['base_parameters']
for row in rows:
    name=row['source_name'].lower();family=row['family']
    parent='photo' if row['textures'] else 'foliage' if family=='leaf' or 'pine needles' in name else family if family in ['glass','water'] else 'surface'
    path=BASE+'/Instances/MI_'+row['id'];mi=assets.load_asset(path)
    if not mi:mi=at.create_asset('MI_'+row['id'],BASE+'/Instances',unreal.MaterialInstanceConstant,unreal.MaterialInstanceConstantFactoryNew())
    ed.set_material_instance_parent(mi,masters[parent])
    a,b,rough,metal=base_parameters(row)
    for key,col in [('ColorA',a),('ColorB',b)]:ed.set_material_instance_vector_parameter_value(mi,key,unreal.LinearColor(*col,1))
    size,relief=(65,.10) if any(x in name for x in ['lawn','grass','soil','bark']) else (30,.28) if parent=='water' else (150,.015) if parent in ['foliage','glass'] else (100,.035)
    for key,val in [('Roughness',rough),('Metallic',metal),('DetailSizeCm',size),('ReliefCm',relief)]:ed.set_material_instance_scalar_parameter_value(mi,key,val)
    if row['textures']:
        file=row['textures'][0];tx=texture(SOURCE/file,Path(file).stem,True);ed.set_material_instance_texture_parameter_value(mi,'Photo',tx)
    ed.update_material_instance(mi);assets.save_loaded_asset(mi)
    reports.append({'id':row['id'],'source_name':row['source_name'],'instance':path,'family':parent,'source_transfer_status':row['transfer_status'],'source_photos':row['textures'],'colour_endpoints':[a,b],'roughness':rough,'metallic':metal})
pending=[]
actors={a.get_actor_label():a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()}
for ch in zone['chunks']:
    mesh=assets.load_asset('/Game/WZMS/South/Meshes/'+ch['name'])
    actor=actors.get(ch['name'])
    if not mesh or not actor:pending.append(ch['name']);continue
    for index,slot in enumerate(mesh.static_materials):
        mid=str(slot.material_slot_name);material=assets.load_asset(BASE+'/Instances/MI_'+mid)
        assert material,mid;actor.static_mesh_component.set_material(index,material)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
(ROOT.parent/'Reports/south_materials.json').write_text(json.dumps({'complete':not pending,'pending_meshes':pending,'materials':reports,'masters':list(masters),'note':'UE reconstruction from recorded source colours and physical scalar values, original photos retained. Procedural graphs are rebuilt for UE, not claimed shader-identical.'},ensure_ascii=False,indent=2),encoding='utf8')
print('WZMS_SOUTH_MATERIALS_COMPLETE',len(reports))
