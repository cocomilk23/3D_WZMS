"""Create native save data and extend the accepted first-person explorer for touring."""
import unreal,json,sys,importlib
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();sys.path.insert(0,str(root.parent/'Automation'))
importlib.reload(importlib.import_module('tour_blueprint_helpers'))
from tour_blueprint_helpers import BP,q,variable,function,node,get,setv,write,compile_save
assets=unreal.EditorAssetLibrary;assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
save=assets.load_asset('/Game/WZMS/Blueprints/BP_WZMS_TourSave') or BP.create('/Game/WZMS/Blueprints','BP_WZMS_TourSave',unreal.SaveGame.static_class())
for n,t in [('SavedPosition','Vector'),('SavedRotation','Rotator'),('SavedQuality','int'),('SavedVolume','float'),('SavedVersion','int')]:variable(save,n,t)
compile_save(save)
bp=assets.load_asset('/Game/WZMS/Blueprints/BP_WZMS_Explorer');assert bp
for n,t in [('TourMenuOpen','bool'),('SafePosition','Vector'),('SafeRotation','Rotator'),('QualityPreset','int'),('TourVolume','float'),('TourSaveClock','float'),('HasSavedVisit','bool'),('SaveSucceeded','bool')]:variable(bp,n,t)
compile_save(bp)
defaults=unreal.get_default_object(bp.generated_class())
for n,v in [('TourMenuOpen',True),('SafePosition',unreal.Vector(-1450,3000,120)),('SafeRotation',unreal.Rotator(pitch=0,yaw=-90,roll=0)),('QualityPreset',3),('TourVolume',.65),('TourSaveClock',0),('HasSavedVisit',False),('SaveSucceeded',True)]:defaults.set_editor_property(n,v)
compile_save(bp)
codes=[]
def install(name,params,body):
 g=function(bp,name,params);code='(fn '+name+' ('+' '.join(p[0] for p in params if p[2])+')\n'+body+'\n)';codes.append(code)
 if name in globals().get('TOUR_EXPLORER_FUNCTIONS',{name}):write(g,code);compile_save(bp)
 return g
g=function(bp,'SaveTourProgress')
save_cast=node(g,'CastToBP_WZMS_TourSave')
assignments='\n'.join('('+node(g,'Set'+dst)+' :self saved :'+dst+' '+value+')' for dst,value in [('SavedPosition',get('SafePosition')),('SavedRotation',get('SafeRotation')),('SavedQuality',get('QualityPreset')),('SavedVolume',get('TourVolume')),('SavedVersion','1')])
install('SaveTourProgress',[],f'''(bind object (SaveGame|CreateSaveGameObject :SaveGameClass "/Game/WZMS/Blueprints/BP_WZMS_TourSave.BP_WZMS_TourSave_C"))
 (bind saved ({save_cast} :Object object)
  (:then {assignments}
   (bind success (SaveGame|SaveGametoSlot :SaveGameObject saved :SlotName "WZMS_CampusTour" :UserIndex 0))
   {setv('SaveSucceeded','success')}
   (if success {setv('HasSavedVisit','true')}))
  (:CastFailed {setv('SaveSucceeded','false')}))''')
g=function(bp,'RestoreTourSafePosition');rotate=node(g,'SetControlRotation')
install('RestoreTourSafePosition',[],f'''{setv('Flying','false')}
 (Pawn|Components|CharacterMovement|SetMovementMode :self (Variables|Character|GetCharacterMovement) :NewMovementMode "MOVE_Walking")
 (Transformation|SetActorLocation :NewLocation {get('SafePosition')} :bTeleport true)
 ({rotate} :self (Game|GetPlayerController 0) :NewRotation {get('SafeRotation')})
 {setv('LastWalkPosition',get('SafePosition'))}''')
g=function(bp,'ApplyTourQuality',[('Quality','int',True)])
install('ApplyTourQuality',[('Quality','int',True)],f'''{setv('QualityPreset','Quality')}
 (bind settings (Settings|GetGameUserSettings))
   (Settings|SetOverallScalabilityLevel :self settings :Value Quality)
   (Settings|SetResolutionScaleValue :self settings :NewScaleValue 100)
 (Settings|ApplySettings :self settings :bCheckForCommandLineOverrides false)
 (Settings|SaveSettings :self settings)''')
g=function(bp,'ApplyTourSoundLevel',[('Volume','float',True)]);mixoverride=node(g,'SetSoundMixClassOverride')
install('ApplyTourSoundLevel',[('Volume','float',True)],setv('TourVolume','Volume')+f'''\n({mixoverride} :InSoundMixModifier "/Game/WZMS/Tour/Audio/Mix_Tour.Mix_Tour" :InSoundClass "/Game/WZMS/Tour/Audio/SC_Tour.SC_Tour" :Volume Volume :Pitch 1 :FadeInTime 0.25 :bApplyToChildren true)''')
install('SetTourMenuState',[('Open','bool',True)],f'''{setv('TourMenuOpen','Open')}
 (if Open ({node(function(bp,'SetTourMenuState'),'StopMovementImmediately')} :self (Variables|Character|GetCharacterMovement)))''')
for name,var,typ in [('GetTourQuality','QualityPreset','int'),('ReadTourSoundLevel','TourVolume','float'),('GetTourSaveSucceeded','SaveSucceeded','bool'),('GetHasSavedVisit','HasSavedVisit','bool')]:install(name,[('Value',typ,False)],'(return '+get(var)+')')
g=function(bp,'InitializeTour');cast=node(g,'CastToBP_WZMS_TourSave');quality=node(g,'ApplyTourQuality');restore=node(g,'RestoreTourSafePosition')
read=lambda name:'('+node(g,'GetSaved'+name)+' :self saved)'
valid='(and (== '+read('Version')+' 1) (and (> (.z '+read('Position')+') -20) (< (.z '+read('Position')+') 2000)))'
install('InitializeTour',[],f'''({node(g,'PushSoundMixModifier')} :InSoundMixModifier "/Game/WZMS/Tour/Audio/Mix_Tour.Mix_Tour")
 (bind object (SaveGame|LoadGamefromSlot :SlotName "WZMS_CampusTour" :UserIndex 0))
 (bind saved ({cast} :Object object)
  (:then
   (if {valid}
    {setv('SafePosition',read('Position'))} {setv('SafeRotation',read('Rotation'))}
    {setv('QualityPreset',read('Quality'))} {setv('TourVolume',read('Volume'))} {setv('HasSavedVisit','true')})
   ({quality} :Quality {get('QualityPreset')}) ({node(g,'ApplyTourSoundLevel')} :Volume {get('TourVolume')}) ({restore}))
  (:CastFailed ({quality} :Quality {get('QualityPreset')}) ({node(g,'ApplyTourSoundLevel')} :Volume {get('TourVolume')}) ({restore})))''')
g=function(bp,'TravelToTourPlace',[('Index','int',True)]);destinations=json.loads((root.parent/'SourceReference/tour_destinations.json').read_text(encoding='utf8'))['destinations'];branches=[]
for p in destinations:
 x,y,z=p['position_cm'];branches.append(f'''(:{p['index']} {setv('SafePosition',f'(Math|Vector|MakeVector {x} {y} {z})')} {setv('SafeRotation',f"(Math|Rotator|MakeRotator :Roll 0 :Pitch 0 :Yaw {p['yaw_ue']})")} ({node(g,'RestoreTourSafePosition')}) ({node(g,'SaveTourProgress')}))''')
install('TravelToTourPlace',[('Index','int',True)],'(switch int Index\n'+'\n'.join(branches)+')')
event=BP.get_graph(bp,'EventGraph');toggle=node(event,'ToggleFlight');restore=node(event,'RestoreTourSafePosition');savefn=node(event,'SaveTourProgress');walking=node(event,'IsMovingOnGround');init=node(event,'InitializeTour')
code=f'''(event EventBeginPlay ({init}))
(event EventEndPlay (EndPlayReason) ({savefn}))
(event EventTick (DeltaSeconds)
 (if (not {get('TourMenuOpen')})
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
  (if {get('Flying')}
   (Pawn|Input|AddMovementInput :WorldDirection (Math|Vector|GetForwardVector (Pawn|GetControlRotation :self pc)) :ScaleValue forward)
   (Pawn|Input|AddMovementInput :WorldDirection (Math|Vector|MakeVector 0 0 1) :ScaleValue (- (select (Game|Player|IsInputKeyDown :self pc :Key "E") 1.0 0.0) (select (Game|Player|IsInputKeyDown :self pc :Key "Q") 1.0 0.0)))
   (else (Pawn|Input|AddMovementInput :WorldDirection (Transformation|GetActorForwardVector) :ScaleValue forward)))
  (Pawn|Input|AddMovementInput :WorldDirection (Transformation|GetActorRightVector) :ScaleValue right)
  (if (Game|Player|WasInputKeyJustPressed :self pc :Key "Tab") ({toggle}))
  (if (Game|Player|WasInputKeyJustPressed :self pc :Key "SpaceBar") (Character|Jump))
  (if (or (Game|Player|WasInputKeyJustPressed :self pc :Key "R") (< (.z (Transformation|GetActorLocation)) -500.0)) ({restore}))
  (if (and (not {get('Flying')}) ({walking} :self movement))
   {setv('SafePosition','(Transformation|GetActorLocation)')}
   {setv('SafeRotation','(Pawn|GetControlRotation :self pc)')})
  {setv('TourSaveClock','(+ '+get('TourSaveClock')+' DeltaSeconds)')}
  (if (> {get('TourSaveClock')} 10) {setv('TourSaveClock','0')} ({savefn}))))'''
write(event,code);codes.append(code);compile_save(bp)
(root.parent/'Reports/tour_explorer_graph.dsl').write_text('\n\n'.join(codes),encoding='utf8')
(root.parent/'Reports/tour_explorer_build.json').write_text(json.dumps({'compiled':True,'save_slot':'WZMS_CampusTour','save_version':1,'destinations':len(destinations),'autosave_seconds':10,'default_quality':3,'volume_sound_mix':'/Game/WZMS/Tour/Audio/Mix_Tour','runtime_validation_pending':True},indent=2),encoding='utf8')
