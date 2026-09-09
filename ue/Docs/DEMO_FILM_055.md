# 温州中学 · 校园漫游 Demo

基于游戏 0.1.0-test.54 的校园场景制作，60 秒，1920×1080，24 fps。使用 UE Movie Render Queue 输出的真实场景画面；这是专门安排镜头的场景演示，不是玩家连续操作录像。

七组镜头：南大门慢推、荷塘水岸侧移、江口路向前漫步、步青广场推进、图书馆外景侧移、图书馆二楼空间、校园全景后退升空。每段镜头采用平滑加减速，隐藏游戏菜单和 HUD。两轮起点、中点、终点检查用于确认构图及避免明显遮挡；正式画面使用四次时间采样及镜头切换预热。

交付目录：`E:/WZMS_Media/demo055`。

- `WZMS_Demo_60s_Promo_1080p.mp4`：宣传版，含片头、片尾、项目原创的轻柔合成音轨与环境声。
- `WZMS_Demo_60s_Clean_1080p.mp4`：纯画面版，无标题和声音，供二次剪辑。
- `Original_Ambient_Score.wav`：48 kHz 立体声音轨。无第三方音乐采样，环境空气声来自项目自制素材，不是学校实地录音。
- `delivery-manifest.json`：视频尺寸、时长、校验值和验证结果。
- `frames-master`：1440 张原始 PNG。保留用于再剪辑和高质量转码，未纳入 Git。

工程中的最终镜头序列为 `/Game/WZMS/Cinematics/LS_Demo055_Campus_r02`。镜头路线与制作脚本纳入 Git；电影渲染插件仅用于编辑器。现有可玩游戏包保持在原交付目录。

`SourceReference/demo_shots_055.json` 保存镜头参数，`Automation/build_demo_sequence.py` 生成序列，`Automation/render_demo_sequence.py` 执行 UE 渲染，`Automation/finish_demo_film.py` 合成片头、声音及视频。重跑时应更换版本路径，保留已交付成片。

字幕字体为 Noto Sans SC，采用 SIL Open Font License；来源与许可见 `SourceFonts/NotoSansSC`。本 Demo 展示当前艺术化重建结果，未新增学校官方背书或发布平台信息。
