"""Anthem-led exterior edit from the accepted final.57 campus, camera-only changes."""
import json,copy
from pathlib import Path
ue=Path(__file__).resolve().parents[1]
old=json.loads((ue/'SourceReference/demo_shots_056.json').read_text(encoding='utf8'))
by={s['id']:s for s in old['shots']}
shots=[]
def reuse(oldid,newid,title,purpose):
 s=copy.deepcopy(by[oldid]);s.update(id=newid,title=title,purpose=purpose);shots.append(s);return s
reuse('01_gate_arc','01_gate','南大门','以校名墙确立身份，侧移抬升，邀请观众入校。')
reuse('02_plaza_rise','02_arrival','南大门广场','从入口走向校园，以广场与德涵楼展开空间。')
shots.append(dict(id='03_crest',title='步青广场',purpose='由校徽特写后拉，展开广场与教学楼前沿，保持文字朝向稳定。',start=[54,133,30],control=[54,125,42],end=[54,116,55],target_start=[54,157,0],target_end=[54,162,1],fov=58))
s=reuse('04_library_orbit','04_library','图书馆','以建筑正立面与入口表达求学主题。');s.update(start=[102,99,16],control=[127,96,18],end=[151,104,19],target_start=[126,155,8],target_end=[126,155,8],fov=62)
shots.append(dict(id='05_teaching',title='教学楼',purpose='以步青广场后方教学楼为主景，缓慢侧向揭示层次。',start=[81,106,31],control=[56,105,33],end=[26,113,32],target_start=[54,194,14],target_end=[54,194,14],fov=60))
reuse('03_lotus_sweep','06_lotus','荷塘 · 网球场','以荷塘、网球场和教学楼形成前中后景关系。')
s=reuse('06_basketball','07_basketball','篮球场','展示八片球场与红色间隔，顺着场地长边环绕。');s.update(start=[65,245,44],control=[70,272,48],end=[55,300,52],target_start=[14.5,267,0],target_end=[14.5,280,0])
shots.append(dict(id='08_goal',title='操场 · 足球场',purpose='以十一人制球门为视觉锚点，沿底线外侧横移，不穿越球网。',start=[-101,212,2.8],control=[-91,215,3.4],end=[-80,217,5],target_start=[-85,228,1.25],target_end=[-85,231,1.6],fov=61))
s=reuse('07_track_low','09_track','操场 · 跑道','沿跑道方向掠过，呼应音乐增强段落。');s.update(start=[-38,247,3],control=[-34,272,5],end=[-43,300,9])
s=reuse('08_track_orbit','10_stadium','操场全景','升至高处，完整交代跑道、绿茵场与体育馆。');s.update(start=[-178,210,86],control=[-145,190,96],end=[-92,190,110])
shots.append(dict(id='11_water',title='校园水岸',purpose='以岛屿建筑、桥与水岸为主体，收束运动段落，过渡到校园全景。',start=[216,169,39],control=[220,162,43],end=[228,156,47],target_start=[275,143,3],target_end=[275,146,3],fov=66))
s=reuse('09_campus_reveal','12_campus','温州中学', '完整校园缓慢后拉升空，保留终止和弦与片尾呼吸。');s.update(start=[-164,67,170],control=[-237,29,235],end=[-240,-55,280],fov=67)
# Cut on measured beats adjacent to major energy/phrase changes. 24 fps quantization.
boundaries=[0,9.91492063,15.95210884,22.95833333,27.36471655,32.75174603,39.35782313,44.15274376,48.36716553,53.75419501,59.95833333,65.75891156,78.54166667]
frames=[round(t*24) for t in boundaries]
for i,s in enumerate(shots):s.update(seconds=(frames[i+1]-frames[i])/24,start_frame=frames[i],end_frame=frames[i+1])
plan={'version':'demo-058-anthem','source_game_version':'0.1.0-final.57','fps':24,'resolution':[1920,1080],'ease_strength':.28,'duration_seconds':frames[-1]/24,'music':'User supplied E:/校歌.mp3; complete performance, original tempo.','shots':shots}
(ue/'SourceReference/demo_shots_058.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(ue/'WZMS/Saved/Logs/demo_build_request.json').write_text(json.dumps({'plan':'demo_shots_058.json','prefix':'LS_Demo058','revision':'r03','report':'demo_sequences_058.json','source':'Accepted final.57 campus; anthem film, final framing.','preview_shots':['03_crest']}))
print('Prepared',len(shots),'shots;',frames[-1],'frames;',frames[-1]/24,'seconds')
