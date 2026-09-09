import unreal
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert world
pc=unreal.GameplayStatics.get_player_controller(world,0);hud=pc.get_hud();hud.call_method('SetTourMenu',(False,));hud.set_editor_property('show_hud',True)
unreal.GameplayStatics.set_game_paused(world,False)
