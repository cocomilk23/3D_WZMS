"""Runtime-only bounded-volume diagnostic; discarded on stopping PIE."""
import unreal
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert world
pc=unreal.GameplayStatics.get_player_controller(world,0);pc.get_hud().call_method('VisitTourPlace',(18,))
a=next(a for a in unreal.GameplayStatics.get_all_actors_of_class(world,unreal.Actor) if a.get_actor_label()=='InteriorExposure_Library')
a.get_component_by_class(unreal.PostProcessComponent).set_editor_property('unbound',True)
