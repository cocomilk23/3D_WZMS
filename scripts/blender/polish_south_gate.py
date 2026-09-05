"""Idempotent visual corrections after the first south gate render."""
import bpy
import random
import math
from mathutils import Vector

scene=bpy.data.scenes['WZMS_SouthGate_Sample']
scene.objects['Late morning sun'].rotation_euler=(math.radians(56),math.radians(-22),math.radians(-35))
wall=scene.objects['South gate · curved name wall']
uv=wall.data.uv_layers.active
for poly in wall.data.polygons:
    for li in poly.loop_indices:
        co=wall.data.vertices[wall.data.loops[li].vertex_index].co
        sx=(co.x+9)/18;sz=(co.z-.22)/4.85
        bow=1-(2*sx-1)**2
        top=.4025+.0105*bow;bottom=.5695+.008*bow
        uv.data[li].uv=(.1915+sx*.619,1-(bottom-sz*(bottom-top)))

if not scene.get('foliage_density_corrected'):
    rng=random.Random(884)
    for o in list(scene.objects):
        if o.type!='MESH' or 'foliage' not in o.name or len(o.data.polygons)<10000:
            continue
        source=o.data
        old=[v.co.copy() for v in source.vertices]
        vs=[]
        # Five vertices form each folded leaf. Increase its silhouette and add
        # a second nearby leaf without duplicating the whole tree object.
        for copy in range(2):
            for k in range(0,len(old),5):
                center=old[k+2]
                offset=Vector((0,0,0)) if copy==0 else Vector((rng.uniform(-.19,.19),rng.uniform(-.19,.19),rng.uniform(-.12,.12)))
                vs.extend([center+(old[k+j]-center)*1.3+offset for j in range(5)])
        fs=[tuple(p.vertices) for p in source.polygons]
        faces=fs+[tuple(i+len(old) for i in f) for f in fs]
        new=bpy.data.meshes.new(o.name+' dense canopy')
        new.from_pydata(vs,[],faces);new.update()
        for m in source.materials:new.materials.append(m)
        indices=[p.material_index for p in source.polygons]*2
        for p,i in zip(new.polygons,indices):p.material_index=i
        o.data=new
        if source.users==0:bpy.data.meshes.remove(source)
    scene['foliage_density_corrected']=True

world=scene.world
if not world.get('camera_sky_corrected'):
    n,l=world.node_tree.nodes,world.node_tree.links
    bg=next(x for x in n if x.type=='BACKGROUND')
    out=next(x for x in n if x.type=='OUTPUT_WORLD')
    camera=n.new('ShaderNodeLightPath')
    camera_bg=n.new('ShaderNodeBackground')
    camera_bg.inputs['Color'].default_value=(.14,.32,.59,1)
    camera_bg.inputs['Strength'].default_value=.8
    mix=n.new('ShaderNodeMixShader')
    l.new(camera.outputs['Is Camera Ray'],mix.inputs[0])
    l.new(bg.outputs[0],mix.inputs[1]);l.new(camera_bg.outputs[0],mix.inputs[2])
    l.new(mix.outputs[0],out.inputs['Surface'])
    world['camera_sky_corrected']=True
print('Visual corrections applied: wall crop, canopy density, clear camera sky.')
