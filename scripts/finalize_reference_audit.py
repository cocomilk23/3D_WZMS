from pathlib import Path
from datetime import datetime,timezone
import csv,json,shutil
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'reference/reports'
inv=json.loads((REPORT/'inventory.json').read_text(encoding='utf8'))
v=json.loads((REPORT/'panorama_verification.json').read_text(encoding='utf8'))
byid={s['scene_id']:s for s in v['scenes']}
ok=set(s['scene_id'] for s in v['scenes'] if s['complete'])
expected=set(s['scene_id'] for s in inv['scenes'])
if ok!=expected or v['summary']['errors']:
    raise SystemExit(f'Cannot pass image gate: complete={len(ok)}, expected={len(expected)}')
now=datetime.now(timezone.utc).isoformat()
initial=REPORT/'素材验收报告_首次访问记录.md'
if not initial.exists():shutil.copy2(REPORT/'素材验收报告.md',initial)
inv['summary'].update(audited_at=now,complete_panoramas=len(ok),decoded_tiles=v['summary']['decoded_tiles'],
    image_access_gate='PASSED',asset_gate='IMAGE_ACCESS_PASSED_GEOMETRY_UNCALIBRATED',
    reason='All 95 advertised highest-resolution cubemaps are downloaded and decoded; measured geometry and coverage of unphotographed areas remain unverified.')
inv['summary']['scene_navigation_hotspots']=249
inv['summary']['text_hotspots']=5
source=json.loads((ROOT/'reference/source/tour.json').read_text(encoding='utf-8-sig'))
text_hotspots=[{'scene_id':s['id'],'scene_name':s['name'],'title':h['title'],'text':h['data']} for s in source['product']['config']['scenes'] for h in s.get('hotspot',[]) if str(h.get('type'))=='4']
(REPORT/'文字说明热点.json').write_text(json.dumps(text_hotspots,ensure_ascii=False,indent=2),encoding='utf8')
for s in inv['scenes']:
    p=byid[s['scene_id']]
    s.update(image_status='full_resolution_decoded',complete_panorama=True,
             local_faces=f"reference/panoramas/faces/{s['scene_id']}",zip_sha256=p['zip_sha256'])
inv['source_notes'].append('2026-09-05: Dedicated Playwright browser connection succeeded via ordinary page fetch; earlier direct HTTP and in-app browser export failures are superseded for image access.')
(REPORT/'inventory.json').write_text(json.dumps(inv,ensure_ascii=False,indent=2),encoding='utf8')
fields=['scene_id','category','name','scene_url','max_cube_face_pixels','image_status','complete_panorama','dimension_calibrated','hotspot_count','local_faces','zip_sha256']
with (REPORT/'scene_inventory.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fields,extrasaction='ignore');w.writeheader();w.writerows(inv['scenes'])
size=v['summary']['zip_bytes']/1024**3
lines=['# 温州中学3D复刻：全景素材读取验收','',f'完成时间：{now}','',
       '**全景图片读取验收：通过。95/95个点位的最高分辨率全景已保存到本地。**','',
       '**三维尺寸校准：尚未完成。图片读取通过不代表未拍摄区域已覆盖，也不代表具备严格1:1测量依据。**','',
       '## 核验结果','',
       '| 项目 | 结果 |','|---|---|',
       '| 分类与点位 | 15个分类、95个点位 |',
       '| 热点 | 249个场景跳转（目标全部有效）及5个文字说明 |',
       f"| 最高分辨率原始切片 | {v['summary']['decoded_tiles']:,}张，全部通过ZIP CRC读取和JPEG完整解码 |",
       '| 完整立方体全景 | 95组，共570面 |',
       '| 航拍图片分辨率 | 2个点位，每面5760 × 5760像素 |',
       '| 其他点位分辨率 | 93个点位，每面4352 × 4352像素 |',
       '| 缺片 / 解码错误 | 0 / 0 |',
       f'| 原始切片包体积 | {size:.2f} GiB（不含派生预览和拼接面） |',
       '| 来源与完整性记录 | 保留逐片来源URL、SHA-256、包校验值、点位对应关系 |','',
       '## 获取方式与先前问题','',
       '直接HTTP访问和初次内置浏览器导出失败后，改用正常加载校园网站的专用浏览器连接。经页面正常fetch读取公开图片资源，在浏览器内打包并通过下载保存；未更改网站防护、账户权限或浏览器安全设置。',
       '本次结果替代首次“0/95”的图片读取结论；首次访问失败记录单独保留。','',
       '## 本地文件','',
       '- [素材浏览器](../素材浏览.html)：按名称搜索，逐方向打开高清图片。',
       '- `../panoramas/tiles/`：95份原始切片ZIP包，保留服务器返回的原始JPEG字节。',
       '- `../panoramas/faces/`：570张拼接面、95张六面预览、逐点核验记录。',
       '- `../panoramas/qa/`：批量目视检查用的预览图。',
       '- `panorama_verification.json`：完整解码、尺寸与文件哈希记录。','',
       '拼接面是质量96、无色度降采样的JPEG派生参考图；需要原始像素时以ZIP中的原始切片为准。方向F/B/L/R/U/D是全景立方体面标签，不是地理方位。','',
       '## 建模前仍需处理的内容','',
       '- 实际比例与标高：全景没有可靠的绝对坐标、测距和建筑尺寸，下一步建立尺度依据与误差记录。',
       '- 覆盖范围：按建筑检查背面、屋顶、遮挡、未拍摄室内；没有证据的部分单独标注。',
       '- 细节辨识度：原始照片自身可能存在模糊、曝光、拼接或年代差异；文件像素完整不等于每个细节都清晰。',
       '- 建模运行环境：Blender/UE连接问题与本次图片读取验收分开处理。','',
       '## 逐点结果','',
       '| ID | 分类 | 场景 | 每面边长 | 切片数 | 读取结果 |','|---|---|---|---:|---:|---|']
for s in inv['scenes']:
    p=byid[s['scene_id']]
    lines.append(f"| {s['scene_id']} | {s['category']} | {s['name']} | {p['face_size']} | {p['decoded_tiles']} | 完整解码 |")
(REPORT/'素材验收报告.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
# Project README is maintained separately; audits must not overwrite project status.
print(json.dumps({'image_gate':'PASSED','scenes':len(ok),'tiles':v['summary']['decoded_tiles'],'original_gib':size},ensure_ascii=False))
