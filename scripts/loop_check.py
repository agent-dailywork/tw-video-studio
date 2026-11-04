"""loop_check.py：第 4 招。證明循環是無縫的。

用法：python3 scripts/loop_check.py <video.mp4> [--project <dir>]

測試 A（帶 --project 時）：用 HyperFrames 渲染 t = 0 和 t = 結尾 兩幀，
  逐像素比較。兩幀必須是同一張畫面。
測試 B（總是做）：比較影片最後一幀和第一幀。這一跳不能比兩幀之間的正常變化大，
  這樣影片重複播放時就看不出接縫。
退出碼 0 = 通過，1 = 不通過。"""
import argparse, os, re, shutil, subprocess, sys, tempfile, statistics
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _media import probe, gray_frames, diff_stats

ap = argparse.ArgumentParser(description='證明循環是無縫的')
ap.add_argument('video', help='要檢查的 mp4')
ap.add_argument('--project', help='專案資料夾；給了就同時做測試 A')
a = ap.parse_args()
ok = True

if a.project:
    html = open(os.path.join(a.project, 'index.html')).read()
    D = float(re.search(r'data-duration="([\d.]+)"', html).group(1))
    tmp = tempfile.mkdtemp()
    # 用一份關掉時鐘迴繞的副本來測，這樣結尾那幀真的是在 t = 結尾 時畫出來的
    proj = os.path.join(tmp, 'proj')
    shutil.copytree(a.project, proj, ignore=shutil.ignore_patterns('*.mp4', 'stills', '.hyperframes', 'out'))
    page = open(os.path.join(proj, 'index.html')).read()
    page = page.replace('<head>', '<head>\n<script>window.STUDIO_NO_WRAP = true;</script>', 1)
    open(os.path.join(proj, 'index.html'), 'w').write(page)
    hf = ['npx', '--yes', 'hyperframes@' + os.environ.get('HF_VERSION', '0.8.181')]
    subprocess.run(hf + ['snapshot', proj, '--at', f'0,{D}', '--no-end', '-o', tmp],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    pngs = sorted(f for f in os.listdir(tmp) if f.startswith('frame') and f.endswith('.png'))
    if len(pngs) < 2:
        print('FAIL 沒能截到首尾兩幀：', pngs); sys.exit(1)
    first, last = os.path.join(tmp, pngs[0]), os.path.join(tmp, pngs[-1])
    fa, w, h = gray_frames(first, None, 640)
    fb, _, _ = gray_frames(last, None, 640)
    mean, moved = diff_stats(fa[0], fb[0], 8)
    same = moved < 0.0005
    ok &= same
    print(f"A. 0 秒的幀 對比 {D} 秒的幀：{moved * 100:.3f}% 的像素不同"
          f"（平均 {mean:.2f} 級）-> {'PASS，同一張畫面' if same else 'FAIL，循環沒有閉合'}")

info = probe(a.video)
frames, w, h = gray_frames(a.video, None, 320)
steps = [diff_stats(frames[i - 1], frames[i])[0] for i in range(1, len(frames))]
seam = diff_stats(frames[-1], frames[0])[0]
typical = statistics.median(steps) if steps else 0
p90 = sorted(steps)[int(0.9 * (len(steps) - 1))] if steps else 0
limit = max(2.5 * typical, p90, 0.6)
seam_ok = seam <= limit
ok &= seam_ok
print(f"B. 接縫跳變（最後一幀到第一幀）{seam:.2f} 級；正常步長 {typical:.2f}，"
      f"上限 {limit:.2f} -> {'PASS，無縫' if seam_ok else 'FAIL，重複播放時會看到跳動'}")
print('PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
