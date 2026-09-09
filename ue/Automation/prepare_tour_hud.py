"""Prepare a native Blueprint HUD and record exact supported node signatures."""
import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as BP
root=Path(unreal.Paths.project_dir()).resolve();assets=unreal.EditorAssetLibrary
bp=assets.load_asset('/Game/WZMS/Blueprints/BP_WZMS_TourHUD') or BP.create('/Game/WZMS/Blueprints','BP_WZMS_TourHUD',unreal.HUD.static_class());graph=BP.get_graph(bp,'EventGraph');types=BP.find_node_types(graph,'')
keys=['DrawText','DrawRect','DrawTexture','DrawLine','DrawMaterial','AddHitBox','ReceiveDrawHUD','ReceiveHitBoxClick','GetOwningPlayerController','GetOwningPawn','GetPlayerPawn','GetHUD','ShowMouseCursor','GetGameUserSettings','SetOverallScalabilityLevel','ApplySettings','SaveSettings','LoadGameFromSlot','SaveGameToSlot','CreateSaveGameObject','GetActorLocation','GetActorRotation','CastToBP_WZMS_Explorer','QuitGame','SetInputModeGameAndUI','SetInputModeGameOnly','GetTextSize','SetGamePaused']
pins={}
for t in types:
 if any(t.lower().endswith(k.lower()) for k in keys):
  try:pins[t]=BP.get_node_type_pins(graph,t)
  except Exception as e:pins[t]=str(e)
(root/'Saved/Logs/tour_hud_pins.json').write_text(json.dumps(pins,indent=2,default=str),encoding='utf8');BP.compile_blueprint(bp);assets.save_loaded_asset(bp)
