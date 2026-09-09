"""Capture open interiors from actual PIE cameras; no temporary lighting changes."""
import argparse,json,time,subprocess,sys,hashlib
from pathlib import Path
from ue_mcp import UnrealMcpClient
from run_campus_zone import run_job
root=Path(__file__).resolve().parents[1]
shots=[('67_Library_ground_hall','Library_Ground'),('69_Library_second_hall','Library_Second'),('70_Library_curved_stairs','Library_Curved'),('Tour_Library_Top','Library_Top'),('106_Zhouyuan_entry','Zhouyuan'),('Tour_Zhouyuan_Inside','Zhouyuan_Inside'),('111_Alumni_exhibition_hall','Alumni'),('148_Gym_table_tennis_hall','Gym_Ground'),('150_Gym_upper_sports_hall','Gym_Upper'),('153_Math_preface_atrium','Math_Ground'),('158_Math_upper_rest_corner','Math_Upper'),('161_History_exhibition_aisle','History'),('164_Canteen_dining_hall','Canteen')]
p=argparse.ArgumentParser();p.add_argument('--window-ref',required=True);p.add_argument('--only',nargs='*');p.add_argument('--prefix',default='Runtime049_');a=p.parse_args()
assert a.prefix.replace('_','').replace('-','').isalnum()
if a.only:shots=[s for s in shots if s[1] in a.only]
client=UnrealMcpClient();client.connect()
try:
 for camera,name in shots:
  request=root/'WZMS/Saved/Logs/tour_camera_request.json'
  request.write_text(json.dumps({'camera':'Review_'+camera}),encoding='utf8')
  run_job(client,'review_tour_runtime_camera.py')
  time.sleep(5)
  out=root/'Reviews/Tour'/(a.prefix+name+'.png')
  subprocess.run([sys.executable,str(root/'Automation/capture_view.py'),str(out),a.window_ref],check=True)
  print('CAPTURED',name,hashlib.sha256(out.read_bytes()).hexdigest(),flush=True)
finally:client.close()
