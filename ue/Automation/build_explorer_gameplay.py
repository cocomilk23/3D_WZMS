import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as BP
ROOT=Path(unreal.Paths.project_dir()).resolve();assets=unreal.EditorAssetLibrary
bp=assets.load_asset('/Game/WZMS/Blueprints/BP_WZMS_Explorer');assert bp
toggle=BP.add_function_graph(bp,'ToggleFlight')
toggle_code='''(fn ToggleFlight ()
 (bind movement (Variables|Character|GetCharacterMovement))
 (if (Variables|Default|GetFlying)
  (Variables|Default|SetFlying false)
  (Transformation|SetActorLocation :NewLocation (Variables|Default|GetLastWalkPosition) :bTeleport true)
  (Pawn|Components|CharacterMovement|SetMovementMode :self movement :NewMovementMode "MOVE_Walking")
  (else
   (Variables|Default|SetLastWalkPosition (Transformation|GetActorLocation))
   (Variables|Default|SetFlying true)
   (Pawn|Components|CharacterMovement|SetMovementMode :self movement :NewMovementMode "MOVE_Flying"))))'''
BP.write_graph_dsl(toggle,toggle_code)
reset=BP.add_function_graph(bp,'ReturnToGate')
reset_code='''(fn ReturnToGate ()
 (Variables|Default|SetFlying false)
 (Transformation|SetActorLocation :NewLocation (Math|Vector|MakeVector -1450 3000 120) :bTeleport true)
 (Pawn|Components|CharacterMovement|SetMovementMode :self (Variables|Character|GetCharacterMovement) :NewMovementMode "MOVE_Walking"))'''
BP.write_graph_dsl(reset,reset_code)
BP.compile_blueprint(bp)
event=BP.get_graph(bp,'EventGraph')
types=BP.find_node_types(event,'')
def function(name):
    candidates=[t for t in types if t.lower().endswith('|'+name.lower())]
    assert len(candidates)==1,(name,candidates)
    return candidates[0]
toggle_node=function('ToggleFlight');reset_node=function('ReturnToGate')
tick_code=f'''(event EventBeginPlay
 (Input|SetInputModeGameOnly (Game|GetPlayerController 0)))
(event EventTick (DeltaSeconds)
 (bind pc (Game|GetPlayerController 0))
 (bind movement (Variables|Character|GetCharacterMovement))
 (bind (mx my) (Game|Player|GetInputMouseDelta :self pc))
 (Pawn|Input|AddControllerYawInput :Val (* mx 0.7))
 (Pawn|Input|AddControllerPitchInput :Val (* my -0.7))
 (bind forward (- (select (Game|Player|IsInputKeyDown :self pc :Key "W") 1.0 0.0) (select (Game|Player|IsInputKeyDown :self pc :Key "S") 1.0 0.0)))
 (bind right (- (select (Game|Player|IsInputKeyDown :self pc :Key "D") 1.0 0.0) (select (Game|Player|IsInputKeyDown :self pc :Key "A") 1.0 0.0)))
 (bind fast (Game|Player|IsInputKeyDown :self pc :Key "LeftShift"))
 (Class|CharacterMovementComponent|SetMaxWalkSpeed :self movement :MaxWalkSpeed (select fast 750.0 420.0))
 (Class|CharacterMovementComponent|SetMaxFlySpeed :self movement :MaxFlySpeed (select fast 5000.0 1800.0))
 (if (Variables|Default|GetFlying)
  (Pawn|Input|AddMovementInput :WorldDirection (Math|Vector|GetForwardVector (Pawn|GetControlRotation :self pc)) :ScaleValue forward)
  (Pawn|Input|AddMovementInput :WorldDirection (Math|Vector|MakeVector 0 0 1) :ScaleValue (- (select (Game|Player|IsInputKeyDown :self pc :Key "E") 1.0 0.0) (select (Game|Player|IsInputKeyDown :self pc :Key "Q") 1.0 0.0)))
  (else (Pawn|Input|AddMovementInput :WorldDirection (Transformation|GetActorForwardVector) :ScaleValue forward)))
 (Pawn|Input|AddMovementInput :WorldDirection (Transformation|GetActorRightVector) :ScaleValue right)
 (if (Game|Player|WasInputKeyJustPressed :self pc :Key "Tab") ({toggle_node}))
 (if (Game|Player|WasInputKeyJustPressed :self pc :Key "SpaceBar") (Character|Jump))
 (if (or (Game|Player|WasInputKeyJustPressed :self pc :Key "R") (< (.z (Transformation|GetActorLocation)) -500.0)) ({reset_node})))'''
BP.write_graph_dsl(event,tick_code)
BP.compile_blueprint(bp)
gm=assets.load_asset('/Game/WZMS/Blueprints/BP_WZMS_GameMode') or BP.create('/Game/WZMS/Blueprints','BP_WZMS_GameMode',unreal.GameModeBase.static_class())
unreal.BlueprintEditorLibrary.compile_blueprint(gm)
unreal.get_default_object(gm.generated_class()).set_editor_property('default_pawn_class',bp.generated_class())
unreal.BlueprintEditorLibrary.compile_blueprint(gm)
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
world.get_world_settings().set_editor_property('default_game_mode',gm.generated_class())
for item in [bp,gm]:assets.save_loaded_asset(item)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
(ROOT.parent/'Reports/explorer_blueprint.json').write_text(json.dumps({'compiled':True,'pawn':bp.get_path_name(),'game_mode':gm.get_path_name(),'capsule_cm':{'radius':30,'half_height':90},'eye_above_capsule_centre_cm':80,'walk_speed_cm_s':420,'fly_speed_cm_s':1800,'controls':{'WASD':'move','mouse':'look','Tab':'flight / return to last walking position','E/Q':'ascend / descend in flight','Shift':'faster','Space':'jump','R':'return to gate'},'runtime_tested':False},indent=2),encoding='utf8')
(ROOT.parent/'Reports/explorer_graph.dsl').write_text(toggle_code+'\n'+reset_code+'\n'+tick_code,encoding='utf8')
