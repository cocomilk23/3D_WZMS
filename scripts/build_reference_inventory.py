"""Audit advertised metadata and locally acquired files without claiming unseen images."""
from pathlib import Path
import csv, hashlib, json, re, shutil, xml.etree.ElementTree as ET
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC, REPORT = ROOT/'reference/source', ROOT/'reference/reports'
BASE = 'https://www.720yun.com/t/a3akiwphz2w'
data = json.loads((SRC/'tour.json').read_text(encoding='utf-8-sig'))
config = data['product']['config']
page = (SRC/'page.html').read_text(encoding='utf-8-sig')
xml_text = re.search(r'<krpano\b.*?</krpano>', page, re.S).group(0)
xml = ET.fromstring(xml_text)
(SRC/'tour.xml').write_text(xml_text, encoding='utf8')
scene_xml = {int(n.get('scene_id')): n for n in xml.findall('scene')}
by_id = {int(s['id']):s for s in config['scenes']}
by_pano = {str(s['panoId']):int(s['id']) for s in config['scenes']}
category_by_id = {str(c['id']):c for c in config['category']}
group_by_scene, groups = {}, []
for root in config['categoryRoot']:
    scenes = [s for child in root['children'] for s in category_by_id[str(child)]['scenes']]
    groups.append({'name':root['title'], 'scene_ids':[s['id'] for s in scenes]})
    for s in scenes:
        group_by_scene[s['id']] = root['title']

bundle_path = Path('C:/Users/63580/AppData/Local/Temp/browser-use/assets/445f38a2-ee51-44d0-9a98-4a9fad6e5601/manifest.json')
bundle = json.loads(bundle_path.read_text(encoding='utf8'))
shutil.copy2(bundle_path, REPORT/'browser_bundle_original.json')
validated = []
for a in bundle['assets']:
    p = Path(a['path'])
    entry = {'url':a['url'], 'name':a['name'], 'status':'invalid'}
    try:
        with Image.open(p) as im:
            im.verify()
        with Image.open(p) as im:
            im.load()
            entry['width'], entry['height'] = im.size
            entry['format'] = im.format
        dest = ROOT/'reference/images/119232347'/a['name']
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p,dest)
        entry.update(status='decoded', path=dest.relative_to(ROOT).as_posix(),
                     sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),bytes=dest.stat().st_size)
    except Exception as e:
        entry['error'] = str(e)
    validated.append(entry)

screenshot = Path('C:/Users/63580/AppData/Local/Temp/codex-clipboard-6557b38f-1721-4993-8385-1256cf304aa9.png')
with Image.open(screenshot) as im:
    im.verify()
shutil.copy2(screenshot,SRC/'user_aerial_screenshot.png')

edges, graph = [], defaultdict(list)
rows = []
for sid, s in by_id.items():
    n = scene_xml.get(sid)
    levels = [] if n is None else [dict(l.attrib, template=l.find('cube').get('url')) for l in n.findall('./image/level')]
    resolutions = [int(l['tiledimagewidth']) for l in levels]
    for h in s.get('hotspot',[]):
        target_data = h.get('data') or {}
        tid = None
        if str(h.get('type')) == '0':
            explicit = str(target_data.get('sceneId','')).removeprefix('s_')
            tid = int(explicit) if explicit.isdigit() and int(explicit) in by_id else by_pano.get(str(target_data.get('panoId','')))
            if tid is not None:
                graph[sid].append(tid)
        edges.append({'from':sid,'hotspot':h.get('title',''),'type':h.get('type'),
                      'to':tid,'raw_target':target_data,'ath':h.get('ath'),'atv':h.get('atv')})
    row = dict(scene_id=sid,pano_id=s['panoId'],category=group_by_scene.get(sid,''),name=s['name'],
               scene_url=f'{BASE}?scene_id={sid}',metadata_valid=n is not None,
               max_cube_face_pixels=max(resolutions,default=0),
               image_status='partial_tiles' if sid == 119232347 and validated else 'not_verified',
               complete_panorama=False,visually_reviewed=False,dimension_calibrated=False,
               hotspot_count=len(s.get('hotspot',[])),
               preview_template=n.find('preview').get('url') if n is not None else None,
               mobile_template=n.findall('./image/cube')[0].get('url') if n is not None and n.findall('./image/cube') else None,
               levels=levels)
    rows.append(row)

reachable, q = set(), deque([119232347])
while q:
    sid = q.popleft()
    if sid in reachable: continue
    reachable.add(sid)
    q.extend(graph[sid])
unresolved = [e for e in edges if str(e['type'])=='0' and e['to'] is None]
summary = dict(audited_at=datetime.now(timezone.utc).isoformat(),tour_url=BASE,
               groups=len(groups),scenes=len(rows),xml_scenes=len(scene_xml),
               configured_hotspots=len(edges),unresolved_scene_hotspots=len(unresolved),
               reachable_from_aerial=len(reachable),
               downloaded_tiles=len(validated),decoded_tiles=sum(a['status']=='decoded' for a in validated),
               browser_export_requested=len(bundle['assets'])+len(bundle['failures']),
               browser_export_failed=len(bundle['failures']),
               complete_panoramas=0,asset_gate='NOT_PASSED',
               reason='Full-resolution panoramas are not locally complete; absolute dimensions and unseen areas lack verified references.')
manifest = dict(summary=summary,groups=groups,scenes=rows,hotspots=edges,downloaded_images=validated,
                source_notes=['Resolution fields are advertised metadata, not proof of successfully retrieved image detail.',
                              'Hotspot angles are viewing directions, not surveyed coordinates.',
                              'The provided screenshot is an overview, not a full-resolution panorama.',
                              'Browser-loaded assets can differ from directly downloadable assets; no security restrictions were bypassed.'])
(REPORT/'inventory.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
fields = ['scene_id','category','name','scene_url','metadata_valid','max_cube_face_pixels','image_status','complete_panorama','visually_reviewed','dimension_calibrated','hotspot_count']
with (REPORT/'scene_inventory.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fields,extrasaction='ignore'); w.writeheader(); w.writerows(rows)

lines = ['# 温州中学3D复刻：素材验收记录','',f"核验时间：{summary['audited_at']}",'',
         '**验收结果：未通过。当前不具备完整高清全景的离线读取能力，不能声称全部素材可用。**','',
         '## 已确认','',f'- 15个分类、95个点位；JSON目录与XML场景逐项匹配：{len(scene_xml)}个。',
         f"- 已解析{len(edges)}个热点；场景跳转目标未解析数：{len(unresolved)}；从航拍沿已配置跳转可达{len(reachable)}个点位（其余仍可从分类目录进入）。",
         f"- 首个航拍资源导出：{summary['browser_export_requested']}个请求，{summary['decoded_tiles']}个图片文件通过解码，{summary['browser_export_failed']}个导出失败。",
         '- 完整全景：0/95。其余94个点位尚未完成图片访问测试，不能标作失败或成功。',
         '- 用户提供的航拍截图已保存并确认可解码。','',
         '## 当前障碍','',
         '- 直接请求公开播放器及图片样本返回HTTP 567和站点防护页面；浏览器资源导出也存在大量失败。',
         '- 没有CAD、带比例总平面图、标高或建筑尺寸资料；不能校准严格1:1。',
         '- 屋顶、背面、树木遮挡与未拍摄室内的覆盖程度，必须在全景可读后逐区核验。',
         '- Blender MCP连接此前测试未成功；UE MCP尚未提供。此项与素材是否完整分开处理。','',
         '## 素材准入条件','',
         '1. 95个点位均有可完整解码的全景原图或六面图；若使用切片，每个必要面和切片必须完整。',
         '2. 对95个点位制作参考视图并目视核对方向、接缝、清晰度、重复点及遮挡区域。',
         '3. 保存来源、点位对应关系、原始分辨率、文件校验值与失败清单。',
         '4. 为全校布局建立尺寸基准；缺少证据的几何单独记录，不能标为实测。','',
         '## 解除访问障碍所需输入','',
         '提供这套作品的原始全景图片目录或720云离线导出包（直接放入reference/incoming即可），或提供已连通且能正常展示全景的受支持浏览器访问。无需逐点截图。',
         '原始素材到位后先批量解码、核对95个点位及缺片，再重新出具验收结果。','',
         '## 分类清单','', '| 分类 | 点位数 |', '|---|---:|']
for g in groups:
    lines.append(f"| {g['name']} | {len(g['scene_ids'])} |")
lines += ['', '## 95个点位核验表','', '| 点位ID | 分类 | 场景 | 配置的最高立方体单面边长 | 图片状态 |', '|---|---|---|---:|---|']
for r in rows:
    status='部分切片已读取；不完整' if r['image_status']=='partial_tiles' else '尚未核验'
    lines.append(f"| {r['scene_id']} | {r['category']} | [{r['name']}]({r['scene_url']}) | {r['max_cube_face_pixels']} px | {status} |")
(REPORT/'素材验收报告.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
(ROOT/'reference/incoming').mkdir(exist_ok=True)
print(json.dumps(summary,ensure_ascii=False,indent=2))
