"""Check whether original luminaire geometry occludes the light source."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve()
sub=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
world=sub.get_game_world() or sub.get_editor_world();assert world
rows=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(world,unreal.Actor):
 name=a.get_actor_label()
 if not name.startswith('InteriorLight_'):continue
 c=a.get_component_by_class(unreal.LocalLightComponent)
 pos=a.get_actor_location();direction=a.get_actor_forward_vector()
 hit=unreal.SystemLibrary.line_trace_single(world,pos,pos+direction*2000,unreal.TraceTypeQuery.ECC_VISIBILITY,True,[a],unreal.DrawDebugTrace.NONE)
 result=None
 if hit:
  h=hit.to_dict();component=h['hit_component']
  result={'distance_cm':(h['impact_point']-pos).length(),'point':list(h['impact_point'].to_tuple()),'initial_overlap':h['initial_overlap'],'actor':component.get_owner().get_actor_label() if component else None}
 extra={}
 for key in ['affects_world','visible','intensity_units','use_inverse_squared_falloff','lighting_channels','cast_shadows','max_draw_distance','max_distance_fade_range','temperature','use_temperature']:
  try:extra[key]=str(c.get_editor_property(key))
  except Exception:pass
 rows.append({'name':name,'position':list(pos.to_tuple()),'forward':list(direction.to_tuple()),'intensity':c.intensity,'color':str(c.get_light_color()),'properties':extra,'hit':result})
(root/'Saved/Logs/tour_light_clearance.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
