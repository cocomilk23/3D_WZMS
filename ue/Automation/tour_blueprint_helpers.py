"""Small helpers for reproducible native Blueprint graph generation."""
import json,unreal,toolset_registry
from editor_toolset.toolsets.blueprint import BlueprintTools as BP
def q(value):return json.dumps(value,ensure_ascii=False)
def variable(bp,name,type_name):
 if name not in BP.list_variables(bp):BP.add_variable(bp,name,type_name)
def function(bp,name,params=()):
 graph=BP.add_function_graph(bp,name)
 for param,type_name,is_input in params:
  if not BP._param_name_exists(graph,param,is_input):
   with toolset_registry.tool_raising_exceptions():BP.add_function_param(graph,param,type_name,is_input)
 return graph
def node(graph,suffix):
 candidates=[t for t in BP.find_node_types(graph,suffix) if t.lower().endswith('|'+suffix.lower())]
 if len(candidates)>1:
  for prefix in ['CallFunction|','SaveGame|','HUD|','Settings|','Game|','Input|','Movement|','Pawn|Components|CharacterMovement|','Pawn|','Variables|Default|']:
   subset=[t for t in candidates if t.startswith(prefix)]
   if len(subset)==1:return subset[0]
 assert len(candidates)==1,(suffix,candidates)
 return candidates[0]
def get(name):return '(Variables|Default|Get'+name+')'
def setv(name,value):return '(Variables|Default|Set'+name+' '+value+')'
def write(graph,code):
 # The stock wrapper removes stale nodes one at a time. On a large HUD graph,
 # every removal rebuilds editor state and can exhaust the system commit limit.
 # Keep the engine transpiler and its rollback, batching its deferred deletions.
 from editor_toolset.toolsets import blueprint_dsl
 pending=[]
 with toolset_registry.tool_raising_exceptions():
  try:
   blueprint_dsl.Transpiler(graph,BP.create_node,BP.connect_pins,BP._get_node_info,
    BP.set_pin_value,lambda g:BP.find_nodes(g),delete_node_fn=pending.append,
    find_node_types_fn=lambda f:BP.find_node_types(graph,f)).transpile(code)
  finally:
   if pending:unreal.BlueprintGraphEditor.get_graph_editor(graph).remove_nodes(pending)
  BP.compile_blueprint(unreal.Blueprint.cast(graph.get_outer()))
def compile_save(bp):
 with toolset_registry.tool_raising_exceptions():BP.compile_blueprint(bp)
 unreal.EditorAssetLibrary.save_loaded_asset(bp)
