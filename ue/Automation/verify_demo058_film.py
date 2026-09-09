"""Validate two final MP4s and extract every shot for visual acceptance."""
import json,subprocess,re
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
u=Path(__file__).resolve().parents[1];m=Path('E:/WZMS_Media/demo058');ff='D:/python/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
p=json.loads((u/'SourceReference/demo_shots_058.json').read_text(encoding='utf8'));manifest=json.loads((m/'delivery-manifest.json').read_text(encoding='utf8'))
qa=m/'qa';qa.mkdir(exist_ok=True);results=[]
for name in ['Clean','Promo']:
 movie=m/f'WZMS_Anthem_{name}_1080p.mp4'
 run=subprocess.run([ff,'-hide_banner','-nostdin','-i',str(movie),'-vf','blackdetect=d=0.08:pix_th=0.06:pic_th=0.98','-progress','pipe:1','-f','null','-'],capture_output=True,text=True,encoding='utf8',errors='replace',check=True)
 (qa/f'{name.lower()}_decode.txt').write_text(run.stdout+'\n'+run.stderr,encoding='utf8')
 frame_counts=re.findall(r'^frame=(\d+)$',run.stdout,re.M);assert int(frame_counts[-1])==1885
 intervals=[{'start':float(a),'end':float(b)} for a,b in re.findall(r'black_start:([\d.]+) black_end:([\d.]+)',run.stderr)]
 assert not any(x['start']>1 and x['end']<76 for x in intervals),intervals
 assert '1920x1080' in run.stderr and '24 fps' in run.stderr
 h=subprocess.check_output([ff,'-v','error','-i',str(movie),'-map','0:a','-c','copy','-f','hash','-hash','sha256','-'],text=True).strip()
 results.append({'version':name,'decoded_frames':1885,'resolution':[1920,1080],'fps':24,'audio_packet_hash':h,'black_intervals':intervals})
assert results[0]['audio_packet_hash']==results[1]['audio_packet_hash'],'Music tracks differ'
fontlog=(m/'encode_promo.log').read_text(encoding='utf8');assert 'Glyph ' not in fontlog,'Font fallback needs review'
assert 'WZMSPromoSans-Bold' in fontlog
for i,s in enumerate(p['shots']):
 t=4.5 if i==0 else (74.2 if i==11 else s['start_frame']/24+min(2.3,s['seconds']/2))
 for name in ['Promo','Clean']:
  subprocess.run([ff,'-v','error','-nostdin','-y','-ss',str(t),'-i',str(m/f'WZMS_Anthem_{name}_1080p.mp4'),'-frames:v','1',str(qa/f'{i+1:02}_{name.lower()}.png')],check=True)
for name in ['promo','clean']:
 for page in range(2):
  sheet=Image.new('RGB',(1440,870),'#14212a');draw=ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
  for j in range(6):
   idx=page*6+j;im=Image.open(qa/f'{idx+1:02}_{name}.png');im.thumbnail((480,270));x=(j%3)*480;y=(j//3)*435
   # Taller rows leave room for editorial labels without reducing rendered image size further.
   sheet.paste(im,(x,y));draw.text((x+10,y+280),p['shots'][idx]['id'],font=font,fill='white')
  sheet=sheet.crop((0,0,1440,740));sheet.save(qa/f'{name}_sheet_{page+1}.jpg',quality=94)
result={'media':results,'audio_identical':True,'font_weight':700,'no_missing_glyphs':True,'visual_review_frames':24,'visual_review_status':'Contact sheets and full-size samples generated; reviewer must inspect before final delivery.','source_game':'0.1.0-final.57'}
(m/'qa_report.json').write_text(json.dumps(result,indent=2)+'\n');(u/'Reports/demo058_qa.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2),flush=True)
