"""higgsfield.py：為素材模式（Media mode）呼叫 Higgsfield API。只用標準庫。

金鑰絕不放進聊天。把它放進 shell（export HIGGSFIELD_API_KEY=...），或者放進專案資料夾裡
名為 .env 的檔案：  HIGGSFIELD_API_KEY=your_key_id:your_key_secret
在 https://console.higgsfield.ai 獲取。本腳本從不印出金鑰。

用法：
  python3 scripts/higgsfield.py check                         是否已設定金鑰？（只印出有/沒有）
  python3 scripts/higgsfield.py estimate --model seedance-2.0 --duration 5 --resolution 720p [--text]
  python3 scripts/higgsfield.py generate --model seedance-2.0 --image photo.jpg --prompt "..." \\
          --duration 5 --resolution 720p --out media/shot2.mp4 --yes
'generate' 會花費 credit。沒有 --yes 就拒絕執行。只有在對方對分鏡和費用說了"yes"之後，才加 --yes。
Base URL：HIGGSFIELD_API_BASE（預設 https://platform.higgsfield.ai；文件裡也寫了 https://api.higgsfield.ai）。"""
import argparse, json, mimetypes, os, shutil, subprocess, sys, time, uuid, urllib.request, urllib.error

BASE = os.environ.get('HIGGSFIELD_API_BASE', 'https://platform.higgsfield.ai').rstrip('/')
MODELS = {
    # 名稱：圖生影片端點、文生影片端點、CLI 任務型別（用於免費查價）、限制
    'seedance-2.0': {'i2v': 'bytedance/seedance-2.0/image-to-video', 't2v': 'bytedance/seedance-2.0/text-to-video',
                     'cli': 'seedance_2_0', 'dur': (4, 15), 'res': ['480p', '720p', '1080p', '4k'], 'audio': True,
                     'end_image': True},
    'seedance-2.5': {'i2v': 'bytedance/seedance-2.5/image-to-video', 't2v': 'bytedance/seedance-2.5/text-to-video',
                     'cli': 'seedance_2_5', 'dur': (4, 30), 'res': ['480p', '720p', '1080p'], 'audio': True,
                     'end_image': True},
    'kling-3-turbo': {'i2v': 'kling-video/v3.0-turbo/image-to-video', 't2v': None, 'cli': 'kling3_0_turbo',
                      'dur': (3, 15), 'res': ['720p', '1080p'], 'audio': False, 'end_image': False},
}


def load_key():
    k = os.environ.get('HIGGSFIELD_API_KEY')
    if not k and os.environ.get('HF_API_KEY_ID') and os.environ.get('HF_API_KEY_SECRET'):
        k = os.environ['HF_API_KEY_ID'] + ':' + os.environ['HF_API_KEY_SECRET']
    if not k:
        for d in (os.getcwd(), os.path.dirname(os.getcwd())):
            p = os.path.join(d, '.env')
            if os.path.exists(p):
                for line in open(p):
                    if line.strip().startswith('HIGGSFIELD_API_KEY='):
                        k = line.split('=', 1)[1].strip().strip('"').strip("'")
    return k or None


def call(method, url, body=None, key=None, headers=None, raw=None):
    h = {'Content-Type': 'application/json'}
    if key:
        h['Authorization'] = 'Key ' + key
    h.update(headers or {})
    data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            txt = r.read().decode() or '{}'
            return r.status, (json.loads(txt) if txt.strip().startswith(('{', '[')) else {})
    except urllib.error.HTTPError as e:
        txt = e.read().decode(errors='replace')
        try:
            return e.code, json.loads(txt)
        except Exception:
            return e.code, {'detail': txt[:300]}


def payload(m, a, image_url=None, end_url=None):
    body = {'duration': int(a.duration), 'resolution': a.resolution}
    if a.prompt:
        body['prompt'] = a.prompt
    if image_url:
        body['image_url'] = image_url
    if end_url and MODELS[m]['end_image']:
        body['end_image_url'] = end_url
    if MODELS[m]['audio']:
        body['generate_audio'] = False      # 聲音在剪輯時加，不燒進每個片段
    if not image_url and getattr(a, 'aspect', None):
        body['aspect_ratio'] = a.aspect
    return body


def endpoint(m, text):
    ep = MODELS[m]['t2v' if text else 'i2v']
    if not ep:
        sys.exit(f'{m} 不支持文生影片。沒有照片的片段請用 seedance-2.0。')
    return ep


def estimate(m, a, key):
    """返回 (credit 數或 None, 這個數字的來源)。絕不花費任何東西。"""
    text = getattr(a, 'text', False)
    if key:
        body = payload(m, a, None if text else 'https://example.com/placeholder.jpg')
        code, r = call('POST', f'{BASE}/estimate/{endpoint(m, text)}', body, key)
        if code == 200 and 'credits' in r:
            return float(r['credits']), 'Higgsfield API 估價'
        if code == 401:
            return None, '金鑰被拒絕 (401)。請到 https://console.higgsfield.ai 檢查'
    if shutil.which('higgsfield'):
        # Higgsfield CLI 也能免費給任務報價；我們不傳送圖片，只傳送引數
        cmd = ['higgsfield', 'generate', 'cost', MODELS[m]['cli'], '--prompt', a.prompt or 'camera move',
               '--duration', str(a.duration), '--resolution', a.resolution, '--json']
        r = subprocess.run(cmd, capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=60)
        try:
            return float(json.loads(r.stdout)['credits']), 'Higgsfield CLI 查價'
        except Exception:
            pass
    return None, '設定金鑰之前無法得知'


def upload(path, key):
    ctype = mimetypes.guess_type(path)[0] or 'image/jpeg'
    code, r = call('POST', f'{BASE}/files/generate-upload-url', {'content_type': ctype}, key)
    if code != 200:
        sys.exit(f'獲取上傳網址失敗 ({code})：{r.get("detail")}')
    hdrs = dict(r.get('upload_headers') or {'Content-Type': ctype})
    req = urllib.request.Request(r['upload_url'], data=open(path, 'rb').read(), method='PUT', headers=hdrs)
    with urllib.request.urlopen(req, timeout=300):
        pass
    return r['public_url']


def main():
    ap = argparse.ArgumentParser(description='為素材模式呼叫 Higgsfield API（從不印出金鑰）')
    ap.add_argument('cmd', choices=['check', 'estimate', 'generate'], help='check：查金鑰；estimate：估價（免費）；generate：生成（花 credit）')
    ap.add_argument('--model', default='seedance-2.0', choices=sorted(MODELS), help='模型')
    ap.add_argument('--image', help='起始照片')
    ap.add_argument('--end-image', help='結束幀照片（僅部分模型支持）')
    ap.add_argument('--prompt', default='', help='提示詞')
    ap.add_argument('--duration', type=int, default=5, help='秒數')
    ap.add_argument('--resolution', default='720p', help='解析度')
    ap.add_argument('--aspect', default='16:9', help='畫面比例（僅文生影片）')
    ap.add_argument('--text', action='store_true', help='文生影片（不用照片）')
    ap.add_argument('--out', help='輸出的 mp4 路徑')
    ap.add_argument('--yes', action='store_true', help='我已獲准花費 credit')
    a = ap.parse_args()
    key = load_key()
    if a.cmd == 'check':
        print('金鑰：有（已隱藏）' if key else '金鑰：沒有。把 HIGGSFIELD_API_KEY 加到 shell 或 .env 檔案裡。千萬不要貼到聊天裡。')
        return
    m = a.model
    lo, hi = MODELS[m]['dur']
    if not lo <= a.duration <= hi or a.resolution not in MODELS[m]['res']:
        sys.exit(f'{m} 支持 {lo} 到 {hi} 秒，解析度 {", ".join(MODELS[m]["res"])}。')
    if a.cmd == 'estimate':
        c, src = estimate(m, a, key)
        print(json.dumps({'model': m, 'duration': a.duration, 'resolution': a.resolution,
                          'credits': c, 'source': src}, ensure_ascii=False))
        return
    # generate：會花費 credit
    if not a.yes:
        sys.exit('不生成：這會花費 credit。先給對方看分鏡和費用，得到 yes 之後再加 --yes。')
    if not key:
        sys.exit('沒有金鑰。把 HIGGSFIELD_API_KEY 加到 shell 或 .env 檔案裡（絕不放進聊天）。')
    if not a.out:
        sys.exit('需要 --out path/for/clip.mp4')
    text = a.text or not a.image
    image_url = None if text else upload(a.image, key)
    end_url = upload(a.end_image, key) if a.end_image else None
    body = payload(m, a, image_url, end_url)
    code, r = call('POST', f'{BASE}/{endpoint(m, text)}', body, key, {'Idempotency-Key': str(uuid.uuid4())})
    if code not in (200, 201, 202) or 'status_url' not in r:
        sys.exit(f'提交失敗 ({code})：{r.get("detail", r)}')
    print(f'已提交，請求 {r["request_id"]}。等待中（通常 1 到 4 分鐘）……', flush=True)
    delay, t0 = 2.0, time.time()
    while True:
        code, s = call('GET', r['status_url'], None, key)
        if code == 200 and s.get('status') in ('completed', 'failed', 'nsfw', 'canceled'):
            break
        if code in (401, 404):
            sys.exit(f'狀態查詢失敗 ({code})：{s.get("detail")}')
        if time.time() - t0 > 1200:
            sys.exit(f'20 分鐘後仍在執行。請求 id：{r["request_id"]}')
        time.sleep(delay)
        delay = min(delay * 1.5, 10.0)
    if s['status'] != 'completed':
        sys.exit(f'生成結果 {s["status"]}：{s.get("error") or ""}（失敗的任務不收費）')
    url = (s.get('video') or {}).get('url')
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    urllib.request.urlretrieve(url, a.out)
    print(f'已儲存 {a.out}')


if __name__ == '__main__':
    main()
