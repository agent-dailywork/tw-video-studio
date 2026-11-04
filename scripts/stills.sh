#!/usr/bin/env bash
# stills.sh：第 5 招。在完整渲染之前，先在鏡頭切換點截幾張靜幀。
# 用法：bash scripts/stills.sh <project dir> [時間點，逗號分隔]   例如 0,3,6
# 不給時間點時，取 0、三分之一、三分之二和結尾。
set -e
HF="npx --yes hyperframes@${HF_VERSION:-0.8.181}"
DIR=$(cd "${1:?用法：stills.sh <dir> [t1,t2,t3]}" && pwd)
D=$(grep -oE 'data-duration="[0-9.]+"' "$DIR/index.html" | head -1 | grep -oE '[0-9.]+')
AT=${2:-$(python3 -c "d=$D; print(','.join(str(round(x,2)) for x in (0, d/3, 2*d/3, d-0.05)))")}
OUT="$DIR/stills"; rm -rf "$OUT"; mkdir -p "$OUT"
$HF snapshot "$DIR" --at "$AT" --no-end -o "$OUT" >/dev/null
# 生成小尺寸副本，方便檢視
for f in "$OUT"/*.png; do ffmpeg -v error -y -i "$f" -vf scale=960:-2 -q:v 7 "${f%.png}.jpg"; done
# 再拼一張小的總覽圖（看圖工具常常拒絕開啟大檔案）
[ -f "$OUT/contact-sheet.jpg" ] && ffmpeg -v error -y -i "$OUT/contact-sheet.jpg" -vf scale=1400:-2 -q:v 8 "$OUT/peek.jpg"
ls "$OUT"/*.jpg
echo "逐張看這些靜幀，把不對的地方改好，然後再執行 render.sh。"
