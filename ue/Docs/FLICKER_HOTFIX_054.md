# 0.1.0-test.54 — 静止闪烁快速修复

针对步青广场地面以及部分建筑阴影的静止闪烁反馈，本次只修改两项。

- 步青广场连续铺装与教学楼底板、图书馆外铺装存在同高重叠；通道与北侧出口也有同高重叠。三个完整铺装体分别下移 2 厘米、上移 1 厘米、上移 2 厘米，消除已定位的共面区域。两个现有网格共修改 24 个顶点，三角形连接不变，未简化建筑。
- 旧运行日志曾报告 VSM One Pass Projection max lights overflow。将 `r.Shadow.Virtual.OnePassProjection.MaxLightsPerPixel` 从 16 提高到官方支持的 32，保留现有灯光和阴影。此设置增加瞬时显存开销，尚未做长时间性能回归。

验证：UE 运行时设置读回为 32；真实角色完成广场北向通道、图书馆门廊、西侧入口三条往返路线。步青广场正面和图书馆前方各采集两张不同时间的原始运行画面，抽查没有明显表面交替现象。该抽查不等于全校园连续视频验收，也不能证明用户未指明的建筑闪烁全部消失。

证据：`buqing_surface_separation_applied.json`、`flicker_shadow_capacity.json`、`tour_flicker_routes_runtime.json` 和 `screenshots/flicker54_*.png`。新的独立程序供用户重点复查步青广场及原先闪烁的建筑。旧版 0.1.0-test.51d 保留。
