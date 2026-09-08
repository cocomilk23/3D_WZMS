"""Balance the library atrium's bright glazing and dark ceiling for sightseeing."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);actors={a.get_actor_label():a for a in sub.get_all_level_actors()}
pp=actors['InteriorExposure_Library'].get_component_by_class(unreal.PostProcessComponent);s=pp.get_editor_property('settings')
for k,v in [('auto_exposure_min_brightness',5.5),('auto_exposure_max_brightness',12.0),('local_exposure_highlight_contrast_scale',.7),('local_exposure_shadow_contrast_scale',.75)]:s.set_editor_property('override_'+k,True);s.set_editor_property(k,v)
pp.set_editor_property('settings',s)
# Keep the lower halls bright while limiting adaptation on the sunlit top gallery.
bp=unreal.load_asset('/Game/WZMS/Blueprints/BP_WZMS_InteriorExposure');label='InteriorExposure_Library_Upper';v=actors.get(label) or sub.spawn_actor_from_class(bp.generated_class(),unreal.Vector(12800,-15500,1060));v.set_actor_label(label);v.set_actor_location(unreal.Vector(12800,-15500,1060),False,True);v.set_folder_path('Environment/Interior Exposure');v.get_component_by_class(unreal.BoxComponent).set_box_extent(unreal.Vector(2300,1900,220),True)
u=v.get_component_by_class(unreal.PostProcessComponent);u.set_editor_property('priority',11);u.set_editor_property('blend_radius',70);us=u.get_editor_property('settings')
for k,value in [('auto_exposure_min_brightness',8.0),('auto_exposure_max_brightness',12.0),('local_exposure_highlight_contrast_scale',.7),('local_exposure_shadow_contrast_scale',.75)]:us.set_editor_property('override_'+k,True);us.set_editor_property(k,value)
u.set_editor_property('settings',us)
rows=[]
for i,(x,y) in enumerate([(118,144),(118,166),(139,144),(139,166)]):
 label=f'Tour_InteriorBounce_Library_Upper_{i:02d}';p=unreal.Vector(x*100,-y*100,1075);rot=unreal.Rotator(pitch=90,yaw=0,roll=0);a=actors.get(label) or sub.spawn_actor_from_class(unreal.RectLight,p,rot);a.set_actor_label(label);a.set_actor_location(p,False,True);a.set_actor_rotation(rot,False);a.set_folder_path('Tour Environment/Interior Lighting')
 c=a.get_component_by_class(unreal.RectLightComponent);c.set_mobility(unreal.ComponentMobility.MOVABLE);c.set_editor_property('intensity_units',unreal.LightUnits.LUMENS);c.set_editor_property('intensity',30000);c.set_editor_property('attenuation_radius',1400);c.set_editor_property('source_width',700);c.set_editor_property('source_height',700);c.set_editor_property('cast_shadows',True);c.set_editor_property('max_draw_distance',16000);c.set_editor_property('max_distance_fade_range',3000);c.set_editor_property('use_temperature',True);c.set_editor_property('temperature',5000)
 rows.append({'actor':label,'estimated_lumens':30000,'purpose':'Approximate broad floor-bounced daylight on the upper ceiling; no invented visible floor fixture.'})
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
p=root.parent/'Reports/tour_interior_lighting.json';r=json.loads(p.read_text(encoding='utf8'));r['library_exposure_ev']={'lower_halls':[5.5,12],'upper_gallery':[8.0,12]};r['library_upper_indirect_fill']=rows;p.write_text(json.dumps(r,indent=2),encoding='utf8')
