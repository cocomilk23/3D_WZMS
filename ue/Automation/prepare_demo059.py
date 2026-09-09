"""User revision: one stadium shot, Taohua, wide Buqing, clean-only delivery."""
import json,os,shutil
from pathlib import Path
u=Path(__file__).resolve().parents[1];base=Path('E:/WZMS_Media/demo058');m=Path('E:/WZMS_Media/demo059');m.mkdir(exist_ok=True)
p=json.loads((u/'SourceReference/demo_shots_058.json').read_text(encoding='utf8'))
p.update(version='demo-059-anthem-clean-revision',delivery='Clean only; complete anthem retained',user_review_policy='Deliver directly for user review; no additional agent visual/decode QA requested.')
by={s['id']:s for s in p['shots']}
by['02_arrival'].update(start=[-8,-13,12],control=[-5,5,22],purpose='升空展开南大门广场与德涵楼，飞行线高于近处树冠。')
by['03_crest'].update(id='03_buqing_wide',title='步青广场与教学楼',purpose='宽景横向弧线同时展现广场、教学楼与两侧建筑，校徽仅是整体的一部分。',start=[8,83,60],control=[52,74,70],end=[102,88,72],target_start=[54,173,9],target_end=[54,177,11],fov=72)
by['08_goal'].update(id='08_math',title='数学馆外景',purpose='以白墙门庭和院落为主体，从侧前上方展开建筑。',start=[178,100,18],control=[167,96,22],end=[152,99,24],target_start=[150,119,3],target_end=[150,122,4],fov=68)
by['09_track'].update(id='09_history',title='校史馆外景',purpose='围绕校史馆入口与两翼建筑，保持完整建筑主体。',start=[220,101,18],control=[221,118,21],end=[229,132,23],target_start=[258,129,5],target_end=[258,129,5],fov=64)
by['11_water'].update(id='11_taohua',title='桃花岛',purpose='以桃花岛彩色门廊、庭园、双亭与岛屿轮廓为明确主体。',start=[245,43,31],control=[252,65,37],end=[245,88,34],target_start=[211,76,1.5],target_end=[211,78,2],fov=68)
(u/'SourceReference/demo_shots_059.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(u/'WZMS/Saved/Logs/demo_build_request.json').write_text(json.dumps({'plan':'demo_shots_059.json','prefix':'LS_Demo059','revision':'r01','report':'demo_sequences_059.json','source':'Accepted final.57; user clean-only revised edit.','skip_preview':True}))
# Immutable shared unchanged images save E: disk space. Replacement files are unlinked first.
out=m/'frames-master';out.mkdir(exist_ok=True)
for src in sorted((base/'frames-master').glob('frame_*.png')):
 dst=out/src.name
 if not dst.exists():os.link(src,dst)
arrival=json.loads((u/'Reports/demo058_arrival_retake_render.json').read_text());assert arrival.get('complete') and arrival.get('success')
patches=sorted((base/'retake-arrival').glob('frame_*.png'));assert len(patches)==145
for i,src in enumerate(patches):
 dst=out/f'frame_{238+i:05}.png'
 if dst.exists():dst.unlink()
 os.link(src,dst)
shutil.copy2(base/'School_Anthem_Master.wav',m/'School_Anthem_Master.wav')
shutil.copy2(base/'audio_provenance.json',m/'audio_provenance.json')
(m/'Source').mkdir(exist_ok=True)
shutil.copy2(base/'Source/School_Anthem.mp3',m/'Source/School_Anthem.mp3')
print('Prepared revised camera plan and shared base frames; only changed shots need rendering',flush=True)
