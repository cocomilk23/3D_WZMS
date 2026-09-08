"""Retain raw full-campus PIE profiler CSVs and summarize each measured view."""
import csv,json,statistics,shutil
from pathlib import Path
root=Path(__file__).resolve().parents[1];capture=json.loads((root/'Reports/campus_profile_captures.json').read_text());assert capture['complete']
results=[]
for record in capture['captures']:
    source=Path(record['csv']);columns=['FrameTime','GameThreadTime','RenderThreadTime','GPUTime','GPUMem/LocalUsedMB'];series={k:[] for k in columns}
    with source.open() as stream:
        for row in csv.DictReader(stream):
            try:frame=float(row['FrameTime'])
            except (ValueError,TypeError,KeyError):continue
            if frame<=0:continue
            for name in columns:
                try:series[name].append(float(row[name]))
                except (ValueError,TypeError,KeyError):pass
    stats={}
    for name,values in series.items():
        if not values:continue
        values=sorted(values);stats[name]={'mean':statistics.mean(values),'median':statistics.median(values),'p95':values[min(len(values)-1,int(len(values)*.95))]}
    dest=root/f'Reports/Campus_Profile_{record["view"]}.csv';shutil.copyfile(source,dest)
    results.append({'view':record['view'],'csv':dest.name,'frames':len(series['FrameTime']),'duration_seconds':sum(series['FrameTime'])/1000,'average_fps':1000/statistics.mean(series['FrameTime']),'timings':stats})
(root/'Reports/campus_performance.json').write_text(json.dumps({'mode':capture['mode'],'fps_cap':60,'gpu':'RTX 3060 Laptop 6GB','views':results,'resolution_note':'Editor viewport, dimensions must be read from the accompanying actual window capture; not a 1080p/4K or packaged-game certification.','limitations':'Three stationary camera samples, 12 seconds each after warmup; first-load streaming or unrestricted movement can differ.'},indent=2))
print(json.dumps(results,indent=2))
