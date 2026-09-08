"""v040 physical surface refinements, preserving all source-image materials."""
import bpy, math

def refine_surfaces(scene):
    protected=set(scene.objects['South name wall reverse photo surface'].data.materials)
    changed=[]
    used={m for o in scene.objects if o.type=='MESH' for m in o.data.materials if m}
    for m in sorted(used,key=lambda x:x.name):
        if not m.use_nodes or m in protected:continue
        nd,lk=m.node_tree.nodes,m.node_tree.links
        bs=next((n for n in nd if n.type=='BSDF_PRINCIPLED'),None)
        if bs is None or any(n.type=='TEX_IMAGE' for n in nd):continue
        name=m.name.lower();kind=None
        if ('water' in name or 'lake' in name) and 'waterside' not in name and not any(t in name for t in ['rail','glass','bank','stone','pav','bridge','lamp','glaz','bed','silt']):kind='water'
        elif any(t in name for t in ['leaf','foliage','frond','groundcover']) and 'pale margin' not in name:kind='leaf'
        elif any(t in name for t in ['timber','oak','hardwood','walnut','wood']) and 'bamboo' not in name:kind='wood'
        elif any(t in name for t in ['upholstery','cushion','curtain','canvas','woven blue']):kind='fabric'
        elif any(t in name for t in ['glazing','glass']) and 'frost' not in name:kind='glass'
        elif any(t in name for t in ['stainless','brushed','silver','steel','aluminium','aluminum']):kind='metal'
        elif any(t in name for t in ['plaster','stucco','concrete','granite','limestone','stone','render','pavers','paving','tiles','ceramic','ashlar','brick']):kind='mineral'
        elif any(t in name for t in ['enamel','coat','plastic','moulded','cyan seats','ivory frames']):kind='paint'
        elif any(t in name for t in ['soil','planted ground','grass base','lawn','ground green']):kind='soil'
        if kind is None:continue
        co=nd.new('ShaderNodeTexCoord');co.name='v040 physical coordinates'
        noise=nd.new('ShaderNodeTexNoise');noise.name='v040 microscopic variation';noise.inputs['Detail'].default_value=3
        lk.new(co.outputs['Object'],noise.inputs['Vector'])
        noise.inputs['Scale'].default_value={'water':.7,'leaf':48,'wood':3,'fabric':200,'glass':1.8,'metal':90,'mineral':110,'paint':150,'soil':4}[kind]
        old_color=bs.inputs['Base Color'].links[0].from_socket if bs.inputs['Base Color'].is_linked else None
        color=tuple(bs.inputs['Base Color'].default_value)
        if kind in ('wood','fabric'):
            stretch=nd.new('ShaderNodeVectorMath');stretch.operation='MULTIPLY'
            stretch.inputs[1].default_value=(2,95,16) if kind=='wood' else (1,1,1)
            lk.new(co.outputs['Generated'] if kind=='wood' else co.outputs['Object'],stretch.inputs[0]);lk.new(stretch.outputs[0],noise.inputs['Vector'])
        if kind=='wood':
            # Replace brick-like timber mapping by grain continuous across each member.
            previous=next((n for n in nd if n.type=='VALTORGB'),None)
            base=tuple(sum(e.color[j] for e in previous.color_ramp.elements)/len(previous.color_ramp.elements) for j in range(3)) if previous else tuple(m.diffuse_color[:3])
            ramp=nd.new('ShaderNodeValToRGB')
            ramp.color_ramp.elements[0].color=(*(v*.48 for v in base),1)
            ramp.color_ramp.elements[1].color=(*(min(v*1.28,.75) for v in base),1)
            lk.new(noise.outputs['Fac'],ramp.inputs[0]);lk.new(ramp.outputs['Color'],bs.inputs['Base Color'])
            bs.inputs['Roughness'].default_value=.52
            bs.inputs['Coat Weight'].default_value=.10
        elif kind=='glass':
            bs.inputs['Base Color'].default_value=(.76,.86,.82,1)
            bs.inputs['Metallic'].default_value=0;bs.inputs['Transmission Weight'].default_value=.90
            bs.inputs['IOR'].default_value=1.46;bs.inputs['Roughness'].default_value=.055
            bs.inputs['Coat Weight'].default_value=.18
        elif kind=='water':
            bs.inputs['Base Color'].default_value=(.045,.092,.068,1)
            for link in list(bs.inputs['Base Color'].links):lk.remove(link)
            bs.inputs['Roughness'].default_value=.13;bs.inputs['IOR'].default_value=1.333
            bs.inputs['Metallic'].default_value=.10;bs.inputs['Transmission Weight'].default_value=.22
            bs.inputs['Coat Weight'].default_value=.4
            stretch=nd.new('ShaderNodeVectorMath');stretch.operation='MULTIPLY';stretch.inputs[1].default_value=(1,5,.5)
            lk.new(co.outputs['Object'],stretch.inputs[0]);lk.new(stretch.outputs[0],noise.inputs['Vector'])
        else:
            ramp=nd.new('ShaderNodeValToRGB');ramp.name='v040 restrained surface mottling'
            lo,hi=(.70,1.12) if kind in ('leaf','soil') else (.86,1.04)
            ramp.color_ramp.elements[0].color=(lo,lo,lo,1);ramp.color_ramp.elements[1].color=(hi,hi,hi,1)
            lk.new(noise.outputs['Fac'],ramp.inputs[0])
            mix=nd.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1
            if old_color:lk.new(old_color,mix.inputs[1])
            else:mix.inputs[1].default_value=color
            lk.new(ramp.outputs[0],mix.inputs[2]);lk.new(mix.outputs[0],bs.inputs['Base Color'])
            if kind=='leaf':
                bs.inputs['Subsurface Weight'].default_value=.16;bs.inputs['Roughness'].default_value=.47
                bs.inputs['Subsurface Radius'].default_value=(.7,1,.3)
            elif kind=='fabric':bs.inputs['Sheen Weight'].default_value=.35;bs.inputs['Roughness'].default_value=.85
            elif kind=='metal':bs.inputs['Metallic'].default_value=.82;bs.inputs['Roughness'].default_value=.28;bs.inputs['Anisotropic'].default_value=.35
        if kind!='glass':
            bump=nd.new('ShaderNodeBump');bump.name='v040 fine normal detail'
            bump.inputs['Strength'].default_value=.20
            bump.inputs['Distance'].default_value={'water':.022,'leaf':.0006,'wood':.0012,'fabric':.00035,'metal':.0002,'mineral':.0012,'paint':.0003,'soil':.008}[kind]
            if bs.inputs['Normal'].is_linked and kind not in ('water','wood'):
                lk.new(bs.inputs['Normal'].links[0].from_socket,bump.inputs['Normal'])
            lk.new(noise.outputs['Fac'],bump.inputs['Height']);lk.new(bump.outputs[0],bs.inputs['Normal'])
        m['v040_surface_family']=kind;changed.append({'material':m.name,'family':kind})
    return changed
