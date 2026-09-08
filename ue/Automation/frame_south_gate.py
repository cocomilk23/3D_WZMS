import unreal,json
from pathlib import Path
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
for label,pos,target in [('Review_Gate_Exterior',(-2500,9000,750),(-2500,2200,500)),('Review_Plaza_Clear',(-1450,1500,190),(-1450,-6000,950))]:
    a=next((a for a in sub.get_all_level_actors() if a.get_actor_label()==label),None)
    loc=unreal.Vector(*pos);rot=unreal.MathLibrary.find_look_at_rotation(loc,unreal.Vector(*target))
    a=a or sub.spawn_actor_from_class(unreal.CameraActor,loc,rot)
    a.set_actor_label(label);a.set_folder_path('Review Cameras');a.set_actor_location(loc,False,True);a.set_actor_rotation(rot,False)
    a.get_component_by_class(unreal.CameraComponent).set_editor_property('field_of_view',65)
    a.get_component_by_class(unreal.CameraComponent).set_editor_property('aspect_ratio',16/9)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
