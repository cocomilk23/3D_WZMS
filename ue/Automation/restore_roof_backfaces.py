"""Keep thin source roofing visible from inside without adding or simplifying geometry."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();source=json.loads(Path('E:/3D_WZMS/builds/v043_ue_bundle/materials.json').read_text(encoding='utf8'));rows=[]
for row in source['materials']:
    if not any(k in row['source_name'].lower() for k in ['roof','tensile']):continue
    mi=unreal.EditorAssetLibrary.load_asset('/Game/WZMS/Materials/Instances/MI_'+row['id']);assert mi
    overrides=mi.get_editor_property('base_property_overrides');overrides.set_editor_property('override_two_sided',True);overrides.set_editor_property('two_sided',True);mi.set_editor_property('base_property_overrides',overrides)
    unreal.MaterialEditingLibrary.update_material_instance(mi);unreal.EditorAssetLibrary.save_loaded_asset(mi)
    rows.append({'material':row['id'],'source_name':row['source_name'],'two_sided':True})
(root.parent/'Reports/campus_roof_backfaces.json').write_text(json.dumps({'materials':rows,'geometry_unchanged':True,'reason':'Source thin roofing must be visible from both exterior and interior in UE.'},indent=2))
