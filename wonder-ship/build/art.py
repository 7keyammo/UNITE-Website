# -*- coding: utf-8 -*-
"""Scene compositions for The Wonder Ship. One function per page beat.

Every scene returns SVG markup drawn inside a 1000 x 640 viewBox.
Scenes shared by all three books take a `w` (world) dict so the same
composition re-skins per book — which is exactly the promise the
template makes on paper.
"""
import math
import random

from prims import (STROKE, KIDS, person, domkam, johnson, ship, sound_rings,
                   star, sparkle, bubble, circle, ellipse, rect, path, g)

W, H = 1000, 640

WORLDS = {
    1: dict(deep="#0b3a4a", mid="#0f6d80", light="#7fd4d8", accent="#ff7a59",
            sand="#f3e2c0", sky="#bfeaf0", ground="#e9d3a3"),
    2: dict(deep="#171a4a", mid="#3b3a8c", light="#a9a6f2", accent="#ffd166",
            sand="#f5f0ff", sky="#2a2a6e", ground="#3b3a8c"),
    3: dict(deep="#1f3d1e", mid="#4a7c3f", light="#b9d99a", accent="#d98555",
            sand="#f4ead3", sky="#cfe8b8", ground="#7ba05b"),
}


def frame(bg):
    return rect(0, 0, W, H, bg, stroke=None)


def rng(seed):
    return random.Random(seed)


# ------------------------------------------------------------ classroom
def classroom(w, ship_glow=0, lamps=0, kid_pose="sit", extra="", ship_s=0.46,
              ship_y=250, kids_y=600, face="calm"):
    """The carpet. Used for the title page, both ritual blocks and the landing."""
    o = [frame(w["sky"])]
    o.append(rect(0, 380, W, H - 380, w["ground"], stroke=None))
    o.append(path(f"M0 380 L{W} 380", sw=6))
    # window, with the world's own colour showing through
    o.append(rect(48, 60, 200, 158, "#eaf6f7", r=12, sw=6))
    o.append(rect(56, 68, 184, 142, w["light"], r=8, stroke=None))
    o.append(path("M148 60 L148 218 M48 139 L248 139", sw=5))
    # bookshelf
    o.append(rect(772, 96, 190, 122, "#c98a4b", r=8, sw=6))
    o.append(path("M772 160 L962 160", sw=5))
    for i, c in enumerate(("#ef476f", "#06d6a0", "#ffd166", "#4cc9f0")):
        o.append(rect(786 + i * 42, 108, 30, 48, c, r=4, sw=4))
    for i, c in enumerate(("#b388eb", "#ff8fab", "#06d6a0")):
        o.append(rect(792 + i * 52, 172, 40, 42, c, r=4, sw=4))
    # carpet
    o.append(ellipse(500, 600, 460, 96, w["light"], sw=6))
    o.append(ellipse(500, 600, 380, 74, "none", stroke="#ffffff", sw=5).replace("/>", ' opacity="0.45"/>'))
    o.append(ship(500, ship_y, ship_s, glow=ship_glow, lamps=lamps))
    # children, large enough to read the pose at a glance
    for i, (x, sc) in enumerate(((150, .95), (322, 1.0), (668, 1.0), (852, .95))):
        k = KIDS[i]
        o.append(person(x, kids_y, sc, pose=kid_pose, face=face, flip=i >= 2,
                        **{q: k[q] for q in ("skin", "hair", "shirt", "hairstyle")}))
    o.append(extra)
    return "".join(o)


def sc_title(w, book):
    o = [classroom(w, ship_glow=2, lamps=0, kid_pose="arms_up", ship_s=0.6, ship_y=250, face="happy")]
    if book == 2:
        o.append("".join(star(120 + i * 38, 96 + (i % 3) * 26, 9, w["accent"]) for i in range(4)))
    if book == 3:
        o.append(path("M700 470 Q760 300 900 470 Z", fill=w["mid"], sw=6, op=.35))
    return "".join(o)


def sc_note(w):
    o = [frame(w["sand"]), ship(500, 400, 0.85, glow=1, lamps=0)]
    o.append("".join(sparkle(200 + i * 160, 120, 16, w["mid"], .5) for i in range(5)))
    return "".join(o)


def sc_breathe_in(w):
    return classroom(w, ship_glow=0, kid_pose="hand_on_chest", face="calm")


def sc_breathe_out(w):
    extra = (sound_rings(500, 250, 3, 34, w["accent"], 6, 150, .6, 160)
             + "".join(path(f"M{x} 470 q16 -30 0 -58", stroke=w["mid"], sw=6, op=.65)
                       for x in (190, 360, 640, 812)))
    return classroom(w, ship_glow=2, kid_pose="hand_on_chest", extra=extra, face="calm")


def _clap_meter(w, lit):
    o = [rect(332, 54, 336, 62, "#ffffff", r=18, sw=6)]
    for i in range(4):
        o.append(circle(392 + i * 74, 85, 21, w["accent"] if i < lit else "#dfe6e9", sw=5))
    return "".join(o)


def sc_clap_slow(w):
    return classroom(w, ship_glow=2, lamps=1, kid_pose="clap",
                     extra=_clap_meter(w, 1))


def sc_clap_fast(w, pilots=True):
    extra = _clap_meter(w, 4)
    extra += "".join(path(f"M{x} {y} l30 -26 M{x} {y + 28} l30 -26", stroke=w["accent"], sw=7, op=.85)
                     for x, y in ((36, 430), (912, 430), (60, 500), (888, 500)))
    o = [classroom(w, ship_glow=3, lamps=4, kid_pose="clap_big", extra=extra, face="happy")]
    if pilots:
        o.append(domkam(428, 452, 0.62, pose="clap_big"))
        o.append(johnson(586, 448, 0.62, pose="point", flip=True))
    return "".join(o)


# ------------------------------------------------------------- porthole
def sc_porthole(w, inner, book):
    o = [frame(w["deep"])]
    o.append(circle(500, 320, 250, w["mid"], sw=14))
    o.append(f'<clipPath id="ph{book}"><circle cx="500" cy="320" r="243"/></clipPath>')
    o.append(f'<g clip-path="url(#ph{book})">{inner}</g>')
    o.append(circle(500, 320, 250, "none", sw=14))
    o.append(path("M370 210 a180 180 0 0 1 120 -58", stroke="#ffffff", sw=16, op=.45))
    for a in range(8):
        ang = math.radians(a * 45 + 22)
        o.append(circle(round(500 + 272 * math.cos(ang)), round(320 + 272 * math.sin(ang)),
                        11, w["accent"], sw=4))
    return "".join(o)


# ============================================================== BOOK 1
def fish(x, y, s, body, fin=None, flip=False):
    fin = fin or body
    o = [ellipse(0, 0, 46, 30, body),
         path("M40 0 L74 -26 L74 26 Z", fill=fin),
         circle(-20, -8, 7, "#fff", sw=3), circle(-21, -8, 3, STROKE, stroke=None),
         path("M-4 -28 L10 -44 L22 -26", fill=fin, sw=4)]
    return f'<g transform="translate({x} {y}) scale({-s if flip else s} {s})">' + "".join(o) + "</g>"


def whale(x, y, s, color="#2b5f7a"):
    o = [path("M-230 0 Q-200 -96 -40 -100 Q140 -100 216 -16 Q150 44 -20 56 Q-190 60 -230 0 Z",
              fill=color, sw=7),
         path("M216 -16 Q286 -76 300 -30 Q284 22 216 4 Z", fill=color, sw=7),
         path("M-190 20 Q-40 62 150 26", fill="none", stroke="#ffffff", sw=6, op=.35),
         circle(-150, -28, 12, "#fff", sw=4), circle(-152, -28, 6, STROKE, stroke=None),
         path("M-70 -100 q10 -30 34 -34", stroke=STROKE, sw=6)]
    return f'<g transform="translate({x} {y}) scale({s})">' + "".join(o) + "</g>"


def seaweed(x, base, h, color, seed=1):
    r = rng(seed)
    d = f"M{x} {base}"
    for i in range(4):
        d += f" q{r.choice([-34, 34])} -{h // 5} 0 -{h // 4}"
    return path(d, stroke=color, sw=16, cap="round", op=.85)


def ocean_bg(w, dark=False):
    top = "#0d5570" if not dark else "#07293a"
    bot = w["mid"] if not dark else "#0b3a4a"
    return (f'<defs><linearGradient id="og{int(dark)}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bot}"/>'
            f'</linearGradient></defs>'
            f'<rect width="{W}" height="{H}" fill="url(#og{int(dark)})"/>'
            + "".join(path(f"M0 {40 + i * 26} q120 -22 240 0 t240 0 t240 0 t240 0",
                           stroke="#ffffff", sw=5, op=.10) for i in range(3)))


def sea_floor(w):
    return (path(f"M0 {H} L0 560 Q250 520 500 552 Q750 584 1000 546 L1000 {H} Z",
                 fill=w["sand"], sw=6)
            + seaweed(120, 566, 170, "#2e9e6b", 3) + seaweed(880, 552, 200, "#2e9e6b", 7))


B1 = {}

B1[7] = lambda w: "".join([                                   # departure, rising
    f'<defs><linearGradient id="up1" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="#4aa3c4"/><stop offset="1" stop-color="#d8f2f7"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" fill="url(#up1)"/>',
    "".join(circle(150 + i * 250, 130 + (i % 2) * 56, 48, "#ffffff", sw=5) for i in range(4)),
    "".join(circle(196 + i * 250, 130 + (i % 2) * 56, 60, "#ffffff", sw=5) for i in range(4)),
    path("M120 300 q28 -24 56 0 M176 300 q28 -24 56 0", stroke=STROKE, sw=6),
    path("M800 230 q28 -24 56 0 M856 230 q28 -24 56 0", stroke=STROKE, sw=6),
    rect(52, 496, 168, 144, "#eaf6f7", r=10, sw=6),
    path("M136 496 L136 640 M52 568 L220 568", sw=5),
    ship(540, 300, 0.98, glow=3, lamps=4, tilt=-6),
    "".join(path(f"M{452 + i * 76} 500 l0 140", stroke="#ffd166", sw=12, op=.6) for i in range(3)),
])

B1[8] = lambda w: sc_porthole(w, "".join([
    rect(0, 0, W, H, "#0d5570", stroke=None),
    "".join(bubble(300 + i * 90, 200 + (i % 3) * 90, 10 + i * 2) for i in range(6)),
    ellipse(560, 400, 210, 96, "#0a4560", stroke=None),
]), 1)

B1[9] = lambda w: "".join([                                   # arrival, bubbles
    ocean_bg(w), sea_floor(w),
    "".join(path(f"M{200 + i * 150} 0 L{240 + i * 150} 300", stroke="#ffffff", sw=26, op=.09)
            for i in range(5)),
    "".join(bubble(340 + (i * 57) % 340, 90 + (i * 83) % 400, 7 + (i % 4) * 4) for i in range(14)),
    ship(520, 400, 0.72, glow=2, lamps=1, tilt=3),
])

B1[10] = lambda w: "".join([                                  # the big reveal
    ocean_bg(w), sea_floor(w),
    path("M60 470 q60 -90 130 -10 q60 -80 120 10 Z", fill="#e86a92", sw=6),
    path("M760 500 q70 -100 150 -10 Z", fill="#f4a261", sw=6),
    fish(230, 250, 1.05, "#ffd166", "#ff7a59"),
    fish(470, 170, 0.8, "#ff7a59", "#ffd166", flip=True),
    fish(700, 300, 1.2, "#7fd4d8", "#2e9e6b"),
    fish(840, 180, 0.7, "#e86a92", "#ffd166", flip=True),
    fish(360, 420, 0.9, "#b388eb", "#7fd4d8"),
    ship(120, 480, 0.42, glow=1, lamps=0),
    "".join(bubble(600 + i * 40, 420 - i * 40, 8 + i * 2) for i in range(5)),
])

B1[11] = lambda w: "".join([                                  # cup your ears
    ocean_bg(w), sea_floor(w),
    person(300, 560, 1.35, pose="cup_ears", **{q: KIDS[0][q] for q in ("skin", "hair", "shirt", "hairstyle")}),
    person(680, 560, 1.35, pose="cup_ears", flip=True, **{q: KIDS[3][q] for q in ("skin", "hair", "shirt", "hairstyle")}),
    fish(900, 250, 1.25, "#ffd166", "#ff7a59", flip=True),
    sound_rings(840, 250, 4, 38, "#ffffff", 6, 60, .55, 150),
])

B1[12] = lambda w: "".join([                                  # muffled fish
    ocean_bg(w),
    rect(0, 0, W, H, "#0d5570", stroke=None).replace("/>", ' opacity="0.35"/>'),
    fish(430, 320, 3.0, "#8fd0d8", "#6fb6c4"),
    sound_rings(600, 320, 3, 52, "#ffffff", 7, 140, .30, 100),
    "".join(bubble(240 + i * 130, 470 + (i % 2) * 50, 9) for i in range(5)),
])

B1[13] = lambda w: "".join([                                  # arm wave
    ocean_bg(w),
    path("M0 330 q125 -110 250 0 t250 0 t250 0 t250 0", stroke=w["accent"], sw=14, op=.9),
    path("M0 400 q125 -110 250 0 t250 0 t250 0 t250 0", stroke="#ffd166", sw=10, op=.6),
    person(250, 600, 1.25, pose="wave_arm", **{q: KIDS[1][q] for q in ("skin", "hair", "shirt", "hairstyle")}),
    person(730, 600, 1.25, pose="wave_arm", flip=True, **{q: KIDS[4][q] for q in ("skin", "hair", "shirt", "hairstyle")}),
])

B1[14] = lambda w: "".join([                                  # whole-body wave
    ocean_bg(w),
    path("M0 300 q125 -120 250 0 t250 0 t250 0 t250 0", stroke=w["accent"], sw=16, op=.95),
    "".join(person(160 + i * 170, 590, 1.0, pose="wave_arm", flip=i % 2 == 1,
                   **{q: KIDS[i][q] for q in ("skin", "hair", "shirt", "hairstyle")}) for i in range(5)),
    fish(880, 250, 0.9, "#ffd166", "#ff7a59", flip=True),
])

B1[15] = lambda w: "".join([                                  # CLICK! shrimp
    ocean_bg(w), sea_floor(w),
    sound_rings(560, 330, 5, 46, "#ffd166", 11, 60, 1.0, 150),
    g(path("M-40 0 q-30 -34 4 -56 q40 -22 66 6 q22 24 6 50 q-30 30 -76 0 Z", fill="#ff7a59", sw=6)
      + path("M26 -34 L84 -70 M26 -22 L88 -34", stroke="#ff7a59", sw=11)
      + circle(-12, -30, 7, "#fff", sw=3) + circle(-13, -30, 3, STROKE, stroke=None)
      + path("M-40 6 q-40 22 -60 6", stroke="#ff7a59", sw=8),
      transform="translate(480 330) scale(1.5)"),
])

B1[16] = lambda w: "".join([                                  # buried, muffled
    ocean_bg(w),
    path(f"M0 {H} L0 420 Q250 380 500 412 Q750 444 1000 406 L1000 {H} Z", fill=w["sand"], sw=6),
    path("M330 428 q170 -104 344 0 Z", fill="#e9d3a3", sw=6),
    path("M614 374 L706 306 M614 392 L716 356", stroke="#ff7a59", sw=17, cap="round"),
    circle(600, 380, 40, "#ff7a59", sw=6),
    circle(586, 368, 8, "#fff", sw=3), circle(585, 368, 4, STROKE, stroke=None),
    sound_rings(650, 366, 2, 26, "#ffd166", 6, 66, .38, 130),
    "".join(bubble(200 + i * 180, 180 + (i % 2) * 80, 10) for i in range(5)),
])

B1[17] = lambda w: "".join([                                  # big clap / tiny clap
    ocean_bg(w),
    path(f"M500 40 L500 600", stroke="#ffffff", sw=5, dash="18 16", op=.35),
    person(250, 560, 1.3, pose="clap_big", **{q: KIDS[2][q] for q in ("skin", "hair", "shirt", "hairstyle")}),
    sound_rings(250, 400, 4, 34, "#ffd166", 10, 90, 1, 170),
    person(750, 560, 1.3, pose="clap", **{q: KIDS[5][q] for q in ("skin", "hair", "shirt", "hairstyle")}),
    sound_rings(750, 420, 2, 20, "#ffd166", 5, 46, .5, 150),
])

B1[18] = lambda w: "".join([                                  # whale tail / seahorse
    ocean_bg(w), sea_floor(w),
    path("M250 392 Q140 300 46 322 Q90 402 250 412 Z", fill="#2b5f7a", sw=7),
    path("M250 392 Q360 300 454 322 Q410 402 250 412 Z", fill="#2b5f7a", sw=7),
    path("M250 400 Q244 490 250 560", stroke="#2b5f7a", sw=52, cap="round"),
    sound_rings(250, 556, 3, 40, "#ffd166", 11, 72, 1.0, 150),
    g(path("M0 0 q-30 -60 10 -100 q30 -34 62 -14 q26 18 6 46 q-20 26 -44 20", fill="#ffd166", sw=6)
      + path("M0 0 q-24 34 8 44 q22 6 24 -18", fill="#ffd166", sw=6)
      + circle(38, -96, 6, STROKE, stroke=None),
      transform="translate(760 470) scale(1.15)"),
    "".join(path(f"M{700 + i * 22} {430 - i * 16} l0 -12", stroke="#ffd166", sw=4, op=.6) for i in range(3)),
])

B1[19] = lambda w: "".join([                                  # the whale sings — quiet page
    ocean_bg(w, dark=True),
    whale(560, 300, 1.15, "#4d8fae"),
    sound_rings(300, 300, 4, 62, "#7fd4d8", 5, 120, .35, 90),
    ship(140, 520, 0.3, glow=1, lamps=0),
])

B1[20] = lambda w: "".join([                                  # hum with her
    ocean_bg(w, dark=True),
    circle(690, 300, 200, "#0f4d66", sw=10),
    whale(700, 300, 0.55, "#5fa3c2"),
    person(280, 580, 1.7, pose="hand_on_chest", face="calm",
           **{q: KIDS[0][q] for q in ("skin", "hair", "shirt", "hairstyle")}),
    sound_rings(400, 330, 4, 40, "#ffd166", 6, 80, .8, 60),
    circle(300, 330, 46, "#ffd166", stroke=None).replace("/>", ' opacity="0.22"/>'),
])


# ============================================================== BOOK 2
def space_bg(w, empty=False):
    o = [f'<defs><radialGradient id="sg{int(empty)}" cx="50%" cy="40%">'
         f'<stop offset="0" stop-color="{"#0d0f30" if empty else "#2a2a6e"}"/>'
         f'<stop offset="1" stop-color="{"#05061a" if empty else "#12143c"}"/>'
         f'</radialGradient></defs>',
         f'<rect width="{W}" height="{H}" fill="url(#sg{int(empty)})"/>']
    r = rng(9)
    n = 26 if empty else 60
    for _ in range(n):
        x, y = r.randint(10, W - 10), r.randint(10, H - 10)
        o.append(circle(x, y, r.choice([2, 2, 3, 4]), "#ffffff", stroke=None)
                 .replace("/>", f' opacity="{r.choice([.35,.55,.8])}"/>'))
    return "".join(o)


def planet(x, y, r_, fill, ring=None):
    o = [circle(x, y, r_, fill, sw=6),
         circle(x - r_ * .32, y - r_ * .3, r_ * .22, "#ffffff", stroke=None).replace("/>", ' opacity="0.25"/>')]
    if ring:
        o.append(ellipse(x, y, r_ * 1.7, r_ * .4, "none", stroke=ring, sw=9, rot=-16))
    return "".join(o)


B2 = {}

B2[7] = lambda w: "".join([
    f'<defs><linearGradient id="up2" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="#12143c"/><stop offset="1" stop-color="#bfeaf0"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" fill="url(#up2)"/>',
    "".join(star(120 + i * 150, 60 + (i % 3) * 30, 11, w["accent"]) for i in range(6)),
    "".join(circle(160 + i * 210, 340 + (i % 2) * 40, 44, "#ffffff", stroke=None) for i in range(4)),
    "".join(circle(200 + i * 210, 340 + (i % 2) * 40, 56, "#ffffff", stroke=None) for i in range(4)),
    path("M120 470 q26 -22 52 0", stroke=STROKE, sw=6),
    rect(60, 540, 140, 100, "#eaf6f7", r=10, sw=6),
    ship(520, 250, 0.78, glow=3, lamps=4, tilt=-5),
    "".join(path(f"M{470 + i * 55} 400 l0 150", stroke="#ffd166", sw=9, op=.5) for i in range(3)),
])

B2[8] = lambda w: sc_porthole(w, "".join([
    rect(0, 0, W, H, "#05061a", stroke=None),
    "".join(sparkle(300 + (i * 61) % 420, 160 + (i * 97) % 340, 12 + (i % 3) * 6, "#ffd166", .95)
            for i in range(11)),
]), 2)

B2[9] = lambda w: "".join([
    space_bg(w),
    planet(830, 140, 74, "#ff7a59"),
    ship(480, 320, 0.8, glow=1, lamps=0, tilt=8),
    "".join(sparkle(180 + i * 120, 520 - (i % 3) * 40, 12, "#ffd166", .8) for i in range(6)),
])

B2[10] = lambda w: "".join([
    space_bg(w),
    planet(200, 180, 92, "#ff7a59", ring="#ffd166"),
    planet(800, 420, 66, "#06d6a0"),
    planet(640, 130, 40, "#b388eb"),
    "".join(star(120 + (i * 137) % 800, 300 + (i * 91) % 260, 14 + (i % 3) * 6, "#ffd166")
            for i in range(9)),
    ship(470, 340, 0.5, glow=1, lamps=0, tilt=-4),
])

B2[11] = lambda w: "".join([                                  # tiny star sings high
    space_bg(w),
    star(500, 300, 46, "#ffd166"),
    sound_rings(500, 300, 6, 20, "#a9a6f2", 6, 66, 1, 360),
    "".join(sparkle(180 + i * 160, 540, 12, "#ffffff", .6) for i in range(5)),
])

B2[12] = lambda w: "".join([                                  # big star sings low
    space_bg(w),
    star(500, 300, 118, "#ff7a59", points=7),
    sound_rings(500, 300, 3, 74, "#a9a6f2", 9, 150, 1, 360),
])

B2[13] = lambda w: "".join([                                  # reach high / curl low
    space_bg(w),
    path("M500 40 L500 600", stroke="#ffffff", sw=5, dash="18 16", op=.3),
    person(280, 560, 1.3, pose="reach_high", **{q: KIDS[3][q] for q in ("skin", "hair", "shirt", "hairstyle")}),
    star(120, 170, 38, "#ffd166"), sound_rings(120, 170, 4, 16, "#a9a6f2", 5, 52, .9, 300),
    person(700, 610, 1.3, pose="curl_low", **{q: KIDS[0][q] for q in ("skin", "hair", "shirt", "hairstyle")}),
    star(880, 430, 66, "#ff7a59", points=7), sound_rings(880, 430, 2, 54, "#a9a6f2", 8, 94, .9, 300),
])

B2[14] = lambda w: "".join([                                  # the body is the dial
    space_bg(w),
    person(260, 560, 1.2, pose="wave_arm", **{q: KIDS[1][q] for q in ("skin", "hair", "shirt", "hairstyle")}),
    sound_rings(330, 240, 6, 17, "#ffd166", 5, 40, .95, 200),
    person(740, 560, 1.2, pose="wave_arm", flip=True, **{q: KIDS[4][q] for q in ("skin", "hair", "shirt", "hairstyle")}),
    sound_rings(670, 300, 3, 52, "#ff7a59", 8, 60, .95, 200),
    johnson(500, 600, 0.75, pose="point"),
])

B2[15] = lambda w: "".join([                                  # no down here
    space_bg(w),
    ship(180, 250, 0.5, glow=1, lamps=0, tilt=14),
    person(560, 420, 1.5, pose="float", **{q: KIDS[2][q] for q in ("skin", "hair", "shirt", "hairstyle")}),
    "".join(sparkle(300 + i * 130, 130 + (i % 2) * 60, 12, "#ffffff", .6) for i in range(5)),
])

B2[16] = lambda w: "".join([                                  # pilots floating
    space_bg(w),
    g(domkam(0, 0, 0.95, pose="float"), transform="translate(300 400) rotate(-24)"),
    g(johnson(0, 0, 0.95, pose="float"), transform="translate(720 340) rotate(168)"),
    "".join(sparkle(140 + i * 150, 560, 11, "#ffd166", .7) for i in range(6)),
])

B2[17] = lambda w: "".join([                                  # three slow steps
    space_bg(w),
    "".join(path(f"M{200 + i * 250} 560 l60 0", stroke="#a9a6f2", sw=6, dash="12 12", op=.6) for i in range(3)),
    "".join(person(230 + i * 250, 540, 1.05, pose="float",
                   **{q: KIDS[i][q] for q in ("skin", "hair", "shirt", "hairstyle")}) for i in range(3)),
    "".join(f'<text x="{230 + i * 250}" y="606" text-anchor="middle" font-family="sans-serif" '
            f'font-size="42" font-weight="700" fill="#ffd166">{i + 1}</text>' for i in range(3)),
])

B2[18] = lambda w: "".join([                                  # moon jump
    space_bg(w),
    path(f"M0 {H} L0 560 Q250 520 500 552 Q750 584 1000 546 L1000 {H} Z", fill="#6b6ba8", sw=6),
    "".join(circle(160 + i * 230, 580 + (i % 2) * 14, 26, "#5a5a94", sw=4) for i in range(4)),
    person(230, 560, 1.0, pose="curl_low", **{q: KIDS[5][q] for q in ("skin", "hair", "shirt", "hairstyle")}),
    person(520, 300, 1.15, pose="jump", **{q: KIDS[0][q] for q in ("skin", "hair", "shirt", "hairstyle")}),
    person(800, 430, 1.05, pose="float", **{q: KIDS[3][q] for q in ("skin", "hair", "shirt", "hairstyle")}),
    path("M300 520 Q420 300 520 340", stroke="#ffd166", sw=6, dash="14 14", op=.8),
    path("M560 360 Q700 320 790 400", stroke="#ffd166", sw=6, dash="14 14", op=.6),
])

B2[19] = lambda w: "".join([                                  # NOTHING — emptiest page
    space_bg(w, empty=True),
    ship(500, 340, 0.28, glow=1, lamps=0),
])

B2[20] = lambda w: "".join([                                  # because YOU are something
    space_bg(w, empty=True),
    circle(500, 300, 210, "#ffd166", stroke=None).replace("/>", ' opacity="0.10"/>'),
    circle(500, 300, 140, "#ffd166", stroke=None).replace("/>", ' opacity="0.14"/>'),
    person(500, 560, 1.75, pose="hand_on_chest", face="calm",
           **{q: KIDS[4][q] for q in ("skin", "hair", "shirt", "hairstyle")}),
    sound_rings(500, 330, 3, 26, "#ffd166", 6, 56, .85, 360),
])


# ============================================================== BOOK 3
def jungle_bg(w, pale=False):
    sky = "#e8f2d4" if pale else w["sky"]
    o = [f'<defs><linearGradient id="jg{int(pale)}" x1="0" y1="0" x2="0" y2="1">'
         f'<stop offset="0" stop-color="{sky}"/><stop offset="1" stop-color="#a8cf8a"/>'
         f'</linearGradient></defs>',
         f'<rect width="{W}" height="{H}" fill="url(#jg{int(pale)})"/>']
    if not pale:
        o.append(path("M0 300 L120 150 L240 300 Z", fill="#7f9c6a", sw=6))
        o.append(path("M760 300 L900 120 L1000 300 Z", fill="#6d8a5a", sw=6))
        o.append(path("M880 120 L900 120 L916 150 L864 150 Z", fill="#ff7a59", sw=5))
    o.append(rect(0, 470, W, H - 470, "#7ba05b", stroke=None))
    o.append(path(f"M0 470 L{W} 470", sw=6))
    return "".join(o)


def fern(x, base, h, color="#3f6b34", flip=False):
    o = [path(f"M0 0 Q{-10 if flip else 10} {-h//2} 0 {-h}", stroke=color, sw=10)]
    for i in range(5):
        yy = -h * (i + 1) / 6
        o.append(path(f"M0 {yy:.0f} q40 -18 62 -6", stroke=color, sw=8))
        o.append(path(f"M0 {yy:.0f} q-40 -18 -62 -6", stroke=color, sw=8))
    return f'<g transform="translate({x} {base}) scale({-1 if flip else 1} 1)">' + "".join(o) + "</g>"


def dino_big(x, y, s, color="#4a9c6d", mouth_open=False):
    """Long-neck sauropod. Body, four legs, long tail, small head up high."""
    o = [# tail
         path("M-90 -110 Q-260 -96 -330 -180", stroke=color, sw=30, cap="round"),
         path("M-330 -180 Q-370 -196 -396 -186", stroke=color, sw=14, cap="round"),
         # body
         ellipse(0, -110, 150, 92, color, sw=7),
         # legs
         path("M-84 -46 L-90 0", stroke=color, sw=44, cap="round"),
         path("M-30 -46 L-34 0", stroke=color, sw=40, cap="round"),
         path("M62 -46 L70 0", stroke=color, sw=44, cap="round"),
         path("M112 -46 L122 0", stroke=color, sw=40, cap="round"),
         # neck
         path("M100 -150 Q196 -206 210 -320", stroke=color, sw=40, cap="round"),
         # head
         ellipse(214, -350, 52, 36, color, sw=7, rot=-12),
         path("M252 -360 q26 4 30 16 q-22 10 -34 2 Z", fill=color, sw=5),
         circle(214, -360, 11, "#fff", sw=4), circle(216, -360, 6, STROKE, stroke=None),
         # belly highlight
         path("M-90 -66 q90 34 180 -4", stroke="#ffffff", sw=8, op=.28)]
    if mouth_open:
        o.append(path("M256 -344 q30 6 26 24 q-24 8 -34 -8 Z", fill="#7a2c3a", sw=5))
    return f'<g transform="translate({x} {y}) scale({s})">' + "".join(o) + "</g>"


def dino_small(x, y, s, color="#e0a44a", flip=False):
    """Little two-legged dinosaur. Chunky, friendly, obviously a dinosaur."""
    o = [path("M-52 -60 Q-120 -50 -150 -96", stroke=color, sw=18, cap="round"),   # tail
         ellipse(0, -62, 62, 48, color, sw=6),                                     # body
         path("M-18 -22 L-22 0", stroke=color, sw=24, cap="round"),                # legs
         path("M26 -22 L32 0", stroke=color, sw=24, cap="round"),
         path("M34 -92 Q46 -128 74 -132", stroke=color, sw=22, cap="round"),       # neck
         ellipse(86, -136, 38, 28, color, sw=6),                                   # head
         path("M116 -142 q22 2 24 12 q-18 10 -28 2 Z", fill=color, sw=5),          # snout
         circle(88, -144, 8, "#fff", sw=3), circle(89, -144, 4, STROKE, stroke=None),
         path("M-30 -34 q34 16 64 -4", stroke="#ffffff", sw=6, op=.3),
         path("M-24 -104 l12 -20 l14 20 l12 -20 l14 20", stroke=color, sw=7)]      # back spikes
    return f'<g transform="translate({x} {y}) scale({-s if flip else s} {s})">' + "".join(o) + "</g>"


def shock_ring(x, y, n, spread, color="#d98555", sw=8, op=.9):
    return "".join(ellipse(x, y, 60 + i * spread, (60 + i * spread) * .26, "none",
                           stroke=color, sw=sw).replace("/>", f' opacity="{op - i * .2}"/>')
                   for i in range(n))


B3 = {}

B3[7] = lambda w: "".join([                                   # up and BACK
    f'<defs><linearGradient id="tb" x1="0" y1="0" x2="1" y2="0">'
    f'<stop offset="0" stop-color="#cfe8b8"/><stop offset="1" stop-color="#1f3d1e"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" fill="url(#tb)"/>',
    "".join(path(f"M{900 - i * 150} 0 L{860 - i * 150} {H}", stroke="#ffffff", sw=30, op=.10)
            for i in range(6)),
    "".join(path(f"M{760 - i * 90} 300 l-70 0", stroke="#ffd166", sw=10, op=.75, cap="round")
            for i in range(5)),
    ship(700, 300, 0.8, glow=3, lamps=4, tilt=6),
])

B3[8] = lambda w: sc_porthole(w, "".join([
    rect(0, 0, W, H, "#3f6b34", stroke=None),
    fern(360, 620, 300, "#2e5426"), fern(660, 640, 340, "#356030", flip=True),
    fern(510, 600, 260, "#4a7c3f"),
    path("M600 300 Q680 220 760 300 Q690 360 600 300 Z", fill="#2a4a24", sw=6),
]), 3)

B3[9] = lambda w: "".join([                                   # landing in tall grass
    jungle_bg(w),
    ship(500, 360, 0.72, glow=2, lamps=1, tilt=-4),
    "".join(path(f"M{40 + i * 52} 640 q{-14 if i % 2 else 14} -110 {6 if i % 2 else -6} -180",
                 stroke="#4a7c3f", sw=13, op=.95) for i in range(19)),
    fern(120, 640, 220), fern(880, 640, 240, flip=True),
])

B3[10] = lambda w: "".join([                                  # the big reveal
    jungle_bg(w),
    dino_big(560, 470, 0.72, "#4a9c6d"),
    dino_small(170, 470, 1.0, "#e0a44a"),
    dino_small(880, 490, 0.8, "#b388eb", flip=True),
    fern(80, 640, 200), fern(940, 640, 210, flip=True),
    ship(340, 560, 0.3, glow=1, lamps=0),
])

B3[11] = lambda w: "".join([                                  # palms flat, waiting
    jungle_bg(w),
    person(300, 600, 1.4, pose="palms_down", **{q: KIDS[0][q] for q in ("skin", "hair", "shirt", "hairstyle")}),
    person(700, 600, 1.4, pose="palms_down", flip=True, **{q: KIDS[3][q] for q in ("skin", "hair", "shirt", "hairstyle")}),
    "".join(path(f"M{430 + i * 40} 596 l0 -14", stroke=w["accent"], sw=5, op=.45) for i in range(4)),
])

B3[12] = lambda w: "".join([                                  # the ground is talking
    jungle_bg(w),
    g(dino_big(0, 0, 0.78, "#4a9c6d"), transform="translate(1010 470)"),
    shock_ring(760, 500, 5, 62, w["accent"], 9, 1.0),
    person(240, 600, 1.3, pose="palms_down", **{q: KIDS[2][q] for q in ("skin", "hair", "shirt", "hairstyle")}),
    person(470, 600, 1.3, pose="palms_down", **{q: KIDS[5][q] for q in ("skin", "hair", "shirt", "hairstyle")}),
])

B3[13] = lambda w: "".join([                                  # four counted stomps
    jungle_bg(w),
    "".join(person(170 + i * 220, 540, 1.0, pose="stomp",
                   **{q: KIDS[i][q] for q in ("skin", "hair", "shirt", "hairstyle")}) for i in range(4)),
    "".join(shock_ring(190 + i * 220, 552, 2, 22, w["accent"], 6, .85) for i in range(4)),
    "".join(f'<text x="{170 + i * 220}" y="620" text-anchor="middle" font-family="sans-serif" '
            f'font-size="44" font-weight="700" fill="{w["deep"]}">{i + 1}</text>' for i in range(4)),
])

B3[14] = lambda w: "".join([                                  # doubling: 4 slow, 8 fast
    jungle_bg(w, pale=True),
    path("M60 300 L940 300", stroke=STROKE, sw=4, dash="14 14", op=.4),
    "".join(shock_ring(150 + i * 230, 200, 1, 0, w["mid"], 9, .95) for i in range(4)),
    "".join(shock_ring(120 + i * 108, 420, 1, 0, w["accent"], 7, .95) for i in range(8)),
    f'<text x="500" y="128" text-anchor="middle" font-family="sans-serif" font-size="40" '
    f'font-weight="700" fill="{w["deep"]}">4</text>',
    f'<text x="500" y="560" text-anchor="middle" font-family="sans-serif" font-size="40" '
    f'font-weight="700" fill="{w["deep"]}">8</text>',
])

B3[15] = lambda w: "".join([                                  # the biggest dinosaur
    jungle_bg(w),
    dino_big(560, 470, 0.92, "#4a9c6d"),
    shock_ring(430, 490, 5, 66, w["accent"], 11, 1.0),
    person(80, 610, 0.7, pose="still", **{q: KIDS[1][q] for q in ("skin", "hair", "shirt", "hairstyle")}),
])

B3[16] = lambda w: "".join([                                  # the littlest dinosaur
    jungle_bg(w),
    path("M180 500 q90 -34 180 0 q-30 34 -90 34 q-60 0 -90 -34 Z", fill="#5c7a45", sw=6),
    dino_small(620, 480, 1.3, "#e0a44a"),
    shock_ring(640, 500, 2, 16, w["accent"], 5, .8),
    fern(920, 640, 200, flip=True),
])

B3[17] = lambda w: "".join([                                  # big / tiny alternating
    jungle_bg(w),
    "".join(person(150 + i * 235, 550, 1.15 if i % 2 == 0 else 0.85,
                   pose="stomp" if i % 2 == 0 else "tiptoe",
                   **{q: KIDS[i][q] for q in ("skin", "hair", "shirt", "hairstyle")}) for i in range(4)),
    "".join(shock_ring(150 + i * 470, 566, 3, 30, w["accent"], 9, .95) for i in range(2)),
    "".join(shock_ring(385 + i * 470, 566, 1, 0, w["accent"], 4, .55) for i in range(2)),
])

B3[18] = lambda w: "".join([                                  # low roar / high squeak
    jungle_bg(w),
    path("M500 40 L500 600", stroke="#ffffff", sw=5, dash="18 16", op=.5),
    dino_big(260, 470, 0.56, "#4a9c6d", mouth_open=True),
    sound_rings(410, 300, 3, 60, w["accent"], 11, 80, .95, 120),
    dino_small(730, 470, 1.0, "#e0a44a"),
    sound_rings(830, 340, 5, 18, "#ffd166", 5, 40, .95, 120),
])

B3[19] = lambda w: "".join([                                  # the canyon — quiet page
    jungle_bg(w, pale=True),
    path(f"M0 {H} L0 380 L160 300 L300 400 L420 330 L520 420 L640 300 L800 380 L1000 320 L1000 {H} Z",
         fill="#c8b48a", sw=6),
    path("M640 300 L800 380 L1000 320 L1000 640 L640 640 Z", fill="#b09a72", sw=6),
    domkam(150, 400, 0.5, pose="cup_mouth"),
    sound_rings(200, 330, 3, 44, w["accent"], 7, 70, .9, 70),
    sound_rings(700, 330, 3, 44, w["accent"], 6, 70, .45, 250),
])

B3[20] = lambda w: "".join([                                  # say your name to the mountain
    jungle_bg(w, pale=True),
    path(f"M0 {H} L0 400 L220 280 L420 400 L620 300 L840 400 L1000 340 L1000 {H} Z",
         fill="#c8b48a", sw=6),
    "".join(person(180 + i * 220, 620, 0.9, pose="cup_mouth",
                   **{q: KIDS[i][q] for q in ("skin", "hair", "shirt", "hairstyle")}) for i in range(4)),
    "".join(path(f"M{230 + i * 220} 470 Q{420 + i * 120} 300 {700} 360",
                 stroke=w["accent"], sw=7 - i * 1.4, dash="16 14",
                 op=.85 - i * .18) for i in range(4)),
])


BOOK_SCENES = {1: B1, 2: B2, 3: B3}

# --- generated books (week 4 onward) ---------------------------------------
_ENGINE = {}


def _engine_book(book):
    """(World, [10 scene keys]) for a generated book, or None for books 1-3."""
    if book in _ENGINE:
        return _ENGINE[book]
    try:
        from plan import by_week
        from worlds import WORLDS as WMAP
        from compose import scene_plan
        row = by_week(book)
        val = (WMAP[row[3]], scene_plan(row[4]))
    except Exception:
        val = None
    _ENGINE[book] = val
    return val


def _engine_scene(book, page):
    import scenes as S
    world, plan10 = _engine_book(book)
    pal = world.pal()
    if page == 1:
        return sc_title(pal, book)
    if page == 2:
        return sc_note(pal)
    if page in (3, 21):
        return sc_breathe_in(pal)
    if page == 4:
        return sc_breathe_out(pal)
    if page == 5:
        return sc_clap_slow(pal)
    if page == 6:
        return sc_clap_fast(pal)
    if page == 22:
        return sc_clap_fast(pal, pilots=False)
    if page == 23:
        return classroom(pal, ship_glow=0, kid_pose="clap", face="happy",
                         extra=domkam(428, 452, 0.62, pose="clap")
                               + johnson(586, 448, 0.62, pose="point", flip=True))
    if page == 24:
        return sc_theme(pal)
    if page == 7:
        return S.b_departure(world)
    if page == 8:
        return S.b_porthole(world)
    if page == 9:
        return S.b_arrival(world)
    if page == 10:
        return S.b_reveal(world)
    if 11 <= page <= 20:
        return S.CONCEPTS[plan10[page - 11]](world)
    raise KeyError((book, page))


def scene(book, page):
    """Return SVG markup for one page of one book."""
    if book not in BOOK_SCENES:
        return _engine_scene(book, page)
    w = WORLDS[book]
    if page == 1:
        return sc_title(w, book)
    if page == 2:
        return sc_note(w)
    if page == 3:
        return sc_breathe_in(w)
    if page == 4:
        return sc_breathe_out(w)
    if page == 5:
        return sc_clap_slow(w)
    if page == 6:
        return sc_clap_fast(w)
    if page == 21:
        return sc_breathe_in(w)
    if page == 22:
        return sc_clap_fast(w, pilots=False)
    if page == 23:
        return classroom(w, ship_glow=0, kid_pose="clap", face="happy",
                         extra=domkam(428, 452, 0.62, pose="clap")
                               + johnson(586, 448, 0.62, pose="point", flip=True))
    if page == 24:
        return sc_theme(w)
    return BOOK_SCENES[book][page](w)


def sc_theme(w):
    """Decorative only. The four labelled beats are drawn by the layout on top,
    so this must not repeat them."""
    o = [frame(w["deep"])]
    for i in range(4):
        x = 155 + i * 230
        o.append(circle(x, 300, 120, w["mid"], stroke=None).replace("/>", ' opacity="0.30"/>'))
        o.append(sound_rings(x, 300, 3, 30, w["accent"], 5, 132, .22, 300))
    o.append("".join(sparkle(70 + (i * 137) % 880, 70 + (i * 91) % 500, 12, w["light"], .22)
                     for i in range(14)))
    o.append(path("M0 596 q125 -46 250 0 t250 0 t250 0 t250 0", stroke=w["mid"], sw=8, op=.35))
    return "".join(o)


# --------------------------------------------------------------- bleed
# The reader letterboxes a 1000x640 scene inside whatever aspect the device
# has. Painting a bleed rect in each scene's own base colour makes those
# bands disappear instead of showing a hard seam.
_CLASSROOM = {1: "#bfeaf0", 2: "#2a2a6e", 3: "#cfe8b8"}
_WORLD = {1: "#0d5570", 2: "#12143c", 3: "#cfe8b8"}
_SPECIAL = {
    (1, 7): "#4aa3c4", (1, 19): "#07293a", (1, 20): "#07293a",
    (2, 7): "#12143c", (2, 19): "#05061a", (2, 20): "#05061a",
    (3, 7): "#cfe8b8", (3, 14): "#e8f2d4", (3, 19): "#e8f2d4", (3, 20): "#e8f2d4",
}


def bg_color(book, page):
    """The colour the letterbox bands should be for this page."""
    if book not in WORLDS:
        eng = _engine_book(book)
        if eng:
            world = eng[0]
            if page == 2:
                return world.sand
            if page in (8, 24):
                return world.deep
            if page in (1, 3, 4, 5, 6, 21, 22, 23):
                return world.sky
            if page == 7:
                return world.deep if world.kind == "space" else "#4aa3c4"
            if world.kind == "space":
                return world.deep
            if world.kind == "water":
                return world.mid
            return world.sky
        return "#0b3a4a"
    if (book, page) in _SPECIAL:
        return _SPECIAL[(book, page)]
    if page == 2:
        return WORLDS[book]["sand"]
    if page in (8, 24):
        return WORLDS[book]["deep"]
    if page in (1, 3, 4, 5, 6, 21, 22, 23):
        return _CLASSROOM[book]
    return _WORLD[book]


def bleed(book, page):
    """A rect large enough to paint the letterbox area outside the viewBox."""
    return (f'<rect x="-1200" y="-1200" width="3400" height="3040" '
            f'fill="{bg_color(book, page)}"/>')
