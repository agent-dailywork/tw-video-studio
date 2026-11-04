# TW 影片工作室（Claude Video 台灣繁體中文版）

一個免費的 Claude Code skill，做出來的動態圖形像專業工作室出品，**以台灣繁體中文為主**。

- **選一個風格**：風格畫廊裡有 21 種風格，每一種都以真實影片播放。
- **回答 5 個簡短問題。**
- **拿到你的影片。** Claude 用程式碼製作，先給你 3 張靜幀確認，再渲染成 MP4，
  並從真實畫面檢查自己的成果。

可以是純圖形，也可以放進你自己的照片和影片片段，或者用 AI 生成片段（優先用 **fal.ai**，也支援 Higgsfield；
都會先給你看分鏡和報價，等你說「好」才花錢）。一般的 Claude Pro 方案即可使用。

## 和原版的差別

這個版本以 [Harry 的中文版](https://github.com/harryleemedia/harry-video-studio) 為基礎，而它又改自
[Claude Video 2.0](https://github.com/ItsssssJack/claude-video-2)。改動：

- **台灣繁體中文**：所有說明、提問、畫廊介面都用台灣繁體與台灣用語（OpenCC `s2twp` 轉換後人工校對）。
- **繁體字型**：中文一律用 Noto Sans TC／Noto Serif TC／LXGW WenKai TC，**禁用 SC 簡體字形**；
  加入中文排版規則（字距、行高、避頭點、不用假斜體、中文字數上限）。
- **台灣平台**：YouTube Shorts、IG Reels、TikTok 的直式安全區。
- **口播轉寫輸出繁體**：Whisper 帶繁體提示，轉完再跑 OpenCC。
- **fal.ai 優先**：AI 片段改用 fal 的 MCP（報價、上傳、生成都走 MCP），Higgsfield 留作備用。
- **個人素材清空**：原版作者的肖像素材全部移除，`assets/me/` 留給你自己的素材，而且預設不進 git。

## 安裝

1. 下載到 skill 資料夾（資料夾名稱必須是 `tw-video-studio`）：
   `git clone https://github.com/agent-dailywork/tw-video-studio.git ~/.claude/skills/tw-video-studio`
   確認存在 `~/.claude/skills/tw-video-studio/SKILL.md`。
2. 另外需要 Node 22 以上（https://nodejs.org）和 ffmpeg（`brew install ffmpeg`）。Claude 會替你檢查，缺什麼就給你一行指令補上。
3. 打開 Claude Code，說：**幫我做個動態圖形**（或 make me a motion graphic）。

### 要用 AI 片段時（選用）

**fal.ai（建議）**：在終端機執行一次
```bash
claude mcp add --transport http --scope user fal https://mcp.fal.ai/mcp-relay
```
然後在 Claude Code 輸入 `/mcp`，選 fal → Authenticate，在瀏覽器登入你的 fal 帳號。不需要 API key。

**Higgsfield（備用）**：到 https://console.higgsfield.ai 取得 key，在專案資料夾的 `.env` 檔案加一行
`HIGGSFIELD_API_KEY=your_key_id:your_key_secret`。千萬不要把 key 貼到聊天裡。

## 放進你自己的素材（選用）

把你的照片、去背人像、口播片段放進 `assets/me/`，命名方式見 `assets/me/README.md`。
需要人物而你沒另外給素材時，Claude 就會用這些。這個資料夾預設不會被推上 git。

## 工作流程

**A. 選風格。** 瀏覽器會開啟風格畫廊，每一格都是真實影片。把工作室作品切到
「帶素材」，就能看到同一個設計放進真實素材的效果。點 **「用這個風格」**，把名稱
貼回 Claude Code。也可以貼你自己的參考連結或圖片。

**B. 五個問題**，放在一則訊息裡，每題都有預設值：

1. 用在哪裡？（YouTube 片頭、YouTube Shorts、IG Reels、TikTok、產品發表、講解、廣告）多長？【12 秒，16:9】
2. 畫面上要出現哪些文字？【我根據你的主題來寫，繁體中文】
3. 需要循環播放嗎？【不需要】
4. 你的品牌：顏色、字型、logo？【用風格內建的；中文用 Noto Sans TC】
5. 要用真實素材嗎？你自己的照片或影片、AI 生成的片段（fal.ai），還是不用（純圖形）？【不用】

問題寫在 `questions.md` 裡，你可以自己改。

**C. 製作。** 先出分鏡表（鏡頭、時間、素材，有 AI 片段時還有報價），
再出 3 張靜幀給你確認（包含檢查字形是不是繁體），然後渲染，最後做節奏檢查；如果是循環作品，還要做像素級循環檢查。

## 21 種風格

工作室作品：`paper-world`、`ink-line`、`weather-widget`、`data-story`、`swiss-kinetic`、
`particle-field`、`growing-city`、`explainer-diagram`、`time-travel`、`editor-ui`、`motion-app-ui`、
`design-app-ui`、`audio-app-ui`。

程式碼風格：`swiss-grid`、`editorial-paper`、`midnight-grid`、`paper-cut`、`risograph`、`blueprint`、
`graphite-ui`、`poster-pop`。

每種風格都是 `styles/` 裡的一個資料夾，裡面有一個 `STYLE.md`（顏色、字型、緩動參數、動態規則、禁用清單），
大多數還附一個可以直接起步的完整作品。隨時開啟風格畫廊：
`python3 ~/.claude/skills/tw-video-studio/scripts/gallery.py`

畫廊裡「帶素材」的樣片來自原版 Claude Video（MIT），畫面中的人物是原版作者。
你可以用自己的素材重做這些樣片來取代。

## 為什麼好看：5 個技巧

1. 先選定一種風格，然後堅持到底。
2. 真實參考勝過形容詞。
3. 用數字寫簡報。
4. 循環：只用一個時鐘，最後一幀必須等於第一幀。
5. 檢查畫面，而不是程式碼。

`references/hacks.md` 逐條解釋每個技巧及其出處。

## 裡面有什麼

- `SKILL.md` Claude 遵循的步驟
- `gallery/` 風格畫廊及其影片
- `styles/` 21 種風格
- `questions.md` 提問清單（隨意修改）和 `config.json`（選填，Claude 在最後提到的一個連結）
- `references/` 5 個技巧、動態參數、引擎規則與中文字型、素材模式（fal.ai／Higgsfield）、如何撰寫風格
- `templates/` 起步頁面和單一時鐘輔助腳本
- `scripts/` 風格畫廊、渲染、靜幀、節奏檢查、循環檢查、分鏡表、Higgsfield
- `examples/` 一份簡短的簡報和一份分鏡表
- `assets/me/` 你自己的預設素材（預設不進 git）

以 [HyperFrames](https://hyperframes.heygen.com) 和 [GSAP](https://gsap.com) 製作。所有字型都免費
（Google Fonts，以及渲染時從 Fontshare 載入的 Switzer）。

## 授權

程式碼和文件：MIT 授權條款（見 `LICENSE`），版權同時屬於本版、Harry Lee 的中文版和原版 Claude Video 的作者。
原版 Harry 中文版中的 Harry Lee 個人肖像素材不在本 repo 內。
