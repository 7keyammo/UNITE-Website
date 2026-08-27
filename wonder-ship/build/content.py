# -*- coding: utf-8 -*-
"""One normalized page model, consumed by every output format.

print HTML -> render.py     app -> app.py
EPUB       -> epub.py       Canva deck -> deck.py

Keeping this in one place is what stops the four exports drifting apart.
"""
import re

from books import BOOKS

NOTE_TEXT = [
    "This book only works if you <b>move</b>.",
    "Every page has a <b>PAUSE</b>. Stop reading. Do the thing. Then keep going.",
    "The breathing on pages 3 and 4 is the same in every Wonder Ship book. That is on "
    "purpose — it becomes a tool your children can use when the book is closed.",
    "You need nothing. No materials. Just bodies, voices, and breath.",
]

CLAP = [("1", "CLAP", "your hands"), ("2", "CLAP", "your hands"),
        ("3", "PAT", "your knees"), ("4", "WHOOSH", "breathe out")]

# Pages that get the animated breathing guide in the app.
BREATH_PAGES = {3, 4, 21}
# Pages that get the tappable 4-beat clap in the app.
CLAP_PAGES = {5, 6, 22, 24}


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s).replace("&amp;", "&").replace("&nbsp;", " ")


def speech_text(lines):
    """Flatten story lines into something a speech synthesiser reads naturally."""
    out = []
    for ln in lines:
        if not ln:
            continue
        t = strip_tags(ln.replace("<br>", " ")).strip()
        if not t or set(t) <= {".", " "}:
            continue
        if not t.endswith((".", "!", "?", ",", "…")):
            t += "."
        out.append(t)
    return " ".join(out)


def pages(book):
    """Return 24 normalized page dicts for one book."""
    out = [
        dict(n=1, kind="title", beat="Title", title=book["title"],
             series="The Wonder Ship",
             pilots="Piloted by Mr. Domkam & Mr. Johnson",
             text=[], pause="", grown="", speech=f"The Wonder Ship. {book['title']}."),
        dict(n=2, kind="note", beat="Front matter", heading="How to Fly This Book",
             kicker="Grown-ups, read this part first",
             text=NOTE_TEXT, pause="", grown="",
             speech="How to fly this book. This book only works if you move."),
    ]
    for i, pg in enumerate(book["pages"]):
        n = i + 3
        if pg["kind"] == "theme":
            out.append(dict(n=n, kind="theme", beat="Series theme",
                            heading="The Wonder Ship Clap",
                            sub="You can fly any time.", clap=CLAP,
                            dial=["Slow to rest.", "Fast to fly."],
                            motto="Mentality Over Excuses — no materials, no excuses, all music.",
                            text=[], pause="", grown="",
                            speech="The Wonder Ship Clap. Clap. Clap. Pat. Whoosh. "
                                   "Slow to rest. Fast to fly."))
            continue
        out.append(dict(n=n, kind="story", beat=pg["beat"], text=pg["text"],
                        pause=pg["pause"], grown=pg["grown"], art=pg["art"],
                        speech=speech_text(pg["text"])))
    for p in out:
        p["breath"] = p["n"] in BREATH_PAGES
        p["clapper"] = p["n"] in CLAP_PAGES
    assert len(out) == 24, f"{book['slug']} produced {len(out)} pages"
    return out


def all_books():
    return [dict(b, model=pages(b)) for b in BOOKS]
