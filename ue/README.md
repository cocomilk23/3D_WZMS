# 温州中学 UE 5.8 工作区

本目录是基于 Blender v0.0.43 的 UE 5.8 南区示范工程（v0.0.44-ue-south）。南门、广场、四片网球场和邻近岸线已导入，基础运行检查通过，并非全校 UE 成品。

- 工作区：`E:/WZMS_UE`，与 `E:/3D_WZMS` 共用同一个 Git 仓库对象库，分支为 `codex/ue-integration`。
- 工程：`ue/WZMS/WZMS.uproject`。
- 启动：PowerShell 执行 `ue/Automation/Start-WZMS.ps1`。仅启动本项目，MCP 端口为 8010。
- MCP：`http://127.0.0.1:8010/mcp`，仅监听本机。使用引擎已有的 `ModelContextProtocol`、`EditorToolset` 等插件。FootballGolf 项目的 8000 端口与配置保持原样。
- Codex 工作区配置：`.codex/config.toml`。若当前会话尚未重新发现工具，可直接通过 `ue/Automation/ue_mcp.py` 调用同一个 MCP 服务；本次验证使用此方式。
- 主要缓存：`E:/WZMS_UE_Cache/DDC`，Zen 数据实际位于其 `Zen` 子目录。临时文件：`E:/WZMS_UE_Cache/Temp`。UE 自身少量安装元数据仍由引擎管理。
- Saved、Intermediate、DerivedDataCache、Binaries 均不提交；uasset/umap 已由既有 Git LFS 规则覆盖。
- 大型 Blender 历史文件未重复检出到新工作区；原交接包仍在 `E:/3D_WZMS/deliverables/v0.0.43/ue/`。

## 验证

`D:/python/python.exe ue/Automation/check_mcp.py`：在空的 Entry 关卡创建唯一命名的临时对象，读取并核对坐标，再删除并确认消失。不保存引擎关卡。实际记录在 `ue/Reports/mcp_connection.json`；在正式制作关卡打开后，此检查会拒绝修改场景。

客户端复用自本机 FootballGolf 项目已经跑通的 `Automation/ue_mcp.py`，仅将端口和客户端标识改为本项目专用值。已完成 initialize、工具发现和 tools/call，当前发现 20 个工具组。

## 南区制作状态

- 54 个分块、13,424 个源对象已导入，坐标和有效几何边界验证通过。UE 世界坐标厘米 = Blender `(X, -Y, Z) * 100`；该版本以 Actor 的 100 倍缩放完成单位转换。
- 152 个材质实例已绑定，颜色沿源材质节点连接读取。UE 材质重新构建，不保证与 Blender 程序材质逐像素一致。
- 实体分块使用源几何作为静态碰撞；植被、水和玻璃未设置阻挡。实际路线验收结果以检查报告为准。
- 默认地图：`/Game/WZMS/Maps/L_WZMS_South`。行走与航拍蓝图已编译；人物在实际 PIE 中前进约 8 米并保持地面碰撞，Tab 切换飞行、R 回南门已通过实际按键测试。
- 42 个植被分块使用 Nanite 并保持远处叶片覆盖面积；10 个实体分块使用完整网格显示，以保留相距很近的标线和铺装层。玻璃和水保持独立透明材质。
- DX12/SM6、Lumen、虚拟阴影、固定 EV13 日光。四张 1600×900 的 UE 实际渲染图位于 `ue/Reviews/South`。
- 最终配置在南门附近固定视角的 12 秒 PIE 采样：716 帧，平均约 59.6 FPS，帧耗时中位数 16.7 ms。显示窗口约 1355×539；这不是 1080p/4K 或整校性能承诺。完整采样和限制见 `ue/Reports/south_performance.json`。
- 工程、UE 缓存均在 E 盘。原 Blender 冻结版本和交接包保留在 `E:/3D_WZMS`。

## 操作

打开工程后点击 Play。WASD 移动，鼠标转向，Shift 加速，空格跳跃，Tab 切换航拍与返回上次步行位置，航拍时 Q/E 降低/升高，R 回南门，Esc 结束编辑器内运行。Shift+F1 释放鼠标供编辑器操作。

地图边缘可见尚未迁入区域的断面，部分背景构件跨区，完整校园需要后续分区接入。尺寸仍按用户接受的估算方案，材质为 UE 重建版本。该批没有 Windows 独立可执行程序，需要 UE 5.8 编辑器打开验收。

## 制作与验证记录

源 FBX 来自 `E:/3D_WZMS/builds/v043_ue_bundle`。首次重建顺序：`import_south.py` → `build_south_materials.py` → `improve_south_nanite.py` → `preserve_solid_surface_detail.py` → `prepare_explorer_blueprint.py` → `build_explorer_gameplay.py` → `light_south.py`。不要对已完成的分块重复导入。材质使用组件覆盖绑定，避免修改每个网格材质槽引起大量重复构建。

`south_import.json` 记录有效几何边界、坐标和导入三角形数量；零面积源面被 UE 清除，不计为可见几何缺失。`south_delivery_validation.json` 复核最终网格、位置和材质绑定；`explorer_runtime.json`、`keyboard_flight.json`、`keyboard_return.json` 记录运行检查。初期调试日志、错误截图与缓存位于忽略的 Saved 目录，不作为最终验收图。

制作脚本通过本项目的 MCP 工具组 `wzms_editor_bridge.WZMSProjectTools` 执行，运行记录位于不提交的 `Saved/AutomationJobs`。源码和结果报告位于 `ue/Automation` 与 `ue/Reports`。
