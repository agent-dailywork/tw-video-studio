#!/usr/bin/env bash
# new_project.sh：新建一個 HyperFrames 專案。
# 用法：bash scripts/new_project.sh <dir> [16x9|9x16] [seconds] [style id]
# 如果給的風格 id 帶參考作品（styles/<id>/index.html），專案會從這份作品的副本開始，
# 你只需改文字、顏色和節奏，不必從零做起。
set -e
HERE=$(cd "$(dirname "$0")/.." && pwd)
DIR=${1:?用法：new_project.sh <dir> [16x9|9x16] [seconds] [style id]}
FMT=${2:-16x9}; SEC=${3:-9}; STYLE=${4:-}
if [ -e "$DIR/index.html" ]; then echo "$DIR 裡已經有 index.html。請換一個新資料夾。"; exit 1; fi
mkdir -p "$DIR/media"
cp "$HERE/templates/motion/"{index.html,studio.js,hyperframes.json,meta.json} "$DIR/"
if [ -n "$STYLE" ]; then
  [ -f "$HERE/styles/$STYLE/STYLE.md" ] || { echo "沒有叫 $STYLE 的風格。請在 $HERE/styles/ 裡檢視。"; exit 1; }
  cp "$HERE/styles/$STYLE/STYLE.md" "$DIR/STYLE.md"
  if [ -f "$HERE/styles/$STYLE/index.html" ]; then
    cp "$HERE/styles/$STYLE/index.html" "$DIR/index.html"
    if [ -f "$HERE/styles/$STYLE/studio.js" ]; then cp "$HERE/styles/$STYLE/studio.js" "$DIR/studio.js"
    elif ! grep -q 'studio.js' "$DIR/index.html"; then rm -f "$DIR/studio.js"; fi
    PW=$(grep -oE 'data-width="[0-9]+"' "$DIR/index.html" | head -1 | grep -oE '[0-9]+')
    PH=$(grep -oE 'data-height="[0-9]+"' "$DIR/index.html" | head -1 | grep -oE '[0-9]+')
    PD=$(grep -oE 'data-duration="[0-9.]+"' "$DIR/index.html" | head -1 | grep -oE '[0-9.]+')
    if [ "$FMT" = 9x16 ]; then WW=1080; WH=1920; else WW=1920; WH=1080; fi
    echo "新專案：${DIR}，從 $STYLE 的參考作品開始（${PW} x ${PH}，${PD} 秒）。"
    if [ "$PW" != "$WW" ] || [ "$PH" != "$WH" ]; then
      echo "警告：你要的是 $WW x ${WH}，但這份作品是 $PW x ${PH}。請按 $WW x $WH 重新排版畫面"
      echo "      （改 data-width/data-height、viewport 和頁面尺寸，再把所有元素重新擺放）。絕不能直接裁切。"
    fi
    if [ "$PD" != "$SEC" ] && [ "$PD" != "$SEC.0" ]; then
      echo "警告：你要的是 $SEC 秒，但這份作品是 $PD 秒。請修改 data-duration，並重新安排各個節拍的時間。"
    fi
    exit 0
  fi
fi
if [ "$FMT" = 9x16 ]; then W=1080; H=1920; else W=1920; H=1080; fi
# 在模板裡設定尺寸和時長
sed -i.bak -e "s/width=1920, height=1080/width=$W, height=$H/" \
  -e "s/width: 1920px; height: 1080px/width: ${W}px; height: ${H}px/g" \
  -e "s/data-duration=\"9\"/data-duration=\"$SEC\"/" \
  -e "s/data-width=\"1920\" data-height=\"1080\"/data-width=\"$W\" data-height=\"$H\"/" "$DIR/index.html"
rm -f "$DIR/index.html.bak"
echo "新專案：${DIR}（$W x ${H}，$SEC 秒）。編輯 $DIR/index.html，然後執行：bash $HERE/scripts/stills.sh $DIR"
