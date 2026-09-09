"""Verify saved position and settings after an actual fresh PIE world startup."""
import unreal,json,math
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert world
pc=unreal.GameplayStatics.get_player_controller(world,0);pawn=unreal.GameplayStatics.get_player_pawn(world,0);hud=pc.get_hud();expected=json.loads((root/'Saved/Logs/tour_restart_expected.json').read_text());position=pawn.get_actor_location();error=(position-unreal.Vector(*expected['position_cm'])).length();rotation=pc.get_control_rotation();angle=abs((rotation.yaw-expected['yaw']+180)%360-180)
r={'position_error_cm':error,'heading_error_degrees':angle,'position_cm':list(position.to_tuple()),'has_saved_visit':bool(pawn.get_editor_property('HasSavedVisit')),'menu_open':bool(hud.get_editor_property('MenuOpen')),'paused':unreal.GameplayStatics.is_game_paused(world),'quality':pawn.get_editor_property('QualityPreset'),'volume':pawn.get_editor_property('TourVolume'),'method':'Fresh PIE startup, loading the disk save written by the destination runtime test.'}
r['passed']=error<15 and angle<2 and r['has_saved_visit'] and r['menu_open'] and r['paused'] and r['quality']==expected['quality'] and abs(r['volume']-expected['volume'])<.001
(root.parent/'Reports/tour_save_restore.json').write_text(json.dumps(r,indent=2),encoding='utf8');print('SAVE_RESTORE',r['passed'],error,angle)
