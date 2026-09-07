"""Decode local sports-batch source faces, without rewriting the frozen source audit."""
from pathlib import Path
import json,hashlib
from PIL import Image
root=Path(__file__).resolve().parents[1]
rows=[]
for ident in [347,348,350,357,358,375,378,379,392]:
    for face in 'fblrud':
        file=root/f'reference/panoramas/faces/119232{ident}/{face}.jpg'
        with Image.open(file) as im:im.load();size=list(im.size)
        assert size[0]==size[1] and size[0]>=4352
        rows.append(dict(scene=119232000+ident,face=face,dimensions=size,sha256=hashlib.sha256(file.read_bytes()).hexdigest()))
out=root/'deliverables/v0.0.30';out.mkdir(parents=True,exist_ok=True)
(out/'reference_readability.json').write_text(json.dumps(dict(images=rows,fully_decoded=len(rows),geometry_calibrated=False),ensure_ascii=False,indent=2),encoding='utf8')
print('SPORTS_REFERENCE_FACES_READ',len(rows))
