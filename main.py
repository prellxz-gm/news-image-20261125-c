#!/usr/bin/env python3
"""news-image-20261125 variant C — "Timeline + Proof".

Draws a 1024x1024 front page for Wednesday, 25 November 2026 entirely
with PIL: a date banner, a hero illustration of the Hormuz tanker fire,
a chronological timeline spine through the day, and a grid of six more
stories. Every story carries a source tag. Fully deterministic: no
timestamps, no randomness, no date calls — the date is a fixed string.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (246, 241, 231)
CARD = (255, 255, 255)
NAVY = (16, 39, 63)
NAVY_LIGHT = (31, 68, 99)
GOLD = (201, 162, 39)
GOLD_DARK = (160, 124, 22)
RED = (178, 38, 30)
INK = (26, 26, 26)
MUTED = (90, 90, 90)
LINE = (200, 190, 170)
SEA = (22, 57, 79)
SEA_DARK = (14, 42, 60)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_center(draw, cx, y, text, fnt, fill):
    w = fnt.getlength(text)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


def draw_spaced(draw, cx, y, text, fnt, fill, tracking=6):
    """Draw text with extra tracking between characters, centred."""
    widths = [fnt.getlength(ch) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking


def draw_source_tag(draw, x, y, text):
    """Small outlined source tag; returns its width."""
    fnt = SANS_B(12)
    pad_x, pad_y = 7, 3
    w = fnt.getlength(text) + pad_x * 2
    h = 20
    draw.rounded_rectangle([x, y, x + w, y + h], radius=4,
                           outline=MUTED, width=1)
    draw.text((x + pad_x, y + pad_y + 1), text, font=fnt, fill=MUTED)
    return w


# ---------------------------------------------------------------- hero art
def draw_hero_art(draw, x0, y0, x1, y1):
    """Stylised flat illustration: tanker burning in the Strait of Hormuz."""
    iw, ih = x1 - x0, y1 - y0
    horizon = y0 + int(ih * 0.58)

    # Dusk sky gradient.
    top = (246, 178, 94)
    bot = (217, 95, 43)
    for i in range(horizon - y0):
        t = i / max(1, horizon - y0 - 1)
        col = tuple(int(top[c] + (bot[c] - top[c]) * t) for c in range(3))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=col)

    # Low sun.
    draw.ellipse([x1 - 118, y0 + 26, x1 - 58, y0 + 86], fill=(250, 226, 160))
    # Distant tanker silhouette on the horizon.
    draw.rectangle([x0 + 30, horizon - 16, x0 + 150, horizon - 4],
                   fill=(120, 62, 40))
    draw.rectangle([x0 + 96, horizon - 30, x0 + 118, horizon - 16],
                   fill=(120, 62, 40))

    # Sea.
    draw.rectangle([x0, horizon, x1, y1], fill=SEA)
    for k, wy in enumerate((0.22, 0.48, 0.74, 0.92)):
        yy = horizon + int((y1 - horizon) * wy)
        draw.line([(x0 + 12, yy), (x1 - 12, yy)], fill=(52, 102, 128),
                  width=2)

    # Tanker hull.
    hull_top = horizon + int((y1 - horizon) * 0.18)
    hull_bot = y1 - 44
    draw.polygon([(x0 + 18, hull_top), (x1 - 18, hull_top),
                  (x1 - 52, hull_bot), (x0 + 52, hull_bot)],
                 fill=(28, 30, 36))
    draw.line([(x0 + 18, hull_top), (x1 - 18, hull_top)], fill=(70, 74, 82),
              width=3)
    # Deck containers.
    for i, cx in enumerate((x0 + 70, x0 + 150, x0 + 230)):
        draw.rectangle([cx, hull_top - 26, cx + 66, hull_top - 2],
                       fill=(176, 62, 44) if i % 2 == 0 else (52, 102, 96))
    # Bridge tower and funnel.
    draw.rectangle([x1 - 128, hull_top - 62, x1 - 66, hull_top - 2],
                   fill=(232, 228, 220))
    draw.rectangle([x1 - 122, hull_top - 58, x1 - 72, hull_top - 40],
                   fill=(31, 68, 99))
    draw.rectangle([x1 - 178, hull_top - 44, x1 - 148, hull_top - 2],
                   fill=(201, 162, 39))

    # Flames rising from the deck: one connected fire mass with tongues.
    fx = x0 + int(iw * 0.52)
    draw.ellipse([fx - 78, hull_top - 52, fx + 48, hull_top + 2],
                 fill=(194, 46, 31))
    draw.ellipse([fx - 52, hull_top - 68, fx + 32, hull_top + 2],
                 fill=(232, 106, 28))
    draw.ellipse([fx - 30, hull_top - 58, fx + 12, hull_top + 2],
                 fill=(245, 184, 29))
    draw.polygon([(fx - 58, hull_top - 38), (fx - 44, hull_top - 96),
                  (fx - 28, hull_top - 38)], fill=(232, 106, 28))
    draw.polygon([(fx - 6, hull_top - 42), (fx + 8, hull_top - 100),
                  (fx + 24, hull_top - 42)], fill=(245, 184, 29))

    # Smoke puffs, small and high so they read as smoke, not balloons.
    for (dx, dy, r, col) in ((-58, -118, 13, (110, 110, 110)),
                             (-30, -134, 15, (140, 140, 140)),
                             (2, -122, 12, (110, 110, 110)),
                             (30, -140, 13, (160, 160, 160))):
        draw.ellipse([fx + dx - r, hull_top + dy - r,
                      fx + dx + r, hull_top + dy + r], fill=col)

    # Sea mines in the foreground water, below the hull.
    for (mx, my, r) in ((x0 + 92, y1 - 24, 13), (x1 - 118, y1 - 20, 11)):
        for ang in range(0, 360, 45):
            import math
            ex = mx + int((r + 9) * math.cos(math.radians(ang)))
            ey = my + int((r + 9) * math.sin(math.radians(ang)))
            draw.line([(mx, my), (ex, ey)], fill=(10, 10, 10), width=3)
        draw.ellipse([mx - r, my - r, mx + r, my + r], fill=(12, 12, 12))
        draw.ellipse([mx - r // 2, my - r // 2, mx - r // 6, my - r // 6],
                     fill=(60, 60, 60))

    draw.rectangle([x0, y0, x1, y1], outline=NAVY, width=2)


# ------------------------------------------------------------------- page
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- header banner ----
    d.rectangle([0, 0, W, 132], fill=NAVY)
    draw_center(d, W // 2, 18, "WEDNESDAY, 25 NOVEMBER 2026",
                SERIF_B(44), (255, 255, 255))
    draw_spaced(d, W // 2, 82, "THE WORLD IN ONE DAY", SANS_B(22),
                GOLD, tracking=8)
    d.rectangle([0, 132, W, 136], fill=GOLD)

    # ---- kicker ----
    draw_center(d, W // 2, 146, "SIX FLASHPOINTS  ·  SIX MORE STORIES  ·  ONE DAY",
                SANS_B(15), MUTED)

    # ---- hero panel ----
    d.rectangle([24, 168, 1000, 452], fill=CARD, outline=LINE, width=1)
    draw_hero_art(d, 32, 176, 596, 444)

    hx, hw = 620, 368
    y = 182
    d.text((hx, y), "HORMUZ IN FLAMES", font=SANS_B(16), fill=RED)
    y += 24
    for line in wrap("Two tankers hit mines, explode and burn",
                     SERIF_B(33), hw):
        d.text((hx, y), line, font=SERIF_B(33), fill=INK)
        y += 38
    y += 4
    for line in wrap("Two oil tankers struck sea mines in the Strait "
                     "of Hormuz and caught fire. Iran says ships must "
                     "coordinate with its navy. The strait stays shut "
                     "until the US lifts its blockade.",
                     SANS(16), hw):
        d.text((hx, y), line, font=SANS(16), fill=(52, 52, 52))
        y += 20
    y += 8
    draw_source_tag(d, hx, y, "REUTERS")

    # ---- timeline spine ----
    ty = 460
    d.text((24, ty), "THE DAY IN ORDER", font=SANS_B(16), fill=NAVY)
    d.line([(218, ty + 10), (1000, ty + 10)], fill=GOLD, width=2)

    spine_y = 580
    d.line([(48, spine_y), (976, spine_y)], fill=NAVY, width=3)
    nodes = [
        ("~01:00", "CARTAGENA",
         "All hostages freed in dawn raid", "Reuters / AFP"),
        ("08:18", "SHENZHOU-24",
         "Long March lifts off from Jiuquan", "Reuters / Xinhua"),
        ("11:56", "TIANGONG DOCKING",
         "Pakistan's first astronaut aboard", "Reuters / Xinhua"),
        ("MIDDAY", "HORMUZ",
         "Two tankers hit mines, burn", "Reuters"),
        ("AFTERNOON", "YEMEN WAR",
         "Ras Tanura + Riyadh hit; Hodeidah struck", "Reuters / WireMinute"),
        ("BY THE CLOSE", "MARKETS SLIDE",
         "Nasdaq futures -2%+ on tariff threat", "Reuters"),
    ]
    col_w = 928 / len(nodes)
    for i, (time, title, desc, src) in enumerate(nodes):
        cx = 48 + col_w * i + col_w / 2
        d.ellipse([cx - 7, spine_y - 7, cx + 7, spine_y + 7], fill=RED,
                  outline=(255, 255, 255), width=2)
        above = (i % 2 == 0)
        lines = wrap(desc, SANS(13), col_w - 12)
        block_h = 20 + 16 + len(lines) * 16 + 14
        if above:
            base = spine_y - 14 - block_h
            d.line([(cx, spine_y - 7), (cx, base + block_h)], fill=NAVY,
                   width=1)
        else:
            base = spine_y + 16
            d.line([(cx, spine_y + 7), (cx, base)], fill=NAVY, width=1)
        yy = base
        draw_center(d, cx, yy, time, SANS_B(17), NAVY)
        yy += 20
        draw_center(d, cx, yy, title, SANS_B(13), RED)
        yy += 16
        for line in lines:
            draw_center(d, cx, yy, line, SANS(13), INK)
            yy += 16
        draw_center(d, cx, yy, src, SANS(11), MUTED)

    # ---- supporting grid ----
    gy = 688
    d.text((24, gy), "ALSO TODAY", font=SANS_B(16), fill=NAVY)
    d.line([(158, gy + 10), (1000, gy + 10)], fill=GOLD, width=2)

    stories = [
        ("Garment wage up 36% in Bangladesh",
         "Raise follows weeks of textile-worker protests.",
         "WireMinute"),
        ("Australia–Solomon security pact signed",
         "Wide pact bars foreign bases; a shift away from China.",
         "WireMinute"),
        ("Russian jets enter Korean air zone",
         "Seoul reports the incursion into its air defence zone.",
         "SRI"),
        ("3 bodies found in flooded Bogor mine",
         "26 miners still trapped ~100 m down in Pongkor.",
         "Reuters"),
        ("Tai Po fire's 168 dead mourned, a year on",
         "Residents return to mark the deadliest fire since 1948.",
         "Reuters"),
        ("Iraq orders seizure of Kurdish oilfields",
         "PM orders federal troops to take oilfields and crossings.",
         "Starlit Daily"),
    ]
    cell_w, cell_h = 476, 88
    for i, (head, summ, src) in enumerate(stories):
        cx0 = 24 + (i % 2) * (cell_w + 8)
        cy0 = 712 + (i // 2) * (cell_h + 6)
        d.rectangle([cx0, cy0, cx0 + cell_w, cy0 + cell_h], fill=CARD,
                    outline=LINE, width=1)
        d.text((cx0 + 14, cy0 + 10), head, font=SANS_B(17), fill=INK)
        for j, line in enumerate(wrap(summ, SANS(14), cell_w - 28)):
            d.text((cx0 + 14, cy0 + 38 + j * 19), line, font=SANS(14),
                   fill=(52, 52, 52))
        tag_w = SANS_B(12).getlength(src) + 14
        d.text((cx0 + cell_w - 14 - tag_w, cy0 + cell_h - 24), src,
               font=SANS_B(12), fill=MUTED)

    # ---- footer ----
    draw_center(d, W // 2, 992, "All events 25 November 2026 — sources: "
                "Reuters, AFP, Xinhua", SANS_B(15), NAVY)
    draw_center(d, W // 2, 1010, "Also: WireMinute  ·  SRI  ·  Starlit Daily",
                SANS(12), MUTED)
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    img = build()
    img.save(os.path.join(out_dir, "entry.png"), "PNG")


if __name__ == "__main__":
    main()
