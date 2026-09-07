"""Decode the archived west-batch reference faces and record their hashes."""
from pathlib import Path
import json,hashlib
from PIL import Image
root=Path(__file__).resolve().parents[1]
ids=[347,348,355,356,360,361,362,374,376,377,378,379,386]
rows=[]
for id in ids:
    for face in 'fblrud':
        file=root/f'reference/panoramas/faces/119232{id}/{face}.jpg'
        with Image.open(file) as im:
            im.load();size=list(im.size)
        assert size[0]==size[1] and size[0]>=4352
        rows.append({'scene':119232000+id,'face':face,'dimensions':size,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
out=root/'deliverables/v0.0.26';out.mkdir(parents=True,exist_ok=True)
(out/'reference_readability.json').write_text(json.dumps({'images':rows,'fully_decoded':len(rows),'geometry_calibrated':False},ensure_ascii=False,indent=2),encoding='utf8')
print('WEST_REFERENCE_FACES_READ',len(rows))
