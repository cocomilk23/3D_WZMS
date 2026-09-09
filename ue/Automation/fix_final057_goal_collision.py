"""Keep goal posts solid while low decorative rear braces do not snag walkers."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
cube=unreal.load_asset('/Engine/BasicShapes/Cube');rows=[]
for side,cy in [('South',227.5),('North',332.5)]:
 actor=next(a for a in sub.get_all_level_actors() if a.get_actor_label()=='SM_Final057_Goal_'+side)
 actor.static_mesh_component.set_collision_profile_name('NoCollision')
 for part,loc,size in [('Left',(-88.72,cy,1.25),(.12,.12,2.5)),('Right',(-81.28,cy,1.25),(.12,.12,2.5)),('Crossbar',(-85,cy,2.5),(7.56,.12,.12))]:
  name='Final057_GoalCollision_'+side+'_'+part
  assert not any(a.get_actor_label()==name for a in sub.get_all_level_actors())
  a=sub.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(loc[0]*100,-loc[1]*100,loc[2]*100));a.set_actor_label(name);a.set_folder_path('Final Delivery/057 Corrections');a.set_actor_scale3d(unreal.Vector(*size))
  c=a.static_mesh_component;c.set_static_mesh(cube);c.set_mobility(unreal.ComponentMobility.STATIC);c.set_collision_profile_name('BlockAll');c.set_editor_property('visible',False);c.set_editor_property('hidden_in_game',True);c.set_editor_property('cast_shadow',False);c.set_editor_property('can_ever_affect_navigation',False)
  rows.append({'actor':name,'centre_blender_m':loc,'size_m':size})
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
(root.parent/'Reports/final057_goal_collision.json').write_text(json.dumps({'posts_and_crossbar_solid':True,'low_braces_visual_only':True,'proxies':rows},indent=2))
