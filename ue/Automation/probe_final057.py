"""Read current geometry APIs and renderer settings before the final corrections."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();out={}
for cls in ['GeometryScript_MeshBasicEditFunctions','GeometryScript_MeshEdits','GeometryScript_MeshMaterialEdits','GeometryScript_MeshQueries','TexturePowerOfTwoSetting']:
 c=getattr(unreal,cls,None);out[cls]=[n for n in dir(c) if any(w in n.lower() for w in ['triangle','material','delete','remove','power','stretch','pad'])] if c else None
out['methods']={}
for cls,name in [('GeometryScript_MeshEdits','delete_triangles_from_mesh'),('GeometryScript_MeshMaterialEdits','get_all_triangle_material_ids'),('GeometryScript_MeshMaterialEdits','get_triangle_material_id'),('GeometryScript_MeshEdits','append_buffers_to_mesh')]:
 f=getattr(getattr(unreal,cls,None),name,None);out['methods'][cls+'.'+name]=f.__doc__ if f else None
out['console']={n:unreal.SystemLibrary.get_console_variable_int_value(n) for n in ['r.Shadow.Virtual.OnePassProjection.MaxLightsPerPixel','r.Shadow.Virtual.MaxPhysicalPages','r.Shadow.Virtual.NonNanite.NumPageAreaDiagSlots','r.Shadow.Virtual.NonNanite.NumPageAreaDiagSlotsPerQueue','r.Shadow.Virtual.NonNanite.MaxCulledInstances','r.Shadow.Virtual.SMRT.RayCountDirectional','r.Shadow.Virtual.SMRT.SamplesPerRayDirectional','r.Lumen.ScreenProbeGather.Temporal.MaxFramesAccumulated']}
out['more_api']={}
for cls in [n for n in dir(unreal) if 'GeometryScript' in n and ('Material' in n or 'List' in n)]:
 out['more_api'][cls]=[n for n in dir(getattr(unreal,cls)) if 'material' in n or 'index' in n or 'array' in n]
out['delete_selected_doc']=unreal.GeometryScript_MeshEdits.delete_selected_triangles_from_mesh.__doc__
out['clip_api']={n:getattr(unreal.GeometryScript_MeshQueries,n).__doc__ for n in ['get_triangle_positions','get_triangle_u_vs','get_triangle_normals']}
out['clip_api']['material']=unreal.GeometryScript_Materials.get_triangle_material_id.__doc__
out['cameras']=[]
out['actors']=[]
for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors():
 if isinstance(a,unreal.CameraActor):out['cameras'].append({'label':a.get_actor_label(),'location':list(a.get_actor_location().to_tuple()),'rotation':list(a.get_actor_rotation().to_tuple())})
 c=a.get_component_by_class(unreal.StaticMeshComponent)
 if c and c.static_mesh:
  out['actors'].append({'label':a.get_actor_label(),'mesh':c.static_mesh.get_path_name(),'transform':a.get_actor_transform().export_text(),'disallow_nanite':c.get_editor_property('disallow_nanite'),'materials':[m.get_path_name() if m else None for m in c.get_materials()]})
(root.parent/'Reports/final057_probe.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf8')
unreal.SystemLibrary.execute_console_command(None,'DumpConsoleCommands r.Shadow.Virtual.NonNanite')
