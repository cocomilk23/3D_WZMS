"""v023 observed Meihua art building, concave front, white frame and paved forecourt."""
import bpy,math,sys
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).parent))
import campus_common as c,north_common as n,north_landscape as l,south_detail_common as s,island_common as h,culture_common as k
sc=bpy.data.scenes['WZMS_Campus'];c.activate(sc);p=n.palette()
oldchain=bpy.data.objects['History shoreline chain runs'];chainverts=[tuple(v.co) for v in oldchain.data.vertices]
# Open only the new shared east-west route in the previous chain run.
removed_blocks=set()
for i in range(0,len(chainverts),12):
    q=sum((Vector(v) for v in chainverts[i:i+12]),Vector())/12
    if q.x>268 and 100<q.y<144:removed_blocks.add(i//12)
chainfaces=[tuple(p.vertices) for p in oldchain.data.polygons if p.vertices[0]//12 not in removed_blocks]
chainmat=oldchain.data.materials[0]
retired_posts=[o.name for o in sc.objects if o.name.startswith('History shoreline granite post') and o.location.x>268 and 100<o.location.y<144]
h.retire('v0.0.23',collections=['172_History_Neighbouring_Cultural_Building_Context'],names=['History shoreline chain runs']+retired_posts)
c.collection('190_Meihua_Island_And_Art_Plaza')
c.mesh('Meihua preserved history chain with shared path opening',chainverts,chainfaces,chainmat)
soil=s.mottled('Meihua planted ground',[(.065,.13,.024),(.24,.25,.065)],2.3);bank=h.pebble('Meihua weathered revetment',(.30,.32,.29))
outline=h.island('Meihua art island',296,127,28,28,soil,bank)
c.box('Meihua east lake extension',(335,125,-1.18),(70,140,.06),bpy.data.materials['Heyu green lake water'])
walk=n.paving('Meihua light rectangular plaza brick',(.65,.66,.57),(.20,.10),.004)
red=n.paving('Meihua rose promenade',(.43,.28,.22),(.60,.40),.007)
green=n.paving('Meihua green plaza bands',(.19,.28,.17),(.20,.10),.004)
s.ribbon('Meihua shared cultural forecourt land',[(246,112),(267,112),(306,112),(323,115)],14,soil,-.03,1.5,miter=True)
s.ribbon('Meihua shared cultural promenade',[(246,112),(267,112),(306,112),(323,115)],3.7,red,0,.20,miter=True)
c.box('Meihua rectangular art forecourt',(294,119,-.11),(49,12,.22),walk)
for x in [273,280,287,294,301,308,315]:c.box('Meihua forecourt green grid',(x,119,.007),(.25,12,.014),green)
for y in [115,120,124.7]:c.box('Meihua forecourt cross bands',(294,y,.008),(49,.22,.016),green)
# Continue toward the stone bridge reserved for the next island.
c.box('Meihua east bridgehead',(322,115,-.10),(6,5,.20),walk)
c.collection('191_Meihua_Curved_Art_Building')
clad=n.paving('Meihua pale aluminium stone panels',(.72,.74,.70),(1.05,.65),.006)
glass=c.material('Meihua translucent green curtain wall',(.12,.34,.27),.17,.20)
bs=glass.node_tree.nodes.get('Principled BSDF');bs.inputs['Transmission Weight'].default_value=.45;bs.inputs['IOR'].default_value=1.45
frame=c.material('Meihua sage green window frames',(.26,.47,.35),.34,.55)
roof=c.material('Meihua zinc roof',(.18,.22,.21),.52,.40)
def fy(x):return 126+.005*(x-301)**2
xs=[282+i*38/24 for i in range(25)]
foundation=c.mesh('Meihua continuous curved foundation',[(x,fy(x),.24) for x in xs]+[(320,141,.24),(282,141,.24)],[tuple(range(27))],p['stone'])
foundation.modifiers.new('Foundation to ground','SOLIDIFY').thickness=.70
for z in [.48,4.55,8.55]:
    v=[(x,fy(x),z) for x in xs]+[(320,141,z),(282,141,z)]
    ob=c.mesh('Meihua curved floor slab',v,[tuple(range(len(v)))],p['stone']);mod=ob.modifiers.new('Concrete slab thickness','SOLIDIFY');mod.thickness=.24
for i,(a,b) in enumerate(zip(xs,xs[1:])):
    ya,yb=fy(a),fy(b)
    # Two storeys: narrow lower slit glazing, broad continuous upper ribbon.
    c.mesh('Meihua upper glazing ribbon',[(a,ya,4.48),(b,yb,4.48),(b,yb,7.72),(a,ya,7.72)],[(0,1,2,3)],glass)
    c.mesh('Meihua continuous cornice',[(a,ya,7.72),(b,yb,7.72),(b,yb,8.72),(a,ya,8.72)],[(0,1,2,3)],clad)
    mid=(a+b)/2;ym=fy(mid)
    if b>291.0 and a<295.5:
        # Entry stays open below its glazed transom.
        c.mesh('Meihua entry transom',[(a,ya,3.3),(b,yb,3.3),(b,yb,4.48),(a,ya,4.48)],[(0,1,2,3)],glass)
    else:
        for lo,hi in [(a,mid-.22),(mid+.22,b)]:
            c.mesh('Meihua lower white panel',[(lo,fy(lo),.48),(hi,fy(hi),.48),(hi,fy(hi),4.48),(lo,fy(lo),4.48)],[(0,1,2,3)],clad)
        c.mesh('Meihua lower narrow window',[(mid-.22,fy(mid-.22),.92),(mid+.22,fy(mid+.22),.92),(mid+.22,fy(mid+.22),4.1),(mid-.22,fy(mid-.22),4.1)],[(0,1,2,3)],glass)
        for xx in [mid-.22,mid+.22]:s.beam('Meihua narrow window side sash',(xx,fy(xx)-.015,.92),(xx,fy(xx)-.015,4.1),.032,.04,frame)
        for z in [.92,2.5,4.1]:s.beam('Meihua narrow window cross sash',(mid-.22,fy(mid-.22)-.015,z),(mid+.22,fy(mid+.22)-.015,z),.03,.04,frame)
        for z0,z1 in [(.48,.92),(4.1,4.48)]:c.mesh('Meihua lower slit sill and head',[(mid-.22,fy(mid-.22),z0),(mid+.22,fy(mid+.22),z0),(mid+.22,fy(mid+.22),z1),(mid-.22,fy(mid-.22),z1)],[(0,1,2,3)],clad)
    s.beam('Meihua upper window upright',(a,ya-.04,4.5),(a,ya-.04,7.75),.055,.07,frame)
    for z in [4.48,5.18,5.88,6.58,7.28,7.72]:s.beam('Meihua upper sash transom',(a,ya-.04,z),(b,yb-.04,z),.055,.07,frame)
# Back and side elevations are estimated enclosure, independently identifiable.
for x in [282,320]:
    c.box('Meihua estimated side wall',(x,(fy(x)+141)/2,4.60),(.24,141-fy(x),8.24),clad)
    for y in [132,136,139]:
        for z in [2.3,6.4]:c.box('Meihua side recessed glazing',(x+(-.14 if x==282 else .14),y,z),(.025,1.3,2.2),glass)
c.box('Meihua estimated rear wall',(301,141,4.6),(38,.25,8.24),clad)
for x in range(284,320,3):
    for z in [2.3,6.4]:c.box('Meihua rear window',(x,141.14,z),(1.35,.03,2.15),glass)
c.box('Meihua low upper roof',(301,135.8,8.77),(38.5,11.2,.20),roof)
for x in range(283,320,2):c.box('Meihua roof seam',(x,135.8,8.88),(.027,11.2,.024),roof)
# Closed shallow roof wedge meets the curved front without open slivers.
v=[(x,fy(x)-.2,8.75) for x in xs]+[(320,131,8.85),(282,131,8.85)]
c.mesh('Meihua curved front roof cap',v,[tuple(range(len(v)))],roof)
c.collection('192_Meihua_White_Entrance_Frame')
white=c.material('Meihua structural white enamel',(.81,.83,.79),.4,.18)
for x in [290.1,296.0]:c.box('Meihua tall entrance square upright',(x,122.9,5.55),(.32,.40,11.1),white)
for z in [.15,4.1,8.1,10.9]:c.box('Meihua entrance frame crossbar',(293.05,122.9,z),(6.22,.42,.26),white)
for z in [3.95,8.0]:
    c.box('Meihua clear entrance canopy',(293.05,124.4,z),(6.4,4.0,.09),glass)
    for x in [290.2,291.6,293,294.4,295.8]:s.beam('Meihua canopy white joist',(x,122.45,z-.1),(x,126.5,z-.1),.11,.14,white)
k.stairs('Meihua entrance granite steps',(293,120,0),(293,122.4,.48),4.8,3,p['stone'],False)
c.box('Meihua upper entry landing',(293,124.45,.36),(5.1,4.1,.24),walk)
for x in [291.7,294.6]:
    c.box('Meihua open glass door',(x,127.5,1.88),(.04,1.2,2.8),glass)
    c.rod('Meihua door handle',(x-.04,127.6,1.2),(x-.04,127.6,1.9),.018,p['steel'])
c.box('Meihua entry vestibule floor',(293,130,.36),(5,7,.24),walk)
c.text('Meihua art building identification','艺 术 楼',(306,fy(306)-.10,8.01),.43,c.material('Meihua bronze lettering',(.16,.18,.08),.4,.55))
c.collection('193_Meihua_Garden_And_Sculpture')
for j,(x,y,scale) in enumerate([(274,104,.74),(287,104,.87),(307,106,.76),(320,124,.77),(324,137,.81),(292,148,.77),(306,148,.80)]):s.tree(x,y,scale,j*.74)
for x,y in [(278,108),(281,109),(305,108),(309,107),(320,131),(286,146)]:l.shrub('Meihua clipped planting',x,y,.9,1.0,int(x*y))
# Observed standing sculpture represented as an unattributed silhouette, no invented name.
l.standing_statue(279,109,.7)
for x,y in [(275,113.9),(302,109),(318,117.7)]:l.lamp(x,y)
for x,y in [(277,113.8),(305,109)]:l.bench(x,y,0)
h.chain_edge('Meihua outer shore',outline,gaps=[((323,115),6),((272,112),12)])
c.collection('198_Meihua_Review_Cameras')
c.camera('89_Meihua_art_facade',(304,111,1.72),(300,128,4.4),22)
c.camera('90_Meihua_entry_frame',(286,112,1.7),(293,126,5),24)
c.camera('91_Meihua_plaza',(275,114,1.7),(299,125,3.2),23)
c.camera('92_Meihua_waterside_overview',(337,81,45),(283,126,3),38)
h.use_facade_uv(clad)
for o in sc.objects:
    if o.type=='MESH' and clad.name in o.data.materials:h.vertical_uv(o)
h.save(23,'Meihua art building exterior and garden plaza, based on 421; replaces only the unconfirmed 172 context. Museum retained. Entry vestibule only; 422 art interiors reserved for a separate stage. Dimensions and rear elevations estimated.',[383,405,421,422,347],'92_Meihua_waterside_overview')
