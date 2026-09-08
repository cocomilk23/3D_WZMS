"""Capture selected real UE cameras; wait for complete image files between requests."""
import argparse,json,time
from pathlib import Path
from PIL import Image
from ue_mcp import UnrealMcpClient
from run_campus_zone import run_job
root=Path(__file__).resolve().parents[1]
shots=[('182_Refined_whole_campus','Campus_Aerial'),('18_Buqing_arrival','Campus_Buqing'),('63_Library_Buqing_front','Campus_Library_Exterior'),('67_Library_ground_hall','Campus_Library_Interior'),('111_Alumni_exhibition_hall','Campus_Alumni'),('139_Basketball_eight_overview','Campus_Basketball'),('148_Gym_table_tennis_hall','Campus_Gym_Ground'),('150_Gym_upper_sports_hall','Campus_Gym_Upper'),('153_Math_preface_atrium','Campus_Math'),('161_History_exhibition_aisle','Campus_History'),('164_Canteen_dining_hall','Campus_Canteen'),('40_North_gate_from_campus','Campus_North_Gate')]
parser=argparse.ArgumentParser();parser.add_argument('--only',nargs='*');parser.add_argument('--group',default='Campus',choices=['Campus','Tour']);args=parser.parse_args()
if args.only:shots=[s for s in shots if s[1] in args.only]
client=UnrealMcpClient();client.connect()
try:
    for camera,filename in shots:
        filename+='.png';out=root/'Reviews'/args.group/filename;start=time.time()
        (root/'WZMS/Saved/Logs/review_request.json').write_text(json.dumps({'camera':'Review_'+camera,'filename':filename,'group':args.group}))
        run_job(client,'render_review_view.py')
        while time.time()-start<120:
            if out.exists() and out.stat().st_mtime>start:
                try:
                    with Image.open(out) as im:im.verify()
                    break
                except (OSError,SyntaxError):pass
            time.sleep(.5)
        else:raise TimeoutError(filename)
        print(filename,flush=True)
finally:client.close()
