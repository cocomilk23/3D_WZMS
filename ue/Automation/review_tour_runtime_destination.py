"""Select a reference destination for rendered runtime review, without altering lighting."""
import json, unreal
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve()
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assert world
request=json.loads((root/'Saved/Logs/tour_visual_request.json').read_text(encoding='utf8'))
index=request['destination_index']
assert isinstance(index,int) and 0<=index<24
pc=unreal.GameplayStatics.get_player_controller(world,0)
pc.get_hud().call_method('VisitTourPlace',(index,))
print('Runtime visual destination',index)
