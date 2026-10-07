# Puts the face bubble, a play button and a label on each booking-page screenshot.
import json
from PIL import Image, ImageDraw, ImageFont, ImageFilter
people = json.load(open('tools/thumbs/people.json'))
face = Image.open('tools/thumbs/face.png').convert('RGB')
cx, cy, r = 158, 172, 124
face = face.crop((cx - r, cy - r, cx + r, cy + r))
try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 26)
except OSError: f = ImageFont.load_default()
for o in people:
    img = Image.open(f"tools/thumbs/out/{o['slug']}.png").convert('RGB').resize((1280, 720), Image.LANCZOS)
    W, H = img.size; S = 4
    D = 200; fx, fy = W - D - 32, H - D - 32
    mask = Image.new('L', (D*S, D*S), 0); ImageDraw.Draw(mask).ellipse((0, 0, D*S-1, D*S-1), fill=255)
    ring = Image.new('L', ((D+12)*S, (D+12)*S), 0); ImageDraw.Draw(ring).ellipse((0, 0, (D+12)*S-1, (D+12)*S-1), fill=255)
    img.paste(Image.new('RGB', (D+12, D+12), (255, 255, 255)), (fx-6, fy-6), ring.resize((D+12, D+12), Image.LANCZOS))
    img.paste(face.resize((D, D), Image.LANCZOS), (fx, fy), mask.resize((D, D), Image.LANCZOS))
    PX, PY = 1100, 250  # centre of the studio's photo
    P = 130; px, py = PX - P//2, PY - P//2
    pl = Image.new('RGBA', (P*S, P*S), (0, 0, 0, 0)); d = ImageDraw.Draw(pl); t = P*S
    d.ellipse((0, 0, t-1, t-1), fill=(139, 30, 70, 238))
    d.polygon([(t*.40, t*.30), (t*.40, t*.70), (t*.72, t*.50)], fill=(255, 255, 255, 255))
    pl = pl.resize((P, P), Image.LANCZOS)
    sh = Image.new('RGBA', (P+40, P+40), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse((20, 24, P+20, P+24), fill=(0, 0, 0, 110)); sh = sh.filter(ImageFilter.GaussianBlur(10))
    img = img.convert('RGBA'); img.alpha_composite(sh, (px-20, py-20)); img.alpha_composite(pl, (px, py))
    txt = f"A 2-min video for {o['first']}"; d = ImageDraw.Draw(img); tw = d.textlength(txt, font=f)
    bx = int(min(PX - tw/2 - 22, W - tw - 44 - 16)); by = py + P + 16
    d.rounded_rectangle((bx, by, bx + tw + 44, by + 50), radius=25, fill=(28, 18, 23, 235)); d.text((bx + 22, by + 10), txt, font=f, fill=(255, 255, 255))
    img.convert('RGB').resize((960, 540), Image.LANCZOS).save(f"thumbs/booking-{o['slug']}.jpg", quality=84, optimize=True)
    print('made', o['slug'])
