# v0.0.43 环境精修与 UE 导入准备

沿用用户接受的 v042 布局和估算尺寸，增加南侧环境细节，并为全校园准备可追溯的 UE 静态资产交接包。

[Blender 主工程](../../models/campus/WZMS_Campus_v043.blend) · [UE 导入说明](../../docs/UE导入准备_v043.md)

## 本版变化

- 13 棵南侧树木调整叶片大小分布，提高树冠覆盖和层次，保留原树干位置。
- 岸线增加 290 块带接缝和倒角的石材压顶、近水湿痕，补入 5 组排水格栅。
- 新增 232 丛折面草叶，复用 3 份草丛网格；树下增加稀疏落叶。
- 18 种草地、树皮材质补充颜色和表面细节。
- 原对象增加稳定的 UE 标识、区域和表面类别；原工程保持可编辑，建筑、门区、球场和桥梁布局延续 v042。

这些细节属于用户授权的估算设计，不是每块石材或每丛植物的精确实物对应。南门背面校歌墙原图和内容保留；没有扩大新疆部或未知室内范围。

## 验收视角

- [南侧航拍](previews/190_Environment_south_aerial.png)
- [南门园景](previews/191_Environment_gate_garden.png)
- [荷塘与岸线](previews/192_Environment_lotus_bank.png)
- [岸边近景](previews/193_Environment_bank_close.png)

模型重开检查、既有 74 条几何路线、球场布局和保留对象核验见同目录 JSON。四张审查图均从同一保存工程生成，1600×1000、Cycles 96 采样；视觉审查记录与交付封存报告记录实际结果。

## UE 交接

交接文件为 `ue/WZMS_UE_Transfer_v043.zip`，采用 Git LFS 管理。包含五个区域的全细节 FBX 分块、原照片、材质迁移清单、源对象对应关系及逐文件回读报告。照片按内容哈希命名，程序材质需要在 UE 中重建；交接 FBX 的基础材质不等同于 Blender 最终画质。未做几何减面，UE 碰撞、运行帧率和漫游打包仍待下一阶段实测。

重建模型和渲染：`python scripts/run_isolated_culture_delivery.py 43 --build`。生成并回读交接包：`python scripts/run_ue_transfer_v043.py`。完整报告见 `ue_transfer_validation.json`。
