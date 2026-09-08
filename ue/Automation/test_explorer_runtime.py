"""Exercise the compiled pawn inside PIE; record evidence, never edit the map."""
import unreal,json,time,traceback,statistics
from pathlib import Path
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert world
pawn=unreal.GameplayStatics.get_player_pawn(world,0);assert pawn
pc=unreal.GameplayStatics.get_player_controller(world,0)
move=pawn.get_component_by_class(unreal.CharacterMovementComponent)
dest=Path(unreal.Paths.project_dir()).resolve().parent/'Reports/explorer_runtime.json'
def vec(v):return [v.x,v.y,v.z]
def state():return {'location_cm':vec(pawn.get_actor_location()),'flying':pawn.get_editor_property('Flying'),'mode':str(move.movement_mode)}
results={'complete':False,'initial':state(),'tests':[]}
pawn.call_method('ReturnToGate')
walk_origin=pawn.get_actor_location()
pawn.call_method('ToggleFlight');assert pawn.get_editor_property('Flying') and move.movement_mode==unreal.MovementMode.MOVE_FLYING
results['tests'].append({'test':'compiled ToggleFlight enters flight','passed':True})
pawn.set_actor_location(unreal.Vector(-1450,3000,5000),False,True)
pawn.call_method('ToggleFlight');assert not pawn.get_editor_property('Flying') and move.movement_mode==unreal.MovementMode.MOVE_WALKING
restored=pawn.get_actor_location()
assert abs(restored.x-walk_origin.x)<1 and abs(restored.y-walk_origin.y)<1 and abs(restored.z-walk_origin.z)<=move.max_step_height
results['tests'].append({'test':'compiled ToggleFlight restores walking XY and snaps capsule to floor within step height','passed':True,'saved_cm':vec(walk_origin),'restored_cm':vec(restored)})
pc.set_editor_property('show_mouse_cursor',False)
clock={'start':time.perf_counter(),'last':None,'frames':[],'phase':0,'phase_start':time.perf_counter(),'start_pos':pawn.get_actor_location()}
holder=[None]
def tick(dt):
    try:
        now=time.perf_counter()
        if clock['last'] is not None:clock['frames'].append(now-clock['last'])
        clock['last']=now
        elapsed=now-clock['phase_start']
        if clock['phase']==0:
            pawn.add_movement_input(unreal.Vector(0,-1,0),1.0,False)
            if elapsed>=2:
                distance=(pawn.get_actor_location()-clock['start_pos']).length()
                results['tests'].append({'test':'character movement and ground collision for two seconds','passed':distance>250 and move.movement_mode==unreal.MovementMode.MOVE_WALKING,'travel_cm':distance,'end':state()})
                clock['phase']=1;clock['phase_start']=now
        elif elapsed>=3:
            results['final']=state();results['slate_tick_median_ms']=statistics.median(clock['frames'])*1000
            results['slate_tick_note']='Editor Slate tick interval, not a standalone GPU benchmark.'
            results['complete']=True
            results['passed']=all(x['passed'] for x in results['tests'])
            unreal.unregister_slate_post_tick_callback(holder[0])
        dest.write_text(json.dumps(results,indent=2))
    except Exception:
        results['error']=traceback.format_exc();dest.write_text(json.dumps(results,indent=2))
        unreal.unregister_slate_post_tick_callback(holder[0])
holder[0]=unreal.register_slate_post_tick_callback(tick)
