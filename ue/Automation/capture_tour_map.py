"""Capture a fixed north-up orthographic map from the actual campus scene."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);actors={a.get_actor_label():a for a in sub.get_all_level_actors()}
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
loc=unreal.Vector(11000,-18500,90000);rot=unreal.Rotator(pitch=-90,yaw=-90,roll=0);name='Tour_Map_Orthographic'
a=actors.get(name) or sub.spawn_actor_from_class(unreal.CameraActor,loc,rot);a.set_actor_label(name);a.set_actor_location(loc,False,True);a.set_actor_rotation(rot,False);a.set_folder_path('Tour Review Cameras');c=a.get_component_by_class(unreal.CameraComponent);c.set_projection_mode(unreal.CameraProjectionMode.ORTHOGRAPHIC);c.set_editor_property('ortho_width',62000);c.set_editor_property('aspect_ratio',1);c.set_editor_property('constrain_aspect_ratio',True)
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
out=root.parent/'SourceTextures/T_Tour_CampusMap.png';unreal.AutomationLibrary.take_high_res_screenshot(2048,2048,str(out),camera=a,delay=5,force_game_view=True)
(root.parent/'SourceReference/tour_map_projection.json').write_text(json.dumps({'source':'Orthographic render of actual UE scene','north':'Blender +Y / UE -Y','centre_blender_m':[110,185],'width_m':620,'bounds_blender_m':[-200,-125,420,495],'pixel_size':[2048,2048],'u_formula':'(source_x+200)/620','v_formula':'(495-source_y)/620','image':'SourceTextures/T_Tour_CampusMap.png'},indent=2),encoding='utf8')
