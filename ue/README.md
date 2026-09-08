# 温州中学 UE 5.8 整校工程

Blender v0.0.43 中已有的本部模型已全部迁入同一张 UE 校园地图，包括建筑、道路、运动场、绿化、水面和已经制作的室内空间。新疆部继续暂缓，尺寸沿用用户认可的估算方案。

## 打开与操作

- 工程：E:/WZMS_UE/ue/WZMS/WZMS.uproject。
- 整校地图：/Game/WZMS/Maps/L_WZMS_Campus，已设为默认启动地图。
- 已验收的南区独立地图仍保留：/Game/WZMS/Maps/L_WZMS_South。
- 启动入口：ue/Automation/Start-WZMS.ps1。使用 UE 5.8、DX12/SM6。
- 点击 Play 开始。WASD 移动，鼠标转向，Shift 加速，空格跳跃；Tab 切换航拍并返回上次步行位置，航拍时 Q/E 降低/升高；R 返回南门；Esc 结束运行，Shift+F1 释放鼠标。

当前交付为可在 UE 编辑器运行的工程，未打包独立 Windows 程序。首次加载需要等待着色器和资源缓存，之后使用 E 盘缓存。

## 迁入内容

| 分区 | 分块数 | 源对象数 |
|---|---:|---:|
| 南区 | 54 | 13,424 |
| 中央区 | 48 | 11,484 |
| 西区 | 42 | 8,039 |
| 东区 | 68 | 12,912 |
| 北区 | 37 | 11,358 |
| 合计 | 249 | 57,217 |

484 个源材质对应的实例和 24 张原始照片纹理已接入。UE 中重建了源颜色、粗糙度、金属度、透明和发光效果；程序材质不是 Blender 着色器的逐像素复制。体育馆等薄屋面补上了内侧显示。

现有图书馆、数学馆、校史馆、体育馆、食堂和校友展厅等室内内容随模型迁入。128 盏局部灯光保留源位置，光通量按 UE 调整；7 处室内曝光区域处理室内外亮度过渡。没有新增参考资料未覆盖的整栋建筑内部。

UE 坐标厘米 = Blender (X, -Y, Z) * 100。FBX 局部顶点保留米数值，通过 Actor 的 100 倍缩放转换。实体分块保留完整可见几何与精确静态碰撞；植被使用 Nanite，保留源细节和叶片覆盖面积；玻璃、水和植被不阻挡人物。当前没有 AI 寻路需求，因此关闭额外的导航网格生成。

为适配本机 6GB 显存，植被在保留完整 Nanite 主几何的前提下压缩非 Nanite 备用网格；重建统计有变化的少数分块保留完整备用网格。实体建筑与碰撞几何不减面，原始 Blender 和 FBX 不修改。当前画质验收针对 DX12/SM6 的 Nanite 路径；如果将来需要非 Nanite 平台或硬件光追，应从源资产重建完整备用网格。其中 185 块压缩备用网格，4 块保留完整备用网格；全部 189 块合计 26,024,846 个 Nanite 主三角形保持不变。RHI 顶点/索引缓冲从约 3,015MiB 降至 630MiB，这不是整张显卡的总占用。具体分块比例和前后三角形数见 campus_foliage_fallback.json。

## 验证与预览

- ue/Reports/campus_delivery_validation.json：249 个分块的位置、几何、材质与碰撞配置复核。
- ue/Reports/campus_route_collision.json：74 条源参考路线、2,572 个地面采样点全部有对应碰撞地面。这是地面采样，不等于所有路线的完整人物通行证明。
- ue/Reports/campus_runtime.json：人物实际走过 10 处代表性通道，覆盖入口、展厅、楼层和食堂，验证行走、楼梯高度、飞行切换与返回。
- ue/Reviews/Campus：UE 实际渲染的整校、广场、运动场及馆内检查图。高分辨率单帧截图仍可能有细线锯齿和间接光噪点，实时稳定画面以编辑器 Play 为准。
- ue/Reports/campus_performance.json 与原始 CSV：整校加载后的地面、航拍、室内三种视角采样。只说明报告记录的设备、窗口和设置，不代表所有分辨率或独立程序性能。

本机 RTX 3060 Laptop 6GB，在最大化编辑器内约 1355×850 的可见游戏区域、60FPS 上限下，地面/航拍/室内各采样 12 秒的平均帧率为 59.6 / 59.8 / 60.0FPS，采样中的显存本地占用约 4.5–4.7GB。它是三个固定视角的短时结果，首次加载和长距离连续移动仍可能出现资源加载波动。

这次交付的“完整”指 v043 中已有本部模型的完整迁移。真实校园未建模的部分、实测尺寸和进一步美术打磨仍是后续工作。

## 存储与 Git

UE 工作区在 E:/WZMS_UE，分支 codex/ue-integration；Blender 源工作区仍为 E:/3D_WZMS。两者共用仓库对象库，不重复检出大型 Blender 历史文件。中央、西、东、北区各有独立提交，最终验收配置另作收尾提交。

缓存使用 E:/WZMS_UE_Cache/DDC，Zen 位于其 Zen 子目录，临时文件在 E:/WZMS_UE_Cache/Temp。Saved、Intermediate、Binaries 不提交，UE 模型和地图由 Git LFS 管理。

## 重建与自动化

源包为 E:/3D_WZMS/builds/v043_ue_bundle。audit_campus_fbx.py 核对 FBX 哈希、非零面积三角形和有效边界；UE 清理零面积面不视作可见几何丢失。

新分块通过 run_campus_zone.py 在 L_WZMS_Transfer 空关卡逐块构建、校验和保存；达到内存阈值会先保存再重启本项目编辑器。assemble_campus_checkpoint.py 将完成的分区合入整校地图并复核。L_WZMS_Transfer 仅供编辑器构建中转。

本项目使用 UE 自带 MCP，地址 http://127.0.0.1:8010/mcp。ue/Automation/ue_mcp.py 调用官方服务，wzms_editor_bridge.WZMSProjectTools.run_script 执行项目目录内的制作脚本；任务结果在忽略的 Saved/AutomationJobs 中。不要在上一个编辑器任务仍运行时并发修改地图。
