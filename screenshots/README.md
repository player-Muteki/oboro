# Preview assets / 截图与配图

Updated **2026-11-01**, for **Oboro 0.3.2**.

## What is shown

- `screenshot-light.png` / `screenshot-dark.png`: actual **Obsidian 1.14.5** captures of
  an isolated demonstration vault, with two notes in reading view. No private notes are shown.
- `promo.png`: an editorial composition of those captures and crops of their table, callout
  and code block. UI pixels are not repainted or replaced with mockups.
- `scrollbar-detail.png`: the actual scrollbar SVG master rendered in all four theme palettes,
  **enlarged 3.5×**. This is an artwork study, **not** an application screenshot, not the actual
  scrollbar size and not a demonstration of thumb movement or its end fades.
- `capture.json`: capture dimensions, typography, glass parameters and crop rectangles in
  CSS pixels. The composition script uses these instead of guessing coordinates.

## Capture configuration / 截图配置

The demonstration vault uses the released `theme.css` and `manifest.json`, plus
**Style Settings 1.0.9**. Only the theme's `oboro@@…` settings were copied from the daily vault;
no unrelated plugins, notes or dashboard snippets were copied.

| Setting | Value |
| --- | --- |
| Main panel opacity / 主面板实度 | 80% |
| Sidebar opacity / 侧栏实度 | 72% |
| Solid mode / 实色模式 | Off |
| Glass saturation / 玻璃饱和度 | 170% |
| Glass brightness / 玻璃亮度 | 108% |
| Glass blur / 玻璃模糊 | Theme default, 18px |
| Interface and text font / 界面与正文字体 | Noto Serif CJK SC, Lora |
| Monospace font preference / 等宽字体首选 | Cascadia Code |
| Text size / 正文字号 | 23px |
| Custom accent / 自定义强调色 | `#c08890` |
| CSS viewport | 2048 × 1232 |
| Device scale | 1.25 |
| Export size | 2560 × 1540 PNG |

Both modes use the corresponding sakura wallpaper from the user's daily vault. Backgrounds
are provided through `--dv-light-bg` / `--dv-dark-bg`, not by changing the theme. Their original
image files are **not bundled or redistributed** in this repository. These previews therefore
show a configured appearance, not the out-of-the-box wallpaper-free appearance.

Capture through Obsidian's `dev:cdp method=Page.captureScreenshot`: the ordinary
`dev:screenshot` command can temporarily hide scrollbars. Check the target vault **before every
capture or configuration change**, allow repainting, and clear temporary viewport emulation
when finished. Desktop captures do not replace iPad/mobile WebKit testing.

## Rebuild the composed artwork / 重建配图

Dependencies: Python 3 with **Pillow**, **Fontconfig**, **Inkscape**, and the
**EB Garamond**, **Noto Sans** and **Noto Serif CJK SC** fonts. These are documentation tools,
not theme runtime requirements.

```sh
python3 scripts/build-promo.py
```

Inputs: the two real screenshots, `capture.json`, and `scripts/assets/scrollbar-art.svg`
with its palette mappings in `scripts/scrollbar_art.py`. Outputs: `promo.png` and
`scrollbar-detail.png`. The script does not launch Obsidian or modify any vault.

For a future capture, update both screenshots and `capture.json` together, then rebuild.
Do not relabel an old capture with a new version without actually updating the installed theme.
