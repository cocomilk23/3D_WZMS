"""Capture every open interior and the repaired circulation in actual UE renders."""
import json,time,argparse
from pathlib import Path
from PIL import Image
from ue_mcp import UnrealMcpClient
from run_campus_zone import run_job
root=Path(__file__).resolve().parents[1]
shots=[('67_Library_ground_hall','Library_Ground'),('69_Library_second_hall','Library_Second'),('70_Library_curved_stairs','Library_Curved'),('Tour_Library_Top','Library_Top'),('106_Zhouyuan_entry','Zhouyuan'),('Tour_Zhouyuan_Inside','Zhouyuan_Inside'),('111_Alumni_exhibition_hall','Alumni'),('148_Gym_table_tennis_hall','Gym_Ground'),('150_Gym_upper_sports_hall','Gym_Upper'),('153_Math_preface_atrium','Math_Ground'),('158_Math_upper_rest_corner','Math_Upper'),('161_History_exhibition_aisle','History'),('164_Canteen_dining_hall','Canteen')]
p=argparse.ArgumentParser();p.add_argument('--only',nargs='*');args=p.parse_args()
if args.only:shots=[s for s in shots if s[1] in args.only]
client=UnrealMcpClient();client.connect()
try:
 for camera,name in shots:
  out=root/'Reviews/Tour'/(name+'.png');start=time.time()
  (root/'WZMS/Saved/Logs/review_request.json').write_text(json.dumps({'camera':'Review_'+camera,'filename':out.name,'group':'Tour'}),encoding='utf8')
  run_job(client,'render_review_view.py')
  while time.time()-start<120:
   if out.exists() and out.stat().st_mtime>start:
    try:
     with Image.open(out) as im:im.verify()
     break
    except (OSError,SyntaxError):pass
   time.sleep(.5)
  else:raise TimeoutError(name)
  print(name,flush=True)
finally:client.close()
