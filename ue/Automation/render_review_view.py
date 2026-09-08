import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve()
request=json.loads((root/'Saved/Logs/review_request.json').read_text())
camera=next(a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors() if a.get_actor_label()==request['camera'])
group=request.get('group','South');assert group in ['South','Campus']
out=root.parent/'Reviews'/group/request['filename'];out.parent.mkdir(parents=True,exist_ok=True)
unreal.AutomationLibrary.take_high_res_screenshot(1600,900,str(out),camera=camera,delay=5.0,force_game_view=True)
