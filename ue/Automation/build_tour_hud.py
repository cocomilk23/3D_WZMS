"""Native, resolution-scaled Chinese sightseeing HUD with map, destinations and pause menu."""
import unreal,json,sys,importlib
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();sys.path.insert(0,str(root.parent/'Automation'))
importlib.reload(importlib.import_module('tour_blueprint_helpers'))
from tour_blueprint_helpers import BP,q,variable,function,node,get,setv,write,compile_save
assets=unreal.EditorAssetLibrary;assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
bp=assets.load_asset('/Game/WZMS/Blueprints/BP_WZMS_TourHUD');assert bp
for name,typ in [('MenuOpen','bool'),('HelpOpen','bool'),('Initialized','bool'),('UIWidth','float'),('UIHeight','float'),('UIScale','float'),('UIOriginX','float'),('UIOriginY','float'),('HoverName','name'),('NearestPlace','string'),('NearestDistance','float'),('HUDQuality','int'),('HUDVolume','float'),('PlayerX','float'),('PlayerY','float')]:variable(bp,name,typ)
compile_save(bp);cdo=unreal.get_default_object(bp.generated_class())
for name,value in [('MenuOpen',True),('HelpOpen',False),('Initialized',False),('UIScale',1),('HUDQuality',3),('HUDVolume',.65),('NearestPlace','南大门')]:cdo.set_editor_property(name,value)
compile_save(bp);destinations=json.loads((root.parent/'SourceReference/tour_destinations.json').read_text(encoding='utf8'))['destinations'];font='/Game/WZMS/Tour/UI/F_Tour_Chinese_Font.F_Tour_Chinese_Font';assert assets.load_asset(font)
font_asset=assets.load_asset(font);font_asset.set_editor_property('legacy_font_size',48);assets.save_loaded_asset(font_asset)
codes=[]
color_types=[t for t in BP.find_node_types(BP.get_graph(bp,'EventGraph'),'Color') if t.endswith('|MakeLinearColor')];assert color_types
make_color=color_types[0]
def install(name,params,body):
 g=function(bp,name,params);code='(fn '+name+' ('+' '.join(p[0] for p in params if p[2])+')\n'+body+'\n)';codes.append(code)
 if not globals().get('TOUR_HUD_EVENTS_ONLY',False) and name in globals().get('TOUR_HUD_FUNCTIONS',{name}):
  print('BUILD HUD',name,flush=True);write(g,code);compile_save(bp)
 return g
def color(r,g,b,a=1):return f'({make_color} :R {r} :G {g} :B {b} :A {a})'
cream=color(.94,.96,.93);muted=color(.55,.66,.62);accent=color(.39,.77,.62);orange=color(1,.65,.26);dark=color(.035,.075,.065,.97)
def tx(x):return f'(+ {get("UIOriginX")} (* {x} {get("UIScale")}))'
def ty(y):return f'(+ {get("UIOriginY")} (* {y} {get("UIScale")}))'
def scale(v):return f'(* {v} {get("UIScale")})'
def rect(x,y,w,h,col):return f'(HUD|DrawRect :RectColor {col} :ScreenX {x} :ScreenY {y} :ScreenW {w} :ScreenH {h})'
def text(value,x,y,size=18,col=cream):return f'({draw_label} :Label {value} :X {x} :Y {y} :Size {size} :TextColor {col})'
def box(name,x,y,w,h):return f'(HUD|AddHitBox :Position (Math|Vector2D|MakeVector2D {x} {y}) :Size (Math|Vector2D|MakeVector2D {w} {h}) :InName {q(name)} :bConsumesInput true :Priority 1)'

label_params=[('Label','string',True),('X','float',True),('Y','float',True),('Size','float',True),('TextColor','LinearColor',True)]
g=function(bp,'DrawTourLabel',label_params)
install('DrawTourLabel',label_params,f'(HUD|DrawText :Text Label :TextColor TextColor :ScreenX X :ScreenY Y :Font {q(font)} :Scale (* (/ Size 64.0) {get("UIScale")}))')
draw_label=node(g,'DrawTourLabel')
def button(name,label,x,y,w,h=32,selected=None):
 return f'({draw_button} :ButtonName {q(name)} :Label {label} :X {x} :Y {y} :W {w} :H {h} :Selected {selected or "false"})'

button_params=[('ButtonName','name',True),('Label','string',True)]+[(n,'float',True) for n in ['X','Y','W','H']]+[('Selected','bool',True)]
g=function(bp,'DrawTourButton',button_params)
bg=f'(select (or (== {get("HoverName")} ButtonName) Selected) {color(.12,.28,.23,.98)} {color(.065,.13,.11,.98)})'
install('DrawTourButton',button_params,'\n'.join([rect(tx('X'),ty('Y'),scale('W'),scale('H'),bg),text('Label',tx('(+ X 10)'),ty('(+ Y 5)'),16),f'(HUD|AddHitBox :Position (Math|Vector2D|MakeVector2D {tx("X")} {ty("Y")}) :Size (Math|Vector2D|MakeVector2D {scale("W")} {scale("H")}) :InName ButtonName :bConsumesInput true :Priority 1)']))
draw_button=node(g,'DrawTourButton')
dot_params=[(n,'float',True) for n in ['X','Y','Side','U','V','Span','DotU','DotV']]+[('Label','string',True),('ClickName','name',True),('Labels','bool',True),('Major','bool',True)]
g=function(bp,'DrawTourMapDot',dot_params)
install('DrawTourMapDot',dot_params,f'''(bind dx (/ (- DotU U) Span)) (bind dy (/ (- DotV V) Span))
 (if (and (and (> dx 0.02) (< dx 0.98)) (and (> dy 0.02) (< dy 0.98)))
  (bind px (+ X (* dx Side))) (bind py (+ Y (* dy Side)))
  {rect('(- px 3)','(- py 3)','6','6',cream)}
  (if (and Labels Major) {text('Label','(+ px 5)','(- py 6)',11,color(1,1,1))})
  (if Labels (HUD|AddHitBox :Position (Math|Vector2D|MakeVector2D (- px 7) (- py 7)) :Size (Math|Vector2D|MakeVector2D 14 14) :InName ClickName :bConsumesInput true :Priority 1)))''')
draw_dot=node(g,'DrawTourMapDot')
place_params=[('X','float',True),('Y','float',True),('Label','string',True)]
g=function(bp,'ConsiderTourPlace',place_params)
install('ConsiderTourPlace',place_params,f'''(bind dx (- {get('PlayerX')} X)) (bind dy (- {get('PlayerY')} Y))
 (bind distance (+ (* dx dx) (* dy dy)))
 (if (< distance {get('NearestDistance')}) {setv('NearestDistance','distance')} {setv('NearestPlace','Label')})''')
consider_place=node(g,'ConsiderTourPlace')
g=function(bp,'SetTourMenu',[('Open','bool',True)]);cast=node(g,'CastToBP_WZMS_Explorer');setstate=node(g,'SetTourMenuState');savefn=node(g,'SaveTourProgress')
install('SetTourMenu',[('Open','bool',True)],f'''{setv('MenuOpen','Open')} {setv('HelpOpen','false')}
 (bind pc (Game|GetPlayerController 0))
 (Class|PlayerController|SetShowMouseCursor :self pc :bShowMouseCursor Open)
 (Class|PlayerController|SetEnableClickEvents :self pc :bEnableClickEvents Open)
 (Class|PlayerController|SetEnableMouseOverEvents :self pc :bEnableMouseOverEvents Open)
 (if Open
  (Input|SetInputModeGameAndUI :PlayerController pc :InMouseLockMode "DoNotLock" :bHideCursorDuringCapture false)
  (else (Input|SetInputModeGameOnly :PlayerController pc)))
 (Game|SetGamePaused :bPaused Open)
 (bind explorer ({cast} :Object (Game|GetPlayerPawn 0))
  (:then ({setstate} :self explorer :Open Open) ({savefn} :self explorer)) (:CastFailed))''')
g=function(bp,'ToggleTourMenu');install('ToggleTourMenu',[],f'({node(g,"SetTourMenu")} :Open (not {get("MenuOpen")}))')
g=function(bp,'VisitTourPlace',[('Index','int',True)]);cast=node(g,'CastToBP_WZMS_Explorer')
install('VisitTourPlace',[('Index','int',True)],f'''(bind explorer ({cast} :Object (Game|GetPlayerPawn 0))
 (:then ({node(g,'TravelToTourPlace')} :self explorer :Index Index) ({node(g,'SetTourMenu')} :Open false)) (:CastFailed))''')
g=function(bp,'SelectTourQuality',[('Quality','int',True)]);cast=node(g,'CastToBP_WZMS_Explorer')
install('SelectTourQuality',[('Quality','int',True)],f'''{setv('HUDQuality','Quality')}
 (bind explorer ({cast} :Object (Game|GetPlayerPawn 0))
 (:then ({node(g,'ApplyTourQuality')} :self explorer :Quality Quality) ({node(g,'SaveTourProgress')} :self explorer)) (:CastFailed))''')
g=function(bp,'CycleTourVolume');cast=node(g,'CastToBP_WZMS_Explorer')
next_volume=f'(select (< {get("HUDVolume")} 0.1) 0.35 (select (< {get("HUDVolume")} 0.5) 0.65 (select (< {get("HUDVolume")} 0.9) 1.0 0.0)))'
install('CycleTourVolume',[],f'''{setv('HUDVolume',next_volume)}
 (bind explorer ({cast} :Object (Game|GetPlayerPawn 0))
 (:then ({node(g,'ApplyTourSoundLevel')} :self explorer :Volume {get('HUDVolume')}) ({node(g,'SaveTourProgress')} :self explorer)) (:CastFailed))''')
g=function(bp,'InitializeTourHUD');cast=node(g,'CastToBP_WZMS_Explorer')
install('InitializeTourHUD',[],f'''(bind explorer ({cast} :Object (Game|GetPlayerPawn 0))
 (:then ({node(g,'RestoreTourSafePosition')} :self explorer) {setv('HUDQuality','('+node(g,'GetTourQuality')+' :self explorer)')} {setv('HUDVolume','('+node(g,'ReadTourSoundLevel')+' :self explorer)')} {setv('Initialized','true')} ({node(g,'SetTourMenu')} :Open true)) (:CastFailed))''')
# DrawMap is called only within ReceiveDrawHUD while Canvas is valid.
params=[(n,'float',True) for n in ['X','Y','Side','U','V','Span']]+[('Labels','bool',True)]
g=function(bp,'DrawTourMap',params)
body=['(HUD|DrawTexture :Texture "/Game/WZMS/Tour/UI/T_Tour_CampusMap.T_Tour_CampusMap" :ScreenX X :ScreenY Y :ScreenW Side :ScreenH Side :TextureU U :TextureV V :TextureUWidth Span :TextureVHeight Span :BlendMode "BLEND_Opaque")']
major={0,2,12,13,14,16,18,20,21}
for p in destinations:
 u,v=p['map_uv'];body.append(f'({draw_dot} :X X :Y Y :Side Side :U U :V V :Span Span :DotU {u} :DotV {v} :Label {q(p["name"])} :ClickName {q("POI%02d"%p["index"])} :Labels Labels :Major {str(p["index"] in major).lower()})')
body.extend(['(bind pawn (Game|GetPlayerPawn 0))','(bind pos (Transformation|GetActorLocation :self pawn))','(bind direction (Transformation|GetActorForwardVector :self pawn))','(bind px (+ X (* (/ (- (/ (+ (.x pos) 20000) 62000) U) Span) Side)))','(bind py (+ Y (* (/ (- (/ (+ (.y pos) 49500) 62000) V) Span) Side)))'])
tipx='(+ px (* (.x direction) 10))';tipy='(+ py (* (.y direction) 10))';leftx='(- (- px (* (.x direction) 7)) (* (.y direction) 6))';lefty='(+ (- py (* (.y direction) 7)) (* (.x direction) 6))';rightx='(+ (- px (* (.x direction) 7)) (* (.y direction) 6))';righty='(- (- py (* (.y direction) 7)) (* (.x direction) 6))'
for x1,y1,x2,y2 in [(tipx,tipy,leftx,lefty),(tipx,tipy,rightx,righty),(leftx,lefty,rightx,righty)]:body.append(f'(HUD|DrawLine :StartScreenX {x1} :StartScreenY {y1} :EndScreenX {x2} :EndScreenY {y2} :LineColor {orange} :LineThickness 2.5)')
install('DrawTourMap',params,'\n'.join(body))
g=function(bp,'DrawTourMenu');drawmap=node(g,'DrawTourMap');body=[rect('0','0',get('UIWidth'),get('UIHeight'),color(0,0,0,.55)),rect(tx(36),ty(48),scale(1208),scale(628),dark),text(q('温州中学'),tx(64),ty(70),30),text(q('校园漫游'),tx(222),ty(80),16,muted),text(q('选择一个地点，开始自由游览'),tx(64),ty(114),17,muted)]
cards=[]
for p in destinations:
 i=p['index'];cards.append(button('POI%02d'%i,q(f'{i+1:02d}  '+p['name']),64+(i//12)*304,148+(i%12)*33,288,28))
cards.append(f'({drawmap} :X {tx(704)} :Y {ty(136)} :Side {scale(488)} :U 0 :V 0 :Span 1 :Labels true)')
cards.append(text(q('北 ↑'),tx(1150),ty(108),16,accent));cards.append(text(q('点击地图上的地点也可直接到达'),tx(704),ty(632),14,muted))
helplines=[('自由游览',[('W / A / S / D','前后左右移动'),('鼠标','环顾四周'),('Shift','加快行走'),('空格','跳跃'),('M / Esc','打开或关闭校园地图')]),('观赏与安全',[('Tab','切换航拍；再次按下回到起飞处'),('Q / E','航拍时下降 / 上升'),('R','回到最近安全位置'),('自动存档','行走时定期保存，也会在离开菜单时保存'),('水域','仅作为环境；请通过桥梁游览各岛屿')])]
helpbody=[text(q('操作说明'),tx(704),ty(110),24)]
for col,(title,lines) in enumerate(helplines):
 x=64+col*580;helpbody.append(text(q(title),tx(x),ty(168),22,accent))
 for j,(key,desc) in enumerate(lines):
  helpbody.extend([text(q(key),tx(x),ty(216+j*62),17),text(q(desc),tx(x),ty(239+j*62),15,muted)])
body.append(f'(if {get("HelpOpen")} '+'\n'.join(helpbody)+' (else '+'\n'.join(cards)+'))')
body.append(text(q('画质'),tx(64),ty(558),15,muted))
for level,label,x in [(1,'流畅',114),(2,'均衡',218),(3,'精致',322)]:body.append(button('Quality'+str(level),q(label),x,552,96,30,f'(== {get("HUDQuality")} {level})'))
volume_label=f'(select (< {get("HUDVolume")} 0.1) "声音：关闭" (select (< {get("HUDVolume")} 0.5) "声音：轻柔" (select (< {get("HUDVolume")} 0.9) "声音：适中" "声音：完整")))'
body.extend([button('Volume',volume_label,432,552,160,30),button('Continue',q('继续游览'),64,614,176,38),button('Help',f'(select {get("HelpOpen")} "返回地图" "操作说明")',256,614,176,38),button('Exit',q('保存并退出'),448,614,176,38)])
install('DrawTourMenu',[],'\n'.join(body))
g=function(bp,'DrawTourMinimap');drawmap=node(g,'DrawTourMap')
body=['(bind pawn (Game|GetPlayerPawn 0))','(bind pos (Transformation|GetActorLocation :self pawn))',f'(bind x (- {get("UIWidth")} {scale(276)}))',f'(bind y {scale(24)})','(bind rawu (- (/ (+ (.x pos) 20000) 62000) 0.14516129))','(bind rawv (- (/ (+ (.y pos) 49500) 62000) 0.14516129))','(bind u (select (< rawu 0.0) 0.0 (select (> rawu 0.70967742) 0.70967742 rawu)))','(bind v (select (< rawv 0.0) 0.0 (select (> rawv 0.70967742) 0.70967742 rawv)))',rect('x','y',scale(252),scale(292),dark),f'({drawmap} :X (+ x {scale(6)}) :Y (+ y {scale(6)}) :Side {scale(240)} :U u :V v :Span 0.29032258 :Labels false)',text(get('NearestPlace'),f'(+ x {scale(10)})',f'(+ y {scale(250)})',16),text(q('M 地图'),f'(+ x {scale(174)})',f'(+ y {scale(250)})',14,muted),text(q('北 ↑'),f'(+ x {scale(208)})',f'(+ y {scale(10)})',13,cream),rect(f'(- (/ {get("UIWidth")} 2) 1)',f'(- (/ {get("UIHeight")} 2) 1)','2','2',color(1,1,1,.55)),text(q('WASD 行走   ·   Tab 航拍   ·   M 校园地图'),scale(24),f'(- {get("UIHeight")} {scale(32)})',14,muted)]
install('DrawTourMinimap',[],'\n'.join(body))
event=BP.get_graph(bp,'EventGraph');toggle=node(event,'ToggleTourMenu');visit=node(event,'VisitTourPlace');setmenu=node(event,'SetTourMenu');selectquality=node(event,'SelectTourQuality');cyclevolume=node(event,'CycleTourVolume');cast=node(event,'CastToBP_WZMS_Explorer');savefn=node(event,'SaveTourProgress')
draw=[setv('UIWidth','SizeX'),setv('UIHeight','SizeY'),setv('UIScale','(select (< (/ SizeX 1280.0) (/ SizeY 720.0)) (/ SizeX 1280.0) (/ SizeY 720.0))'),setv('UIOriginX','(/ (- SizeX (* 1280 '+get('UIScale')+')) 2)'),setv('UIOriginY','(/ (- SizeY (* 720 '+get('UIScale')+')) 2)'),f'(if (not {get("Initialized")}) ({node(event,"InitializeTourHUD")}))','(bind pc (Game|GetPlayerController 0))',f'(if (or (Game|Player|WasInputKeyJustPressed :self pc :Key "M") (Game|Player|WasInputKeyJustPressed :self pc :Key "Escape")) ({toggle}))','(bind pos (Transformation|GetActorLocation :self (Game|GetPlayerPawn 0)))',setv('NearestDistance','100000000000')]
draw.extend([setv('PlayerX','(.x pos)'),setv('PlayerY','(.y pos)')])
for p in destinations:
 x,y,_=p['position_cm'];draw.append(f'({consider_place} :X {x} :Y {y} :Label {q(p["name"])})')
draw.append(f'(if {get("MenuOpen")} ({node(event,"DrawTourMenu")}) (else ({node(event,"DrawTourMinimap")})))')
actions=[('POI%02d'%p['index'],f'({visit} :Index {p["index"]})') for p in destinations]+[('Continue',f'({setmenu} :Open false)'),('Help',setv('HelpOpen','(not '+get('HelpOpen')+')')),('Volume',f'({cyclevolume})')]+[('Quality'+str(i),f'({selectquality} :Quality {i})') for i in [1,2,3]]+[('Exit',f'''(bind explorer ({cast} :Object (Game|GetPlayerPawn 0))
 (:then ({savefn} :self explorer) (Game|QuitGame :SpecificPlayer (Game|GetPlayerController 0) :QuitPreference "Quit")) (:CastFailed))''')]
# The toolset currently fails to rename SwitchOnName exec pins. Explicit equality branches preserve the actual hit-box names.
click=[f'(if (== BoxName {q(name)}) {action})' for name,action in actions]
code='(event EventReceiveDrawHUD (SizeX SizeY)\n'+'\n'.join(draw)+')\n(event EventHitBoxClicked (BoxName)\n'+'\n'.join(click)+')\n(event EventHitBoxBeginCursorOver (BoxName) '+setv('HoverName','BoxName')+')\n(event EventHitBoxEndCursorOver (BoxName) '+setv('HoverName',q('None'))+')'
write(event,code);codes.append(code);compile_save(bp)
gm=assets.load_asset('/Game/WZMS/Blueprints/BP_WZMS_GameMode');unreal.get_default_object(gm.generated_class()).set_editor_property('hud_class',bp.generated_class());compile_save(gm)
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
(root.parent/'Reports/tour_hud_graph.dsl').write_text('\n\n'.join(codes),encoding='utf8')
(root.parent/'Reports/tour_hud_build.json').write_text(json.dumps({'compiled':True,'map':'Fixed orthographic campus texture; dynamic UV crop and position/orientation arrow','destinations':len(destinations),'language':'Chinese','font':font,'font_source':'SourceFonts/NotoSansSC/OFL.txt','runtime_validation_pending':True},indent=2),encoding='utf8')
