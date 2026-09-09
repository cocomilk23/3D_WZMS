"""Restore source local light poses and add bounded indoor exposure adaptation."""
import unreal,json,math
from pathlib import Path
from editor_toolset.toolsets.blueprint import BlueprintTools as BP
root=Path(unreal.Paths.project_dir()).resolve();assets=unreal.EditorAssetLibrary
source=json.loads(Path('E:/3D_WZMS/builds/v043_ue_bundle/scene_reference.json').read_text(encoding='utf8'))
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);existing={a.get_actor_label():a for a in actors.get_all_level_actors()};rows=[]
for i,l in enumerate(source['lights']):
    if l['type']=='SUN':continue
    m=l['world_matrix'];d=(-m[0][2],m[1][2],-m[2][2]);pos=unreal.Vector(m[0][3]*100,-m[1][3]*100,m[2][3]*100)
    rot=unreal.Rotator(pitch=math.degrees(math.atan2(d[2],math.hypot(d[0],d[1]))),yaw=math.degrees(math.atan2(d[1],d[0])),roll=0)
    name=f'InteriorLight_{i:03d}_{l["name"]}';cls=unreal.SpotLight if l['type']=='SPOT' else unreal.RectLight
    a=existing.get(name) or actors.spawn_actor_from_class(cls,pos,rot)
    a.set_actor_label(name);a.set_actor_location(pos,False,True);a.set_actor_rotation(rot,False);a.set_folder_path('Environment/Interior Lights')
    c=a.get_component_by_class(unreal.LocalLightComponent);c.set_mobility(unreal.ComponentMobility.MOVABLE)
    c.set_editor_property('intensity_units',unreal.LightUnits.LUMENS)
    # Artistic estimate for this source package; Blender watts are not UE lumens.
    lumens=l['energy_blender_units']*70
    c.set_editor_property('intensity',lumens);c.set_light_color(unreal.LinearColor(r=l['color'][0],g=l['color'][1],b=l['color'][2],a=1))
    radius=2200 if l['name'].startswith('Library') else 1800 if 'upper industrial' in l['name'] else 950 if l['name'].startswith(('Gym','Canteen')) else 650
    c.set_editor_property('attenuation_radius',radius);c.set_editor_property('cast_shadows',True)
    c.set_editor_property('max_draw_distance',18000);c.set_editor_property('max_distance_fade_range',3000)
    if isinstance(c,unreal.RectLightComponent):
        c.set_editor_property('source_width',300 if l['name'].startswith('Library') else 120)
        c.set_editor_property('source_height',200 if l['name'].startswith('Library') else 35)
    if isinstance(c,unreal.SpotLightComponent):
        c.set_editor_property('inner_cone_angle',32);c.set_editor_property('outer_cone_angle',60)
    rows.append({'source_name':l['name'],'ue_label':name,'position_cm':list(pos.to_tuple()),'estimated_lumens':lumens,'radius_cm':radius})

path='/Game/WZMS/Blueprints/BP_WZMS_InteriorExposure'
bp=assets.load_asset(path) or BP.create('/Game/WZMS/Blueprints','BP_WZMS_InteriorExposure',unreal.Actor.static_class())
ss=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);handles=ss.k2_gather_subobject_data_for_blueprint(bp)
def obj(h):return unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h))
box_handle=next((h for h in handles if isinstance(obj(h),unreal.BoxComponent)),None)
if box_handle is None:
    box_handle,reason=ss.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=handles[0],new_class=unreal.BoxComponent,blueprint_context=bp));assert not str(reason),str(reason)
    ss.rename_subobject(box_handle,unreal.Text('InteriorBounds'))
box=obj(box_handle);box.set_collision_enabled(unreal.CollisionEnabled.QUERY_ONLY);box.set_collision_response_to_all_channels(unreal.CollisionResponseType.ECR_IGNORE);box.set_editor_property('generate_overlap_events',False);box.set_editor_property('hidden_in_game',True)
pp_handle=next((h for h in ss.k2_gather_subobject_data_for_blueprint(bp) if isinstance(obj(h),unreal.PostProcessComponent)),None)
if pp_handle is None:
    pp_handle,reason=ss.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=box_handle,new_class=unreal.PostProcessComponent,blueprint_context=bp));assert not str(reason),str(reason)
    ss.rename_subobject(pp_handle,unreal.Text('InteriorExposure'))
pp=obj(pp_handle);pp.set_editor_property('unbound',False);pp.set_editor_property('priority',10);pp.set_editor_property('blend_radius',150)
s=pp.get_editor_property('settings')
for k,v in {'auto_exposure_method':unreal.AutoExposureMethod.AEM_HISTOGRAM,'auto_exposure_min_brightness':5.5,'auto_exposure_max_brightness':13.0,'auto_exposure_speed_up':3.0,'auto_exposure_speed_down':2.0}.items():
    s.set_editor_property('override_'+k,True);s.set_editor_property(k,v)
pp.set_editor_property('settings',s);unreal.BlueprintEditorLibrary.compile_blueprint(bp);assets.save_loaded_asset(bp)
# Estimated building envelopes; outdoor daylight retains approved fixed EV13.
rooms=[('Library',(105,136,-.2),(151,174,8.6)),('Zhouyuan',(-48,124,-.2),(-27,136,3.7)),('Alumni',(-55.2,151,-.2),(-28.8,170.2,9.3)),('Gym',(-100,385,1.0),(-52,432,15.0)),('Math',(135,112,-.2),(165,134,8.6)),('History',(250,117,-.2),(264,143,3.7)),('Canteen',(109,351,1.0),(140,392,5.0))]
volumes=[]
for name,lo,hi in rooms:
    centre=[(lo[j]+hi[j])/2 for j in range(3)];extent=unreal.Vector(*[(hi[j]-lo[j])*50 for j in range(3)])
    pos=unreal.Vector(centre[0]*100,-centre[1]*100,centre[2]*100);label='InteriorExposure_'+name
    a=existing.get(label) or actors.spawn_actor_from_class(bp.generated_class(),pos)
    a.set_actor_label(label);a.set_folder_path('Environment/Interior Exposure');a.set_actor_location(pos,False,True)
    a.get_component_by_class(unreal.BoxComponent).set_box_extent(extent,True)
    volumes.append({'name':name,'bounds_blender_m':[lo,hi]})
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
(root.parent/'Reports/campus_interior_lighting.json').write_text(json.dumps({'source_local_lights':len(rows),'lights':rows,'indoor_exposure_ev_range':[5.5,13],'bounded_volumes':volumes,'outdoor_ev':13,'estimated_photometry':True},indent=2))
