# v0.0.47：路缘通行与封闭网格朝向修复

本次是制作中的工程存档，尚不是最终发布程序。校园位置、外观细节数量、Blender v043 与冻结导出保持不变。

## 问题与修复

74 条真实人物路线首轮完成 64 条，另 10 条被数厘米高的路缘卡住。物理扫测与源脚本检查发现，部分闭合道路条带的面朝向全部向内，人物碰到的是错误朝向的底面。图书馆及其他实体中也存在同类组件。

以 UE 自带立方体校准正面方向，检查全部 51 个当前校园实体网格；仅选择封闭、每条边恰有两个反向连接面的组件。对 32 个网格中的 783 个向内组件、90,116 个三角面反转朝向和法线。未合并顶点、移动位置、降低面数或删除细节；开放面和拓扑不一致组件不自动修改。

## 验证

- `Reports/tour_orientation_repair.json`：逐网格记录修改范围、位置哈希及前后面数。
- `Reports/tour_orientation_after.json`：重新读取实际保存后的 UE 网格；符合上述封闭条件的反向组件已清零。该检查不声称开放或不一致组件全部正确。
- `Reports/tour_orientation_routes_runtime.json`：10 条原失败路线全部通过，另通过图书馆直梯、两侧弧梯和体育馆楼梯，共 14 条真实人物路线。仅在每条路线起点定位，中途实际行走。
- `Reports/campus_delivery_validation.json`：249 个校园网格及已记录的图书馆修复副本通过数量、位置和材质检查。
- `Reviews/Tour/Orientation_Library_Second.png`、`Orientation_Library_Top.png`：修复后实际 UE 图书馆画面。截图仍有采样噪点，最终画面调优待完成。

`Reports/TourBaseline/tour_complete_routes_before_orientation.json` 保留完整首轮失败证据。修复后的全 74 条路线仍须在最终环境整合后重新检查，不能将这次 14 条通过等同于全地图最终验收。

## 后续

周边围合与湖岸视觉融合、最终照明与材质调优、地图和游览地点选择、存档与菜单、Windows 独立运行测试及发布包仍在目标范围内。

## 重现注意

`repair_tour_orientation.py` 的选择与哈希对应修改前网格；它不是可反复盲目执行的脚本。若从新导出重建，应先重新审计并生成对应选择。`analyze_tour_orientation.py --output Reports/tour_orientation_after.json` 可保留原修复依据并记录后验结果。
