"""Measure settling on four six-second static views with the shipped renderer settings."""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image
ue=Path(__file__).resolve().parents[1];base=Path(sys.argv[1] if len(sys.argv)>1 else 'E:/WZMS_Media/final057/hold-default')
plan=json.loads((ue/'SourceReference/final057_hold_shots.json').read_text());rows=[];cursor=0
for s in plan['shots']:
 length=round(s['seconds']*plan['fps']);row={'view':s['id'],'seconds':s['seconds'],'first_frame':cursor,'last_frame':cursor+length-1}
 for label,a,b in [('first_second',0,24),('last_second',length-24,length)]:
  frames=np.stack([np.asarray(Image.open(base/f'frame_{cursor+j:05}.png').convert('RGB'),dtype=np.float32) for j in range(a,b)])
  std=frames.std(0).max(2);row[label]={'mean_std_8bit':float(std.mean()),'percent_std_over_12':float((std>12).mean()*100)}
 rows.append(row);cursor+=length
report={'views':rows,'render_settings':'Same 1280x720 MRQ samples=1 settings as before/after comparison. Six-second stationary hold per view. No Nanite pool increase or quality reduction.','interpretation':'Temporal variability also includes AA, GI, vegetation streaming and legitimate water motion; inspect frames before attributing changes.'}
report['frames_directory']=str(base)
(ue/'Reports'/(sys.argv[2] if len(sys.argv)>2 else 'final057_hold_analysis.json')).write_text(json.dumps(report,indent=2));print(json.dumps(rows,indent=2))
