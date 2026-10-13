# Wave 2 email picture: the tour's first screen (booking page, phone app and dashboard together)
# with a small "Built for <studio>" label. No face bubble or play button: this wave leads with the setup, not a video.
import json, os
from PIL import Image, ImageDraw, ImageFont
if not os.path.exists('tools/thumbs/setup.json'): raise SystemExit
people = json.load(open('tools/thumbs/setup.json'))
def font(size):
    try: return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', size)
    except OSError: return ImageFont.load_default()
for o in people:
    src = f"tools/thumbs/out/setup-{o['slug']}.png"
    if not os.path.exists(src): continue
    img = Image.open(src).convert('RGB').resize((1280, 720), Image.LANCZOS)
    W, H = img.size
    d = ImageDraw.Draw(img)
    txt = f"Built for {o['studio']}"
    size = 32
    f = font(size)
    while d.textlength(txt, font=f) > W - 160 and size > 18:
        size -= 2; f = font(size)
    tw = d.textlength(txt, font=f); bh = size + 30
    bx, by = 32, H - bh - 32
    d.rounded_rectangle((bx, by, bx + tw + 48, by + bh), radius=bh // 2, fill=(126, 27, 64))
    d.text((bx + 24, by + 14), txt, font=f, fill=(255, 247, 250))
    img.resize((960, 540), Image.LANCZOS).save(f"thumbs/setup-{o['slug']}.jpg", quality=84, optimize=True)
    print('made setup', o['slug'])
