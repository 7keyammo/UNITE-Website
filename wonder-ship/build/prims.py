# -*- coding: utf-8 -*-
"""SVG primitives for The Wonder Ship.

Everything is plain SVG string building. No dependencies, so the output
inlines cleanly into an offline HTML package, a print page, and an EPUB.

Art rules (from brief/ILLUSTRATION-BRIEF.md):
  bright, high-contrast, simple shapes; heavy outlines; nothing photoreal;
  a 3-year-old must be able to name every object in one word.
"""

STROKE = "#23303a"      # single heavy outline colour used everywhere
SW = 5                  # default stroke weight

# Six recurring children. Consistent skin/hair/shirt so a child can find
# "their" kid across all three books.
KIDS = [
    dict(skin="#8d5524", hair="#2b1b12", shirt="#ef476f", hairstyle="puff"),
    dict(skin="#f1c27d", hair="#c46a10", shirt="#06d6a0", hairstyle="short"),
    dict(skin="#5c3317", hair="#1a1008", shirt="#ffd166", hairstyle="braids"),
    dict(skin="#ffdbac", hair="#f4d35e", shirt="#4cc9f0", hairstyle="bob"),
    dict(skin="#a86b3c", hair="#3d2314", shirt="#b388eb", hairstyle="curls"),
    dict(skin="#e0ac69", hair="#6b3e26", shirt="#ff8fab", hairstyle="short"),
]


def g(content, **attrs):
    a = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return f"<g {a}>{content}</g>" if a else f"<g>{content}</g>"


def circle(cx, cy, r, fill, stroke=STROKE, sw=SW):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"{s}/>'


def ellipse(cx, cy, rx, ry, fill, stroke=STROKE, sw=SW, rot=0):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    t = f' transform="rotate({rot} {cx} {cy})"' if rot else ""
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}"{s}{t}/>'


def rect(x, y, w, h, fill, r=0, stroke=STROKE, sw=SW, rot=None):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    t = f' transform="rotate({rot[0]} {rot[1]} {rot[2]})"' if rot else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{s}{t}/>'


def path(d, fill="none", stroke=STROKE, sw=SW, cap="round", join="round", dash=None, op=None):
    s = f' stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}" stroke-linejoin="{join}"' if stroke else ""
    da = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' opacity="{op}"' if op is not None else ""
    return f'<path d="{d}" fill="{fill}"{s}{da}{o}/>'


def limb(x1, y1, x2, y2, color, sw=13):
    """A thick rounded line. Arms and legs are just these."""
    return path(f"M{x1} {y1} L{x2} {y2}", stroke=color, sw=sw, cap="round")


def bent_limb(x1, y1, xm, ym, x2, y2, color, sw=13):
    return path(f"M{x1} {y1} Q{xm} {ym} {x2} {y2}", stroke=color, sw=sw, cap="round")


# --------------------------------------------------------------- people
POSES = (
    "hand_on_chest", "clap", "clap_big", "arms_up", "float", "cup_ears",
    "stomp", "tiptoe", "wave_arm", "reach_high", "curl_low", "sit",
    "point", "cup_mouth", "palms_down", "jump", "roar", "still",
)


def person(x, y, s=1.0, skin="#e0ac69", hair="#3d2314", shirt="#ef476f",
           hairstyle="short", pose="still", flip=False, pants="#3a5a8c",
           face="happy"):
    """A child. (x, y) is the point between the feet. s scales everything.

    Built at a nominal 200px tall and scaled, so poses stay consistent.
    """
    o = []
    HB = 96          # head bottom / shoulder line, in local units above feet
    hy = -HB - 34    # head centre y
    hr = 34

    # ---- legs
    if pose == "stomp":
        o.append(limb(-16, -46, -26, -2, skin, 16))                      # planted
        o.append(bent_limb(16, -46, 46, -34, 34, -6, skin, 16))          # driving down
    elif pose == "jump":
        o.append(bent_limb(-16, -46, -44, -20, -34, -30, skin, 16))      # tucked
        o.append(bent_limb(16, -46, 44, -20, 34, -30, skin, 16))
    elif pose == "tiptoe":
        o.append(limb(-14, -46, -18, -4, skin, 15))
        o.append(limb(14, -46, 18, -4, skin, 15))
    elif pose == "sit":
        # cross-legged: two shallow arcs meeting in the middle at floor level
        o.append(path("M-14 -44 Q-52 -18 -6 -8 L6 -8 Q52 -18 14 -44",
                      fill="none", stroke=skin, sw=17, cap="round"))
        o.append(path("M-30 -12 Q0 -22 30 -12", fill="none", stroke=skin, sw=15, cap="round"))
    elif pose == "float":
        o.append(bent_limb(-14, -46, -40, -22, -20, 2, skin, 15))
        o.append(bent_limb(14, -46, 44, -26, 26, -2, skin, 15))
    elif pose == "curl_low":
        o.append(bent_limb(-14, -34, -34, -12, -10, -2, skin, 16))
        o.append(bent_limb(14, -34, 34, -12, 10, -2, skin, 16))
    else:
        o.append(limb(-15, -46, -17, -2, skin, 15))
        o.append(limb(15, -46, 17, -2, skin, 15))

    # ---- shoes
    if pose not in ("sit", "jump"):
        o.append(ellipse(-19, 0, 15, 9, "#2f3e4d", sw=4))
        o.append(ellipse(19, 0, 15, 9, "#2f3e4d", sw=4))

    # ---- body
    body_top = -HB
    if pose == "curl_low":
        body_top = -HB + 30
        hy = -HB - 4
    o.append(path(
        f"M-30 {body_top} Q0 {body_top - 10} 30 {body_top} L26 -44 Q0 -34 -26 -44 Z",
        fill=shirt, sw=SW))

    # ---- arms (shoulder anchors)
    sl, sr = (-30, body_top + 14), (30, body_top + 14)
    if pose == "hand_on_chest":
        cy = body_top + 30
        o.append(bent_limb(sl[0], sl[1], -50, cy + 16, -13, cy, skin))
        o.append(bent_limb(sr[0], sr[1], 50, cy + 16, 13, cy + 8, skin))
        o.append(ellipse(-13, cy, 13, 11, skin, sw=4))
        o.append(ellipse(13, cy + 8, 13, 11, skin, sw=4))
    elif pose == "clap":
        o.append(bent_limb(sl[0], sl[1], -48, body_top + 34, -11, body_top + 26, skin))
        o.append(bent_limb(sr[0], sr[1], 48, body_top + 34, 11, body_top + 26, skin))
        o.append(circle(-11, body_top + 26, 13, skin, sw=4))
        o.append(circle(11, body_top + 26, 13, skin, sw=4))
    elif pose == "clap_big":
        o.append(limb(sl[0], sl[1], -74, body_top - 12, skin))
        o.append(limb(sr[0], sr[1], 74, body_top - 12, skin))
        o.append(circle(-74, body_top - 12, 14, skin, sw=4))
        o.append(circle(74, body_top - 12, 14, skin, sw=4))
    elif pose in ("arms_up", "reach_high", "jump"):
        o.append(limb(sl[0], sl[1], -46, body_top - 62, skin))
        o.append(limb(sr[0], sr[1], 46, body_top - 62, skin))
        o.append(circle(-46, body_top - 62, 12, skin, sw=4))
        o.append(circle(46, body_top - 62, 12, skin, sw=4))
    elif pose == "float":
        o.append(bent_limb(sl[0], sl[1], -70, body_top + 4, -62, body_top - 34, skin))
        o.append(bent_limb(sr[0], sr[1], 70, body_top + 4, 62, body_top - 34, skin))
        o.append(circle(-62, body_top - 34, 12, skin, sw=4))
        o.append(circle(62, body_top - 34, 12, skin, sw=4))
    elif pose == "cup_ears":
        o.append(bent_limb(sl[0], sl[1], -70, body_top - 6, -48, hy + 12, skin))
        o.append(bent_limb(sr[0], sr[1], 70, body_top - 6, 48, hy + 12, skin))
        o.append(path(f"M-40 {hy - 20} A26 26 0 0 0 -40 {hy + 22}", stroke=skin, sw=13))
        o.append(path(f"M40 {hy - 20} A26 26 0 0 1 40 {hy + 22}", stroke=skin, sw=13))
    elif pose == "cup_mouth":
        o.append(bent_limb(sl[0], sl[1], -58, body_top + 4, -26, hy + 20, skin))
        o.append(bent_limb(sr[0], sr[1], 58, body_top + 4, 26, hy + 20, skin))
        o.append(path(f"M-26 {hy + 2} A22 22 0 0 0 -26 {hy + 38}", stroke=skin, sw=13))
        o.append(path(f"M26 {hy + 2} A22 22 0 0 1 26 {hy + 38}", stroke=skin, sw=13))
    elif pose == "wave_arm":
        o.append(limb(sl[0], sl[1], -52, body_top + 40, skin))
        o.append(limb(sr[0], sr[1], 58, body_top - 52, skin))
        o.append(circle(58, body_top - 52, 13, skin, sw=4))
    elif pose == "palms_down":
        o.append(bent_limb(sl[0], sl[1], -54, body_top + 50, -38, -10, skin))
        o.append(bent_limb(sr[0], sr[1], 54, body_top + 50, 38, -10, skin))
        o.append(ellipse(-40, -6, 16, 9, skin, sw=4))
        o.append(ellipse(40, -6, 16, 9, skin, sw=4))
    elif pose == "point":
        o.append(limb(sl[0], sl[1], -48, body_top + 44, skin))
        o.append(limb(sr[0], sr[1], 66, body_top - 30, skin))
        o.append(circle(66, body_top - 30, 12, skin, sw=4))
        o.append(path(f"M66 {body_top - 30} L84 {body_top - 42}", stroke=skin, sw=7))
    elif pose == "roar":
        o.append(bent_limb(sl[0], sl[1], -66, body_top - 20, -44, body_top - 46, skin))
        o.append(bent_limb(sr[0], sr[1], 66, body_top - 20, 44, body_top - 46, skin))
    elif pose == "stomp":
        o.append(limb(sl[0], sl[1], -54, body_top + 34, skin))
        o.append(limb(sr[0], sr[1], 56, body_top - 20, skin))
    elif pose == "tiptoe":
        o.append(bent_limb(sl[0], sl[1], -50, body_top + 10, -34, body_top - 30, skin))
        o.append(bent_limb(sr[0], sr[1], 50, body_top + 10, 34, body_top - 30, skin))
    elif pose == "curl_low":
        o.append(bent_limb(sl[0], sl[1], -46, body_top + 30, -18, body_top + 34, skin))
        o.append(bent_limb(sr[0], sr[1], 46, body_top + 30, 18, body_top + 34, skin))
    else:
        o.append(limb(sl[0], sl[1], -46, body_top + 46, skin))
        o.append(limb(sr[0], sr[1], 46, body_top + 46, skin))

    # ---- head
    o.append(circle(0, hy, hr, skin))
    o.append(_hair(hairstyle, hy, hr, hair))
    o.append(_face(hy, face, pose))

    tr = f"translate({x} {y}) scale({-s if flip else s} {s})"
    return f'<g transform="{tr}">' + "".join(o) + "</g>"


def _hair(style, hy, hr, hair):
    if style == "puff":
        return (circle(-24, hy - 22, 17, hair, sw=4) + circle(0, hy - 32, 19, hair, sw=4)
                + circle(24, hy - 22, 17, hair, sw=4))
    if style == "braids":
        return (path(f"M-{hr} {hy - 6} a{hr} {hr} 0 0 1 {hr * 2} 0", fill=hair, sw=4)
                + circle(-38, hy + 16, 11, hair, sw=4) + circle(38, hy + 16, 11, hair, sw=4))
    if style == "bob":
        return (path(f"M-{hr + 4} {hy + 8} L-{hr + 4} {hy - 8} a{hr + 4} {hr + 4} 0 0 1 {(hr + 4) * 2} 0 "
                     f"L{hr + 4} {hy + 8} L{hr - 4} {hy + 8} L{hr - 4} {hy - 6} L-{hr - 4} {hy - 6} "
                     f"L-{hr - 4} {hy + 8} Z", fill=hair, sw=4))
    if style == "curls":
        return "".join(circle(-26 + i * 17, hy - 26 + (4 if i % 2 else -4), 13, hair, sw=4)
                       for i in range(4))
    return path(f"M-{hr} {hy - 4} a{hr} {hr} 0 0 1 {hr * 2} 0 L{hr - 6} {hy - 14} "
                f"L0 {hy - 8} L-{hr - 6} {hy - 16} Z", fill=hair, sw=4)


def _face(hy, face, pose):
    o = []
    closed = pose in ("hand_on_chest", "still") and face == "calm"
    if closed:
        o.append(path(f"M-16 {hy - 2} q7 7 14 0", sw=4))
        o.append(path(f"M2 {hy - 2} q7 7 14 0", sw=4))
    else:
        o.append(circle(-11, hy - 4, 5, STROKE, stroke=None))
        o.append(circle(11, hy - 4, 5, STROKE, stroke=None))
    if pose in ("roar", "jump", "clap_big"):
        o.append(ellipse(0, hy + 16, 12, 14, "#7a2c3a", sw=4))
    elif face == "o":
        o.append(ellipse(0, hy + 15, 8, 10, "#7a2c3a", sw=4))
    else:
        o.append(path(f"M-13 {hy + 12} q13 13 26 0", sw=4))
    return "".join(o)


def domkam(x, y, s=1.0, pose="still", flip=False):
    """Tall, warm, round-shouldered. Teal jacket, mustard scarf. He grins."""
    p = person(x, y, s, skin="#7a4a24", hair="#241608", shirt="#0f6d80",
               hairstyle="short", pose=pose, flip=flip)
    scarf = (f'<g transform="translate({x} {y}) scale({-s if flip else s} {s})">'
             + path("M-32 -96 Q0 -84 32 -96 Q34 -78 24 -74 Q0 -64 -24 -74 Q-34 -78 -32 -96 Z",
                    fill="#ffd166", sw=4)
             + path("M20 -74 Q30 -60 27 -46", stroke="#ffd166", sw=12)
             + "</g>")
    return p + scarf


def johnson(x, y, s=1.0, pose="still", flip=False):
    """Compact, energetic, glasses. Rust vest, teal sneakers. He counts."""
    p = person(x, y, s * 0.92, skin="#c98b52", hair="#2b1b12", shirt="#d4562a",
               hairstyle="short", pose=pose, flip=flip)
    sc = s * 0.92
    glasses = (f'<g transform="translate({x} {y}) scale({-sc if flip else sc} {sc})">'
               + circle(-12, -134, 15, "none", sw=4) + circle(12, -134, 15, "none", sw=4)
               + path("M-27 -134 L-34 -136 M3 -134 L-3 -134 M27 -134 L34 -136", sw=4)
               + "</g>")
    vest = (f'<g transform="translate({x} {y}) scale({-sc if flip else sc} {sc})">'
            + path("M-22 -94 L-14 -46 M22 -94 L14 -46", stroke="#fff", sw=6, op=.75)
            + "</g>")
    return p + vest + glasses


# ----------------------------------------------------------------- ship
def ship(x, y, s=1.0, glow=0, lamps=0, porthole="#7fd4d8", tilt=0):
    """The Wonder Ship. Round and friendly, NOT a rocket.

    glow  0-3   brightness of the ring of breath-lights
    lamps 0-4   how many clap-meter lamps are lit
    """
    o = []
    hull = "#c98a4b"
    o.append(path("M-150 -20 Q-150 90 0 96 Q150 90 150 -20 Q150 -60 120 -66 "
                  "L-120 -66 Q-150 -60 -150 -20 Z", fill=hull, sw=6))
    o.append(path("M-150 -20 Q-150 90 0 96 Q150 90 150 -20", fill="none",
                  stroke="#9c6631", sw=4))
    o.append(rect(-158, -80, 316, 22, "#0f6d80", r=11, sw=6))          # rail
    o.append(circle(0, 4, 68, "#eaf6f7", sw=7))                         # porthole
    o.append(circle(0, 4, 56, porthole, stroke=None))
    o.append(path("M-34 -26 a56 56 0 0 1 34 -14", stroke="#ffffff", sw=8, op=.7))

    # breath-lights: a ring of soft dots following the hull rim
    import math
    op = [0.20, 0.5, 0.8, 1.0][max(0, min(3, glow))]
    for i in range(11):
        t = i / 10.0
        ang = math.radians(180 * t)                    # sweep left rim to right rim
        rx = -134 * math.cos(ang)
        ry = -6 + 92 * math.sin(ang)
        o.append(circle(round(rx, 1), round(ry, 1), 9, "#ffd166", stroke=STROKE, sw=3)
                 .replace("/>", f' opacity="{op}"/>'))
        if glow >= 2:
            o.append(circle(round(rx, 1), round(ry, 1), 17, "#ffd166", stroke=None)
                     .replace("/>", f' opacity="{0.16 * glow}"/>'))

    # clap-meter: four lamps on the rail
    for i in range(4):
        lit = i < lamps
        o.append(circle(-72 + i * 48, -69, 11,
                        "#ff7a59" if lit else "#0b3a4a", sw=4))

    # fins
    o.append(path("M-146 6 Q-214 26 -196 92 Q-168 64 -138 52 Z", fill="#d4562a", sw=6))
    o.append(path("M146 6 Q214 26 196 92 Q168 64 138 52 Z", fill="#d4562a", sw=6))
    return f'<g transform="translate({x} {y}) scale({s}) rotate({tilt})">' + "".join(o) + "</g>"


def ship_small(x, y, s=1.0):
    return ship(x, y, s, glow=1, lamps=0)


# ------------------------------------------------------------ sound art
def sound_rings(x, y, n=3, spacing=26, color="#ffd166", sw=7, start=30, op=.9, arc=110):
    """Arcs radiating from a point. Tight spacing = high frequency,
    wide spacing = low. Used constantly across all three books."""
    import math
    o = []
    for i in range(n):
        r = start + i * spacing
        a = math.radians(arc / 2)
        x1, y1 = x + r * math.cos(-a), y + r * math.sin(-a)
        x2, y2 = x + r * math.cos(a), y + r * math.sin(a)
        o.append(path(f"M{x1:.1f} {y1:.1f} A{r} {r} 0 0 1 {x2:.1f} {y2:.1f}",
                      stroke=color, sw=sw, op=op - i * 0.16))
    return "".join(o)


def star(x, y, r, fill="#ffd166", points=5, sw=4):
    import math
    pts = []
    for i in range(points * 2):
        rr = r if i % 2 == 0 else r * 0.44
        a = math.radians(i * 180 / points - 90)
        pts.append(f"{x + rr * math.cos(a):.1f},{y + rr * math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="{STROKE}" stroke-width="{sw}" stroke-linejoin="round"/>'


def sparkle(x, y, r, fill="#fff", op=.9):
    return path(f"M{x} {y - r} Q{x} {y} {x + r} {y} Q{x} {y} {x} {y + r} "
                f"Q{x} {y} {x - r} {y} Q{x} {y} {x} {y - r} Z",
                fill=fill, stroke=None, op=op)


def bubble(x, y, r):
    return (circle(x, y, r, "#ffffff", stroke="#cfeef2", sw=3).replace("/>", ' opacity="0.55"/>')
            + circle(x - r * .3, y - r * .3, max(2, r * .22), "#ffffff", stroke=None))
