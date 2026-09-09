"""Clip only proven same-facing overlaps; preserve the union, height and all non-overlapping geometry."""
import json,sys,collections,hashlib
from pathlib import Path
sys.path.append('E:/WZMS_UE_Cache/Python')
import numpy as np
import shapely
from shapely.geometry import Polygon
from shapely.ops import unary_union
ue=Path(__file__).resolve().parents[1];folder=ue/'WZMS/Saved/OrientationAudit'
audit=json.loads((ue/'Reports/final057_surface_audit.json').read_text());meta={x['name']:x for x in json.loads((folder/'meshes.json').read_text())};chunks={x['name']:x for x in json.loads((folder/'source_chunks.json').read_text())}
initial=json.loads((ue/'SourceReference/final057_surface_patch.json').read_text());patch={x['name']:x for x in initial};data={};graph=collections.defaultdict(set);info={}
def get(key):
 name,tid=key
 if name not in data:
  r=meta[name];base=next(k for k in chunks if name.startswith(k));v=np.fromfile(r['positions_file'],np.float64).reshape(-1,3);t=np.fromfile(r['triangles_file'],np.int32).reshape(-1,3);world=v*np.array([1,-1,1])+np.array(chunks[base]['pivot']);data[name]=(v,t,world)
 v,t,w=data[name];return w[t[tid]]
for pair in audit['coplanar_pairs']:
 a,b=tuple(pair['a']),tuple(pair['b']);aa,bb=get(a),get(b);na=np.cross(aa[1]-aa[0],aa[2]-aa[0]);nb=np.cross(bb[1]-bb[0],bb[2]-bb[0])
 if np.dot(na,nb)<=0:continue # opposite-facing internal joints do not z-fight
 for k,tri in [(a,aa),(b,bb)]:info[k]=(pair['axis'],Polygon(np.delete(tri,pair['axis'],axis=1)))
 graph[a].add(b);graph[b].add(a)
seen=set();changes=collections.defaultdict(list);groups=[]
for start in graph:
 if start in seen:continue
 stack=[start];component=[]
 while stack:
  k=stack.pop()
  if k in seen:continue
  seen.add(k);component.append(k);stack.extend(graph[k]-seen)
 component.sort(key=lambda k:(round(info[k][1].area,6),k));retained={};before=unary_union([info[k][1] for k in component]);after=[]
 for k in component:
  axis,poly=info[k];blockers=[retained[j] for j in graph[k] if j in retained];new=poly.difference(unary_union(blockers)) if blockers else poly
  retained[k]=new;after.append(new)
  if poly.area-new.area<1e-6:continue
  tri=get(k);coords=np.delete(tri,axis,axis=1);A=np.vstack([coords.T,np.ones(3)]);inv=np.linalg.inv(A);out=[]
  for part in shapely.get_parts(new):
   if part.geom_type!='Polygon' or part.area<1e-8:continue
   for t in shapely.get_parts(shapely.constrained_delaunay_triangles(part)):
    pp=np.array(t.exterior.coords)[:3];weights=np.array([inv@np.array([x,y,1]) for x,y in pp]);verts=weights@tri
    if np.dot(np.cross(verts[1]-verts[0],verts[2]-verts[0]),np.cross(tri[1]-tri[0],tri[2]-tri[0]))<0:weights=weights[[0,2,1]]
    out.append(weights.tolist())
  changes[k[0]].append({'triangle':k[1],'barycentric_triangles':out,'original_area_m2':poly.area,'retained_area_m2':new.area,'axis':axis})
 union=unary_union(after);error=before.symmetric_difference(union).area;assert error<.0001,(component,error)
 groups.append({'faces':len(component),'union_area_m2':round(before.area,6),'union_error_m2':error})
for name,rows in changes.items():
 if name not in patch:
  r=meta[name];patch[name]={'mesh':r['path'],'name':name,'positions_sha256':hashlib.sha256(Path(r['positions_file']).read_bytes()).hexdigest(),'triangles_sha256':hashlib.sha256(Path(r['triangles_file']).read_bytes()).hexdigest(),'delete_triangles':[],'duplicates':0,'replacements':{}}
 excluded=set(patch[name]['delete_triangles']);patch[name]['clipped_triangles']=[r for r in rows if r['triangle'] not in excluded]
report={'same_facing_overlap_groups':len(groups),'clipped_source_triangles':sum(len(x.get('clipped_triangles',[])) for x in patch.values()),'maximum_union_area_error_m2':max(x['union_error_m2'] for x in groups),'method':'Polygon subtraction of measured same-facing coplanar overlaps, smaller surface retained as detail. Barycentric interpolation preserves existing UVs/normals/material IDs. Opposite-facing internal joints left unchanged.','groups':groups}
(ue/'SourceReference/final057_surface_patch.json').write_text(json.dumps(list(patch.values()),separators=(',',':'))+'\n',encoding='utf8')
(ue/'Reports/final057_coplanar_plan.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
print({k:v for k,v in report.items() if k!='groups'})
