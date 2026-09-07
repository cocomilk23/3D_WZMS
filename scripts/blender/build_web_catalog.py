"""Create web camera presets from the loaded v015 campus and existing review PNGs."""
import bpy,json,shutil
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
entries=[('campus','南侧整合 · 本轮四场景','62_'),('route','校园总览 · 南门至北门','43_'),
 ('tennis','网球场 · 双场与围网','48_'),('tennis_ground','网球场 · 场内视角','45_'),
 ('daosi','道司前路 · 林荫弯道','49_'),('daosi_bridge','道司前路 · 花桥','50_'),
 ('heyu','荷屿 · 榕树与步道','54_'),('heyu_aerial','荷屿 · 岛岸全貌','57_'),
 ('shuinan','水南路 · 回望荷屿','58_'),('shuinan_aerial','水南路 · 步桥全貌','61_'),
 ('front','南大门 · 正面','01_'),('oblique','南大门 · 斜侧','02_'),
 ('aerial','南大门 · 航拍','03_'),('detail','南大门 · 近景','04_'),
 ('plaza','南大门广场','08_'),('buildings','德涵楼与贯真楼','12_'),
 ('bridge','中山路 · 跨水桥','15_'),('buqing','步青广场','18_'),
 ('middle','中山路 · 中段','23_'),('north','中山路 · 北段','28_'),
 ('canteen','食堂外景','33_'),('northgate','北门','38_')]
presets={};dst=ROOT/'web-preview/assets/campus';dst.mkdir(parents=True,exist_ok=True)
for key,label,prefix in entries:
 camera=next(o for o in bpy.data.scenes['WZMS_Campus'].objects if o.type=='CAMERA' and o.name.startswith(prefix))
 forward=camera.rotation_euler.to_quaternion()@Vector((0,0,-1))
 distance=abs(camera.location.z/forward.z) if camera.location.z>25 and abs(forward.z)>.1 else 30
 target=camera.location+forward*distance
 image=next(ROOT.glob('deliverables/*/previews/'+camera.name+'.png'),None)
 if image is None:image=ROOT/'web-preview/assets'/(camera.name+'.png')
 assert image.is_file(),camera.name
 shutil.copy2(image,dst/image.name)
 presets[key]={'label':label,'position':[round(v,5) for v in (camera.location.x,camera.location.z,-camera.location.y)],
 'target':[round(v,5) for v in (target.x,target.z,-target.y)],'lens':camera.data.lens,'image':'campus/'+image.name}
(ROOT/'web-preview/views.js').write_text('export default '+json.dumps(presets,ensure_ascii=False,indent=2)+';\n',encoding='utf8')
print('WEB_CATALOG_READY',len(presets))
