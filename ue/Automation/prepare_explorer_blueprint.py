import unreal,json,dataclasses
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as BP
ROOT=Path(unreal.Paths.project_dir()).resolve()
assets=unreal.EditorAssetLibrary
bp=assets.load_asset('/Game/WZMS/Blueprints/BP_WZMS_Explorer') or BP.create('/Game/WZMS/Blueprints','BP_WZMS_Explorer',unreal.Character.static_class())
graph=BP.get_graph(bp,'EventGraph')
varnames=set(BP.list_variables(bp))
for name,type_name in [('Flying','bool'),('LastWalkPosition','Vector')]:
    if name not in varnames:BP.add_variable(bp,name,type_name)
unreal.BlueprintEditorLibrary.compile_blueprint(bp)
cdo=unreal.get_default_object(bp.generated_class())
cdo.set_editor_property('use_controller_rotation_yaw',True)
cdo.set_editor_property('use_controller_rotation_pitch',False)
cdo.get_component_by_class(unreal.CapsuleComponent).set_capsule_size(30,90)
movement=cdo.get_component_by_class(unreal.CharacterMovementComponent)
movement.set_editor_property('max_walk_speed',420)
movement.set_editor_property('max_fly_speed',1800)
movement.set_editor_property('max_step_height',45)
movement.set_editor_property('jump_z_velocity',420)
movement.set_editor_property('air_control',.3)
ss=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
handles=ss.k2_gather_subobject_data_for_blueprint(bp)
camera=None
for h in handles:
    data=unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h)
    obj=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(data)
    if isinstance(obj,unreal.CameraComponent):camera=obj;break
if camera is None:
    h,reason=ss.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=handles[0],new_class=unreal.CameraComponent,blueprint_context=bp))
    if str(reason):raise RuntimeError(str(reason))
    ss.rename_subobject(h,unreal.Text('ExplorerCamera'))
    camera=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h))
camera.set_editor_property('relative_location',unreal.Vector(0,0,80))
camera.set_editor_property('use_pawn_control_rotation',True)
camera.set_editor_property('field_of_view',80)
unreal.BlueprintEditorLibrary.compile_blueprint(bp);assets.save_loaded_asset(bp)
types=BP.find_node_types(graph,'')
keywords=['GetCharacterMovement','GetActorLocation','SetActorLocation','GetInputMouseDelta','WasInputKeyJustPressed','IsInputKeyDown','GetPlayerController','AddControllerYawInput','AddControllerPitchInput','AddMovementInput','SetMovementMode','GetActorForwardVector','GetActorRightVector','GetControlRotation','Math|Vector|GetForwardVector','Math|Vector|GetRightVector','MakeVector','SetMaxWalkSpeed','SetMaxFlySpeed','Flying','LastWalkPosition','Jump','EventTick']
types=[t for t in types if t not in ['Utilities|Casting|CastToCharacterMovementComponent'] and any(t.endswith(k) for k in keywords)]
r={}
for t in types:
    try:r[t]=BP.get_node_type_pins(graph,t)
    except Exception as e:r[t]=str(e)
(ROOT/'Saved/Logs/explorer_pins.json').write_text(json.dumps(r,indent=2,default=str),encoding='utf8')
