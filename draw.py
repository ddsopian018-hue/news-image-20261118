#!/usr/bin/env python3
"""Draw the front page for Wednesday 18 November 2026.

A newspaper-style summary of the day's world news, drawn entirely with
PIL shapes and text: no photos, no network. Run: python3 draw.py
Writes entry.png (1024x1024, under 1 MiB) next to this file.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 243, 230)
INK = (17, 17, 17)
RED = (176, 42, 32)
BLUE = (31, 78, 121)
GREY = (90, 90, 86)
LIGHT = (233, 226, 208)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, color=INK):
    """Draw wrapped text; return y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def kicker(draw, x, y, text, color=RED):
    draw.text((x, y), text, font=font(SANSB, 19), fill=color)
    return y + 26


def rule(draw, y, x0=36, x1=988, width=2, color=INK):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


def flag_us(draw, x, y, w=62, h=40):
    for i in range(7):
        draw.rectangle([x, y + i * h // 7, x + w, y + (i + 1) * h // 7],
                       fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    draw.rectangle([x, y, x + int(w * 0.42), y + int(h * 0.55)], fill=(30, 50, 110))
    for r in range(3):
        for c in range(4):
            draw.ellipse([x + 4 + c * 8, y + 4 + r * 7, x + 7 + c * 8, y + 7 + r * 7],
                         fill=(255, 255, 255))
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def flag_jp(draw, x, y, w=62, h=40):
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    draw.ellipse([x + w // 2 - 11, y + h // 2 - 11, x + w // 2 + 11, y + h // 2 + 11],
                 fill=(188, 0, 45))
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def flag_in(draw, x, y, w=62, h=40):
    draw.rectangle([x, y, x + w, y + h // 3], fill=(255, 153, 51))
    draw.rectangle([x, y + h // 3, x + w, y + 2 * h // 3], fill=(255, 255, 255))
    draw.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(19, 136, 8))
    draw.ellipse([x + w // 2 - 6, y + h // 2 - 6, x + w // 2 + 6, y + h // 2 + 6],
                 outline=(0, 0, 128), width=2)
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def flag_au(draw, x, y, w=62, h=40):
    draw.rectangle([x, y, x + w, y + h], fill=(0, 40, 104))
    draw.line([(x, y), (x + 30, y + 20)], fill=(255, 255, 255), width=3)
    draw.line([(x + 30, y), (x, y + 20)], fill=(255, 255, 255), width=3)
    for sx, sy in [(50, 8), (52, 30), (38, 18)]:
        draw.ellipse([x + sx - 2, y + sy - 2, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def skyline(draw, x0, y0, x1, y1):
    """Manila skyline at dusk with a sun and a small plane."""
    draw.rectangle([x0, y0, x1, y1], fill=(214, 226, 236))
    draw.ellipse([x1 - 78, y0 + 12, x1 - 28, y0 + 62], fill=(232, 170, 60))
    # plane: small silhouette, fuselage + tail + wing
    px, py = x0 + 28, y0 + 30
    draw.ellipse([px, py, px + 52, py + 9], fill=INK)
    draw.polygon([(px + 44, py + 2), (px + 52, py - 10), (px + 56, py + 2)], fill=INK)
    draw.polygon([(px + 20, py + 4), (px + 30, py + 16), (px + 36, py + 4)], fill=INK)
    # buildings
    heights = [0.42, 0.66, 0.52, 0.80, 0.58, 0.72, 0.46, 0.62]
    bw = (x1 - x0) // len(heights)
    for i, frac in enumerate(heights):
        bx = x0 + i * bw + 2
        top = y1 - int((y1 - y0) * frac)
        draw.rectangle([bx, top, bx + bw - 4, y1], fill=(52, 74, 96))
        for wy in range(top + 10, y1 - 8, 16):
            for wx in range(bx + 6, bx + bw - 10, 12):
                draw.rectangle([wx, wy, wx + 4, wy + 6], fill=(240, 220, 130))
    draw.rectangle([x0, y1 - 4, x1, y1], fill=(52, 74, 96))


def cyclone(draw, cx, cy, r):
    """Spiral storm: nested arcs in storm blue."""
    for k in range(5):
        rr = r - k * (r // 5)
        draw.arc([cx - rr, cy - rr, cx + rr, cy + rr],
                 start=40 + k * 55, end=300 + k * 55, fill=(31, 78, 121), width=5)
    draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(248, 243, 230),
                 outline=(31, 78, 121), width=3)


def chart(draw, x0, y0, x1, y1):
    """Falling market line, red, with grid and axes."""
    draw.rectangle([x0, y0, x1, y1], fill=(255, 255, 255), outline=GREY, width=1)
    for gy in (y0 + 26, y0 + 44, y0 + 62):
        draw.line([(x0, gy), (x1, gy)], fill=(220, 220, 215), width=1)
    pts = [(x0 + 8, y0 + 22), (x0 + 60, y0 + 30), (x0 + 110, y0 + 28),
           (x0 + 160, y0 + 42), (x0 + 210, y0 + 48), (x0 + 260, y0 + 58),
           (x0 + 310, y0 + 56), (x0 + 360, y0 + 66)]
    draw.line(pts, fill=RED, width=3, joint="curve")
    draw.ellipse([pts[-1][0] - 4, pts[-1][1] - 4, pts[-1][0] + 4, pts[-1][1] + 4],
                 fill=RED)
    draw.text((x0 + 8, y0 + 4), "ASX 200  -1.8%", font=font(SANSB, 15), fill=RED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.text((W // 2, 26), "THE WORLD TODAY", font=font(SERIF, 66),
           fill=INK, anchor="ma")
    rule(d, 104, width=3)
    d.text((36, 114), "WEDNESDAY 18 NOVEMBER 2026",
           font=font(SANSB, 21), fill=INK)
    d.text((988, 114), "ONE DAY  ·  ONE PICTURE",
           font=font(SANSB, 21), fill=RED, anchor="ra")
    rule(d, 142, width=2)

    # ---- Lead story: Trump in Manila ----
    y = 156
    y = kicker(d, 36, y, "MANILA  ·  DIPLOMACY")
    for ln in wrap(d, "TRUMP MEETS MARCOS IN MANILA", font(SERIF, 46), 590):
        d.text((36, y), ln, font=font(SERIF, 46), fill=INK)
        y += 54
    y += 6
    y = para(d, 36, y,
             "After a first Quad summit in two years, the US president "
             "meets the Philippines' leader — then flies to Shenzhen "
             "for nuclear talks with Xi and Putin.",
             font(SANS, 21), 560, 27)
    y += 6
    y = para(d, 36, y,
             "Donald Trump landed in Manila on Tuesday, joining the "
             "leaders of Japan, India and Australia at the Quad table. "
             "On Wednesday he holds talks with Ferdinand Marcos Jr. "
             "before heading to China.",
             font(SANS, 19), 560, 25)
    # illustration: skyline + Quad flags
    ix0, iy0, ix1, iy1 = 640, 158, 988, 330
    skyline(d, ix0, iy0, ix1, iy1)
    d.text((ix0, iy1 + 10), "THE QUAD, BACK AT ONE TABLE",
           font=font(SANSB, 16), fill=GREY)
    fx, fy = ix0, iy1 + 36
    for fn in (flag_us, flag_jp, flag_in, flag_au):
        fn(d, fx, fy)
        fx += 74
    d.text((ix0, fy + 48), "US  ·  JAPAN  ·  INDIA  ·  AUSTRALIA",
           font=font(SANSB, 15), fill=INK)

    rule(d, 494, width=2)

    # ---- Row 2: markets + cyclone ----
    y = 510
    # left: markets
    y = kicker(d, 36, y, "MARKETS  ·  BUSINESS")
    for ln in wrap(d, "WALL ST BRACES FOR NVIDIA", font(SERIF, 26), 460):
        d.text((36, y), ln, font=font(SERIF, 26), fill=INK)
        y += 32
    by = y + 6
    by = para(d, 36, by,
              "Asian shares slid as investors awaited Nvidia's results "
              "after the US close.",
              font(SANS, 18), 440, 24)
    chart(d, 36, by + 8, 480, by + 78)
    # right: cyclone
    y2 = 510
    y2 = kicker(d, 524, y2, "WEATHER  ·  BAY OF BENGAL")
    d.text((524, y2), "CYCLONE AKVAN BEARS DOWN", font=font(SERIF, 23), fill=INK)
    cy = y2 + 30
    cy = para(d, 524, cy,
              "India's weather office warned the storm is likely to "
              "become severe by Thursday as it churns towards the coast.",
              font(SANS, 18), 300, 24)
    cyclone(d, 908, 640, 56)

    rule(d, 724, width=2)

    # ---- Row 3: three stories ----
    cols = [
        (36, "TAIWAN", "TAIWAN SEEKS $14BN IN ARMS",
         "Taipei says it urgently needs the arms, as Washington "
         "pressed the UN over Taiwan flight rules."),
        (362, "TRADE  ·  INDIA", "AMAZON BETS $7BN ON GREEN INDIA",
         "The tech giant plans $7bn of renewable-energy investment "
         "in India by 2030."),
        (688, "UKRAINE  ·  DIPLOMACY", "NEW KYIV TALKS, ZELENSKY SAYS",
         "Ukraine's president said fresh talks were held between "
         "Kyiv, Europe and the US."),
    ]
    for x, kick, head, body in cols:
        yy = 738
        yy = kicker(d, x, yy, kick)
        for ln in wrap(d, head, font(SERIF, 23), 288):
            d.text((x, yy), ln, font=font(SERIF, 23), fill=INK)
            yy += 29
        yy += 6
        para(d, x, yy, body, font(SANS, 17), 288, 22)
        if x < 688:
            d.line([(x + 300, 738), (x + 300, 892)], fill=(200, 192, 172), width=1)

    rule(d, 906, width=2)

    # ---- Briefs strip ----
    by = 920
    d.text((36, by), "SPORT", font=font(SANSB, 17), fill=RED)
    d.text((118, by), "UEFA backs France's Diallo to challenge Infantino for the FIFA presidency.",
           font=font(SANS, 17), fill=INK)
    by += 28
    d.text((36, by), "ROME", font=font(SANSB, 17), fill=RED)
    d.text((118, by), "Pope Leo is struck in the eye by a rosary thrown from the crowd in Peru.",
           font=font(SANS, 17), fill=INK)
    by += 28
    d.text((36, by), "TECH", font=font(SANSB, 17), fill=RED)
    d.text((118, by), "Baidu's chief warns of an AI 'bubble' as leaders gather for APEC in Shenzhen.",
           font=font(SANS, 17), fill=INK)

    d.text((W // 2, 1004), "Wednesday 18 November 2026  ·  All stories reported on 18 November 2026  ·  Drawn, not photographed",
           font=font(SANS, 13), fill=GREY, anchor="ma")

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
