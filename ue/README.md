# 温州中学 UE 5.8 工作区

本目录是 UE 接入阶段的起点，基于 Blender v0.0.43。当前完成 MCP 连通和临时对象读写验证，尚未导入校园资产。

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

## 下一步

先就南门示范区与用户确认画面和漫游思路，再导入南区、核对坐标单位、重建材质、配置碰撞和行走/航拍控制。本次接入验证不代表上述制作已完成。
