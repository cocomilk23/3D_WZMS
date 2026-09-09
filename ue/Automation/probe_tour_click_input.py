import unreal,json
from pathlib import Path
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert world
pc=unreal.GameplayStatics.get_player_controller(world,0)
before={n:pc.get_editor_property(n) for n in ['enable_click_events','enable_mouse_over_events','show_mouse_cursor']}
pc.set_editor_property('enable_click_events',True)
pc.set_editor_property('enable_mouse_over_events',True)
root=Path(unreal.Paths.project_dir()).resolve();(root/'Saved/Logs/tour_click_probe.json').write_text(json.dumps(before,indent=2),encoding='utf8')
