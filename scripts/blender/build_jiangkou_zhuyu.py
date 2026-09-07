"""v025 two evidenced branches: Jiushan-Jiangkou-Nantian and Zhongshan-Zhuyu."""
import bpy,math,random,sys
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).parent))
import campus_common as c,north_common as n,north_landscape as l,south_detail_common as s,island_common as h
sc=bpy.data.scenes['WZMS_Campus'];c.activate(sc);p=n.palette()
h.retire('v0.0.25',names=['North regional terrain CONTEXT_ESTIMATED'])
c.collection('210_Jiangkou_Walks_And_Continuous_Land')
grey=n.paving('Jiangkou pale granite slabs',(.51,.52,.47),(.65,.40),.006)
grass=s.mottled('Jiangkou garden lawn',[(.07,.13,.025),(.25,.27,.085)],1.8)
edge=h.pebble('Jiangkou grey granite border',(.39,.42,.37))
main=[(172,136),(172,181),(119,181),(119,209),(83,209)]
west=[(54,209),(40,209),(40,200),(8,200)]
for name,poly in [('east connection',main),('Nantian west connection',west)]:
    s.ribbon('Jiangkou '+name+' supporting ground',poly,11,grass,-.025,1.6,miter=True)
    s.ribbon('Jiangkou '+name+' granite paving',poly,3.3,grey,0,.18,miter=True)
    for side in [-1,1]:s.ribbon('Jiangkou '+name+' low granite kerb',s.miter_offset(poly,side*1.74),.15,edge,.045,.20,miter=True)
# The pre-existing x83..54 crossing belongs to the already modelled avenue.
# Split the previous broad estimated ground to expose the photographed bamboo lake.
for name,loc,size in [('west',(41.5,297.5,-.4),(133,185,.6)),('south',(136.5,241.5,-.4),(57,73,.6)),('north',(136.5,354.5,-.4),(57,71,.6))]:
    c.box('North regional terrain preserved '+name,loc,size,p['green'])
c.collection('211_Jiangkou_Trees_Benches_And_Cultural_Screens')
for j,(x,y,scale) in enumerate([(176,148,.90),(167.6,157,.91),(176,170,.86),(164,185,.85),(152,177,.87),(139,185,.85),(123,189,.77),(114.5,198,.75),(31,204,.77),(20,196,.80)]):s.tree(x,y,scale,j*.94)
for x,y,angle in [(168.5,149,math.pi/2),(175.5,164,-math.pi/2),(155,177.8,0),(137,184.2,math.pi),(115.4,191,math.pi/2),(28,203.3,math.pi)]:
    l.bench(x,y,angle);l.lamp(x+1.5,y+1.5)
for x,y in [(168,174),(153,184.6),(128,184),(115,205),(26,196)]:l.shrub('Jiangkou clipped grass-border shrub',x,y,.85,.95,int(x*y))
# The screen layout and isolated large characters are legible in 385; small print is not fabricated.
bronze=c.material('Jiangkou dark cultural screen metal',(.06,.052,.042),.52,.40)
paper=c.material('Jiangkou screen ivory field',(.65,.63,.53),.86)
for i in range(7):
    x=10+i*2.05;y=203.3
    for dx in [-.78,.78]:c.box('Jiangkou culture screen upright',(x+dx,y,1.46),(.075,.09,2.92),bronze)
    c.box('Jiangkou culture screen top',(x,y,2.87),(1.65,.12,.16),bronze)
    # Curved top/bottom profile seen in 385, with pale inset against a dark border.
    for width,dy,mat in [(1.51,0,bronze),(1.39,-.06,paper)]:
        outline=[]
        for q in range(25):
            xx=-width/2+width*q/24;outline.append((x+xx,y+dy,2.50+.14*math.cos(xx/width*math.tau)))
        for q in range(24,-1,-1):
            xx=-width/2+width*q/24;outline.append((x+xx,y+dy,1.02-.14*math.cos(xx/width*math.tau)))
        c.mesh('Jiangkou shaped cultural panel',outline,[tuple(range(len(outline)))],mat)
    for z in [.40,.68,2.7]:c.box('Jiangkou culture screen cross rail',(x,y,z),(1.64,.095,.06),bronze)
    for dx in [-.60,-.4,-.2,0,.2,.4,.6]:c.box('Jiangkou screen lower slat',(x+dx,y,.65),(.03,.08,.8),bronze)
    if i in [1,3,5]:c.text('Jiangkou observed screen character',['廉','清','正'][[1,3,5].index(i)],(x,y-.07,2.01),.36,bronze)
    for j in range(4):c.box('Jiangkou screen unresolved text layout',(x,y-.07,1.26+j*.13),(.96,.006,.014),p['seam'])
# Neutral information board and drainage strips at the future Nantian continuation.
for x in [10,12.4]:c.box('Jiangkou information board post',(x,197.3,1.23),(.1,.1,2.46),bronze)
c.box('Jiangkou information board',(11.2,197.3,1.63),(2.5,.10,1.5),paper)
for x,y in [(120.8,207),(9.5,201.2)]:
    c.box('Jiangkou drain recess',(x,y,.002),(.40,.80,.045),p['dark'])
    for j in range(12):c.box('Jiangkou drain grate',(x,y-.36+j*.065,.032),(.39,.016,.02),p['steel'])
c.collection('212_Zhuyu_Lake_And_Bamboo_Island')
c.box('Zhuyu green lake',(154,298.5,-1.18),(92,41,.06),bpy.data.materials['Heyu green lake water'])
outline=h.island('Zhuyu bamboo island',144,295,12,10,grass,edge)
h.chain_edge('Zhuyu island granite edge',outline,gaps=[((136,287),6)])
c.collection('213_Zhuyu_Angled_Timber_Boardwalk')
wood=c.material('Zhuyu honey timber rail',(.43,.23,.075),.65);c.noise(wood,11,.28,.024)
walk=[(108,294),(118,294),(118,286),(134,286),(143,294)]
pebble=h.pebble('Zhuyu dark pebble paving',(.29,.30,.26))
s.ribbon('Zhuyu zigzag pebble boardwalk',walk,2.7,pebble,0,.30,miter=True)
for sign in [-1,1]:
    side=s.miter_offset(walk,sign*1.38)
    s.ribbon('Zhuyu pale boardwalk edge band',side,.20,p['stone'],.012,.28,miter=True)
    for a,b in zip(side,side[1:]):
        a,b=Vector(a),Vector(b);d=(b-a).normalized();count=max(1,math.ceil((b-a).length/1.6))
        for j in range(count):
            aa=a.lerp(b,j/count);bb=a.lerp(b,(j+1)/count)
            c.box('Zhuyu timber square post',(*aa,.59),(.15,.15,1.18),wood,.012)
            c.box('Zhuyu timber post cap',(*aa,1.2),(.19,.19,.085),wood,.01)
            for z in [.31,.72,1.03]:s.beam('Zhuyu horizontal timber rail',(*aa,z),(*bb,z),.09,.10,wood)
            mid=aa.lerp(bb,.5)
            s.beam('Zhuyu central balustrade upright',(*mid,.31),(*mid,1.03),.065,.065,wood)
    for i in range(0,len(side),2):q=side[i];c.box('Zhuyu boardwalk masonry pier',(*q,-.8),(.35,.4,1.8),edge)
for points in [[(143,294),(150,299),(154,292)]]:s.ribbon('Zhuyu internal pebble path',points,2.2,pebble,0,.17,miter=True)
c.box('Zhuyu waterside viewing platform',(134,286,-.13),(5.4,4.5,.26),pebble)
c.collection('214_Zhuyu_Bamboo_And_Garden_Detail')
rng=random.Random(2363);stem=c.material('Zhuyu bamboo olive culm',(.16,.26,.045),.6);nodes=c.material('Zhuyu pale bamboo nodes',(.34,.36,.14),.75)
v,f,mi=[],[],[];branch_v,branch_f=[],[];mats=c.foliage_materials('Zhuyu narrow bamboo leaf ')
for cx,cy in [(137,299),(141,302),(146,303),(150,304),(154,300),(135,292)]:
    for j in range(17):
        a=rng.random()*math.tau;r=rng.uniform(.05,1.3);x=cx+r*math.cos(a);y=cy+r*math.sin(a);height=rng.uniform(3.8,6.2);lean=Vector((rng.uniform(-.5,.5),rng.uniform(-.5,.5),0))
        for z in range(9):
            aa=Vector((x,y,height*z/9))+lean*z/9;bb=Vector((x,y,height*(z+1)/9))+lean*(z+1)/9
            c.rod('Zhuyu segmented bamboo culm',aa,bb,.031,stem,.028,8)
            c.rod('Zhuyu bamboo node ring',bb-Vector((0,0,.025)),bb+Vector((0,0,.025)),.037,nodes,sides=8)
        for q in range(9):
            zz=height*(.46+.5*q/8);az=rng.random()*math.tau;rr=rng.uniform(.45,1.1)
            base=Vector((x,y,zz))+lean*zz/height
            tip=base+Vector((rr*math.cos(az),rr*math.sin(az),.12))
            c.tube_data(branch_v,branch_f,base,tip,.012,.004,5)
            # Leaves attach in pairs along actual twigs, rather than floating around culms.
            for leaf in range(12):
                angle=az+(-1 if leaf%2 else 1)*.62
                attach=base.lerp(tip,.22+.76*(leaf//2)/5)
                st=len(v);u=Vector((math.cos(angle),math.sin(angle),-.45))*.22
                side=Vector((-math.sin(angle),math.cos(angle),0))*.032;pp=attach+u
                v.extend([attach,pp+side,pp+u,pp-side]);f.append((st,st+1,st+2,st+3));mi.append(rng.randrange(len(mats)))
c.mesh('Zhuyu bamboo leaf-bearing twigs',branch_v,branch_f,stem)
c.mesh('Zhuyu clustered slender bamboo leaves',v,f,mats,mi)
for j,(x,y) in enumerate([(136,303),(151,304),(155,296)]):s.tree(x,y,.66,j*.9)
for x,y in [(140,289),(152,290)]:l.shrub('Zhuyu waterside low planting',x,y,.65,.9,int(x*y))
for x,y in [(146.7,289.2),(147,301)]:l.lamp(x,y)
c.collection('218_Island_Batch_Final_Cameras')
c.camera('97_Jiangkou_shaded_walk',(171.5,145,1.7),(172,177,2.5),28)
c.camera('98_Jiangkou_cultural_screens',(30,197.5,1.7),(17,203.3,1.8),27)
c.camera('99_Zhuyu_timber_walk',(113.8,294,1.7),(132,286,1.4),24)
c.camera('100_Zhuyu_lakeside',(133,284,1.7),(145,299,2.8),23)
c.camera('101_Island_batch_overview',(480,-70,320),(230,185,0),30)
h.save(25,'Integrated island batch. Jiangkou follows Jiushan to future Nantian branch; Zhuyu independently joins Zhongshan. Bamboo lake replaces one broad estimated terrain object. Buildings, distances and branch bends remain image estimates, not survey calibration.',[380,384,385,386,370,363],'101_Island_batch_overview')
