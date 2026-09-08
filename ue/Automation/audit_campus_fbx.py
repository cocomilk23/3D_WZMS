"""Audit exported triangle buffers with Blender's installed binary FBX parser."""
import importlib,json,sys,types,hashlib
from pathlib import Path
import numpy as np
addon=Path('D:/Program Files/Blender Foundation/Blender 5.1/5.1/scripts/addons_core/io_scene_fbx')
package=types.ModuleType('wzms_fbx_parser');package.__path__=[str(addon)];sys.modules[package.__name__]=package
parser=importlib.import_module('wzms_fbx_parser.parse_fbx')
source=Path('E:/3D_WZMS/builds/v043_ue_bundle');root=Path(__file__).resolve().parents[1]
def audit(chunk):
    path=source/chunk['file'];assert hashlib.sha256(path.read_bytes()).hexdigest()==chunk['sha256']
    data,_=parser.parse(str(path))
    objects=next(e for e in data.elems if e.id==b'Objects')
    geometries=[e for e in objects.elems if e.id==b'Geometry' and e.props[-1]==b'Mesh'];assert len(geometries)==1
    fields={e.id:e for e in geometries[0].elems}
    v=np.asarray(fields[b'Vertices'].props[0],dtype=np.float32).astype(np.float64).reshape(-1,3)
    indices=np.asarray(fields[b'PolygonVertexIndex'].props[0],dtype=np.int64)
    assert np.all(indices.reshape(-1,3)[:,:2]>=0) and np.all(indices.reshape(-1,3)[:,2]<0)
    f=np.where(indices<0,-indices-1,indices).reshape(-1,3)
    area=np.linalg.norm(np.cross(v[f[:,1]]-v[f[:,0]],v[f[:,2]]-v[f[:,0]]),axis=1)/2
    used=np.unique(f[area>=1e-12].reshape(-1));points=v[used]
    assert len(f)==chunk['triangles']
    return {'name':chunk['name'],'vertices':len(v),'used_vertices':len(used),'triangles':len(f),'zero_area_faces':int(np.sum(area<1e-12)),'used_local_bounds_m':[points.min(0).tolist(),points.max(0).tolist()]}
south=json.loads((source/'zone_south.json').read_text(encoding='utf8'))
trusted={r['name']:r for r in json.loads((root/'Reports/fbx_used_bounds.json').read_text())}
for chunk in south['chunks']:
    row=audit(chunk);ref=trusted[row['name']]
    assert row['zero_area_faces']==ref['zero_area_faces'],(row['name'],'face area')
    assert np.max(np.abs(np.array(row['used_local_bounds_m'])-ref['used_local_bounds_m']))<1e-5,(row['name'],'bounds')
print('Verified raw FBX audit against all 54 prior Blender round trips.',flush=True)
for name in ['central','west','east','north']:
    zone=json.loads((source/f'zone_{name}.json').read_text(encoding='utf8'))
    rows=[audit(c) for c in zone['chunks']]
    (root/f'Reports/fbx_bounds_{name}.json').write_text(json.dumps(rows,indent=2))
    print(name,len(rows),'verified',flush=True)
