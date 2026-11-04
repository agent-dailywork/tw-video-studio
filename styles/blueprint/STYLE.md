# 藍圖（Blueprint）

id: blueprint
參考作品：styles/blueprint/index.html（12 s，循環）
畫廊影片：gallery/videos/blueprint.mp4
適合：工作原理、產品部件、工程、分步講解。
氣質：一張自己逐線繪製出來的技術圖紙。

## 配色 (hex)
- 底色：#0E3A66
- 線條：#CFE3F7（2 px 描邊）
- 淡網格：#1C4D80
- 文字：#EAF3FC
- 強調色：#FFD23F（唯一的高亮：最關鍵的那個部件）

## 字型
- 標籤：IBM Plex Mono 500，26 到 32 px，全大寫，字距 0.06em
- 大數字：IBM Plex Mono 700
- 字型連結：
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500;700&display=swap">
- 中文文字用 Noto Sans TC（無襯線），從 Google Fonts 引入，因為拉丁字型沒有中文字形：`<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@500;700&display=swap">`

## 緩動 (數值)
- 描一筆：power1.inOut，0.6 到 1.2 s（stroke-dashoffset）
- 尺寸箭頭：expo.out，0.5 s
- 鏡頭：power2.inOut，1.0 s 平移

## 動效規則
- 一切先以描邊畫出，之後（如果需要）再填充。
- 標籤出現時帶一條引線，從部件畫向標籤。
- 只有強調部件填充黃色。

## 標誌動作
- 輔助線先橫掃整張圖紙，真正的線條沿著它們描出，然後輔助線淡出。
- 爆炸檢視：部件沿一條軸滑開，帶小幅錯開和阻尼回穩。內部部件滯後。
- 隱藏線：被包在另一個部件裡的部件畫成虛線，一旦露出立刻變成實線。
- 尺寸線從數字處向外生長，箭頭騎線上端。
- 關鍵部件自下而上擦入黃色填充，它的標籤變黃，鏡頭推近它。

## 網格
細網格 24 px，粗網格 120 px。邊距 96 px。
向內 48 px 處有一道細圖框，帶角標、比例尺和一個空白標題欄。
網格以鏡頭 30% 的速度移動，形成視差。

## 帶素材
- 照片不要放進圖紙本身。
- 照片可以放在圖紙旁邊，用同樣 2 px 的線畫出直角邊框，調成冷藍雙色調。
- 或者從照片裡描出物體，然後在一筆描線上從照片切到圖紙。

## 停用清單
- 圖紙內部出現照片
- 柔和陰影、輝光
- 圓潤可愛的字型
- 同時出現多於一個高亮
