#!/usr/bin/env python3
"""Render the front page for Tuesday 24 November 2026.

Build-time only: runs here on this machine with Pillow and the system
DejaVu fonts, and writes entry.png (1024x1024, under 1 MiB). The graded
program is main.py, which only copies the finished entry.png.

Layout (1024 x 1024, newspaper front page):
  masthead -> lead story (Nvidia/Huang) with a drawn chip illustration
  -> three featured boxes -> UTC timeline of the day as reported
  -> the day in 40 stories (numbered, three columns) -> footer with sources
    and a date check.

Every story on the page happened, or was first reported, on Tuesday
24 November 2026, and was checked against AP, Reuters, AFP, CNN,
Times of India, Bernama-dpa and the News Guild of New York.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (25, 25, 25)
NAVY = (20, 33, 61)
RED = (179, 32, 44)
GREEN = (14, 110, 69)
TEAL = (14, 107, 107)
GREY = (232, 226, 212)
MIDGREY = (110, 104, 90)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
MONO = lambda s: font("DejaVuSansMono.ttf", s)


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if text_w(draw, trial, fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def fit(draw, text, fnt, max_w, max_lines, label):
    """Wrap and assert the text fits; fail loudly so strings get trimmed."""
    lines = wrap(draw, text, fnt, max_w)
    if len(lines) > max_lines:
        raise SystemExit(
            "OVERFLOW %s: %d lines (max %d): %r" % (label, len(lines), max_lines, text)
        )
    return lines


# ---------------------------------------------------------------- stories

LEAD_KICKER = "TECHNOLOGY  ·  LEAD STORY"
LEAD_HEAD = ["HUANG IS BACK", "AT NVIDIA"]
LEAD_DECK = (
    "Nvidia's board reinstates Jensen Huang as CEO; shares surge "
    "31% in a day. A Senate hearing is set for 3 December."
)
LEAD_CAPTION = "Jensen Huang returns to Nvidia HQ"

FEATURED = [
    {
        "color": RED,
        "kicker": "KOREA",
        "head": "Russian jets enter Seoul's air-defence zone",
        "body": "Seoul says Russian aircraft entered its zone; a brief evacuation alert followed.",
    },
    {
        "color": NAVY,
        "kicker": "UKRAINE",
        "head": "Strikes kill 12 near Kyiv",
        "body": "Russian strikes kill at least 12 near Kyiv; Ukraine hits oil sites in three regions.",
    },
    {
        "color": TEAL,
        "kicker": "INDONESIA",
        "head": "Search goes on at Serang candy factory",
        "body": "34 still missing after Saturday's fire; 24 confirmed dead; DNA tests under way.",
    },
]

TIMELINE = [
    "00:07  Reuters journalists vote 94% to strike  ·  00:18  12 killed near Kyiv  ·  00:34  Ukraine hits Russian oil sites",
    "01:00  Russian jets in Korea's air zone  ·  01:22  Brookfield's $2.53bn bid backed  ·  01:47  US may renew Iran strikes",
]

# Stories 5-40: one line each in the data, wrapped to at most two lines.
LISTED = [
    "Reuters journalists vote 94% to authorise a strike over AI protections.",
    "Chicago O'Hare hit by brief ground stop amid the Thanksgiving rush.",
    "US may renew strikes on Iran after the New Year if no deal is reached.",
    "Israeli bombing in Gaza City kills at least three, Palestinian media say.",
    "UN condemns strikes on Sudan's capital, said to come from Ethiopian soil.",
    "Turkey and Egypt discuss trade ties and regional de-escalation by phone.",
    "Murmansk governor detained in Moscow, Russian state media report.",
    "China sentences an official to death for leaking about 100 secrets.",
    "Bangladesh court seeks social-media curbs for under-16s.",
    "Thai protesters march 16 km to a refinery over fuel margins.",
    "Thai court frees MP \u201cIce\u201d Rakchanok on bail in royal-insult case.",
    "Lahore tops world pollution ranking as AQI passes 500.",
    "Magnitude 4.0 quake strikes Pakistan near the Afghan border.",
    "Pakistan to invite India to an SCO culture ministers' meeting.",
    "Yunus blames \u201chigher level\u201d direction as Grameen branches are hit.",
    "Dutch activist, 28, dies by euthanasia after years of suffering.",
    "Russia plans railway ferries to keep Kaliningrad supplied.",
    "Trump assails Newsom at DOJ over 548 commuted death sentences.",
    "Mossad ex-chief: Israel foiled an ISIS plot on Swift's Vienna shows.",
    "King Charles reaches out to Meghan after her father's arrest.",
    "FBI raids Minnesota child centres in a $41m fraud probe.",
    "Tyson Fury reveals he has been diagnosed with schizophrenia.",
    "Iowa lead blast on hold again as Trump orders Army to wait.",
    "White House pulls Heidi Overton's nomination to lead the FDA.",
    "Democrats set broad rules for the party's 2028 debates.",
    "Senators probe RFK Jr.'s Samoa testimony after documents refute it.",
    "Three killed, one hurt in a shooting at an Ohio baby shower.",
    "AustralianSuper backs Brookfield's $2.53bn Reliance Worldwide bid.",
    "Meta pauses Class C share issue amid a shareholder lawsuit.",
    "CFTC finalises permanent rules for event-contract reporting.",
    "Yankees add left-hander Brent Suter to the bullpen.",
    "Mets' Cohen spends big again to land Tarik Skubal.",
    "Alleged drug lord \u201cEl Chapo Isidro\u201d to be tried in Mexico.",
    "LSU's Fulwiley returns after an arrest-related absence.",
    "Soldiers attacked in Mexico after a drug lord's arrest.",
    "Gulf states brace for a tougher Democrat-led Congress.",
]

FOOTER_CHECK = (
    "DATE CHECK \u2014 Every story on this page happened, or was first reported, "
    "on Tuesday 24 November 2026."
)
FOOTER_SOURCES = (
    "Sources: AP \u00b7 Reuters \u00b7 AFP \u00b7 CNN \u00b7 Times of India \u00b7 "
    "Bernama-dpa \u00b7 News Guild of New York \u00b7 make.fun news-image-20261124"
)


# ---------------------------------------------------------------- drawing

def draw_chip(draw, x0, y0, x1, y1):
    """A simple drawn processor: dark body, pins on four sides, NVDA die."""
    draw.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=NAVY)
    # pins
    pin = 10
    for i in range(5):
        px = x0 + 30 + i * 34
        draw.rectangle([px, y0 - pin, px + 14, y0], fill=INK)
        draw.rectangle([px, y1, px + 14, y1 + pin], fill=INK)
    for i in range(3):
        py = y0 + 32 + i * 34
        draw.rectangle([x0 - pin, py, x0, py + 14], fill=INK)
        draw.rectangle([x1, py, x1 + pin, py + 14], fill=INK)
    # die
    draw.rounded_rectangle([x0 + 44, y0 + 30, x1 - 44, y1 - 30], radius=8,
                           outline=(120, 200, 170), width=2)
    fnt = SANS_B(34)
    label = "NVDA"
    lw = text_w(draw, label, fnt)
    draw.text(((x0 + x1 - lw) / 2, y0 + 52), label, font=fnt, fill=(255, 255, 255))


def render(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.rectangle([0, 0, W, 106], fill=NAVY)
    title = "THE WORLD TODAY"
    f_title = SERIF_B(62)
    tw = text_w(d, title, f_title)
    d.text(((W - tw) / 2, 10), title, font=f_title, fill=(255, 255, 255))
    f_date = SANS_B(17)
    dateline = "TUESDAY, 24 NOVEMBER 2026  ·  ONE DAY, ONE PAGE, 40 SOURCED STORIES"
    dw = text_w(d, dateline, f_date)
    d.text(((W - dw) / 2, 78), dateline, font=f_date, fill=(200, 210, 230))
    d.rectangle([0, 106, W, 110], fill=RED)

    # ---- lead story
    lx, lw_ = 28, 612
    y = 122
    d.text((lx, y), LEAD_KICKER, font=SANS_B(16), fill=RED)
    y = 146
    f_head = SERIF_B(46)
    for line in LEAD_HEAD:
        d.text((lx, y), line, font=f_head, fill=INK)
        y += 52
    y += 4
    deck_lines = fit(d, LEAD_DECK, SANS(19), lw_, 2, "lead deck")
    y = draw_wrapped(d, lx, y, deck_lines, SANS(19), INK, 25)
    # chip illustration, right of the lead
    draw_chip(d, 700, 124, 940, 252)
    # green up arrow + surge, below the chip (never overlapping the die)
    ax = 748
    ay = 272
    d.polygon([(ax - 13, ay + 6), (ax, ay - 8), (ax + 13, ay + 6),
               (ax + 6, ay + 6), (ax + 6, ay + 18), (ax - 6, ay + 18),
               (ax - 6, ay + 6)], fill=GREEN)
    d.text((770, 258), "+31% IN A DAY", font=SANS_B(22), fill=GREEN)
    f_cap = SERIF(14)
    cap = LEAD_CAPTION
    cw = text_w(d, cap, f_cap)
    d.text((820 - cw / 2, 290), cap, font=f_cap, fill=MIDGREY)

    # ---- featured strip
    fy0, fy1 = 318, 438
    boxes = [(28, 344), (356, 672), (684, 996)]
    for (bx0, bx1), feat in zip(boxes, FEATURED):
        d.rectangle([bx0, fy0, bx1, fy1], fill=(255, 255, 255),
                    outline=(200, 192, 172), width=1)
        d.rectangle([bx0, fy0, bx1, fy0 + 6], fill=feat["color"])
        x = bx0 + 14
        d.text((x, fy0 + 14), feat["kicker"], font=SANS_B(13), fill=feat["color"])
        head_lines = fit(d, feat["head"], SANS_B(19), bx1 - bx0 - 28, 2,
                         "featured head")
        yy = draw_wrapped(d, x, fy0 + 34, head_lines, SANS_B(19), INK, 23)
        body_lines = fit(d, feat["body"], SANS(13), bx1 - bx0 - 28, 2,
                         "featured body")
        draw_wrapped(d, x, yy + 4, body_lines, SANS(13), (60, 60, 60), 16)

    # ---- timeline band
    ty0, ty1 = 446, 492
    d.rectangle([28, ty0, 996, ty1], fill=GREY)
    d.text((40, ty0 + 6), "THE DAY AS REPORTED  ·  UTC",
           font=SANS_B(12), fill=NAVY)
    yy = ty0 + 22
    for line in TIMELINE:
        d.text((40, yy), line, font=MONO(12), fill=INK)
        yy += 15

    # ---- list header
    hy = 502
    d.text((28, hy), "THE DAY IN 40 STORIES", font=SANS_B(20), fill=INK)
    note = "Numbered 5\u201340 \u00b7 lead + featured above"
    nw = text_w(d, note, SANS(13))
    d.text((996 - nw, hy + 4), note, font=SANS(13), fill=MIDGREY)
    d.line([28, hy + 28, 996, hy + 28], fill=INK, width=2)

    # ---- numbered list, three columns
    assert len(LISTED) == 36, "expected 36 listed stories, got %d" % len(LISTED)
    cols = [(28, 340), (356, 668), (684, 996)]
    per_col = 12
    list_y0 = 544
    row_h = 34
    for ci, (cx0, cx1) in enumerate(cols):
        chunk = LISTED[ci * per_col:(ci + 1) * per_col]
        yy = list_y0
        for j, story in enumerate(chunk):
            num = str(5 + ci * per_col + j)
            d.text((cx0, yy), num, font=SANS_B(14), fill=RED)
            num_w = text_w(d, num + "  ", SANS_B(14))
            lines = fit(d, story, SANS(14), cx1 - cx0 - num_w - 4, 2,
                        "story %s" % num)
            draw_wrapped(d, cx0 + num_w, yy, lines, SANS(14), INK, 17)
            yy += row_h

    # ---- footer
    d.line([28, 962, 996, 962], fill=INK, width=2)
    d.text((28, 972), FOOTER_CHECK, font=SANS_B(14), fill=INK)
    d.text((28, 994), FOOTER_SOURCES, font=SANS(12), fill=MIDGREY)

    img.save(path, "PNG", optimize=True)
    return img


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    render(out)
    size = os.path.getsize(out)
    im = Image.open(out)
    print("entry.png: %dx%d, %d bytes (limit 1048576)" % (im.size[0], im.size[1], size))
    assert im.size == (1024, 1024), "wrong dimensions"
    assert size <= 1048576, "over 1 MiB"
    print("OK")


if __name__ == "__main__":
    main()
