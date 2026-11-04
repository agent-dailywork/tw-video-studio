#!/usr/bin/env bash
# doctor.sh：檢查本 skill 需要的工具。每缺一個工具，印出一條修復命令。
# 用法：bash scripts/doctor.sh [motion|media]
MODE=${1:-motion}
ok=1
say() { printf '%-10s %s\n' "$1" "$2"; }

if command -v node >/dev/null; then
  v=$(node -p 'process.versions.node.split(".")[0]')
  if [ "$v" -ge 22 ]; then say node "正常 ($(node -v))"; else say node "版本太舊 ($(node -v))。修復：從 https://nodejs.org 安裝 Node 22 或更新版本"; ok=0; fi
else say node "缺失。修復：從 https://nodejs.org 安裝 Node 22 或更新版本"; ok=0; fi

for t in ffmpeg ffprobe; do
  if command -v $t >/dev/null; then say $t 正常; else say $t "缺失。修復：brew install ffmpeg"; ok=0; fi
done

if command -v python3 >/dev/null; then say python3 "正常"; else say python3 "缺失。修復：brew install python"; ok=0; fi

if [ "$MODE" = media ]; then
  if [ -n "$HIGGSFIELD_API_KEY" ] || [ -n "$HF_API_KEY_ID" ] || grep -qs '^HIGGSFIELD_API_KEY=' .env; then
    say higgsfield "已找到金鑰（不顯示）"
  else
    say higgsfield "沒有金鑰。在這個資料夾裡建一個名為 .env 的檔案，只寫一行：HIGGSFIELD_API_KEY=your_key_id:your_key_secret（在 https://console.higgsfield.ai 獲取）。千萬不要把它貼到聊天裡。"
  fi
fi

[ $ok = 1 ] && echo "就緒" || { echo "請先修好上面幾行，再執行一次"; exit 1; }
