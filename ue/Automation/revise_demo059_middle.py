"""Replace the repetitive 27s/33s shots without creating a new delivery folder."""
import json
from pathlib import Path
u=Path(__file__).resolve().parents[1]
path=u/'SourceReference/demo_shots_059.json'
p=json.loads(path.read_text(encoding='utf8'))
by={s['id']:s for s in p['shots']}
assert '05_teaching' in by and '06_lotus' in by,'Middle revision already applied'
by['05_teaching'].update(id='05_meihua',title='梅花岛艺术楼',purpose='独立展现艺术楼白色入口框架和弧形玻璃立面，轻抬升侧移交代完整建筑，区别于教学楼全景。',start=[280,90,14],control=[295,93,16],end=[315,99,17],target_start=[300,131,5],target_end=[300,131,5],fov=62)
by['06_lotus'].update(id='06_gym',title='体育馆外景',purpose='以体育馆入口、百叶立面和曲面屋顶为唯一主体，侧前方平缓掠行，自然衔接下一段篮球场。',start=[-115,349,26],control=[-98,344,29],end=[-77,344,31],target_start=[-76,399,8],target_end=[-76,399,8],fov=60)
p.update(edit_revision='r02',revision_note='Replace 27.375–39.375s only; same demo059 output path, music and all other shot timings unchanged.')
path.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(u/'WZMS/Saved/Logs/demo_build_request.json').write_text(json.dumps({'plan':path.name,'prefix':'LS_Demo059','revision':'r02','report':'demo_sequences_059.json','source':'Accepted final.57; demo059 same-file revision of 27s/33s shots.','skip_preview':True}))
print('Prepared Meihua and Gym replacement camera paths, frames 657–945.')
