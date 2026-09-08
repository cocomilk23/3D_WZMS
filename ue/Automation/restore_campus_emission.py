"""Add emissive variants only for source materials with authored emission."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();assets=unreal.EditorAssetLibrary;ed=unreal.MaterialEditingLibrary
source=json.loads(Path('E:/3D_WZMS/builds/v043_ue_bundle/materials.json').read_text(encoding='utf8'))
base='/Game/WZMS/Materials';masters={}
for family in ['surface','photo']:
    path=base+'/M_WZMS_'+family+'_emissive';mat=assets.load_asset(path)
    if not mat:
        mat=assets.duplicate_asset(base+'/M_WZMS_'+family,path);assert mat
        strength=ed.create_material_expression(mat,unreal.MaterialExpressionScalarParameter);strength.set_editor_property('parameter_name','EmissionStrength');strength.set_editor_property('default_value',0)
        if family=='photo':
            colour=ed.get_material_property_input_node(mat,unreal.MaterialProperty.MP_BASE_COLOR)
            output=ed.get_material_property_input_node_output_name(mat,unreal.MaterialProperty.MP_BASE_COLOR)
        else:
            colour=ed.create_material_expression(mat,unreal.MaterialExpressionVectorParameter);colour.set_editor_property('parameter_name','EmissionColor');colour.set_editor_property('default_value',unreal.LinearColor(r=1,g=1,b=1,a=1));output='RGB'
        multiply=ed.create_material_expression(mat,unreal.MaterialExpressionMultiply)
        assert ed.connect_material_expressions(colour,output,multiply,'A')
        assert ed.connect_material_expressions(strength,'',multiply,'B')
        assert ed.connect_material_property(multiply,'',unreal.MaterialProperty.MP_EMISSIVE_COLOR)
        ed.layout_material_expressions(mat);ed.recompile_material(mat);assets.save_loaded_asset(mat)
    masters[family]=mat
rows=[]
for row in source['materials']:
    node=next((n for n in row['nodes'] if n['type']=='ShaderNodeBsdfPrincipled'),None)
    if not node:continue
    strength=node['inputs'].get('28:Emission Strength',0)
    if strength<=0:continue
    family='photo' if row['textures'] else 'surface';mi=assets.load_asset(base+'/Instances/MI_'+row['id']);assert mi
    ed.set_material_instance_parent(mi,masters[family]);col=node['inputs'].get('27:Emission Color',[1,1,1,1])
    # Restore relative source emission; local luminaires provide the physical illumination.
    ed.set_material_instance_scalar_parameter_value(mi,'EmissionStrength',strength*100)
    ed.set_material_instance_vector_parameter_value(mi,'EmissionColor',unreal.LinearColor(r=col[0],g=col[1],b=col[2],a=1))
    ed.update_material_instance(mi);assets.save_loaded_asset(mi)
    rows.append({'id':row['id'],'source_strength':strength,'ue_emission_multiplier':strength*100,'source_name':row['source_name']})
(root.parent/'Reports/campus_emission.json').write_text(json.dumps({'materials':rows,'count':len(rows),'estimated_radiometric_conversion':True},ensure_ascii=False,indent=2),encoding='utf8')
