# -*- coding: utf-8 -*-
"""Crops and resizes the photo masters into web-ready images.

    pip install Pillow
    python3 tools/images/process.py

Each master in tools/images/masters/ is cut into the crops listed in CROPS,
and every crop is written at each width as both WebP (small) and JPEG (for
older phones and browsers that cannot show WebP). Output goes to
assets/img/photos/. To swap a photo, replace the master with an image of the
same name, adjust its crop box if needed, and run this again.
"""
import json, os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
MASTERS = os.path.join(HERE, 'masters')
OUT = os.path.join(HERE, '..', '..', 'assets', 'img', 'photos')

# name: (master, crop box in master pixels or None for the full frame, widths)
# Masters are 1672 x 941.
WIDE = (800, 1400)
CROPS = {
    'port-crane-tall':     ('port-crane',      (420, 0, 1238, 941),  (640, 1000)),
    'fleet-tall':          ('fleet',           (0, 0, 753, 941),     (600, 900)),
    'warehouse-team-tall': ('warehouse-team',  (830, 0, 1583, 941),  (600, 900)),
    'reach-stacker':       ('reach-stacker',   None, WIDE),
    'customs-counter':     ('customs-counter', None, WIDE),
    'gate-check':          ('gate-check',      None, WIDE),
    'warehouse-aisle':     ('warehouse-aisle', None, WIDE),
    'sealed-container':    ('sealed-container',None, WIDE),
    'highway-truck':       ('highway-truck',   None, WIDE),
    'fleet':               ('fleet',           None, WIDE),
}


def main():
    os.makedirs(OUT, exist_ok=True)
    manifest = {}
    for name, (master, box, widths) in CROPS.items():
        im = Image.open(os.path.join(MASTERS, master + '.jpg')).convert('RGB')
        if box:
            im = im.crop(box)
        sizes = []
        for w in widths:
            w = min(w, im.width)
            h = round(im.height * w / im.width)
            r = im.resize((w, h), Image.LANCZOS)
            r.save(os.path.join(OUT, f'{name}-{w}.webp'), quality=78, method=6)
            r.save(os.path.join(OUT, f'{name}-{w}.jpg'), quality=80, optimize=True, progressive=True)
            sizes.append([w, h])
        manifest[name] = sizes
    with open(os.path.join(HERE, '..', 'photos.json'), 'w') as f:
        json.dump(manifest, f, indent=1)
    for name, s in manifest.items():
        print(f'{name:22}', ', '.join(f'{w}x{h}' for w, h in s))


def font(path, size, weight, width=100):
    f = ImageFont.truetype(path, size)
    try:
        f.set_variation_by_axes([weight, width])
    except OSError:
        pass
    return f


def og_card():
    """1200x630 link preview for WhatsApp, Facebook and others: photo right, brand left."""
    root = os.path.join(HERE, '..', '..')
    ARCHIVO = os.path.join(root, 'assets', 'fonts', 'archivo-var.woff2')
    MONO = os.path.join(root, 'assets', 'fonts', 'jetbrains-mono-500.woff2')
    NIGHT, GOLD, WHITE, SOFT = (6, 28, 19), (245, 197, 24), (255, 255, 255), (196, 212, 203)
    W, H, PX = 1200, 630, 520          # photo occupies x >= PX

    card = Image.new('RGB', (W, H), NIGHT)
    photo = Image.open(os.path.join(MASTERS, 'port-crane.jpg')).convert('RGB')
    pw = W - PX
    cw = round(photo.height * pw / H)
    photo = photo.crop((300, 0, 300 + cw, photo.height)).resize((pw, H), Image.LANCZOS)
    # Blend the photo in over its first 300px: transparent at its left edge, opaque from there on.
    mask = Image.new('L', (pw, H), 255)
    ramp = Image.new('L', (300, H))
    ramp.putdata([round(255 * (x / 299) ** 1.6) for y in range(H) for x in range(300)])
    mask.paste(ramp, (0, 0))
    card.paste(photo, (PX, 0), mask)

    d = ImageDraw.Draw(card)
    logo = Image.open(os.path.join(root, 'assets', 'img', 'logo-mark.png')).convert('RGBA')
    logo = logo.resize((150, round(logo.height * 150 / logo.width)), Image.LANCZOS)
    card.paste(logo, (64, 62), logo)

    x, y = 64, 170
    size = 58                                   # largest size that keeps the wordmark on the dark panel
    while True:
        brand = font(ARCHIVO, size, 800, 118)
        if d.textlength('PEAK LOGISTICS', font=brand) <= PX - x - 36 or size <= 30:
            break
        size -= 1
    d.text((x, y), 'PEAK', font=brand, fill=GOLD)
    d.text((x + d.textlength('PEAK ', font=brand), y), 'LOGISTICS', font=brand, fill=WHITE)
    d.text((x + 2, y + size + 18), 'S E R V I C E S   ·   L I B E R I A', font=font(MONO, 17, 500), fill=GOLD)

    head = font(ARCHIVO, 40, 700, 104)
    d.text((x, 300), 'Your cargo.', font=head, fill=WHITE)
    d.text((x, 348), 'Our commitment.', font=head, fill=GOLD)
    body = font(ARCHIVO, 22, 450)
    d.text((x, 420), 'Freight forwarding · Customs clearing', font=body, fill=SOFT)
    d.text((x, 450), 'Supply chain · Air, sea, road & rail', font=body, fill=SOFT)

    for i in range(0, 380, 36):                                      # the dashed road
        d.rounded_rectangle((x + i, 512, x + i + 22, 516), radius=2, fill=GOLD)
    d.text((x, 540), '+231 886 826 289  ·  Monrovia', font=font(MONO, 20, 500), fill=WHITE)

    out = os.path.join(root, 'assets', 'img', 'og-card.jpg')
    card.save(out, quality=86, optimize=True, progressive=True)
    print('og-card', card.size, os.path.getsize(out) // 1024, 'KB')


if __name__ == '__main__':
    main()
    og_card()
