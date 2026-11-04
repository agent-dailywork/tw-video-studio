#!/usr/bin/env bash
# render.sh：把專案渲染成 MP4。
# 用法：bash scripts/render.sh <project dir> <out.mp4> [draft|high] [composition.html]   （HF_WORKERS=2 可限制 CPU 佔用）
set -e
HF="npx --yes hyperframes@${HF_VERSION:-0.8.181}"
DIR=$(cd "${1:?用法：render.sh <dir> <out.mp4> [draft|high]}" && pwd)
OUT=${2:?需要輸出路徑}; Q=${3:-draft}; C=${4:-}
case "$OUT" in /*) ;; *) OUT="$PWD/$OUT";; esac
mkdir -p "$(dirname "$OUT")"
ARGS=(render "$DIR" -o "$OUT" -q "$Q" -w "${HF_WORKERS:-auto}" --quiet)
[ -n "$C" ] && ARGS+=(-c "$C")
$HF "${ARGS[@]}"
ffprobe -v error -show_entries format=duration:stream=width,height -of compact=p=0 "$OUT" | tr '\n' ' '; echo
echo "已渲染：$OUT ($(python3 -c "import os;print(round(os.path.getsize('$OUT')/1e6,1))") MB)"
