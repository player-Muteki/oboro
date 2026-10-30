# 维护手册

## 日常改动

1. 修改 `theme.css`（唯一样式源文件；调色板集中在第 2/3/4 节）。
2. `npm run lint` —— 使用官方 `stylelint-config-obsidianmd`（与社区主题审核同一套规则）。
3. `./scripts/install.sh <vault路径> <配置目录>` 安装到测试库，重载后目检。
4. 提交时同步更新 `CHANGELOG.md` 的 `[Unreleased]` 段。

## 发版

1. `CHANGELOG.md`：把 `[Unreleased]` 内容落到新版本号段（SemVer）。
2. `manifest.json` 的 `version` 改为同一版本号。
3. 提交后打同号标签并推送：

   ```bash
   git tag -a 0.1.1 -m "0.1.1"
   git push origin main 0.1.1
   ```

4. `release.yml` 工作流会自动创建 Draft Release 并附上 `manifest.json` + `theme.css`，
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

## Callout / 表格玻璃回归

- 桌面、手机和平板尺寸，浅色/深色，分别检查阅读视图与实时预览。
- 覆盖普通表格、callout 内表格、嵌套 callout、折叠/展开、未知类型和自定义完整颜色。
  阅读侧不应泛白，callout 外侧阴影不被裁切；表头渐变保留且不再叠实色，悬停仍有轻染。
- 检查标题/图标类型色、表格外框和内部格线、正文斑马纹、左中右对齐、宽表横向滚动，
  以及实时预览中的单元格编辑/选择；普通 HTML 和嵌入内容不应被整体隔离。
- 开启 `ob-solid` 和系统减少透明度，callout 渐变、阴影、模糊应退场，类型色和边框仍有效。
- 对比编辑视图修改前后的背景、色晕、缘光、模糊和表头；类型色格式修复会恢复原生
  标题/图标和块内表格配色，但不应重调玻璃材质。桌面浏览器回归不能代替移动 WebKit 真机目检。

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
  用 `--ob-callout-*` 的顶部高光弧、右下类型色晕与底部色缘模拟玻璃厚度。类型色只允许
  出现在缘光、图标和标题，不要把类型色的透明混合写回整块
  `background-color`——青+粉会互相抵消成灰卡。`ob-solid` 与
  `prefers-reduced-transparency` 已显式清掉 `background-image` / `box-shadow`。
- **Callout 颜色变量契约**：`--callout-color` 必须是完整 CSS 颜色（如 `rgb(62 113 104)`），
  与当前原生标题、图标、Bases 和表格 `color-mix()` 共用；逗号三元组会让原生声明失效，
  甚至使块内表格边框变成 `none`。透明度用
  `color-mix(in srgb, var(--callout-color) 25%, transparent)`，不要再套 `rgb(var(...), …)`。
  内置类型保留原 RGB 值及各处混合比例，未知类型沿用原生默认色；自定义类型也应提供完整颜色。
- **阅读视图绘制边界**：实时预览的 CM widget 有原生 `contain: paint`，阅读视图没有。
  浅色原生 callout 的混合会因此与整张笔记合成，呈现白雾；仅对阅读视图中直接包含 callout
  的 `.el-div` 使用 `isolation: isolate`，不隔离整个 preview sizer 或所有 HTML 块，
  也不用会裁掉外侧阴影的 `contain: paint`。该 `:has(> .callout)` 只检查原生块包装的
  直接子级，局部豁免 stylelint 的 `:has` 警告，不扩展为全页面后代搜索。
- **阅读表头叠底**：原生 `thead tr` 的实色会盖住 `th` 的透明渐变。只清除阅读视图的
  行底色，悬停时使用 7% 强调色；不重置所有 `tr`/`td`，以保留正文斑马纹、对齐和选择。
  透明问题的修复不改实时预览的单元格编辑控件与滚动；共同视觉细节由下述薄晶外观规则负责。
- **樱色薄晶表格**：普通笔记表格的外观规则限于阅读/实时预览，排除 `.dataview` 与
  `.table-view-table`；不改 Bases 数据表。强调色优先使用 callout 类型色，否则使用主题强调色。
  表头首格的 3px 书签是 inset 阴影，不加粗实际边框，避免扰动原生选择框、列宽与拖拽几何；
  RTL 表格将书签移到右侧。12px 圆角与 widget 外包装保持一致，行渐变必须透明。
  阅读/实时预览 callout 的渲染单元格与原生表格编辑器 `.table-cell-wrapper` 使用相同留白，
  但实时预览表格 widget 的 `th`/`td` 本体仍须保持原生零 padding；水平留白用 `clamp()` 随窄屏收紧，避免两字表头挤成竖排。
  不可覆盖选择/拖拽的伪元素，也不引入动画或强制列对齐。
  对比材料背景/滤镜不回归；检查手机窄屏滚动、浅深色和减少透明度。
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
