"""Compare late stationary frames at identical camera positions; retain data, not a zero-flicker claim."""
import json
from pathlib import Path
import numpy as np
from PIL import Image
ue=Path(__file__).resolve().parents[1];base=Path('E:/WZMS_Media/final057');shots=json.loads((ue/'SourceReference/final057_review_shots.json').read_text())['shots'];rows=[]
for i,s in enumerate(shots):
 row={'view':s['id'],'index':i}
 for phase in ['before','after']:
  frames=np.stack([np.asarray(Image.open(base/phase/f'frame_{i*24+j:05}.png').convert('RGB'),dtype=np.float32) for j in range(12,24)])
  std=frames.std(0).max(2);row[phase]={'mean_pixel_std_8bit':float(std.mean()),'pixels_std_over_3_percent':float((std>3).mean()*100),'pixels_std_over_12_percent':float((std>12).mean()*100),'p99_std':float(np.quantile(std,.99))}
 rows.append(row)
report={'views':rows,'method':'12 final frames from 30 identical stationary camera views, 1280x720, 24fps, MRQ temporal samples=1. Pixel variability includes legitimate water motion, temporal AA and GI noise, not solely z-fighting. Changed crest/court geometry is expected to change image content.','visual_review_required':True}
(ue/'Reports/final057_temporal_comparison.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
for r in rows:print(r['index'],r['view'],round(r['before']['pixels_std_over_12_percent'],3),'->',round(r['after']['pixels_std_over_12_percent'],3),flush=True)
