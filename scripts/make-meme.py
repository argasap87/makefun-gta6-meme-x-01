#!/usr/bin/env python3
"""Draw the gta6-meme-x-01 meme: 'Waited 13 years. Downloaded 240 GB.
The ghost got paid first.'

Scene: a Vice City sunset. Jason and Lucia lean on a neon sports car,
watching make.fun's ghost float by, clutching its magenta star coin.
A GTA-style 'BOUNTY COLLECTED' popup delivers the punchline.

The ghost is pasted in from make.fun's own press kit (mark-1024.png),
the white ghost with sparkle eyes on its magenta disc, holding the
magenta coin with the white star. No Rockstar artwork is used: the car,
the figures, the skyline and the palms are all drawn here with PIL.
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(size, bold=True):
    return ImageFont.truetype(BOLD if bold else REG, size)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def sunset(img):
    """Vertical gradient: deep purple dusk at the top, magenta, then
    burning orange at the horizon."""
    d = ImageDraw.Draw(img)
    stops = [(0.0, (38, 8, 64)), (0.35, (122, 20, 110)),
             (0.62, (214, 44, 120)), (0.8, (255, 110, 60)),
             (1.0, (255, 176, 66))]
    for y in range(640):
        t = y / 639
        for i in range(len(stops) - 1):
            t0, c0 = stops[i]
            t1, c1 = stops[i + 1]
            if t0 <= t <= t1:
                d.line([(0, y), (W, y)], fill=lerp(c0, c1, (t - t0) / (t1 - t0)))
                break


def sun(d):
    cx, cy, r = 300, 260, 110
    for i in range(14):
        rr = r + i * 4
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=(255, 200, 120))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 224, 150))
    # retro sun slats across the lower half
    for yy in range(cy + 10, cy + r, 16):
        half = int(math.sqrt(max(0, r * r - (yy - cy) ** 2)))
        d.rectangle([cx - half, yy, cx + half, yy + 7], fill=(214, 44, 120))


def skyline(d, rng):
    """Dark building silhouettes with lit windows along the horizon."""
    base = 640
    x = -20
    while x < W + 40:
        bw = rng.randint(60, 130)
        bh = rng.randint(90, 240)
        top = base - bh
        d.rectangle([x, top, x + bw, base], fill=(24, 6, 40))
        if rng.random() < 0.6:  # rooftop antenna
            d.line([x + bw // 2, top, x + bw // 2, top - 26], fill=(24, 6, 40), width=4)
            d.ellipse([x + bw // 2 - 4, top - 32, x + bw // 2 + 4, top - 24],
                      fill=(255, 80, 120))
        for wy in range(top + 14, base - 12, 22):
            for wx in range(x + 10, x + bw - 10, 20):
                if rng.random() < 0.35:
                    col = rng.choice([(255, 210, 110), (120, 240, 255), (255, 120, 190)])
                    d.rectangle([wx, wy, wx + 9, wy + 12], fill=col)
        x += bw + rng.randint(4, 18)


def palm(d, x, y, s, lean):
    """A simple palm silhouette: curved trunk + fronds."""
    pts = []
    for i in range(9):
        pts.append((x + lean * i * i * 0.12, y - i * s * 0.11))
    d.line(pts, fill=(16, 4, 28), width=max(6, int(s * 0.09)))
    cx, cy = pts[-1]
    for k in range(7):
        ang = math.pi * (0.05 + k * 0.15)
        ex = cx + math.cos(ang) * s * 0.5 * (1 if lean > 0 else -1)
        ey = cy + abs(math.sin(ang)) * s * 0.28 + s * 0.10
        mx = cx + math.cos(ang) * s * 0.26 * (1 if lean > 0 else -1)
        my = cy - s * 0.06
        d.line([cx, cy, mx, my, ex, ey], fill=(16, 4, 28), width=max(3, int(s * 0.035)))


def road(d):
    d.rectangle([0, 640, W, H], fill=(18, 8, 30))
    # wet-road neon reflections
    for x0, w, col in [(90, 130, (255, 60, 160)), (430, 180, (40, 220, 255)),
                       (760, 120, (255, 140, 60))]:
        for i in range(26):
            yy = 646 + i * 8
            d.line([(x0, yy), (x0 + w, yy)], fill=col, width=3)
    d.rectangle([0, 640, W, 646], fill=(255, 120, 90))


def car(d):
    """A low neon sports car, side view, centre of the road band."""
    body = (150, 14, 60)
    d.polygon([(150, 790), (240, 710), (430, 682), (640, 682),
               (760, 722), (880, 760), (880, 800), (150, 800)], fill=body)
    d.polygon([(270, 710), (430, 686), (620, 686), (720, 722), (270, 722)],
              fill=(10, 16, 34))  # glasshouse
    d.polygon([(290, 706), (430, 690), (520, 690), (520, 718), (290, 718)],
              fill=(90, 200, 235))  # windshield glint
    d.polygon([(540, 690), (610, 690), (690, 716), (540, 718)],
              fill=(60, 150, 200))
    d.polygon([(150, 794), (880, 794), (880, 802), (150, 802)], fill=(255, 40, 140))
    for cx in (300, 730):  # wheels
        d.ellipse([cx - 52, 748, cx + 52, 852], fill=(8, 8, 12))
        d.ellipse([cx - 30, 770, cx + 30, 830], fill=(190, 190, 205))
        d.ellipse([cx - 12, 788, cx + 12, 812], fill=(30, 30, 40))
    d.ellipse([852, 738, 884, 762], fill=(255, 240, 160))  # headlight
    d.rectangle([158, 748, 176, 766], fill=(255, 60, 60))  # taillight
    # magenta underglow
    for i in range(8):
        d.line([(170, 856 + i * 2), (860, 856 + i * 2)],
               fill=(255, 40, 160), width=2)


def figure(d, x, y, s, kind):
    """A flat-style figure seen from behind, leaning on the car and
    looking up at the ghost. kind: 'jason' (cap, tank top) or 'lucia'
    (long dark hair, red top)."""
    if kind == "jason":
        skin, top, pants, hair = (196, 140, 100), (240, 240, 235), (40, 60, 110), (30, 22, 16)
    else:
        skin, top, pants, hair = (214, 164, 120), (220, 30, 60), (20, 20, 28), (24, 12, 10)
    # legs
    d.polygon([(x - 26 * s, y), (x - 8 * s, y), (x - 4 * s, y - 95 * s),
               (x - 24 * s, y - 95 * s)], fill=pants)
    d.polygon([(x + 8 * s, y), (x + 26 * s, y), (x + 24 * s, y - 95 * s),
               (x + 4 * s, y - 95 * s)], fill=pants)
    # torso, leaning slightly
    d.polygon([(x - 30 * s, y - 92 * s), (x + 30 * s, y - 92 * s),
               (x + 24 * s, y - 175 * s), (x - 24 * s, y - 175 * s)], fill=top)
    # arms: one on the car, one raised toward the ghost
    d.line([(x + 22 * s, y - 165 * s), (x + 58 * s, y - 130 * s)], fill=skin, width=int(13 * s))
    d.line([(x - 22 * s, y - 165 * s), (x - 48 * s, y - 118 * s)], fill=skin, width=int(13 * s))
    # head
    d.ellipse([x - 22 * s, y - 218 * s, x + 22 * s, y - 174 * s], fill=skin)
    if kind == "jason":
        d.pieslice([x - 24 * s, y - 224 * s, x + 24 * s, y - 186 * s], 180, 360,
                   fill=(200, 30, 40))  # cap dome, seen from behind
    else:
        d.pieslice([x - 24 * s, y - 226 * s, x + 24 * s, y - 180 * s], 180, 360, fill=hair)
        d.polygon([(x - 24 * s, y - 200 * s), (x - 30 * s, y - 150 * s),
                   (x - 8 * s, y - 165 * s), (x - 12 * s, y - 200 * s)], fill=hair)
        d.polygon([(x + 24 * s, y - 200 * s), (x + 30 * s, y - 150 * s),
                   (x + 8 * s, y - 165 * s), (x + 12 * s, y - 200 * s)], fill=hair)


def outline_text(d, xy, text, fnt, fill, stroke=(0, 0, 0), sw=6):
    d.text(xy, text, font=fnt, fill=fill, anchor="ma",
           stroke_width=sw, stroke_fill=stroke)


def main():
    rng = random.Random(619)
    img = Image.new("RGB", (W, H), (38, 8, 64))
    d = ImageDraw.Draw(img)
    sunset(img)
    sun(d)
    skyline(d, rng)
    palm(d, 40, 640, 190, lean=1)
    palm(d, 1000, 640, 170, lean=-1)
    road(d)
    car(d)
    figure(d, 290, 860, 1.0, "jason")
    figure(d, 700, 860, 0.95, "lucia")

    # The ghost: make.fun's own mascot, large and unmissable, floating
    # over the scene with its magenta star coin.
    ghost = Image.open(os.path.join(ROOT, "assets", "mark-1024.png")).convert("RGBA")
    ghost = ghost.resize((320, 320), Image.LANCZOS).rotate(-8, expand=True,
                                                          resample=Image.BICUBIC)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([600, 160, 980, 540], fill=(255, 40, 160, 60))
    img = Image.alpha_composite(img.convert("RGBA"), glow)
    img.paste(ghost, (620, 180), ghost)
    d = ImageDraw.Draw(img)

    # Top caption: the setup, two big beats.
    outline_text(d, (W // 2, 18), "WAITED 13 YEARS.", font(72), (255, 255, 255))
    outline_text(d, (W // 2, 96), "DOWNLOADED 240 GB.", font(72), (255, 220, 90))

    # GTA-style popup: black slab, yellow headline, white subline.
    d.rounded_rectangle([110, 878, 914, 1006], radius=18,
                        fill=(0, 0, 0), outline=(255, 215, 0), width=5)
    d.text((512, 892), "★ BOUNTY COLLECTED ★", font=font(46), fill=(255, 215, 0),
           anchor="ma")
    d.text((512, 946), "THE GHOST GOT PAID FIRST — make.fun",
           font=font(30), fill=(255, 255, 255), anchor="ma")

    out = os.path.join(ROOT, "meme.png")
    img.convert("RGB").save(out, "PNG")
    print("wrote", out)


if __name__ == "__main__":
    main()
