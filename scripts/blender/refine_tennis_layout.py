"""Rotate the complete four-court precinct 90 degrees to follow the main road."""
import bpy,math
from mathutils import Matrix,Vector
import campus_common as c,north_common as n,south_detail_common as s,north_landscape as l

def refine_tennis(scene,changes):
    p=n.palette();blue=bpy.data.materials['Tennis cyan enamel'];green=bpy.data.materials['Tennis weathered sage surround']
    white=bpy.data.materials['Tennis warm white court paint']
    source=[o for o in bpy.data.collections['90_Tennis_Courts_And_Access'].objects if o.name.startswith(('Tennis violet','Tennis singles','Tennis baseline','Tennis service','Tennis centre'))]
    source+=list(bpy.data.collections['92_Tennis_Nets_And_Practice_Wall'].objects)
    rot=Matrix.Translation((83,8,0))@Matrix.Rotation(math.pi/2,4,'Z')@Matrix.Translation((-83,-8,0))
    c.collection('360_Refined_Tennis_Four_Rotated_Courts')
    for shift in [0,36]:
        for old in source:
            obj=old.copy();obj.name='v040 '+('north ' if shift else 'south ')+old.name;c.COL.objects.link(obj)
            obj.matrix_world=Matrix.Translation((0,shift,0))@rot@old.matrix_world
            obj['v040_detail']='Complete 90 degree rotated court component';obj['source_component']=old.name
    retired=set(source)
    for label in ['91_Tennis_Blue_Fencing','93_Tennis_Lights_And_Furniture','94_Tennis_Adjacent_Planting','311_Tennis_Additional_Two_Courts','312_Tennis_Extended_Base_And_Divider','313_Tennis_East_Lights_And_Border','316_Tennis_Heyu_Reconnected_Waterside_Bridge']:
        retired.update(bpy.data.collections[label].objects)
    retired.update(o for o in bpy.data.collections['90_Tennis_Courts_And_Access'].objects if o.name in ['Tennis raised aggregate foundation','Tennis two court continuous surround'])
    for name in ['Tennis estimated southern landscape infill','Tennis estimated east water continuation','Tennis water infill to existing diagonal shore']:
        retired.discard(bpy.data.objects[name])
    changes['retired_objects']+=sorted(o.name for o in retired)
    bpy.data.batch_remove(ids=tuple(retired))
    print('TENNIS_OLD_ASSEMBLY_REPLACED',len(retired),flush=True)
    # Retain the real island components; relocate the previously estimated island north.
    moved=set()
    for label in ['111_Heyu_Paths_And_Entry_Bridge','112_Heyu_Variegated_Banks_And_Lawn','113_Heyu_Banyans_And_Aerial_Roots','114_Heyu_Lotus_Beds','115_Heyu_Lights_And_Lifesaving']:
        moved.update(bpy.data.collections[label].objects)
    for name in ['Heyu closed island soil and revetment','Heyu grass island top']:moved.add(bpy.data.objects[name])
    for o in moved:
        o.matrix_world=Matrix.Translation((0,36,0))@o.matrix_world
        changes['transformed_objects'].append(o.name)
    print('TENNIS_ISLAND_RELOCATED',len(moved),flush=True)
    c.collection('361_Refined_Tennis_Enclosure_And_Divider')
    c.box('v040 four tennis continuous foundation',(83,26,-.28),(36.4,72.4,.52),p['stone'])
    c.box('v040 four tennis continuous green surround',(83,26,-.028),(36,72,.036),green)
    c.box('v040 tennis horizontal solid divider',(83,25.9,1.55),(28,.30,3.1),blue,.025)
    c.box('v040 tennis divider concrete coping',(83,25.9,3.12),(28.2,.42,.10),p['stone'],.025)
    for y in [25.738,26.062]:
        c.box('v040 divider net height line',(83,y,.914),(27.8,.008,.055),white)
        for x in [74,92]:
            for z in [1.45,2.0]:c.box('v040 divider target line',(x,y,z),(.55,.01,.035),white)
            for dx in [-.275,.275]:c.box('v040 divider target side',(x+dx,y,1.725),(.035,.01,.55),white)
    segments=[((65,-10),(101,-10)),((65,-10),(65,16)),((65,18),(65,62)),((65,62),(93.5,62)),((96.5,62),(101,62)),((101,-10),(101,62))]
    for a,b in segments:s.wire_fence('v040 tennis cyan enclosure',a,b,4,blue)
    for x in [65.15,100.85]:
        for y in [-9.5,26,61.5]:
            c.rod('v040 tennis tapered floodlight mast',(x,y,0),(x,y,7.2),.065,blue,.04,16)
            dx=.5 if x<80 else -.5
            c.rod('v040 tennis floodlight bracket',(x,y,7),(x+dx,y,7),.035,blue,sides=12)
            c.box('v040 floodlight ribbed aluminium housing',(x+dx,y,6.95),(.48,.32,.12),p['dark'],.02)
            c.box('v040 floodlight lens',(x+dx,y,6.883),(.42,.26,.008),white)
            for k in range(6):c.box('v040 floodlight heatsink fin',(x+dx-.18+k*.072,y,7.03),(.015,.30,.045),p['steel'])
    # Preserve the main road, using real outside paths and a northern bridge landing.
    c.collection('362_Refined_Tennis_Heyu_Connections')
    pave=bpy.data.materials['Waterside fine rectangular granite']
    c.box('v040 north court mainland support',(62,65,-.5),(6,42,.9),p['stone'])
    s.ribbon('v040 mainland path to relocated Heyu',[(62,47),(62,80),(63.5,80)],2.6,pave,-.01,.20)
    s.bridge('v040 Heyu east bridge',[(87,78),(106,78),(106,65.5)],2.4,miter=True)
    s.bridge('v040 court north gate bridge',[(104.5,64),(95,64),(95,62)],2.4,miter=True)
    s.bridge('v040 east waterside link',[(106,62.5),(106,39)],2.4,miter=True)
    c.box('v040 three way open bridge landing',(106,64,-.11),(3,3,.20),pave)
    s.glass_rail((107.5,62.5),(107.5,65.5),name='v040 junction outside guard')
    s.ribbon('v040 utility retained threshold link',[(106,39),(106,35)],2.4,pave,-.01,.20)
    c.box('v040 tennis east retaining bank',(101.25,26,-.8),(.45,72,1.6),p['stone'])
    for y in [4,44]:l.bench(63,y,math.pi/2)
    complete_tennis_shore(changes)
    scene['tennis_grid']='two north/south pairs, long axis Y; whole precinct rotated 90 degrees'
    scene['tennis_rotation_degrees']=90
    scene['tennis_count']=4

def complete_tennis_shore(changes):
    c.collection('362_Refined_Tennis_Heyu_Connections')
    baseline=['Heyu connected east lake surface','Tennis estimated east water continuation','Tennis water infill to existing diagonal shore']
    replaced=[bpy.data.objects[n] for n in baseline+['v040 east lake restored beneath old estimate','v040 relocated island surrounding water'] if n in bpy.data.objects]
    changes['retired_objects'].extend(n for n in baseline if n in bpy.data.objects)
    bpy.data.batch_remove(ids=tuple(replaced))
    # One union outline retains the existing lake footprint and closes the
    # estimated relocated island shore, without stacked refractive surfaces.
    outline=[(101,-10),(135,-10),(135,-31),(171,-31),(171,71),(135,71),(135,145),(90,145),(90,95),(64,95),(64,71),(61.9,71),(61.9,26),(101,26)]
    c.mesh('v040 continuous tennis and Heyu lake surface',[(x,y,-1.15) for x,y in outline],[tuple(range(len(outline)))],bpy.data.materials['Heyu green lake water'])
    c.mesh('v040 tennis and island lake bed extension',[(x,y,-2.75) for x,y in outline],[tuple(range(len(outline)))],n.palette()['seam'])
    # Fill two inherited gaps between the known plaza and garden edges.
    lawn=bpy.data.objects['East entrance garden ground'].data.materials[0]
    c.box('v040 closed entrance garden southern lawn',(42,-4,-.50),(14,18,.90),lawn)
    c.box('v040 entrance plaza garden boundary infill',(28.5,4,-.50),(13,2,.90),lawn)
