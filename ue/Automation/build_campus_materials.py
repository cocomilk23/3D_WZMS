"""Extend the approved material library without rebuilding existing master materials."""
import unreal,json,runpy
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();source=Path('E:/3D_WZMS/builds/v043_ue_bundle')
rows=json.loads((source/'materials.json').read_text(encoding='utf8'))['materials']
assets=unreal.EditorAssetLibrary;at=unreal.AssetToolsHelpers.get_asset_tools();ed=unreal.MaterialEditingLibrary
base='/Game/WZMS/Materials';masters={k:assets.load_asset(base+'/M_WZMS_'+k) for k in ['surface','foliage','glass','water','photo']}
assert all(masters.values())
values=runpy.run_path(str(Path(__file__).with_name('source_material_values.py')))['base_parameters']
results=[]
def texture(file):
    name=Path(file).stem;path='/Game/WZMS/Textures/'+name;tx=assets.load_asset(path)
    if not tx:
        task=unreal.AssetImportTask();task.filename=str(source/file);task.destination_path='/Game/WZMS/Textures';task.destination_name=name;task.automated=True;task.save=True
        at.import_asset_tasks([task]);tx=assets.load_asset(path);assert tx
        tx.set_editor_property('srgb',True);assets.save_loaded_asset(tx)
    return tx
for row in rows:
    name=row['source_name'].lower();family=row['family']
    parent='photo' if row['textures'] else 'foliage' if family=='leaf' or 'pine needles' in name else family if family in ['glass','water'] else 'surface'
    path=base+'/Instances/MI_'+row['id'];mi=assets.load_asset(path);created=mi is None
    if created:
        mi=at.create_asset('MI_'+row['id'],base+'/Instances',unreal.MaterialInstanceConstant,unreal.MaterialInstanceConstantFactoryNew());assert mi
        ed.set_material_instance_parent(mi,masters[parent])
        a,b,rough,metal=values(row)
        for key,col in [('ColorA',a),('ColorB',b)]:ed.set_material_instance_vector_parameter_value(mi,key,unreal.LinearColor(r=col[0],g=col[1],b=col[2],a=1))
        size,relief=(65,.10) if any(x in name for x in ['lawn','grass','soil','bark']) else (30,.28) if parent=='water' else (150,.015) if parent in ['foliage','glass'] else (100,.035)
        for key,val in [('Roughness',rough),('Metallic',metal),('DetailSizeCm',size),('ReliefCm',relief)]:ed.set_material_instance_scalar_parameter_value(mi,key,val)
        if row['textures']:ed.set_material_instance_texture_parameter_value(mi,'Photo',texture(row['textures'][0]))
        ed.update_material_instance(mi);assets.save_loaded_asset(mi)
    results.append({'id':row['id'],'source_name':row['source_name'],'instance':path,'family':parent,'created':created,'source_photos':row['textures']})
    if len(results)%20==0:(root.parent/'Reports/campus_materials.json').write_text(json.dumps({'complete':False,'materials':results},ensure_ascii=False,indent=2),encoding='utf8')
(root.parent/'Reports/campus_materials.json').write_text(json.dumps({'complete':True,'materials':results,'count':len(results),'source_colour_links_followed':True},ensure_ascii=False,indent=2),encoding='utf8')
