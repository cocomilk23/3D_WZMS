"""Check the exported campus, view catalog, local HTTP assets and frozen source."""
import json,struct,hashlib,urllib.request
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parents[1];WEB=ROOT/'web-preview';OUT=ROOT/'deliverables/v0.0.16'
export=json.loads((OUT/'export_validation.json').read_text(encoding='utf8'))
assert hashlib.sha256((ROOT/export['source']).read_bytes()).hexdigest()==export['source_sha256']
data=(ROOT/export['file']).read_bytes();magic,version,total=struct.unpack_from('<III',data)
assert magic==0x46546C67 and version==2 and total==len(data)==export['bytes']
assert hashlib.sha256(data).hexdigest()==export['sha256']
length,kind=struct.unpack_from('<II',data,12);assert kind==0x4E4F534A
gltf=json.loads(data[20:20+length]);assert gltf['meshes'] and gltf['scenes']
for view in gltf['bufferViews']:
 assert view.get('byteOffset',0)+view['byteLength']<=gltf['buffers'][view.get('buffer',0)]['byteLength']
assert all('uri' not in item for item in gltf.get('images',[])), 'Photographs must be embedded'
catalog=(WEB/'views.js').read_text(encoding='utf8')
views=json.loads(catalog.removeprefix('export default ').strip().removesuffix(';'))
assert len(views)==22
for preset in views.values():
 image=WEB/'assets'/preset['image'];header=image.read_bytes()[:24]
 assert header[:8]==b'\x89PNG\r\n\x1a\n' and all(struct.unpack('>II',header[16:24]))
paths=['','viewer.js','views.js','style.css','assets/campus-v015.glb',
 'node_modules/three/build/three.module.js','node_modules/three/examples/jsm/libs/draco/gltf/draco_decoder.wasm']
paths+=['assets/'+preset['image'] for preset in views.values()]
def check(path):
 req=urllib.request.Request('http://127.0.0.1:8766/'+path,method='HEAD')
 with urllib.request.urlopen(req,timeout=15) as response:assert response.status==200
 return path
with ThreadPoolExecutor(max_workers=4) as pool:resources=list(pool.map(check,paths))
report={'version':'v0.0.16','model_version':'v0.0.15','source_blend_unchanged':True,'glb_bytes':len(data),
 'meshes':len(gltf['meshes']),'primitives':sum(len(m['primitives']) for m in gltf['meshes']),
 'triangles':sum(gltf['accessors'][p['indices']]['count']//3 for m in gltf['meshes'] for p in m['primitives']),
 'embedded_images':len(gltf.get('images',[])),'camera_presets':len(views),'http_resources_passed':len(resources),
 'url':'http://127.0.0.1:8766/','public_deployment':False}
(OUT/'asset_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=False))
