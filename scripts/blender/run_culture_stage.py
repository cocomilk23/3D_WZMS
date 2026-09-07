import bpy,sys,runpy,gc
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];S=ROOT/'scripts/blender';sys.path.insert(0,str(S))
from culture_stages import STAGES
args=sys.argv[sys.argv.index('--')+1:];rev=int(args[0]);stage=STAGES[rev]
if '--skip-build' not in args:
 bpy.ops.wm.open_mainfile(filepath=str(ROOT/f'models/campus/WZMS_Campus_v{stage["previous"]:03}.blend'))
 runpy.run_path(str(S/stage['builder']),run_name='__main__');gc.collect()
sys.argv=['audit','--',str(rev)];runpy.run_path(str(S/'audit_culture_delivery.py'),run_name='__main__');gc.collect()
sys.argv=['render','--',f'v0.0.{rev}']+stage['cameras'];runpy.run_path(str(S/'render_campus.py'),run_name='__main__')
if rev in (29,33,39):
 sys.argv=['south-wall','--',f'v0.0.{rev}'];runpy.run_path(str(S/'audit_culture_south_wall.py'),run_name='__main__')
print('CULTURE_STAGE_REVIEW_READY',rev,flush=True)
