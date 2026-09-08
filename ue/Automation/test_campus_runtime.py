"""Drive the real PIE CharacterMovement through representative main-campus aisles."""
import unreal,json,time,traceback,math
from pathlib import Path
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert world
pawn=unreal.GameplayStatics.get_player_pawn(world,0);assert pawn
pc=unreal.GameplayStatics.get_player_controller(world,0);move=pawn.get_component_by_class(unreal.CharacterMovementComponent)
root=Path(unreal.Paths.project_dir()).resolve();dest=root.parent/'Reports/campus_runtime.json'
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));old=settings.get_editor_property('bThrottleCPUWhenNotForeground');settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
cases=[('South gate',(-14.5,-30,0),(0,1,0)),('Library ground entry',(116,155,0),(1,0,0)),('Library upper entry',(116,155,4.25),(1,0,0)),('Mathematics gallery',(143,131,0),(1,0,0)),('History gallery',(253,124,0),(0,1,0)),('Alumni east exit',(-42,162,0),(1,0,0)),('Basketball central aisle',(14.5,280,0),(0,1,0)),('Gym ground hall',(-81.5,399,1.08),(0,1,0)),('Gym upper hall',(-76,405,6.08),(0,1,0)),('Canteen central aisle',(124.4,358,1.04),(0,1,0))]
results={'complete':False,'tests':[],'map':world.get_name(),'notes':'Actual compiled pawn movement in PIE for 1.5 seconds per sample; does not certify every possible player route.'};holder=[None];state={'index':0,'phase':'settle','start':time.perf_counter()}
def enter(i):
    name,p,d=cases[i]
    if pawn.get_editor_property('Flying'):pawn.call_method('ToggleFlight')
    move.stop_movement_immediately();move.set_movement_mode(unreal.MovementMode.MOVE_WALKING)
    pawn.set_actor_location(unreal.Vector(p[0]*100,-p[1]*100,p[2]*100+94),False,True)
    pc.set_control_rotation(unreal.Rotator(pitch=0,yaw=math.degrees(math.atan2(-d[1],d[0])),roll=0))
    state.update(index=i,phase='settle',start=time.perf_counter())
def finish():
    pawn.call_method('ReturnToGate');settings.set_editor_property('bThrottleCPUWhenNotForeground',old)
    unreal.unregister_slate_post_tick_callback(holder[0]);dest.write_text(json.dumps(results,indent=2))
def tick(dt):
    try:
        elapsed=time.perf_counter()-state['start'];i=state['index'];name,p,d=cases[i]
        if state['phase']=='settle':
            if elapsed<1:return
            state.update(phase='walk',start=time.perf_counter(),origin=pawn.get_actor_location());return
        pawn.add_movement_input(unreal.Vector(d[0],-d[1],d[2]),1,False)
        if elapsed<1.5:return
        location=pawn.get_actor_location();travel=(location-state['origin']).length();on_floor=move.movement_mode==unreal.MovementMode.MOVE_WALKING
        expected_floor=p[2]*100
        if name=='Library ground entry':
            # Frozen source route v18 starts its real staircase at x=121 m.
            expected_floor=max(0,min(425,(location.x/100-121)/6.72*425))
        z_error=abs(location.z-(expected_floor+90));passed=travel>300 and on_floor and z_error<45
        results['tests'].append({'location':name,'travel_cm':travel,'walking_on_floor':on_floor,'floor_capsule_height_error_cm':z_error,'passed':passed,'end_position_cm':list(location.to_tuple())})
        dest.write_text(json.dumps(results,indent=2))
        if i+1<len(cases):enter(i+1)
        else:
            pawn.call_method('ReturnToGate');before=pawn.get_actor_location();pawn.call_method('ToggleFlight')
            flight=pawn.get_editor_property('Flying') and move.movement_mode==unreal.MovementMode.MOVE_FLYING
            pawn.set_actor_location(unreal.Vector(10000,-18000,20000),False,True);pawn.call_method('ToggleFlight')
            restored=(pawn.get_actor_location()-before).length()<50
            results['flight_toggle_passed']=bool(flight and restored);results['complete']=True;results['passed']=all(t['passed'] for t in results['tests']) and results['flight_toggle_passed'];finish()
    except Exception:
        results['error']=traceback.format_exc();finish()
enter(0);holder[0]=unreal.register_slate_post_tick_callback(tick)
