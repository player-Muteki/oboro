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
  出现在缘光、图标和标题，不要把 `rgb(var(--callout-color), …)` 写回整块
  `background-color`——青+粉会互相抵消成灰卡。`ob-solid` 与
  `prefers-reduced-transparency` 已显式清掉 `background-image` / `box-shadow`。
- **逗号三元组颜色变量**：`--callout-color` 的值是 `"r, g, b"` 逗号三元组，
  `rgb(var(--callout-color) / 25%)`（斜杠+逗号混合）在 Chromium **非法会被整条丢弃**；
  必须写 `rgb(var(--callout-color), 0.25)`（逗号记法，实测有效）。
- **backdrop-filter 包含块陷阱**：带 `backdrop-filter` 的元素会成为其**绝对定位后代**的
  包含块。侧栏开关按钮（`.sidebar-toggle-button`）在 DOM 里是 Ribbon 的后代——曾因给
  Ribbon 加模糊导致按钮被"搬位"到标签栏下方。因此：**Ribbon 永远不加 backdrop-filter**；
  给含原生浮件（absolute 定位 UI）的容器加模糊前，务必 A/B 实测按钮位置
  （摘除主题 style 标签前后对比 `getBoundingClientRect()`）。
