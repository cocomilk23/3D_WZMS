"""Correct the court row and its building/shore relationships from two user photos."""
import bpy, sys, math, json
from pathlib import Path
from mathutils import Matrix
sys.path.insert(0, str(Path(__file__).parent))
import campus_common as c, island_common as h, south_detail_common as s, north_common as n

sc=bpy.data.scenes['WZMS_Campus']; c.activate(sc)
out=c.ROOT/'deliverables/v0.0.41'; out.mkdir(parents=True,exist_ok=True)
changes=dict(retired_objects=[],transformed_objects=[],modified_objects=[],
 reason='User ground panorama and aerial: four courts in a row along the school facade, long axes toward the facade; divider between courts two and three.')
def turn(x,y,angle):
 return Matrix.Translation((x,y,0))@Matrix.Rotation(angle,4,'Z')@Matrix.Translation((-x,-y,0))
precinct=turn(83,8,-math.pi/2)
for o in bpy.data.collections['360_Refined_Tennis_Four_Rotated_Courts'].objects:
 pivot=44 if o.name.startswith('v040 north ') else 8
 o.matrix_world=precinct@turn(83,pivot,math.pi/2)@o.matrix_world
 o['v041_orientation']='Court long axis Y toward school; four centres along X'
 changes['transformed_objects'].append(o.name)
old_fences=[]
for o in bpy.data.collections['361_Refined_Tennis_Enclosure_And_Divider'].objects:
 if o.name.startswith('v040 tennis cyan enclosure'):old_fences.append(o)
 else:
  o.matrix_world=precinct@o.matrix_world
  changes['transformed_objects'].append(o.name)
old_connections=[o for o in bpy.data.collections['362_Refined_Tennis_Heyu_Connections'].objects
 if o.name not in ('v040 closed entrance garden southern lawn','v040 entrance plaza garden boundary infill')]
retired=old_fences+old_connections
changes['retired_objects']=[o.name for o in retired]
bpy.data.batch_remove(ids=tuple(retired))
island=set()
for name in ['111_Heyu_Paths_And_Entry_Bridge','112_Heyu_Variegated_Banks_And_Lawn','113_Heyu_Banyans_And_Aerial_Roots','114_Heyu_Lotus_Beds','115_Heyu_Lights_And_Lifesaving']:
 island.update(bpy.data.collections[name].objects)
island.update(bpy.data.objects[name] for name in ['Heyu closed island soil and revetment','Heyu grass island top'])
for o in island:
 o.matrix_world=Matrix.Translation((0,-36,0))@o.matrix_world
 changes['transformed_objects'].append(o.name)

# Restore only the three prior shore surfaces. Reuse current refined materials.
materials={m.name:m for m in bpy.data.materials}
shore_names=['Heyu connected east lake surface','Tennis estimated east water continuation','Tennis water infill to existing diagonal shore']
with bpy.data.libraries.load(str(c.ROOT/'models/campus/WZMS_Campus_v035.blend'),link=False) as (src,dst):
 assert all(name in src.objects for name in shore_names)
 dst.objects=shore_names
c.collection('379_Tennis_Aerial_Corrected_Shore_And_Access')
for o in dst.objects:
 c.COL.objects.link(o)
 for i,m in enumerate(o.data.materials):
  base=m.name.rsplit('.',1)[0] if m.name.rsplit('.',1)[-1].isdigit() else m.name
  if base in materials:o.data.materials[i]=materials[base]
blue=materials['Tennis cyan enamel']; p=n.palette()
for a,b in [((65,-10),(137,-10)),((65,-10),(65,16)),((65,18),(65,26)),((65,26),(102.6,26)),((105.4,26),(137,26)),((137,-10),(137,26))]:
 s.wire_fence('v041 tennis blue boundary',a,b,4,blue)
s.bridge('v041 Heyu and utility connection',[(87,42),(104,42),(104,32)],2.4,miter=True,open_land_end=True)
s.bridge('v041 north tennis gateway',[(104,32),(104,26)],2.4)
s.ribbon('v041 retained utility branch',[(104,39),(106,39)],2.4,materials['Waterside fine rectangular granite'],-.01,.20)
c.box('v041 east court retaining bank',(137.25,8,-.8),(.45,36,1.6),p['stone'])

c.collection('380_Tennis_Orientation_Review_Cameras')
c.camera('183_Tennis_toward_school',(83,-3,1.72),(78,40,2.8),13.5)
cam=c.camera('184_Tennis_four_top_plan',(101,8,115),(101,8,0),40)
cam.data.type='ORTHO';cam.data.ortho_scale=91
c.camera('185_Tennis_aerial_relationships',(194,-110,127),(52,25,0),44)
sc['tennis_count']=4
sc['tennis_grid']='Four courts in one X row, centres (74,8),(92,8),(110,8),(128,8); long axis Y toward school; divider X=100.9'
sc['tennis_rotation_degrees']=90
sc['tennis_layout_authority']='User ground panorama and aerial screenshots received 2026-09-08'
sc['render_review_samples']=96
for key in ['retired_objects','transformed_objects','modified_objects']:changes[key]=sorted(set(changes[key]))
(out/'replacement_scope.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf8')
h.save(41,'Correct four-court arrangement using user ground panorama plus aerial. Four parallel courts face the school, divider separates second/third courts. Restore Heyu position and its earlier waterside access, retain v040 campus construction and surface refinement. Positions remain photographic estimates.',[347,348,359,364,365],'185_Tennis_aerial_relationships')
