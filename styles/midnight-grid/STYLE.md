# 午夜網格（Midnight Grid）

id: midnight-grid
適合：科技講解、AI 和軟體話題、圖表、流程。
氣質：深藏青、安靜的點陣網格，由一抹乾淨的藍來說話。
參考作品：styles/midnight-grid/index.html（12 s，循環）
畫廊影片：gallery/videos/midnight-grid.mp4

## 配色 (hex)
- 底色：#0B1220
- 圓點：#1E2A44（40 px 網格上的 2 px 圓點）
- 面板：#111A2E，2 px 邊框 #22304D（連線 3 px）
- 文字：#E8EDF7
- 弱化文字：#8C98B3
- 強調色：#3D8BFF（唯一的藍，只用在當前啟用的東西上）

## 字型
- 展示字：Inter 700，字距 -0.03em
- 標籤：Inter 500，28 px
- 程式碼或數字：JetBrains Mono 500
- 字型連結（貼上到 <head>；所有字型均免費）：
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500&display=swap">
  （參考作品只用 Inter，所以只連結了 Inter）
- 中文文字用 Noto Sans TC（無襯線），從 Google Fonts 引入，因為拉丁字型沒有中文字形：`<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@500;700&display=swap">`

## 緩動 (數值)
- 落定：power3.out，0.5 s（15 幀）
- 移動：power3.inOut，0.8 s
- 連一條線：power2.inOut，0.6 s
- 離場：power2.in，0.3 s
- 錯開：0.05 s

## 動效規則
- 圖表逐個節點搭建。畫一條線，然後下一個節點落下。
- 當前啟用的節點拿到藍色。舊節點回到弱化色。
- 鏡頭像平穩的幻燈片一樣在網格上平移，絕不甩鏡。

## 標誌動作
- 每條連線描畫時，一個藍色脈衝騎線上端，然後把藍色交給它抵達的節點。
- 節點從輸入一側擦入並短距離滑動落下；標籤在 0.1 s 後透過遮罩升起。
- 鏡頭一次停留一個節點間距；平移途中點陣網格稍微滯後，然後落回網格對齊。
- 結尾流程倒放：節點倒序離場，連線縮回它們的源頭。

## 網格
點陣網格 40 px。每個方框都吸附到網格上。安全邊距 96 px。

## 帶素材
- 把截圖或片段放進節點面板：同樣的 #111A2E 填充、1 px #22304D 邊框、16 px 圓角，吸附到網格。
- 讓素材保持平靜、略暗，讓藍色強調色依然勝出。不要加偏紫或偏青的調色。
- 當前啟用的素材面板拿到藍色邊框。其他保持弱化。
- 用與節點相同的擦入方式顯露素材。絕不放進漂浮的玻璃卡片。

## 停用清單
- 輝光、泛光、鏡頭光暈、霓虹邊
- 紫到藍的漸變
- 帶模糊的玻璃卡片
- 假的 HUD 圓環、假時間碼、角落標籤
