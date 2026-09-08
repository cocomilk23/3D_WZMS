import unreal,json
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as BP
bp=unreal.EditorAssetLibrary.load_asset('/Game/WZMS/Blueprints/BP_WZMS_Explorer');graph=BP.get_graph(bp,'EventGraph')
report={'input_mode_nodes':list(BP.find_node_types(graph,'SetInputModeGameOnly')),'nodes':[]}
for node in BP.find_nodes(graph):
    info=BP.get_node_infos([node])[0]
    if not any(x in info.type_id for x in ['GetInputMouseDelta','InputKey']):continue
    row={'type':info.type_id,'inputs':[(str(p.name),str(p.value)) for p in info.input_pins],'outputs':[(str(p.name),[str(q) for q in p.connected_pins]) for p in info.output_pins]}
    report['nodes'].append(row)
Path(unreal.Paths.project_saved_dir(),'Logs/input_graph_audit.json').write_text(json.dumps(report,indent=2))
