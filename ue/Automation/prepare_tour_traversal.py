"""Prepare reproducible continuous character routes for the current UE tour geometry."""
import argparse,json,math
from pathlib import Path
root=Path(__file__).resolve().parents[1]
r=json.loads(Path('E:/3D_WZMS/builds/v043_ue_bundle/scene_reference.json').read_text(encoding='utf8'))
p=argparse.ArgumentParser();p.add_argument('--only',nargs='*');p.add_argument('--report',default='tour_complete_routes_runtime.json');args=p.parse_args();cases=[]
for row in r['walkthrough_routes']:
 points=row['floor_points_m']
 if row['name'].startswith('v18: Second floor external'):
  points=[[116,155,4.25],[121.8,155,4.25],[121.8,156.4,4.25],[123.32,156.4,4.58]]+points[4:]
 if args.only and not any(k in row['name'] for k in args.only):continue
 dense=[points[0]]
 for a,b in zip(points,points[1:]):
  n=max(1,math.ceil(math.dist(a,b)/20));dense.extend([[a[j]+(b[j]-a[j])*i/n for j in range(3)] for i in range(1,n+1)])
 cases.append({'name':row['name'],'points':dense})
assert cases
request={'report':args.report,'cases':cases}
(root/'WZMS/Saved/Logs/traversal_request.json').write_text(json.dumps(request),encoding='utf8')
if not args.only:(root/'SourceReference/tour_traversal_cases.json').write_text(json.dumps(request),encoding='utf8')
print('Prepared',len(cases),'connected routes ->',args.report)
