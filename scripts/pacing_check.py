"""pacing_check.py：第 5 招的第二部分。從渲染好的影片像素裡測量節奏。

用法：python3 scripts/pacing_check.py <video.mp4> [--loop] [--max-gap 1.0] [--min-hold 0.3] [--end-hold 0]

檢查項：
  1. 沒有死寂空檔：至少每 --max-gap 秒就有肉眼可見的變化。
     一次"變化"指：0.1 秒的一步裡，超過 0.4% 的像素變化超過 14 級。
  2. 沒有閃爍：兩個硬切之間沒有短於 --min-hold 秒的鏡頭，
     也沒有在 --min-hold 秒內冒出來又消失的元素。
寫出 <video>-contact.jpg（從 0 秒起每秒一幀，從左到右）和 <video>-pacing.json。
什麼算變化：大的東西在動。小標籤滑動或緩慢的顏色漸變可能不算，
所以在循環接縫附近，每秒都要保持一個大動作。快於約每秒 3 次的閃動會被看成閃爍。
退出碼 0 = 通過，1 = 不通過。"""
import argparse, json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _media import probe, gray_frames, diff_stats

ap = argparse.ArgumentParser(description='從影片像素測量節奏')
ap.add_argument('video', help='要檢查的 mp4')
ap.add_argument('--max-gap', type=float, default=1.0, help='允許的最長無變化時間（秒）')
ap.add_argument('--min-hold', type=float, default=0.3, help='鏡頭或元素最短停留時間（秒）')
ap.add_argument('--end-hold', type=float, default=0.0, help='允許結尾靜止這麼久（秒）')
ap.add_argument('--loop', action='store_true', help='循環影片：同時測量跨越循環點的空檔')
a = ap.parse_args()
info = probe(a.video)
dur = info['dur']

# 1. 死寂空檔，每秒 10 步
f10, w, h = gray_frames(a.video, 10, 240)
events = []
for i in range(1, len(f10)):
    _, moved = diff_stats(f10[i - 1], f10[i])
    if moved > 0.004:
        events.append(round(i / 10, 2))
pts = [0.0] + events + [round(dur, 2)]
gaps = [(pts[i], pts[i + 1], round(pts[i + 1] - pts[i], 2)) for i in range(len(pts) - 1)]
if a.loop and len(pts) > 2:   # 結尾的靜止時間會直接接上開頭的靜止時間
    wrap = round((pts[-1] - pts[-2]) + (pts[1] - pts[0]), 2)
    gaps.append((pts[-2], pts[1], wrap))
dead = [g for g in gaps if g[2] > a.max_gap + 0.05]
if a.end_hold:
    dead = [g for g in dead if not (g[1] >= dur - 0.05 and g[2] <= a.end_hold + 0.05)]

# 2. 閃爍，每秒 30 步
f30, _, _ = gray_frames(a.video, 30, 160)
k = max(1, int(round(a.min_hold / 2 * 30)))   # 向前後各看這麼多幀
cuts, flashes = [], []
for i in range(1, len(f30)):
    _, moved = diff_stats(f30[i - 1], f30[i], 30)
    if moved > 0.35:
        cuts.append(i / 30)
for i in range(k, len(f30) - k, 2):
    _, ac = diff_stats(f30[i - k], f30[i], 30)
    _, ab = diff_stats(f30[i - k], f30[i + k], 30)
    if ac > 0.01 and ab < 0.25 * ac:
        flashes.append(round(i / 30, 2))
shots = [0.0] + cuts + [dur]
short_shots = [(round(shots[i], 2), round(shots[i + 1], 2)) for i in range(len(shots) - 1)
               if shots[i + 1] - shots[i] < a.min_hold - 0.01]
# 合併相鄰的閃爍幀
merged = []
for t in flashes:
    if merged and t - merged[-1][1] <= 0.1:
        merged[-1][1] = t
    else:
        merged.append([t, t])

# 總覽圖，每秒一幀
base = os.path.splitext(a.video)[0]
cols = 6 if info['w'] >= info['h'] else 8
rows = max(1, int((dur + cols - 1) // cols))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', a.video, '-vf',
                f'fps=1:round=down,scale={320 if info["w"] >= info["h"] else 180}:-2,tile={cols}x{rows}:padding=8:margin=8:color=white',
                '-frames:v', '1', '-q:v', '4', base + '-contact.jpg'], check=False)

rep = {'video': a.video, 'duration': round(dur, 2), 'change_steps': len(events),
       'longest_gap_s': max(g[2] for g in gaps), 'dead_gaps': dead,
       'hard_cuts': [round(c, 2) for c in cuts], 'too_short_shots': short_shots,
       'flashes': [m for m in merged], 'pass': not dead and not short_shots and not merged}
json.dump(rep, open(base + '-pacing.json', 'w'), indent=1)
print(f"節奏：最長空檔 {rep['longest_gap_s']} 秒（上限 {a.max_gap}），{len(events)} 個變化步，"
      f"{len(cuts)} 個硬切")
for g in dead:
    print(f"  FAIL 死寂空檔 {g[0]} 到 {g[1]} 秒（{g[2]} 秒內什麼都沒動）")
for s in short_shots:
    print(f"  FAIL 鏡頭 {s[0]} 到 {s[1]} 秒，短於 {a.min_hold} 秒")
for m in merged:
    print(f"  FAIL 大約 {m[0]} 到 {m[1]} 秒有東西冒出來又消失（停留不到 {a.min_hold} 秒）")
print('PASS' if rep['pass'] else 'FAIL', '| 總覽圖：', base + '-contact.jpg')
sys.exit(0 if rep['pass'] else 1)
