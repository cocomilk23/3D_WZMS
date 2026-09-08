# v0.0.48：外围围合与连续湖面

本次为继续制作中的环境存档，尚未完成游览界面、最终画面与独立发布包。

## 环境变化

在已接受校园布局外增加约 1.3 公里围墙、外围道路、人行道、63 栋估算的远景住宅及 262 棵复用校园原树木的行道树。周边属于补充环境，不是实测邻近建筑；原校园建筑与通路位置不变。树木共享两个网格，叶片保持完整 Nanite 源面数，背景绿化不阻挡人物。

补上原地形到新增围墙之间的承重地面。墙体实际阻挡人物，已有水域禁入体继续封闭临水部分。外围道路在人为边界之外，仅作背景。

原有水面存在重叠透明层与材质色块接缝。使用原始水面轮廓的精确并集生成一个连续水面，保留 -1.15 米水位和桥梁、岛屿位置。采用统一的有轻微流动细纹的湖水材质；旧水面网格保留在工程中并隐藏，禁入碰撞独立保留。

## 验证范围

- `tour_perimeter_collision.json`：622 个边界位置，按站立和接近跳跃最高点的胶囊高度检查。完整落在禁入水域内部的扫测，通过实际物理射线确认所在封闭水域；其余由墙体或水域表面阻挡。74 条参考路线与新增围墙无冲突。
- `tour_perimeter_runtime.json`：6 处实际人物靠墙行走与跳跃，必须留在校园一侧并最终站立于地面。
- `tour_water_collision_audit.json`、`tour_water_runtime.json`：完整水域静态检查和 12 处实际人物禁入尝试。
- `campus_delivery_validation.json`：249 个源网格保留，已记录的图书馆修复副本按其专用记录验证。旧水面隐藏及新湖面替代关系在 `tour_water_surface.json` 单独记录。
- `Reviews/Tour/Campus_Aerial.png`、`Campus_North_Gate.png` 为本次真实 UE 画面，已核对外围位置、绿化与湖面接缝。画面最终调优和打包性能验收仍未完成。

新增周边建筑、围墙、树木尚须纳入后续整体性能测试；完整 74 条人物路线复测、可行走区域抽查、游览功能和最终独立版验收继续推进。

## 重建

离线：`plan_tour_perimeter.py` → `build_tour_perimeter_buffers.py`、`plan_tour_water_surface.py`、`plan_tour_context_planting.py`。树木数据由 `extract_tour_context_tree.py` 只读提取，未保存或修改 Blender 源文件。

停止 PIE 后：`build_tour_perimeter.py`、`build_tour_water_surface.py`、`build_tour_context_planting.py`。物理检查在编辑器中进行，真实人物测试在 PIE 中进行，并等待结果文件 `complete=true` 后再修改编辑器资产。
