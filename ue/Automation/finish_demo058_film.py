"""Full-anthem promo and matching clean film, with measured sound and bold licensed type."""
import argparse,hashlib,json,shutil,subprocess,sys
from pathlib import Path
from PIL import Image
ue=Path(__file__).resolve().parents[1];media=Path('E:/WZMS_Media/demo058')
ff='D:/python/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
plan=json.loads((ue/'SourceReference/demo_shots_058.json').read_text(encoding='utf8'))
duration=plan['duration_seconds'];frames=round(duration*24)
parser=argparse.ArgumentParser();parser.add_argument('--prepare-only',action='store_true');parser.add_argument('--encode-only',action='store_true');parser.add_argument('--reuse-clean',action='store_true');args=parser.parse_args()
def digest(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def run(cmd,log):
 with (media/log).open('w',encoding='utf8') as f:subprocess.run([ff,'-hide_banner','-nostdin',*cmd],stdout=f,stderr=subprocess.STDOUT,check=True,cwd=media)
def ass_time(t):
 cs=round(t*100);return f'{cs//360000}:{cs//6000%60:02}:{cs//100%60:02}.{cs%100:02}'
def prepare():
 fonts=media/'fonts';fonts.mkdir(exist_ok=True)
 source=media/'Source';source.mkdir(exist_ok=True)
 shutil.copy2('E:/校歌.mp3',source/'School_Anthem.mp3')
 sys.path.insert(0,'E:/WZMS_UE_Cache/Python')
 from fontTools.ttLib import TTFont
 from fontTools.varLib.instancer import instantiateVariableFont
 from fontTools import subset
 text='温州中学校园南大门广场步青图书馆教学楼荷塘网球篮操足球跑道全景水岸在歌声里，重访青春向而行初见求知跃动远望徽篇掠影1902· /—0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
 f=TTFont(ue/'SourceFonts/NotoSansSC/NotoSansSC.ttf');s=subset.Subsetter();s.populate(text=text);s.subset(f);f=instantiateVariableFont(f,{'wght':700},inplace=True)
 for nameid,value in {1:'WZMS Promo Sans',2:'Bold',4:'WZMS Promo Sans Bold',6:'WZMSPromoSans-Bold',16:'WZMS Promo Sans',17:'Bold'}.items():
  f['name'].setName(value,nameid,3,1,0x409)
 f['OS/2'].usWeightClass=700;f['OS/2'].fsSelection=(f['OS/2'].fsSelection|32)&~64;f['head'].macStyle|=1
 f.save(fonts/'WZMSPromoSans-Bold.ttf');shutil.copy2(ue/'SourceFonts/NotoSansSC/OFL.txt',fonts/'OFL.txt')
 # Do not let an earlier experimental font compete for family matching.
 font_source={'base':'Noto Sans SC','base_sha256':digest(ue/'SourceFonts/NotoSansSC/NotoSansSC.ttf'),'license':'SIL Open Font License 1.1','derivative':'WZMS Promo Sans Bold','weight':700,'subset_text':text,'sha256':digest(fonts/'WZMSPromoSans-Bold.ttf')}
 (media/'font_provenance.json').write_text(json.dumps(font_source,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 header='''[Script Info]
Title: WZMS — In the school song
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Location,WZMS Promo Sans,62,&H00F5F8FA,&H00FFFFFF,&H80221A10,&HB020160F,-1,0,0,0,100,100,2,0,1,0.6,1.8,7,0,0,0,1
Style: Small,WZMS Promo Sans,25,&H00CAD8E2,&H00FFFFFF,&H80221A10,&HB020160F,-1,0,0,0,100,100,3,0,1,0,1.2,7,0,0,0,1
Style: Hero,WZMS Promo Sans,104,&H00F5F8FA,&H00FFFFFF,&H80221A10,&HB020160F,-1,0,0,0,100,100,7,0,1,0.6,2,7,0,0,0,1
Style: Shape,WZMS Promo Sans,20,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
 events=[]
 def ev(start,end,style,tags,text,layer=1):events.append(f'Dialogue: {layer},{ass_time(start)},{ass_time(end)},{style},,0,0,0,,{{{tags}}}{text}')
 def label(start,end,title,chapter,top=False):
  y=155 if top else 814
  ev(start,end,'Shape',rf'\pos(130,{y-28})\1c&H709CC8&\p1\fad(400,400)','m 0 0 l 68 0 68 5 0 5',0)
  ev(start,end,'Small',rf'\move(130,{y-3},130,{y-15},0,500)\fad(450,400)',chapter)
  ev(start,end,'Location',rf'\move(126,{y+42},126,{y+30},0,500)\fad(450,400)',title)
 ev(.85,8.8,'Small',r'\pos(132,739)\fad(800,700)','南大门 · 校歌篇')
 ev(.85,8.8,'Hero',r'\move(124,784,124,766,0,900)\fad(800,700)','温州中学')
 ev(1.35,8.8,'Small',r'\pos(132,914)\fs32\fsp2\fad(800,700)','在歌声里，重访校园')
 chapters=['初见','初见','求知','求知','求知','校园','跃动','跃动','跃动','跃动','远望','远望']
 for i,s in enumerate(plan['shots'][1:-1],1):
  a=s['start_frame']/24+.45;b=min(s['end_frame']/24-.4,a+4.4)
  label(a,b,s['title'],f'{i+1:02} / {chapters[i]}',top=s['id']=='03_crest')
 label(66.3,70.2,'校园全景','12 / 远望')
 ev(72.3,78.25,'Small',r'\an8\pos(960,379)\fad(900,1300)','在歌声里，重访校园')
 ev(72.3,78.25,'Hero',r'\an8\pos(960,440)\fs110\fsp12\fad(900,1300)','温州中学')
 ev(72.3,78.25,'Small',r'\an8\pos(960,602)\fsp5\fad(900,1300)','校 园 掠 影')
 ass=header+'\n'.join(events)+'\n';(media/'titles.ass').write_text(ass,encoding='utf-8-sig')
 # Full performance, unchanged speed. Two-pass normalization preserves musical dynamics.
 p=subprocess.run([ff,'-hide_banner','-nostdin','-i',str(source/'School_Anthem.mp3'),'-af','loudnorm=I=-16:TP=-1.5:LRA=20:print_format=json','-f','null','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf8',errors='replace',check=True)
 stats=json.loads(p.stderr[p.stderr.rfind('{'):p.stderr.rfind('}')+1]);(media/'audio_measurement.json').write_text(json.dumps(stats,indent=2)+'\n')
 filt=f'loudnorm=I=-16:TP=-1.5:LRA=20:measured_I={stats["input_i"]}:measured_TP={stats["input_tp"]}:measured_LRA={stats["input_lra"]}:measured_thresh={stats["input_thresh"]}:offset={stats["target_offset"]}:linear=true,apad'
 run(['-y','-i',str(source/'School_Anthem.mp3'),'-af',filt,'-ar','48000','-ac','2','-t',str(duration),'-c:a','pcm_s24le','School_Anthem_Master.wav'],'audio_prepare.log')
 (media/'audio_provenance.json').write_text(json.dumps({'source':'User supplied E:/校歌.mp3','source_sha256':digest(source/'School_Anthem.mp3'),'local_reference_copy':'Source/School_Anthem.mp3','full_performance':True,'tempo_changed':False,'editing':'Full original performance; linear loudness normalization to -16 LUFS with -1.5 dBTP target, no synthetic music, silence pad under one video frame.','duration_seconds':duration,'both_versions_have_same_music':True},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 print('PREPARED titles, bold font and complete anthem audio',flush=True)
if not args.encode_only:prepare()
if args.prepare_only:raise SystemExit(0)
state=json.loads((ue/'Reports/demo058_final_render.json').read_text());assert state.get('complete') and state.get('success')
images=sorted((media/'frames-master').glob('frame_*.png'));assert [p.name for p in images]==[f'frame_{i:05}.png' for i in range(frames)]
if not args.reuse_clean:
 for p in images:
  with Image.open(p) as im:assert im.size==(1920,1080);im.verify()
clean=media/'WZMS_Anthem_Clean_1080p.mp4';promo=media/'WZMS_Anthem_Promo_1080p.mp4'
assert not promo.exists(),'Preserve existing delivered files; choose a new version.'
if args.reuse_clean:
 saved=json.loads((media/'clean_checkpoint.json').read_text())
 assert digest(clean)==saved['sha256'],'Existing clean master changed'
else:assert not clean.exists(),'Preserve existing clean master'
# The same modest grade, 2:1 picture area and beginning/end fades in both versions.
grade=f'eq=contrast=1.025:brightness=0.006:saturation=1.035:gamma=1.025,drawbox=x=0:y=0:w=iw:h=60:color=black:t=fill,drawbox=x=0:y=1020:w=iw:h=60:color=black:t=fill,fade=t=in:st=0:d=0.8,fade=t=out:st=76.4:d=2.141667'
if not args.reuse_clean:
 run(['-n','-framerate','24','-i','frames-master/frame_%05d.png','-i','School_Anthem_Master.wav','-vf',grade,'-map','0:v','-map','1:a','-frames:v',str(frames),'-t',str(duration),'-c:v','libx264','-preset','slow','-crf','16','-pix_fmt','yuv420p','-threads','6','-c:a','aac','-b:a','320k','-ar','48000','-movflags','+faststart',clean.name],'encode_clean.log')
print('ENCODED clean with school anthem',flush=True)
# Bold type is rendered by libass from an explicit local font folder, never OS fallback.
run(['-n','-framerate','24','-i','frames-master/frame_%05d.png','-i',clean.name,'-vf',grade+",ass=filename=titles.ass:fontsdir=fonts",'-map','0:v','-map','1:a','-frames:v',str(frames),'-t',str(duration),'-c:v','libx264','-preset','slow','-crf','16','-pix_fmt','yuv420p','-threads','6','-c:a','copy','-movflags','+faststart',promo.name],'encode_promo.log')
print('ENCODED promo with place labels',flush=True)
for p in [clean,promo]:run(['-v','error','-i',p.name,'-f','null','-'],'decode_'+p.stem+'.log')
manifest={'source_game':'0.1.0-final.57','duration_seconds':duration,'fps':24,'frames':frames,'resolution':[1920,1080],'picture_aspect':'2:1 within 16:9 frame','all_exterior':True,'fresh_render':True,'render_samples':8,'complete_anthem_original_speed':True,'clean_definition':'Same edit, music, grading and fades; no titles, captions or branding overlays.','font':'WZMS Promo Sans Bold, static weight 700 subset of Noto Sans SC under OFL.','full_decode_pass':True,'files':[{'path':str(p),'bytes':p.stat().st_size,'sha256':digest(p)} for p in [promo,clean]],'user_review_pending':True}
(media/'delivery-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(ue/'Reports/demo058_delivery.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(manifest,ensure_ascii=False,indent=2),flush=True)
