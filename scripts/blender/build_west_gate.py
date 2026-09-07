"""v030 historic west gate: brick arches, circular windows, stone court and open passage."""
import bpy,math,sys,json
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).parent))
import campus_common as c,north_common as n,north_landscape as l
import south_detail_common as s,island_common as h,sports_common as q,culture_common as u
sc=bpy.data.scenes['WZMS_Campus'];c.activate(sc);p=n.palette();before=set(bpy.data.objects)
brick=n.paving('West gate irregular grey brick',(.29,.29,.26),(.29,.064),.007)
h.use_facade_uv(brick)
nd,ln=brick.node_tree.nodes,brick.node_tree.links
bt=next(a for a in nd if a.type=='TEX_BRICK')
bt.inputs['Color1'].default_value=(.082,.089,.084,1);bt.inputs['Color2'].default_value=(.27,.265,.23,1)
bt.inputs['Mortar'].default_value=(.18,.185,.16,1)
co=next(a for a in nd if a.type=='TEX_COORD');weather=nd.new('ShaderNodeTexNoise');weather.inputs['Scale'].default_value=3.8;weather.inputs['Detail'].default_value=5
ln.new(co.outputs['UV'],weather.inputs['Vector'])
shade=nd.new('ShaderNodeValToRGB');shade.color_ramp.elements[0].position=.25;shade.color_ramp.elements[0].color=(.22,.24,.23,1)
shade.color_ramp.elements[1].position=.72;shade.color_ramp.elements[1].color=(1,1,.92,1);ln.new(weather.outputs['Fac'],shade.inputs[0])
mix=nd.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.8
ln.new(bt.outputs['Color'],mix.inputs[1]);ln.new(shade.outputs[0],mix.inputs[2]);ln.new(mix.outputs[0],nd['Principled BSDF'].inputs['Base Color'])
stone=s.mottled('West gate worn limestone mouldings',[(.27,.27,.24),(.47,.46,.40)],4)
c.noise(stone,68,.27,.012)
trim=c.material('West gate dark fired brick moulding',(.13,.135,.12),.86)
iron=c.material('West gate black wrought iron',(.018,.024,.023),.43,.62)
glass=c.material('West gate round smoked glass',(.05,.10,.13),.17,.32)
orange=c.material('West gate terracotta flower inlays',(.55,.24,.115),.84)
paving=n.paving('West gate large aged stone flags',(.48,.46,.39),(1.1,.48),.013)
soil=s.mottled('West gate garden soil',[(.065,.085,.025),(.19,.22,.075)],3)
c.collection('260_West_Gate_Continuous_Ground')
c.box('West gate court retaining foundation',(-112,169,-.85),(47,46,1.64),stone)
c.box('West gate large stone courtyard',(-112,169,-.055),(47,46,.11),paving)
c.box('West gate inner bank joins existing campus ESTIMATED',(-80.75,169,-.90),(15.5,46,1.60),soil)
s.ribbon('West gate Daosi connector bank',[(-81,136),(-84,136),(-84,169),(-90,169)],7,soil,-.08,1.7,miter=True)
s.ribbon('West gate Daosi connector paving',[(-81,136),(-84,136),(-84,169),(-100,169)],4.0,paving,0,.18,miter=True)
c.collection('261_West_Gate_Historic_Brick_Arcades')
x=-92;y=169
q.arched_bay('West gate central arch',x,y,2.4,3.2,6.1,3.6,.60,brick)
for sign in [-1,1]:
    q.arched_bay('West gate side entrance',x,y+sign*5.15,1.45,2.55,6.1,3.6,.8,brick)
    c.box('West gate continuous wing junction masonry',(x,y+sign*7.48,2.2),(3.6,.48,4.4),brick)
    for j in range(4):
        yy=y+sign*(9.15+j*3.18)
        q.arched_bay('West gate low arcade',x,yy,1.25,2.12,4.25,3.6,.34,brick)
        q.radial_bricks('West gate arcade arch stone',x-1.87,yy,2.12,1.25,.23,stone)
        c.box('West gate low arcade rear wall',(x+1.65,yy,1.9),(.3,3.18,3.8),brick)
        c.box('West gate recessed historical plaque',(x+1.475,yy,1.45),(.025,1.2,.78),trim)
        for dy in [-1.47,1.47]:
            c.box('West gate arcade moulded impost',(x-.02,yy+dy,2.12),(3.83,.55,.16),stone,.02)
            c.box('West gate arcade pier plinth',(x-.02,yy+dy,.15),(3.83,.57,.30),stone,.014)
    c.box('West gate low arcade roof',(x,y+sign*14.0,4.34),(3.9,14,.20),stone)
    for z,dep in [(4.47,4.05),(5.12,3.85)]:c.box('West gate balustrade horizontal coping',(x,y+sign*14,z),(dep,14,.14),stone,.015)
    for yy in [y+sign*(7.3+j*.44) for j in range(32)]:
        for xx in [x-1.65,x+1.65]:
            c.rod('West gate turned stone baluster stem',(xx,yy,4.53),(xx,yy,5.04),.058,stone,sides=12)
            l.ellipsoid('West gate baluster swelling',(xx,yy,4.75),(.105,.105,.17),stone,12,8)
    for yy in [y+sign*8,y+sign*14,y+sign*20]:
        c.box('West gate balustrade square pedestal',(x-1.65,yy,4.83),(.34,.34,.66),brick)
        l.ellipsoid('West gate stone crown',(x-1.65,yy,5.30),(.19,.19,.21),stone,16,10)
c.box('West gate upper central facade',(x,y,7.88),(3.6,14.3,3.56),brick)
for yy,r,zz in [(y,1.12,8.03),(y-4.78,.59,7.19),(y+4.78,.59,7.19)]:
    disc=n.disk('West gate circular window',0,0,0,r,glass,96);disc.location=(x-1.815,yy,zz);disc.rotation_euler.y=math.pi/2
    q.arch_x('West gate full circular stone surround',x-1.87,yy,zz,r,.18,.20,stone,0,math.tau,96)
    q.radial_bricks('West gate radial window masonry',x-1.96,yy,zz,r+.20,.22,brick,True)
    q.arch_x('West gate black circular glazing frame',x-1.973,yy,zz,r-.035,.03,.045,iron,0,math.tau,96)
for yy,r,zz in [(y,2.4,3.2),(y-5.15,1.45,2.55),(y+5.15,1.45,2.55)]:
    q.radial_bricks('West gate principal arch masonry',x-1.94,yy,zz,r,.30,stone)
for dy in [-7.05,-3.08,3.08,7.05]:
    yy=y+dy
    c.box('West gate projecting decorative pier',(x-1.85,yy,1.7),(.42,.73,3.4),brick)
    for z in [.13,.45,1.1,1.77,2.44,3.14]:c.box('West gate layered pier moulding',(x-1.99,yy,z),(.49,.92,.12),stone,.016)
    for z in [.78,1.45,2.12,2.80]:
        c.box('West gate inset ornament panel',(x-2.115,yy,z),(.04,.56,.47),trim)
        # Eight-point terracotta flower motif visible on the historic gate piers.
        v=[(x-2.145,yy,z)]
        for k in range(16):
            a=k*math.tau/16;r=.235 if k%2==0 else .105;v.append((x-2.145,yy+r*math.cos(a),z+r*math.sin(a)))
        c.mesh('West gate terracotta floral inlay',v,[(0,k+1,(k+1)%16+1) for k in range(16)],orange)
for z,width in [(9.66,14.7),(9.86,15.0)]:c.box('West gate upper cornice',(x,y,z),(3.98,width,.16),stone)
# Curved gable profile, independent editable masonry thickness.
outline=[(y-6.8,9.91)]+[(y-6.8+13.6*i/64,10.18+1.25*math.sin(math.pi*i/64)**2) for i in range(65)]+[(y+6.8,9.91)]
v=[(xx,yy,zz) for xx in [x-1.81,x+1.81] for yy,zz in outline];nn=len(outline)
f=[tuple(reversed(range(nn))),tuple(range(nn,2*nn))]+[(i,(i+1)%nn,(i+1)%nn+nn,i+nn) for i in range(nn)]
c.mesh('West gate curved central gable',v,f,stone)
for a,b in zip(outline[1:-1],outline[2:-1]):c.rod('West gate gable curved coping',(x-1.85,*a),(x-1.85,*b),.09,trim,sides=8)
c.text('West gate photographed school title','温 州 中 学',(x-1.91,y,10.20),.55,trim,(math.pi/2,0,-math.pi/2))
c.collection('262_West_Gate_Ironwork_And_Garden')
# Hinged leaves are shown open to keep the passage usable; source photograph has them closed.
for sign in [-1,1]:
    yy=y+sign*2.30
    for xx in [x+1.4+i*.14 for i in range(16)]:
        zz=2.25+.25*math.sin((xx-x-1.4)/2.1*math.pi)
        c.rod('West gate open iron leaf upright',(xx,yy,.12),(xx,yy,zz),.020,iron,sides=8)
        l.ellipsoid('West gate wrought spear finial',(xx,yy,zz+.06),(.025,.025,.09),iron,8,6)
    for z in [.16,.44,1.08,2.21]:c.rod('West gate open leaf horizontal',(x+1.4,yy,z),(x+3.5,yy,z),.029,iron,sides=8)
    u.pot(x-2.4,y+sign*3.75,scale=1.3,seed=350+sign)
c.box('West gate pine raised planting bed',(-118,184,.22),(10.5,8.2,.44),brick)
c.box('West gate pine bed stone coping',(-118,184,.46),(10.7,8.4,.12),stone)
c.box('West gate pine soil',(-118,184,.55),(10.05,7.75,.12),soil)
q.clipped_pine('West gate photographed layered pine',-118,184)
for xx in [-123.2,-112.8]:
    for yy in [180,188]:
        c.box('West gate low garden lantern pedestal',(xx,yy,.54),(.59,.59,1.08),brick)
        c.box('West gate garden lantern glazing',(xx,yy,1.25),(.35,.35,.33),c.material('West gate lantern warm glass',(.64,.53,.30),.35))
        c.box('West gate lantern cap',(xx,yy,1.46),(.51,.51,.09),iron,.02)
for xx,yy in [(-126,185),(-89,190)]:s.tree(xx,yy,.65,yy*.02)
# Stone end wall with visibly framed panels. Unreadable relief is simplified, not invented history.
c.box('West gate garden end wall',(-118,191.4,1.6),(24,.60,3.2),brick)
for xx in [-125,-113]:
    c.box('West gate framed stone relief backing',(xx,191.05,1.65),(8,.11,1.65),stone)
    for z in [.77,2.53]:c.box('West gate relief moulded border',(xx,190.96,z),(8.2,.18,.10),trim)
    for xxx in [xx-4.05,xx+4.05]:c.box('West gate relief vertical border',(xxx,190.96,1.65),(.10,.18,1.85),trim)
c.collection('268_West_Gate_Review_Cameras')
c.camera('121_West_gate_front',(-130,169,1.7),(-92,169,4.9),28)
c.camera('122_West_gate_arch_detail',(-103,162,1.7),(-92,166.2,3.8),23)
c.camera('123_West_gate_court',(-113,157,1.7),(-116,183,2.8),26)
c.camera('124_West_gate_connection',(-139,121,47),(-96,163,0),32)
for obj in set(bpy.data.objects)-before:
    if obj.type=='MESH' and brick.name in [m.name for m in obj.data.materials]:h.vertical_uv(obj)
h.save(30,'Historic west gate and grey brick arcades from 350, stone court and layered pine; connection to Daosi. Leaves held open for walking. Unreadable relief and hidden rear details simplified; geometry image-estimated.',[350,375,347,348],'121_West_gate_front')
