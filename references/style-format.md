# 風格怎麼寫

風格畫廊裡的每種風格都是 `styles/<id>/` 下的一個資料夾：

- `STYLE.md` 規範（必有）。格式見下。控制在大約 80 行以內。
- `index.html` 用這種風格做的完整作品（如果有）。複製它作為起點。
- `studio.js` 僅當該作品用到單一時鐘輔助腳本時才有。

根據使用者參考新建的風格也用同樣的格式，儲存為 `styles/<new-id>/STYLE.md`。

## STYLE.md 格式

```
# <中文名>（<English name>）

id: <id>
適合：<3 到 6 種影片>
氣質：<一句話>
參考作品：styles/<id>/index.html（<時長> 秒，<循環或不循環>）   或   無，只有規範
畫廊影片：gallery/videos/<id>.mp4

## 配色 (hex)
- 底色：#......
- 墨色：#......
- ……（每種顏色都要命名；標出唯一的強調色）

## 字型
- 標題：<字型> <字重>，字距 <em>，行高 <n>
- 標籤：<字型> <字重>，<px>
- 中文：Noto Sans TC（無襯線）、Noto Serif TC（襯線）或 LXGW WenKai TC（手寫），按拉丁字型的風格選；字距 0 到 0.02em，行高 1.3 到 1.5
- 字型連結（貼進 <head>；所有字型都免費）：
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=...&display=swap">

## 緩動 (數值)
- 落定：<ease>，<秒>
- 離開：<ease>，<秒>
- 移動：<ease>，<秒>
- 錯開：<秒>

## 動效規則
- <4 到 8 條，讓動效有這個風格的感覺>

## 標誌動作
- <2 到 4 個讓人一眼認出的動作>

## 構圖
- <網格、邊距、主體放哪、畫面填多滿>

## 帶素材
- <真實照片或片段怎麼放進這個風格：遮罩、調色、取景；人物預設用 assets/me/ 裡使用者自己的素材>

## 停用清單
- <會破壞這個風格的東西>
```

標題行和段落標題都用上面的中文寫法，和 `styles/*/STYLE.md` 保持一致；H1 寫中文名，後面括號裡保留英文原名。

## 字型規則（所有風格）
- 只用免費字型：Google Fonts，或渲染時從 Fontshare 官方連結載入的 Fontshare 字型。
- 只要加了任何字型 `<link>`，就把作品用到的**每個**字型都連結上（這時 HyperFrames 會跳過它自己的字型載入）。
- 中文文字要連結繁體 TC 字型（Noto Sans TC、Noto Serif TC 或 LXGW WenKai TC；Switzer 和 Inter 沒有中文字形）。絕不用 SC 字型。
- 絕不附帶字型檔案。絕不用付費字型。
