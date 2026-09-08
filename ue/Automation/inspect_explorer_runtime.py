import unreal,json
from pathlib import Path
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert world
pc=unreal.GameplayStatics.get_player_controller(world,0);pawn=unreal.GameplayStatics.get_player_pawn(world,0);assert pawn
move=pawn.get_component_by_class(unreal.CharacterMovementComponent)
def vec(v):return [v.x,v.y,v.z]
report={'pawn':pawn.get_class().get_name(),'location_cm':vec(pawn.get_actor_location()),'movement_mode':str(move.movement_mode),'flying':pawn.get_editor_property('Flying'),'camera':str(pc.get_view_target()),'camera_components':[(x.get_name(),vec(x.get_world_location())) for x in pawn.get_components_by_class(unreal.CameraComponent)],'collision_enabled':str(pawn.get_component_by_class(unreal.CapsuleComponent).get_collision_enabled()),'ground_checks':[]}
for name,x,y in [('spawn',-1450,3000),('gate',0,0),('plaza_near',0,-1000),('plaza_middle',0,-2500),('plaza_far',0,-4400),('tennis',3100,4200)]:
    hit=unreal.SystemLibrary.line_trace_single(world,unreal.Vector(x,y,500),unreal.Vector(x,y,-500),unreal.TraceTypeQuery.ECC_VISIBILITY,False,[pawn],unreal.DrawDebugTrace.NONE)
    report['ground_checks'].append({'point':name,'xy_cm':[x,y],'blocking_hit':hit is not None})
Path(unreal.Paths.project_dir()).resolve().parent.joinpath('Reports/runtime_initial.json').write_text(json.dumps(report,indent=2))
