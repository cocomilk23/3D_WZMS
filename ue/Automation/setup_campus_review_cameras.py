"""Transfer representative current source cameras, retaining source lens and pose."""
import unreal,json,math
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve()
source=json.loads(Path('E:/3D_WZMS/builds/v043_ue_bundle/scene_reference.json').read_text(encoding='utf8'))
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);existing={a.get_actor_label():a for a in sub.get_all_level_actors()};rows=[]
prefixes=['18_','38_','40_','63_','67_','69_','70_','106_','111_','138_','139_','141_','147b_','148_','149_','150_','152_','153_','155_','156_','157_','159_','161_','164_','167_','172_','174_','176_','177_','178_','179_','180_','181_','182_']
for row in source['cameras']:
    if not any(row['name'].startswith(p) for p in prefixes):continue
    m=row['world_matrix'];direction=(-m[0][2],m[1][2],-m[2][2]);pos=unreal.Vector(m[0][3]*100,-m[1][3]*100,m[2][3]*100)
    rot=unreal.Rotator(pitch=math.degrees(math.atan2(direction[2],math.hypot(direction[0],direction[1]))),yaw=math.degrees(math.atan2(direction[1],direction[0])),roll=0)
    name='Review_'+row['name'];a=existing.get(name) or sub.spawn_actor_from_class(unreal.CameraActor,pos,rot)
    a.set_actor_label(name);a.set_actor_location(pos,False,True);a.set_actor_rotation(rot,False);a.set_folder_path('Review Cameras/Campus')
    fov=math.degrees(2*math.atan(row['sensor_width_mm']/(2*row['lens_mm'])))
    c=a.get_component_by_class(unreal.CameraComponent);c.set_editor_property('field_of_view',fov);c.set_editor_property('aspect_ratio',16/9)
    rows.append({'label':name,'position_cm':list(pos.to_tuple()),'fov':fov})
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
(root.parent/'Reports/campus_review_cameras.json').write_text(json.dumps(rows,indent=2))
