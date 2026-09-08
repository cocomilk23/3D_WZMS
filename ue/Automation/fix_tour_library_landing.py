"""Finish two side entries and guard the new central headroom opening at floor two."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);existing={a.get_actor_label():a for a in sub.get_all_level_actors()};cube=unreal.load_asset('/Engine/BasicShapes/Cube')
data=json.loads(Path('E:/3D_WZMS/builds/v043_ue_bundle/materials.json').read_text(encoding='utf8'));ids={r['source_name']:r['id'] for r in data['materials']}
def material(name):return unreal.load_asset('/Game/WZMS/Materials/Instances/MI_'+ids[name])
floor=material('Library polished brown hall tile');wood=material('Library oak fine vertical panels');steel=material('Library ivory floor border');rows=[]
def box(name,lo,hi,mat):
 a=existing.get(name) or sub.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector());a.set_actor_label(name);a.set_folder_path('Tour Environment/Library Stair Landings');a.set_actor_location(unreal.Vector((lo[0]+hi[0])*50,-(lo[1]+hi[1])*50,(lo[2]+hi[2])*50),False,True);a.set_actor_scale3d(unreal.Vector(*[hi[j]-lo[j] for j in range(3)]));c=a.static_mesh_component;c.set_static_mesh(cube);c.set_material(0,mat);c.set_collision_profile_name('BlockAll');rows.append({'actor':name,'bounds_m':[lo,hi]})
for sign in [-1,1]:
 y=155+sign*1.4
 for i in range(3):
  box(f'Tour_Library_Entry_{sign}_{i}',[122+i*.44,y-.44,4.20],[122+(i+1)*.44,y+.44,4.25+(i+1)*.11],floor)
# Upper-floor guard at the western edge of the newly opened ceiling slot.
for y in [154.16,155,155.84]:box('Tour_Library_Opening_Post_'+str(y),[122.70,y-.025,4.25],[122.75,y+.025,5.30],steel)
for z in [4.72,5.28]:box('Tour_Library_Opening_Rail_'+str(z),[122.685,154.12,z],[122.765,155.88,z+.06],wood)
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
(root.parent/'Reports/tour_library_landing.json').write_text(json.dumps({'objects':rows,'estimated_circulation_adjustment':True,'purpose':'Side access to both curved stair flights while retaining central stair headroom and guarding the upper-floor opening.'},indent=2),encoding='utf8')
