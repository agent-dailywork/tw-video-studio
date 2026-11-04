# 素材模式：圖形 + 真實照片、影片片段和 AI 片段

素材模式就是放進了真實畫面的動效模式。圖形依然是主角，素材嵌在圖形裡面。

## 三類素材（從便宜到貴）
1. 使用者自己的照片。免費。程式碼可以讓照片活起來：緩慢推近、去背與背景之間的
   視差、光線掃過、遮罩揭示。
2. 使用者自己的影片片段（螢幕錄影、產品鏡頭、口播）。免費。
3. AI 生成的片段（優先用 fal.ai，備用 Higgsfield）。要花錢。最適合把**一張**靜態照片變成 4 到 8 秒的
   運動鏡頭（圖生影片），或者生成沒人拍過的 B-roll（文生影片）。

## 預設人物素材
當作品需要出現人物、而使用者沒有提供其他素材時，使用 `assets/me/` 裡使用者自己的素材（先讀 `assets/me/README.md`）。
資料夾是空的就請使用者提供，或改成純圖形。絕不把文字壓在臉上。

## AI 片段計費順序
1. **fal.ai（優先）**：透過 fal 的 MCP 工具。
   - 挑模型：`recommend_model`，描述需求（例如「image to video, 5 seconds, slow push in, keep the face consistent」）。
     使用者指定模型時直接用那個端點 id，原樣複製，不要自己猜或加前綴。
   - 參考照片：先 `upload_file` 上傳，用回傳的網址當模型的 image 輸入。
   - 報價：`estimate_cost`（或 `get_pricing`），把美金金額填進分鏡表該鏡頭的 `estimate_usd`，
     再跑一次 `storyboard.py` 給使用者看總價。
   - 拿到明確的「yes」才執行：一次一個鏡頭用 `submit_job`，用 `check_job` 輪詢到完成；
     多個鏡頭可以用 `submit_jobs` + `wait_for_jobs`。
   - 下載結果到專案的 `media/shotN.mp4`（`curl -L -o`），截 3 幀檢查後才放進合成。
   - fal 帳號：如果 MCP 連到多個帳號，先用 `list_accounts` 確認是使用者要的那個，再花錢。
2. **Higgsfield（備用）**：沒連 fal MCP、或使用者指定時才用。走 `scripts/higgsfield.py`（API，key 在 `.env`）。
   改用 Higgsfield 之前，先告訴使用者原因。下方「Key」「API」兩節是 Higgsfield 的細節。
付費片段一律先展示價格，等使用者明確說「好」再生成。

## Higgsfield Key（絕不出現在聊天裡）
- 使用者在 shell 裡設定 `HIGGSFIELD_API_KEY=key_id:key_secret`，或者寫進專案資料夾裡的
  `.env` 檔案。Key 在 https://console.higgsfield.ai 獲取。
- `python3 scripts/higgsfield.py check` 只回答有或沒有，絕不印出 key。
- 絕不讓使用者貼上 key。絕不回顯、記錄或提交 key。`.env` 已在 `.gitignore` 裡。

## Higgsfield API（腳本做了什麼）
- Base：`https://platform.higgsfield.ai`（設定 `HIGGSFIELD_API_BASE` 可修改；文件裡寫的是 `https://api.higgsfield.ai`）。
- 請求頭：`Authorization: Key <key_id>:<key_secret>`。
- 上傳照片：`POST /files/generate-upload-url`，body 為 `{"content_type": "image/jpeg"}`，然後帶上返回的請求頭，
  把檔案 PUT 到 `upload_url`。把 `public_url` 作為 `image_url` 使用。
- 查價，免費：`POST /estimate/<endpoint>`，body 相同。返回 `credits`。
- 提交：`POST /<endpoint>`，帶 `Idempotency-Key` 請求頭。返回 `status_url`。
- 輪詢 `status_url`（間隔從 2 秒逐漸增加到 10 秒），直到狀態為 `completed`、`failed`、`nsfw` 或 `canceled`。
  片段在 `video.url`。要下載下來；連結大約 7 天有效。失敗的任務不扣費。
- 文件：https://docs.higgsfield.ai

| 本技能裡的名稱 | 端點 | 適合 | 時長 |
|---|---|---|---|
| seedance-2.0（預設） | `bytedance/seedance-2.0/image-to-video` 和 `/text-to-video` | 照片轉片段、任何較複雜的運動、起始幀 + 結束幀 | 4 到 15 秒 |
| seedance-2.5 | `bytedance/seedance-2.5/image-to-video` 和 `/text-to-video` | 更長的單鏡頭 | 4 到 30 秒 |
| kling-3-turbo | `kling-video/v3.0-turbo/image-to-video` | 便宜的簡單運動 | 3 到 15 秒 |

腳本會關閉生成的聲音（`generate_audio: false`）。聲音在剪輯裡處理。

## 分鏡表關卡（始終執行）
花任何錢之前：
1. 寫 `storyboard.json`（參見 `examples/storyboard.json`）：每個鏡頭、它的時間、圖形
   做什麼，以及用哪種素材：`code`、`user_photo`、`user_clip` 或 `generate`（附模型、prompt、
   時長、解析度）。
2. 執行 `python3 scripts/storyboard.py storyboard.json`。它會印出表格和費用估算（fal 用 `estimate_usd`，Higgsfield 自動估 credit）。
3. 把這張表給使用者看。等使用者明確說「好」。有任何改動：更新後再給使用者看一遍。
4. 這之後才生成（fal 用 MCP 的 `submit_job`；Higgsfield 用 `scripts/higgsfield.py generate ... --yes`），一次生成一個鏡頭，每個片段用之前
   都要檢查（截 3 幀）。

## 照片轉片段的有效 prompt
- 描述**鏡頭運動**和**一個**動作："slow push in, she looks up from the laptop and smiles, soft window light"。
- 構圖盡量貼近原照片。構圖變化太大會讓模型在片段中途切鏡。
- 做循環時，把同一張照片也作為結束圖傳入（seedance），讓片段結束在開始的地方。
- 絕不要求片段裡出現文字。文字永遠用程式碼疊加在上面。
- prompt 用英文寫，因為它會發給英文影片模型。

## 把素材放進合成
- 把檔案複製到專案的 `media/` 資料夾。
- 片段寫成 `<video class="clip" muted playsinline data-start=".." data-duration=".." data-media-start="..">`。
- 把素材放進圖形**裡面**（遮罩、卡片、形狀），讓它讀起來是一個整體設計，而不是投影片。
- 絕不在人臉上疊畫任何東西。不說明就絕不把 16:9 片段裁成奇怪的形狀。
- 統一顏色：從片段取色，把風格的底色往它靠一點；或者用 CSS filter 給片段調色，讓兩者像同一個世界。
