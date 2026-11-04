---
name: tw-video-studio
description: TW 影片工作室（基於 Claude Video 2.0 與 Harry 中文版改寫的台灣繁體中文版）。用 Claude Code 免費做出工作室級的動態圖形：先開啟有 21 種風格、每格都是真實影片的風格畫廊讓使用者挑選，問 5 個簡短問題，再用程式碼製作（HTML + GSAP，用 HyperFrames 渲染成 MP4）。可以是純圖形、放使用者自己的照片和影片（預設素材在 assets/me/），或用 fal.ai（優先）或 Higgsfield 生成的 AI 片段（先給分鏡表和報價，等明確的「yes」才花錢）。繁體中文字型、台灣用語、直式短影音安全區都已內建。每支片都從真實畫面檢查：3 張靜幀確認、節奏檢查、循環片的像素級循環檢查。當有人說「做個動態圖形」「做個片頭」「把這個動起來」「做個循環動畫」「做個標題卡」「用我的照片做動畫」「把我的照片變成影片」「做個 Reels / Shorts / TikTok 廣告」「根據這支影片做動畫」「Claude Video」，或 make me a motion graphic / make a video intro / animate this / make a loop / make a title card / "/tw-video-studio" 時使用。
---

# TW 影片工作室（台灣繁體中文版）

三個階段：**A. 選風格**（風格畫廊）→ **B. 五個問題** → **C. 製作**（分鏡表、靜幀、渲染、檢查）。
每一步都遵守 `references/hacks.md` 裡的 5 個技巧：只用一種風格、用真實參考、簡報寫成數字、一個循環時鐘、看畫面而不是看程式碼。

下文的 `$SKILL` 指這個 skill 的資料夾（通常是 `~/.claude/skills/tw-video-studio`）。
每支片新建一個工作資料夾（例如 `./video-<短名>/`），絕不在 `$SKILL` 裡面製作。

## 語言

- 和使用者溝通一律用**台灣繁體中文**與台灣慣用語：影片（不是視頻）、字型、預設、資料夾、專案、短影音、品質、螢幕、點數。
- 畫面上的中文文字也一律用繁體字與台灣用語，標點用全形（，。、「」『』！？）。
- 使用者給的是簡體文字時，先轉成台灣繁體再用（見下方「簡轉繁」），除非他明確要簡體。

## 使用者的預設素材

`$SKILL/assets/me/` 放使用者自己的素材（照片、去背人像、口播、AI 片段），格式和命名見 `assets/me/README.md`。
- 資料夾是空的：需要人物時就請使用者提供素材，或改用純圖形。
- 資料夾裡有檔案：使用者沒給別的素材時，預設用這些。用之前先讀 `assets/me/README.md` 了解每個檔案是什麼。
- 用到人臉時：絕不讓文字或圖形蓋住臉。

## 開始之前

先跑一次 `bash $SKILL/scripts/doctor.sh`。最後一行是「就緒」才繼續；有缺的就把那一條修復指令給使用者，然後停下。

## 階段 A：選風格

1. 在背景啟動風格畫廊（用背景執行；它只在 127.0.0.1 上服務，90 分鐘後自動停止）：
   `python3 $SKILL/scripts/gallery.py`
   它會在瀏覽器裡開啟並印出網址。把網址也給使用者，以防沒自動開啟（只想要網址就加 `--no-open`）。選好後可以停掉，不停也會自己停。
2. 用一則簡短訊息說：
   「風格畫廊已經開啟：<網址>。每一格都是用程式碼做出來的真實影片。把格子切到『帶素材』，可以看到放進真實照片和畫面後的樣子。看中哪個就點『用這個風格』，把風格名稱貼回來；也可以直接貼 1 到 3 個你自己的參考連結或圖片。」
3. 使用者回覆後：
   - 風格 id（例如 `paper-world`）：讀 `$SKILL/styles/<id>/STYLE.md`。這份規範就是這支片的法則。
   - 他自己的參考：逐一查看（開啟連結、讀圖片）。在工作資料夾裡按 `$SKILL/references/style-format.md` 的格式寫一份新的 `STYLE.md`，寫清楚每個參考**是怎麼做出來的**（遮罩文字、慢鏡頭、長停頓），附 hex 色碼和緩動數值。用 5 行說明給他聽。
     如果參考是照片而不是動態作品（例如定裝照），就從照片裡提取背景、光線、服裝、姿勢，推出一套動態風格；同時問清楚這套風格要用在哪支片上。
   - 「你來選」：依主題挑最合適的風格，用一句話說明原因。

## 階段 B：五個問題

讀 `$SKILL/questions.md`，把兩條 `---` 之間的內容作為**一則**訊息原樣發出。
使用者已經說過的就跳過。「go」「開始」「預設」都算全部用預設值。只在需要時才用裡面的追問。

如果使用者給的是一段影片（例如他的口播），先把內容弄清楚再問問題：
- 先用 ffmpeg 抽一張縮圖總表（contact sheet）看畫面。
- 影片有人聲時，在本機轉寫：用 `mlx-whisper`（Apple 晶片，模型 `mlx-community/whisper-large-v3-turbo`），需要逐字時間就加 `word_timestamps=True`。
  **繁體輸出**：一定要帶 `language="zh"` 和 `initial_prompt="以下是台灣繁體中文的逐字稿，使用全形標點。"`；Whisper 還是可能吐出簡體字，所以轉完一律再跑一次 `opencc -c s2twp`（見下方「簡轉繁」）。
  第一次要裝在獨立的 venv 裡並下載約 1.5GB 模型，裝之前先告訴使用者。音訊不上傳。
- 有口誤、重來的地方，用逐字時間和靜音偵測（`silencedetect`）找剪輯點，剪成乾淨版本；剪輯點盡量藏在鏡頭離開人臉、或畫面轉場的時刻。

### 簡轉繁

用 OpenCC 的 `s2twp`（簡體 → 台灣正體，含台灣慣用詞）。
- 指令列：`brew install opencc`，然後 `opencc -c s2twp -i in.txt -o out.txt`。
- Python：在 venv 裡 `pip install opencc`，然後 `opencc.OpenCC('s2twp').convert(text)`。
轉完仍要看一遍：專有名詞、人名、品牌名可能被誤轉。

## 階段 C：製作

1. **把簡報寫成數字**（技巧 3）。在工作資料夾寫 `BRIEF.md`：尺寸（16:9 是 1920×1080，9:16 是 1080×1920）、時長、30 fps、是否循環、畫面上的原文、hex 配色（品牌色取代風格色，風格的規則不變）、字型和連結、緩動數值，以及永遠生效的禁用清單：
   不用會變色相的漸層；不用發光、泛光、鏡頭光暈；視線會跟隨的東西不用線性緩動；不要所有東西都置中；不要從 0 放大出現；畫面上同時最多 6 個英文字或 **12 個中文字**；只用一種強調色；不做假的介面外框。
   風格自己的招牌元素和這份清單衝突時（例如太陽的光暈、置中的小元件），以風格為準，它的畫廊影片就是證明。清單其餘部分照樣生效。

   **繁體中文字型與排版**（詳見 `$SKILL/references/hyperframes.md` 的「中文字型」）：
   - Switzer、Inter 等拉丁字型沒有中文字形。中文一律另外用 Google Fonts 的**繁體**字型，和其他字型一樣用 `<link>` 引入：
     無襯線用 **Noto Sans TC**，襯線用 **Noto Serif TC**，手寫溫暖感用 **LXGW WenKai TC**。
     **絕不用 Noto Sans SC / Noto Serif SC**：SC 是簡體字形，「骨、直、說、令」等字的寫法和台灣標準不同。
   - `font-family` 把拉丁字型放前面、TC 字型放後面，例如 `"Switzer", "Noto Sans TC", sans-serif`，讓英數字用拉丁字型。
   - 字距：中文用 `0` 到 `0.02em`，**不要用負字距**（不要照搬拉丁字的 -0.035em）。行高 1.3 到 1.5。
   - 不用斜體（CJK 沒有真斜體，只會被機器硬拉）。強調用字重、顏色或底線。
   - 中文文字容器加 `line-break: strict; word-break: normal;`，避免「，。、」出現在行首。大標題寧可手動斷行（`<br>`），按詞斷，不要讓一個詞被拆兩行。
   - 字幕和標題通常不加句尾句號；問號、驚嘆號保留。

   **直式（IG Reels / YouTube Shorts / TikTok）安全區**：上方約 200px、下方約 420px、右側約 120px 會被平台介面擋住。人臉、標題、@帳號都放在中間區域。
2. **分鏡表**。寫 `storyboard.json`（每個鏡頭的時間、圖形做什麼、用什麼素材：`code`、`user_photo`、`user_clip` 或 `generate`；參考 `$SKILL/examples/storyboard.json`）。執行
   `python3 $SKILL/scripts/storyboard.py storyboard.json`，把表格給使用者看。
   - 有任何 `generate`（AI 片段）時，依照 `$SKILL/references/media.md` 的「AI 片段計費順序」：
     1. **fal.ai（優先）**：用 fal 的 MCP 工具。先 `recommend_model` 挑模型，用 `estimate_cost`（或 `get_pricing`）報價；使用者的照片先用 `upload_file` 上傳拿到網址當參考圖。
     2. 沒連 fal MCP、或使用者指定時，才用 **Higgsfield**：`python3 $SKILL/scripts/higgsfield.py generate ... --out media/shotN.mp4 --yes`（API，金鑰在 `.env`），並先說明為什麼改用它。
     無論哪條路，都要先給出分鏡表和報價，**停下來等明確的「yes」**才花錢。生成後每段片段先看 3 幀再用。
   - 沒有 AI 片段時，給使用者看表格後直接繼續，除非他有意見。
3. **製作**。`bash $SKILL/scripts/new_project.sh <work>/proj 16x9|9x16 <秒數> <風格 id>`。
   風格有參考作品時，專案會從它複製開始：照簡報改文字、顏色、時間和尺寸（尺寸或時長不同時腳本會警告；那就重新排版，絕不直接裁切）。
   參考作品裡的英文文案換成中文時，記得同時加上 TC 字型連結、改字距（見上方），並重新檢查每行長度。
   沒有參考作品就從模板做。要循環但參考作品不循環時，照 `$SKILL/references/loops.md` 做。
   要緊的規則：
   - 所有動態只用一個時鐘（技巧 4）：`studio.js` 的 `STUDIO.play(t => render(t), { loop })`，或一條暫停的 GSAP 時間軸。同樣的時間進，同樣的畫面出：不用 Math.random（用 `STUDIO.rng`），不用 Date.now，不用計時器。
   - 字型：只用免費字型，每個都用 `<link>` 引入；只要有一個字型用了連結，所有字型都要連結（見 `$SKILL/references/hyperframes.md`）。
   - 起始狀態用 `gsap.set` 設定，不要寫在 CSS 的 `transform` 裡，否則會和 GSAP 的位移疊加（lint 會報 `gsap_css_transform_conflict`）。
   - 動態插入的 SVG／圖示只用自己寫死的字串，用 `insertAdjacentHTML` 或 DOM 方法，文字用 `textContent`。
   - 素材放進設計裡（遮罩、卡片、形狀裡），不放在看不清的文字下面，絕不蓋住臉。
   - 照片要去背時，在本機用 `rembg`（Python 3.12 的 venv，模型 `isnet-general-use`，約 170MB），裝之前先告訴使用者。
   - 使用者的照片和影片複製到 `<work>/proj/media/`，絕不移動或修改原檔。
4. **3 張靜幀給使用者確認**（技巧 5）。`bash $SKILL/scripts/stills.sh <work>/proj <t1>,<t2>,<t3>`，每張取在鏡頭切換後約 0.6 秒、東西都落定之後（自己檢查時可以多看幾張）。讀 `stills/peek.jpg`（沒有就自己用 ffmpeg 拼一張）。像嚴格的資深動態設計師一樣，給構圖、動態、文字、配色、創意各打 1 到 10 分。
   中文額外檢查：**字形是不是繁體 TC**（看「說」「骨」「直」）、有沒有標點落在行首、有沒有字被裁掉或擠在一起。
   修最差的 3 處，重複到全部 8 分以上。然後把 3 張靜幀和分數給使用者看，問：「可以渲染了嗎？」等他說可以（有意見就改、重出靜幀、再問）。
5. **渲染**。`bash $SKILL/scripts/render.sh <work>/proj <work>/out/draft.mp4 draft`。
   有人聲時，畫面渲染成無聲片，再用 ffmpeg 把音軌合進去：
   `ffmpeg -i draft-silent.mp4 -i media/voice.m4a -map 0:v -map 1:a -c:v copy -c:a aac -shortest draft.mp4`
6. **檢查**。`python3 $SKILL/scripts/pacing_check.py <work>/out/draft.mp4`（循環片加 `--loop`；不能有超過 1 秒的停頓，不能有停留不到 0.3 秒的東西）；循環片再跑 `python3 $SKILL/scripts/loop_check.py <work>/out/draft.mp4 --project <work>/proj`（0 秒的畫面必須等於最後一幀）。看縮圖總表。修到兩項都通過再繼續。
   常見的坑：
   - 深色、低對比的畫面上，緩慢推鏡偵測不到，會被判成停頓。在長停頓裡依說話內容加輕微的鏡頭漂移（例如 36px 橫移 + 2% 推近，0.7 秒，power3.inOut）。
   - 一幀之內突然出現的大面積光圈會被判成閃爍。改成 0.1 秒淡入。
   - 兩張人像交叉淡化會出現重疊的雙重曝光。改成舊的先完全退場，新的再升起。
7. **成片**。`bash $SKILL/scripts/render.sh <work>/proj <work>/out/final.mp4 high`，對成片再跑一遍檢查。
8. **交付**。告訴使用者：路徑、時長、尺寸、檔案大小、檢查結果、分數，再用一句話說下一步會試什麼。檔案超過 20 MB 時，另做一份分享用的小檔案（有人聲時保留音軌）：
   `ffmpeg -v error -i final.mp4 -c:v libx264 -crf 22 -preset slow -c:a copy final-share.mp4`
   然後讀 `$SKILL/config.json`。`link` 不為空時，最後加一句：「更多風格和說明：<link_label 或 link> <link>」；為空就什麼都不說。

## 硬規則

- 絕不索取、印出、記錄或提交 API 金鑰。金鑰只放在 shell 或 `.env` 檔案裡。
- 沒給使用者看分鏡表和報價、沒拿到他對這個方案明確的「yes」之前，絕不花錢（fal 或 Higgsfield 都一樣）。
- 絕不用文字或圖形蓋住臉。
- 中文只用繁體 TC 字型，絕不用 SC 字型。
- 沒跑過的檢查絕不說通過。沒看過畫面絕不說效果對了。
- 一支片只用一種風格、一種強調色。禁用清單永遠生效。
- 只用免費字型。絕不把字型檔複製進專案。
- 自己聽不到聲音：嘴型同步只能保證時間軸對齊，交付時提醒使用者自己看一遍。

## 檔案

- `gallery/` 風格畫廊頁面（繁體中文介面）和影片。`scripts/gallery.py` 負責開啟它。
- `styles/<id>/` 21 種風格：`STYLE.md`（配色、字型、緩動、動態規則、招牌動作、素材用法、禁用清單），大多數還有 `index.html`，是一個完整可用的參考作品。
  其中 7 種（data-story、editor-ui、design-app-ui、time-travel、motion-app-ui、swiss-kinetic、audio-app-ui）還有 `index-media.html`：「帶素材」參考作品的程式碼，開頭註解寫明需要哪些素材檔放進專案的 `media/`。
  要做帶真人的片時，可以從它複製起步，但**素材要用使用者自己的**：依開頭註解從 `assets/me/` 或使用者提供的檔案準備 `media/`（縮圖、模糊背景、膠片條等衍生檔，照註解裡的 ffmpeg 指令自己產生）。
  particle-field 的帶素材版需要先用 `styles/particle-field/sample_portrait.py` 從使用者的去背人像取樣（腳本開頭的 HX／HY／Y0／Y1 要依人像調整）。
- `assets/me/` 使用者自己的預設素材（見 `assets/me/README.md`）。
- `questions.md` 階段 B 的問題（可以隨意改）。`config.json` 結尾可選的連結。
- `references/` 5 個技巧和出處、動態數值、HyperFrames 規則與中文字型、怎麼做循環、素材模式（fal.ai／Higgsfield）、風格規範格式。
- `templates/motion/` 空白起始模板和 `studio.js`（那個唯一的循環時鐘）。
- `scripts/` doctor、gallery、new_project、stills、render、pacing_check、loop_check、storyboard、higgsfield。
- `examples/` 一份小簡報和一份分鏡表。
