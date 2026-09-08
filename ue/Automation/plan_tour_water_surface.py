"""Unify overlapping authored water patches without moving the shoreline or bridges."""
import json,sys
from pathlib import Path
sys.path.insert(0,'E:/WZMS_UE_Cache/Python')
import shapely
from shapely.geometry import Polygon
from shapely.ops import unary_union
from tour_mesh_buffers import buffer,flat
root=Path(__file__).resolve().parents[1]
source=json.loads((root/'SourceReference/terrain_source.json').read_text(encoding='utf8'))
lake=unary_union([Polygon(p['xy']) for p in source['water_surfaces']])
b=buffer();flat(b,lake,-1.15);b['material']=0
(root/'SourceReference/tour_water_surface_buffers.json').write_text(json.dumps({'source':'Exact union of original water footprints; no wave displacement or collision','level_m':-1.15,'area_m2':lake.area,'buffers':[b]}),encoding='utf8')
print('Unified water',round(lake.area),'m2',len(b['triangles']),'triangles')
