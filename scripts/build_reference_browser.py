from pathlib import Path
import json, html
ROOT=Path(__file__).resolve().parents[1]
inv=json.loads((ROOT/'reference/reports/inventory.json').read_text(encoding='utf8'))
rows=[]
for s in inv['scenes']:
    sid=s['scene_id']
    v=ROOT/f'reference/panoramas/faces/{sid}/verification.json'
    if not v.exists() or not json.loads(v.read_text(encoding='utf8')).get('complete'): continue
    links=' '.join(f'<a href="panoramas/faces/{sid}/{f}.jpg" target="_blank">{label}</a>' for f,label in zip('fblrud',['前面 F','后面 B','左面 L','右面 R','上面 U','下面 D']))
    title=html.escape(f"{s['category']} · {s['name']} · {sid}")
    rows.append(f'<article data-text="{title}"><h2>{title}</h2><p>{s["max_cube_face_pixels"]} × {s["max_cube_face_pixels"]} 像素 / 面 · 原始切片已完整解码</p><a href="panoramas/faces/{sid}/f.jpg" target="_blank"><img loading="lazy" src="panoramas/faces/{sid}/preview.jpg" alt="{title} 六面预览"></a><nav>{links} <a href="panoramas/tiles/{sid}.zip">原始切片包</a></nav></article>')

page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>温州中学 · 建模参考图库</title>
<style>*{box-sizing:border-box}body{margin:0;background:#f5f4ef;color:#20342f;font:16px/1.7 system-ui,"Microsoft YaHei",sans-serif}header{padding:40px 5vw 25px;border-bottom:1px solid #d0d8d1}h1{margin:0;font-size:30px}header p{max-width:900px;margin:12px 0}main{max-width:1600px;margin:auto;padding:24px}input{width:min(600px,100%);padding:12px 16px;font:inherit;border:1px solid #8e9f95;border-radius:6px;background:white}article{padding:24px 0;border-bottom:1px solid #ccd4ce}article h2{font-size:19px;margin:0}article p{font-size:14px;color:#617068;margin:4px 0 12px}img{display:block;width:100%;height:auto;border:1px solid #d1d8d3}nav{display:flex;gap:12px;flex-wrap:wrap;margin-top:12px}a{color:#186d50}nav a{background:#fff;border:1px solid #d1d8d3;padding:6px 14px;border-radius:4px;text-decoration:none}small{display:block;margin-top:15px;color:#617068}</style>
<header><h1>温州中学 · 建模参考图库</h1><p>已保存 <b>__COUNT__ / 95</b> 个完整全景。六面预览用于快速定位；点击下方方向入口打开该面的完整分辨率图片，再放大检查门窗、屋顶和材质。所有参考图片均在本地。</p><input id="search" placeholder="搜索：图书馆、数学馆、南大门、点位编号…"><small>F/B/L/R为全景立方体方向标签，不代表地理方位。展示图由原始切片拼接后保存；原始JPEG字节保留在切片包中。素材读取完整不等于空间覆盖完整或尺寸已校准。</small></header><main>__ROWS__</main>
<script>document.querySelector('#search').addEventListener('input',e=>{const q=e.target.value.trim().toLowerCase();document.querySelectorAll('article').forEach(x=>x.hidden=!x.dataset.text.toLowerCase().includes(q));});</script></html>'''
dest=ROOT/'reference/素材浏览.html'
dest.write_text(page.replace('__COUNT__',str(len(rows))).replace('__ROWS__','\n'.join(rows)),encoding='utf8')
print(f'Offline reference browser: {len(rows)} scenes')
