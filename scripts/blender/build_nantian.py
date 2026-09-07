"""v029 Nantian shaded avenue and west-batch integration; sports grounds remain next."""
import bpy,bmesh,math,sys,json
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).parent))
import campus_common as c,north_common as n,north_landscape as l,south_detail_common as s,island_common as h,west_common as w
sc=bpy.data.scenes['WZMS_Campus'];c.activate(sc);p=n.palette()
c.collection('250_Nantian_Road_And_Joined_Ground')
# Trim only the new east-west connection through the pre-existing planting strip.
retire=[];replacement_notes=[]
for name in ['Buqing western lawn','Buqing western low planting']:
    old=sc.objects[name];obj=old.copy();obj.data=old.data.copy();obj.name='Nantian trimmed '+name;c.COL.objects.link(obj)
    bm=bmesh.new();bm.from_mesh(obj.data);cut=[v for v in bm.verts if 161.65<(obj.matrix_world@v.co).y<166.35]
    bmesh.ops.delete(bm,geom=cut,context='VERTS');bm.to_mesh(obj.data);bm.free();obj.data.update();retire.append(name)
    replacement_notes.append({'old':name,'new':obj.name,'scope':'Remove only planting intersecting y161.65..166.35 connector; retain original remaining mesh coordinates and material assignments'})
for old in list(bpy.data.collections['46_Buqing_Trees_And_Furniture'].all_objects):
    if old.type!='MESH' or not old.name.startswith(('Buqing granite seat','Seat stone support','Buqing litter bin','Bin vertical metal slat')):continue
    pts=[old.matrix_world@Vector(v) for v in old.bound_box];q=sum(pts,Vector())/8
    if q.x<0 and 160<q.y<164:
        obj=old.copy();obj.name='Nantian relocated '+old.name;obj.location.y-=4;c.COL.objects.link(obj);retire.append(old.name)
        replacement_notes.append({'old':old.name,'new':obj.name,'scope':'Move roadside seat/bin four metres south, retaining mesh, to open Buqing connection'})
h.retire('v0.0.29',names=retire)
out=c.ROOT/'deliverables/v0.0.29';(out/'landscape_adjustments.json').write_text(json.dumps(replacement_notes,ensure_ascii=False,indent=2),encoding='utf8')
asphalt=s.mottled('Nantian fine weathered asphalt',[(.052,.06,.057),(.145,.155,.14)],3)
c.noise(asphalt,130,.21,.008)
concrete=n.paving('Nantian light entry paving',(.48,.48,.42),(.8,.5),.005)
grass=s.mottled('Nantian shaded verge soil',[(.07,.10,.026),(.19,.22,.067)],2)
paint=c.material('Nantian worn ivory lane paint',(.71,.70,.62),.86)
s.ribbon('Nantian continuous roadside ground',[(-20,146),(-20,350)],16,grass,-.04,1.6)
# Continuous ground between the new road, existing plaza/courts, and the
# photographed sports-side verge. These are estimated landscape infills.
# Keep infills below the existing -0.04m ribbon tops to avoid coplanar surfaces.
c.box('Nantian Jiangkou junction ground infill ESTIMATED',(18.5,193.5,-.88),(71,27,1.6),grass)
c.box('Nantian alumni north ground transition ESTIMATED',(-50.5,182.5,-.88),(45,17,1.6),grass)
s.ribbon('Nantian continuous asphalt avenue',[(-20,146),(-20,350)],5.6,asphalt,.03,.22)
branches=[('Buqing entry',[(-20,164),(3,164)],4.4,concrete),('Jiangkou join',[(-20,200),(8,200)],3.6,concrete),('Track gate one',[(-20,218),(-36,218)],4.5,concrete),('Track gate three',[(-20,318),(-36,318)],4.5,concrete),('Basketball reserved branch',[(-20,330),(-3,330)],3.2,concrete),('Gym reserved branch',[(-20,346),(-43,346)],4.0,concrete)]
for name,poly,width,mat in branches:
    s.ribbon('Nantian '+name+' ground',poly,width+1.8,grass,-.04,1.5)
    s.ribbon('Nantian '+name+' paving',poly,width,mat,.03,.20)
for y in range(149,350,4):
    if any(abs(y-j)<3 for j in [160,164,200,218,318,330,346]):continue
    c.box('Nantian broken centre line',(-20,y,.037),(.11,1.7,.012),paint)
gaps=[(156,168),(197,203),(215,221),(315,321),(327,333),(343,349)]
segments=[];start=146
for lo,hi in gaps:
    if lo>start:segments.append((start,lo))
    start=hi
if start<350:segments.append((start,350))
for side in [-1,1]:
    for lo,hi in segments:s.ribbon('Nantian low continuous stone kerb',[(-20+side*2.95,lo),(-20+side*2.95,hi)],.20,p['stone'],.12,.24)
c.collection('251_Nantian_Buqing_Entry_Portal')
white=c.material('Nantian entry ivory stone',(.66,.67,.60),.77)
green=c.material('Nantian entry blue green glass',(.055,.24,.25),.20,.24)
for y in [158.7,169.3]:c.box('Nantian visible portal pier',(-13,y,4.25),(3.4,.70,8.5),white)
c.box('Nantian elevated portal floor',(-13,164,4.80),(3.4,11.4,.24),white)
c.box('Nantian elevated portal roof',(-13,164,8.52),(3.4,11.4,.22),white)
for x in [-14.74,-11.26]:
    c.box('Nantian upper bridge green glazing',(x,164,6.26),(.028,10.25,2.82),green)
    for y in [158.9+i*.91 for i in range(12)]:c.box('Nantian bridge glazing upright',(x, min(y,169.1),6.26),(.09,.05,2.82),p['steel'])
    for z in [5.02,5.85,6.68,7.43]:c.box('Nantian bridge glazing horizontal',(x,164,z),(.09,10.3,.045),p['steel'])
    # Source 376 has a curved top edge above the green glazed bridge.
    points=[];fascia_x=x+(-.055 if x<-13 else .055)
    for i in range(49):
        t=i/48;y=158.85+10.3*t;z=7.3+.40*math.sin(math.pi*t);points.extend([(fascia_x,y,z),(fascia_x,y,8.5)])
    c.mesh('Nantian curved white bridge fascia',points,[(2*i,2*i+2,2*i+3,2*i+1) for i in range(48)],white)
for y in [161,164,167]:c.box('Nantian portal soffit light',(-13,y,4.67),(.22,.22,.025),p['white'])
c.collection('252_Nantian_Banyan_Avenue_And_Low_Planting')
proto=[sc.objects['Rongyu spreading old banyan connected trunks roots and twigs'],sc.objects['Rongyu spreading old banyan attached broadleaf canopy']]
whitewash=proto[0].data.materials[0].copy();whitewash.name='Nantian bark with photographed limewashed roots'
nd=whitewash.node_tree.nodes;ln=whitewash.node_tree.links;bs=nd['Principled BSDF'];base=bs.inputs['Base Color'].links[0].from_socket
geo=nd.new('ShaderNodeNewGeometry');xyz=nd.new('ShaderNodeSeparateXYZ');ln.new(geo.outputs['Position'],xyz.inputs[0])
threshold=nd.new('ShaderNodeMath');threshold.operation='LESS_THAN';threshold.inputs[1].default_value=1.1;ln.new(xyz.outputs['Z'],threshold.inputs[0])
mix=nd.new('ShaderNodeMixRGB');mix.blend_type='MIX';mix.inputs[2].default_value=(.64,.66,.60,1)
ln.new(base,mix.inputs[1]);ln.new(threshold.outputs[0],mix.inputs[0]);ln.new(mix.outputs[0],bs.inputs['Base Color'])
for j,y in enumerate(range(182,341,14)):
    for sign in [-1,1]:
        if any(abs(y-branch)<5 for branch in [200,218,318,330,346]):continue
        x=-20+sign*6.2;scale=.80+(j%3)*.025;angle=j*.84+sign*.3
        for original in proto:
            obj=original.copy();obj.name='Nantian avenue '+original.name;c.COL.objects.link(obj)
            obj.location=(x,y,0);obj.rotation_euler.z=angle;obj.scale=(scale,scale,scale)
            if original==proto[0]:
                for slot in obj.material_slots:slot.link='OBJECT';slot.material=whitewash
        w.meadow('Nantian low grass clump',x,y,1.45,2.35,.03,2900+j*3+sign)
c.collection('253_Nantian_Fence_And_Reserved_Sports_Entries')
# This is the photographed edge only, not a completed track or playing field.
c.box('Nantian western athletic verge CONTEXT_ESTIMATED',(-49.5,269.5,-.44),(47,161,.7),grass)
fence=c.material('Nantian green sports fence',(.025,.13,.062),.46,.37)
for lo,hi in [(190,215),(221,315),(321,340)]:s.wire_fence('Nantian sports boundary',(-32,lo),(-32,hi),1.8,fence,.14)
for number,y in [(1,218),(3,318)]:
    for yy in [y-3,y+3]:c.box('Nantian sports entrance gatepost',(-32,yy,1.04),(.18,.18,2.08),fence)
    disc=n.disk('Nantian gate number disc',0,0,0,.34,c.material('Nantian blue gate number enamel',(.035,.075,.28),.51),48)
    disc.location=(-31.89,y+3,1.72);disc.rotation_euler=(0,math.pi/2,0)
    c.text('Nantian observed gate number',str(number),(-31.865,y+3,1.57),.27,p['white'],(math.pi/2,0,math.pi/2))
c.collection('254_Nantian_Road_Furniture')
blue=c.material('Nantian blue parking sign',(.022,.12,.32),.48)
c.box('Nantian parking pole',(-25,151,1.6),(.06,.06,3.2),p['steel'])
c.box('Nantian parking sign',(-25,151,2.9),(.72,.06,.72),blue)
c.text('Nantian observed parking P','P',(-25,150.961,2.66),.53,p['white'])
for y in [184,240,296]:
    x=-15;c.rod('Nantian banner mast',(x,y,0),(x,y,5.1),.035,p['steel'])
    for sign,col in [(-1,(.02,.13,.32)),(1,(.38,.035,.045))]:
        mat=c.material('Nantian banner '+str(sign),col,.78)
        c.box('Nantian observed colour banner',(x+sign*.30,y,3.7),(.48,.025,1.45),mat)
        c.rod('Nantian banner upper arm',(x,y,4.5),(x+sign*.59,y,4.5),.018,p['steel'])
for y in [176,232,286,336]:s.slit_lamp(-23.9,y)
for y in [180,240,300]:
    c.box('Nantian roadside storm drain',(-17.45,y,.038),(.35,.75,.035),p['dark'])
    for j in range(12):c.box('Nantian storm grate crossbar',(-17.45,y-.34+j*.061,.059),(.34,.016,.016),p['steel'])
c.collection('258_West_Batch_Review_Cameras')
c.camera('115_Nantian_shaded_avenue',(-20,225,1.7),(-20,286,2.3),30)
c.camera('116_Nantian_Buqing_portal',(-28,164,1.7),(-13,164,4.0),22)
c.camera('117_Nantian_Jiangkou_connection',(-10,200,1.7),(-23,205,2),27)
c.camera('118_Nantian_sports_edge',(-20,307,1.7),(-30,320,2),28)
c.camera('119_West_precinct_overview',(-138,74,108),(-18,185,0),34)
c.camera('120_Campus_integrated_v029',(-225,-100,370),(105,150,0),28)
h.save(29,'Integrated west batch. Nantian asphalt, shade avenue, Buqing entry bridge and links to Alumni, Jiangkou and future sports entries based on 376-379. Two planting meshes trimmed for the new connector and seat/bin shifted locally. Field and gym interiors not delivered; scale image-estimated.',[376,377,378,379,374,386,355,347,348],'120_Campus_integrated_v029')
