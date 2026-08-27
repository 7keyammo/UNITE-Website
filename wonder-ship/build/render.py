# -*- coding: utf-8 -*-
"""Render the print interiors: 8.5 x 8.5 in, 24 pages, real illustrations.

Also emits Canva-importable HTML (one <section data-document-role="page">
per book page) so the same file serves both purposes.
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import art                                          # noqa: E402
from content import all_books                       # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "canva")

PAGE = 816          # 8.5 in @ 96 dpi
SAFE = 46           # 0.5 in safe margin (approx)

STORY_FONT = "'Baloo 2','Quicksand','Trebuchet MS','DejaVu Sans',sans-serif"
UI_FONT = "'Nunito','Trebuchet MS','DejaVu Sans',sans-serif"


def css(p):
    return f"""
:root{{--deep:{p['deep']};--mid:{p['mid']};--light:{p['light']};
--accent:{p['accent']};--sand:{p['sand']};}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#4a4a4a;font-family:{UI_FONT}}}
.page{{position:relative;width:{PAGE}px;height:{PAGE}px;margin:0 auto 26px;
  overflow:hidden;background:var(--sand);display:flex;flex-direction:column}}
.art{{position:relative;flex:1 1 auto;min-height:0;overflow:hidden}}
.art svg{{position:absolute;inset:0;width:100%;height:100%;display:block}}
.story{{flex:0 0 auto;padding:18px {SAFE}px 12px;text-align:center;
  font:700 26px/1.3 {STORY_FONT};color:var(--deep);background:#fffaf0}}
.story .sp{{display:block;height:.44em}}
.story .log{{display:block;margin:10px auto 0;max-width:30ch;padding:10px 16px;
  border:3px solid var(--accent);border-radius:14px;font:700 18px/1.4 {UI_FONT};color:var(--mid)}}
.band{{flex:0 0 auto;background:var(--deep);color:#dff3f6;padding:12px {SAFE}px 14px}}
.band .p{{font:700 16px/1.35 {UI_FONT}}}
.band .p b{{color:var(--accent);letter-spacing:.09em}}
.band .g{{font:400 12px/1.45 {UI_FONT};opacity:.8;margin-top:5px}}
.folio{{position:absolute;bottom:5px;right:13px;font:700 11px/1 {UI_FONT};
  color:#dff3f6;opacity:.55}}
.full{{position:relative;flex:1 1 auto;display:flex;flex-direction:column;
  align-items:center;justify-content:center;text-align:center;padding:{SAFE}px;color:#fff}}
.full .bg{{position:absolute;inset:0;overflow:hidden}}
.full .bg svg{{width:100%;height:100%;display:block}}
.full .scrim{{position:absolute;inset:0;background:
  linear-gradient(180deg,rgba(8,26,34,.80),rgba(8,26,34,.32) 44%,
  rgba(8,26,34,.36) 58%,rgba(8,26,34,.82))}}
.full .in{{position:relative;z-index:1;max-width:30ch}}
.full.cover{{justify-content:flex-end;padding-bottom:76px}}
.full.cover .scrim{{background:linear-gradient(180deg,rgba(8,26,34,.34) 0%,
  rgba(8,26,34,.20) 34%,rgba(8,26,34,.72) 62%,rgba(8,26,34,.92) 100%)}}
.full .sup{{font:800 20px/1 {UI_FONT};letter-spacing:.3em;text-transform:uppercase;color:var(--light)}}
.full h1{{font:800 66px/1.05 {STORY_FONT};margin:12px 0 8px;text-shadow:0 3px 18px rgba(0,0,0,.55)}}
.full .pilots{{font:600 19px/1.5 {UI_FONT};color:#eaf6f7}}
.note{{background:var(--sand);color:var(--deep);text-align:left;
  align-items:flex-start;justify-content:center}}
.note .kick{{font:700 13px/1 {UI_FONT};letter-spacing:.2em;text-transform:uppercase;color:var(--mid)}}
.note h2{{font:800 40px/1.15 {STORY_FONT};margin:10px 0 16px}}
.note .rule{{width:88px;height:5px;background:var(--accent);border-radius:3px;margin-bottom:22px}}
.note p{{font:400 20px/1.6 {UI_FONT};margin-bottom:16px;max-width:52ch}}
.note p b{{color:var(--mid)}}
.beats{{display:flex;gap:14px;justify-content:center;margin:22px 0;width:100%}}
.beat{{flex:1 1 0;background:rgba(255,255,255,.10);border:3px solid var(--mid);
  border-radius:16px;padding:16px 6px}}
.beat .n{{font:800 28px/1 {STORY_FONT};color:var(--accent)}}
.beat .w{{font:800 21px/1.2 {STORY_FONT};margin:6px 0 3px}}
.beat .d{{font:400 13px/1.3 {UI_FONT};color:var(--light)}}
.dial{{font:700 23px/1.55 {STORY_FONT};color:var(--light)}}
.motto{{margin-top:20px;font:600 15px/1.5 {UI_FONT};color:var(--accent);font-style:italic}}
@page{{size:8.5in 8.5in;margin:0}}
@media print{{
  body{{background:#fff}}
  .page{{margin:0;page-break-after:always;break-after:page}}
  .page:last-child{{page-break-after:auto;break-after:auto}}
}}
"""


def svg(book, page, par="xMidYMid slice"):
    return (f'<svg viewBox="0 0 1000 640" preserveAspectRatio="{par}" role="img" '
            f'aria-hidden="true">{art.bleed(book, page)}{art.scene(book, page)}</svg>')


def story(lines):
    return "".join("<span class='sp'></span>" if not l else l + "<br>" for l in lines)


def render(book):
    bn = book["number"]
    out = [f'<title>The Wonder Ship — {html.escape(book["title"])}</title>',
           f"<style>{css(book['palette'])}</style>"]

    for p in book["model"]:
        n = p["n"]
        head = (f'<section class="page" data-document-role="page" '
                f'data-label="p{n} · {html.escape(p["beat"])}" '
                f'data-speaker-notes="{html.escape(p.get("pause", "") or p["beat"], quote=True)}">')

        if p["kind"] == "title":
            out.append(f'''{head}<div class="full cover"><div class="bg">{svg(bn, n)}</div>
<div class="scrim"></div><div class="in"><div class="sup">{p["series"]}</div>
<h1>{html.escape(p["title"])}</h1>
<div class="pilots">{html.escape(p["pilots"])}</div></div></div>
<div class="folio">{n}</div></section>''')
        elif p["kind"] == "note":
            ps = "".join(f"<p>{t}</p>" for t in p["text"])
            out.append(f'''{head}<div class="full note"><div class="in" style="max-width:56ch">
<div class="kick">{html.escape(p["kicker"])}</div><h2>{html.escape(p["heading"])}</h2>
<div class="rule"></div>{ps}</div></div>
<div class="folio" style="color:var(--mid)">{n}</div></section>''')
        elif p["kind"] == "theme":
            beats = "".join(f'<div class="beat"><div class="n">{a}</div>'
                            f'<div class="w">{b}</div><div class="d">{c}</div></div>'
                            for a, b, c in p["clap"])
            out.append(f'''{head}<div class="full"><div class="bg">{svg(bn, n)}</div>
<div class="scrim" style="background:rgba(8,26,34,.66)"></div>
<div class="in" style="max-width:40ch"><h1 style="font-size:44px">{html.escape(p["heading"])}</h1>
<div class="pilots">{html.escape(p["sub"])}</div><div class="beats">{beats}</div>
<div class="dial">{"<br>".join(p["dial"])}</div>
<div class="motto">{html.escape(p["motto"])}</div></div></div>
<div class="folio">{n}</div></section>''')
        else:
            out.append(f'''{head}
<div class="art"><!-- ART: {html.escape(p["art"])} -->{svg(bn, n)}</div>
<div class="story">{story(p["text"])}</div>
<div class="band"><div class="p"><b>PAUSE:</b> {p["pause"]}</div>
<div class="g"><b>GROWN-UPS:</b> {p["grown"]}</div></div>
<div class="folio">{n}</div></section>''')

    return "\n".join(out)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for b in all_books():
        doc = render(b)
        with open(os.path.join(OUT, b["slug"] + ".html"), "w", encoding="utf-8") as f:
            f.write(doc)
        print(f'{b["slug"]}.html — {doc.count("data-document-role")} pages, {len(doc)/1024:.0f} KB')
