# v0.0.46：校园游览通行与照明阶段存档

这是一份继续制作中的 UE 工程存档，不是最终可发布程序。基线为 v0.0.45-ue-campus，Blender v043 和冻结导出保持原样。

## 本次变化

- 从原始地面、水域与桥面轮廓生成连续补地和水域阻挡。保留桃花岛下沉平台、桥梁和木栈道的高差与通路。修正新增网格正反面，补地在航拍中正常显示。
- 草叶所在网格分段关闭碰撞，保留草坪地面承托与所有可见草叶。
- 图书馆补外部楼梯前的地面；为中央直梯开出真实净空；保留二楼两侧转接走道，增加浅接梯与开口护栏，调整弧形楼梯外扶手的入口。改动存在 UE 专用网格副本中，原导入网格保留。
- 恢复 6 类原有灯罩的发光材质。图书馆最高开放楼层补 6 组灯具，并增加 4 处宽范围间接补光；上下层分别调整曝光，照明参数属于视觉估算。
- 保留 249 个校园源网格及其位置和材质；验证程序仅对明确记录的两个图书馆修改副本使用新三角面数量，其余仍按冻结导出严格验证。

## 当前证据与范围

- `Reports/tour_water_collision_audit.json`：2,784 个水域网格点、621 次岸边胶囊扫测通过；74 条原参考路线不落入水域阻挡。
- `Reports/tour_water_runtime.json`：12 个不同岸边的真实人物进入尝试均被阻挡，人物停留在地面。
- `Reports/tour_critical_traversal_validation.json`：15 条关键连续人物路线通过，含图书馆两侧弧形楼梯往返、内外直梯、体育馆楼梯、数学馆二楼、食堂、草坪、石桥与木栈道。
- `Reports/campus_delivery_validation.json`：249 个校园源网格及两个明确记录的 UE 修复副本通过检查。
- `Reports/tour_interior_lighting.json` 与 `Reviews/Tour/`：7 处已建开放室内的灯光清单与实际 UE 画面。高分辨率截图有单帧采样噪点，不代表最终输出品质验收。
- `Reports/TourBaseline/` 保存修复前失败与诊断记录，不应作为当前测试状态。

## 仍须完成

外围围合环境、湖面和补地的整体视觉融合；74 条路线的完整连续行走与开放区域补充检查；最终灯光、材质和稳定画面调优；小地图/全图、地点选择、安全位置存档、菜单；Windows 独立打包、程序内操作验收、性能测试与发布说明。不得将本次阶段通过等同于最终目标完成。

## 重建入口

地形来源与施工数据保存在 `SourceReference/`。离线地形规划脚本使用 Shapely 2.1.2，当前安装位置为 E:/WZMS_UE_Cache/Python。UE 修改通过本项目 `Automation/run_ue_scripts.py` 顺序执行；必须在停止 PIE 后改动资产。

顺序：`build_tour_terrain.py`、`fix_tour_grass_collision.py`、`fix_tour_stair_headroom.py`、`fix_tour_library_approach.py`、`fix_tour_library_landing.py`、`finish_tour_interior_lighting.py`、`tune_tour_library_light.py`。行走测试使用 `prepare_tour_traversal.py` 生成请求，再在 PIE 中运行 `test_tour_traversal.py`，等待报告 complete=true。
