# Changelog

本项目的所有显著变更都记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

## [Unreleased]

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
