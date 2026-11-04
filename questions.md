# 提問清單（階段 B / Stage B）

使用者選好風格後，Claude 把下面這段作為**一則**訊息原樣發出。
要改問題就改這個檔案。保持編號、每題一行、預設值放在【】裡。
使用者已經回答過的題目，Claude 跳過，其餘照問。

---

1. 用在哪裡？（YouTube 片頭、YouTube Shorts、IG Reels、TikTok、產品發表、講解、廣告）多長？【12 秒，16:9】
2. 畫面上要出現哪些文字？【我根據你的主題來寫，繁體中文】
3. 需要循環播放嗎？【不需要】
4. 你的品牌：顏色、字型、logo？【用風格內建的；中文用 Noto Sans TC】
5. 要用真實素材嗎？你自己的照片或影片片段、AI 生成的片段（fal.ai），還是不用（純圖形）？【不用】

只要回覆你想改的題號就好，例如「1：IG Reels，8 秒。5：用我的照片」。或者直接回覆「開始」（或 "go"），全部用預設值。

---

## 追問（只在需要時）

- 如果第 5 題選「我的照片或片段」：「把檔案拖進來，或者告訴我資料夾路徑。」如果 `assets/me/` 裡有素材，再補一句：「不給的話，我就用 assets/me 裡你的預設素材。」
- 如果第 5 題選「AI 片段」：照 `references/media.md` 的「AI 片段計費順序」。
  - 有 fal 的 MCP 工具（名稱裡有 `fal`）：直接用，不用問 key。
  - 沒有 fal MCP 時說：
    「要用 fal.ai 生成，請先在終端機執行：
    `claude mcp add --transport http --scope user fal https://mcp.fal.ai/mcp-relay`
    然後在 Claude Code 輸入 `/mcp`，選 fal → Authenticate，在瀏覽器登入你的 fal 帳號。弄好了告訴我。」
  - 使用者指定 Higgsfield：先執行 `python3 scripts/higgsfield.py check`。沒有 key 就說：
    「把你的 Higgsfield key 寫進這個資料夾裡一個叫 .env 的檔案，只要一行：
    HIGGSFIELD_API_KEY=your_key_id:your_key_secret（到 https://console.higgsfield.ai 取得）。千萬不要貼到聊天裡。弄好了告訴我。」
