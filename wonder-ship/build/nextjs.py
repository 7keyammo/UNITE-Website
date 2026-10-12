# -*- coding: utf-8 -*-
"""Generate the UNITE STEAM site's book content module.

The Next.js site at unite-steam/ serves the books to paying members. It takes
its content from one server-only module with a fixed shape:

    export { art, chooseArt, BOOKS, ORDER }

This writes that module from the same 13-book content model everything else
uses, so the paid site, the free reader, the print PDFs and the EPUBs never
drift. The site's own interaction — the "choose" pages where children pick
what happens next — is kept and generated per book from that world's cast.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import art as ART                                     # noqa: E402
import scenes as S                                    # noqa: E402
from content import all_books                         # noqa: E402
from plan import by_week                              # noqa: E402
from worlds import WORLDS                             # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "unite-steam", "lib", "content", "wonder-ship.js")

TAG = re.compile(r"<[^>]+>")


def svg_doc(inner, vb="0 0 1000 640"):
    """The site injects these straight into the page, so each must be a whole
    <svg>, not the inner markup the other outputs wrap themselves."""
    return (f'<svg viewBox="{vb}" xmlns="http://www.w3.org/2000/svg" '
            f'preserveAspectRatio="xMidYMid slice" role="img" aria-hidden="true">'
            f'{inner}</svg>')


def plain(s):
    return TAG.sub("", s).replace("&amp;", "&").replace("&nbsp;", " ").strip()


def line_of(page):
    """Join a page's story lines into one spoken line."""
    parts = [plain(l) for l in page.get("text", []) if l and plain(l)]
    parts = [p for p in parts if set(p) - set(". ")]
    out = " ".join(parts)
    return re.sub(r"\s+", " ", out).strip()


def kicker_of(page):
    b = page.get("beat", "")
    b = re.sub(r"^\d+\s*-\s*", "", b)
    return {"Liftoff Ritual": "Start the ship", "Departure": "Departure",
            "Arrival": "Arrival", "Explore A": "Look closer",
            "Explore B": "Look closer", "MOVEMENT": "Move with us",
            "Wonder Moment": "Wonder moment", "Return Ritual": "Return ritual",
            "Landing": "Landing", "Series theme": "The Wonder Ship Clap",
            "Front matter": "For grown-ups", "Title": "The Wonder Ship"}.get(b, b)


def secs_of(page):
    """Pacing. Movement pages need doing time; the hush pages need holding."""
    beat = page.get("beat", "")
    if "MOVEMENT" in beat:
        return 75
    if "Wonder" in beat:
        return 85
    if "Ritual" in beat:
        return 70
    n = len(line_of(page).split())
    return max(40, min(70, 28 + n * 2))


SLUG = re.compile(r"^book-\d+-")


def short_slug(s):
    return SLUG.sub("", s)


# ----------------------------------------------------------- choose pages
PICK_Q = [
    ("Who should come and say hello first?", "Here it comes — look!"),
    ("What should we say before we fly home?", "Perfect — it heard you!"),
]
FAREWELL = [("ic_star", "“Thank you!”"), ("ic_wave", "“See you soon!”"),
            ("ic_heart", "“Come and visit!”")]


def choose_meet(week, world, cast_n):
    opts = []
    for i in range(min(3, max(1, cast_n))):
        opts.append(dict(icon=f"ic_w{week:02d}_{i}", label=None, go=f"ch_w{week:02d}_{i}"))
    return opts


def build_js():
    books = all_books()
    art_map = {}          # key -> svg string
    out_books = {}
    order = []

    for b in books:
        wk = b["week"]
        row = by_week(wk)
        world_key = row[3]
        w = WORLDS.get(world_key)
        slug = short_slug(b["slug"])
        order.append(slug)

        # --- art for every page of this book
        for p in b["model"]:
            key = f"w{wk:02d}p{p['n']:02d}"
            art_map[key] = svg_doc(ART.bleed(wk, p["n"]) + ART.scene(wk, p["n"]))

        # --- choose-option art, drawn from this world's own cast
        cast_n = len(w.cast) if w and w.cast else 0
        labels = []
        for i in range(min(3, max(1, cast_n))):
            art_map[f"ic_w{wk:02d}_{i}"] = svg_doc(S.c_option_icon(w, i))
            art_map[f"ch_w{wk:02d}_{i}"] = svg_doc(ART.bleed(wk, 10) + S.c_option_scene(w, i))
            labels.append(CAST_LABEL.get((world_key, i), "A new friend"))

        pages = []

        def add_read(p):
            pages.append(dict(type="read", art=f"w{wk:02d}p{p['n']:02d}",
                              kicker=kicker_of(p), line=line_of(p),
                              cue=plain(p.get("pause", "")),
                              note=plain(p.get("grown", "")) or None,
                              secs=secs_of(p)))

        by_n = {p["n"]: p for p in b["model"]}
        for n in range(3, 21):                      # ritual through wonder
            add_read(by_n[n])
            if n == 10 and cast_n:                  # after the world reveal
                q, note = PICK_Q[0]
                pages.append(dict(type="choose", art=f"w{wk:02d}p10", kicker="Your turn",
                                  q=q, note=note, secs=90,
                                  options=[dict(icon=o["icon"], label=labels[i], go=o["go"])
                                           for i, o in enumerate(choose_meet(wk, w, cast_n))]))
        q, note = PICK_Q[1]
        pages.append(dict(type="choose", art=f"w{wk:02d}p20", kicker="Your turn",
                          q=q, note=note, secs=90,
                          options=[dict(icon=i, label=l, go=None) for i, l in FAREWELL]))
        for n in range(21, 25):                     # return, landing, the clap
            add_read(by_n[n])

        out_books[slug] = dict(
            title=b["title"],
            cover=f"w{wk:02d}p10",   # the world reveal makes a far better cover than the classroom
            blurb=(f"Week {wk}. {row[6]}. A guided read-aloud with a movement "
                   f"break on every page, piloted by Mr. Domkam and Mr. Johnson."),
            status="ready",
            week=wk,
            world=b["world"],
            curriculum=row[5],
            pages=pages,
        )

    # the three small farewell icons are world-independent
    for k in ("star", "wave", "heart"):
        art_map["ic_" + k] = svg_doc(_glyph(k))

    return art_map, out_books, order


def _glyph(kind):
    from prims import circle, path, star as star_shape
    base = '<rect width="1000" height="640" rx="40" fill="#0f6d80"/>'
    if kind == "star":
        return base + star_shape(500, 320, 190, "#ffd166")
    if kind == "wave":
        return (base + path("M120 320 q95 -120 190 0 t190 0 t190 0 t190 0",
                            stroke="#ffd166", sw=34))
    return (base + path("M500 480 C300 340 300 170 420 170 C480 170 500 220 500 250 "
                        "C500 220 520 170 580 170 C700 170 700 340 500 480 Z",
                        fill="#ff7a59", sw=14))


CAST_LABEL = {
    ("reef", 0): "A yellow fish", ("reef", 1): "A green fish", ("reef", 2): "A pink fish",
    ("openocean", 0): "A great whale", ("openocean", 1): "A blue whale",
    ("icewater", 0): "A pale seal", ("icewater", 1): "A snow creature",
    ("kelp", 0): "A gold fish", ("kelp", 1): "A kelp crab",
    ("river", 0): "A river fish", ("river", 1): "A green frog",
    ("prehistoric", 0): "The long-neck", ("prehistoric", 1): "The spiky one",
    ("prehistoric", 2): "The purple one",
    ("rainforest", 0): "A bright bird", ("rainforest", 1): "A furry friend",
    ("rainforest", 2): "A buzzing bee",
    ("meadow", 0): "A busy bee", ("meadow", 1): "A little hopper",
    ("meadow", 2): "A white butterfly",
    ("desert", 0): "A desert hopper", ("desert", 1): "A humped walker",
    ("arctic", 0): "A snow hopper", ("arctic", 1): "A white walker",
    ("arctic", 2): "A cold-sky bird",
    ("savanna", 0): "The tall one", ("savanna", 1): "The horned one",
    ("mountain", 0): "A mountain bird", ("mountain", 1): "A rock hopper",
    ("forest", 0): "A forest hopper", ("forest", 1): "A singing bird",
    ("forest", 2): "A big brown one",
    ("bamboo", 0): "A black-and-white one", ("bamboo", 1): "A bamboo bird",
    ("volcano", 0): "A warm giant", ("volcano", 1): "An ember hopper",
    ("cave", 0): "A cave flier", ("cave", 1): "A cave hopper",
    ("mine", 0): "A tunnel hopper", ("mine", 1): "A tunnel flier",
    ("saltflat", 0): "A white bird", ("saltflat", 1): "A salt hopper",
    ("canyon", 0): "A canyon bird", ("canyon", 1): "A canyon hopper",
    ("farm", 0): "A woolly one", ("farm", 1): "A farm hopper", ("farm", 2): "A white hen",
    ("town", 0): "A city bird", ("town", 1): "A city hopper",
    ("storm", 0): "A storm bird",
    ("windy", 0): "A wind bird",
    ("aurora", 0): "A light bird",
}


JS_HEAD = """import 'server-only';
// Wonder Ship book content and art. Server-only: this module never ships to the browser.
//
// GENERATED by wonder-ship/build/nextjs.py — do not edit by hand.
// Change the words in wonder-ship/build/specs.py or the art in
// wonder-ship/build/art.py, then run:  python3 bot.py build
//
// %(nbooks)d books, %(npages)d reader pages, %(nart)d pieces of art.
"""

JS_TAIL = """
  function art(key){ return ART[key] || ''; }
  function chooseArt(go){ return go && ART[go] ? ART[go] : null; }

export { art, chooseArt, BOOKS, ORDER };
"""


def write():
    art_map, books, order = build_js()
    npages = sum(len(b["pages"]) for b in books.values())

    parts = [JS_HEAD % dict(nbooks=len(books), npages=npages, nart=len(art_map))]
    parts.append("  var ART = {\n")
    for k in sorted(art_map):
        parts.append(f"    {k}: {json.dumps(art_map[k])},\n")
    parts.append("  };\n")

    # cover() is a function in the site's contract
    parts.append("  var BOOKS = {\n")
    for slug in order:
        b = books[slug]
        pages = json.dumps(b["pages"], ensure_ascii=False)
        parts.append(
            f"    {json.dumps(slug)}: {{ title: {json.dumps(b['title'])}, "
            f"blurb: {json.dumps(b['blurb'])}, status: {json.dumps(b['status'])}, "
            f"week: {b['week']}, world: {json.dumps(b['world'])}, "
            f"curriculum: {json.dumps(b['curriculum'])}, "
            f"cover: (function(k){{ return function(){{ return art(k); }}; }})"
            f"({json.dumps(b['cover'])}), pages: {pages} }},\n")
    parts.append("  };\n")
    parts.append(f"  var ORDER = {json.dumps(order)};\n")
    parts.append(JS_TAIL)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("".join(parts))
    mb = os.path.getsize(OUT) / 1024 / 1024
    print(f"unite-steam/lib/content/wonder-ship.js — {len(books)} books, "
          f"{npages} reader pages, {len(art_map)} art pieces, {mb:.1f} MB")
    return OUT


if __name__ == "__main__":
    write()
