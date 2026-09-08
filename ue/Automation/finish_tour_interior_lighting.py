"""Restore authored glowing lamp lenses and illuminate the highest open library level."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();assets=unreal.EditorAssetLibrary;ed=unreal.MaterialEditingLibrary
source=json.loads(Path('E:/3D_WZMS/builds/v043_ue_bundle/materials.json').read_text(encoding='utf8'))
path='/Game/WZMS/Tour/Materials/M_Tour_Luminaire'
mat=assets.load_asset(path) or assets.duplicate_asset('/Game/WZMS/Materials/M_WZMS_surface',path)
# Re-use the full surface shader; the new branch only adds a calibrated visible lamp emission.
node=ed.get_material_property_input_node(mat,unreal.MaterialProperty.MP_EMISSIVE_COLOR)
if node is None:
 color=ed.create_material_expression(mat,unreal.MaterialExpressionVectorParameter,0,0);color.set_editor_property('parameter_name','LampEmissionColor');color.set_editor_property('default_value',unreal.LinearColor(1,1,1,1))
 power=ed.create_material_expression(mat,unreal.MaterialExpressionScalarParameter,0,0);power.set_editor_property('parameter_name','LampLuminance');power.set_editor_property('default_value',0)
 multiply=ed.create_material_expression(mat,unreal.MaterialExpressionMultiply,0,0)
 assert ed.connect_material_expressions(color,'',multiply,'A') and ed.connect_material_expressions(power,'',multiply,'B')
 assert ed.connect_material_property(multiply,'',unreal.MaterialProperty.MP_EMISSIVE_COLOR)
mat.set_editor_property('two_sided',True);ed.layout_material_expressions(mat);ed.recompile_material(mat);assets.save_loaded_asset(mat)
rows=[];ids={r['source_name']:r['id'] for r in source['materials']}
for row in source['materials']:
 if row['textures']:continue # Exhibition photographs retain their original appearance.
 bsdf=next((n for n in row['nodes'] if n['type']=='ShaderNodeBsdfPrincipled'),None)
 if not bsdf:continue
 inputs=bsdf['inputs'];strength=inputs.get('28:Emission Strength',0)
 if strength<1:continue
 mi=assets.load_asset('/Game/WZMS/Materials/Instances/MI_'+row['id']);assert mi
 col=inputs['27:Emission Color'];ed.set_material_instance_parent(mi,mat)
 ed.set_material_instance_vector_parameter_value(mi,'LampEmissionColor',unreal.LinearColor(*col[:3],1))
 luminance=strength*120;ed.set_material_instance_scalar_parameter_value(mi,'LampLuminance',luminance);ed.update_material_instance(mi);assets.save_loaded_asset(mi)
 rows.append({'source_material':row['source_name'],'instance':mi.get_path_name(),'emission_color':col,'estimated_luminance':luminance})
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);actors={a.get_actor_label():a for a in sub.get_all_level_actors()}
volume=actors['InteriorExposure_Library'];volume.set_actor_location(unreal.Vector(12800,-15500,630),False,True);volume.get_component_by_class(unreal.BoxComponent).set_box_extent(unreal.Vector(2300,1900,650),True)
cube=assets.load_asset('/Engine/BasicShapes/Cube');lens=assets.load_asset('/Game/WZMS/Materials/Instances/MI_'+ids['Library warm LED diffuser']);housing=assets.load_asset('/Game/WZMS/Materials/Instances/MI_'+ids['Library ivory floor border'])
lights=[]
for i,(x,y) in enumerate([(118,144),(118,155),(118,166),(139,145),(139,155),(139,165)]):
 name=f'Tour_InteriorLight_Library_Upper_{i:02d}';pos=unreal.Vector(x*100,-y*100,1210);a=actors.get(name) or sub.spawn_actor_from_class(unreal.RectLight,pos,unreal.Rotator(pitch=-90,yaw=0,roll=0));a.set_actor_label(name);a.set_actor_location(pos,False,True);a.set_actor_rotation(unreal.Rotator(pitch=-90,yaw=0,roll=0),False);a.set_folder_path('Tour Environment/Interior Lighting')
 c=a.get_component_by_class(unreal.RectLightComponent);c.set_mobility(unreal.ComponentMobility.MOVABLE);c.set_editor_property('intensity_units',unreal.LightUnits.LUMENS);c.set_editor_property('intensity',35000);c.set_editor_property('attenuation_radius',1600);c.set_editor_property('source_width',116);c.set_editor_property('source_height',32);c.set_editor_property('cast_shadows',True);c.set_editor_property('max_draw_distance',18000);c.set_editor_property('max_distance_fade_range',3000);c.set_editor_property('use_temperature',True);c.set_editor_property('temperature',4200)
 for kind,z,scale,material in [('Housing',12.20,(1.24,.40,.08),housing),('Lens',12.155,(1.16,.32,.015),lens)]:
  label=f'Tour_Library_Upper_Lamp_{i:02d}_{kind}';b=actors.get(label) or sub.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector());b.set_actor_label(label);b.set_actor_location(unreal.Vector(x*100,-y*100,z*100),False,True);b.set_actor_scale3d(unreal.Vector(*scale));b.set_folder_path('Tour Environment/Interior Lighting');bc=b.static_mesh_component;bc.set_static_mesh(cube);bc.set_material(0,material);bc.set_collision_profile_name('NoCollision')
 lights.append({'actor':name,'position_cm':list(pos.to_tuple()),'estimated_lumens':35000,'temperature_k':4200})
# Record actual enabled local lights and volumes for every currently reconstructed open interior.
all_actors=sub.get_all_level_actors();audit=[]
for area in ['Library','Zhouyuan','Alumni','Gym','Math','History','Canteen']:
 enabled=[]
 for a in all_actors:
  if not (a.get_actor_label().startswith(('InteriorLight_','Tour_InteriorLight_')) and area in a.get_actor_label()):continue
  c=a.get_component_by_class(unreal.LocalLightComponent)
  assert c and c.intensity>0 and c.is_visible(),a.get_actor_label()
  enabled.append({'actor':a.get_actor_label(),'intensity':c.intensity})
 assert enabled,area
 v=next(a for a in all_actors if a.get_actor_label()=='InteriorExposure_'+area);box=v.get_component_by_class(unreal.BoxComponent)
 audit.append({'area':area,'enabled_light_count':len(enabled),'lights':enabled,'exposure_bounds_centre_cm':list(v.get_actor_location().to_tuple()),'exposure_bounds_extent_cm':list(box.get_unscaled_box_extent().to_tuple())})
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
(root.parent/'Reports/tour_interior_lighting.json').write_text(json.dumps({'authored_lamp_materials_restored':rows,'additional_upper_library_lights':lights,'open_interior_audit':audit,'photometry':'Artistic estimates, to be verified by rendered views and runtime walkthroughs.','visual_validation_pending':True},indent=2),encoding='utf8')
