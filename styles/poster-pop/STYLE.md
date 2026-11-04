# 海報爆破（Poster Pop）

id: poster-pop
適合：開頭鉤子、Shorts、大膽主張、倒計時、「3 件事」清單。
氣質：一張響亮的演出海報。巨大的窄體字、平塗色、硬切。
參考作品：styles/poster-pop/index.html（12 s，循環）
畫廊影片：gallery/videos/poster-pop.mp4

## 配色 (hex)
- 底色：#FFD400（黃）
- 墨色：#111111
- 紙白：#FFFFFF（用於卡片和鏤空文字）
- 強調色：黃底上的 #111111 就是強調色。沒有其他顏色。

## 字型
- 展示字：League Gothic，全大寫，字距 0.01em，行高 0.85
- 主詞：畫面高度的 50% 到 90%
- 輔助字：Archivo Black，40 px 或更大
- 字型連結（貼上到 <head>；所有字型均免費）：
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=League+Gothic&family=Archivo+Black&display=swap">
- 中文文字用 Noto Sans TC（無襯線），從 Google Fonts 引入，因為拉丁字型沒有中文字形：`<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@900&display=swap">`

## 緩動 (數值)
- 砸入：power4.out，0.2 s
- 縮放衝擊：在拍上 1.0 到 1.06 再回 1.0。0.05 s 內放大，0.4 s 內回落（sine.inOut）。回得更快會看起來像閃光。
- 離場：power3.in，0.2 s
- 每 0.5 到 1.0 s 切一次

## 動效規則
- 每拍一個詞或數字。在拍上切。
- 文字從畫面外砸入，戛然停住。
- 用滿整個畫面。故意讓字母被邊緣裁掉。

## 標誌動作
- 大到裝不下海報的詞：主詞和數字佔畫面高度的 80% 到 150%，被兩條邊裁掉。
- 字母砸入：字母一個接一個到達，間隔 0.033 s，戛然停住。拉鏈版本讓奇數位字母從上方來、偶數位字母從下方來。
- 底色翻轉：一次硬切交換黃色底和墨色，讓文字變成墨底黃字。
- 紙卡：一張白卡橫砸過巨大的數字，2 幀後卡上的 Archivo Black 詞從卡片邊緣內升起。
- 落地震動：一個詞砸中時整張海報下沉 18 px，0.15 s 內回穩。

## 網格
主詞沒有邊距。輔助文字邊距 64 px。

## 帶素材
- 照片和片段放在紙卡或硬邊矩形遮罩裡。不要圓角。
- 調成高對比黑白，讓黃色始終是唯一的顏色。
- 像切詞一樣在拍上切素材。絕不淡入。

## 停用清單
- 漸變、陰影、輝光
- 小字
- 螢幕上超過 3 個詞
- 柔和緩慢的淡化
