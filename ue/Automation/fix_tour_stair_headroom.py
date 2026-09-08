"""Create bounded stair-headroom variants; original imported meshes remain preserved."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();actors={a.get_actor_label():a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()};rows=[]
for name in ['SM_east_solid_061','SM_east_solid_062']:
 a=actors[name];original='/Game/WZMS/East/Meshes/'+name;variant='/Game/WZMS/Tour/Meshes/'+name+'_Tour';asset=unreal.EditorAssetLibrary.load_asset(original);before=asset.get_num_triangles(0)
 mesh=unreal.EditorAssetLibrary.load_asset(variant) or unreal.EditorAssetLibrary.duplicate_asset(original,variant);assert mesh
 dynamic=unreal.DynamicMesh();dynamic,outcome=unreal.GeometryScript_AssetUtils.copy_mesh_from_static_mesh(asset,dynamic,unreal.GeometryScriptCopyMeshFromAssetOptions(apply_build_settings=True),unreal.GeometryScriptMeshReadLOD(lod_type=unreal.GeometryScriptLODType.SOURCE_MODEL,lod_index=0));assert outcome==unreal.GeometryScriptOutcomePins.SUCCESS
 pos=a.get_actor_location()
 # Source local vertices are metres; the actor supplies the 100x centimetre conversion.
 centre=unreal.Vector(123.65-pos.x/100,-155-pos.y/100,3.975-pos.z/100)
 cutter=unreal.DynamicMesh();unreal.GeometryScript_Primitives.append_box(cutter,unreal.GeometryScriptPrimitiveOptions(),unreal.Transform(location=centre),1.7,1.6,.75,origin=unreal.GeometryScriptPrimitiveOriginMode.CENTER)
 unreal.GeometryScript_MeshBooleans.apply_mesh_boolean(dynamic,unreal.Transform(),cutter,unreal.Transform(),unreal.GeometryScriptBooleanOperation.SUBTRACT,unreal.GeometryScriptMeshBooleanOptions(fill_holes=False,simplify_output=False))
 # A short side-entry gap in the curved stair outer handrail connects the preserved landing.
 # The lower entry is rebuilt with three shallow landing steps in fix_tour_library_landing.py.
 for sign in [-1,1]:
  rail_centre=unreal.Vector(122.45-pos.x/100,-(155+sign*1.375)-pos.y/100,5.10-pos.z/100)
  rail_cut=unreal.DynamicMesh();unreal.GeometryScript_Primitives.append_box(rail_cut,unreal.GeometryScriptPrimitiveOptions(),unreal.Transform(location=rail_centre),.9,1.05,1.60,origin=unreal.GeometryScriptPrimitiveOriginMode.CENTER)
  unreal.GeometryScript_MeshBooleans.apply_mesh_boolean(dynamic,unreal.Transform(),rail_cut,unreal.Transform(),unreal.GeometryScriptBooleanOperation.SUBTRACT,unreal.GeometryScriptMeshBooleanOptions(fill_holes=False,simplify_output=False))
 opts=unreal.GeometryScriptCopyMeshToAssetOptions(enable_recompute_normals=False,enable_recompute_tangents=True,replace_materials=False,apply_nanite_settings=False)
 _,outcome=unreal.GeometryScript_AssetUtils.copy_mesh_to_static_mesh(dynamic,mesh,opts,unreal.GeometryScriptMeshWriteLOD(lod_index=0));assert outcome==unreal.GeometryScriptOutcomePins.SUCCESS
 unreal.EditorAssetLibrary.save_loaded_asset(mesh);after=mesh.get_num_triangles(0);assert before*.98<after<before*1.02,(name,before,after)
 comp=a.static_mesh_component;materials=[comp.get_material(i) for i in range(comp.get_num_materials())];comp.set_static_mesh(mesh)
 for i,mat in enumerate(materials):comp.set_material(i,mat)
 comp.set_editor_property('disallow_nanite',True);comp.set_collision_profile_name('BlockAll')
 rows.append({'actor':name,'original':original,'replacement':variant,'triangles_before':before,'triangles_after':after,'cut_world_blender_m':[[122.8,154.2,3.6],[124.5,155.8,4.35]],'curved_stair_side_entries_m':[[[122,155.85,4.30],[122.9,156.9,5.9]],[[122,153.1,4.30],[122.9,154.15,5.9]]],'purpose':'Provide real headroom above the central stair; visual geometry and collision both updated.'})
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
(root.parent/'Reports/tour_stair_geometry.json').write_text(json.dumps({'replacements':rows,'original_assets_preserved':True},indent=2))
