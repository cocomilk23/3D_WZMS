"""v040: campus-wide material/construction pass and full tennis precinct rotation."""
import bpy,sys,json,math,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import campus_common as c,island_common as h
from refine_tennis_layout import refine_tennis
from refine_component_library import refine_components
from refine_surface_library import refine_surfaces

sc=bpy.data.scenes['WZMS_Campus'];c.activate(sc)
changes={'retired_objects':[],'transformed_objects':[],'modified_objects':[],
 'reason':'User authorized whole-campus realism pass and full 90 degree tennis rotation; dated 2026-09-08.'}
out=c.ROOT/'deliverables/v0.0.40';out.mkdir(parents=True,exist_ok=True)
refine_tennis(sc,changes);print('REFINED_TENNIS_GEOMETRY',flush=True)
bpy.context.view_layer.update()
stats=refine_components(sc,changes);print('REFINED_CONSTRUCTION',stats,flush=True)
tennis_enamel=bpy.data.materials['Tennis cyan enamel']
tennis_enamel.diffuse_color=(.015,.15,.34,1)
tennis_enamel.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.015,.15,.34,1)
materials=refine_surfaces(sc);print('REFINED_SURFACES',len(materials),flush=True)
# A gentler sun avoids bleaching pale masonry. Source photos remain unchanged.
sun=sc.objects.get('Campus clear morning sun')
if sun:
 sun.data.energy=2.6;sun.data.angle=math.radians(.7)
sc.world=sc.world.copy();sc.world.name='v040 balanced campus daylight'
for node in sc.world.node_tree.nodes:
 if node.type=='BACKGROUND':node.inputs['Strength'].default_value=.22
sc.view_settings.exposure=-.25
c.collection('378_Refined_Campus_Review_Cameras')
c.camera('169_Tennis_rotated_precinct',(140,-31,85),(83,30,0),38)
c.camera('170_Tennis_baseline_and_divider',(74,-5,1.72),(74,22,1.3),26)
c.camera('171_Tennis_island_and_connections',(143,105,54),(86,48,0),36)
c.camera('172_Refined_facade_windows',(-33,42,7),(-31,52.5,6.4),36)
c.camera('173_Refined_ac_and_upper_facade',(6,200,5.1),(9.6,193.4,4.6),38)
c.camera('174_Refined_moulded_grandstand',(-136.5,246.5,2.2),(-139,245,2.0),32)
# Keep established review viewpoints for comparisons; do not overwrite their objects.
aliases=[('175_Refined_south_gate','01_Front_reference'),('176_Refined_library','67_Library_ground_hall'),('177_Refined_landscape','104_Rongyu_banyan_walk'),('178_Refined_math_furniture','158_Math_upper_rest_corner'),('179_Refined_canteen','165_Canteen_blue_stool_detail'),('180_Refined_history','160_History_century_and_miniatures'),('181_Refined_gym','150_Gym_upper_sports_hall'),('182_Refined_whole_campus','168_Campus_integrated_v039')]
for name,source in aliases:
 if source not in sc.objects:
  if name=='175_Refined_south_gate':source='05_Plaza_from_gate'
  else:raise KeyError(source)
 old=sc.objects[source];obj=old.copy();obj.data=old.data.copy();obj.name=name;c.COL.objects.link(obj)
changes['retired_objects']=sorted(set(changes['retired_objects']))
changes['transformed_objects']=sorted(set(changes['transformed_objects']))
changes['modified_objects']=sorted(set(changes['modified_objects']))
(out/'replacement_scope.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf8')
(out/'refinement_manifest.json').write_text(json.dumps({'construction':stats,'materials':materials,'surface_count':len(materials),'scope':'All existing main-campus scene families; inferred hardware and construction detailing. No new unknown rooms, no Xinjiang work, no survey claim.','tennis_layout':'two pairs along the road; each 23.77m long axis Y; centres (74,8),(92,8),(74,44),(92,44); horizontal divider Y=25.9','protected_south_wall':True},ensure_ascii=False,indent=2),encoding='utf8')
sc['realism_revision']='v040 material and physical construction refinement'
sc['render_review_samples']=96
h.save(40,'Campus-wide realism refinement: hollow window reveals, seals and latches, pleated curtains, condenser wire guards and mountings, manufactured edge radii, roof coping, moulded stadium and dining seats, school furniture joinery, sofa cushions/piping, miniature fenestration, PBR surface layers. Entire tennis precinct rotated 90 degrees along road; north island connection explicitly revised. Unknown rooms remain unclaimed; source-backed exhibits and deferred south wall retained.',[347,349,352,354,357,359,364,365,393,394,397,403,417,427],'182_Refined_whole_campus')
