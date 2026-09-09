"""Check bounded exposure with a queryable, nonblocking shape in the actual game world."""
import unreal
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert world
a=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(world,unreal.Actor) if a.get_actor_label()=='InteriorExposure_Library')
box=a.get_component_by_class(unreal.BoxComponent)
box.set_collision_enabled(unreal.CollisionEnabled.QUERY_ONLY)
box.set_collision_response_to_all_channels(unreal.CollisionResponseType.ECR_IGNORE)
box.set_editor_property('generate_overlap_events',False)
a.get_component_by_class(unreal.PostProcessComponent).set_editor_property('unbound',False)
