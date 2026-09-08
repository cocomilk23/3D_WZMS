"""Persist UE 5.8 Nanite material usage before final review and editor restart."""
import unreal,json
from pathlib import Path
source=Path('E:/3D_WZMS/builds/v043_ue_bundle');root=Path(unreal.Paths.project_dir()).resolve();used=set()
for zone in ['south','central','west','east','north']:
    data=json.loads((source/f'zone_{zone}.json').read_text(encoding='utf8'))
    used.update(mid for chunk in data['chunks'] if chunk['role']=='foliage' for mid in chunk['materials'])
usage=next(getattr(unreal.MaterialUsage,n) for n in dir(unreal.MaterialUsage) if n.upper().endswith('NANITE'))
for mid in sorted(used):
    mi=unreal.EditorAssetLibrary.load_asset('/Game/WZMS/Materials/Instances/MI_'+mid);assert mi
    unreal.MaterialEditingLibrary.set_material_usage_override(mi,usage,True,True)
    unreal.MaterialEditingLibrary.update_material_instance(mi);unreal.EditorAssetLibrary.save_loaded_asset(mi)
(root.parent/'Reports/campus_material_usage.json').write_text(json.dumps({'nanite_material_instances':len(used),'ids':sorted(used),'usage_persisted':True},indent=2))
