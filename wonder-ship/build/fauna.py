# -*- coding: utf-8 -*-
"""Parametric creatures, plants and props.

The series needs 50 worlds. Hand-drawing every animal does not scale, so
everything living is built from a handful of parametric generators: give a
generator a palette and a few proportions and it produces a creature that
matches the house style (flat colour, heavy outline, one-word readable).
"""
import math

from prims import (STROKE, circle, ellipse, rect, path, capsule, star,
                   sparkle, sound_rings)


def _wrap(x, y, s, flip, body):
    return (f'<g transform="translate({x} {y}) scale({-s if flip else s} {s})">'
            + "".join(body) + "</g>")


def eye(x, y, r=8):
    return circle(x, y, r, "#ffffff", sw=3) + circle(x + 1, y, r * 0.45, STROKE, stroke=None)


# ---------------------------------------------------------------- swimmers
def swimmer(x, y, s=1.0, body="#ffd166", fin=None, flip=False, tall=0.62, tail=1.0):
    """Fish, whale, seal, tadpole — anything that moves through water."""
    fin = fin or body
    r = 46
    o = [path(f"M{r * .9} 0 L{r * 1.6 * tail} {-26 * tail} L{r * 1.6 * tail} {26 * tail} Z", fill=fin),
         ellipse(0, 0, r, r * tall, body),
         path(f"M-4 {-r * tall - 2} L10 {-r * tall - 18} L22 {-r * tall} Z", fill=fin, sw=4),
         eye(-r * .44, -r * tall * .28)]
    return _wrap(x, y, s, flip, o)


# ---------------------------------------------------------------- fliers
def flier(x, y, s=1.0, body="#e86a92", wing=None, flip=False, beak="#ffd166", wingspan=1.0):
    """Bird, bat, butterfly-ish. Wings up = mid-flap."""
    wing = wing or body
    o = [path(f"M-10 -6 Q{-70 * wingspan} {-60 * wingspan} {-86 * wingspan} {-14 * wingspan} "
              f"Q{-52 * wingspan} -6 -8 8 Z", fill=wing, sw=5),
         path(f"M10 -6 Q{70 * wingspan} {-60 * wingspan} {86 * wingspan} {-14 * wingspan} "
              f"Q{52 * wingspan} -6 8 8 Z", fill=wing, sw=5),
         ellipse(0, 0, 30, 24, body),
         circle(20, -24, 18, body),
         path("M34 -26 L58 -20 L34 -12 Z", fill=beak, sw=4),
         eye(24, -30, 6)]
    return _wrap(x, y, s, flip, o)


def bug(x, y, s=1.0, body="#ffd166", stripe="#23303a", wing="#eaf6f7", flip=False):
    """Bee, beetle, fly. The wings are the fast-vibration prop."""
    o = [ellipse(-26, -22, 22, 13, wing, sw=3, rot=-22).replace("/>", ' opacity="0.75"/>'),
         ellipse(26, -22, 22, 13, wing, sw=3, rot=22).replace("/>", ' opacity="0.75"/>'),
         ellipse(0, 0, 38, 27, body),
         path("M-12 -24 L-12 24 M8 -25 L8 25", stroke=stripe, sw=9),
         circle(34, -8, 17, body),
         eye(40, -12, 6),
         path("M40 -22 L52 -38 M46 -18 L60 -28", stroke=STROKE, sw=4)]
    return _wrap(x, y, s, flip, o)


# ---------------------------------------------------------------- walkers
def beast(x, y, s=1.0, body="#4a9c6d", legs=4, neck=0.0, tail=1.0, horns=0,
          flip=False, ears=0, mouth_open=False, humps=0):
    """One generator for every four-legged animal in the series.

    neck  0 = head sits on the body (bear, sheep)  1 = long neck (sauropod)
    tail  length multiplier                        horns/ears  0-2 features
    """
    BY, RX, RY = -150, 128, 72           # body centre and radii
    o = []
    if tail:
        tx, ty = -RX - 110 * tail, BY - 40 * tail
        o.append(capsule(-RX + 20, BY - 6, tx, ty, body, 28))
        o.append(circle(tx, ty, 14, body, stroke=None))
    o.append(ellipse(0, BY, RX, RY, body, sw=7))
    for i in range(humps):
        o.append(path(f"M{-52 + i * 104} {BY - RY + 8} q52 -70 104 0 Z", fill=body, sw=7))
    span = 176
    step = span // max(1, legs - 1)
    for i in range(legs):
        lx = -span // 2 + i * step
        o.append(capsule(lx, BY + RY - 14, lx + (8 if i % 2 else -8), 0, body, 38))
        o.append(ellipse(lx + (8 if i % 2 else -8), -4, 24, 12, body, sw=5))
    hx, hy = 92 + 92 * neck, BY - 52 - 150 * neck
    o.append(capsule(RX - 44, BY - 30, hx, hy + 24, body, 38))
    o.append(ellipse(hx, hy, 52, 37, body, sw=7, rot=-10))
    o.append(path(f"M{hx + 38} {hy - 10} q28 4 32 17 q-24 11 -36 2 Z", fill=body, sw=5))
    o.append(eye(hx - 2, hy - 12, 10))
    if mouth_open:
        o.append(path(f"M{hx + 42} {hy + 6} q30 6 26 26 q-26 8 -36 -8 Z", fill="#7a2c3a", sw=5))
    for i in range(horns):
        o.append(capsule(hx - 12 + i * 26, hy - 30, hx - 28 + i * 56, hy - 78, "#f4ead3", 13))
    for i in range(ears):
        o.append(ellipse(hx - 18 + i * 34, hy - 36, 15, 23, body, sw=5, rot=-22 + i * 44))
    o.append(path(f"M-72 {BY + 26} q72 32 144 -4", stroke="#ffffff", sw=9, op=.26))
    return _wrap(x, y, s, flip, o)


def critter(x, y, s=1.0, body="#e0a44a", ears=2, tail=0.5, flip=False):
    """Small ground animal — mouse, frog, rabbit, crab-ish."""
    o = [capsule(-38, -44, -38 - 40 * tail, -64 - 26 * tail, body, 15),
         circle(-38 - 40 * tail, -64 - 26 * tail, 8, body, stroke=None),
         ellipse(0, -38, 48, 35, body, sw=6),
         capsule(-20, -14, -24, -4, body, 22), capsule(20, -14, 26, -4, body, 22),
         ellipse(-24, -3, 17, 9, body, sw=4), ellipse(26, -3, 17, 9, body, sw=4),
         circle(36, -62, 28, body, sw=6),
         path("M62 -60 q18 3 20 13 q-16 8 -24 0 Z", fill=body, sw=4),
         eye(42, -68, 7)]
    for i in range(ears):
        o.append(ellipse(22 + i * 26, -84, 11, 20, body, sw=5, rot=-16 + i * 32))
    return _wrap(x, y, s, flip, o)


# ---------------------------------------------------------------- flora
def tree(x, base, s=1.0, trunk="#8b5a2b", leaf="#3f6b34", kind="round", h=200):
    o = [capsule(0, 0, 0, -h, trunk, 26)]
    if kind == "round":
        o += [circle(0, -h - 40, 78, leaf, sw=6), circle(-58, -h + 4, 52, leaf, sw=6),
              circle(58, -h + 4, 52, leaf, sw=6)]
    elif kind == "palm":
        for a in (-70, -35, 0, 35, 70):
            o.append(path(f"M0 -{h} q{a} -46 {a * 1.7} -6", stroke=leaf, sw=17))
    elif kind == "pine":
        for i in range(3):
            w = 86 - i * 20
            o.append(path(f"M0 {-h - 30 - i * 52} L{-w} {-h + 24 - i * 52} L{w} {-h + 24 - i * 52} Z",
                          fill=leaf, sw=6))
    elif kind == "bare":
        for a, ln in ((-1, 70), (1, 78), (-1, 50)):
            o.append(capsule(0, -h + 20, a * ln, -h - 46, trunk, 12))
    return _wrap(x, base, s, False, o)


def frond(x, base, h=200, color="#3f6b34", flip=False, blades=5):
    o = [path(f"M0 0 Q{-10 if flip else 10} {-h // 2} 0 {-h}", stroke=color, sw=10)]
    for i in range(blades):
        yy = -h * (i + 1) / (blades + 1)
        o.append(path(f"M0 {yy:.0f} q40 -18 62 -6", stroke=color, sw=8))
        o.append(path(f"M0 {yy:.0f} q-40 -18 -62 -6", stroke=color, sw=8))
    return _wrap(x, base, 1.0, flip, o)


def grass_row(y, color="#4a7c3f", n=19, w=1000, h=180, seed=1):
    out = []
    for i in range(n):
        x = 20 + i * (w / n)
        lean = 14 if i % 2 else -14
        out.append(path(f"M{x:.0f} {y} q{lean} {-h//2} {-lean//2} {-h}", stroke=color, sw=13, op=.95))
    return "".join(out)


# ---------------------------------------------------------------- terrain
def hills(y, color, n=3, amp=90, w=1000, H=640):
    d = f"M0 {H} L0 {y}"
    step = w / n
    for i in range(n):
        d += f" q{step/2:.0f} {-amp} {step:.0f} 0"
    d += f" L{w} {H} Z"
    return path(d, fill=color, sw=6)


def peaks(y, color, pts=None, w=1000, H=640):
    pts = pts or [(0, 60), (160, -80), (300, 20), (420, -50), (520, 40),
                  (640, -80), (800, 0), (1000, -60)]
    d = f"M0 {H} L0 {y + pts[0][1]}"
    for px, py in pts[1:]:
        d += f" L{px} {y + py}"
    d += f" L{w} {H} Z"
    return path(d, fill=color, sw=6)


def flat_ground(y, color, w=1000, H=640):
    return path(f"M0 {H} L0 {y} L{w} {y} L{w} {H} Z", fill=color, sw=6)


def dunes(y, color, w=1000, H=640):
    return path(f"M0 {H} L0 {y + 30} Q250 {y - 50} 500 {y + 10} "
                f"Q750 {y + 60} {w} {y - 20} L{w} {H} Z", fill=color, sw=6)


def crystal(x, base, h=140, color="#a9a6f2", w=44):
    return path(f"M{x} {base} L{x - w} {base - h * .55} L{x - w * .5} {base - h} "
                f"L{x + w * .5} {base - h} L{x + w} {base - h * .55} Z", fill=color, sw=6)


def cloud(x, y, s=1.0, color="#ffffff", sw=5):
    o = [circle(-46, 6, 40, color, sw=sw), circle(0, -14, 52, color, sw=sw),
         circle(48, 6, 38, color, sw=sw), rect(-46, -4, 96, 44, color, r=22, sw=sw)]
    return _wrap(x, y, s, False, o)


def bubble(x, y, r):
    return (circle(x, y, r, "#ffffff", stroke="#cfeef2", sw=3).replace("/>", ' opacity="0.5"/>')
            + circle(x - r * .3, y - r * .3, max(2, r * .22), "#ffffff", stroke=None))


def building(x, base, w=120, h=200, color="#c98a4b", windows="#ffd166", rows=3):
    o = [rect(-w / 2, -h, w, h, color, r=8, sw=6)]
    for r_ in range(rows):
        for c in range(2):
            o.append(rect(-w / 2 + 18 + c * (w / 2 - 4), -h + 22 + r_ * (h / rows - 6),
                          w / 4 - 6, h / rows - 30, windows, r=4, sw=4))
    return _wrap(x, base, 1.0, False, o)
