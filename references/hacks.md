# 5 個技巧

成品之所以像工作室做的、而不像一句隨手寫的 prompt 生成的，靠的就是這五個習慣。
技能會替你把五個都做到。下面說明每個技巧是什麼、出處在哪。

## 1. 先選定一種風格，然後堅持到底

寫任何程式碼之前，先從 `styles/` 裡選定**一種**風格（或根據使用者給的參考新建一種）。
風格是一份簡短的規範：hex 顏色、字型、緩動引數、動效規則和停用清單。
作品裡的每個鏡頭都用這同一份規範，不混搭。

原因：風格不定下來，每個模型都會退回同一個預設樣子
（深色背景、發光、紫色漸變）。固定的規範能防止鏡頭之間風格漂移。

技能的做法：階段 A 展示風格畫廊，使用者選一種風格。它的 STYLE.md 會貼上進簡報，
它的顏色會變成檔案頂部的 CSS token。其他任何地方都不手寫顏色。

出處：
- Motion Lab 主張一開始就禁掉預設的 AI 風格：https://github.com/NovusEdge/motion-lab
- 「鎖定設計 token」，放在一個共享的地方：https://aiartimind.com/how-to-make-motion-graphics-with-claude-opus-5-5/

## 2. 真實參考勝過形容詞

「做得簡潔現代一點」毫無意義，一部真實影片裡的一幀真實畫面卻資訊量巨大。
向使用者要 1 到 3 個參考，然後描述它們是**怎麼**做出來的（遮罩文字、緩慢的鏡頭、
長時間停留），而不只是它們給人什麼感覺。

去哪裡找好參考：
- https://savee.com（設計與動效靜幀的情緒板）
- https://godly.website（真實網站上最好的動效）
- https://mobbin.com（真實的 App 介面，很適合做產品演示）
- Linear、Apple 和 Cursor 的發布影片（搜尋 "<company> launch video"）

出處：
- 逐幀拆解 Linear Agent 發布影片（遮罩揭示、長時間停留、快起步的緩動）：
  https://impractical.ai/launch-videos/linear-agent
- 「先找參考，再用文字描述它的製作方法」：
  https://aiartimind.com/how-to-make-motion-graphics-with-claude-opus-5-5/

## 3. 用數字寫簡報

開工前，把每個形容詞都換成數字：
- 時長（秒）和畫幅（1920 x 1080 或 1080 x 1920）
- 顏色用 hex
- 緩動寫名稱和秒數（expo.out，0.6 秒），絕不寫「順滑」
- 每個鏡頭一個主動作，寫明開始時間
- 一份停用清單

預設停用清單（始終生效）：
- 不要變色相的漸變
- 不要發光、泛光或鏡頭光暈
- 眼睛追隨的任何東西都不要用線性緩動
- 不要所有東西都居中的版式
- 強調色最多一種
- 任何東西都不從 0 開始放大（縮放起點用 0.6 到 0.9，配合透明度漸顯）

出處：
- Motion Lab 的數字化簡報：時間、hex 色板、緩動與彈簧引數、鏡頭列表、每個鏡頭一個主動作：
  https://github.com/NovusEdge/motion-lab
- 停用變色漸變、發光和線性緩動：https://aiartimind.com/how-to-make-motion-graphics-with-claude-opus-5-5/

## 4. 循環：只用一個時鐘，最後一幀 = 第一幀

只有結尾真的就是開頭，循環才看起來無縫。所以：
- **所有**動效都由同一個時鐘驅動（`templates/motion/studio.js` 裡的 `STUDIO.play(render)`）。
  render(t) 只憑 t 畫出整幀畫面。
- 每個重複動作在整個時長內都要走完整數個週期（`STUDIO.wave(t, 2)`），
  每個一次性動作結束時都要回到起點。
- 要把不循環的作品改成循環：按 `references/loops.md` 裡的清單逐項做。
- 證明它：`scripts/loop_check.py` 渲染 0 秒處和結尾處的幀，逐像素比對。
  只要有差異就判定失敗。它還會檢查從最後一幀跳回第一幀的變化
  不大於正常的一幀步進。

出處：
- 讓首尾幀一致的循環相位輔助函式：https://github.com/NovusEdge/motion-lab
- HyperFrames 逐幀渲染一條暫停的時間軸，所以同一時間永遠得到同一畫面：
  https://hyperframes.heygen.com（或執行 `npx hyperframes docs gsap`）

## 5. 檢查畫面幀，而不是程式碼

看起來正確的程式碼，畫面仍可能是錯的。所以要在關鍵時刻看圖：
1. 完整渲染前，截 3 到 4 張靜幀，每張在鏡頭切換後約 0.6 秒、畫面元素落定之後（`scripts/stills.sh`）。
   逐張檢視，修好不對的地方，拿到使用者點頭。
2. 渲染完成後，執行節奏檢查（`scripts/pacing_check.py`）：
   不能有超過 1 秒的空檔，任何東西在畫面上停留都不少於 0.3 秒。
3. 檢視它生成的縮圖總表（每秒一幀）。

出處：
- 「看完整影片之前，先檢查切換處的幀」：https://aiartimind.com/how-to-make-motion-graphics-with-claude-opus-5-5/
- 鏡頭切換處的靜幀、帶編號的縮圖總表、幀差比對：https://github.com/NovusEdge/motion-lab
- HyperFrames 的 `snapshot` 能從合成中擷取精確的幀：https://hyperframes.heygen.com
