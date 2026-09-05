"""Validate every original tile, reconstruct faces and make labeled QA previews."""
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timezone
import hashlib, json, math, sys, time

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'reference/panoramas'
REPORT=ROOT/'reference/reports'
INV=json.loads((REPORT/'inventory.json').read_text(encoding='utf8'))
SCENES={s['scene_id']:s for s in INV['scenes']}
FONT=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',20)
FACES='fblrud'

def verify(path):
    sid=int(path.stem)
    output=BASE/'faces'/str(sid)
    output.mkdir(parents=True,exist_ok=True)
    statusfile=output/'verification.json'
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    if statusfile.exists():
        old=json.loads(statusfile.read_text(encoding='utf8'))
        if old.get('zip_sha256')==digest and old.get('complete'):
            return old
    result={'scene_id':sid,'name':SCENES[sid]['name'],'category':SCENES[sid]['category'],
            'zip_sha256':digest,'zip_bytes':path.stat().st_size,'complete':False,'errors':[],
            'tiles':[],'faces':[], 'checked_at':datetime.now(timezone.utc).isoformat()}
    try:
        with ZipFile(path) as z:
            manifest=json.loads(z.read('manifest.json'))
            size=manifest['face_size']; count=math.ceil(size/512)
            result['face_size']=size
            if manifest['errors']: raise ValueError('Acquisition contains failed requests')
            expected={u['name'] for u in manifest['urls']}
            actual={n for n in z.namelist() if n.endswith('.jpg')}
            if expected!=actual or len(actual)!=6*count*count: raise ValueError('Missing/unexpected tiles')
            preview=Image.new('RGB',(1536,308),'#f5f4ef')
            draw=ImageDraw.Draw(preview)
            draw.text((8,5),f"{sid} · {result['category']} · {result['name']}",font=FONT,fill='#182528')
            for i,face in enumerate(FACES):
                canvas=Image.new('RGB',(size,size))
                for row in range(1,count+1):
                    for col in range(1,count+1):
                        name=f'{face}/{row:02}_{col:02}.jpg'
                        raw=z.read(name) # ZipFile checks the original CRC while reading.
                        with Image.open(BytesIO(raw)) as im:
                            im.load()
                            want=(min(512,size-(col-1)*512),min(512,size-(row-1)*512))
                            if im.size!=want: raise ValueError(f'{name}: size {im.size} != {want}')
                            canvas.paste(im.convert('RGB'),((col-1)*512,(row-1)*512))
                        result['tiles'].append({'name':name,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)})
                dest=output/f'{face}.jpg'
                canvas.save(dest,quality=96,subsampling=0)
                with Image.open(dest) as check:
                    check.load()
                    if check.size!=(size,size): raise ValueError('Reconstructed face size mismatch')
                result['faces'].append({'face':face,'path':dest.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
                preview.paste(canvas.resize((256,256),Image.Resampling.LANCZOS),(i*256,52))
                draw.text((i*256+8,29),face.upper(),font=FONT,fill='#182528')
                canvas.close()
            preview.save(output/'preview.jpg',quality=92)
            result.update(complete=True,decoded_tiles=len(result['tiles']))
    except Exception as e:
        result['errors'].append(str(e))
    statusfile.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({k:result[k] for k in ['scene_id','complete','errors']},ensure_ascii=False),flush=True)
    return result

def main():
    paths=sorted((BASE/'tiles').glob('*.zip'))
    with ThreadPoolExecutor(max_workers=2) as pool:
        results=list(pool.map(verify,paths))
    summary={'available_archives':len(paths),'complete_panoramas':sum(r['complete'] for r in results),
             'decoded_tiles':sum(r.get('decoded_tiles',0) for r in results),
             'zip_bytes':sum(r['zip_bytes'] for r in results),'errors':[{'scene_id':r['scene_id'],'errors':r['errors']} for r in results if not r['complete']]}
    (REPORT/'panorama_verification.json').write_text(json.dumps({'summary':summary,'scenes':results},ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(summary,ensure_ascii=False),flush=True)
    if '--sheets' in sys.argv:
        complete=[r for r in results if r['complete']]
        qa=BASE/'qa';qa.mkdir(exist_ok=True)
        for start in range(0,len(complete),5):
            subset=complete[start:start+5]
            sheet=Image.new('RGB',(1536,308*len(subset)),'white')
            for j,r in enumerate(subset):
                with Image.open(BASE/'faces'/str(r['scene_id'])/'preview.jpg') as im: sheet.paste(im,(0,308*j))
            sheet.save(qa/f'sheet_{start//5+1:02}.jpg',quality=92)

if __name__=='__main__':
    if '--follow' in sys.argv:
        deadline=time.monotonic()+2400
        last_count=-1
        while time.monotonic()<deadline:
            count=len(list((BASE/'tiles').glob('*.zip')))
            if count!=last_count:
                main()
                last_count=count
                if count==len(SCENES):break
            time.sleep(5)
    else:
        main()
