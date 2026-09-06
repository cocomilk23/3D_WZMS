"""Fresh-load baseline preservation and sampled body clearance for v012-v015.
Usage: blender --background --factory-startup --python audit_south_deliveries.py -- 12
Checks editable mesh/UV/material assignments/transforms in the full predecessor,
then actual ray-cast surfaces at 0.35m intervals. Not an Unreal collision test.
"""
import bpy,sys,math,json,hashlib,array
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
rev=int(sys.argv[sys.argv.index('--')+1]);version='v0.0.'+str(rev)
out=ROOT/'deliverables'/version;out.mkdir(parents=True,exist_ok=True)
connection_plants=['Heyu arching variegated strap foliage','Heyu sparse grass blades'] if rev==15 else []
def plant_faces(name):
 o=bpy.data.objects[name];m=o.data
 return {tuple([p.material_index]+[tuple(m.vertices[i].co) for i in p.vertices]) for p in m.polygons}
def snapshots():
 bpy.context.view_layer.update();meshes={};result={}
 for o in bpy.data.objects:
  if o.type=='MESH' and o.data.name not in meshes:
   m=o.data;h=hashlib.sha256()
   for items,prop,mult,typ in [(m.vertices,'co',3,'f'),(m.loops,'vertex_index',1,'i'),(m.polygons,'loop_total',1,'i'),(m.polygons,'material_index',1,'i')]:
    a=array.array(typ,[0])*(len(items)*mult);items.foreach_get(prop,a);h.update(a.tobytes())
   for uv in m.uv_layers:
    a=array.array('f',[0])*(len(uv.data)*2);uv.data.foreach_get('uv',a);h.update(a.tobytes())
   h.update(str([m.name for m in m.materials]).encode());meshes[m.name]=h.hexdigest()
  result[o.name]={'type':o.type,'matrix':[list(row) for row in o.matrix_world],
   'geometry':meshes.get(o.data.name) if o.type=='MESH' else None,
   'modifiers':[(m.name,m.type) for m in o.modifiers],
   'hidden':(o.hide_render,o.hide_viewport)}
 return result
bpy.ops.wm.open_mainfile(filepath=str(ROOT/f'models/campus/WZMS_Campus_v{rev-1:03}.blend'))
bpy.context.window.scene=bpy.data.scenes['WZMS_Campus']
before=snapshots()
before_plants={name:plant_faces(name) for name in connection_plants}
bpy.ops.wm.open_mainfile(filepath=str(ROOT/f'models/campus/WZMS_Campus_v{rev:03}.blend'))
sc=bpy.data.scenes['WZMS_Campus'];bpy.context.window.scene=sc
after=snapshots()
changed=[name for name,val in before.items() if after.get(name)!=val]
adjustments=[]
for name in connection_plants:
 if name not in changed:continue
 old,new=before_plants[name],plant_faces(name);removed=old-new
 same_properties=all(before[name][key]==after[name][key] for key in before[name] if key!='geometry')
 local_only=bool(removed) and new<=old and all(any(86.1<=v[0]<=91.7 and 39.85<=v[1]<=44.15 for v in face[1:]) for face in removed)
 if same_properties and local_only:adjustments.append({'object':name,'removed_faces':len(removed),'scope':'Only existing leaf faces removed at the new east island bridge exit; remaining faces and object properties unchanged'})
unexpected=[name for name in changed if name not in {a['object'] for a in adjustments}]
pres={'baseline':f'v0.0.{rev-1}','objects_checked':len(before),'changed_or_missing':changed,
 'new_objects':len(after)-len(before),'unchanged':not changed,
 'scope':'mesh coordinates, topology, UVs, material assignments, transforms, modifier identities, visibility; camera/scene settings excluded'}
pres.update(expected_connection_adjustments=adjustments,unexpected_changes=unexpected,all_unexpected_changes_absent=not unexpected)
(out/'preservation_validation.json').write_text(json.dumps(pres,ensure_ascii=False,indent=2),encoding='utf8')
print('SOUTH_PREDECESSOR_PRESERVED',not changed,'DOCUMENTED_CONNECTION_TRIMS',adjustments,'UNEXPECTED',unexpected[:5],flush=True)
deps=bpy.context.evaluated_depsgraph_get()
routes=[('Tennis entrance from existing road',[(54,47),(62,47),(62,17),(68,17),(76,17)]),
 ('Tennis court west ends',[(69,17),(69,-1),(77,-1)]),
 ('Tennis north runout and east gate',[(69,24.5),(97,24.5),(97,23),(100.5,23)])]
if rev==13:
 # This addition is west of the campus; the independently sealed tennis checks
 # remain valid. Only the new west routes need repeating for this revision.
 routes=[]
 sys.path.insert(0,str(Path(__file__).parent));from south_detail_common import smooth_path
 routes.append(('Daosi south curve',smooth_path([(-50,47),(-59,48),(-67,59),(-70,72),(-69,86)],18)))
 routes.append(('Daosi flower bridge',[(-69,86),(-69,128)]))
 routes.append(('Daosi north junction and Nantian reserved link',smooth_path([(-69,128),(-69,136),(-58,145),(-30,146),(-20,146)],18)))
if rev>=14:routes.append(('Heyu entry bridge and island path',[(62,44),(70,44),(77,42),(87,42)]))
if rev>=15:routes.append(('Shuinan waterside bridge to tennis',[(87,42),(106,42),(106,23),(99,23)]))
if rev>=15:routes.append(('Shuinan peninsula utility room approach',[(106,30),(106,23),(106,19),(109,19),(109,19.7)]))
# Conservative broad phase: rays cannot reach geometry outside these bounds.
# Link original objects into a temporary query scene, avoiding traversal of remote
# classrooms on every ray. Evaluated bounds include modifiers; no proxy surfaces.
route_points=[p for _,poly in routes for p in poly]
lo=[min(p[0] for p in route_points)-.5,min(p[1] for p in route_points)-.5,-1.1]
hi=[max(p[0] for p in route_points)+.5,max(p[1] for p in route_points)+.5,2.4]
original_scene=sc
query=bpy.data.scenes.new('Temporary southern geometric clearance query')
for o in original_scene.objects:
 if o.type not in {'MESH','CURVE','SURFACE','FONT','META'} or o.hide_viewport:continue
 ev=o.evaluated_get(deps);bounds=[ev.matrix_world@Vector(v) for v in ev.bound_box]
 if all(max(v[i] for v in bounds)>=lo[i] and min(v[i] for v in bounds)<=hi[i] for i in range(3)):
  query.collection.objects.link(o)
bpy.context.window.scene=query;bpy.context.view_layer.update();sc=query;deps=bpy.context.evaluated_depsgraph_get()
print('SOUTH_QUERY_OBJECTS',len(query.objects),'of',len(original_scene.objects),flush=True)
reports=[]
for name,poly in routes:
 failures=[];count=0;lastz=None
 for a,b in zip(poly,poly[1:]):
  a,b=Vector(a),Vector(b);delta=b-a;dist=delta.length
  if dist<1e-6:continue
  tangent=delta.normalized();normal=Vector((-tangent.y,tangent.x))
  for i in range(math.ceil(dist/.35)+1):
   q=a.lerp(b,i/math.ceil(dist/.35));count+=1
   hit,pos,nor,idx,obj,mat=sc.ray_cast(deps,Vector((q.x,q.y,1.0)),Vector((0,0,-1)),distance=2)
   if not hit or pos.z<-.18 or pos.z>.55:
    failures.append({'xy':list(q),'reason':'missing or obstructed floor','z':pos.z if hit else None,'object':obj.name if obj else None});continue
   if lastz is not None and abs(pos.z-lastz)>.20:failures.append({'xy':list(q),'reason':'step >0.20m','delta':pos.z-lastz})
   lastz=pos.z
   hit2,p2,_,_,o2,_=sc.ray_cast(deps,pos+Vector((0,0,.025)),Vector((0,0,1)),distance=1.70)
   if hit2:failures.append({'xy':list(q),'reason':'headroom','object':o2.name})
   for h in [.45,1.1,1.60]:
    for sign in [-1,1]:
     hit2,p2,_,_,o2,_=sc.ray_cast(deps,pos+Vector((0,0,h)),Vector((normal.x*sign,normal.y*sign,0)),distance=.35)
     if hit2:failures.append({'xy':list(q),'reason':'body width','object':o2.name})
 reports.append({'name':name,'samples':count,'failure_count':len(failures),'failures':failures[:30]})
 print('SOUTH_ROUTE',name,count,'FAILURES',len(failures),failures[:3],flush=True)
report={'version':version,'sample_spacing_max_m':.35,'body_width_m':.70,'headroom_m':1.70,'routes':reports,
 'all_passed':not any(r['failure_count'] for r in reports),'ue_verified':False,
 'query_geometry':'original objects intersecting conservative evaluated bounds; no proxy colliders',
 'query_objects':len(query.objects),'query_bounds':[lo,hi]}
(out/'geometry_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
bpy.context.window.scene=original_scene;bpy.data.scenes.remove(query)
if unexpected or not report['all_passed']:raise RuntimeError('Southern scene validation failed; inspect saved reports')
print('SOUTH_BATCH_AUDIT_COMPLETE',version,flush=True)
