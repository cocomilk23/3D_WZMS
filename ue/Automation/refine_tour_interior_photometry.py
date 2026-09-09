"""Increase useful interior illumination from existing luminaires, preserving geometry."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve()
sub=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
assert not sub.get_game_world()
actors={a.get_actor_label():a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()}
baseline=json.loads((root.parent/'Reports/campus_interior_lighting.json').read_text(encoding='utf8'))
changes=[]
for row in baseline['lights']:
 name=row['source_name'];area=name.split(' ')[0]
 if area=='Library':continue
 factor=3.0 if 'upper industrial' in name or area=='Canteen' else {'Gym':2.0,'Zhouyuan':1.8,'Math':1.6,'Alumni':1.6,'History':1.3}.get(area,1.0)
 a=actors[row['ue_label']];c=a.get_component_by_class(unreal.LocalLightComponent)
 intensity=150000 if area=='Canteen' else row['estimated_lumens']*factor
 c.set_intensity(intensity)
 c.set_light_color(unreal.LinearColor(1,1,1,1))
 c.set_editor_property('use_temperature',True)
 temperature=4200 if area in ['Alumni','History'] else 5000
 c.set_editor_property('temperature',temperature)
 changes.append({'actor':a.get_actor_label(),'original_estimated_lumens':row['estimated_lumens'],'revised_lumens':intensity,'temperature_k':temperature})
materials=[]
lighting=json.loads((root.parent/'Reports/tour_interior_lighting.json').read_text(encoding='utf8'))
for row in lighting['authored_lamp_materials_restored']:
 if row['source_material'].startswith('Library'):continue
 mi=unreal.EditorAssetLibrary.load_asset(row['instance']);assert mi
 luminance=row['estimated_luminance']*8
 unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(mi,'LampLuminance',luminance)
 unreal.MaterialEditingLibrary.update_material_instance(mi)
 unreal.EditorAssetLibrary.save_loaded_asset(mi)
 materials.append({'material':row['source_material'],'instance':row['instance'],'luminance':luminance})
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
(root.parent/'Reports/tour_interior_photometry.json').write_text(json.dumps({'purpose':'Improve darker gym upper hall and canteen, reduce colored cast using existing neutral/warm-white luminaires. No global exposure or geometry change.','lights':changes,'lamp_materials':materials,'visual_validation_pending':True,'estimated_photometry':True},indent=2),encoding='utf8')
