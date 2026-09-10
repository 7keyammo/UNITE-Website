# -*- coding: utf-8 -*-
"""The 50 destinations, as visual specs.

One entry per book. The engine turns each of these into all 13 of a book's
world-specific pages, so adding a destination is a dozen lines, not a dozen
drawings.
"""
from scenes import World
import fauna as F

# handy shorthands for the cast lists
def sw(c, f=None, **k):  return (F.swimmer, dict(body=c, fin=f, **k))
def fl(c, w=None, **k):  return (F.flier,   dict(body=c, wing=w, **k))
def bg_(c, **k):         return (F.bug,     dict(body=c, **k))
def be(c, **k):          return (F.beast,   dict(body=c, **k))
def cr(c, **k):          return (F.critter, dict(body=c, **k))
def tr(**k):             return (F.tree,    dict(**k))
def fr(**k):             return (F.frond,   dict(**k))
def cl(**k):             return (F.cloud,   dict(**k))


def _w(key, kind, deep, mid, light, accent, sand, sky, ground, **kw):
    return World(key, deep, mid, light, accent, sand, sky, ground, kind=kind, **kw)


WORLDS = {}


def add(key, **kw):
    WORLDS[key] = _w(key, **kw)
    return WORLDS[key]


# ---------------------------------------------------------------- water
add("reef", kind="water", deep="#0b3a4a", mid="#0d5570", light="#7fd4d8",
    accent="#ff7a59", sand="#f3e2c0", sky="#bfeaf0", ground="#e9d3a3",
    quiet="#07293a", horizon=420,
    flora=[fr(h=200, color="#2e9e6b"), fr(h=240, color="#3fae7b", flip=True)],
    cast=[sw("#ffd166", "#ff7a59"), sw("#7fd4d8", "#2e9e6b"), sw("#e86a92", "#ffd166")])

add("openocean", kind="water", deep="#062535", mid="#0a4a63", light="#6fc4d8",
    accent="#ffd166", sand="#e8dcc0", sky="#a9dfe8", ground="#dccfa8",
    quiet="#04141f", horizon=470,
    cast=[sw("#4d8fae", "#4d8fae", tall=.5, tail=1.6), sw("#5fa3c2", tall=.55, tail=1.4)])

add("kelp", kind="water", deep="#0a3320", mid="#12613f", light="#8fd6a8",
    accent="#ffd166", sand="#e6dcbb", sky="#c7ecd6", ground="#d8cca4",
    quiet="#061e13", horizon=430,
    flora=[fr(h=300, color="#1f7a4d"), fr(h=260, color="#2b9160", flip=True)],
    cast=[sw("#ffb703", "#fb8500"), cr("#f4a261", ears=0, tail=1.2)])

add("icewater", kind="water", deep="#0d2b45", mid="#1b5378", light="#a9dcf0",
    accent="#ff7a59", sand="#eaf4fb", sky="#dceefc", ground="#cfe6f5",
    quiet="#08192a", horizon=450,
    cast=[sw("#dff0fa", "#9fc9e0", tall=.55), cr("#eaf4fb", ears=0, tail=.8)])

add("river", kind="water", deep="#0e3b3f", mid="#146b6e", light="#8ed9d2",
    accent="#ffb703", sand="#e6d9b0", sky="#cdeeea", ground="#d6c79c",
    quiet="#082628", horizon=440,
    flora=[fr(h=180, color="#3f8f5e")],
    cast=[sw("#8ecae6", "#219ebc"), cr("#90be6d", ears=0, tail=.4)])

# ---------------------------------------------------------------- land
add("prehistoric", kind="land", deep="#1f3d1e", mid="#4a7c3f", light="#b9d99a",
    accent="#d98555", sand="#f4ead3", sky="#cfe8b8", ground="#7ba05b",
    terrain="peaks", horizon=470,
    flora=[fr(h=220), fr(h=240, flip=True)],
    cast=[be("#4a9c6d", neck=1.0, tail=1.0), be("#e0a44a", neck=.2, tail=.6),
          be("#b388eb", neck=.6, tail=.8)])

add("rainforest", kind="land", deep="#123a1f", mid="#2f7a3f", light="#a7d98a",
    accent="#ff7a59", sand="#efe4c4", sky="#d8efc4", ground="#4e8c46",
    horizon=460,
    flora=[tr(kind="palm", leaf="#2f7a3f", h=240), fr(h=200, color="#1f6b33")],
    cast=[fl("#e86a92", "#b388eb"), cr("#f4a261"), bg_("#ffd166")],
    air=[fl("#4cc9f0", "#7fd4d8"), fl("#ffd166", "#ff7a59")])

add("meadow", kind="land", deep="#2b4a1c", mid="#5f9a3c", light="#cfe8a0",
    accent="#ff7a59", sand="#f6efd2", sky="#dff0c8", ground="#8fbc5a",
    terrain="hills", horizon=440,
    flora=[tr(kind="round", leaf="#4a8c34", h=180)],
    cast=[bg_("#ffd166"), cr("#e0a44a"), fl("#ffffff", "#ffd166")],
    air=[cl()])

add("desert", kind="land", deep="#4a2c14", mid="#b07a3c", light="#f0d9a8",
    accent="#e05a3c", sand="#f7ecd2", sky="#ffdfa8", ground="#e0b878",
    terrain="dunes", horizon=450,
    cast=[cr("#c98a4b", ears=2, tail=.3), be("#c98a4b", neck=.3, tail=.3, humps=2)])

add("arctic", kind="land", deep="#0d2740", mid="#2f6790", light="#9fcbe6",
    accent="#ff7a59", sand="#eaf6ff", sky="#6fa8cc", ground="#cfe4f2",
    terrain="peaks", horizon=460,
    cast=[cr("#f7fbff", ears=2, tail=.3), be("#eaf4fb", neck=.2, tail=.4),
          fl("#2f6790", "#9fcbe6")])

add("savanna", kind="land", deep="#4a3a12", mid="#a8862c", light="#f0dc9a",
    accent="#e0603c", sand="#f7eed0", sky="#ffe9b0", ground="#d8b45c",
    terrain="flat", horizon=450,
    flora=[tr(kind="palm", leaf="#7a8c34", trunk="#8b5a2b", h=200)],
    cast=[be("#e0a44a", neck=1.0, tail=.6, ears=2), be("#c98a4b", neck=.2, horns=2, ears=2)])

add("mountain", kind="land", deep="#2b2f4a", mid="#5f6a94", light="#c9d2ec",
    accent="#ffd166", sand="#f2f0fa", sky="#dfe6f7", ground="#8b94b8",
    terrain="peaks", horizon=440,
    flora=[tr(kind="pine", leaf="#2e5426", h=200)],
    cast=[fl("#8b94b8", "#c9d2ec"), cr("#a86b3c", ears=2)])

add("forest", kind="land", deep="#1c3a22", mid="#3f7a44", light="#b8dfa8",
    accent="#e08a3c", sand="#f2ead0", sky="#dceec8", ground="#5f9a4c",
    horizon=450,
    flora=[tr(kind="pine", leaf="#2e5426", h=230), tr(kind="round", leaf="#3f7a44", h=190)],
    cast=[cr("#a86b3c", ears=2), fl("#e86a92", "#ffd166"), be("#8b5a2b", neck=.3, ears=2)])

add("bamboo", kind="land", deep="#1f3a24", mid="#4f8a44", light="#cfe8a8",
    accent="#ffb703", sand="#f4eed4", sky="#e2f2cc", ground="#6faa54",
    horizon=450,
    flora=[fr(h=320, color="#4f8a44"), fr(h=280, color="#6faa54", flip=True)],
    cast=[cr("#2b2b2b", ears=2, tail=.2), fl("#7fd4d8", "#cfe8a8")])

add("volcano", kind="land", deep="#3a1414", mid="#8c3a24", light="#f0a878",
    accent="#ffd166", sand="#f2ddc4", sky="#ffc49a", ground="#4a2018",
    terrain="peaks", horizon=470,
    cast=[be("#d97a4c", neck=.4, tail=.8), cr("#f0a878")])

add("cave", kind="interior", deep="#120e1c", mid="#4a3d63", light="#b9a9dc",
    accent="#ffd166", sand="#6b5a8a", sky="#4a3d63", ground="#584a75",
    terrain="peaks", horizon=470, quiet="#0d0a14",
    cast=[fl("#d4c4f0", "#a08cc8"), cr("#c4b4e0", ears=2)])

add("mine", kind="interior", deep="#241a12", mid="#5a4230", light="#c4a583",
    accent="#ffd166", sand="#3a2b1f", sky="#5a4230", ground="#3a2b1f",
    terrain="flat", horizon=470, quiet="#140e09",
    cast=[cr("#c4a583", ears=2), fl("#3a2b1f", "#8b6a48")])

add("saltflat", kind="land", deep="#4a4a52", mid="#9a9aa8", light="#f0f0f5",
    accent="#ff7a59", sand="#fafaff", sky="#e8e8f2", ground="#e0e0ea",
    terrain="flat", horizon=460,
    cast=[fl("#8a8a9c", "#c8c8d8"), cr("#b0b0c0", ears=2)])

add("canyon", kind="land", deep="#4a2418", mid="#a85a34", light="#f0c49a",
    accent="#ffd166", sand="#f7e6cc", sky="#ffd9b0", ground="#c8804c",
    terrain="peaks", horizon=440,
    cast=[fl("#a85a34", "#f0c49a"), cr("#c98a4b", ears=2)])

add("farm", kind="land", deep="#3a3212", mid="#8a7a2c", light="#e8dc9a",
    accent="#e05a3c", sand="#f7f0d2", sky="#ffefb8", ground="#b8a44c",
    terrain="flat", horizon=450,
    flora=[tr(kind="round", leaf="#6a8c34", h=170)],
    cast=[be("#f4f0e0", neck=.2, ears=2), cr("#e0a44a"), fl("#ffffff", "#ffd166")])

add("town", kind="land", deep="#2b3448", mid="#5a6a8c", light="#c4d0e8",
    accent="#ff7a59", sand="#f2f2f8", sky="#dfe8f7", ground="#8a94ac",
    terrain="flat", horizon=460,
    flora=[(F.building, dict(w=110, h=210, color="#c98a4b")),
           (F.building, dict(w=130, h=170, color="#8fb0c9"))],
    cast=[fl("#5a6a8c", "#c4d0e8"), cr("#8b5a2b", ears=2)])

# ---------------------------------------------------------------- sky
add("storm", kind="sky", deep="#1f2438", mid="#4a5470", light="#b0bcd8",
    accent="#ffd166", sand="#e8ecf5", sky="#5a6480", ground="#3f4860",
    terrain="hills", horizon=470, quiet="#141826",
    air=[cl(color="#8a94ac"), cl(color="#a0a8bc")],
    cast=[fl("#4a5470", "#b0bcd8")])

add("windy", kind="sky", deep="#2b4458", mid="#5f8ca8", light="#cfe6f0",
    accent="#ffb703", sand="#f0f6fa", sky="#d8ecf5", ground="#8fb8a0",
    terrain="hills", horizon=450,
    air=[cl()], flora=[tr(kind="bare", h=190)],
    cast=[fl("#ffffff", "#cfe6f0")])

add("aurora", kind="sky", deep="#0d1f2b", mid="#1f5a5f", light="#8fe8c4",
    accent="#b388eb", sand="#dff5ec", sky="#123844", ground="#e8f4f8",
    terrain="peaks", horizon=470, quiet="#06121a",
    cast=[fl("#8fe8c4", "#b388eb")])

# ---------------------------------------------------------------- space
add("space", kind="space", deep="#171a4a", mid="#3b3a8c", light="#a9a6f2",
    accent="#ffd166", sand="#f5f0ff", sky="#2a2a6e", ground="#3b3a8c",
    quiet="#05061a")

add("moon", kind="space", deep="#12142e", mid="#3a3a5c", light="#c4c4dc",
    accent="#ffd166", sand="#e8e8f2", sky="#1f2140", ground="#6b6ba8",
    terrain="hills", horizon=520, quiet="#08091c")

add("station", kind="interior", deep="#101a2b", mid="#26405f", light="#8fc4e8",
    accent="#ff7a59", sand="#dceefc", sky="#26405f", ground="#1a2b40",
    terrain="flat", horizon=470, quiet="#080f1a")

add("ringed", kind="space", deep="#2b1a3a", mid="#5f3a7a", light="#d4a8f0",
    accent="#ffd166", sand="#f4e8fa", sky="#3a2450", ground="#5f3a7a",
    quiet="#150d1f")

add("comet", kind="space", deep="#0d1a2b", mid="#1f4a70", light="#8fd4f0",
    accent="#ffd166", sand="#e0f2fa", sky="#12283f", ground="#1f4a70",
    quiet="#060d16")

# ---------------------------------------------------------------- inside
add("instrument", kind="interior", deep="#3a2412", mid="#8a5a2c", light="#e8c49a",
    accent="#ff7a59", sand="#f7e8d2", sky="#8a5a2c", ground="#5a3a1c",
    terrain="flat", horizon=470, quiet="#1f1209")

add("body", kind="interior", deep="#4a1424", mid="#a83a54", light="#f0a8bc",
    accent="#ffd166", sand="#fae0e8", sky="#a83a54", ground="#6b1f30",
    terrain="hills", horizon=470, quiet="#2b0a14")

add("studio", kind="interior", deep="#1a1a24", mid="#3f3f52", light="#a8a8c4",
    accent="#ff7a59", sand="#e8e8f0", sky="#3f3f52", ground="#2b2b38",
    terrain="flat", horizon=470, quiet="#0d0d14")

add("hall", kind="interior", deep="#2b1a3a", mid="#6b4a8c", light="#d4b8ec",
    accent="#ffd166", sand="#f4ecfa", sky="#6b4a8c", ground="#3f2b52",
    terrain="flat", horizon=470, quiet="#160d1f")
