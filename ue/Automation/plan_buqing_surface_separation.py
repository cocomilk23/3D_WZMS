"""Select exact connected source slabs implicated in the reported plaza z-fighting."""
import hashlib,json,pathlib
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
ue=pathlib.Path(__file__).resolve().parents[1]
source=json.loads(pathlib.Path('E:/3D_WZMS/builds/v043_ue_bundle/zone_central.json').read_text(encoding='utf8'))
chunks={x['name']:x for x in source['chunks']}
specs=[('Buqing continuous plaza slab','SM_central_solid_037',[-3,134,111,181],-.02),('Buqing through-passage floor','SM_central_solid_038',[47,180,61,196],.01),('Buqing north exit apron','SM_central_solid_038',[47,194.5,61,205.5],.02)]
rows=[]
for meshname in sorted({x[1] for x in specs}):
 vp=ue/'WZMS/Saved/OrientationAudit'/f'{meshname}.f64';tp=vp.with_suffix('.i32')
 v=np.fromfile(vp,dtype=np.float64).reshape(-1,3);t=np.fromfile(tp,dtype=np.int32).reshape(-1,3)
 _,weld=np.unique(np.round(v,6),axis=0,return_inverse=True);wt=weld[t];edges=np.concatenate([wt[:,[0,1]],wt[:,[1,2]],wt[:,[2,0]]])
 _,labels=connected_components(coo_matrix((np.ones(len(edges)),(edges[:,0],edges[:,1])),shape=(int(weld.max()+1),)*2),directed=False)
 groups=labels[wt[:,0]];pivot=np.array(chunks[meshname]['pivot_blender_m']);world=v*np.array([1,-1,1])+pivot
 candidates=[]
 for g in np.unique(groups):
  ids=np.unique(t[groups==g]);vv=world[ids];lo=vv.min(0);hi=vv.max(0)
  if abs(hi[2]+.01)<.003:candidates.append((ids,lo,hi))
 changes=[]
 for objectname,_,bounds,dz in [s for s in specs if s[1]==meshname]:
  found=[c for c in candidates if np.max(np.abs(np.array([c[1][0],c[1][1],c[2][0],c[2][1]])-bounds))<.003]
  assert len(found)==1,(objectname,len(found))
  ids,lo,hi=found[0]
  changes.append({'object':objectname,'vertex_ids':ids.tolist(),'old_bounds_blender_m':[lo.tolist(),hi.tolist()],'translation_local':[0,0,dz],'old_top_z_m':float(hi[2]),'new_top_z_m':float(hi[2]+dz)})
 rows.append({'mesh':'/Game/WZMS/Central/Meshes/'+meshname,'positions_sha256':hashlib.sha256(vp.read_bytes()).hexdigest(),'triangles_sha256':hashlib.sha256(tp.read_bytes()).hexdigest(),'vertex_count':len(v),'triangle_count':len(t),'changes':changes})
out=ue/'SourceReference/buqing_surface_separation.json'
out.write_text(json.dumps({'reason':'Source footprint intersections prove coplanar overlaps between plaza, classroom ground slab, library apron and passage. Preserve connected slab geometry with <=2cm vertical separation.','meshes':rows},indent=2)+'\n',encoding='utf8')
print(json.dumps(rows,indent=2))
