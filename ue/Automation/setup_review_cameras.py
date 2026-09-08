"""Reproduce the frozen Blender review cameras in Unreal coordinates."""
import unreal,json,math
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve()
source=json.loads(Path('E:/3D_WZMS/builds/v043_ue_bundle/scene_reference.json').read_text())
names=['188_South_gate_registered_axis','05_Plaza_from_gate','187_Tennis_registered_school_view','186_South_registered_aerial']
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
existing={a.get_actor_label():a for a in sub.get_all_level_actors()}
rows=[]
for row in source['cameras']:
    if row['name'] not in names:continue
    matrix=row['world_matrix'];direction=(-matrix[0][2],matrix[1][2],-matrix[2][2])
    pos=unreal.Vector(matrix[0][3]*100,-matrix[1][3]*100,matrix[2][3]*100)
    rot=unreal.Rotator(pitch=math.degrees(math.atan2(direction[2],math.hypot(direction[0],direction[1]))),yaw=math.degrees(math.atan2(direction[1],direction[0])),roll=0)
    name='Review_'+row['name'];camera=existing.get(name) or sub.spawn_actor_from_class(unreal.CameraActor,pos,rot)
    camera.set_actor_location(pos,False,True);camera.set_actor_rotation(rot,False);camera.set_actor_label(name);camera.set_folder_path('Review Cameras')
    fov=math.degrees(2*math.atan(row['sensor_width_mm']/(2*row['lens_mm'])))
    camera.get_component_by_class(unreal.CameraComponent).set_editor_property('field_of_view',fov)
    camera.get_component_by_class(unreal.CameraComponent).set_editor_property('aspect_ratio',16/9)
    rows.append({'label':name,'location_cm':[pos.x,pos.y,pos.z],'rotation':{'pitch':rot.pitch,'yaw':rot.yaw,'roll':rot.roll},'fov':fov})
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
(root.parent/'Reports/review_cameras.json').write_text(json.dumps(rows,indent=2))
