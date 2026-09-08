"""Derive continuous land and water exclusion from source footprints, keeping bridge passages."""
import json,sys
from pathlib import Path
sys.path.insert(0,'E:/WZMS_UE_Cache/Python')
import shapely
from shapely.geometry import Polygon,mapping
from shapely.ops import unary_union
root=Path(__file__).resolve().parents[1];source=json.loads((root/'SourceReference/terrain_source.json').read_text(encoding='utf8'))
def polygon(r):return shapely.make_valid(Polygon(r['xy']))
water=unary_union([polygon(r) for r in source['water_surfaces']]);all_ground=unary_union([polygon(r) for r in source['land_surfaces']])
land_source=unary_union([polygon(r) for r in source['land_surfaces'] if not any(t in r['object'].lower() for t in ['bridge','deck','boardwalk','trestle'])])
envelope=land_source.convex_hull.buffer(2,join_style=2)
land=shapely.make_valid(envelope.difference(water).union(land_source)).buffer(.45,join_style=2).buffer(-.45,join_style=2).simplify(.06,preserve_topology=True)
# Documented stair approach belongs to the pedestrian footprint.
approach=Polygon([(98,130),(106,130),(106,134.5),(98,134.5)])
land=land.union(approach);walk=land.union(all_ground).buffer(.06,join_style=2)
low=unary_union([polygon(r) for r in source['land_surfaces'] if r['z']<-.12]);upper=unary_union([polygon(r) for r in source['land_surfaces'] if r['z']>=-.12])
low_visible=low.difference(upper).buffer(.04).simplify(.02,preserve_topology=True)
terrain_skin=land.difference(low_visible)
blocked=water.difference(walk).buffer(0).simplify(.10,preserve_topology=True)
result={'units':'Blender metres, X east-ish/Y north; UE uses (X,-Y,Z)*100','derivation':'Source horizontal surfaces, source lake polygons and enclosing campus ground envelope. Bridge/deck surfaces retained as passages and excluded from base-land infill. No measured survey accuracy claimed.','ground_z_m':-.065,'land':mapping(land),'terrain_skin':mapping(terrain_skin),'preserved_low_terraces':mapping(low_visible),'water':mapping(water),'blocked_water':mapping(blocked),'envelope':mapping(envelope),'land_area_m2':land.area,'water_exclusion_area_m2':blocked.area}
(root/'SourceReference/tour_terrain_plan.json').write_text(json.dumps(result),encoding='utf8')
from PIL import Image,ImageDraw,ImageFont
image=Image.new('RGB',(1500,1500),'#e7e7db');draw=ImageDraw.Draw(image);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
minx,miny,maxx,maxy=envelope.union(water).bounds;scale=min(1380/(maxx-minx),1330/(maxy-miny))
def xy(p):return (60+(p[0]-minx)*scale,1430-(p[1]-miny)*scale)
def paint(geo,colour,holecolour):
 for p in shapely.get_parts(geo):
  if p.geom_type!='Polygon':continue
  mask=Image.new('L',image.size,0);pen=ImageDraw.Draw(mask)
  pen.polygon([xy(v) for v in p.exterior.coords],fill=255)
  for ring in p.interiors:pen.polygon([xy(v) for v in ring.coords],fill=0)
  image.paste(colour,(0,0),mask)
paint(envelope,'#d5d7be','#e7e7db');paint(water,'#638f9b','#d5d7be');paint(land,'#a8b68b','#638f9b');paint(all_ground,'#d6cfba','#a8b68b')
for label,x,y in [('South gate',-14.5,-30),('Library',130,155),('Gym',-76,408),('Field',-70,263),('Basketball',14,280),('North gate',94,416),('Tennis',75,-10),('History',257,130),('Math',149,123)]:
 px,py=xy((x,y));draw.ellipse((px-4,py-4,px+4,py+4),fill='#583e2c');draw.text((px+7,py-24),label,font=font,fill='#202a25')
draw.text((60,30),'Campus terrain integration | source footprints and connected land',font=font,fill='#202a25')
draw.text((60,65),'Blue: water  /  green: integrated ground  /  sand: source horizontal surfaces',font=font,fill='#202a25')
out=root/'Reviews/Tour';out.mkdir(parents=True,exist_ok=True);image.save(out/'Terrain_Plan.png')
print('LAND',round(land.area),'WATER_EXCLUSION',round(blocked.area),'POLYGONS',len(list(shapely.get_parts(blocked))),flush=True)
