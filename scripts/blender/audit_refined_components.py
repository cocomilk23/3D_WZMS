"""Saved-file checks for physical improvements, independent of construction functions."""
import bpy,json
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[2];out=R/'deliverables/v0.0.40'
if Path(bpy.data.filepath).name!='WZMS_Campus_v040.blend':bpy.ops.wm.open_mainfile(filepath=str(R/'models/campus/WZMS_Campus_v040.blend'))
sc=bpy.data.scenes['WZMS_Campus'];rows=[]
reveals=[o for o in sc.objects if o.name.startswith(('Window recessed opening','Window dark reveal'))]
assert len(reveals)==578
for o in reveals:
    mesh=o.data;tree=BVHTree.FromPolygons([v.co for v in mesh.vertices],[p.vertices[:] for p in mesh.polygons],all_triangles=False)
    depth=max(abs(v.co.y) for v in mesh.vertices)
    hit=tree.ray_cast(Vector((0,-depth-.02,0)),Vector((0,1,0)),2*depth+.04)
    assert hit[0] is None,o.name+' centre must be open'
seats=[o for o in sc.objects if o.name.startswith('Grandstand seat pan')]
backs=[o for o in sc.objects if o.name.startswith('Grandstand curved seat back')]
stools=[o for o in sc.objects if o.name.startswith('Dining cyan round stool')]
assert len(seats)==1452 and len(backs)==1452 and len(stools)==112
for o in seats[:3]:
    assert len(o.data.vertices)>100 and max(v.co.z for v in o.data.vertices)-min(v.co.z for v in o.data.vertices)>.035
    assert sum(p.normal.z for p in list(o.data.polygons)[:144])>100,'Seat upper normals must face up'
for o in stools:
    mesh=o.data
    centre=[v.co.z for v in mesh.vertices if v.co.x*v.co.x+v.co.y*v.co.y<.00001]
    rim=[v.co.z for v in mesh.vertices if v.co.x*v.co.x+v.co.y*v.co.y>.18*.18]
    assert max(rim)>max(centre)+.009,'Stool must be concave'
    assert sum(p.normal.z for p in list(mesh.polygons)[:128])>100,'Stool seat normals must face up'
assert not any(o.name.startswith('Dining stool concave inset') for o in sc.objects)
water=sc.objects['v040 continuous tennis and Heyu lake surface']
points=[water.matrix_world@v.co for v in water.data.vertices]
tree=BVHTree.FromPolygons(points,[p.vertices[:] for p in water.data.polygons],all_triangles=False)
for x,y in [(120,8),(145,20),(126,36),(66,85)]:
    hit=tree.ray_cast(Vector((x,y,0)),Vector((0,0,-1)),2)
    assert hit[0] is not None and abs(hit[0].z+1.15)<.001 and hit[1].z>.99,'Continuous lake surface gap or reversed normal'
for name,size in [('v040 closed entrance garden southern lawn',(14,18)),('v040 entrance plaza garden boundary infill',(13,2))]:
    o=sc.objects[name];assert abs(o.dimensions.x-size[0])<.001 and abs(o.dimensions.y-size[1])<.001
    assert abs(max((o.matrix_world@v.co).z for v in o.data.vertices)+.05)<.001
report={'all_passed':True,'saved_model':bpy.data.filepath,'hollow_reveal_centres_checked':len(reveals),'moulded_stadium_seats':len(seats),'moulded_stadium_backs':len(backs),'concave_stools_checked':len(stools),'seat_surfaces_face_up':True,'old_stool_discs_absent':True,'mesh_library_count_for_stadium_parts':len({o.data.name for o in seats+backs})}
report.update(continuous_water_points_checked=4,entrance_garden_gaps_closed=2)
(out/'component_validation.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print('REFINEMENT_COMPONENTS_PASSED',flush=True)
