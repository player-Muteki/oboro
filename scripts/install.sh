#!/usr/bin/env bash
# 将主题安装/更新到指定 vault 的主题目录
# 用法: ./scripts/install.sh <vault路径> [配置目录名，默认 .obsidian]
set -euo pipefail

VAULT="${1:?用法: install.sh <vault路径> [配置目录名 默认 .obsidian]}"
CFG="${2:-.obsidian}"
SRC="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$VAULT/$CFG/themes/Sakura Macaron"

if [ ! -d "$VAULT/$CFG" ]; then
  echo "错误: 配置目录 $VAULT/$CFG 不存在（检查是否应为 .obsidian_pc / .obsidian_linux）" >&2
  exit 1
fi

mkdir -p "$DEST"
cp "$SRC/manifest.json" "$DEST/"
cp "$SRC/theme.css" "$DEST/"
echo "已安装到: $DEST"
echo "在 Obsidian 设置 → 外观 → 主题 中选择 Sakura Macaron；若已选中，Ctrl/Cmd+P 运行「重新加载」即可热更新。"
