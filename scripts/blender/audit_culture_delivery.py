"""Fresh-file geometric preservation and 3D pedestrian route sampling. Not UE collision certification."""
import bpy,sys,json,math,hashlib,array
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).parent))
from culture_stages import STAGES
ROOT=Path(__file__).resolve().parents[2];rev=int(sys.argv[sys.argv.index('--')+1]);stage=STAGES[rev]
if rev in (21,25,29,33,39,40):
 superseded={r for st in STAGES.values() if st['previous']<rev for r in st.get('supersedes_routes',[])}
 stage=dict(stage,routes=[(f'v{r}: '+name,poly) for r in range(17,rev+1) if r not in superseded for name,poly in STAGES[r]['routes']])
 if rev==33:
  # Surface the new connection checks early; every registered route still runs.
  stage['routes'].sort(key=lambda item:0 if item[0].startswith('v33:') or item[0]=='v25: Jiangkou west branch toward Nantian' else 1)
 if rev==39:
  # Inspect the newly added dining circulation first; retain every prior route.
  stage['routes'].sort(key=lambda item:0 if item[0].startswith('v39:') else 1)
 if rev==40:stage['routes'].sort(key=lambda item:0 if item[0].startswith('v40:') else 1)
out=ROOT/f'deliverables/v0.0.{rev}';out.mkdir(parents=True,exist_ok=True)
def snapshot():
 bpy.context.view_layer.update();meshes={};result={}
 for o in bpy.data.objects:
  if o.type=='MESH' and o.data.name not in meshes:
   m=o.data;h=hashlib.sha256()
   for items,prop,mult,typ in [(m.vertices,'co',3,'f'),(m.loops,'vertex_index',1,'i'),(m.polygons,'loop_total',1,'i'),(m.polygons,'material_index',1,'i')]:
    a=array.array(typ,[0])*(len(items)*mult);items.foreach_get(prop,a);h.update(a.tobytes())
   for uv in m.uv_layers:
    a=array.array('f',[0])*(len(uv.data)*2);uv.data.foreach_get('uv',a);h.update(a.tobytes())
   h.update(str([m.name for m in m.materials]).encode());meshes[m.name]=h.hexdigest()
  result[o.name]={'type':o.type,'matrix':[list(r) for r in o.matrix_world],'geometry':meshes.get(o.data.name) if o.type=='MESH' else None,'modifiers':[(m.name,m.type) for m in o.modifiers],'hidden':(o.hide_render,o.hide_viewport)}
 return result
bpy.ops.wm.open_mainfile(filepath=str(ROOT/f'models/campus/WZMS_Campus_v{stage["previous"]:03}.blend'))
bpy.context.window.scene=bpy.data.scenes['WZMS_Campus'];before=snapshot()
allowed=set(json.loads((out/'replacement_scope.json').read_text(encoding='utf8'))['retired_objects']) if (out/'replacement_scope.json').exists() else set()
if rev>=40:
 scope=json.loads((out/'replacement_scope.json').read_text(encoding='utf8'))
 allowed.update(scope.get('modified_objects',[]));allowed.update(scope.get('transformed_objects',[]))
bpy.ops.wm.open_mainfile(filepath=str(ROOT/f'models/campus/WZMS_Campus_v{rev:03}.blend'))
sc=bpy.data.scenes['WZMS_Campus'];bpy.context.window.scene=sc;after=snapshot()
if rev>=34:
 centres=[]
 for number in range(1,9):
  col=bpy.data.collections['301_Basketball_8_Court_'+str(number)]
  obj=next(o for o in col.objects if o.name.startswith('Basketball red centre circle'))
  centre=obj.matrix_world@Vector((0,0,.037));centres.append([round(centre.x,3),round(centre.y,3)])
  assert centres[-1]==[[-1,30][(number-1)%2],[222,248,274,300][(number-1)//2]]
  for line in [o for o in col.objects if o.name.startswith('Basketball baseline')]:
   pts=[line.matrix_world@v.co for v in line.data.vertices]
   assert max(v.y for v in pts)-min(v.y for v in pts)>14.9 and max(v.x for v in pts)-min(v.x for v in pts)<.1
 semantic={'saved_file':bpy.data.filepath,'basketball_centres':centres,'basketball_count':8,'basketball_rotation_degrees':90}
 if rev>=35:
  courts=[o for o in sc.objects if 'Tennis violet doubles playing area' in o.name]
  actual=sorted((round(o.matrix_world.translation.x,3),round(o.matrix_world.translation.y,3)) for o in courts)
  if rev<40:
   assert actual==[(83,-1),(83,17),(119,-1),(119,17)],actual
   wall=sc.objects['Tennis middle solid dividing practice wall'];assert wall.dimensions.y>27.9 and wall.dimensions.z>3
  else:
   assert actual==[(74,8),(74,44),(92,8),(92,44)],actual
   def world_size(o):
    points=[o.matrix_world@v.co for v in o.data.vertices]
    return [max(p[i] for p in points)-min(p[i] for p in points) for i in range(3)]
   court_sizes=[world_size(o) for o in courts]
   assert all(abs(d[1]-23.77)<.02 and abs(d[0]-10.97)<.02 for d in court_sizes)
   wall=sc.objects['v040 tennis horizontal solid divider'];assert wall.dimensions.x>27.9 and wall.dimensions.y<.5 and wall.dimensions.z>3
   nets=[o for o in sc.objects if 'Tennis actual woven sagging net' in o.name]
   net_sizes=[world_size(o) for o in nets]
   assert len(nets)==4 and all(d[0]>12.7 and d[1]<.03 for d in net_sizes)
   semantic.update(tennis_rotation_degrees=90,tennis_long_axis='Y',tennis_net_count=4,tennis_world_dimensions=court_sizes,net_world_dimensions=net_sizes)
  semantic.update(tennis_centres=actual,tennis_count=4,solid_divider=True)
 semantic['all_passed']=True
 (out/'saved_layout_validation.json').write_text(json.dumps(semantic,indent=2),encoding='utf8')
changed=[x for x in before if before[x]!=after.get(x)];unexpected=[x for x in changed if x not in allowed]
pres={'baseline':f'v0.0.{stage["previous"]}','objects_checked':len(before),'changed_or_missing':changed,'approved_context_replacements':sorted(allowed),'unexpected_changes':unexpected,'all_unexpected_changes_absent':not unexpected,'new_objects':len(set(after)-set(before)),'scope':'Mesh coordinates, topology, UV, material slot assignments, object transforms, modifier identities, visibility; no blanket shader parameter or UE collision claim'}
(out/'preservation_validation.json').write_text(json.dumps(pres,ensure_ascii=False,indent=2),encoding='utf8')
# Build a bounded query using original evaluated geometry, not substitute floor planes.
pts=[p for _,route in stage['routes'] for p in route]
lo=[min(p[i] for p in pts)-(.6 if i<2 else 1) for i in range(3)];hi=[max(p[i] for p in pts)+(.6 if i<2 else 2.3) for i in range(3)]
corridors=[]
for _,route in stage['routes']:
 for a,b in zip(route,route[1:]):
  corridors.append(([min(a[i],b[i])-(.6 if i<2 else 1) for i in range(3)],[max(a[i],b[i])+(.6 if i<2 else 2.3) for i in range(3)]))
deps=bpy.context.evaluated_depsgraph_get();query=bpy.data.scenes.new('Temporary culture route query');candidates=[]
for o in sc.objects:
 if o.type!='MESH' or o.hide_viewport:continue
 ev=o.evaluated_get(deps);bounds=[ev.matrix_world@Vector(v) for v in ev.bound_box]
 oblo=[min(v[i] for v in bounds) for i in range(3)];obhi=[max(v[i] for v in bounds) for i in range(3)]
 if all(obhi[i]>=lo[i] and oblo[i]<=hi[i] for i in range(3)) and any(all(obhi[i]>=clo[i] and oblo[i]<=chi[i] for i in range(3)) for clo,chi in corridors):
  candidates.append((o,oblo,obhi))
  if rev!=40:query.collection.objects.link(o)
bpy.context.window.scene=query;bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();reports=[]
for name,poly in stage['routes']:
 if rev==40:
  # The same evaluated objects and conservative padding, scoped to this route.
  # Excluding distant routes reduces per-ray scene overhead without changing
  # sample spacing, clearances, actual geometry or longitudinal body sweeps.
  local_bounds=[([min(a[i],b[i])-(.6 if i<2 else 1) for i in range(3)],[max(a[i],b[i])+(.6 if i<2 else 2.3) for i in range(3)]) for a,b in zip(poly,poly[1:])]
  wanted={o for o,oblo,obhi in candidates if any(all(obhi[i]>=clo[i] and oblo[i]<=chi[i] for i in range(3)) for clo,chi in local_bounds)}
  current=set(query.objects)
  for o in current-wanted:query.collection.objects.unlink(o)
  for o in wanted-current:query.collection.objects.link(o)
  bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get()
 failures=[];count=0;last=None;lastpos=None;lastnormal=None
 for a,b in zip(poly,poly[1:]):
  a,b=Vector(a),Vector(b);d=b-a
  if d.length<1e-6:continue
  normal=Vector((-d.y,d.x,0)).normalized();steps=math.ceil(d.length/.14)
  for i in range(steps+1):
   q=a.lerp(b,i/steps);count+=1
   hit,pos,_,_,obj,_=query.ray_cast(deps,q+Vector((0,0,.24)),Vector((0,0,-1)),distance=.52)
   if not hit or abs(pos.z-q.z)>.23:
    failures.append(dict(at=list(q),reason='floor continuity',object=obj.name if obj else None,z=pos.z if hit else None));continue
   if last is not None and abs(pos.z-last)>.201:failures.append(dict(at=list(q),reason='step above 0.20m',delta=pos.z-last))
   last=pos.z
   hit,_,_,_,ob,_=query.ray_cast(deps,pos+Vector((0,0,.028)),Vector((0,0,1)),distance=1.72)
   if hit:failures.append(dict(at=list(q),reason='headroom',object=ob.name))
   for h in [.45,1.1,1.6]:
    for sign in [-1,1]:
     hit,_,_,_,ob,_=query.ray_cast(deps,pos+Vector((0,0,h)),normal*sign,distance=.35)
     if hit:failures.append(dict(at=list(q),reason='body width',object=ob.name))
   # Sweep longitudinal rays as well: thin uprights can fall between discrete samples.
   if lastpos is not None:
    for h in [.45,1.1,1.6]:
     for side in [-.34,0,.34]:
      aa=lastpos+Vector((0,0,h))+lastnormal*side;bb=pos+Vector((0,0,h))+normal*side;dd=bb-aa
      if dd.length<1e-6:continue
      hit,_,_,_,ob,_=query.ray_cast(deps,aa,dd.normalized(),distance=dd.length)
      if hit:failures.append(dict(at=list(q),reason='longitudinal body sweep',object=ob.name))
   lastpos=pos.copy();lastnormal=normal.copy()
  
 reports.append(dict(name=name,samples=count,failure_count=len(failures),failures=failures[:40],query_objects=len(query.objects)))
 print('CULTURE_ROUTE',name,count,'FAILURES',len(failures),failures[:4],flush=True)
 if rev==40 and failures:
  print('REFINEMENT_ROUTE_STOPPED_ON_FAILURE; remaining routes are not certified',flush=True)
  break
report=dict(version=f'v0.0.{rev}',routes=reports,all_passed=len(reports)==len(stage['routes']) and all(r['failure_count']==0 for r in reports),sample_spacing_max_m=.14,body_width_m=.70,headroom_m=1.72,step_limit_m=.20,ue_verified=False,query_objects=len(candidates),route_local_queries=rev==40,query_geometry='Original evaluated geometry within conservative segment bounds; 0.60m XY padding exceeds 0.35m query reach; v040 limits each query to the current route')
(out/'geometry_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
bpy.context.window.scene=sc;bpy.data.scenes.remove(query)
if unexpected or not report['all_passed']:raise RuntimeError('Culture audit failed: inspect JSON reports')
print('CULTURE_AUDIT_COMPLETE',rev,flush=True)
