#!/usr/bin/env python3
"""Render the 25 November 2026 world-news infographic.

Reads nothing from the network. Draws a single-column newspaper page
with Pillow and writes asset/entry.png (1024 x 1024, PNG).
Run: python3 render.py
"""

import hashlib
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "asset", "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 26, 34)
GOLD = (176, 141, 60)
RED = (178, 34, 34)
GREY = (92, 88, 80)
LIGHT_LINE = (205, 198, 184)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy wrap on pixel width; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


STORIES = [
    (
        "NVIDIA RALLY FADES",
        "Huang apologises to staff and says he is in daily therapy; "
        "shares slide after Monday's 31% comeback jump.",
    ),
    (
        "UKRAINE ADMITS SEA STRIKE",
        "Zelenskiy confirms a drone hit on a Russian cargo ship in the "
        "Gulf of Finland; ally Norway urges caution.",
    ),
    (
        "RIYADH TOWER HIT AGAIN",
        "Houthis strike the Saudi capital's tallest skyscraper, 11 hurt "
        "— the second attack on the landmark in under a week.",
    ),
    (
        "CHINA PROBES TOP OFFICIAL",
        "Politburo member Chen Jining, Shanghai party chief, is placed "
        "under investigation for suspected serious violations.",
    ),
    (
        "US READIES NEW TARIFFS",
        "Washington plans higher tariffs on India, China and 14 other "
        "economies as early as this week, the Journal reports.",
    ),
    (
        "SHENZHOU-24 LIFTS OFF",
        "China launches its crewed spacecraft from Jiuquan at dawn, "
        "bound for the Tiangong space station.",
    ),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead banner ---
    banner_h = 168
    d.rectangle([0, 0, W, banner_h], fill=INK)
    title_f = font(FONT_BOLD, 58)
    d.text((48, 26), "THE WORLD IN ONE DAY", font=title_f, fill=PAPER)
    date_f = font(FONT_BOLD, 30)
    d.text((48, 104), "25 NOVEMBER 2026 · WEDNESDAY", font=date_f, fill=GOLD)
    d.rectangle([0, banner_h, W, banner_h + 6], fill=GOLD)

    # --- stories ---
    head_f = font(FONT_BOLD, 30)
    body_f = font(FONT_REG, 25)
    num_f = font(FONT_BOLD, 26)
    x_text = 132
    text_w = W - x_text - 48
    y = banner_h + 34
    row_h = 118
    for i, (head, body) in enumerate(STORIES, 1):
        # numbered red disc
        cx, cy, r = 82, y + 34, 30
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
        label = str(i)
        lw = d.textlength(label, font=num_f)
        d.text((cx - lw / 2, cy - 19), label, font=num_f, fill=(255, 255, 255))
        # headline + body, wrapped to two lines each
        d.text((x_text, y), head, font=head_f, fill=INK)
        lines = wrap(d, body, body_f, text_w)[:2]
        by = y + 44
        for line in lines:
            d.text((x_text, by), line, font=body_f, fill=GREY)
            by += 32
        # hairline between stories, except after the last one
        if i < len(STORIES):
            d.line([(48, y + row_h - 14), (W - 48, y + row_h - 14)],
                   fill=LIGHT_LINE, width=2)
        y += row_h

    # overflow guard: the last story must end above the footer
    footer_h = 74
    assert y <= H - footer_h - 8, "stories overflow into the footer"

    # --- footer ---
    d.rectangle([0, H - footer_h - 6, W, H - footer_h], fill=GOLD)
    d.rectangle([0, H - footer_h, W, H], fill=INK)
    foot_f = font(FONT_REG, 22)
    d.text((48, H - footer_h + 14),
           "Six stories that defined Wednesday, 25 November 2026",
           font=foot_f, fill=PAPER)
    d.text((48, H - footer_h + 44),
           "Sources: Reuters, AP, SCMP, The Japan Times, ECNS, WSJ",
           font=foot_f, fill=GOLD)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, format="PNG")
    with open(OUT, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    size = os.path.getsize(OUT)
    print(f"wrote {OUT} ({size} bytes, sha256 {digest})")
    assert size <= 1024 * 1024, "image over the 1 MiB limit"
    print("render ok")


if __name__ == "__main__":
    main()
