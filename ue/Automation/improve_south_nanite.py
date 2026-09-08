import unreal,json,gc
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();report=root.parent/'Reports/south_nanite.json'
zone=json.loads(Path('E:/3D_WZMS/builds/v043_ue_bundle/zone_south.json').read_text())
ss=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem);rows=[]
for ch in zone['chunks']:
    if ch['role'] not in ['foliage','solid']:continue
    mesh=unreal.EditorAssetLibrary.load_asset('/Game/WZMS/South/Meshes/'+ch['name'])
    ns=ss.get_nanite_settings(mesh)
    ns.enabled=True
    ns.shape_preservation=unreal.NaniteShapePreservation.PRESERVE_AREA if ch['role']=='foliage' else unreal.NaniteShapePreservation.NONE
    ns.keep_percent_triangles=1;ns.trim_relative_error=0
    ns.fallback_target=unreal.NaniteFallbackTarget.PERCENT_TRIANGLES;ns.fallback_percent_triangles=1
    ss.set_nanite_settings(mesh,ns,True)
    unreal.EditorAssetLibrary.save_loaded_asset(mesh)
    rows.append({'mesh':ch['name'],'enabled':True,'shape_preservation':str(ns.shape_preservation),'source_retained':True,'fallback_percent':1.0})
    report.write_text(json.dumps({'complete':False,'meshes':rows},indent=2))
report.write_text(json.dumps({'complete':True,'meshes':rows},indent=2))
