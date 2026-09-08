# v0.0.41 网球场方向与航拍布局校正

根据用户新提供的地面全景和航拍，修正 v040 的网球场方向判断：四块场地同向排开，各场长边朝向教学楼，蓝色实体隔墙位于第二、第三块之间，并与场地长边平行。面对楼体站在第一组两场之间，隔墙在右手侧。

- [完整校园工程](../../models/campus/WZMS_Campus_v041.blend)
- [地面审查图](previews/183_Tennis_toward_school.png)
- [四场俯视图](previews/184_Tennis_four_top_plan.png)
- [南侧航拍关系图](previews/185_Tennis_aerial_relationships.png)
- 用户依据：[地面全景](reference/user_ground.png)、[航拍](reference/user_aerial.png)。原始全景点位 119232347、119232348、119232359。

## 本次修改

四场中心为 (74,8)、(92,8)、(110,8)、(128,8)，沿项目 X 轴排开；每场长边沿 Y 轴，球网横跨 X 轴。每场比赛区域仍为 23.77 × 10.97 米。隔墙中心为 (100.9,8)，长边沿 Y 轴，两端保留通行空间。

整体围合由 v040 的向荷屿伸长改为沿教学楼方向展开。荷屿恢复至 v035—v039 的位置，重新接回岛屿步道、北侧球场入口和水南路支路。v040 的门窗、家具、表面等整体精修保留；旧模型与旧交付文件不改写。

两张照片用于确认朝向、排列和相邻关系，不是测绘图。球场相对楼体的精确偏移、绿地与岸线轮廓仍沿用项目估算，地面审查图也不是对全景镜头的逐像素匹配。新疆部、网页和 UE 漫游不在本次修改范围。

## 核验

保存后重新打开工程，核对四场中心、实际世界坐标尺寸、球网方向、隔墙及八块篮球场。对照 v040 的网格、UV、材质槽、变换与可见性，只允许 `replacement_scope.json` 登记的网球场及相邻环境调整。整合检查 v017 起仍有效的步行路线；新增路线穿过两组球场中央通道，并绕行隔墙两端。

最终结果以同目录 `saved_layout_validation.json`、`preservation_validation.json`、`geometry_validation.json`、`south_gate_preservation_validation.json`、`render_validation.json` 和 `delivery_validation.json` 为准。三个视角均从保存后的工程渲染，人工审图后才封存交付。用户验收与 UE 实际行走验收仍待进行。
