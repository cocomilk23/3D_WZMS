"""Read-only whole-campus solid audit, and precise selections for replaced sports/crest surfaces."""
import json,hashlib,sys
sys.path.append('E:/WZMS_UE_Cache/Python')
from pathlib import Path
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
import shapely
from shapely.geometry import Polygon
ue=Path(__file__).resolve().parents[1];folder=ue/'WZMS/Saved/OrientationAudit'
rows=json.loads((folder/'meshes.json').read_text());chunks={c['name']:c for c in json.loads((folder/'source_chunks.json').read_text())}
report={'meshes':[],'coplanar_pairs':[]};patch=[];faces={}
for row in rows:
 name=row['name'];base=next((k for k in chunks if name.startswith(k)),None)
 if base is None:continue
 v=np.fromfile(row['positions_file'],np.float64).reshape(-1,3);t=np.fromfile(row['triangles_file'],np.int32).reshape(-1,3)
 world=v*np.array([1,-1,1])+np.array(chunks[base]['pivot']);tri=world[t]
 _,weld=np.unique(np.round(v,6),axis=0,return_inverse=True);keys=np.sort(weld[t],axis=1)
 _,first,inv,cnt=np.unique(keys,axis=0,return_index=True,return_inverse=True,return_counts=True)
 dup=np.where(np.arange(len(t))!=first[inv])[0];remove=set(dup.tolist())
 specific={}
 if base=='SM_central_solid_038':
  rad=np.linalg.norm(tri[:,:,:2]-np.array([54,157]),axis=2)
  crest=np.where((rad.max(axis=1)<8.105)&(tri[:,:,2].min(axis=1)>.004)&(tri[:,:,2].max(axis=1)<.16))[0]
  specific['old_crest']=crest.tolist();remove.update(crest.tolist())
 if base in ['SM_central_solid_037','SM_central_solid_038']:
  # All painted court lines, keys and centre circles are planar, within the existing enclosure.
  planar=(np.ptp(tri[:,:,2],axis=1)<.0001)&(tri[:,:,2].min(axis=1)>.025)&(tri[:,:,2].max(axis=1)<.065)
  inside=(tri[:,:,0].min(axis=1)>-16.71)&(tri[:,:,0].max(axis=1)<45.71)&(tri[:,:,1].min(axis=1)>210.99)&(tri[:,:,1].max(axis=1)<319.01)
  court=np.where(planar&inside)[0];specific['old_court_paint']=court.tolist();remove.update(court.tolist())
  if base.endswith('038'):
   wt=weld[t];edges=np.concatenate([wt[:,[0,1]],wt[:,[1,2]],wt[:,[2,0]]]);_,labels=connected_components(coo_matrix((np.ones(len(edges)),(edges[:,0],edges[:,1])),shape=(int(weld.max()+1),)*2),directed=False)
   groups=labels[wt[:,0]];found=[]
   for g in np.unique(groups):
    ids=np.where(groups==g)[0];vv=tri[ids].reshape(-1,3);lo=vv.min(0);hi=vv.max(0)
    if np.max(np.abs(lo-[-16.7,211,-.055]))<.002 and np.max(np.abs(hi-[45.7,319,.025]))<.002:found.extend(ids.tolist())
   assert len(found)==12,('surround component',len(found));specific['old_court_surround']=found;remove.update(found)
 cross=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);area=np.linalg.norm(cross,axis=1)*.5
 n=cross/np.maximum(area[:,None]*2,1e-15);axis=np.argmax(np.abs(n),axis=1)
 candidates=np.where((area>.2)&(np.max(np.abs(n),axis=1)>.99999))[0]
 for tid in candidates:
  if int(tid) in remove:continue
  ax=int(axis[tid]);plane=float(tri[tid,:,ax].mean());key=(ax,round(plane,3))
  points=np.delete(tri[tid],ax,axis=1);poly=Polygon(points)
  if poly.is_valid and poly.area>.2:faces.setdefault(key,[]).append((name,int(tid),plane,poly))
 report['meshes'].append({'mesh':name,'triangles':len(t),'duplicate_triangles':len(dup),'replacement_triangles':{k:len(x) for k,x in specific.items()}})
 if remove:
  patch.append({'mesh':row['path'],'name':name,'positions_sha256':hashlib.sha256(Path(row['positions_file']).read_bytes()).hexdigest(),'triangles_sha256':hashlib.sha256(Path(row['triangles_file']).read_bytes()).hexdigest(),'delete_triangles':sorted(remove),'duplicates':len(dup),'replacements':{k:len(x) for k,x in specific.items()}})
 print(name,len(t),'duplicates',len(dup),'replacement',{k:len(x) for k,x in specific.items()},flush=True)
for (axis,plane),items in faces.items():
 if len(items)<2:continue
 geos=np.array([x[3] for x in items],dtype=object);tree=shapely.STRtree(geos)
 pairs=tree.query(geos,predicate='intersects')
 for i,j in zip(*pairs):
  if i>=j:continue
  a,b=items[i],items[j]
  if abs(a[2]-b[2])>.00015:continue
  overlap=a[3].intersection(b[3]).area
  if overlap>.08 and overlap/min(a[3].area,b[3].area)>.05:
   report['coplanar_pairs'].append({'a':[a[0],a[1]],'b':[b[0],b[1]],'axis':axis,'plane':plane,'overlap_m2':round(overlap,4),'bounds_2d':list(a[3].intersection(b[3]).bounds)})
report['summary']={'solid_meshes':len(report['meshes']),'triangles':sum(x['triangles'] for x in report['meshes']),'exact_duplicate_triangles':sum(x['duplicate_triangles'] for x in report['meshes']),'large_coplanar_triangle_pairs':len(report['coplanar_pairs'])}
(ue/'Reports/final057_surface_audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
(ue/'SourceReference/final057_surface_patch.json').write_text(json.dumps(patch,indent=2)+'\n',encoding='utf8')
print(report['summary'])
