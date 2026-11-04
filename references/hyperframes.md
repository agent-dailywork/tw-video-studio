# HyperFrames：要緊的規則

HyperFrames 把一個帶有暫停 GSAP 時間軸的 HTML 頁面逐幀轉成 MP4。
文件：https://hyperframes.heygen.com ，或在終端執行：`npx hyperframes docs gsap`、
`npx hyperframes docs compositions`、`npx hyperframes docs data-attributes`。
腳本鎖定版本 0.8.181（用 `HF_VERSION` 修改）。需要 Node 22+ 和 ffmpeg。

## 約定
- 只有一個根元素：`<div id="root" data-composition-id="main" data-start="0" data-duration="9" data-width="1920" data-height="1080">`。
- 只有一條暫停的時間軸，註冊為 `window.__timelines["main"] = tl`。`STUDIO.play()` 會替你完成。
- 有時間段的媒體加上 `class="clip"` 以及 `data-start` 和 `data-duration`。
  影片：`<video class="clip" src="media/x.mp4" muted playsinline data-start="2" data-duration="4" data-media-start="0.5">`。
- 渲染：`npx hyperframes render <dir> -o out.mp4 -q draft`（快速草稿）或 `-q high`（最終版）。
- 靜幀：`npx hyperframes snapshot <dir> --at 0,3,6 --no-end -o stills/`。
- 檢查程式碼：`npx hyperframes lint <dir>`。

## 必須遵守的規則（否則渲染會閃爍或每次不一樣）
- 同一時間輸入，同一畫面輸出。不用 `Math.random`（改用 `STUDIO.rng(seed)`），不用 `Date.now`，不用定時器，不用 `requestAnimationFrame` 循環。
- 隨時間變化的文字，要在 render 函式或補間的 onUpdate 裡改，絕不用 gsap.set 改 innerHTML。
- Canvas：在 render(t) 裡根據 t 畫出整幀。
- 從專案資料夾（`media/`）載入媒體。檔名保持簡單。

## 字型
- 只用免費字型：Google Fonts，或渲染時從 Fontshare 官方連結載入的 Fontshare 字型
  （例如 Switzer：`https://api.fontshare.com/v2/css?f[]=switzer@400,500,600,700,800&display=swap`）。
  絕不把字型檔案複製進專案。絕不用付費字型。
- 每個字型都在 `<head>` 裡用 `<link>` 載入。只要加了**任何**字型連結，就要把頁面用到的**每個**字型都連結上：
  這時 HyperFrames 會跳過它自己的字型載入，沒連結的字型會退回成 Times。
- 系統字型名會被 HyperFrames 替換："Helvetica Neue"、"Avenir"、"SF Pro" 會變成 Inter，
  "Futura" 會變成 Montserrat。請主動選一款 Google Font（Inter、Jost、Bodoni Moda、Playfair Display……）。
- 在程式碼裡測量的文字（canvas、offsetWidth）必須在字型載入後重新測量
  （`document.fonts.ready.then(redraw)`）。`studio.js` 會替你完成。
- 渲染需要聯網，因為 GSAP 和字型都從公共 CDN 載入。
- 中文也一樣：一定要用 Google Fonts 連結，不能寫 "PingFang TC" 或 "Microsoft JhengHei"。

## 中文字型（台灣繁體）
- Switzer、Inter 等拉丁字型沒有中文字形，中文一律另外連結**繁體 TC** 字型：
  - 無襯線：Noto Sans TC
    `https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap`
  - 襯線（明體）：Noto Serif TC
    `https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;600;700;900&display=swap`
  - 手寫溫暖感：LXGW WenKai TC
    `https://fonts.googleapis.com/css2?family=LXGW+WenKai+TC:wght@400;700&display=swap`
  只連結會用到的字重，CJK 字型很大，多一個字重就多一份下載。
- **絕不用 Noto Sans SC / Noto Serif SC**。SC 是簡體字形：「說、骨、直、令、角」等字的寫法和台灣教育部標準字體不同，
  畫面一看就像大陸字。靜幀檢查時特別看這幾個字。
- `font-family` 把拉丁字型放前面、TC 放後面：`"Switzer", "Noto Sans TC", sans-serif`。
  英數字用拉丁字型、中文落到 TC，兩者的基線和粗細要在靜幀裡確認是否協調；不協調就讓中英文都用 Noto Sans TC。
- 排版：
  - 字距 `0` 到 `0.02em`，不用負字距。大標題可以到 `0.04em`。
  - 行高 1.3 到 1.5（拉丁字常用的 0.9 到 1.1 會讓中文上下擠在一起）。
  - 不用 `font-style: italic`：CJK 沒有真斜體。
  - 文字容器加 `line-break: strict; word-break: normal;`，避免標點落在行首。
  - 大標題手動用 `<br>` 斷行，按詞斷；不要靠自動換行。
  - 同樣字級下，中文視覺上比英文大且重。照搬英文設計時，中文字級通常縮 5% 到 10%、字重降一級（900 → 700）。
- 在程式碼裡逐字做動畫（逐字出現、打字機效果）時，用 `Array.from(text)` 拆字，不要用 `text.split('')`，
  才不會拆壞罕用字或 emoji。


## 畫幅
- 16:9 是 1920 x 1080，9:16 是 1080 x 1920。每種畫幅都重新排版，絕不直接裁切。
- 給剪輯軟體用的透明疊加層：`--format mov` 並使用透明背景。
