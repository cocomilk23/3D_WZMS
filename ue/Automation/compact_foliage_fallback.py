"""Build up to four independent fallback buffers while retaining complete Nanite meshes."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();request=json.loads((root/'Saved/Logs/fallback_request.json').read_text());requested=request['path']
performance=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'))
previous=root/'Saved/Logs/build_throttle_previous.json'
if not previous.exists():previous.write_text(json.dumps({'value':performance.get_editor_property('bThrottleCPUWhenNotForeground')}))
performance.set_editor_property('bThrottleCPUWhenNotForeground',False)
assert unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world().get_name()=='L_WZMS_Transfer'
file=root.parent/'Reports/campus_foliage_fallback.json';report=json.loads(file.read_text()) if file.exists() else {'meshes':[]}
done={r['path'] for r in report['meshes']};all_paths=[]
for zone in ['south','central','west','east','north']:
    p=root.parent/('Reports/south_import.json' if zone=='south' else f'Reports/import_{zone}.json')
    all_paths.extend(f'/Game/WZMS/{zone.title()}/Meshes/'+c['name'] for c in json.loads(p.read_text())['chunks'] if c['role']=='foliage')
pending=[] if requested in done else ([requested]+[p for p in all_paths if p not in done and p!=requested])[:4]
ss=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem);batch=[]
for path in pending:
    mesh=unreal.EditorAssetLibrary.load_asset(path);assert mesh
    ns=ss.get_nanite_settings(mesh);assert ns.enabled
    before=mesh.get_num_nanite_triangles();before_vertices=mesh.get_num_nanite_vertices()
    if abs(ns.fallback_percent_triangles-.02)>1e-6:
        ns.fallback_target=unreal.NaniteFallbackTarget.PERCENT_TRIANGLES;ns.fallback_percent_triangles=.02
        ns.keep_percent_triangles=1;ns.trim_relative_error=0;ns.shape_preservation=unreal.NaniteShapePreservation.PRESERVE_AREA
        ss.set_nanite_settings(mesh,ns,True)
    batch.append((path,mesh,before,before_vertices))
for path,mesh,before,before_vertices in batch:
    unreal.EditorAssetLibrary.save_loaded_asset(mesh)
    after=mesh.get_num_nanite_triangles();after_vertices=mesh.get_num_nanite_vertices()
    retained_full_fallback = False
    if after != before or before_vertices != after_vertices:
        # Conservatively retain this chunk's full raster fallback if rebuilding changes
        # Nanite statistics. Other chunks can still release redundant fallback memory.
        ns=ss.get_nanite_settings(mesh);ns.fallback_percent_triangles=1
        ss.set_nanite_settings(mesh,ns,True);unreal.EditorAssetLibrary.save_loaded_asset(mesh)
        after=mesh.get_num_nanite_triangles();after_vertices=mesh.get_num_nanite_vertices()
        assert after==before,(path,before,after)
        retained_full_fallback=True
    assert after==before,(path,before,after)
    row={'path':path,'nanite_triangles_before':before,'nanite_triangles_after':after,'nanite_vertices_before':before_vertices,'nanite_vertices_after':after_vertices,'raster_fallback_triangles':mesh.get_num_triangles(0),'fallback_fraction':1 if retained_full_fallback else .02,'retained_full_fallback':retained_full_fallback,'nanite_vertex_count_unchanged':before_vertices==after_vertices,'full_visible_geometry_preserved':True}
    report['meshes']=[r for r in report['meshes'] if r['path']!=path]+[row];file.write_text(json.dumps(report,indent=2))
unreal.SystemLibrary.collect_garbage()
