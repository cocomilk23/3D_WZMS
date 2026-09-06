"""One stage at a time: build, reopen and audit, then render review cameras.
Example: blender -b --factory-startup --python-exit-code 1 --python run_south_stage.py -- 13
Pass --skip-build after a local correction, never rebuild a user-modified delivery.
"""
import bpy,sys,runpy,gc
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];S=ROOT/'scripts/blender'
args=sys.argv[sys.argv.index('--')+1:];rev=int(args[0]);ver=f'v0.0.{rev}'
stages={12:('build_tennis.py',['45_Tennis_ground_toward_wall','46_Tennis_net_and_campus','47_Tennis_entry','48_Tennis_overview']),
13:('build_daosi.py',['49_Daosi_shaded_curve','50_Daosi_flower_bridge','51_Daosi_lakeside_lookback','52_Daosi_north_junction','53_Daosi_overview']),
14:('build_heyu.py',['54_Heyu_island_and_banyans','55_Heyu_bridge_toward_campus','56_Heyu_lotus_and_courts','57_Heyu_overview']),
15:('build_shuinan.py',['58_Shuinan_toward_island','59_Shuinan_toward_court_peninsula','60_Shuinan_court_and_lotus','61_Shuinan_bridge_overview','62_Southern_four_scene_integration'])}
builder,cameras=stages[rev]
if '--skip-build' not in args:
 bpy.ops.wm.open_mainfile(filepath=str(ROOT/f'models/campus/WZMS_Campus_v{rev-1:03}.blend'))
 runpy.run_path(str(S/builder),run_name='__main__');gc.collect()
sys.argv=['audit','--',str(rev)];runpy.run_path(str(S/'audit_south_deliveries.py'),run_name='__main__');gc.collect()
sys.argv=['render','--',ver]+cameras;runpy.run_path(str(S/'render_campus.py'),run_name='__main__')
print('SOUTH_STAGE_REVIEW_READY',ver,flush=True)
