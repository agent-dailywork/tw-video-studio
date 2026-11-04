# 社論紙面（Editorial Paper）

id: editorial-paper
適合：資料、圖表、講解、「數字在說什麼」。
氣質：一張活過來的報紙圖表。暖色紙張、黑色墨水、一抹藍。
參考作品：styles/editorial-paper/index.html（10 s，循環）
畫廊影片：gallery/videos/editorial-paper.mp4

## 配色 (hex)
- 底色：#FFF1E5（鮭魚色紙）
- 墨色：#1A1A1A
- 分隔線和網格線：#E3D3C3
- 弱化文字：#6B5E55
- 強調色：#0F5499（最關鍵的那條線、那根柱或那個數字）

## 字型
- 標題：Playfair Display 700，字距 -0.02em
- 數字：Playfair Display 900，等寬數字
- 標籤：Inter 500，26 到 32 px
- 字型連結（貼上到 <head>；所有字型均免費）：
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:wght@700;900&display=swap">
- 中文文字：標題和數字用 Noto Serif TC（襯線），標籤用 Noto Sans TC（無襯線），從 Google Fonts 引入，因為拉丁字型沒有中文字形：`<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@700;900&family=Noto+Sans+TC:wght@500&display=swap">`

## 緩動 (數值)
- 落定：power3.out，0.7 s（21 幀）
- 畫線：power2.inOut，1.2 到 2.0 s
- 數字計數：power2.out，時長與它同步的那條線相同
- 離場：power2.in，0.4 s

## 動效規則
- 線條從左到右畫出。數字同步向上計數。
- 鏡頭可以縮放圖表（改變座標軸），絕不晃動。
- 可以有細膩的紙張顆粒。保持靜止或非常緩慢。

## 標誌動作
- 一根柱子變藍，然後長過其餘柱子。它的數字同步計數。
- 座標軸拉遠以容納領先者。網格線滑動，新的一條進入。
- 平滑的重新排名：藍色那一行攀升，其他行緊隨其後依次下移。
- 聚焦：其他柱子淡成分隔線的顏色，讓藍色那根獨自突出。
- 標題在一條短墨條下透過遮罩逐詞替換。

## 網格
12 欄，邊距 120 px，欄間距 32 px。圖表立在清晰的基線上。

## 帶素材
- 照片放在網格上的硬邊矩形裡，不要圓角，不要陰影。
- 把照片調成偏暖、略平的色調，讓它融入紙面。絕不出現純黑。
- 上方一條細墨線，下方一行 Inter 500 弱化色的說明文字。
- 圖表或數字始終是主角。照片只是輔助，最多佔半個畫面。

## 停用清單
- 3D 圖表、超過 3 塊的餅圖
- 霓虹、輝光、柱子上的漸變
- 螢幕上的來源行或小號腳註
- 多於一種強調色
