# 维护手册

## 日常改动

1. 修改 `theme.css`（唯一样式源文件；调色板集中在第 2/3/4 节）。
2. `npm ci && npm run check` —— 官方 stylelint、版本检查器单元测试、版本与 SVG 一致性；CI 的 Node 22/24 矩阵执行同一入口。
   涉及视觉/交互时另跑 `npm run check:browser`（需 agent-browser、其 Chromium、Python 3 与 Pillow；不会连接用户库）。
3. `./scripts/install.sh <vault路径> <配置目录>` 安装到测试库，重载后目检。
4. 提交时同步更新 `CHANGELOG.md` 的 `[Unreleased]` 段。

## 开发依赖安全审计

- 2026-11-01 本地 `npm audit` 返回 5 条中危报告，源于同一个
  `minimatch` 拒绝服务问题（`GHSA-g3hv-75wg-m249`），沿官方 lint 配置的
  `stylelint-no-unsupported-browser-features → doiuse → multimatch → minimatch` 链传播；
  不是 5 个独立漏洞，当次审计未提供自动修复路径。
- 这些包仅用于开发检查，不包含在发布的 `theme.css` / `manifest.json` 中；
  当次 `npm audit --omit=dev` 为 0，但不代表开发工具链没有风险。
- 后续升级时重新执行两种审计，跟踪上游兼容修复；避免仅为消除告警而运行
  `npm audit fix --force` 或强制跨大版本覆盖传递依赖。处理不可信配置/输入时，
  应在隔离环境中运行检查并限制执行时间。

## 发版

1. `CHANGELOG.md`：把 `[Unreleased]` 内容落到新版本号段（SemVer）。
2. 同步修改 `manifest.json`、`package.json`、`package-lock.json` 顶层及 `packages[""].version`，执行 `npm run check`。
3. 提交后打同号标签并推送：

   ```bash
   git tag -a 0.1.1 -m "0.1.1"
   git push origin main 0.1.1
   ```

4. `release.yml` 先执行 `npm run check`，再校验标签与 manifest 版本完全一致（不加 `v` 前缀）；
   全部通过后才创建 Draft Release 并附上 `manifest.json` + `theme.css`，
   到 GitHub Releases 页补写说明并 Publish。

## 上架社区目录（首次）

前置：仓库根目录需有 `README.md`、`LICENSE`、`manifest.json`，以及一张
**512×288** 的主题截图（建议放 `screenshots/` 并在 README 引用）。

1. 完成 `0.1.0` 发版（Release 挂件必须包含 manifest 与 theme.css）。
2. 在 [community.obsidian.md](https://community.obsidian.md) 用 Obsidian 账号登录并绑定 GitHub。
3. 「Add your theme」提交仓库，等待自动审查；有报错就修仓库、升版本、重新发版。

## 设计常量速查

| 常量 | 浅色（樱粉） | 深色（夜樱） |
| --- | --- | --- |
| 编辑器背景 | `#FFF0F5`（90%） | `#3C2D3C`（88%） |
| 侧栏背景 | `#FDE4EC`（84%） | `#352737`（80%） |
| 强调色 | `#C45A6D` | `#E3B1C9` |
| 正文 | `#5E3A46` | `#EBC4D7` |
| 粗体渐变 | `#B11F52 → #A02C80` | `#E6B397 → #EED0A6` |
| 代码底 | `#F2DEE4` | `#342834` |
| 关键字 | `#BB2557` | `#F3A4B8` |
| 字符串 | `#3C7016` | `#ACD39A` |
| 数字 | `#7B5F19` | `#EAD3A0` |

标题六色（h1→h6）：
浅色 `#A23B4E → #BD4F6C → #C96A83 → #D47B93 → #DF8CA2 → #E59EB1`；
深色 `#EAD3A0 → #F3A4B8 → #CCB0F0 → #ACD39A → #F3B795 → #93D2BC`。

> 括号内的百分比为面板不透明度（`color-mix`），调低更透、毛玻璃更明显。

## 移动端主编辑区圆角回归

- 第 23 节的移动端分支使用 `body.is-mobile`，覆盖手机和平板，不按屏幕宽度或悬停能力判断。
- 圆角与裁切放在主编辑区的 `.workspace-tabs` 或 root 直属 `.workspace-leaf`；不要给
  整个 `.workspace`、Ribbon、侧栏抽屉增加裁切，也不要直接去掉桌面规则的 `:not(.is-mobile)`。
- 外间距沿用 `--ob-card-gap`，叠加顶部、左右安全区；手机 root 不重复叠加顶部安全区，
  底部安全区仍由原生内容区处理。核对圆角时也要检查 root/嵌套 split 是否透出方形底色。
- 真机验收：iOS / Android 手机与平板，浅色/深色、横竖屏、编辑/阅读、键盘开关、
  底部导航显隐、侧栏抽屉与平板分屏；桌面圆角、侧栏按钮位置应保持不变。
- 桌面浏览器中的 DOM/CSS 测试只能验证选择器、层叠和几何布局，不能替代 iPad WebKit 真机验证。

## 无障碍回归

- `python3 scripts/check-accessibility.py`：隔离 Chromium 会话，覆盖浅深色阅读/编辑粗体、
  `<b>`、粗体内公式/行内代码，以及强制颜色模式下的实际字形像素。
- 高对比由 Chromium 启动参数模拟，并断言 `(forced-colors: active)` 生效。
  显式回退为 `currentcolor`，不依赖透明填充的引擎兜底；不能据计算样式透明就断言字形不可见。
- 减少动态效果时，代码光带、弹窗、菜单、建议、通知和悬停预览动画应停用；
  **不能全局清除动画**：`ob-scrollbar-progress` 是滚动状态同步，仍须从 0 更新到 1。
- 输出截图在 `/tmp/oboro-accessibility-*`。浏览器模拟不替代 Windows 高对比、iPad/手机真机验证。
- 浏览器套件目前需本地执行；CI/发布门禁只包含 lint、元数据和 SVG 静态回归。

## 粗体配色回归

- `--ob-bold-color` 与 `--ob-bold-gradient-end` 控制阅读 `strong` / `b` 和编辑 `.cm-strong` 的渐变；
  官方 `--bold-color` 引用同一实色起点，供打印与使用官方变量的实色场景共用。
- 浅色莓红 / 紫红去掉棕色感，深色采用柔和桃金 / 香槟金，减少粉色比例并保留轻微暖粉调；不加描边、光晕或底色。
  在不透明主题主底色上采样整条渐变，最小对比度分别约 5.97:1 / 6.90:1；
  玻璃背景随壁纸改变，不能将此数值视为所有自定义背景的对比度保证。
- 回归浅深色、阅读/编辑、手机/平板/桌面宽度、长文本换行、不透明模式及打印实色；
  检查粗体内公式 `.MathJax` 的 `-webkit-text-fill-color: currentcolor` 和行内代码独立配色仍有效。
  不改变字重、留白或表格/callout 材质；移动 WebKit 仍需真机目检。

## Callout / 表格玻璃回归

- 桌面、手机和平板尺寸，浅色/深色，分别检查阅读视图与实时预览。
- 覆盖普通表格、callout 内表格、嵌套 callout、折叠/展开、未知类型和自定义完整颜色。
  阅读侧不应泛白，callout 外侧阴影不被裁切；表头渐变保留且不再叠实色，悬停仍有轻染。
- 检查标题/图标类型色、表格外框和内部格线、正文斑马纹、左中右对齐、宽表横向滚动，
  以及实时预览中的单元格编辑/选择；普通 HTML 和嵌入内容不应被整体隔离。
- 开启 `ob-solid` 和系统减少透明度，callout 渐变、阴影、模糊应退场，类型色和边框仍有效。
- 对比编辑视图修改前后的背景、色晕、缘光、模糊和表头；类型色格式修复会恢复原生
  标题/图标和块内表格配色，但不应重调玻璃材质。桌面浏览器回归不能代替移动 WebKit 真机目检。

## 编辑区与面板细枝繁樱滚动条回归

- 图稿唯一源文件是 `scripts/assets/scrollbar-art.svg`（可直接打开的 SVG），四色映射在
  `scripts/scrollbar_art.py`。修改后执行 `python3 scripts/check-scrollbar-art.py --write`，统一生成
  浅深色轨道、选中图与端部渐隐图；不要手改 CSS 内嵌 SVG。默认检查会验证生成结果与主稿一致。
  浅深色生成结果集中在第 2/3 节：`--ob-scrollbar-art-image` 是轨道原画，
  `--ob-scrollbar-active-art-image` 是原生滑块的变色版。两者仅允许 paint 颜色不同，
  路径、花位、变换、透明度、18×192 图幅必须完全相同。执行
  `python3 scripts/check-scrollbar-art.py` 检查不变量；不要通过增加形状、底色、光晕或色条替代重着色。
  `--ob-scrollbar-active-top-image` / `--ob-scrollbar-active-bottom-image` 是自动生成的端部版本，
  内部只重复同一原画并渐隐其 alpha；改配色或花朵缩放后执行 `python3 scripts/check-scrollbar-art.py --write`，不要手改派生 SVG。
- 轨道原画固定、连续且透明；透明留白直接透出各编辑器/面板的实际背景，包括玻璃、壁纸和渐变。
  滑块只在其自身范围内绘制同相的变色原画：浅色未选中花枝使用更淡、低饱和的雾樱灰，
  选中枝面和花瓣保持浓莓樱红；只改画内 paint，不通过降低整条轨道的 opacity 弱化背景。深色以暖金枝干、
  珊瑚粉花心和奶金瓣缘拉开与灰紫原画的色差；深色未选中花枝降低明度，但不压暗透明背景或铺设色条。
  上下各 18px 缓入/缓出，中段保留完整色差；端部裁切在 SVG 内完成，原生伪元素不依赖 mask/filter 支持。
  精绘主稿保留主要花位与枝干轮廓，补入不对称花瓣、翻折透色、分叉花脉、疏密花丝、侧花与伴生花苞；
  枝干保留断续皴理和横向皮孔。原画、变色版与端部派生图始终共享同一几何与透明度，
  不为高亮单独增加花朵、花签、胶囊底框、亮边或端光，也不改变透明背景。
  保留原生比例长度、64px 最小高度和完整拖动热区；短笔记按实际滑块长度变色。
- 几何同步使用 CSS 滚动时间线 `--ob-scrollbar-progress`，并非自动播放动效；减少动态效果时
  仍需跟随用户滚动，不能停止同步使原画错位。高度容器设在无内边距的 `.cm-editor` /
  `.markdown-reading-view`，不能移到有 `--file-margins` 内边距的 CM6 scroller。
  滑块背景百分比基于「滑块高 − 图高」；背景偏移抵消原生滑块位移，保留图案原位。
  原生滑块坐标向下取整，对应负背景偏移用 `round(up, …, 1px)`；同时通过滚动状态容器查询
  在横向溢出时扣除 `--scrollbar-height`，防止宽表/代码导致纵向错位。
  三层背景都以 border-box 为原点：中段以 18px 透明上下边框裁切，端部层不重复且无外层 viewBox，
  避免拉伸原画。顶部图像高度为「24px + 滑块顶坐标」，内部图案上移「图像高度 − 24px」；
  底部图像高度为「24px + 滑块底坐标」，底部对齐、图案下移 24px。两者恰好抵消原生滑块位移。
  CSS 的 18px/24px 必须与生成脚本的 EDGE_PX/PHASE_PAD_PX 一致；24px 是透明视口余量，不是端光或装饰。
- 内置面板的滚动容器自身使用 `container-type: size scroll-state`，而不是整个叶面板的高度，避免工具栏/搜索框
  被算入轨道。`100cqh` 只包含 content-box，`--ob-scrollbar-block-inset` 补回原有上下 padding；
  `--ob-scrollbar-panel-top/bottom` 按面板对应的原生间距变量配置，文件列表移动抽屉顶部为 12px，
  设置内容还需兼顾 setting-page、手机顶部标题、安全区和键盘留白。不要直接修改用户 padding 来凑齐图案。
  Chromium 的容器查询高度仍包含横向滚动条占用；面板和 Markdown 一样通过 `scroll-state(scrollable: inline)`
  扣除一次 `--scrollbar-height`。必须以 `clientHeight` 做实测对照，不能假定自身 size 容器会自动排除该占用。
  面板必须有确定高度或 flex-fill 布局，不能把 size containment 扩展到自动内容高度的弹窗、嵌入查询或手机设置子列表。
  手机设置菜单滚动的是外层 `.vertical-tab-header`，桌面/平板是内部分类/搜索列表；不要同时装饰父子两层。
  共享 `:is()` 的特异性取最高分支，默认间距使用 `var()` 回退，避免高特异性默认值压过各面板的单独配置。
  `scroll-state(scrollable: inline)` 对 `overflow-x:hidden` 的程序化滚动也可能成立，不等于有可见横向槽。
  原生文件列表必须使用 `--ob-scrollbar-inline-gutter: 0px`，避免多扣 12px 使高亮原画随进度偏移。
- `python3 scripts/check-scrollbar-panels.py` 使用独立 agent-browser 会话和 Python Pillow，打开仓库内的
  `scripts/fixtures/scrollbar-panels.html`，不连接/修改用户 Obsidian。检查浅深色、390/834/1440px、
  非整数高度、横向溢出、安全区、键盘和手机设置；校验尺寸/内容高度、轨道原位、面板独立进度、
  高亮只出现在原生滑块内、短内容不造滑块及嵌入滚动区保持原生，并验证原生拖动和 PageDown，
  截图/报告写入临时目录。
- `python3 scripts/check-scrollbar-motion.py` 保留原画几何/透明度和 18px 渐隐，以白色轨道/红色高亮在黑底上校验轮廓；
  连续正反向滚动期间不切样式、不切 overflow、不重建滚动条，检查高亮像素不得落在静止原画轮廓外，防止视觉重影。
- 所需特性以 `@supports` 联合检测（滚动时间线、size/scroll-state 容器和 CSS round）；
  不支持时去除装饰原画并回退基础滑块，不展示未同步的花枝副本。强制颜色模式普通/悬停/按压均为系统实色。
  纵向覆盖主区/侧栏的 Markdown 阅读容器与 CM6 scroller，以及文件、全局搜索、目录、标签、书签、
  属性、反向/出站链接和设置滚动区；不通配任意 `.view-content` 或插件容器。嵌入笔记、嵌入查询、
  代码/表格内部滚动条以及所有横向滚动条保持原样；Canvas/PDF/Bases/插件自有滚动器不在本次装饰范围。
  不使用 JS、滚动事件、定位覆盖层、巨大投影、滤镜或编辑器裁切。
- 回归应覆盖浅深色、长短/空笔记、顶部/任意中间位置/底部、独立分栏、原生拖动和键盘，
  390/834/1440 宽度、超过 1000px 及非整数高度、有/无横向溢出、纯色与异色玻璃背景。
  对比关闭滑块图案的原画与完全透明滚动条：变化必须局限于滑块覆盖的原有花枝轮廓，
  检查透明留白没有矩形色带；抗锯齿边缘允许像素舍入误差，不得出现枝花双影、错位或断裂。
  移动滑块后同一高度的轨道图案保持原位；正文、编辑器尺寸和其他滚动条不变。
  另与无端部渐隐的完整重着色对照：上下各 18px 的色差强度平滑递增/递减，中段强度不变，
  不能用整根滚动条不变的截图作为渐隐生效的证据。
- 枝干保留独立左右边缘的封闭填充、收尖分杈、断续树皮和节疤；花瓣保留缺口、叠染、花脉和花蕊。
  不简化为等宽描线；长卷上下端必须衔接，花梗须连枝，正常宽度下目检，不仅放大看图。
- Obsidian `dev:screenshot` 会临时隐藏滚动条，实际滚动条截图可用 `dev:cdp method=Page.captureScreenshot`。
  后台截图可能保留旧帧。iOS/iPadOS 系统覆盖式滚动条可能忽略自定义图案，不强行替换触控滚动；
  桌面截图与窄屏模拟不代替移动 WebKit 真机验收。

## 已知事项

- **展开按钮悬停归属**：`.sidebar-toggle-button` 内部还有 `.clickable-icon`，后者原生
  `:hover` 会另画底色并改变图标颜色、SVG 透明度。仅给外层加 hover 会造成边缘与图标中心
  两级反馈。桌面端由外层 hover 同步控制背景与图标反馈，内部背景固定透明；不要清除
  `.clickable-icon:focus-visible` 的原生焦点提示。复核左右按钮边缘与中心的计算样式应一致。
  右侧原生布局包含不对称内边距；将悬停底色放在外层后须改为对称内边距并垂直居中，
  检查 SVG 与外层背景中心重合，同时保持外层按钮位置和尺寸不变。
- **左上角方形背板的真实来源**：Obsidian 1.14.5 的
  `.workspace-ribbon.mod-primary::before` 是独立的标题拖动占位层，原生尺寸取
  `--ribbon-width` × `--header-height`，底色取 `--titlebar-background`，并绘制底边线。
  Ribbon 卡和按钮的圆角不会裁切该层；此前将它归因于壁纸或 Ribbon 卡片方角的判断不成立。
  桌面端只将该伪元素底色、底边线设为透明，保留 `content`、尺寸和 `app-region: drag`，
  不用隐藏工具栏或调整按钮定位来规避。排查时须同时检查元素及 `::before` / `::after`；
  更新样式后等待重绘再截图，且移除临时诊断样式后复核安装版本。
  参考 Minimal 的 Ribbon 变体对 `::before` 的独立处理，以及 AnuPpuccin 卡片布局对
  Ribbon 伪元素背景和底边线的显式控制；本主题只按自身布局清除绘制，不移植它们的布局规则。
- **对比度**：浅色 h6 `#E59EB1`（1.93:1）与次要文字 `#8E6F7A`（4.05:1）低于 WCAG AA 的 4.5:1，
  为「樱花木彩墨」标题阶梯与次要信息的既有设计取向；如需收紧，压深 h6 至 `#C96A83` 一档即可。
- **顶部标签留白**：主编辑区非堆叠的 `.workspace-tab-header-container` 内，活动/悬停
  底色统一放在 `.workspace-tab-header-inner`，外层透明；利用原生外层的底部 padding
  留出约 4px，不通过缩短整个 tab 的高度、加 margin 或抬高标签栏来制造间隙。
  活动态沿用原生 `--tab-inner-background-active`，悬停/触摸反馈共用
  `--tab-inner-background-hover`；外层点击区域及关闭按钮位置不能缩小或跳动。
  回归检查桌面与平板浅深色、多标签切换、悬停、分屏；手机原生隐藏顶部标签栏的行为、
  侧栏图标标签、移动端抽屉选项及 `.mod-stacked` 堆叠标签应保持原样。
- **渐变粗体与公式**：`-webkit-text-fill-color: transparent` 会向后代继承；MathJax 的
  公式根节点 `.MathJax` 必须恢复 `currentcolor`，避免移动端 WebKit 依赖祖先的
  `background-clip: text` 来绘制公式。只重置公式，不取消整段粗体渐变，也不要给公式
  所有后代强制指定颜色，否则会破坏 `\textcolor` 等显式着色。与粗体内联代码补丁一起维护。
  回归时在手机/平板浅深色阅读模式检查 `**文字 $x^2+y_1$ 文字**`、`**$x^2$**`、
  `**分式 $\frac{1}{2}+\sqrt{x}+\text{speed}$**` 以及
  `**着色 $\textcolor{red}{x}+y$**`；公式须完整可见且显式着色保留，普通粗体仍是渐变。
  同时检查非粗体公式、粗体内行内代码、`<b>` 和实时预览不回归。桌面浏览器的移动端
  尺寸测试不等于 iPad/iPhone WebKit 真机验证，后者需另行目检。
- **stylelint 豁免**（见 `.stylelintrc.json`）：`selector-class-pattern` 置空（Obsidian 内部类如
  `HyperMD-codeblock-begin` 非 kebab-case）；`declaration-block-no-duplicate-custom-properties`
  置空（「先实色、再 color-mix」双写兜底模式必需）；`property-no-vendor-prefix` 置空与
  `declaration-block-no-duplicate-properties` 的前缀忽略（Safari/WKWebView 需要
  `-webkit-backdrop-filter` / `-webkit-mask-image` / `-webkit-background-clip` 等前缀成对声明，
  **切勿对 theme.css 裸跑 `stylelint --fix` 后不复核——它曾把前缀行当重复属性删除**）；
  `no-descending-specificity` 置空（阅读模式与实时预览两套选择器必然交替优先级，属规则误报）。
  `text-decoration*` 的 partial-support warning 来自插件的 caniuse 数据，可忽略。
- **callout 类型色**：浅色侧 8 组标题色全部压至对比度 ≥4.5:1（青 `#3E7168` 绿 `#4C7343`
  金 `#8A6E1F` 橙 `#A85F2D` 玫 `#A94658` 蓝 `#4A6FA5` 红 `#B03A4E` 紫 `#8A5F9E`）。
- **Callout 玻璃配方**：纯 CSS 主题无法向 DOM 注入 SVG filter，因此不做真实折射；
  用 `--ob-callout-*` 的顶部高光弧、右下类型色晕与底部色缘模拟玻璃厚度。
  类型色薄底由 `--ob-callout-tint` 控制（浅色 7%、深色 9%），边框将类型色 32% 混入原玻璃缘色，
  仅略微增强背景区分；不要加大整块染色或叠不透明色板，避免青+粉互相抵消成灰卡。
  高光、色晕、阴影、模糊沿用既有配方；`ob-solid` 与 `prefers-reduced-transparency`
  继续使用原 10% 类型色底，并显式清掉 `background-image` / `box-shadow`。
- **Callout 颜色变量契约**：`--callout-color` 必须是完整 CSS 颜色（如 `rgb(62 113 104)`），
  与当前原生标题、图标、Bases 和表格 `color-mix()` 共用；逗号三元组会让原生声明失效，
  甚至使块内表格边框变成 `none`。透明度用
  `color-mix(in srgb, var(--callout-color) 25%, transparent)`，不要再套 `rgb(var(...), …)`。
  内置类型保留原 RGB 值，未知类型沿用原生默认色；自定义类型也应提供完整颜色。
- **引用块樱粉 / 藤紫配色**：浅色 `#C45A6D` 的 10% 薄底、深色 `#C8B4E0` 的 12% 薄底，
  浅色与主题樱粉呼应，深色与夜樱背景保持温和区分；缎带和引号取同一强调色。官方 `--blockquote-*`、
  渲染 `blockquote` 与编辑行 `.HyperMD-quote` 同源，不改变正文色、字体或原生引用标记。
- **阅读视图绘制边界**：实时预览的 CM widget 有原生 `contain: paint`，阅读视图没有。
  浅色原生 callout 的混合会因此与整张笔记合成，呈现白雾；仅对阅读视图中直接包含 callout
  的 `.el-div` 使用 `isolation: isolate`，不隔离整个 preview sizer 或所有 HTML 块，
  也不用会裁掉外侧阴影的 `contain: paint`。该 `:has(> .callout)` 只检查原生块包装的
  直接子级，局部豁免 stylelint 的 `:has` 警告，不扩展为全页面后代搜索。
- **阅读表头叠底**：原生 `thead tr` 的实色会盖住 `th` 的透明渐变。只清除阅读视图的
  行底色，悬停时使用 7% 强调色；不重置所有 `tr`/`td`，以保留正文斑马纹、对齐和选择。
  透明问题的修复不改实时预览的单元格编辑控件与滚动；共同视觉细节由下述晶签外观规则负责。
- **悬浮晶签表格**：普通笔记表格的外观规则限于阅读/实时预览，排除 `.dataview` 与
  `.table-view-table`；不改 Bases 数据表。强调色优先使用 callout 类型色，否则使用主题强调色。
  签头的圆角、透明渐变与内阴影直接画在 `th` 上，`background-clip: padding-box` 让原有
  色线分隔各列晶签；整条 `thead tr` 不叠背景，不能用 `border-spacing` 或调整边框宽度
  来做悬浮间距，否则会扰动原生选择/拖拽几何。外框取 66% 强调色，内侧 1px 亮缘与底部 3px / 18% 色缘构成双层包边；
  表头下沿取 72% 强调色，配合 1px 亮线与 3px / 32% 内色缘单独收边。
  其余表头及正文四边取 52% 强调色，正文顶/左侧叠 1px 亮缘形成刻线质感；
  不能再透明化纵线或末行边界，不改原生边框宽度。新阴影只用 inset，避免窄屏滚动裁掉外发光；
  不透明/减少透明度模式通过 `--ob-table-frame-shadow`、`--ob-table-header-edge`、
  `--ob-table-cell-etch` 关闭新增玻璃装饰，保留色线与首列色脊。
  首列用 2px inset 色脊定位，RTL 时反向，不新增行号或内容。
  不用单元格伪元素，避免覆盖原生选择层；不移动表头或修改表格显示类型。
  12px 外圆角与 widget 外包装保持一致，不追加模糊层、不覆盖字体或列对齐。
  阅读/实时预览 callout 的渲染单元格与原生表格编辑器 `.table-cell-wrapper` 使用相同留白，
  但实时预览表格 widget 的 `th`/`td` 本体仍须保持原生零 padding；水平留白用 `clamp()` 随窄屏收紧。
  表头提亮只响应真正悬停或 `:focus-within`，无动画、不屏蔽原生焦点。
  回归需对比改动前后单元格的 padding、四边宽度、对齐与尺寸，以及表格背景/滤镜；
  检查 1440/834/390 宽度、浅深色、不透明模式、RTL、callout 类型色、宽表滚动和选择层。
  DOM/CSS 模拟可验证样式与几何，不能替代原生单元格编辑/拖拽操作或 iPad WebKit 目检。
- **阅读表格二次提亮**：表体即使是 18% 轻染，重复使用含 `brightness(108%)` 的
  chip 滤镜也会将已提亮的浅色面板冲白。阅读表格取消自身的二次 backdrop 滤镜
  （保留 WebKit 前缀），直接透出外层面板或 callout 已有的玻璃模糊；保留轻染、缘光、
  斑马纹和表头渐变。不要只删滤镜中的亮度：再次饱和采样仍会改变浅色底，表格本身不应
  再变成一块玻璃面板。编辑表格继续使用原 chip 配方，不透明/减少透明度分支不变。
  回归除检查透明 alpha 外，应在 80% 实度的浅色面板上对照表体与底色截图，避免
  “样式透明、视觉白板”的漏测；另查深色、嵌套 callout 表格与窄屏横向滚动。
  桌面 Chromium 的截图不代替 iPad WebKit 目检。
- **backdrop-filter 包含块陷阱**：带 `backdrop-filter` 的元素会成为其**绝对定位后代**的
  包含块。侧栏开关按钮（`.sidebar-toggle-button`）在 DOM 里是 Ribbon 的后代——曾因给
  Ribbon 加模糊导致按钮被"搬位"到标签栏下方。因此：**Ribbon 永远不加 backdrop-filter**；
  给含原生浮件（absolute 定位 UI）的容器加模糊前，务必 A/B 实测按钮位置
  （摘除主题 style 标签前后对比 `getBoundingClientRect()`）。
