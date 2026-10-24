# Changelog

本项目的所有显著变更都记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### Added

- **入场动效（第 19 节）**：弹窗 / 菜单 / 命令面板建议列表弹性绽放（scale+fade，弹性曲线），
  通知淡入；跟随系统 `prefers-reduced-motion` 偏好自动停用全部主题动画（含代码块光带）。
- **Callout 别名**：`seealso`→蓝、`add`/`added`→绿、`change`/`updated`→橙、
  `remove`/`removed`/`deleted`→红。

### Changed

- **私有变量前缀 `--rtm-` → `--smc-`**（42 个变量）：`rtm` 前缀属于 Retroma 主题的命名空间
  （其主题内含 3300+ 个 `--rtm-*` 变量），独立主题改用自有前缀，彻底切断命名混淆。
### Added

- **组件个性化设计**（调研 Minimal / Things / AnuPpuccin / Catppuccin 后补齐）：
  - 链接悬停着色、高亮圆角荧光笔胶囊（换行断片克隆）、标签胶囊圆角。
  - 列表三级圆点（实心樱点 → 空心圆 → 方点）；任务框重绘为马卡龙圆角方块 + 对勾 SVG，
    已完成退隐、已取消删除线、延期高亮（读取与实时预览双模式）。
  - Callout 玻璃化：圆角 12px、类型色描边与 8% 玻璃底，8 组类型色映射八色基板
    （浅色压深至对比度 ≥4.5:1）。
  - 引用块：强调色左缎带 + 玻璃底（双模式）；分隔线渐隐线 + 居中樱花符号 ❀。
  - 图片圆角卡片（樱粉柔影 + 悬停微抬）；笔记嵌入玻璃卡 + 强调色顶边。
  - 属性面板配色（键名次要色、图标强调色）；关系图 10 项色板双模式。
  - UI 控件：tooltip / 右键菜单 / 弹窗 / 命令面板建议列表（玻璃 + 圆角 + 选中强调态）、
    通知、主按钮马卡龙渐变、输入框聚焦光环、开关强调色、滑条 accent-color、
    滚动条圆角、搜索命中高亮、状态栏字号、空状态、移动端底栏玻璃。

### Fixed

- 恢复 `stylelint --fix` 误删的 `-webkit-` 前缀声明（backdrop-filter ×6、mask-image ×2、
  background-clip ×4），并在 `.stylelintrc.json` 豁免前缀属性的重复检查，防止复发。

## [0.1.0] - 2026-10-24

### Added

- 初始版本：从库内 CSS 片段移植为独立主题。
- 双模式调色板：浅色「樱粉」（樱花粉渐变）与深色「夜樱」（樱粉微光 + 藤紫微光 + 斜向深樱底）。
- Obsidian 原生变量接驳层（深浅各约 90 项），全部 `color-mix` 声明带实色兜底，旧渲染内核自动回退。
- 字体接入官方主题入口：正文衬线族（Lora → 思源宋体 → 宋体系列）、代码等宽族（Cascadia Code → JetBrains Mono）。
- 浅色语法色板（正文墨色 + 暖木彩语法），与深色夜樱语法色板对称。
- 组件规则：六级标题色阶梯、渐变加粗（含行内代码拯救补丁与打印/PDF 回退）、毛玻璃面板、代码块七段脉冲光带（浅色樱花粉 / 深色夜樱语法色）、语言胶囊（C/C++/C#/x86/ASM/Verilog/Java/Python/Rust）、Copy 按钮修补、代码区字重免疫。
- 壁纸引擎：`--app-bg-image` 优先、渐变兜底；支持 Style Settings 输入或脚本注入 `--dv-light-bg` / `--dv-dark-bg`。
- Style Settings 配置面板：壁纸 ×2、代码块光带开关。
- 移动端适配：`(hover: none)` 下背景回退为随内容定位。
- 工程：stylelint（官方 obsidianmd 规则）+ GitHub Actions lint / 自动发版工作流 + 一键安装脚本。

[Unreleased]: https://github.com/player-Muteki/sakura-macaron-obsidian/compare/0.1.0...HEAD
[0.1.0]: https://github.com/player-Muteki/sakura-macaron-obsidian/releases/tag/0.1.0
