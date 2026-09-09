"""Local, provisional sung-word timestamps, never used as public lyric captions."""
import os,sys,json
from pathlib import Path
os.environ['HF_HOME']='E:/WZMS_UE_Cache/AudioModels'
os.environ['HF_HUB_DISABLE_XET']='1'
sys.path.insert(0,'E:/WZMS_UE_Cache/AudioAnalysis')
from faster_whisper import WhisperModel
model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=6,download_root='E:/WZMS_UE_Cache/AudioModels')
segments,info=model.transcribe('E:/校歌.mp3',language='zh',beam_size=5,word_timestamps=True,vad_filter=False,condition_on_previous_text=False)
rows=[]
for s in segments:
 row={'start':s.start,'end':s.end,'text':s.text,'words':[{'start':w.start,'end':w.end,'word':w.word,'probability':w.probability} for w in s.words]}
 rows.append(row);print(json.dumps(row,ensure_ascii=False),flush=True)
p=Path('E:/WZMS_Media/demo058/provisional_music_transcription.json')
p.write_text(json.dumps({'warning':'Unverified automatic transcription of singing; editorial timing aid only, not public captions or authoritative lyrics.','segments':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
