# Saves a still frame and a small moving copy of each studio's Sendspark preview, so the send kit can show them.
import json, urllib.request, io
from PIL import Image
for o in json.load(open('tools/thumbs/spark.json')):
    try:
        req = urllib.request.Request(o['gif'], headers={'User-Agent': 'Mozilla/5.0'})
        data = urllib.request.urlopen(req, timeout=60).read()
        im = Image.open(io.BytesIO(data))
        frames = []
        try:
            n = 0
            while True:
                im.seek(n); frames.append(im.convert('RGB').copy()); n += 1
        except EOFError:
            pass
        mid = frames[len(frames) // 3] if frames else im.convert('RGB')
        w = 640; h = round(mid.height * w / mid.width)
        mid.resize((w, h), Image.LANCZOS).save(f"thumbs/spark-{o['slug']}.jpg", quality=80, optimize=True)
        print('ok', o['slug'], len(frames), 'frames')
    except Exception as e:
        print('fail', o['slug'], e)
