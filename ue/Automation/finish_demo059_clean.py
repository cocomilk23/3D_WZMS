"""Render requested replacement shots, encode clean film and hand off without extra QA."""
import argparse,hashlib,json,os,subprocess,sys,time
from pathlib import Path
from ue_mcp import UnrealMcpClient
from run_campus_zone import run_job
u=Path(__file__).resolve().parents[1];m=Path('E:/WZMS_Media/demo059')
p=json.loads((u/'SourceReference/demo_shots_059.json').read_text(encoding='utf8'));by={s['id']:s for s in p['shots']}
seq=json.loads((u/'Reports/demo_sequences_059.json').read_text())['final']['sequence']
args=argparse.ArgumentParser()
args.add_argument('--replace-middle',action='store_true',help='Replace only the two user-rejected middle shots, atomically updating the same delivered MP4')
args=args.parse_args()
groups=([('middle_r02',['05_meihua','06_gym'])] if args.replace_middle else [('buqing',['03_buqing_wide']),('cultural',['08_math','09_history']),('taohua',['11_taohua'])])
client=UnrealMcpClient();client.connect();patch_reports=[]
try:
 for name,ids in groups:
  start=by[ids[0]]['start_frame'];end=by[ids[-1]]['end_frame'];folder=m/'retakes'/name;report=u/f'Reports/demo059_{name}_render.json'
  req={'name':'Anthem clean revision '+name,'sequence':seq,'directory':str(folder),'resolution':[1920,1080],'samples':8,'frame_range':[start,end],'report':report.name}
  (u/'WZMS/Saved/Logs/demo_render_request.json').write_text(json.dumps(req))
  print('RENDER_START',name,start,end,flush=True);run_job(client,'render_demo_sequence.py');t=time.monotonic()
  while True:
   try:r=json.loads(report.read_text())
   except (FileNotFoundError,json.JSONDecodeError):r={}
   if r.get('complete'):
    if not r.get('success'):raise RuntimeError(r)
    break
   if time.monotonic()-t>1800:raise TimeoutError(name+' render still running')
   time.sleep(3)
  # Basic output completion is necessary to assemble the film; no visual/decode QA pass.
  srcs=sorted(folder.glob('frame_*.png'));assert len(srcs)==end-start,(name,len(srcs),end-start)
  for i,src in enumerate(srcs):
   dst=(m/'frames-master'/f'frame_{start+i:05}.png').resolve()
   assert dst.parent==(m/'frames-master').resolve()
   if dst.exists():dst.unlink()
   os.link(src,dst)
  patch_reports.append({'id':name,'range':[start,end],'report':str(report),'success':True})
  print('RENDER_COMPLETE',name,flush=True);time.sleep(2)
 run_job(client,'close_demo059_editor.py')
finally:
 try:client.close()
 except (OSError,ConnectionError):pass
ff='D:/python/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
out=m/'WZMS_Anthem_Clean_v2_1080p.mp4'
if not args.replace_middle:assert not out.exists(),'Preserve prior deliverables'
# Keep the current playable deliverable until encoding completes successfully.
encoded=m/'WZMS_Anthem_Clean_v2_1080p.pending.mp4' if args.replace_middle else out
assert not encoded.exists(),'Inspect an interrupted encode before retrying'
grade='eq=contrast=1.025:brightness=0.006:saturation=1.035:gamma=1.025,drawbox=x=0:y=0:w=iw:h=60:color=black:t=fill,drawbox=x=0:y=1020:w=iw:h=60:color=black:t=fill,fade=t=in:st=0:d=0.8,fade=t=out:st=76.4:d=2.141667'
print('ENCODE_START clean only',flush=True)
with (m/'encode_clean.log').open('w',encoding='utf8') as log:
 subprocess.run([ff,'-hide_banner','-nostdin','-n','-framerate','24','-i','frames-master/frame_%05d.png','-i','School_Anthem_Master.wav','-filter_threads','4','-vf',grade,'-map','0:v','-map','1:a','-frames:v','1885','-t',str(p['duration_seconds']),'-c:v','libx264','-preset','slow','-crf','16','-pix_fmt','yuv420p','-threads','16','-c:a','aac','-b:a','320k','-ar','48000','-movflags','+faststart',encoded.name],cwd=m,stdout=log,stderr=subprocess.STDOUT,check=True)
if encoded!=out:os.replace(encoded,out)
h=hashlib.sha256()
with out.open('rb') as f:
 for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
r={'version':'demo059','source_game':'0.1.0-final.57','duration_seconds':p['duration_seconds'],'fps':24,'resolution':[1920,1080],'frames':1885,'clean_only':True,'school_anthem_retained':True,'changes':['Single stadium overview only; separate goal/track shots replaced by Math Museum and School History Museum exteriors','Generic waterfront replaced by Taohua Island','Buqing wide arc includes plaza and teaching buildings','Arrival flight raised above near foreground canopy'],'render_patches':patch_reports,'path':str(out),'bytes':out.stat().st_size,'sha256':h.hexdigest(),'additional_visual_and_decode_qa':'Not performed, per explicit user instruction; direct owner acceptance.','user_review_pending':True}
if args.replace_middle:
 r.update(edit_revision='r02',sequence=seq,replaced_in_place=True)
 r['changes']+=['27.375–32.750s: repetitive teaching buildings replaced by Meihua art building facade and entrance','32.750–39.375s: ambiguous lotus/tennis shot replaced by Gym exterior leading into basketball']
 prior=json.loads((m/'delivery-manifest.json').read_text(encoding='utf8'))
 r['render_patches']=prior['render_patches']+patch_reports
(m/'delivery-manifest.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8');(u/'Reports/demo059_delivery.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('DELIVERY_READY',json.dumps(r,ensure_ascii=False),flush=True)
