# 15 秒穿越 30,000 年（30,000 years in 15 seconds）

id: time-travel
適合：一個想法的歷史、「過去 vs 現在」、演化故事、時間軸、起源故事。
氣質：史詩而溫暖；一台鏡頭沿一條無盡的時間軸穿越每個時代，每個時代都用它自己的時代風格繪製。
參考作品：styles/time-travel/index.html（17 s，不循環）
畫廊影片：gallery/videos/time-travel.mp4

## 配色 (hex)
- 底色：墨色 #15120F
- 文字和時間軸：象牙白 #F3EEE4（唯一永不改變的東西；它把所有時代串在一起）
- 洞穴：赭石 #C86E3C，配暖色岩石
- 陶瓶：赤陶 #B95F35，高光 #D88B5C，黑釉 #17110E
- 西洋鏡（zoetrope）：黃銅 #C9A15A，配奶油色紙
- 膠片：銀 #C8C8C4
- 電視：胡桃木 #4A2B18，熒光 #78C8F0
- 8 位像素：夜 #0E0B24、#2A1D5C，草 #5BBF5A，磚 #B4532A，金 #F2C14E
- 每個時代有自己的配色；象牙白是所有時代唯一共享的顏色

## 字型
- 年份標籤：每個用它所在時代的字型，38 到 44 px，字距 2 到 6 px
  - 30,000 BC：Libre Baskerville · 500 BC：Tenor Sans · 1834：Bodoni Moda
  - 1895：Playfair Display 斜體 · 1951：Jost 500 · 1980：用程式碼畫的像素字型 · 2026：JetBrains Mono
- 程式碼行：JetBrains Mono 400，58 px
- 螢幕上最多兩個詞：年份，以及最後一個時代裡的程式碼行。
- 字型連結（貼上到 <head>；所有字型均免費）：
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:wght@400&family=JetBrains+Mono:wght@400&family=Jost:wght@500&family=Libre+Baskerville&family=Playfair+Display:ital,wght@1,400&family=Tenor+Sans&display=swap">
- 中文文字按時代選：襯線時代（30,000 BC、1834、1895）用 Noto Serif TC（襯線），無襯線時代（500 BC、1951、2026）用 Noto Sans TC（無襯線），從 Google Fonts 引入，因為拉丁字型沒有中文字形：`<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400&family=Noto+Sans+TC:wght@400;500&display=swap">`

## 緩動 (數值)
- 時代穿越：power4.inOut，每次切換 0.5 s（拍前 0.24 s 到拍後 0.26 s）
- 切換前推進：power3.in，約 0.55 s
- 揭示和轉向：power3.inOut，0.3 到 0.45 s
- 排隊落定：expo.out，0.4 s，錯開 0.035 s
- 跑步循環：每秒 1.5 步，所有時代共用一個時鐘
- 每次切換的曝光衝擊：0.35 s 淡出，7% 暖白

## 動效規則
- 一個跑者是每個時代的主角：同一副骨架，同一個相位時鐘。只有畫法改變。
- 每個時代在運動中變成下一個，按形狀匹配（陶瓶變鼓，縫隙變齒孔，螢幕變電視）。
- 每次切換落在 0.5 s 的拍上。
- 年份標籤騎在時間軸上，鏡頭快速移動時帶著殘影拖尾。
- 處處有質感：顆粒、暗角、火光閃爍、光束裡的灰塵。
- 鏡頭從不停下；它推進一個細節，然後順著這個運動切換。

## 標誌動作
- 匹配剪輯鏈：洞穴野牛到陶瓶到西洋鏡到膠片到電視到像素到程式碼。
- 打出 `draw(frame + 1)`，然後程式碼把跑者畫成一條象牙白線。
- 終章：七個跑者在一條傾斜的時間軸上排成一排，步調一致地奔跑。

## 構圖
- 全畫面，一次一個時代，主角居中。
- 象牙白時間軸低低地橫在 y 996，每 24 px 一個刻度；年份在它上方靠左。
- 終章時間軸向右上傾斜；過去小而遠，現在大而近。

## 帶素材
- 渲染器裡 canvas 無法繪製影片幀，所以要分層：底層背景 canvas，然後每幀用 CSS（position、transform、clip-path、filter）擺放的 video 元素，再上面是一層疊加 canvas，用於顆粒、劃痕、掃描線、標籤和時間軸。
- 把每個片段調成它所在時代的樣子。1895 膠片：grayscale、sepia 0.28、contrast 1.38、blur 0.6 px、閃爍、片門晃動、劃痕、灰塵。1951 電視：grayscale、sepia 0.32、hue-rotate 168 deg、saturate 0.55、contrast 1.3、彎曲掃描線、圓角、玻璃高光。
- 現代可以是一個真人全螢幕奔跑，然後縮成一張圓角卡片，作為第七個跑者。絕不在人臉上畫圖形。
- 人物預設用使用者自己的素材（`assets/me/`，命名規則見其中的 README.md）：`assets/me/p1.png`–`p5.png`（已去背景）、`assets/me/photo1.jpg`–`photo5.jpg`（原圖）、`assets/me/webcam.mp4`（口播片段）、`assets/me/ai-walk.mp4`（AI 走路片段）、`assets/me/ai-turn.mp4`（AI 轉身片段）。文字絕不壓在臉上。

## 停用清單
- 所有時代用同一種字型
- 沒有質感的乾淨扁平向量風格
- 沒有按形狀或運動匹配的硬切
- 螢幕上超過兩個詞
- 破壞時代感的顏色（洞穴裡不要霓虹，8 位像素裡不要棕褐色）
