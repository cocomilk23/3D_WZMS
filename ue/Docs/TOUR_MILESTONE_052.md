# Windows 用户验收包 0.1.0-test.51d

2026-09-09 已成功执行 Win64 Shipping 的完整 Cook、Stage、Package、Archive；AutomationTool 返回 0，资源包数 1292。本次成功构建耗时约 6 分 42 秒。

## 可追溯性

- 打包资产与配置的 Git 提交：78dd205f961a5c4122c04287decb5a1da235f60a。
- 标签：v0.1.0-test.51d，指向上述构建提交。
- 输出：E:/WZMS_ValidationBuilds/0.1.0-test.51d。
- 独立程序：Windows/WZMS.exe。完整 ZIP、源文件 SHA-256 清单、文件校验清单及压缩包校验值由交付脚本生成；构建后重新核对资产与配置哈希。
- 详细包体大小、ZIP 哈希与完整性结果见该目录的 delivery-manifest.json，以及工程 Reports/tour_test_delivery_052.json。

## 实际启动检查

通过 Windows 启动真实的独立程序，观察到中文校园地图、24 个地点列表、设置和校园背景。运行的是随包的 UnrealGame-Win64-Shipping.exe，未使用编辑器 PIE。

当时有 Windows 安全中心的 UnrealPak 联网提示覆盖在程序前方，因此没有继续操作系统权限或进行鼠标交互验收。用户已明确表示自行验证；本轮只声明打包完成及启动到地图画面，不声明完整体验验收通过。

## 打包修复

- 保留引擎预编译版本的默认插件组合，解决纯蓝图工程被判为需要 C++ 临时目标的问题。
- bUseZenStore=False：将烹饪输出直接写到 E 盘，解决打包阶段读取 Zen 操作日志失败的问题；保留 IoStore 压缩及原有渲染设置。
- 排除打包工具自动生成的 Android 文件服务配置，使用确定性配置值，避免构建改写源配置。
- 随包的微软运行库实际文件为 vc_redist.x64.exe，操作说明已按实际包体核对。

## 验收边界

这是用户验收测试版。室内局部偏绿、室内外曝光过渡、图书馆和体育馆性能、长时间稳定性仍需结合用户反馈完善；不标记最终质量目标完成。
