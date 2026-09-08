import bpy,json,numpy as np
from pathlib import Path
root=Path('E:/3D_WZMS/builds/v043_ue_bundle')
zone=json.loads((root/'zone_south.json').read_text(encoding='utf8'));rows=[]
for c in zone['chunks']:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=str(root/c['file']))
    obj=next(o for o in bpy.context.scene.objects if o.type=='MESH');mesh=obj.data;mesh.calc_loop_triangles()
    v=np.array([tuple(x.co) for x in mesh.vertices]);f=np.array([tuple(x.vertices) for x in mesh.loop_triangles])
    area=np.linalg.norm(np.cross(v[f[:,1]]-v[f[:,0]],v[f[:,2]]-v[f[:,0]]),axis=1)/2
    used=np.unique(f[area>=1e-12].reshape(-1));points=v[used]
    rows.append({'name':c['name'],'vertices':len(v),'used_vertices':len(used),'triangles':len(f),'zero_area_faces':int(np.sum(area<1e-12)),'used_local_bounds_m':[points.min(0).tolist(),points.max(0).tolist()]})
    print('FBX_BOUNDS_AUDITED',c['name'],flush=True)
Path('E:/WZMS_UE/ue/Reports/fbx_used_bounds.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
