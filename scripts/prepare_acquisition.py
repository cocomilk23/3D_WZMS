from pathlib import Path
import json, math, re, sys
ROOT=Path(__file__).resolve().parents[1]
inv=json.loads((ROOT/'reference/reports/inventory.json').read_text(encoding='utf8'))
jobs=[]
for s in inv['scenes']:
    level=max(s['levels'],key=lambda v:int(v['tiledimagewidth']))
    size=int(level['tiledimagewidth']); template=level['template']
    template=re.sub(r'%\$cdnDomain(\d+)%',r'https://ssl-panoimg\1.720static.com',template)
    urls=[]
    for face in 'fblrud':
        for row in range(1,math.ceil(size/512)+1):
            for col in range(1,math.ceil(size/512)+1):
                url=template.replace('%s',face).replace('%0v',f'{row:02}').replace('%0h',f'{col:02}').replace('%v',str(row)).replace('%h',str(col))
                urls.append(dict(url=url,name=f'{face}/{row:02}_{col:02}.jpg'))
    jobs.append(dict(id=s['scene_id'],name=s['name'],faceSize=size,urls=urls))
(ROOT/'reference/panoramas/tiles').mkdir(parents=True,exist_ok=True)
(ROOT/'reference/reports/acquisition_jobs.json').write_text(json.dumps(jobs,ensure_ascii=False),encoding='utf8')
start=int(sys.argv[1]) if len(sys.argv)>1 else 0
count=int(sys.argv[2]) if len(sys.argv)>2 else 1
template=(ROOT/'scripts/browser_acquire_template.js').read_text(encoding='utf8')
out=ROOT/'scripts/browser_acquire_batch.js'
out.write_text(template.replace('__JOBS__',json.dumps(jobs[start:start+count],ensure_ascii=False)),encoding='utf8')
print(json.dumps({'start':start,'count':len(jobs[start:start+count]),'scene_ids':[j['id'] for j in jobs[start:start+count]],'tiles':sum(len(j['urls']) for j in jobs[start:start+count])}))
