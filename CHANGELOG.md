# Changelog

本项目的所有显著变更都记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

## [Unreleased]

## [0.1.4] - 2026-10-30

### Fixed

- **顶部活动标签留白**：桌面端与移动端主编辑区的普通顶部标签统一在内层绘制选中与悬停
  底色，保留原生底部约 4px 间距，避免活动标签贴住内容边界；点击区域、栏高、侧栏和
  堆叠标签保持不变。
- **粗体内嵌公式显示**：阻止渐变粗体的透明文字填充传入 MathJax，修复移动端阅读模式
  中粗体包裹的 `$...$` 公式显示异常；公式使用实色，周围粗体仍保留渐变，兼顾实时预览。
- **移动端主编辑器圆角**：手机与平板统一启用浮动窗格圆角，在窗格容器层裁切标签栏与
  内容背景，避免内部方形背景露角；外间距保留原生安全区差异，不改动桌面、Ribbon
  或侧栏抽屉布局。

## [0.1.3] - 2026-10-26

### Added

- **宣传图**：`screenshots/promo.png`（2560×1440），改为“设计标本板”构图：
  浅色笔记大卡 + 浅色 Liquid Glass callout + 深色代码卡 + 六色色板 + 8 组
  callout 色点，并带 `01` / `02` 标注；README 中英文预览置顶。

### Changed

- **Callout 换成更透亮的 Liquid Glass**：参考 Apple clear-glass 的分层做法，去掉原来的
  10% 类型色实底，改为 3% 中性白 + 顶部镜面高光弧 + 极薄液面纱 + 双色缘光；类型色
  只留在图标、标题、右下折射晕与底部色缘。`--ob-callout-*` 在浅/深色块分别定义，
  `ob-solid` 与 `prefers-reduced-transparency` 下退回实色。
- **面板默认更透**：浅/深色默认面板实度统一为 60% / 54%，壁纸纹理能真正透过编辑器、
  侧栏与标签条；原先浅色 78/72、深色 74/68 与 Style Settings 的 74/68 不一致。
- **截图重拍**：`screenshots/screenshot-light.png` / `screenshot-dark.png` 使用新版
  液态玻璃与樱枝壁纸重拍（2560×1490）。

### Fixed

- **无 Style Settings 时面板实度取错默认值**：浅色块曾写 78/72、深色块 74/68，
  而 Style Settings 声明 74/68，导致装与不装插件看到两种默认。现统一为 60/54。

## [0.1.2] - 2026-10-25

### Changed

- **壁纸引擎语义修正：留空 = 无任何背景图**。移除内置兜底渐变（浅色樱花粉渐变、
  深色夜樱三层渐变）——渐变本质也是客制化背景，不该替用户做主。
  `--app-bg-image`（即 Style Settings 的浅色/深色壁纸两项）成为唯一图源，
  留空时主题为纯色底，玻璃观感依赖壁纸。壁纸设置只支持完整
  background-image 值（相对路径经实测无法由纯 CSS 解析，撤回）。

## [0.1.1] - 2026-10-25

### Fixed

- 官方主题库提审修复：README 增加英文说明（社区以英文为主）；
  `manifest.json` 增补 `screenshot` 字段指向 `screenshots/screenshot-light.png`
  ——审查扫描的提交早于截图入库，故报缺失。

### Accepted warnings（审查警告的取舍说明）

- `text-decoration` 部分特性警告：来自行内链接点状下划线（主题签名设计，保留）；
- 重复 `background-color`：旧 webview 不支持 `color-mix` 时的实色回退写法，故意为之；
- `:has()`：仅用于档案条两枚图标的子树定位，失效重算开销可忽略；
- CSS 体积偏大：源码可读优先，发布资产未做压缩。

## [0.1.0] - 2026-10-25

Oboro（朧樱）首个公开版本，自 Sakura Macaron 更名而来。

### Changed

- **主题更名 Sakura Macaron → Oboro（朧樱）**：「朧」即玻璃的雾，一词收拢夜樱、
  樱粉与磨玻璃。全部私有变量前缀
  `--smc-*` → `--ob-*`，Style Settings 面板 id `smc-*` → `ob-*`
  （**已保存的 Style Settings 自定义值会重置为默认**）；安装目录
  `themes/Sakura Macaron/` → `themes/Oboro/`。

### Added

- **浮动圆角玻璃卡（第 23 节）**：组件交界从扁平板拼接升级为 macOS 浮动卡语言——
  工作区 flex `gap` + 四边衬距透出壁纸，侧栏（含新类名 `mod-sidedock`）/编辑器主区/Ribbon/
  状态栏各自成为带圆角（14px 卡 / 10px 药丸）、悬浮投影与镜面缘的独立玻璃卡；
  标签区顶部、编辑器底部、侧栏 vault 档案条同步圆角衔接防方角穿孔。
  截图视检 + 几何实测复核（缝隙 60px 处壁纸可见、圆角无穿帮）。

### Fixed

- **右侧展开按钮悬停对齐**：改用对称内边距并垂直居中，消除图标相对悬停背景偏左的问题，保持外层按钮位置和尺寸。
- **左右展开按钮双层悬停**：由外层按钮统一控制背景、图标颜色和透明度，内部图标背景保持透明；鼠标从边缘移入图标时不再触发第二级视觉状态，保留原生键盘焦点提示。
- **左上角圆钮几何微调**：直径从 30px 调整为 36px，横向对齐工具栏中线，纵向对齐顶部标签栏中线；保持圆形玻璃和透明背板。
- **左上角圆钮背后的方形层**：清除原生 `.workspace-ribbon.mod-primary::before`
  的标题栏底色与底边线，保留其拖动区域和尺寸；不移动圆钮、不隐藏 Ribbon、不更改侧栏状态。
- **逗号三元组颜色记法**：`rgb(var(--callout-color) / N%)` 斜杠+逗号混合在 Chromium
  非法（整条丢弃，callout 边框/底色因此失效）——统一改为实测有效的
  `rgb(var(--callout-color), 0.N)` 逗号记法（采纳用户先行修复，撤 stylelint 行级豁免）。
- **工作区层级适配**：侧栏真实类名为 `.mod-sidedock.mod-primary/secondary-split`，
  浮动卡与圆角规则补齐新类名选择器（保留旧类名兼容）。
### Fixed

- **顶部标签条/活动标签/侧栏活动标签/视图标题栏/Ribbon 全面接入玻璃体系**（实测验证）：
  - 关键发现：Obsidian 的 app.css 在 `.workspace-tabs.mod-top` 上把
    `--tab-container-background` 重定义为 `var(--titlebar-background)`——顶部标签条实际
    读取的是标题栏变量，此前 90% 实度即来源于此；已把 `--titlebar-background(-focused)`
    接入玻璃实度滑条（深浅双模式）。
  - 活动标签：`--tab-background-active` 从 92% 实底降为 26% 轻染（渐变指示条标识活动态），
    标签本体透明化，消除「标签叠标签栏」的实心叠加；侧栏活动标签以决胜特异性规则同款处理。
  - 视图标题栏（文件名条）透明，玻璃由 leaf-content 单层承担。
  - Ribbon 62% 粉调玻璃 + 0.75 剂量模糊 + 镜面侧缘。
  - 「减少透明度」回退改为实度变量 100% 方案（所有 color-mix 自动变实），
    同时修复此前回退行会被 color-mix 行压住的隐患。
- **表格玻璃改轻染（tint）架构**：此前表格底 76% × 行纹 55% × 编辑器面板 78% 三层相乘，
  壁纸透过率仅 2.4%，观感即完全不透明。现表格底 = 面板色 30% 染色（`--smc-table-tint` 可调，
  阅读模式与实时预览 widget 双路径）、行纹降至 16%/18%、表头渐变 48%→12%，
  表格区域壁纸透过率恢复到约 15%；代码块保持 slab 形态（88/90%）保等宽文本可读。
- **状态栏液态玻璃化**：此前仍是 snippet 时代的不透明粉色实条（右下角字数/反链区域），
  与整体玻璃体系脱节。现为粉调玻璃——浅色 `#F8BBD0 @55%` / 深色 `#AD7F96 @45%` +
  0.75 剂量模糊 + 饱和度 + 镜面上缘 + 顶部分隔线；深色文字色随玻璃底改为浅粉
  `#F5CFE1`；「减少透明度」回退时还原为实底粉条与深梅字。
### Added

- **官方变量补全层（第 22 节）**：对照官方 CSS 变量参考文档（46 页 / 651 项）做全量审计后补齐
  约 200 个原生变量——樱李/樱粉 **color-base 中性灰阶**（全应用表面底座）、图标四态色、
  加粗/斜体/标点色、语义色（success/warning/error 双模式）、导航选中/高亮/缩进参考线、
  表格编辑态（选区/拖拽手柄/添加按钮）、滑块/胶囊/拖拽幽灵/色板、弹窗与输入基础几何、
  圆角阶梯（6/10/14/18px）、标题字重与行内标题排版、脚注字号、**Bases 核心视图**、
  半透明窗口底色；布局基元（间距/图层）保持官方默认。
- **悬停预览卡片（Popover）玻璃化**（18.12）：页面预览弹层接入液态玻璃 + 弹性入场。
- 采纳实测修正：Editing Toolbar 真实选择器 `#editingToolbarModalBar`（替换错误的
  `.editing-toolbar` 猜测）。
### Added

- **液态玻璃扩展到笔记内容物**：表格玻璃底 + 0.5 剂量模糊（阅读模式）、代码块底色玻璃化
  （深 92% / 浅 94%，壁纸微透）、callout 玻璃升级（模糊 + 饱和度 + 10% 色底）、
  笔记嵌入卡片加模糊；「减少透明度」回退同步覆盖内容物。
- **插件适配（第 21 节）**：Dataview（内联查询结果药丸，表格自动继承玻璃表格）、
  Tasks（计数药丸）、Calendar（今日强调圆点 / 选中描边 / 周末樱色）、
  Editing Toolbar（浮动工具条液态玻璃）、Table Editor（容器圆角衔接）、
  Kanban（看板 / 列表 / 卡片玻璃 + 拖拽樱粉辉光）。
### Added

- **标志性细节（第 20 节）**：形状级一眼可辨的定制——
  - 标题装饰：h1 渐变底线（阅读+实时预览）、h2 渐变左缎带；
  - 活动标签页渐变指示条；
  - 任务方块六变体：`x` 实心对勾、`/` 半填充琥珀、`-` 横线取消、`!` 红底惊叹、`?` 蓝虚线、`>` 紫晕延期，配文字变色；
  - 引用块 ❝ 装饰符；callout 图标类型色圆芯片；
  - 文件导航药丸条目 + 活动文件左侧竖标；表格圆角外框 + 渐变表头 + 行悬停着色；
  - ribbon 图标悬停弹性旋转；视图标题栏樱粉底边光；状态栏条目药丸；
  - 纤细渐变滚动条；空状态 ❀ 前缀；行内链接点状下划线；属性值药丸底；
  - inline title 接入 h1 标题色。
### Added

- **液态玻璃引擎（第 6 节重制）**：调研 Glass Scholar / Isinglass / AbsolutelyGlass / macOS Tahoe
  四个成熟实现后，把毛玻璃升级为 Apple Liquid Glass 质感——
  - `backdrop-filter: blur(24px) saturate(170%)`：饱和度提升是「液体感」的关键（编辑器 0.6 剂量保可读性）；
  - 镜面高光缘：`inset 0 1px 0` 上缘高光 + 0.5px 内描边（深浅分别调校）；
  - 细颗粒噪点：弹层叠加 feTurbulence SVG 颗粒（3.5% 不透明度）；
  - 弹层全玻璃化：菜单 / 弹窗 / 命令面板 / 通知 / 移动端底栏（实底 82–88% + 多层镜面阴影）；
  - **面板实度 / 模糊 / 饱和度全部变量化**，Style Settings 新增 4 个滑条实时调节；
  - 无障碍：系统「减少透明度」（`prefers-reduced-transparency`）时自动退回实色面板并停用壁纸。

### Changed

- 面板默认实度下调（深色 88/80 → 78/72，浅色 90/84 → 82/76），液态玻璃通透感立现；
  壁纸与玻璃滑条联动说明写入 Style Settings 面板。
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

### Fixed

- **主面板不透明**：Obsidian 的 root split / leaf / view-content 会各自画一遍半透明背景，
  三层 82% 叠加后有效不透明度 ≈99.4%，液态玻璃完全失效。新增「递归透明链」——中间层
  一律透明，玻璃底只由挂 `backdrop-filter` 的单一层承担（编辑器落在 leaf-content，
  侧栏落在 split 层）；实探验证透过率从 <1% 恢复到 18%（82% 单层）。

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

[Unreleased]: https://github.com/player-Muteki/oboro/compare/0.1.3...HEAD
[0.1.3]: https://github.com/player-Muteki/oboro/releases/tag/0.1.3
[0.1.2]: https://github.com/player-Muteki/oboro/releases/tag/0.1.2
[0.1.1]: https://github.com/player-Muteki/oboro/releases/tag/0.1.1
[0.1.0]: https://github.com/player-Muteki/oboro/releases/tag/0.1.0
