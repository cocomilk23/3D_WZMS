"""Fresh-world distance queries for every bounded interior exposure shape."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert world
cases=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(world,unreal.Actor):
 if not a.get_actor_label().startswith('InteriorExposure_'):continue
 box=a.get_component_by_class(unreal.BoxComponent);pp=a.get_component_by_class(unreal.PostProcessComponent)
 centre=box.get_world_location();extent=box.get_scaled_box_extent()
 inside=box.get_closest_point_on_collision(centre)
 outside=box.get_closest_point_on_collision(centre+unreal.Vector(extent.x+250,0,0))
 channels=[getattr(unreal.CollisionChannel,n) for n in dir(unreal.CollisionChannel) if n.startswith('ECC_') and not n.endswith('MAX')]
 responses={str(c):str(box.get_collision_response_to_channel(c)) for c in channels}
 nonblocking=bool(channels) and all(box.get_collision_response_to_channel(c)==unreal.CollisionResponseType.ECR_IGNORE for c in channels)
 passed=inside[0]>=0 and inside[0]<1 and outside[0]>200 and nonblocking and not pp.get_editor_property('unbound')
 cases.append({'name':a.get_actor_label(),'inside_distance_cm':inside[0],'outside_distance_cm':outside[0],'all_channels_ignored':nonblocking,'channel_responses':responses,'passed':passed})
r={'complete':True,'passed':len(cases)==8 and all(c['passed'] for c in cases),'cases':cases,'method':'Fresh PIE world. Actual primitive collision distance inside/outside each volume and response on every exported collision channel. Visual exposure and movement checked separately.'}
(root.parent/'Reports/tour_exposure_runtime.json').write_text(json.dumps(r,indent=2),encoding='utf8')
print('EXPOSURE_BOUNDS',r['passed'])
