"""Disable unused AI navigation generation, retaining exact player collision meshes."""
import unreal,json
from pathlib import Path
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world();assert world.get_name()=='L_WZMS_Campus'
settings=world.get_world_settings();settings.set_editor_property('navigation_system_config',None)
count=0
for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors():
    if a.get_actor_label().startswith('SM_'):
        c=a.get_component_by_class(unreal.StaticMeshComponent)
        if c:c.set_editor_property('can_ever_affect_navigation',False);count+=1
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
(Path(unreal.Paths.project_dir()).resolve().parent/'Reports/campus_navigation.json').write_text(json.dumps({'mesh_components':count,'ai_navigation_generation':False,'player_collision_preserved':True,'reason':'Campus uses directly controlled walking/flying; it does not currently have AI pathfinding agents.'},indent=2))
