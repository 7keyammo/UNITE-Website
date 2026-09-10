# -*- coding: utf-8 -*-
"""The scene engine.

Books 1-3 were hand-composed. That does not scale to 50, so every book from
4 onward is generated from two small inputs:

  a WORLD  — palette, backdrop kind, terrain, and a cast of creatures
  a BEAT   — which reusable concept scene each page carries

The concept scenes are the curriculum made visual: two_sizes is amplitude,
two_speeds is frequency, feel_ground is energy through solids, and so on.
A new book picks six of them and names a world; the art follows.
"""
import math

from prims import (STROKE, KIDS, person, domkam, johnson, ship, sound_rings,
                   star, sparkle, circle, ellipse, rect, path, g)
import fauna as F

W, H = 1000, 640


def _kid(i, **kw):
    k = KIDS[i % 6]
    return dict({q: k[q] for q in ("skin", "hair", "shirt", "hairstyle")}, **kw)


def _hex(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def shade(col, t, toward="#0a1018"):
    """Mix col toward another colour. t=0 unchanged, t=1 fully toward."""
    a, b = _hex(col), _hex(toward)
    m = tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))
    return "#%02x%02x%02x" % m


def frame(c):
    return rect(0, 0, W, H, c, stroke=None)


def grad(gid, top, bottom):
    return (f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{top}"/>'
            f'<stop offset="1" stop-color="{bottom}"/></linearGradient></defs>'
            f'<rect width="{W}" height="{H}" fill="url(#{gid})"/>')


# ===================================================================== world
class World:
    """Everything the engine needs to draw one destination."""

    def __init__(self, key, deep, mid, light, accent, sand, sky, ground,
                 kind="land", terrain="hills", flora=(), cast=(), hero=None,
                 air=(), horizon=430, quiet=None):
        self.key, self.kind = key, kind
        self.deep, self.mid, self.light = deep, mid, light
        self.accent, self.sand = accent, sand
        self.sky, self.ground = sky, ground
        self.terrain, self.flora, self.cast = terrain, list(flora), list(cast)
        self.hero = hero or (self.cast[0] if self.cast else None)
        self.air, self.horizon = list(air), horizon
        self.quiet = quiet or deep          # colour for the hush pages

    # -- backdrop ---------------------------------------------------------
    def bg(self, dim=False, pale=False):
        gid = f"g{self.key}{int(dim)}{int(pale)}"
        if self.kind == "water":
            top = self.quiet if dim else self.mid
            o = [grad(gid, top, self.deep if dim else self.deep)]
            o += [path(f"M0 {36 + i * 26} q120 -22 240 0 t240 0 t240 0 t240 0",
                       stroke="#ffffff", sw=5, op=.10) for i in range(3)]
            return "".join(o)
        if self.kind == "space":
            o = [f'<defs><radialGradient id="{gid}" cx="50%" cy="40%">'
                 f'<stop offset="0" stop-color="{self.quiet if dim else self.mid}"/>'
                 f'<stop offset="1" stop-color="{self.deep}"/></radialGradient></defs>',
                 f'<rect width="{W}" height="{H}" fill="url(#{gid})"/>']
            n = 24 if dim else 58
            for i in range(n):
                x = (i * 137 + 61) % (W - 20) + 10
                y = (i * 89 + 31) % (H - 20) + 10
                o.append(circle(x, y, 2 + (i % 3), "#ffffff", stroke=None)
                         .replace("/>", f' opacity="{[.35,.55,.8][i%3]}"/>'))
            return "".join(o)
        if self.kind == "interior":
            top = self.mid if not (dim or pale) else (
                shade(self.mid, .45) if dim else shade(self.light, .25, "#ffffff"))
            return grad(gid, top, self.deep if not pale else self.mid)
        top, bot = self.sky, self.light
        if dim:
            top, bot = shade(top, .58), shade(bot, .46)
        elif pale:
            top, bot = shade(top, .45, "#ffffff"), shade(bot, .35, "#ffffff")
        return grad(gid, top, bot)

    # -- ground -----------------------------------------------------------
    def floor(self, y=None, dim=False, pale=False):
        y = self.horizon if y is None else y
        gcol = self.ground
        if dim:
            gcol = shade(gcol, .52)
        elif pale:
            gcol = shade(gcol, .34, "#ffffff")
        if self.kind == "water":
            return (path(f"M0 {H} L0 {y + 90} Q250 {y + 40} 500 {y + 76} "
                         f"Q750 {y + 112} {W} {y + 62} L{W} {H} Z",
                         fill=shade(self.sand, .5) if dim else self.sand, sw=6))
        if self.kind == "space":
            return ""
        t = self.terrain
        if t == "peaks":
            return F.peaks(y, gcol)
        if t == "dunes":
            return F.dunes(y, gcol)
        if t == "flat":
            return F.flat_ground(y, gcol)
        return F.hills(y, gcol)

    def scenery(self, seed=0, n=None):
        """Flora scattered along the horizon."""
        out = []
        if not self.flora:
            return ""
        n = n if n is not None else min(4, len(self.flora) * 2)
        for i in range(n):
            fn, kw = self.flora[(i + seed) % len(self.flora)]
            x = 70 + (i * 263 + seed * 91) % (W - 140)
            out.append(fn(x, self.horizon + 190, **kw))
        return "".join(out)

    # The generators have wildly different intrinsic sizes (a beast is drawn
    # ~370 units tall, a flier ~60), so normalise them: s=1.0 should mean the
    # same apparent size whichever animal a world happens to cast.
    NORM = {"swimmer": 1.0, "flier": 1.35, "bug": 1.15,
            "beast": 0.30, "critter": 0.95}

    def creature(self, i, x, y, s=1.0, flip=False):
        if not self.cast:
            return ""
        fn, kw = self.cast[i % len(self.cast)]
        n = self.NORM.get(getattr(fn, "__name__", ""), 1.0)
        return fn(x, y, s * n, flip=flip, **kw)

    def creature_lift(self, i):
        """Beasts stand on their feet; swimmers and fliers hang from the middle."""
        if not self.cast:
            return 0
        return 0 if getattr(self.cast[i % len(self.cast)][0], "__name__", "") in (
            "beast", "critter") else 0

    def airborne(self, seed=0, n=3):
        out = []
        for i in range(n):
            if self.air:
                fn, kw = self.air[(i + seed) % len(self.air)]
                out.append(fn(120 + i * 300, 120 + (i % 2) * 70, **kw))
            elif self.kind == "water":
                out.append(F.bubble(140 + i * 240, 120 + (i % 3) * 80, 9 + i * 3))
            elif self.kind == "space":
                out.append(sparkle(150 + i * 260, 110 + (i % 2) * 70, 13, "#ffffff", .7))
        return "".join(out)

    def pal(self):
        """The palette dict shape art.py's shared classroom scenes expect."""
        return dict(deep=self.deep, mid=self.mid, light=self.light,
                    accent=self.accent, sand=self.sand, sky=self.sky,
                    ground=self.ground)

    def stand_y(self):
        """Where a child's feet go."""
        return 600 if self.kind != "water" else 596


# ============================================================ generic beats
def b_departure(w, ups=4):
    """The ship climbing away from the classroom toward the new world."""
    o = [grad("dep" + w.key, w.deep if w.kind == "space" else "#4aa3c4", w.sky)]
    for i in range(ups):
        o.append(F.cloud(140 + i * 250, 130 + (i % 2) * 58, 0.9))
    o.append(rect(52, 496, 168, 144, "#eaf6f7", r=10, sw=6))
    o.append(path("M136 496 L136 640 M52 568 L220 568", sw=5))
    o.append(ship(540, 300, 0.98, glow=3, lamps=4, tilt=-6))
    o += [path(f"M{452 + i * 76} 500 l0 140", stroke="#ffd166", sw=12, op=.6) for i in range(3)]
    return "".join(o)


def b_porthole(w, inner=None):
    o = [frame(w.deep), circle(500, 320, 250, w.mid, sw=14),
         f'<clipPath id="ph{w.key}"><circle cx="500" cy="320" r="243"/></clipPath>']
    body = inner if inner is not None else (w.bg() + w.floor(520) + w.scenery(2, 3))
    o.append(f'<g clip-path="url(#ph{w.key})">{body}</g>')
    o.append(circle(500, 320, 250, "none", sw=14))
    o.append(path("M370 210 a180 180 0 0 1 120 -58", stroke="#ffffff", sw=16, op=.45))
    for a in range(8):
        ang = math.radians(a * 45 + 22)
        o.append(circle(round(500 + 272 * math.cos(ang)), round(320 + 272 * math.sin(ang)),
                        11, w.accent, sw=4))
    return "".join(o)


def b_arrival(w):
    o = [w.bg(), w.floor(), w.scenery(1, 3)]
    o.append(ship(500, 350, 0.72, glow=2, lamps=1, tilt=-4))
    o.append(w.airborne(1, 4))
    return "".join(o)


def b_reveal(w):
    """The busiest page in the book: the whole world at once."""
    o = [w.bg(), w.floor(), w.scenery(0, 4)]
    spots = [(200, 1.15), (520, 1.4), (830, 0.95)]
    for i, (x, s) in enumerate(spots):
        yy = w.horizon + 110 if w.kind != "water" else 290 + i * 90
        o.append(w.creature(i, x, yy, s, flip=i % 2 == 1))
    o.append(w.airborne(2, 4))
    o.append(ship(120, w.horizon + 150, 0.3, glow=1, lamps=0))
    return "".join(o)


# ========================================================== concept scenes
def c_listen(w, **kw):
    """Cup your ears. STEAM Class 7 — the outer ear is a dish."""
    y = w.stand_y()
    return "".join([w.bg(), w.floor(), w.scenery(3, 2),
                    person(300, y, 1.3, pose="cup_ears", **_kid(0)),
                    person(660, y, 1.3, pose="cup_ears", flip=True, **_kid(3)),
                    w.creature(0, 890, y - 290, 1.2, flip=True),
                    sound_rings(840, y - 300, 4, 38, "#ffffff", 6, 60, .55, 150)])


def c_two_sizes(w, **kw):
    """Big vs tiny — amplitude. EFV Lesson 4."""
    y = w.stand_y()
    return "".join([w.bg(), w.floor(), w.scenery(4, 2),
                    path("M500 40 L500 600", stroke="#ffffff", sw=5, dash="18 16", op=.35),
                    person(250, y, 1.35, pose="clap_big", **_kid(2)),
                    sound_rings(250, y - 200, 4, 34, w.accent, 10, 90, 1, 170),
                    person(750, y, 1.0, pose="clap", **_kid(5)),
                    sound_rings(750, y - 160, 2, 20, w.accent, 5, 46, .5, 150)])


def c_two_speeds(w, **kw):
    """Fast vs slow — frequency. EFV Lesson 3."""
    y = w.stand_y()
    return "".join([w.bg(), w.floor(), w.scenery(5, 2),
                    path("M500 40 L500 600", stroke="#ffffff", sw=5, dash="18 16", op=.3),
                    person(260, y, 1.25, pose="reach_high", **_kid(3)),
                    sound_rings(300, 190, 6, 17, "#ffd166", 5, 44, .95, 210),
                    person(730, y, 1.25, pose="curl_low", **_kid(0)),
                    sound_rings(770, 330, 3, 52, w.accent, 8, 64, .95, 210)])


def c_wave(w, **kw):
    """Draw the wave with your arm. EFV Lesson 13."""
    y = w.stand_y()
    return "".join([w.bg(),
                    path("M0 300 q125 -120 250 0 t250 0 t250 0 t250 0", stroke=w.accent, sw=16, op=.95),
                    path("M0 370 q125 -120 250 0 t250 0 t250 0 t250 0", stroke="#ffd166", sw=10, op=.6),
                    "".join(person(160 + i * 170, y, 1.0, pose="wave_arm", flip=i % 2 == 1, **_kid(i))
                            for i in range(5))])


def c_count(w, n=4, **kw):
    """n counted stomps. EFV Lesson 6 / STEAM Class 4."""
    y = w.stand_y() - 60
    o = [w.bg(), w.floor(), w.scenery(6, 2)]
    for i in range(n):
        x = 170 + i * (660 // max(1, n - 1))
        o.append(person(x, y, 0.95, pose="stomp", **_kid(i)))
        o.append(F.hills(0, w.accent) if False else "")
        o.append("".join(ellipse(x + 20, y + 12, 50 + j * 22, (50 + j * 22) * .26, "none",
                                 stroke=w.accent, sw=6).replace("/>", f' opacity="{.8 - j * .3}"/>')
                         for j in range(2)))
        o.append(f'<text x="{x}" y="{y + 84}" text-anchor="middle" font-family="sans-serif" '
                 f'font-size="44" font-weight="700" fill="{w.deep}">{i + 1}</text>')
    return "".join(o)


def c_double(w, **kw):
    """Four, then eight. EFV Lesson 10 — doubling."""
    o = [w.bg(pale=True), w.floor(pale=True),
         path("M60 300 L940 300", stroke=STROKE, sw=4, dash="14 14", op=.4)]
    for i in range(4):
        o.append("".join(ellipse(150 + i * 230, 200, 60 + j * 0, 16, "none", stroke=w.mid,
                                 sw=9) for j in range(1)))
    for i in range(8):
        o.append(ellipse(120 + i * 108, 420, 46, 13, "none", stroke=w.accent, sw=7))
    o.append(f'<text x="500" y="126" text-anchor="middle" font-family="sans-serif" '
             f'font-size="42" font-weight="700" fill="{w.deep}">4</text>')
    o.append(f'<text x="500" y="556" text-anchor="middle" font-family="sans-serif" '
             f'font-size="42" font-weight="700" fill="{w.deep}">8</text>')
    return "".join(o)


def c_feel_ground(w, **kw):
    """Palms flat — energy travelling through solids. EFV Lessons 2 and 11."""
    y = w.stand_y()
    o = [w.bg(), w.floor(), w.scenery(7, 2),
         person(250, y, 1.3, pose="palms_down", **_kid(2)),
         person(470, y, 1.3, pose="palms_down", **_kid(5))]
    o.append(w.creature(0, 1010, w.horizon + 120, 1.3))
    o += [ellipse(770, w.horizon + 90, 60 + i * 62, (60 + i * 62) * .26, "none",
                  stroke=w.accent, sw=9).replace("/>", f' opacity="{1 - i * .2}"/>')
          for i in range(5)]
    return "".join(o)


def c_echo(w, **kw):
    """Call, then wait. STEAM Class 9 — acoustics."""
    y = w.stand_y() + 20
    o = [w.bg(pale=True),
         F.peaks(360, shade(w.ground, .18), [(0, 40), (220, -80), (420, 40),
                                             (620, -60), (840, 40), (1000, -20)])]
    o += [person(180 + i * 220, y, 0.9, pose="cup_mouth", **_kid(i)) for i in range(4)]
    o += [path(f"M{230 + i * 220} 470 Q{420 + i * 120} 300 700 360",
               stroke=w.accent, sw=7 - i * 1.4, dash="16 14", op=.85 - i * .18)
          for i in range(4)]
    return "".join(o)


def c_silence(w, **kw):
    """The hush. Deliberately the emptiest page in the book."""
    o = [w.bg(dim=True)]
    if w.kind != "space":
        o.append(w.floor(dim=True))
    o.append(ship(500, 340, 0.28, glow=1, lamps=0))
    return "".join(o)


def c_resonance(w, **kw):
    """Hum with it and feel it in your own chest. EFV Lesson 9."""
    o = [w.bg(dim=True)]
    if w.kind != "space":
        o.append(w.floor(dim=True))
    o.append(circle(690, 290, 205, shade(w.mid, .2, "#ffffff"), sw=10)
             .replace("/>", ' opacity="0.7"/>'))
    o.append(w.creature(0, 690, 330, 1.5))
    o.append(person(270, 580, 1.65, pose="hand_on_chest", face="calm", **_kid(0)))
    o.append(sound_rings(400, 320, 4, 40, "#ffd166", 6, 80, .8, 60))
    o.append(circle(290, 330, 46, "#ffd166", stroke=None).replace("/>", ' opacity="0.22"/>'))
    return "".join(o)


def c_layers(w, **kw):
    """Three sound sources at once. STEAM Class 10 — layering."""
    y = w.stand_y()
    o = [w.bg(), w.floor(), w.scenery(8, 2)]
    for i, (x, s, n, sp) in enumerate(((210, 1.15, 2, 54), (500, 1.0, 4, 30), (790, 0.85, 6, 17))):
        o.append(person(x, y, s, pose="clap", **_kid(i + 1)))
        o.append(sound_rings(x, y - 210, n, sp, [w.accent, "#ffd166", w.light][i], 7, 56, .9, 220))
    return "".join(o)


def c_absorb(w, **kw):
    """Soft things eat sound. EFV Lesson 12 / STEAM Class 14."""
    y = w.stand_y()
    o = [w.bg(), w.floor(y - 40)]
    o.append(path(f"M330 {y - 46} q170 -104 344 0 Z", fill=w.sand, sw=6))
    o.append(w.creature(0, 560, y - 84, 0.9))
    o.append(sound_rings(640, y - 130, 2, 26, "#ffd166", 6, 66, .38, 130))
    o.append(person(180, y, 1.0, pose="cup_ears", **_kid(4)))
    return "".join(o)


def c_travel(w, **kw):
    """Pass it down the line. EFV Lesson 11 — a wave is a chain of pushes."""
    y = w.stand_y()
    o = [w.bg(), w.floor(), w.scenery(9, 2)]
    for i in range(5):
        x = 130 + i * 185
        o.append(person(x, y, 0.95, pose="clap" if i % 2 == 0 else "still", **_kid(i)))
        if i < 4:
            o.append(path(f"M{x + 60} {y - 150} L{x + 128} {y - 150}", stroke=w.accent,
                          sw=8, dash="14 12", op=.9))
    return "".join(o)


def c_hero(w, **kw):
    """A single big creature, close and calm — the awe beat."""
    o = [w.bg(dim=True)]
    if w.kind != "space":
        o.append(w.floor(dim=True))
    o.append(w.creature(0, 520, 330 if w.kind == "water" else w.horizon + 90, 2.3))
    o.append(sound_rings(250, 310, 4, 62, w.light, 6, 120, .45, 90))
    o.append(ship(120, 560, 0.3, glow=1, lamps=0))
    return "".join(o)


def c_close_up(w, **kw):
    """One creature, the children watching. The quieter discovery beat."""
    y = w.stand_y()
    return "".join([w.bg(), w.floor(), w.scenery(10, 2),
                    w.creature(0, 620, w.horizon + 100, 1.5),
                    sound_rings(700, w.horizon - 20, 3, 40, "#ffd166", 7, 90, .7, 140),
                    person(200, y, 1.05, pose="point", **_kid(1))])


CONCEPTS = {
    "listen": c_listen, "two_sizes": c_two_sizes, "two_speeds": c_two_speeds,
    "wave": c_wave, "count": c_count, "double": c_double,
    "feel_ground": c_feel_ground, "echo": c_echo, "silence": c_silence,
    "resonance": c_resonance, "layers": c_layers, "absorb": c_absorb,
    "travel": c_travel, "hero": c_hero, "close_up": c_close_up,
}
