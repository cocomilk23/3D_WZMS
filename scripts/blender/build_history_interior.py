"""v038: school history ground gallery, source-backed panels and editable cabinets."""
import bpy,sys,math
from pathlib import Path
from mathutils import Matrix,Vector
sys.path.insert(0,str(Path(__file__).parent))
import campus_common as c,north_common as n,south_detail_common as s
import island_common as h,culture_common as k,indoor_common as i
sc=bpy.data.scenes['WZMS_Campus'];c.activate(sc);p=n.palette();bpy.context.view_layer.update()
def original_panel(name,source,face,vertices,uvs,emission=.08):
 """Projective UV sampling of intact source faces, without a diagonal affine seam."""
 obj=i.photo_panel(name,source,face,vertices,uvs,emission)
 p0,p1,p2,p3=uvs;dx1=p1[0]-p2[0];dx2=p3[0]-p2[0];dx3=p0[0]-p1[0]+p2[0]-p3[0]
 dy1=p1[1]-p2[1];dy2=p3[1]-p2[1];dy3=p0[1]-p1[1]+p2[1]-p3[1]
 den=dx1*dy2-dx2*dy1
 g=(dx3*dy2-dx2*dy3)/den if abs(den)>1e-10 else 0
 hh=(dx1*dy3-dx3*dy1)/den if abs(den)>1e-10 else 0
 a=p1[0]-p0[0]+g*p1[0];b=p3[0]-p0[0]+hh*p3[0]
 d=p1[1]-p0[1]+g*p1[1];e=p3[1]-p0[1]+hh*p3[1]
 vv=[];uv=[];ff=[];steps=32;corners=[Vector(v) for v in vertices]
 for iy in range(steps+1):
  t=iy/steps
  for ix in range(steps+1):
   u=ix/steps;vv.append(corners[0]*(1-u)*(1-t)+corners[1]*u*(1-t)+corners[2]*u*t+corners[3]*(1-u)*t)
   q=g*u+hh*t+1;uv.append(((a*u+b*t+p0[0])/q,(d*u+e*t+p0[1])/q))
 for iy in range(steps):
  for ix in range(steps):
   j=iy*(steps+1)+ix;ff.append((j,j+1,j+steps+2,j+steps+1))
 mat=obj.data.materials[0];mesh=bpy.data.meshes.new(name+' projective surface');mesh.from_pydata(vv,[],ff);mesh.materials.append(mat)
 layer=mesh.uv_layers.new(name='Projective original source corners')
 for loop in mesh.loops:layer.data[loop.index].uv=uv[loop.vertex_index]
 obj.data=mesh;obj['reference_projection']='32 by 32 projective UV grid from four reviewed source corners'
 return obj
ret=[]
for o in bpy.data.collections['172_History_Neighbouring_Cultural_Building_Context'].objects:
 if o.name.startswith(('History curved gallery glass','History curved white structural','History curved facade horizontal')):
  bounds=[o.matrix_world@Vector(v) for v in o.bound_box]
  if min(v.x for v in bounds)<264.1 and max(v.y for v in bounds)>118.1:ret.append(o.name)
h.retire('v0.0.38',names=ret)
c.collection('340_History_Interior_Floor_And_Ceiling')
dark=c.material('History black anodized slatted ceiling',(.022,.026,.025),.43,.30)
cream=c.material('History cream exhibit backing',(.60,.53,.41),.82)
frame=c.material('History graphite display frame',(.09,.115,.12),.45,.3)
wood=bpy.data.materials['Math classroom aged timber'].copy();wood.name='History cabinet dark walnut'
grain=next(node for node in wood.node_tree.nodes if node.type=='VALTORGB')
grain.color_ramp.elements[0].color=(.035,.014,.007,1);grain.color_ramp.elements[1].color=(.13,.065,.026,1)
floor=n.paving('History interior grey stone floor',(.26,.285,.265),(.50,.50),.003)
c.box('History ground gallery finish',(257,130,.025),(13.6,23.6,.05),floor)
c.box('History dark ceiling background',(257,130,3.79),(13.6,23.6,.08),dark)
for x in [250.3+j*.14 for j in range(97)]:c.box('History parallel black ceiling slat',(x,130,3.59),(.045,23.6,.26),dark)
red=c.material('History foyer red carpet',(.43,.012,.022),.94)
c.box('History interior red entry runner',(252.5,120,.059),(4.5,1.65,.02),red)
c.collection('341_History_House_Frame_Exhibition_Bays')
panel_uv={
 407:[(.115,.343),(.877,.343),(.877,.657),(.115,.657)],
 410:[(.10,.405),(.715,.42),(.715,.595),(.10,.615)],
 411:[(.69,.43),(.97,.397),(.97,.64),(.69,.58)],
 413:[(.16,.40),(.88,.36),(.88,.575),(.16,.55)],
 414:[(.225,.39),(.98,.26),(.98,.65),(.225,.57)],
 416:[(.10,.397),(.89,.397),(.89,.567),(.10,.567)]}
def bay(title,x,y,width,source,face,angle=0):
 before=set(c.COL.objects)
 c.box('History '+title+' cream backing',(0,0,1.52),(width,.18,3.04),cream)
 points=[(-width/2,-.13,.05),(-width/2,-.13,2.9),(0,-.13,3.30),(width/2,-.13,2.9),(width/2,-.13,.05)]
 for a,b in zip(points,points[1:]):s.beam('History house outline '+title,a,b,.095,.11,frame)
 c.text('History section '+title,title,(0,-.112,2.76),.23,p['seam'])
 if source==405:
  # The photographed preface crosses two cube faces; both original parts remain.
  for label,lo,hi,fc,uv in [('left',-width*.45,width*.16,'l',[(.522,.23),(1,.098),(1,.8),(.522,.69)]),('right',width*.16,width*.45,'f',[(0,.184),(.183,.25),(.183,.76),(0,.824)])]:
   original_panel('History original preface '+label,405,fc,[(lo,-.116,1.25),(hi,-.116,1.25),(hi,-.116,2.63),(lo,-.116,2.63)],uv,.04)
 elif source==417:
  for label,xx,w,uv in [('portrait',-2.3,1.0,[(.49,.44),(.575,.44),(.575,.57),(.49,.56)]),('narrow scroll',0,.58,[(.641,.412),(.706,.406),(.706,.585),(.641,.58)]),('large scroll',2.3,.76,[(.808,.355),(.94,.345),(.94,.616),(.808,.60)])]:
   original_panel('History original framed '+label,417,'l',[(xx-w/2,-.116,1.25),(xx+w/2,-.116,1.25),(xx+w/2,-.116,2.63),(xx-w/2,-.116,2.63)],uv,.04)
 else:
  original_panel('History original '+title,source,face,[(-width*.45,-.116,1.25),(width*.45,-.116,1.25),(width*.45,-.116,2.63),(-width*.45,-.116,2.63)],panel_uv[source],.04)
 c.box('History '+title+' low cabinet',(0,-.46,.52),(width-.35,.68,.95),wood,.018)
 c.box('History '+title+' cabinet pale display bed',(0,-.46,1.005),(width-.44,.59,.022),cream)
 c.box('History '+title+' real glass cover',(0,-.46,1.20),(width-.40,.64,.026),i.glass())
 for xx in [-width/2+.23,width/2-.23]:c.box('History cabinet glass side',(xx,-.46,1.105),(.02,.63,.18),i.glass())
 c.box('History cabinet glass front',(0,-.79,1.105),(width-.40,.02,.18),i.glass())
 for j in range(max(2,int(width/.6))):
  xx=-width*.35+j*width*.7/max(1,int(width/.6)-1)
  c.box('History archival paper facsimile support',(xx,-.46,1.03),(.34,.39,.009),p['white'])
 c.box('History bay concealed warm LED',(0,-.15,.20),(width-.30,.028,.04),i.glow('History warm exhibit lighting',(.98,.80,.49),2))
 k.area('History exhibit wash',(0,-.70,3.30),45,1.5,(1,.89,.68),(0,0,1.7))
 bpy.context.view_layer.update();m=Matrix.Translation((x,y,0))@Matrix.Rotation(angle,4,'Z')
 for o in set(c.COL.objects)-before:o.matrix_world=m@o.matrix_world
# Long perimeter bays retain a clear circulation lane on each side of the central islands.
for title,y,id,face in [('温中百年',125,407,'f'),('英奇匡国',131,410,'l'),('历任校长',137,411,'f')]:bay(title,250.45,y,4.8,id,face,math.pi/2)
for title,y,id,face in [('名师荟萃',125,413,'l'),('孙诒让',131,414,'l'),('英奇匡国',137,416,'f')]:bay(title,263.55,y,4.8,id,face,-math.pi/2)
bay('前言',259.5,118.45,5.8,405,'l',math.pi)
bay('校友题词',257,141.55,8.0,417,'l')
c.collection('342_History_Campus_Miniatures_And_Photo_Wall')
# Two free-standing islands use source images for historical content; miniatures are illustrative.
for y in [126.4,133.8]:
 c.box('History central island cream partition',(257,y,1.47),(2.9,4.0,2.94),cream)
 for x,ang,id in [(255.5,-math.pi/2,408),(258.5,math.pi/2,418)]:
  before=set(c.COL.objects)
  uv=[(.185,.32),(.83,.32),(.83,.69),(.185,.69)] if id==408 else [(.04,.30),(.985,.30),(.985,.645),(.04,.645)]
  original_panel('History original campus and photo wall',id,'f',[(-1.8,0,.85),(1.8,0,.85),(1.8,0,2.75),(-1.8,0,2.75)],uv,.06)
  bpy.context.view_layer.update();m=Matrix.Translation((x,y,0))@Matrix.Rotation(ang,4,'Z')
  for obj in set(c.COL.objects)-before:obj.matrix_world=m@obj.matrix_world
  bpy.context.view_layer.update()
  for obj in set(c.COL.objects)-before:
   normal=obj.matrix_world.to_3x3()@obj.data.polygons[0].normal
   assert normal.x*(-1 if x<257 else 1)>.99,'Exhibit image must face its viewing aisle'
for y in [122.6,130.8]:
 c.box('History campus model walnut plinth',(257,y,.51),(3.0,1.7,1.02),wood,.015)
 c.box('History miniature green terrain',(257,y,1.04),(2.9,1.6,.04),c.material('History miniature lawn',(.13,.27,.065),.85))
 for xx,yy,w,d,z in [(-.8,-.2,.65,.20,.24),(-.1,-.2,.65,.20,.24),(.7,-.2,.7,.22,.24),(-.7,.4,.5,.26,.17),(.6,.4,.65,.28,.17)]:
  c.box('History illustrative miniature school massing',(257+xx,y+yy,1.06+z/2),(w,d,z),p['white'])
  c.box('History miniature blue roof',(257+xx,y+yy,1.07+z),(w+.015,d+.015,.018),c.material('History miniature roof',(.035,.18,.24),.6))
 c.box('History miniatures glass top',(257,y,1.63),(3.0,1.7,.025),i.glass())
 for x in [255.5,258.5]:c.box('History miniatures glass end',(x,y,1.325),(.02,1.7,.60),i.glass())
 for yy in [y-.85,y+.85]:c.box('History miniatures glass side',(257,yy,1.325),(3,.02,.60),i.glass())
c.collection('343_History_Warm_Photo_Corner_And_Lights')
c.box('History amber photograph corner',(262.9,120.5,1.8),(.1,3.5,3.3),cream)
original_panel('History original warm photograph mosaic',412,'f',[(262.835,122.1,.55),(262.835,118.9,.55),(262.835,118.9,3.08),(262.835,122.1,3.08)],[(.01,.294),(.255,.35),(.255,.598),(.01,.654)],.20)
for x in [252.9,261.1]:
 c.box('History black lighting track',(x,130,3.37),(.06,23,.05),dark)
 for y in [120,123,126,129,132,135,138,140]:
  c.rod('History adjustable cylindrical spotlight',(x,y,3.34),(x,y,3.15),.065,p['white'],.08,12)
  k.area('History soft gallery light',(x,y,3.10),38,1.2,(1,.91,.77))
c.collection('348_History_Indoor_Cameras')
c.camera('159_History_entry_preface',(251.5,120,1.7),(260,119.5,1.8),23)
c.camera('160_History_century_and_miniatures',(253.5,120.8,2.55),(257,125,1.15),23)
c.camera('161_History_exhibition_aisle',(252.9,137.8,1.7),(252.9,125,1.6),24)
c.camera('162_History_teachers_and_photo_wall',(261.1,130,1.7),(261.3,138,1.6),23)
c.camera('163_History_calligraphy_and_ceiling',(260.5,139,1.7),(255,141,2.2),23)
h.save(38,'Ground-floor school history gallery from 405-418: black slatted ceiling, house-outline bays, source-backed century/alumni/headteacher/teacher panels, photo wall, calligraphy, real glazed cases and illustrative miniature displays. Gallery arrangement inferred within prior exterior. Original historical wording is not invented; source panels retain photographic perspective. Upper floors and neighboring cultural interiors not claimed.',list(range(405,419)),'160_History_century_and_miniatures')
