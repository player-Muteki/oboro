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
- **backdrop-filter 包含块陷阱**：带 `backdrop-filter` 的元素会成为其**绝对定位后代**的
  包含块。侧栏开关按钮（`.sidebar-toggle-button`）在 DOM 里是 Ribbon 的后代——曾因给
  Ribbon 加模糊导致按钮被"搬位"到标签栏下方。因此：**Ribbon 永远不加 backdrop-filter**；
  给含原生浮件（absolute 定位 UI）的容器加模糊前，务必 A/B 实测按钮位置
  （摘除主题 style 标签前后对比 `getBoundingClientRect()`）。

