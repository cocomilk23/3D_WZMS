"""v0.0.4: connected south inner plaza, from original panoramas 352/353.
Run with the v0.0.2 Blender file as input. Does not modify that snapshot.
"""
import sys, math, json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import bpy
import campus_common as c
scene=bpy.data.scenes['WZMS_SouthGate_Sample'];scene.name='WZMS_Campus'
c.activate(scene)
for col in scene.collection.children:
    if col.name.endswith('.001'):col.name=col.name[:-4]
# Use a fresh explicit daylight source; old light node state is not inherited.
old_sun=scene.objects.get('Late morning sun')
if old_sun:bpy.data.objects.remove(old_sun,do_unlink=True)
c.collection('07_Lighting')
ld=bpy.data.lights.new('Campus clear morning sun','SUN');ld.energy=4.0;ld.angle=.018
lo=bpy.data.objects.new('Campus clear morning sun',ld);c.COL.objects.link(lo)
lo.rotation_euler=(math.radians(36),math.radians(-25),math.radians(-35))
for n in scene.world.node_tree.nodes:
    if n.type=='BACKGROUND' and n.name=='Background':n.inputs['Strength'].default_value=.085
# Retire the estimated inner landscape and solid backdrop. Outer gate stays intact.
for colname in ['05_Landscape','06_Background']:
    col=bpy.data.collections[colname]
    for o in list(col.objects):
        if colname=='05_Landscape' and (o.name.startswith(('Round forecourt','Island border','Forecourt central'))):continue
        bpy.data.objects.remove(o,do_unlink=True)
ground=scene.objects['Entrance plaza']
# Existing slab ended at y=34; trim to y=3. New slab starts there at the same -0.01 top.
ground.scale.y=35/66;ground.location.y=-14.5
for o in list(bpy.data.collections['01_Ground'].objects):
    if o.name.startswith('Drive edge band'):bpy.data.objects.remove(o,do_unlink=True)
    elif o.name.startswith(('Tactile tile','Tactile raised')) and o.location.y>2.7:bpy.data.objects.remove(o,do_unlink=True)
stone=c.material('Plaza pale fine granite',(.58,.57,.51),.84);c.noise(stone,90,.17,.012)
edge=c.material('Plaza blue-grey stone bands',(.23,.27,.28),.82);c.noise(edge,85,.2,.012)
soil=c.material('Planting soil',(.06,.044,.025),1)
dark=c.material('Graphite painted metal',(.032,.044,.052),.34,.65)
wood=c.material('Oiled dark timber',(.085,.032,.016),.65);c.noise(wood,18,.2,.006)
silver=c.material('Brushed stainless steel',(.46,.5,.51),.29,.85)
paving=c.material('South plaza warm ashlar',(.48,.46,.39),.86)
n,l=paving.node_tree.nodes,paving.node_tree.links;p=next(n for n in n if n.type=='BSDF_PRINCIPLED')
t=n.new('ShaderNodeTexCoord');b=n.new('ShaderNodeTexBrick')
b.inputs['Color1'].default_value=(.53,.52,.46,1);b.inputs['Color2'].default_value=(.37,.39,.37,1)
b.inputs['Mortar'].default_value=(.21,.23,.22,1);b.inputs['Scale'].default_value=1
b.inputs['Mortar Size'].default_value=.003;b.inputs['Brick Width'].default_value=.9;b.inputs['Row Height'].default_value=.45
l.new(t.outputs['Object'],b.inputs['Vector']);l.new(b.outputs['Color'],p.inputs['Base Color'])
bn=n.new('ShaderNodeBump');bn.inputs['Strength'].default_value=.35;bn.inputs['Distance'].default_value=.011
l.new(b.outputs['Fac'],bn.inputs['Height']);l.new(bn.outputs['Normal'],p.inputs['Normal'])
c.collection('10_Plaza_Paving')
c.box('Inner plaza slab · y3 to y52',(0,27.5,-.16),(44,49,.3),paving)
for x in [-10,-3.9,3.9,10]:c.box('Continuous granite longitudinal band',(x,27.5,-.010),(.22,49,.004),edge)
for y in [5,15,25,35,45,51]:c.box('Cross band',(0,y,-.010),(22,.22,.004),edge)
# Flush square maintenance covers with recessed lifting eyes.
for x,y in [(2.7,18),(-2.2,33),(8.9,42),(-9.1,12)]:
    c.box('Recessed service frame',(x,y,-.025),(.77,.77,.03),edge,.004)
    c.box('Granite inset service cover',(x,y,-.014),(.72,.72,.01),stone,.002)
    for dx in [-.23,.23]:c.box('Recessed lifting slot',(x+dx,y,-.008),(.06,.022,.002),dark)
for side in [-1,1]:
    c.box('Outer planted lawn soil',(side*16.5,27,-.03),(10,42,.1),soil)
    c.box('Lawn base',(side*16.5,27,.023),(9.9,41.9,.02),c.material('Lawn soil green',(.11,.17,.04)))
    c.grass('Lawn individual blades',(side*16.5,27),(9.9,41.9),21+side)
    c.box('Outer garden kerb',(side*21.7,27,.04),(.18,42,.12),stone,.025)
c.collection('11_Plaza_Tree_Islands')
for side in [-1,1]:
    for j,y in enumerate([10,20,30,40]):
        x=side*6.3
        c.box('Sunken rectangular tree soil',(x,y,-.005),(3.25,5.5,.07),soil)
        c.planting('Low rectangular groundcover',(x,y),(3.25,5.5),.29,100+j+side*10,950)
        c.tree('Plaza row %s-%s'%(side,j),x,y,7.8+(j%2)*.6,1.85,400+j+side*25)
c.collection('12_Plaza_Furniture')
def lamp(x,y):
    c.box('Garden light solid pedestal',(x,y,.73),(.18,.18,1.46),dark,.015)
    for dx in [-.078,.078]:c.box('Garden light open frame',(x+dx,y,2.25),(.024,.10,1.6),dark,.006)
    c.box('Garden light top hood',(x,y,3.1),(.21,.18,.24),dark,.01)
    c.box('Garden light lens',(x,y,2.98),(.13,.11,.024),c.material('Garden light opal lens',(.76,.74,.62),.35))
for side in [-1,1]:
    for j,y in enumerate([10,20,30,40]):
        x=side*6.3;by=y-3.16
        for dx in [-1.37,1.37]:c.box('Bench granite end',(x+dx,by,.24),(.42,.62,.48),stone,.028)
        for k in range(5):c.box('Bench timber seat plank',(x,by-.24+k*.12,.44),(2.34,.105,.065),wood,.009)
        for z in [.15,.26,.37]:c.box('Bench timber apron',(x,by-.305,z),(2.3,.045,.09),wood,.005)
        lamp(x-side*1.1,y+2)
        for dx in [-1.22,1.22]:
            for dy in [-.19,.19]:c.rod('Bench fixing bolt',(x+dx,by+dy,.479),(x+dx,by+dy,.486),.009,silver,sides=8)
# Information boards are modeled frames; contents remain explicitly undeciphered.
for j in range(5):
    x=13.1;y=9+j*4.9
    for dy in [-1.5,1.5]:c.box('Noticeboard timber post',(x,y+dy,1.23),(.16,.16,2.46),wood,.018)
    c.box('Noticeboard frame',(x,y,1.57),(.16,3.18,1.43),wood,.02)
    c.box('Noticeboard cream display',(x-.095,y,1.56),(.021,2.93,1.15),stone)
    c.box('Noticeboard header',(x-.109,y,2.03),(.008,2.87,.20),c.material('Notice burgundy',(.19,.025,.02)))
    for k in range(3):c.box('Notice panel division',(x-.11,y-.93+k*.93,1.49),(.01,.018,.88),wood)
    # Physical glazed sheet; small printed notices deferred instead of invented writing.
    o=c.box('Notice glazing',(x-.12,y,1.55),(.005,2.89,1.13),c.material('Noticeboard subtle glass',(.36,.42,.39),.21,.25))
c.box('Garden display housing',(-13.1,17,2.45),(.30,5.1,2.8),silver,.04)
c.box('Garden display reverse',(-12.93,17,2.45),(.028,4.86,2.57),edge)
for y in [15.3,18.7]:c.rod('Display stand',(-13.1,y,.04),(-13.1,y,1.13),.09,silver)
for side in [-1,1]:
    for y in [12,37]:
        x=side*11.1
        c.box('Campus litter bin',(x,y,.53),(.55,.52,1.06),dark,.045)
        c.box('Litter opening',(x,y-.27,.83),(.38,.035,.19),soil,.02)
        c.box('Bin stainless top',(x,y,1.065),(.56,.53,.06),silver,.018)
# Wall reverse: original photographed relief/anniversary panel, packed unchanged.
c.collection('14_Plaza_Wall_Reverse')
im=bpy.data.images.load(str(c.ROOT/'reference/panoramas/faces/119232353/r.jpg'),check_existing=True);im.pack()
wm=c.material('South wall reverse · photographed 119232353',(.6,.59,.54),.85)
wn,wl=wm.node_tree.nodes,wm.node_tree.links;wp=next(n for n in wn if n.type=='BSDF_PRINCIPLED')
it=wn.new('ShaderNodeTexImage');it.image=im;wl.new(it.outputs['Color'],wp.inputs['Base Color'])
verts=[]
for i in range(41):
    x=-9+i*.45;y=.38*(x/9)**2+.64;verts.extend([(x,y,.22),(x,y,5.07)])
faces=[(2*i,2*i+1,2*i+3,2*i+2) for i in range(40)]
wall=c.mesh('South name wall reverse photo surface',verts,faces,wm)
uv=wall.data.uv_layers.new(name='Original photograph UV')
# Source wall from viewed north side: image left corresponds to model +X.
for p in wall.data.polygons:
    for li in p.loop_indices:
        co=wall.data.vertices[wall.data.loops[li].vertex_index].co
        sx=(9-co.x)/18;sz=(co.z-.22)/4.85
        u=.665+sx*.197;top=.477-sx*.012;bottom=.529-sx*.004
        uv.data[li].uv=(u,1-(bottom-sz*(bottom-top)))
wall['reference_limit']='Photo projection; tree occlusions and perspective remain, not sculpted relief'
c.collection('13_Plaza_Mature_Gardens')
for side in [-1,1]:
    for j,y in enumerate([11,27,43]):c.tree('Garden broadleaf %d %d'%(side,j),side*(17+(j%2)*1.5),y,9.2+j*.5,3.7,800+side*50+j,True)
    c.planting('Garden low border',(side*11.8,27),(1.2,40),.42,98+side,250)
# The next delivery replaces this explicitly named context block with the observed facade.
c.collection('19_Portal_Context_PENDING_FACADE')
for side in [-1,1]:c.box('Portal context side pier',(side*9.5,56,8.7),(4,8,17.4),stone)
c.box('Portal context elevated span',(0,56,15),(15,8,4.8),c.material('Muted teal glazing',(.10,.26,.25),.2,.38))
for i in range(7):c.box('Portal approach step',(0,49.2+i*.4,(i+1)*.075),(15,.4,(i+1)*.15),stone,.012)
# Floor under the portal is reserved at +1.05 m, clear opening remains unobstructed.
c.box('Portal context landing',(0,55.5,.445),(15,7.4,1.21),stone)
c.collection('18_Plaza_Cameras')
c.camera('05_Plaza_from_gate',(1,4.5,1.72),(0,35,3.1),28)
c.camera('06_Plaza_toward_gate',(-1,44,1.72),(0,0,2.1),30)
c.camera('07_Plaza_bench_detail',(-1,15.3,1.65),(-6.3,19,1.1),29)
c.camera('08_Plaza_overview',(43,-14,40),(0,25,1.5),43)
scene.camera=scene.objects['06_Plaza_toward_gate']
scene['scope']='South gate + south inner plaza; portal context is replaced in v0.0.5'
c.save(c.ROOT/'models/campus/WZMS_Campus_v004.blend','v0.0.4',[119232349,119232352,119232353])
print('WZMS_BUILD_COMPLETE v0.0.4',flush=True)
