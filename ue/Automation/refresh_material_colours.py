import unreal,json,runpy
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()).resolve()
values=runpy.run_path(str(ROOT.parent/'Automation/source_material_values.py'))['base_parameters']
source=json.loads(Path('E:/3D_WZMS/builds/v043_ue_bundle/materials.json').read_text(encoding='utf8'))
report_path=ROOT.parent/'Reports/south_materials.json';report=json.loads(report_path.read_text(encoding='utf8'));used={r['id'] for r in report['materials']}
for row in source['materials']:
    if row['id'] not in used:continue
    mi=unreal.load_asset('/Game/WZMS/Materials/Instances/MI_'+row['id']);assert mi
    a,b,rough,metal=values(row)
    for key,col in [('ColorA',a),('ColorB',b)]:unreal.MaterialEditingLibrary.set_material_instance_vector_parameter_value(mi,key,unreal.LinearColor(r=col[0],g=col[1],b=col[2],a=1))
    unreal.MaterialEditingLibrary.update_material_instance(mi);unreal.EditorAssetLibrary.save_loaded_asset(mi)
    r=next(r for r in report['materials'] if r['id']==row['id']);r['colour_endpoints']=[a,b]
report['source_colour_links_followed']=True;report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
