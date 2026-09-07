"""v037: a connected interpretation of the eight photographed mathematics museum points."""
import bpy,sys,math
from pathlib import Path
from mathutils import Vector,Matrix
sys.path.insert(0,str(Path(__file__).parent))
import campus_common as c,north_common as n,south_detail_common as s
import island_common as h,culture_common as k,indoor_common as i
sc=bpy.data.scenes['WZMS_Campus'];c.activate(sc);p=n.palette();bpy.context.view_layer.update()
ret=[]
for col in ['150_Math_Podium_Approach_And_Courtyard','154_Math_Bougainvillea_And_Courtyard_Furniture']:
 for o in bpy.data.collections[col].objects:
  if o.type!='MESH':continue
  bounds=[o.matrix_world@Vector(v) for v in o.bound_box];mid=sum(bounds,Vector())/8
  if col.startswith('150_'):
   if o.name.startswith('Math clipped'):ret.append(o.name)
  elif 134<mid.x<166 and 114<mid.y<137 and (mid.x<143.2 or mid.x>155.8 or mid.y>127.8):ret.append(o.name)
# The old thin, unmeasured placeholder wings cannot house the photographed rooms.
h.retire('v0.0.37',collections=['152_Math_Exhibition_Exterior_Shells'],names=ret)
created_before=set(sc.objects)
c.collection('330_Math_Connected_Interior_Shell')
white=bpy.data.materials['Math white rendered plaster'];blue=c.material('Math exhibition deep blue',(.014,.16,.28),.7)
gold=c.material('Math exhibition warm gold',(.64,.37,.08),.43,.35)
floor=n.paving('Math exhibition grey floor',(.31,.34,.32),(.60,.60),.002)
wood=n.paving('Math upper warm oak boards',(.36,.25,.15),(.11,.70),.002)
dark=bpy.data.materials['Math charcoal coping'];glass=i.glass()
for x,y,w,d in [(139.5,125,7,22),(160.5,125,9,22),(149.5,132,13,8)]:
 c.box('Math U wing ground finish',(x,y,.025),(w,d,.09),floor)
 c.box('Math U wing white roof',(x,y,8.5),(w+.2,d+.2,.24),white)
# Exterior walls have actual openings, not window images on opaque planes.
for x in [136,165]:
 c.box('Math museum external sill',(x,125,.35),(.20,22,.70),white)
 c.box('Math museum external upper sill',(x,125,4.25),(.20,22,.50),white)
 c.box('Math museum roof lintel',(x,125,8.14),(.20,22,.48),white)
 for y in [115.5+3*j for j in range(7)]:
  for z in [2.35,6.2]:i.window_x('Math museum tall narrow window',x,y,z,1.35,3.2)
  for yy in [y-1.5,y+1.5]:c.box('Math window plaster pier',(x,yy,4.4),(.22,1.64,7.6),white)
for y in [114,136]:
 for x,w in [(139.5,7),(160.5,9)]:c.box('Math wing end wall',(x,y,4.2),(w,.20,8.4),white)
c.box('Math north connecting gallery back',(149.5,136,4.2),(13,.20,8.4),white)
c.box('Math north connecting gallery courtyard side',(149.5,128,4.2),(13,.20,8.4),white)
for lo,hi in [(114,118.7),(123.1,128)]:c.box('Math west courtyard wall around entrance',(143,(lo+hi)/2,4.2),(.20,hi-lo,8.4),white)
c.box('Math west entrance lintel',(143,120.9,5.65),(.22,4.4,5.5),white)
for y in [119,122.8]:i.window_y('Math courtyard open glass leaf',144,y,1.4,1.6,2.8)
c.box('Math east courtyard wall',(156,121,4.2),(.20,14,8.4),white)
# Upper level: open atrium and stair void in the west wing, full floor elsewhere.
for x,y,w,d in [(141.5,122.2,3,16.4),(139.5,133.2,7,5.6),(149.5,132,13,8),(160.5,125,9,22)]:
 obj=c.box('Math upper floor around atrium',(x,y,4.08),(w,d,.24),wood);obj.data.materials.append(white)
 for face in obj.data.polygons:face.material_index=0 if face.normal.z>.5 else 1
k.stairs('Math white straight internal stair',(138,122,0),(138,130.4,4.2),2.5,24,white,False)
for x in [136.7,139.3]:
 c.mesh('Math sloping stair glass',[(x,122,.1),(x,130.4,4.3),(x,130.4,5.25),(x,122,1.05)],[(0,1,2,3)],glass)
 c.rod('Math stair oak handrail',(x,122,1.1),(x,130.4,5.3),.03,gold,sides=10)
i.glass_rail('Math upper atrium guard',[(140,114.3),(140,130.4)],4.2)
c.collection('331_Math_Blue_Exhibits_And_Original_Panels')
def display(name,x,y,width,source,face,title,uvs):
 c.box(name+' blue wall',(x,y,1.78),(width,.12,3.56),blue)
 c.text(name+' heading',title,(x,y-.075,2.98),.30,gold)
 i.photo_panel(name+' original interpretation',source,face,[(x-width*.43,y-.077,1.15),(x+width*.43,y-.077,1.15),(x+width*.43,y-.077,2.75),(x-width*.43,y-.077,2.75)],uvs)
 c.box(name+' white low exhibit case',(x,y-.45,.79),(width-.25,.68,.38),white,.02)
 c.box(name+' glass case cover',(x,y-.45,1.00),(width-.30,.62,.025),glass)
 for dx in [-.9,0,.9]:c.box(name+' archival paper support',(x+dx,y-.45,1.02),(.5,.40,.012),p['white'])
display('Math Su Buqing gallery',139.6,135.7,5.8,398,'l','苏步青',[(.39,.29),(.985,.34),(.985,.82),(.39,.70)])
display('Math Gu Chaohao gallery',147.2,135.7,5.5,399,'l','谷超豪',[(.49,.44),(.985,.30),(.985,.70),(.49,.61)])
display('Math stars gallery',153.3,135.7,5.3,400,'f','群星璀璨',[(.01,.28),(.525,.36),(.525,.72),(.01,.79)])
# Foyer panel faces across the double-height atrium, with clear entry and stair approach.
c.box('Math foyer blue feature wall',(139.5,114.2,3.5),(6.7,.12,7.0),blue)
c.text('Math foyer observed title','数学馆',(139.5,114.28,5.7),.64,gold,(math.pi/2,0,math.pi))
i.photo_panel('Math foyer original preface',398,'b',[(140.4,114.275,.3),(138.6,114.275,.3),(138.6,114.275,4.3),(140.4,114.275,4.3)],[(.735,.377),(.875,.365),(.875,.70),(.735,.687)])
for x,y,z in [(138,117,6),(141,119,6.7),(138,120,5.4)]:
 c.rod('Math cream cylindrical pendant',(x,y,z),(x,y,z+1.6),.35,i.glow('Math warm paper lantern',(.95,.74,.37),1.8),sides=48)
 c.rod('Math lantern suspension',(x,y,z+1.6),(x,y,8.36),.008,dark,sides=6)
 k.area('Math warm pendant fill',(x,y,z-.02),80,1.0,(1,.82,.57))
for x,y,z in [(140,133,3.85),(148,132,3.85),(154,133,3.85),(160,129,3.85),(141,124,8.2),(149,132,8.2),(161,124,8.2)]:k.area('Math ceiling soft exhibit light',(x,y,z),140,3,(1,.93,.82))
c.collection('332_Math_Upper_Projection_Theatre')
# Curved wooden tiers built as real annular solid meshes, with a side staircase.
for j in range(5):
 ri=1.6+j*.43;ro=ri+.43
 v=[];segments=64
 for a in [math.pi+math.pi*t/segments for t in range(segments+1)]:
  for r,z in [(ri,4.2),(ro,4.2),(ri,4.2+(j+1)*.18),(ro,4.2+(j+1)*.18)]:v.append((149.5+r*math.cos(a),132.4+r*math.sin(a),z))
 faces=[]
 for t in range(segments):
  a=4*t;b=a+4;faces.extend([(a+2,a+3,b+3,b+2),(a,a+2,b+2,b),(a+1,b+1,b+3,a+3)])
 faces.extend([(0,1,3,2),(4*segments,4*segments+2,4*segments+3,4*segments+1)])
 c.mesh('Math curved timber audience tier',v,faces,wood)
 # Fine vertical battens reproduce the photographed ribbed timber risers.
 for t in range(max(2,round(math.pi*ri/.075))+1):
  a=math.pi+math.pi*t/max(2,round(math.pi*ri/.075))
  xx=149.5+(ri-.006)*math.cos(a);yy=132.4+(ri-.006)*math.sin(a)
  c.rod('Math audience vertical timber riser batten',(xx,yy,4.2+j*.18),(xx,yy,4.2+(j+1)*.18),.009,wood,sides=4)
k.stairs('Math theatre side steps',(153.6,130.25,4.2),(153.6,132.4,5.1),.8,5,wood,False)
c.box('Math projection dark backing',(149.5,135.65,6.55),(4.6,.12,2.45),dark)
i.photo_panel('Math photographed projection screen',402,'f',[(147.35,135.573,5.43),(151.65,135.573,5.43),(151.65,135.573,7.64),(147.35,135.573,7.64)],[(.395,.495),(.770,.495),(.770,.789),(.395,.760)],.5)
for x in [146,153]:s.beam('Math theatre dark light truss',(x,129,7.9),(x,135.5,7.9),.055,.055,dark)
for y in [130,132,134]:
 s.beam('Math theatre cross truss',(146,y,7.9),(153,y,7.9),.055,.055,dark)
 for x in [147,149.5,152]:c.rod('Math black theatre spotlight',(x,y,7.82),(x,y,7.55),.09,dark,.13,12)
c.collection('333_Math_Rest_Area_And_Traditional_Classroom')
# Rest corner upstairs faces actual glazed exterior; transparent floor strips are local details.
fabric=c.material('Math rest grey upholstery',(.26,.29,.28),.93)
for x in [158,162.5]:
 c.box('Math rest sofa seat',(x,120,4.64),(2.4,.85,.40),fabric,.10)
 c.box('Math rest sofa back',(x,120.4,5.03),(2.4,.22,.85),fabric,.07)
 for xx in [x-1.07,x+1.07]:c.box('Math rest sofa arm',(xx,120,4.96),(.26,.95,.52),fabric,.06)
def add_math_rest_details():
 c.collection('333_Math_Rest_Area_And_Traditional_Classroom')
 foot=bpy.data.materials['Math charcoal coping'];accent=c.material('Math rest photographed mustard cushion',(.63,.30,.035),.9)
 for x in [158,162.5]:
  for xx in [x-.8,x+.8]:
   for yy in [119.7,120.3]:c.box('Math rest sofa supporting foot',(xx,yy,4.33),(.075,.075,.26),foot)
  c.box('Math rest mustard cushion',(x+.25,120.18,5.03),(.4,.18,.42),accent,.06)
 light=bpy.data.lights.new('Math rest ambient fill','AREA');light.energy=200;light.shape='DISK';light.size=3;light.color=(.95,.95,1)
 lamp=bpy.data.objects.new(light.name,light);c.COL.objects.link(lamp);lamp.location=(160.5,117,8.1)
add_math_rest_details()
c.box('Math rest low oak table',(160.2,118,4.65),(1.4,.75,.08),wood,.025)
for x in [159.65,160.75]:
 for y in [117.75,118.25]:c.box('Math rest table leg',(x,y,4.42),(.05,.05,.44),dark)
k.pot(164,122,4.2,.8,seed=403)
# Ground-floor classroom: paired old desks, real chairs, beams, tall windows and chalkboard.
def configure_math_timber():
 mat=c.material('Math classroom aged timber',(.22,.145,.09),.65)
 nd,lk=mat.node_tree.nodes,mat.node_tree.links;nd.clear()
 out=nd.new('ShaderNodeOutputMaterial');bs=nd.new('ShaderNodeBsdfPrincipled');bs.inputs['Roughness'].default_value=.65
 co=nd.new('ShaderNodeTexCoord');scale=nd.new('ShaderNodeVectorMath');scale.operation='MULTIPLY';scale.inputs[1].default_value=(3,75,12)
 tex=nd.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=3;tex.inputs['Detail'].default_value=3
 ramp=nd.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.12,.066,.031,1);ramp.color_ramp.elements[1].color=(.29,.18,.087,1)
 bump=nd.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.18;bump.inputs['Distance'].default_value=.003
 lk.new(co.outputs['Generated'],scale.inputs[0]);lk.new(scale.outputs[0],tex.inputs['Vector']);lk.new(tex.outputs['Fac'],ramp.inputs[0]);lk.new(ramp.outputs[0],bs.inputs['Base Color'])
 lk.new(tex.outputs['Fac'],bump.inputs['Height']);lk.new(bump.outputs[0],bs.inputs['Normal']);lk.new(bs.outputs[0],out.inputs[0])
 return mat
desk=configure_math_timber()
c.box('Math classroom timber floor',(160.5,120.5,.083),(8.6,12.8,.024),wood)
for x in [158,160.5,163]:
 for y in [118,120.3,122.6,124.9]:
  c.box('Math old double school desk',(x,y,.74),(1.7,.54,.065),desk,.012)
  for dx in [-.72,.72]:
   for dy in [-.18,.18]:c.box('Math old desk leg',(x+dx,y+dy,.36),(.065,.065,.72),desk)
  for dx in [-.43,.43]:
   c.box('Math classroom timber chair seat',(x+dx,y+.58,.43),(.38,.40,.045),desk)
   c.box('Math classroom chair back',(x+dx,y+.76,.69),(.38,.045,.48),desk)
   for xx in [-.15,.15]:
    for yy in [-.15,.15]:c.box('Math classroom chair leg',(x+dx+xx,y+.58+yy,.21),(.038,.038,.42),desk)
c.box('Math classroom chalkboard',(160.5,114.3,1.9),(5.7,.09,1.7),c.material('Math classroom dark chalkboard',(.025,.055,.06),.9))
c.box('Math classroom lectern',(160.5,115.6,.58),(1.4,.55,1.16),desk)
for y in [116,120,124]:
 c.box('Math classroom exposed oak beam',(160.5,y,3.92),(8.6,.23,.36),desk)
 for x in [158,163]:
  c.rod('Math classroom pendant wire',(x,y,3.75),(x,y,3.2),.008,dark,sides=6)
  c.rod('Math classroom porcelain pendant',(x,y,3.07),(x,y,3.19),.20,white,.08,24)
  k.area('Math classroom pendant light',(x,y,3.0),40,.45,(1,.92,.8))
c.collection('338_Math_Indoor_Cameras')
c.camera('153_Math_preface_atrium',(138.7,121,1.7),(139.5,114.2,3.1),22)
c.camera('154_Math_biography_galleries',(143.5,130.5,1.7),(151,135.6,1.7),24)
c.camera('155_Math_stair_and_upper_level',(141,120,1.7),(137.7,129,3.1),22)
c.camera('156_Math_curved_projection_theatre',(154.4,129,5.9),(149.5,134,5.7),20)
c.camera('157_Math_traditional_classroom',(160.5,127,1.7),(160.5,115,1.8),23)
c.camera('158_Math_upper_rest_corner',(160.5,115,5.9),(160.5,120,5.0),23)
bpy.context.view_layer.update()
# Keep the pre-existing Jiushan connector at Y=136 clear of the rear wall.
for obj in set(sc.objects)-created_before:obj.matrix_world=Matrix.Translation((0,-1,0))@obj.matrix_world
h.save(37,'Reference-led mathematics museum interiors from points 397-404. Estimated U-shaped two-floor circulation replaces v019 thin placeholder wings; gateway and surrounding routes retained. Preface, Su Buqing, Gu Chaohao and stars use packed original source panels; theater, rest area and classroom modeled as editable geometry. Room dimensions and relative placements are interpretations, not a measured floor plan.',list(range(397,405)),'153_Math_preface_atrium')
