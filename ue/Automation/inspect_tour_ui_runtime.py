"""Capture authoritative UI/player state for manual input verification."""
import unreal,json,time
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve()
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
result={'observed_unix':time.time(),'playing':bool(world)}
if world:
 pc=unreal.GameplayStatics.get_player_controller(world,0);pawn=unreal.GameplayStatics.get_player_pawn(world,0);hud=pc.get_hud()
 result.update(paused=unreal.GameplayStatics.is_game_paused(world),hud_class=hud.get_class().get_name(),position_cm=list(pawn.get_actor_location().to_tuple()),yaw=pc.get_control_rotation().yaw)
 result['hud']={n:hud.get_editor_property(n) for n in ['MenuOpen','HelpOpen','Initialized','UIWidth','UIHeight','UIScale','UIOriginX','UIOriginY','NearestPlace','HUDQuality','HUDVolume','HoverName']}
 result['player']={n:pawn.get_editor_property(n) for n in ['TourMenuOpen','QualityPreset','TourVolume','HasSavedVisit','SaveSucceeded','Flying']}
 result['resolution_scale']=unreal.GameUserSettings.get_game_user_settings().get_resolution_scale_information_ex()
out=root/'Saved/Logs/tour_ui_observation.json';out.write_text(json.dumps(result,ensure_ascii=False,indent=2,default=str),encoding='utf8')
print(json.dumps(result,ensure_ascii=False,default=str))
