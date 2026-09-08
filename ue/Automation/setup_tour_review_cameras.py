"""Add a highest-library-floor review viewpoint without changing the tour start."""
import unreal,math,json
from pathlib import Path
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);actors={a.get_actor_label():a for a in sub.get_all_level_actors()}
name='Review_Tour_Library_Top';pos=unreal.Vector(11800,-14400,1015);delta=unreal.Vector(13900,-16600,1015)-pos;rot=unreal.Rotator(pitch=0,yaw=math.degrees(math.atan2(delta.y,delta.x)),roll=0)
a=actors.get(name) or sub.spawn_actor_from_class(unreal.CameraActor,pos,rot);a.set_actor_label(name);a.set_actor_location(pos,False,True);a.set_actor_rotation(rot,False);a.set_folder_path('Tour Review Cameras');a.get_component_by_class(unreal.CameraComponent).set_field_of_view(80)
source=json.loads(Path('E:/3D_WZMS/builds/v043_ue_bundle/scene_reference.json').read_text(encoding='utf8'))
for row in source['cameras']:
 if not row['name'].startswith('158_'):continue
 m=row['world_matrix'];d=(-m[0][2],m[1][2],-m[2][2]);p=unreal.Vector(m[0][3]*100,-m[1][3]*100,m[2][3]*100);r=unreal.Rotator(pitch=math.degrees(math.atan2(d[2],math.hypot(d[0],d[1]))),yaw=math.degrees(math.atan2(d[1],d[0])),roll=0)
 label='Review_'+row['name'];b=actors.get(label) or sub.spawn_actor_from_class(unreal.CameraActor,p,r);b.set_actor_label(label);b.set_folder_path('Tour Review Cameras');b.get_component_by_class(unreal.CameraComponent).set_editor_property('field_of_view',math.degrees(2*math.atan(row['sensor_width_mm']/(2*row['lens_mm']))))
label='Review_Tour_Zhouyuan_Inside';b=actors.get(label) or sub.spawn_actor_from_class(unreal.CameraActor,unreal.Vector(-3000,-13000,165),unreal.Rotator(pitch=0,yaw=180,roll=0));b.set_actor_label(label);b.set_folder_path('Tour Review Cameras');b.get_component_by_class(unreal.CameraComponent).set_editor_property('field_of_view',80)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
