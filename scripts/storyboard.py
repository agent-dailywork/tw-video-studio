"""storyboard.py：在花任何錢之前，展示素材模式的計劃和費用。

用法：python3 scripts/storyboard.py <storyboard.json>

storyboard.json（由 Claude 編寫；參見 examples/storyboard.json）：
  {"title": "...", "format": "16:9", "seconds": 12,
   "shots": [{"time": "0.0-3.0", "graphic": "畫面做什麼",
              "asset": {"kind": "code"}},                                   # 純程式碼，免費
             {"time": "3.0-8.0", "graphic": "...",
              "asset": {"kind": "user_photo", "path": "media/me.jpg"}},     # 對方的照片，免費
             {"time": "...", "graphic": "...",
              "asset": {"kind": "user_clip", "path": "media/demo.mp4"}},    # 對方的影片片段，免費
             {"time": "...", "graphic": "...",
              "asset": {"kind": "generate", "provider": "fal", "endpoint": "<fal 端點 id>",
                        "from": "media/me.jpg", "prompt": "...", "duration": 5,
                        "estimate_usd": 0.5}},                               # fal.ai，花費美金
             {"time": "...", "graphic": "...",
              "asset": {"kind": "generate", "provider": "higgsfield", "from": "media/me.jpg",
                        "model": "seedance-2.0", "prompt": "...", "duration": 5, "resolution": "720p"}}]}  # Higgsfield，花費 credit
provider 預設是 "fal"。fal 的 estimate_usd 由 Claude 先用 fal MCP 的 estimate_cost 查好再填；沒填就顯示「?」。
Higgsfield 的 credit 由 scripts/higgsfield.py estimate 估算。
印出一張表、每個 'generate' 鏡頭的估價和總計，並寫出 storyboard.md。
它從不生成任何東西。"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sb = json.load(open(sys.argv[1], encoding='utf-8'))
root = os.path.dirname(os.path.abspath(sys.argv[1]))
rows, total, unknown, sources, missing = [], 0.0, 0, set(), []
usd = 0.0
for n, s in enumerate(sb['shots'], 1):
    a = s.get('asset', {'kind': 'code'})
    kind = a.get('kind', 'code')
    cost = '0'
    if kind in ('user_photo', 'user_clip'):
        p = a.get('path', '')
        if not os.path.exists(os.path.join(root, p)) and not os.path.exists(p):
            missing.append(p)
        what = f"你的{'照片' if kind == 'user_photo' else '影片片段'}：{os.path.basename(p)}"
    elif kind == 'generate' and a.get('provider', 'fal') == 'fal':
        frm = a.get('from')
        what = (f"fal.ai {a.get('endpoint', '（端點待定）')} 片段，"
                + (f"由 {os.path.basename(frm)} 生成" if frm else '由文字生成') + f"，{a.get('duration', 5)} 秒。"
                f"提示詞：\"{a.get('prompt', '')}\"")
        e = a.get('estimate_usd')
        if e is None:
            cost, unknown = '?', unknown + 1
        else:
            cost = f"US${float(e):.2f}"
            usd += float(e)
        sources.add('fal.ai 報價')
    elif kind == 'generate':
        frm = a.get('from')
        what = (f"Higgsfield {a.get('model', 'seedance-2.0')} 片段，"
                + (f"由 {os.path.basename(frm)} 生成" if frm else '由文字生成') + f"，{a.get('duration', 5)} 秒，"
                f"{a.get('resolution', '720p')}。提示詞：\"{a.get('prompt', '')}\"")
        cmd = [sys.executable, os.path.join(HERE, 'higgsfield.py'), 'estimate', '--model', a.get('model', 'seedance-2.0'),
               '--duration', str(a.get('duration', 5)), '--resolution', a.get('resolution', '720p'),
               '--prompt', a.get('prompt', '')]
        if not frm:
            cmd.append('--text')
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=root)
        try:
            est = json.loads(r.stdout.strip().splitlines()[-1])
        except Exception:
            est = {'credits': None, 'source': (r.stderr or r.stdout)[-200:]}
        sources.add(est['source'])
        if est['credits'] is None:
            cost, unknown = '?', unknown + 1
        else:
            cost = f"{est['credits']:g} credit"
            total += est['credits']
    else:
        what = '純程式碼（無素材）'
    rows.append((n, s.get('time', ''), s.get('graphic', ''), what, cost))

gen = sum(1 for s in sb['shots'] if s.get('asset', {}).get('kind') == 'generate')
lines = [f"# 分鏡：{sb.get('title', '未命名')}", '',
         f"{sb.get('format', '16:9')}，{sb.get('seconds', '?')} 秒。還沒有生成任何東西，也沒有花任何錢。", '',
         '| 鏡頭 | 時間（秒） | 畫面做什麼 | 素材 | 費用 |', '|---|---|---|---|---|']
lines += [f'| {n} | {t} | {g} | {w} | {c} |' for n, t, g, w, c in rows]
lines.append('')
if gen:
    parts = []
    if usd:
        parts.append(f'US${usd:.2f}')
    if total:
        parts.append(f'{total:g} Higgsfield credit')
    tot = ' + '.join(parts) if parts else ''
    if unknown:
        tot = (tot + '，' if tot else '') + f'另有 {unknown} 個鏡頭尚未報價'
    lines.append(f"生成 {gen} 個片段，總計約 {tot}"
                 f"（{'；'.join(sorted(sources))}）。失敗的任務通常不收費。")
    lines.append('')
    lines.append('回覆 "yes" 就開始生成。回覆其他內容，我會先修改計畫。')
else:
    lines.append('這個計畫裡沒有 AI 片段，所以不花任何錢。')
if missing:
    lines.append('')
    lines.append('缺少檔案：' + '、'.join(missing))
md = '\n'.join(lines)
open(os.path.join(root, 'storyboard.md'), 'w', encoding='utf-8').write(md + '\n')
print(md)
