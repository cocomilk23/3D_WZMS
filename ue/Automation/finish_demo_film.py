"""Create original restrained audio/titles and encode the verified UE image sequence."""
import argparse,json,hashlib,math,subprocess,wave
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ue=Path(__file__).resolve().parents[1]
media=Path('E:/WZMS_Media/demo055');media.mkdir(parents=True,exist_ok=True)
ff=Path('D:/python/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe')
font=ue/'SourceFonts/NotoSansSC/NotoSansSC.ttf'
parser=argparse.ArgumentParser();parser.add_argument('--prepare-only',action='store_true');parser.add_argument('--reuse-clean',action='store_true');args=parser.parse_args()

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(8*1024*1024),b''):h.update(block)
    return h.hexdigest()

def prepare():
    sr=48000;seconds=60;rng=np.random.default_rng(55);audio=np.zeros((sr*seconds,2),np.float64)
    def tone(midi,start,duration,level,pan,pad=False):
        n=int(sr*duration);t=np.arange(n)/sr;hz=440*2**((midi-69)/12)
        if pad:
            env=np.sin(np.pi*np.minimum(t/duration,1))**2
            y=(np.sin(2*np.pi*hz*t)+.22*np.sin(2*np.pi*hz*1.0018*t+.3))*env
        else:
            env=(1-np.exp(-t/0.018))*np.exp(-t/2.0)*np.minimum(1,(duration-t)/.4)
            y=(np.sin(2*np.pi*hz*t)+.25*np.sin(2*np.pi*hz*2.002*t)*np.exp(-t/.8)+.06*np.sin(2*np.pi*hz*3*t)*np.exp(-t/.3))*env
        a=int(sr*start);b=min(len(audio),a+n)
        if b>a:audio[a:b]+=y[:b-a,None]*level*np.array([math.sqrt((1-pan)/2),math.sqrt((1+pan)/2)])
    # Original D major / B minor / G major / A suspended progression, no sampled recording.
    chords=[[50,57,61,66],[47,54,57,62],[43,50,57,59],[45,52,57,62]]
    for bar in range(8):
        start=bar*8;chord=chords[bar%4]
        for j,m in enumerate(chord):tone(m,start,min(8.8,60-start),.005,-.45+j*.3,True)
        for j in range(4):
            at=start+1+j*1.65
            if at<58:tone(chord[(j+bar)%4]+12,at,5,.034,-.35+.7*rng.random())
    wet=np.zeros_like(audio)
    for delay,gain in [(.083,.16),(.149,.13),(.263,.10),(.431,.075),(.691,.04)]:
        shift=int(sr*delay);wet[shift:]+=audio[:-shift,::-1]*gain
    audio+=wet
    with wave.open(str(ue/'SourceAudio/Tour_Gentle_Air.wav'),'rb') as f:
        source=np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').astype(np.float64)/32768
        source=source.reshape(-1,f.getnchannels()).mean(axis=1);source_sr=f.getframerate()
    t=np.arange(sr*seconds)/sr
    air=np.interp((t% (len(source)/source_sr))*source_sr,np.arange(len(source)),source)
    audio+=air[:,None]*.22
    fade=np.minimum(t/2,1)*np.minimum((seconds-t)/3,1);audio*=fade[:,None]
    rms=float(np.sqrt(np.mean(audio**2)));audio*=10**(-23/20)/max(rms,1e-9)
    peak=float(np.max(np.abs(audio)));audio*=min(1,.82/max(peak,1e-9))
    with wave.open(str(media/'Original_Ambient_Score.wav'),'wb') as f:
        f.setnchannels(2);f.setsampwidth(2);f.setframerate(sr);f.writeframes((audio*32767).astype('<i2').tobytes())
    def title(path,end=False):
        im=Image.new('RGBA',(1920,1080));draw=ImageDraw.Draw(im)
        def face(size):
            f=ImageFont.truetype(str(font),size);f.set_variation_by_axes([400]);return f
        if end:
            draw.rectangle((0,0,1920,1080),fill=(6,15,18,85))
            x,y=960,425;anchor='mt'
            draw.text((x,y),'温州中学',font=face(76),fill=(255,255,252,255),anchor=anchor)
            draw.text((x,y+110),'校 园 漫 游',font=face(36),fill=(245,246,237,250),anchor=anchor)
            draw.text((x,y+191),'3D 场景 Demo  ·  自由探索',font=face(25),fill=(235,239,229,245),anchor=anchor)
            draw.line((885,y+173,1035,y+173),fill=(206,220,195,205),width=2)
        else:
            # Quiet lower-left lockup, leaving the actual gate lettering readable.
            for y in range(730,1080):
                draw.line((0,y,1919,y),fill=(4,12,16,int(115*(y-730)/350)))
            draw.text((126,819),'校园漫游',font=face(60),fill=(255,255,252,255))
            draw.text((130,911),'温州中学  /  3D 场景 Demo',font=face(27),fill=(240,244,237,250))
            draw.line((130,807,194,807),fill=(215,225,196,255),width=3)
        im.save(media/path)
    title('title_intro.png');title('title_outro.png',True)
    (media/'audio_provenance.json').write_text(json.dumps({'composition':'Original deterministic ambient keys/pads by this project; no third-party recording or music sample.','environment':'Project original Tour_Gentle_Air.wav, synthesized air ambience; not a recording of the school.','audio':{'sample_rate':sr,'seconds':seconds,'channels':2,'sha256':digest(media/'Original_Ambient_Score.wav')},'font':'Noto Sans SC, SIL Open Font License; see project ue/SourceFonts/NotoSansSC/OFL.txt.'},indent=2)+'\n',encoding='utf8')

prepare()
if args.prepare_only:
    print('Prepared original stereo audio and title overlays',flush=True);raise SystemExit(0)
state=json.loads((ue/'Reports/demo055_final_render.json').read_text())
assert state.get('complete') and state.get('success'),state
frames=media/'frames-master';files=sorted(frames.glob('frame_*.png'))
assert [p.name for p in files]==[f'frame_{i:05}.png' for i in range(1440)],'Missing, extra or misnumbered frames'
if not args.reuse_clean:
    for p in files:
        with Image.open(p) as im:assert im.size==(1920,1080);im.verify()
clean=media/'WZMS_Demo_60s_Clean_1080p.mp4';promo=media/'WZMS_Demo_60s_Promo_1080p.mp4'
assert not promo.exists(),'Preserve existing deliverables'
if args.reuse_clean:
    previous=json.loads((media/'delivery-manifest-r01.json').read_text(encoding='utf8'))
    expected=next(x['sha256'] for x in previous['files'] if Path(x['path']).name==clean.name)
    assert digest(clean)==expected,'Clean master changed'
else:
    assert not clean.exists(),'Preserve existing clean master'
    subprocess.run([str(ff),'-hide_banner','-nostdin','-n','-framerate','24','-i',str(frames/'frame_%05d.png'),'-c:v','libx264','-preset','slow','-crf','17','-pix_fmt','yuv420p','-threads','6','-movflags','+faststart',str(clean)],check=True)
filters='[0:v]fade=t=in:st=0:d=0.7,fade=t=out:st=58:d=2[base];[1:v]format=rgba,fade=t=in:st=0.9:d=0.8:alpha=1,fade=t=out:st=5.8:d=0.8:alpha=1[intro];[2:v]format=rgba,fade=t=in:st=53.7:d=1.2:alpha=1,fade=t=out:st=58:d=2:alpha=1[outro];[base][intro]overlay=0:0:shortest=1[v1];[v1][outro]overlay=0:0:shortest=1[v]'
subprocess.run([str(ff),'-hide_banner','-nostdin','-n','-i',str(clean),'-loop','1','-framerate','24','-i',str(media/'title_intro.png'),'-loop','1','-framerate','24','-i',str(media/'title_outro.png'),'-i',str(media/'Original_Ambient_Score.wav'),'-filter_complex_threads','2','-filter_complex',filters,'-map','[v]','-map','3:a','-t','60','-r','24','-c:v','libx264','-preset','slow','-crf','18','-pix_fmt','yuv420p','-threads','6','-c:a','aac','-b:a','256k','-movflags','+faststart',str(promo)],check=True)
for p in [clean,promo]:
    subprocess.run([str(ff),'-v','error','-nostdin','-i',str(p),'-f','null','-'],check=True)
report={'duration_seconds':60,'fps':24,'resolution':[1920,1080],'frame_count':1440,'render_success':True,'decoded_without_errors':True,'visual_source':'Current UE campus with cinematic cameras; not uninterrupted first-person gameplay.','audio':'Original ambient score mixed with project-synthesized air ambience.','files':[{'path':str(p),'bytes':p.stat().st_size,'sha256':digest(p)} for p in [promo,clean]],'user_review_pending':True}
(media/'delivery-manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)
