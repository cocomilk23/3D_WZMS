import unreal,json
from pathlib import Path
ROOT=Path(unreal.Paths.project_dir()).resolve()
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
existing={a.get_actor_label():a for a in actors.get_all_level_actors()}
def spawn(cls,name,location=unreal.Vector(0,0,0),rotation=unreal.Rotator(0,0,0)):
    a=existing.get(name) or actors.spawn_actor_from_class(cls,location,rotation)
    a.set_actor_label(name);a.set_folder_path('Environment');a.set_actor_rotation(rotation,False);return a
sun=spawn(unreal.DirectionalLight,'WZMS_Daylight',unreal.Vector(0,0,10000),unreal.Rotator(pitch=-42,yaw=-130,roll=0))
sc=sun.get_component_by_class(unreal.DirectionalLightComponent)
sc.set_mobility(unreal.ComponentMobility.MOVABLE);sc.set_editor_property('intensity',35000)
sc.set_editor_property('atmosphere_sun_light',True);sc.set_editor_property('light_source_angle',1.1)
sc.set_editor_property('use_temperature',True);sc.set_editor_property('temperature',5700)
sky=spawn(unreal.SkyLight,'WZMS_SkyLight')
sk=sky.get_component_by_class(unreal.SkyLightComponent);sk.set_mobility(unreal.ComponentMobility.MOVABLE)
sk.set_editor_property('real_time_capture',True);sk.set_editor_property('intensity',1.0)
spawn(unreal.SkyAtmosphere,'WZMS_Atmosphere')
fog=spawn(unreal.ExponentialHeightFog,'WZMS_DistanceHaze',unreal.Vector(0,0,-500))
fc=fog.get_component_by_class(unreal.ExponentialHeightFogComponent);fc.set_editor_property('fog_density',.008)
fc.set_editor_property('start_distance',18000)
pp=spawn(unreal.PostProcessVolume,'WZMS_Exposure');pp.set_editor_property('unbound',True)
s=pp.get_editor_property('settings')
settings={'auto_exposure_method':unreal.AutoExposureMethod.AEM_HISTOGRAM,'auto_exposure_min_brightness':13.0,'auto_exposure_max_brightness':13.0,'auto_exposure_bias':0.0,'bloom_intensity':.08,'vignette_intensity':.12,'motion_blur_amount':0.0}
for key,val in settings.items():s.set_editor_property('override_'+key,True);s.set_editor_property(key,val)
pp.set_editor_property('settings',s)
start=spawn(unreal.PlayerStart,'WZMS_GateStart',unreal.Vector(-1450,3000,120),unreal.Rotator(pitch=0,yaw=-90,roll=0))
start.set_actor_location(unreal.Vector(-1450,3000,120),False,True)
for key,value in [('r.DefaultFeature.AutoExposure.ExtendDefaultLuminanceRange',1),('r.MotionBlurQuality',0),('r.ScreenPercentage',100),('r.Streaming.PoolSize',1500),('t.MaxFPS',60)]:
    unreal.SystemLibrary.execute_console_command(None,f'{key} {value}')
unreal.EditorLevelLibrary.set_level_viewport_camera_info(unreal.Vector(17000,17000,14000),unreal.Rotator(pitch=-34,yaw=-130,roll=0))
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
(ROOT.parent/'Reports/south_lighting.json').write_text(json.dumps({'sun_lux':35000,'sun_euler_ue':[-42,-130,0],'fixed_exposure_ev':13,'sky_realtime_capture':True,'motion_blur':False,'spawn_cm':[-1450,3000,120]},indent=2),encoding='utf8')
