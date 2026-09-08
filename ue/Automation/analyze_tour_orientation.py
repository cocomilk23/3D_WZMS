"""Identify consistently inward closed components, calibrated against UE's own cube."""
import json,hashlib,argparse
from pathlib import Path
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
parser=argparse.ArgumentParser();parser.add_argument('--output',default='SourceReference/tour_orientation_selection.json');args=parser.parse_args()
root=Path(__file__).resolve().parents[1];source=root/'WZMS/Saved/OrientationAudit';meshes=json.loads((source/'meshes.json').read_text());output=[];canonical=None
for row in meshes:
 v=np.fromfile(row['positions_file'],dtype=np.float64).reshape(-1,3);t=np.fromfile(row['triangles_file'],dtype=np.int32).reshape(-1,3)
 # Positional weld is analytical only; the original vertices and UV seams are never merged.
 _,weld=np.unique(np.round(v,6),axis=0,return_inverse=True);wt=weld[t];edges=np.concatenate([wt[:,[0,1]],wt[:,[1,2]],wt[:,[2,0]]]);n=int(weld.max()+1)
 graph=coo_matrix((np.ones(len(edges)),(edges[:,0],edges[:,1])),shape=(n,n));count,labels=connected_components(graph,directed=False);group=labels[wt[:,0]]
 sorted_edges=np.sort(edges,axis=1);unique,inv,edge_count=np.unique(sorted_edges,axis=0,return_inverse=True,return_counts=True);sign=np.where(edges[:,0]<edges[:,1],1,-1);balance=np.bincount(inv,weights=sign,minlength=len(unique));bad=(edge_count!=2)|(balance!=0)|(unique[:,0]==unique[:,1]);bad_groups=set(labels[unique[bad,0]].tolist())
 a,b,c=v[t[:,0]],v[t[:,1]],v[t[:,2]];signed=np.einsum('ij,ij->i',a,np.cross(b,c))/6;vol=np.bincount(group,weights=signed,minlength=count);sizes=np.bincount(group,minlength=count)
 if row['name']=='Cube':
  assert count==1 and not bad_groups and abs(vol[0])>1;canonical=float(np.sign(vol[0]));print('Canonical cube signed volume',vol[0])
 assert canonical is not None,'Cube must be first in the audit'
 inward=[g for g in range(count) if g not in bad_groups and sizes[g]>=4 and vol[g]*canonical < -1e-9]
 selected=np.flatnonzero(np.isin(group,inward));components=[]
 for g in inward:
  verts=v[t[group==g].reshape(-1)];components.append({'triangles':int(sizes[g]),'signed_volume':float(vol[g]),'bounds_local': [verts.min(0).tolist(),verts.max(0).tolist()]})
 output.append({**row,'canonical_outward_volume_sign':canonical,'connected_components':count,'open_or_inconsistent_components':len(bad_groups),'inward_closed_components':components,'flip_triangle_ids':selected.tolist(),'positions_sha256':hashlib.sha256(Path(row['positions_file']).read_bytes()).hexdigest(),'triangles_sha256':hashlib.sha256(Path(row['triangles_file']).read_bytes()).hexdigest()})
 print(row['name'],'components',count,'unresolved topology',len(bad_groups),'inward',len(inward),'flip triangles',len(selected),flush=True)
(root/args.output).write_text(json.dumps({'method':'Closed components with exactly two oppositely directed faces per edge. Signed-volume orientation calibrated against UE Engine Cube. No vertex welding or decimation in the output. Open or inconsistently oriented components are excluded.','meshes':output},indent=2),encoding='utf8')
