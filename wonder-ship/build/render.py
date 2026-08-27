# -*- coding: utf-8 -*-
"""Render The Wonder Ship books to print-ready, Canva-importable HTML.

Each page is a top-level <section data-document-role="page"> so Canva's
import-design-from-url turns one section into one artboard.

Trim 8.5 x 8.5 in.  Built at 8.5in = 816px @ 96dpi.
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from books import BOOKS  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "canva")

PAGE = 816          # 8.5in @ 96dpi
BLEED = 12          # 0.125in
SAFE = 48           # 0.5in

STORY_FONT = "'Baloo 2', 'Quicksand', 'Trebuchet MS', 'DejaVu Sans', sans-serif"
UI_FONT = "'Nunito', 'Trebuchet MS', 'DejaVu Sans', sans-serif"


def css(p):
    return f"""
:root {{
  --deep: {p['deep']};
  --mid: {p['mid']};
  --light: {p['light']};
  --accent: {p['accent']};
  --sand: {p['sand']};
  --band: {p['band']};
  --bandtext: {p['bandtext']};
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ background: #4a4a4a; font-family: {UI_FONT}; }}

.page {{
  position: relative;
  width: {PAGE}px;
  height: {PAGE}px;
  margin: 0 auto 28px;
  overflow: hidden;
  background: var(--sand);
  display: flex;
  flex-direction: column;
}}

/* ---------- illustration zone ---------- */
.art {{
  flex: 1 1 auto;
  min-height: 0;
  margin: {SAFE}px {SAFE}px 0;
  border: 3px dashed var(--mid);
  border-radius: 18px;
  background: linear-gradient(160deg, var(--light) 0%, var(--sand) 100%);
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 26px 30px;
  color: var(--deep);
}}
.art .tag {{
  font: 700 12px/1 {UI_FONT};
  letter-spacing: .16em;
  text-transform: uppercase;
  color: var(--mid);
  margin-bottom: 10px;
}}
.art .dir {{ font: 400 15px/1.5 {UI_FONT}; opacity: .85; }}

/* ---------- story text ---------- */
.story {{
  flex: 0 0 auto;
  padding: 22px {SAFE}px 14px;
  font: 700 27px/1.32 {STORY_FONT};
  color: var(--deep);
  text-align: center;
}}
.story .blank {{ display: block; height: .5em; }}
.story .log {{
  display: block;
  margin-top: 12px;
  padding: 12px 18px;
  border: 3px solid var(--accent);
  border-radius: 14px;
  font: 600 20px/1.4 {UI_FONT};
  color: var(--mid);
}}

/* ---------- teacher band ---------- */
.band {{
  flex: 0 0 auto;
  background: var(--band);
  color: var(--bandtext);
  padding: 14px {SAFE}px 16px;
}}
.band .pause {{ font: 700 17px/1.35 {UI_FONT}; }}
.band .pause b {{ color: var(--accent); letter-spacing: .1em; }}
.band .grown {{ font: 400 13px/1.45 {UI_FONT}; opacity: .8; margin-top: 6px; }}
.band .grown b {{ letter-spacing: .1em; opacity: .9; }}

/* ---------- folio ---------- */
.folio {{
  position: absolute;
  bottom: 6px;
  right: 14px;
  font: 700 12px/1 {UI_FONT};
  color: var(--bandtext);
  opacity: .55;
}}
.beat {{
  position: absolute;
  top: 16px;
  left: {SAFE}px;
  font: 700 11px/1 {UI_FONT};
  letter-spacing: .14em;
  text-transform: uppercase;
  color: var(--mid);
  opacity: .65;
}}

/* ---------- title page ---------- */
.page.title {{
  background: var(--deep);
  justify-content: flex-start;
  align-items: center;
  text-align: center;
  padding: {SAFE}px;
}}
.page.title .series {{
  font: 700 26px/1 {UI_FONT};
  letter-spacing: .3em;
  text-transform: uppercase;
  color: var(--light);
  margin-top: 26px;
}}
.page.title h1 {{
  font: 800 74px/1.05 {STORY_FONT};
  color: #fff;
  margin: 14px 0 8px;
}}
.page.title .pilots {{
  font: 600 20px/1.5 {UI_FONT};
  color: var(--light);
  opacity: .9;
}}
.page.title .art {{
  width: 100%;
  margin: 26px 0 0;
  border-color: var(--mid);
  background: rgba(255,255,255,.06);
  color: var(--light);
}}
.page.title .art .dir {{ color: var(--light); }}
.page.title .art .tag {{ color: var(--accent); }}

/* ---------- how-to page ---------- */
.page.note {{ background: var(--sand); padding: {SAFE}px; justify-content: center; }}
.page.note h2 {{
  font: 800 40px/1.15 {STORY_FONT};
  color: var(--deep);
  margin-bottom: 22px;
}}
.page.note p {{ font: 400 21px/1.6 {UI_FONT}; color: var(--deep); margin-bottom: 18px; }}
.page.note p b {{ color: var(--mid); }}
.page.note .rule {{ height: 5px; width: 90px; background: var(--accent); border-radius: 3px; margin-bottom: 26px; }}
.page.note .kicker {{
  font: 700 14px/1 {UI_FONT};
  letter-spacing: .2em;
  text-transform: uppercase;
  color: var(--mid);
  margin-bottom: 14px;
}}

/* ---------- theme page ---------- */
.page.theme {{ background: var(--deep); color: #fff; padding: {SAFE}px; justify-content: center; text-align: center; }}
.page.theme h2 {{ font: 800 48px/1.1 {STORY_FONT}; margin-bottom: 10px; }}
.page.theme .sub {{ font: 400 22px/1.5 {UI_FONT}; color: var(--light); margin-bottom: 34px; }}
.page.theme .beats {{ display: flex; gap: 16px; justify-content: center; margin-bottom: 34px; }}
.page.theme .b {{
  flex: 1 1 0;
  background: rgba(255,255,255,.09);
  border: 3px solid var(--mid);
  border-radius: 18px;
  padding: 20px 8px;
}}
.page.theme .b .n {{ font: 800 30px/1 {STORY_FONT}; color: var(--accent); }}
.page.theme .b .w {{ font: 800 22px/1.2 {STORY_FONT}; margin: 8px 0 4px; }}
.page.theme .b .d {{ font: 400 14px/1.35 {UI_FONT}; color: var(--light); opacity: .85; }}
.page.theme .dial {{ font: 700 24px/1.6 {STORY_FONT}; color: var(--light); }}
.page.theme .motto {{
  margin-top: 32px;
  font: 600 17px/1.5 {UI_FONT};
  color: var(--accent);
  font-style: italic;
}}

@page {{ size: 8.5in 8.5in; margin: 0; }}
@media print {{
  body {{ background: #fff; }}
  .page {{ margin: 0; page-break-after: always; break-after: page; }}
  .page:last-child {{ page-break-after: auto; break-after: auto; }}
}}
"""


def story_html(lines):
    out = []
    for ln in lines:
        out.append("<span class='blank'></span>" if ln == "" else ln + "<br>")
    return "".join(out)


def art_block(text):
    return (f"<div class='art'><div class='tag'>Illustration</div>"
            f"<div class='dir'>{text}</div></div>")


def render(book):
    p = book["palette"]
    parts = [
        "<title>The Wonder Ship — " + html.escape(book["title"]) + "</title>",
        "<style>" + css(p) + "</style>",
    ]

    # -- page 1: title
    parts.append(f"""
<section class="page title" data-document-role="page" data-label="p1 · Title"
         data-speaker-notes="Cover / title page. Trim 8.5x8.5in, 0.125in bleed.">
  <div class="series">The Wonder Ship</div>
  <h1>{html.escape(book['title'])}</h1>
  <div class="pilots">Piloted by Mr. Domkam &amp; Mr. Johnson</div>
  {art_block(book['cover_art'])}
  <div class="folio">1</div>
</section>""")

    # -- page 2: how to fly this book
    parts.append(f"""
<section class="page note" data-document-role="page" data-label="p2 · How to Fly This Book"
         data-speaker-notes="Adult-facing front matter. Read silently before reading aloud.">
  <div class="kicker">Grown-ups, read this part first</div>
  <h2>How to Fly<br>This Book</h2>
  <div class="rule"></div>
  <p>This book only works if you <b>move</b>.</p>
  <p>Every page has a <b>PAUSE</b>. Stop reading. Do the thing. Then keep going.</p>
  <p>The breathing on pages 3 and 4 is the same in every Wonder Ship book. That is on
     purpose — it becomes a tool your children can use when the book is closed.</p>
  <p>You need nothing. No materials. Just bodies, voices, and breath.</p>
  <div class="folio" style="color:var(--mid)">2</div>
</section>""")

    # -- pages 3-24
    for i, pg in enumerate(book["pages"]):
        n = i + 3
        if pg["kind"] == "theme":
            parts.append(f"""
<section class="page theme" data-document-role="page" data-label="p{n} · The Wonder Ship Clap"
         data-speaker-notes="Series theme page. Identical in all three books.">
  <h2>The Wonder Ship Clap</h2>
  <div class="sub">You can fly any time.</div>
  <div class="beats">
    <div class="b"><div class="n">1</div><div class="w">CLAP</div><div class="d">your hands</div></div>
    <div class="b"><div class="n">2</div><div class="w">CLAP</div><div class="d">your hands</div></div>
    <div class="b"><div class="n">3</div><div class="w">PAT</div><div class="d">your knees</div></div>
    <div class="b"><div class="n">4</div><div class="w">WHOOSH</div><div class="d">breathe out</div></div>
  </div>
  <div class="dial">Slow to rest.<br>Fast to fly.</div>
  <div class="motto">Mentality Over Excuses — no materials, no excuses, all music.</div>
  <div class="folio">{n}</div>
</section>""")
            continue

        parts.append(f"""
<section class="page" data-document-role="page" data-label="p{n} · {html.escape(pg['beat'])}"
         data-speaker-notes="{html.escape(pg['beat'])} — PAUSE: {html.escape(pg['pause'])}">
  <div class="beat">{html.escape(pg['beat'])}</div>
  {art_block(pg['art'])}
  <div class="story">{story_html(pg['text'])}</div>
  <div class="band">
    <div class="pause"><b>PAUSE:</b> {pg['pause']}</div>
    <div class="grown"><b>GROWN-UPS:</b> {pg['grown']}</div>
  </div>
  <div class="folio">{n}</div>
</section>""")

    return "\n".join(parts)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for b in BOOKS:
        path = os.path.join(OUT, b["slug"] + ".html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(render(b))
        pages = render(b).count('data-document-role="page"')
        print(f"{b['slug']}.html  —  {pages} pages")
