"""Review saved lighting through a camera in the real PIE world, without exposure overrides."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve()
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assert world
request=json.loads((root/'Saved/Logs/tour_camera_request.json').read_text(encoding='utf8'))
label=request['camera']
assert label.startswith('Review_')
cameras=[a for a in unreal.GameplayStatics.get_all_actors_of_class(world,unreal.CameraActor) if a.get_actor_label()==label]
assert len(cameras)==1,(label,len(cameras))
pc=unreal.GameplayStatics.get_player_controller(world,0)
hud=pc.get_hud()
hud.call_method('SetTourMenu',(False,))
hud.set_editor_property('show_hud',False)
pawn=unreal.GameplayStatics.get_player_pawn(world,0)
if not pawn.get_editor_property('Flying'):pawn.call_method('ToggleFlight')
pawn.set_actor_location(cameras[0].get_actor_location()-unreal.Vector(0,0,80),False,True)
pc.set_control_rotation(cameras[0].get_actor_rotation())
pc.set_view_target_with_blend(cameras[0],0)
print('Runtime camera',label)
