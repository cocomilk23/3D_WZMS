"""Make bounded indoor exposure work in PIE/cooked play without blocking characters."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();assets=unreal.EditorAssetLibrary
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
bp=assets.load_asset('/Game/WZMS/Blueprints/BP_WZMS_InteriorExposure');assert bp
sub=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
def configure(box):
 box.set_collision_enabled(unreal.CollisionEnabled.QUERY_ONLY)
 box.set_collision_response_to_all_channels(unreal.CollisionResponseType.ECR_IGNORE)
 box.set_editor_property('generate_overlap_events',False)
for h in sub.k2_gather_subobject_data_for_blueprint(bp):
 o=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h))
 if isinstance(o,unreal.BoxComponent):configure(o)
unreal.BlueprintEditorLibrary.compile_blueprint(bp);assets.save_loaded_asset(bp)
rows=[]
for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors():
 if not a.get_actor_label().startswith('InteriorExposure_'):continue
 box=a.get_component_by_class(unreal.BoxComponent);pp=a.get_component_by_class(unreal.PostProcessComponent);assert box and pp
 configure(box);pp.set_editor_property('unbound',False)
 rows.append({'actor':a.get_actor_label(),'query_shape':str(box.get_collision_enabled()),'responses':str(box.get_editor_property('body_instance').get_editor_property('collision_responses'))})
assert len(rows)==8
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
(root.parent/'Reports/tour_exposure_bounds_fix.json').write_text(json.dumps({'cause':'The NoCollision shape did not supply a runtime distance query for the bounded PostProcessComponent. QueryOnly with all responses ignored restores exposure without blocking movement.','volumes':rows,'runtime_library_probe':'Bounded query enabled: real first-person library stair view changed from near-black to illuminated; unbound probe first isolated the cause.','fresh_world_validation_pending':True},indent=2),encoding='utf8')
