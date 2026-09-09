import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert world
pc=unreal.GameplayStatics.get_player_controller(world,0);pawn=unreal.GameplayStatics.get_player_pawn(world,0);cam=pawn.get_component_by_class(unreal.CameraComponent)
fields=['override_auto_exposure_method','auto_exposure_method','override_auto_exposure_min_brightness','auto_exposure_min_brightness','override_auto_exposure_max_brightness','auto_exposure_max_brightness','override_auto_exposure_bias','auto_exposure_bias']
def props(o,names):
 r={}
 for n in names:
  try:r[n]=str(o.get_editor_property(n))
  except Exception as e:r[n]=str(e)
 return r
r={'camera':props(cam,['post_process_blend_weight']),'camera_exposure':props(cam.get_editor_property('post_process_settings'),fields),'lights':[],'volumes':[]}
for a in unreal.GameplayStatics.get_all_actors_of_class(world,unreal.Actor):
 name=a.get_actor_label()
 if isinstance(a,unreal.PostProcessVolume):r['volumes'].append({'name':name,'position':str(a.get_actor_location()),'bounds':str(a.get_actor_bounds(False)),'properties':props(a,['enabled','unbound','priority','blend_weight','blend_radius']),'exposure':props(a.get_editor_property('settings'),fields)})
 pp=a.get_component_by_class(unreal.PostProcessComponent)
 if pp:r['volumes'].append({'name':name,'component':True,'position':str(a.get_actor_location()),'bounds':str(a.get_actor_bounds(False)),'parent':str(pp.get_attach_parent()),'properties':props(pp,['enabled','unbound','priority','blend_weight','blend_radius']),'exposure':props(pp.get_editor_property('settings'),fields)})
 if 'Library' in name or 'library' in name:
  c=a.get_component_by_class(unreal.LightComponent)
  if c:r['lights'].append({'name':name,'position':str(a.get_actor_location()),'rotation':str(a.get_actor_rotation()),'properties':props(c,['intensity','visible','cast_shadows','mobility','attenuation_radius','indirect_lighting_intensity'])})
(root/'Saved/Logs/tour_runtime_lighting.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8')
