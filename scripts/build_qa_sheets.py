from pathlib import Path
from PIL import Image
import json
ROOT=Path(__file__).resolve().parents[1]
base=ROOT/'reference/panoramas'
paths=[]
for p in sorted((base/'faces').glob('*/verification.json')):
    if json.loads(p.read_text(encoding='utf8')).get('complete'):
        paths.append(p.parent/'preview.jpg')
qa=base/'qa';qa.mkdir(exist_ok=True)
for start in range(0,len(paths),5):
    subset=paths[start:start+5]
    image=Image.new('RGB',(1536,308*len(subset)),'white')
    for j,p in enumerate(subset):
        with Image.open(p) as im:image.paste(im,(0,308*j))
    image.save(qa/f'sheet_{start//5+1:02}.jpg',quality=92)
print(json.dumps({'scenes':len(paths),'sheets':(len(paths)+4)//5}))
