"""Seal an actually reviewed saved-file culture milestone, then Git it separately."""
from pathlib import Path
import argparse,json,hashlib,struct,zlib,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts/blender'))
from culture_stages import STAGES
p=argparse.ArgumentParser();p.add_argument('revision',type=int);p.add_argument('--images-reviewed',action='store_true');a=p.parse_args()
if not a.images_reviewed:raise SystemExit('Review every rendered image before sealing.')
ver=f'v0.0.{a.revision}';out=ROOT/'deliverables'/ver;stage=STAGES[a.revision]
r=json.loads((out/'render_validation.json').read_text(encoding='utf8'));g=json.loads((out/'geometry_validation.json').read_text(encoding='utf8'));b=json.loads((out/'preservation_validation.json').read_text(encoding='utf8'))
assert r['version']==ver and g['all_passed'] and b['all_unexpected_changes_absent'] and not r['missing_external_images']
assert [x['camera'] for x in r['renders']]==stage['cameras']
images=[]
for rec in r['renders']:
 data=(out/rec['file']).read_bytes();assert data[:8]==b'\x89PNG\r\n\x1a\n';w,h=struct.unpack('>II',data[16:24]);assert (w,h)==(1600,1000)
 pos=8;compressed=[]
 while pos<len(data):
  length=struct.unpack('>I',data[pos:pos+4])[0];typ=data[pos+4:pos+8];body=data[pos+8:pos+8+length];crc=struct.unpack('>I',data[pos+8+length:pos+12+length])[0];assert zlib.crc32(typ+body)&0xffffffff==crc
  if typ==b'IDAT':compressed.append(body)
  pos+=length+12
 assert zlib.decompress(b''.join(compressed))
 images.append(dict(file=rec['file'],dimensions=[w,h],sha256=hashlib.sha256(data).hexdigest()))
file=ROOT/f'models/campus/WZMS_Campus_v{a.revision:03}.blend'
report=dict(version=ver,title=stage['title'],model=file.relative_to(ROOT).as_posix(),bytes=file.stat().st_size,sha256=hashlib.sha256(file.read_bytes()).hexdigest(),images_visually_reviewed=True,previews=images,geometry_passed=True,unexpected_predecessor_changes=False,approved_replacements=b['approved_context_replacements'],user_acceptance='pending',absolute_1_to_1_calibrated=False,ue_playthrough_verified=False,web_preview_updated=False)
(out/'delivery_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(ver,'SEALED',len(images),'images',report['sha256'])
