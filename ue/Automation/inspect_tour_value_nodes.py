import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as BP
root=Path(unreal.Paths.project_dir()).resolve()
bp=unreal.EditorAssetLibrary.load_asset('/Game/WZMS/Blueprints/BP_WZMS_TourHUD');g=BP.get_graph(bp,'EventGraph')
types=[t for needle in ['Color','Rotator'] for t in BP.find_node_types(g,needle) if t.endswith('|MakeLinearColor') or t.endswith('|MakeColor') or t.endswith('|MakeRotator')]
r={t:BP.get_node_type_pins(g,t) for t in types}
(root/'Saved/Logs/tour_value_nodes.json').write_text(json.dumps(r,default=str,indent=2),encoding='utf8')
