"""Measure user-supplied anthem without altering its tempo or uploading its audio."""
import json,hashlib,subprocess
from pathlib import Path
import numpy as np
import librosa
from PIL import Image,ImageDraw
ue=Path(__file__).resolve().parents[1]
media=Path('E:/WZMS_Media/demo058');media.mkdir(parents=True,exist_ok=True)
source=Path('E:/校歌.mp3')
ff='D:/python/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
raw=subprocess.check_output([ff,'-v','error','-i',str(source),'-f','f32le','-ar','22050','-ac','1','-'])
y=np.frombuffer(raw,dtype='<f4');sr=22050;hop=256
onset=librosa.onset.onset_strength(y=y,sr=sr,hop_length=hop)
tempo,beatframes=librosa.beat.beat_track(onset_envelope=onset,sr=sr,hop_length=hop,trim=False)
beats=librosa.frames_to_time(beatframes,sr=sr,hop_length=hop)
rms=librosa.feature.rms(y=y,frame_length=2048,hop_length=hop)[0]
times=librosa.frames_to_time(np.arange(len(rms)),sr=sr,hop_length=hop)
from scipy.signal import find_peaks
smooth=np.convolve(rms,np.ones(43)/43,'same')
quiet,_=find_peaks(-smooth,distance=int(2.0*sr/hop),prominence=.008)
result={'source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'duration_seconds':len(y)/sr,'estimated_bpm':float(np.asarray(tempo).reshape(-1)[0]),'beats_seconds':beats.tolist(),'phrase_gap_candidates_seconds':times[quiet].tolist(),'method':'Local spectral onset / beat tracking and 0.5-second smoothed energy minima; candidates are editorial guides, not verified lyric boundaries.','tempo_preserved':True}
(ue/'Reports/demo058_music_analysis.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
im=Image.new('RGB',(1800,520),'#101c25');d=ImageDraw.Draw(im)
for t,v in zip(times,smooth):
 x=round(70+t/(len(y)/sr)*1660);h=round(v/max(smooth)*340)
 d.line((x,430-h,x,430),fill='#81b9b3')
for t in times[quiet]:
 x=round(70+t/(len(y)/sr)*1660);d.line((x,55,x,445),fill='#cca266');d.text((x-8,35),f'{t:.1f}',fill='white')
for t in range(0,80,5):
 x=round(70+t/(len(y)/sr)*1660);d.text((x,460),str(t),fill='white')
d.text((70,495),f'Anthem duration {len(y)/sr:.3f}s | onset tempo estimate {result["estimated_bpm"]:.2f} BPM | vertical markers: energy minima',fill='white')
im.save(media/'music_structure.png')
print(json.dumps(result,ensure_ascii=False),flush=True)
