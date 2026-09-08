"""Read-only extraction of authored ground/water footprints for UE terrain integration."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
sc=bpy.data.scenes['WZMS_Campus'];surfaces=[];water=[];library=[];objects=0
water_names=set()
for zone in ['south','central','west','east','north']:
 d=json.loads(Path(f'E:/3D_WZMS/builds/v043_ue_bundle/zone_{zone}.json').read_text(encoding='utf8'))
 water_names.update(n for c in d['chunks'] if c['role']=='water' for n in c['source_objects'])
for o in sc.objects:
 if o.type!='MESH' or o.hide_render:continue
 objects+=1;m=o.matrix_world;b=[m@Vector(p) for p in o.bound_box];lo=[min(v[i] for v in b) for i in range(3)];hi=[max(v[i] for v in b) for i in range(3)]
 if o.name.startswith('Library') and any(s in o.name.lower() for s in ['stair','slab','ceiling','bridge','lintel']):library.append({'name':o.name,'bounds':[lo,hi]})
 iswater=o.name in water_names
 ispassage=any(t in o.name.lower() for t in ['bridge','deck','boardwalk','trestle'])
 maxz=6.0 if ispassage else 1.25
 if not iswater and (lo[2]>maxz or hi[2]<-1.10 or (hi[0]-lo[0])*(hi[1]-lo[1])<1):continue
 if o.get('ue_surface_role')=='foliage':continue
 if len(o.data.vertices)>100000:continue
 vs=[m@v.co for v in o.data.vertices]
 for p in o.data.polygons:
  coords=[vs[i] for i in p.vertices]
  if len(coords)<3:continue
  z=sum(v.z for v in coords)/len(coords)
  if not iswater and not (-1.10<=z<=maxz):continue
  # Upward, nearly horizontal surfaces only. Shape remains source-authored.
  n=sum(((coords[i]-coords[0]).cross(coords[i+1]-coords[0]) for i in range(1,len(coords)-1)),Vector());length=n.length
  if length<1e-8 or (abs(n.z)/length if iswater or hi[2]-lo[2]<.10 else n.z/length)<.85:continue
  area=abs(sum(a.x*c.y-c.x*a.y for a,c in zip(coords,coords[1:]+coords[:1]))/2)
  if area<.04:continue
  row={'object':o.name,'z':round(z,5),'xy':[[round(v.x,5),round(v.y,5)] for v in coords],'material':o.data.materials[p.material_index].name if o.data.materials and o.data.materials[p.material_index] else ''}
  (water if iswater else surfaces).append(row)
print('SOURCE_FOOTPRINTS',objects,len(surfaces),len(water),flush=True)
Path('E:/WZMS_UE/ue/SourceReference/terrain_source.json').write_text(json.dumps({'source':'Blender v043, read-only','source_file':bpy.data.filepath,'units':'metres','land_surfaces':surfaces,'water_surfaces':water,'library_structures':library},ensure_ascii=False),encoding='utf8')
