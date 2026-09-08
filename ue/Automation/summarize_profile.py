import csv,json,statistics,shutil
from pathlib import Path
root=Path(__file__).resolve().parents[1]
source=max((root/'WZMS/Saved/Profiling/CSV').glob('*.csv'),key=lambda p:p.stat().st_mtime)
columns=['FrameTime','GameThreadTime','RenderThreadTime','GPUTime','GPUMem/LocalUsedMB']
series={name:[] for name in columns}
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
    values=sorted(values)
    stats[name]={'mean':statistics.mean(values),'median':statistics.median(values),'p95':values[min(len(values)-1,int(len(values)*.95))]}
dest=root/'Reports/South_Runtime_Profile.csv';shutil.copyfile(source,dest)
result={'source':dest.name,'frames':len(series['FrameTime']),'duration_seconds':sum(series['FrameTime'])/1000,'average_fps':1000/statistics.mean(series['FrameTime']),'timings':stats,'mode':'UE 5.8 Play In Editor, south gate/plaza view','gpu':'RTX 3060 Laptop 6GB','fps_cap':60,'displayed_game_viewport_pixels':[1355,539],'limitations':['One fixed ground view over about 12 seconds; not a whole-zone walk or packaged benchmark.','Viewport dimensions measured from the Slate screenshot; this does not certify 1080p or 4K performance.']}
(root/'Reports/south_performance.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
