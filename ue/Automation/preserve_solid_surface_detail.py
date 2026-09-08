import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();rows=[]
for actor in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors():
    if not actor.get_actor_label().startswith('SM_south_solid_'):continue
    actor.static_mesh_component.set_editor_property('disallow_nanite',True)
    rows.append(actor.get_actor_label())
assert len(rows)==10
unreal.SystemLibrary.execute_console_command(None,'r.Shadow.Virtual.NonNanite.IncludeInCoarsePages 0')
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
(root.parent/'Reports/south_render_fidelity.json').write_text(json.dumps({'solid_components_use_full_source_fallback':rows,'reason':'Retain millimetre-separated painted lines and layered paving; Nanite simplification/quantization caused visible distant surface artifacts at actor scale 100.','foliage_nanite_retained':True,'non_nanite_coarse_shadow_pages':False},indent=2))
