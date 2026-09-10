# -*- coding: utf-8 -*-
"""Build the offline interactive reader.

Output: app/index.html  — one self-contained file. Every scene, style and
script is inlined, so it runs from a USB stick, an email attachment or
file:// with no network at all. sw.js + manifest.webmanifest add
install-to-homescreen when it happens to be served over http.
"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import art                                            # noqa: E402
from app_css import CSS                               # noqa: E402
from app_js import JS                                 # noqa: E402
from content import all_books                         # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "app")

ICON = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'>%s</svg>")
ICONS = dict(
    home="<path d='M3 11l9-8 9 8'/><path d='M5 10v10h14V10'/>",
    prev="<path d='M15 5l-7 7 7 7'/>",
    next="<path d='M9 5l7 7-7 7'/>",
    read="<path d='M11 5L6 9H3v6h3l5 4V5z'/><path d='M16 9a4 4 0 0 1 0 6'/>",
    clap="<path d='M5 12l3-7 2 1-2 6'/><path d='M9 11l3-7 2 1-2 7'/><path d='M13 12l3-6 2 1-3 8'/>"
         "<path d='M5 12c-1 4 2 8 6 8s6-3 6-6'/>",
    notes="<path d='M4 5h16v14H4z'/><path d='M8 9h8M8 13h6'/>",
    full="<path d='M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5'/>",
)


def svg(book, page, cls="", fill=False):
    """fill=True crops to fill the frame (covers, theme, library cards);
    otherwise the whole scene stays visible and letterboxes."""
    c = f' class="{cls}"' if cls else ""
    par = "xMidYMid slice" if fill else "xMidYMid meet"
    return (f'<svg{c} viewBox="0 0 1000 640" preserveAspectRatio="{par}" '
            f'role="img" aria-hidden="true">{art.bleed(book, page)}{art.scene(book, page)}</svg>')


def story_lines(lines):
    return "".join("<span class='sp'></span>" if not l else l + "<br>" for l in lines)


ARTBG = {1: "#0b3a4a", 2: "#08091f", 3: "#1f3d1e"}


def page_html(book_no, p):
    n = p["n"]
    breath = ('<div class="breath"><i></i><span>breathe</span></div>' if p["breath"] else "")
    clap_attr = ' data-clap="1"' if p["clapper"] else ""
    speech = html.escape(p["speech"], quote=True)

    if p["kind"] == "title":
        return (f'<section class="pg" data-speech="{speech}">'
                f'<div class="full cover"><div class="bg">{svg(book_no, n, fill=True)}</div><div class="scrim"></div>'
                f'<div class="in"><div class="sup">{p["series"]}</div>'
                f'<h1>{html.escape(p["title"])}</h1>'
                f'<div class="pilots">{html.escape(p["pilots"])}</div></div>'
                f'<button class="tap l" aria-label="Previous page"></button>'
                f'<button class="tap r" aria-label="Next page"></button></div></section>')

    if p["kind"] == "note":
        ps = "".join(f"<p>{t}</p>" for t in p["text"])
        return (f'<section class="pg" data-speech="{speech}">'
                f'<div class="full note"><div class="in" style="max-width:60ch">'
                f'<div class="kick">{html.escape(p["kicker"])}</div>'
                f'<h2>{html.escape(p["heading"])}</h2><div class="rule"></div>{ps}</div></div>'
                f'<div style="position:relative;height:0">'
                f'<button class="tap l" aria-label="Previous page"></button>'
                f'<button class="tap r" aria-label="Next page"></button></div></section>')

    if p["kind"] == "theme":
        beats = "".join(f'<div class="beat"><div class="n">{n_}</div>'
                        f'<div class="w">{w}</div><div class="d">{d}</div></div>'
                        for n_, w, d in p["clap"])
        return (f'<section class="pg"{clap_attr} data-speech="{speech}">'
                f'<div class="full"><div class="bg">{svg(book_no, n, fill=True)}</div>'
                f'<div class="scrim" style="background:rgba(8,26,34,.62)"></div>'
                f'<div class="in" style="max-width:44ch">'
                f'<h1 style="font-size:clamp(26px,6.4vw,48px)">{html.escape(p["heading"])}</h1>'
                f'<div class="pilots">{html.escape(p["sub"])}</div>'
                f'<div class="beats">{beats}</div>'
                f'<div style="font-weight:800;font-size:clamp(15px,3.6vw,22px);color:#eaf6f7">'
                f'{"<br>".join(p["dial"])}</div>'
                f'<div class="motto">{html.escape(p["motto"])}</div></div>'
                f'<button class="tap l" aria-label="Previous page"></button>'
                f'<button class="tap r" aria-label="Next page"></button></div></section>')

    return (f'<section class="pg story-page"{clap_attr} data-speech="{speech}">'
            f'<div class="art" style="background:{art.bg_color(book_no, n)}">{svg(book_no, n)}{breath}'
            f'<button class="tap l" aria-label="Previous page"></button>'
            f'<button class="tap r" aria-label="Next page"></button></div>'
            f'<div class="txt">'
            f'<div class="copy">{story_lines(p["text"])}</div>'
            f'<div class="band"><div class="p"><b>PAUSE:</b> {p["pause"]}</div>'
            f'<div class="g"><b>GROWN-UPS:</b> {p["grown"]}</div></div>'
            f'</div></section>')


def shelf(books):
    """The year, in terms. Written books open; the rest show their week."""
    from plan import PLAN, TERMS
    have = {b["week"]: b for b in books}
    out = []
    for a, z, name, blurb in TERMS:
        out.append(f'<div class="term"><h3>{html.escape(name)}</h3>'
                   f'<span>{html.escape(blurb)}</span></div><div class="shelf">')
        for row in PLAN:
            wk, slug, title, world, concepts, tag, big = row
            if not (a <= wk <= z):
                continue
            b = have.get(wk)
            if b:
                out.append(
                    f'<button class="card" data-week="{wk}" '
                    f'aria-label="Open {html.escape(title)}">'
                    f'<span class="wk">Week {wk}</span>'
                    f'{svg(wk, 1, fill=True)}<div class="meta">'
                    f'<h2>{html.escape(title)}</h2>'
                    f'<div class="world">{html.escape(b["world"])} · 24 pages</div>'
                    f'<div class="curric">{html.escape(tag)}</div>'
                    f'<span class="go">Fly this one</span></div></button>')
            else:
                out.append(
                    f'<button class="card soon" data-week="{wk}" '
                    f'aria-label="{html.escape(title)}, arriving week {wk}">'
                    f'<span class="wk">Week {wk}</span>'
                    f'<div style="aspect-ratio:1000/640;position:relative;'
                    f'background:linear-gradient(150deg,#123,#245)">'
                    f'<div class="lock"><b>Arrives week {wk}</b></div></div>'
                    f'<div class="meta"><h2>{html.escape(title)}</h2>'
                    f'<div class="world">{html.escape(big)}</div>'
                    f'<div class="curric">{html.escape(tag)}</div>'
                    f'<span class="go">Scheduled</span></div></button>')
        out.append("</div>")
    return "".join(out)


def build():
    books = all_books()
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(os.path.join(OUT, "books"), exist_ok=True)

    # each book is its own chunk, loaded on demand and cached offline
    for b in books:
        inner = "".join(page_html(b["week"], p) for p in b["model"])
        js = ("window.__ws_book(" + str(b["week"]) + ","
              + json.dumps(inner) + ");\n")
        with open(os.path.join(OUT, "books", f'{b["week"]:02d}.js'), "w",
                  encoding="utf-8") as f:
            f.write(js)

    cards = shelf(books)
    wraps = ""
    pct = round(len(books) / 50 * 100)
    ready = len(books)

    def btn(bid, icon, label, extra=""):
        return (f'<button class="btn" id="{bid}" title="{label}" aria-label="{label}"{extra}>'
                f'{ICON % ICONS[icon]}<span class="lbl">{label}</span></button>')

    clapbar = ('<div id="clapbar" class="hide" style="position:absolute;left:0;right:0;bottom:100%;'
               'background:rgba(11,58,74,.96);padding:10px 12px;display:flex;justify-content:center">'
               '<div class="beats" style="margin:0">'
               + "".join(f'<div class="beat"><div class="n">{n}</div><div class="w">{w}</div>'
                         f'<div class="d">{d}</div></div>'
                         for n, w, d in (("1", "CLAP", "hands"), ("2", "CLAP", "hands"),
                                         ("3", "PAT", "knees"), ("4", "WHOOSH", "breathe")))
               + "</div></div>")

    body = f"""
<div id="app">
  <div id="library">
    <div class="lib-head">
      <div class="sup">The Wonder Ship</div>
      <h1>A school year of read-alouds.</h1>
      <p>Fifty weekly adventures for ages 3, built on the STEAM&nbsp;+&nbsp;Music and
         Energy, Frequency &amp; Vibration K–2 curricula. One book a week, a movement
         break on every page, and nothing to buy. Works with no internet.</p>
      <div class="yearbar"><i style="width:{pct}%"></i></div>
      <div class="yearnote">{ready} of 50 books ready · a new one every week</div>
    </div>
    {cards}
    <div class="lib-foot">
      Tap the sides of a page to turn it, or swipe. <b>Read to me</b> speaks the page aloud.
      <b>Clap</b> plays the four-beat Wonder Ship Clap. <b>Notes</b> hides the teacher band
      so children see only the story.
      <br>Mentality Over Excuses — no materials, no excuses, all music.
    </div>
  </div>

  <div id="reader" class="hide">
    <div id="stage">{wraps}</div>
    <div id="bar">
      <div id="prog"><i style="width:0"></i></div>
      {clapbar}
      {btn('bHome','home','Library')}
      {btn('bPrev','prev','Back')}
      {btn('bNext','next','Next')}
      <span class="sp"></span>
      <span id="pgno">1 / 24</span>
      <span class="sp"></span>
      {btn('bRead','read','Read to me')}
      {btn('bClap','clap','Clap')}
      <button class="btn" id="tSlow" title="Slow claps">Slow</button>
      <button class="btn" id="tFast" title="Fast claps">Fast</button>
      {btn('bNotes','notes','Notes')}
      {btn('bFull','full','Full screen')}
    </div>
  </div>
  <div id="toast" style="position:fixed;left:50%;bottom:78px;transform:translateX(-50%);
       background:rgba(11,58,74,.96);color:#fff;padding:10px 18px;border-radius:999px;
       font-weight:700;font-size:14px;opacity:0;transition:opacity .3s;pointer-events:none;
       z-index:40;max-width:88vw;text-align:center"></div>
</div>"""

    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,maximum-scale=5">
<meta name="theme-color" content="#0b3a4a">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="description" content="The Wonder Ship — three read-aloud picture books for ages 3, with movement breaks on every page. Works offline.">
<title>The Wonder Ship</title>
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="data:image/svg+xml,{ICON_HREF}">
<style>{CSS}</style>
</head>
<body>
{body}
<script>{JS}</script>
</body>
</html>"""
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(doc)
    return doc


ICON_HREF = ("%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E"
             "%3Crect width='100' height='100' rx='22' fill='%230b3a4a'/%3E"
             "%3Ccircle cx='50' cy='52' r='24' fill='%237fd4d8' stroke='%23fff' stroke-width='5'/%3E"
             "%3Crect x='18' y='24' width='64' height='9' rx='4' fill='%23ff7a59'/%3E%3C/svg%3E")

if __name__ == "__main__":
    d = build()
    import glob as _g
    n = len(_g.glob(os.path.join(OUT, "books", "*.js")))
    tot = sum(os.path.getsize(f) for f in _g.glob(os.path.join(OUT, "**", "*"), recursive=True) if os.path.isfile(f))
    print(f"app/ — shell {len(d)/1024:.0f} KB + {n} book chunks, {tot/1024/1024:.1f} MB total")
