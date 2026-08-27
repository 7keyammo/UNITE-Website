# -*- coding: utf-8 -*-
"""Build the 16:9 presentation deck — for Canva import and smartboard reading.

Same 24 beats, landscape: illustration on the left, words large on the right,
teacher cue underneath. Sized 1920x1080 so it imports as a standard
presentation and projects at full size in a classroom.
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import art                                          # noqa: E402
from content import all_books                       # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "presentation")
W, H = 1920, 1080

UI = "'Nunito','Trebuchet MS','DejaVu Sans',sans-serif"
ST = "'Baloo 2','Quicksand','Trebuchet MS','DejaVu Sans',sans-serif"


def css(p):
    return f"""
:root{{--deep:{p['deep']};--mid:{p['mid']};--light:{p['light']};
--accent:{p['accent']};--sand:{p['sand']}}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#333;font-family:{UI}}}
.slide{{position:relative;width:{W}px;height:{H}px;margin:0 auto 24px;overflow:hidden;
  background:var(--sand);display:flex}}
.left{{position:relative;flex:0 0 58%;overflow:hidden}}
.left svg{{position:absolute;inset:0;width:100%;height:100%}}
.right{{flex:1 1 auto;display:flex;flex-direction:column;background:#fffaf0}}
.copy{{flex:1 1 auto;display:flex;flex-direction:column;justify-content:center;
  padding:56px 64px;text-align:center;font:800 52px/1.3 {ST};color:var(--deep)}}
.copy .sp{{display:block;height:.4em}}
.copy .log{{display:block;margin:22px auto 0;max-width:22ch;padding:20px 26px;
  border:4px solid var(--accent);border-radius:20px;font:700 32px/1.4 {UI};color:var(--mid)}}
.band{{flex:0 0 auto;background:var(--deep);color:#dff3f6;padding:26px 40px 30px}}
.band .p{{font:800 30px/1.3 {UI}}}
.band .p b{{color:var(--accent);letter-spacing:.08em}}
.band .g{{font:400 21px/1.45 {UI};opacity:.8;margin-top:10px}}
.folio{{position:absolute;bottom:16px;right:26px;font:700 20px/1 {UI};color:#dff3f6;opacity:.5}}
.wide{{flex:1 1 100%;position:relative;display:flex;align-items:center;
  justify-content:center;text-align:center;color:#fff;padding:80px}}
.wide .bg{{position:absolute;inset:0;overflow:hidden}}
.wide .bg svg{{width:100%;height:100%}}
.scrim{{position:absolute;inset:0}}
.in{{position:relative;z-index:1;max-width:30ch}}
.wide.cover{{align-items:flex-end;padding-bottom:74px}}
.sup{{font:800 34px/1 {UI};letter-spacing:.32em;text-transform:uppercase;color:var(--light)}}
h1{{font:800 132px/1.03 {ST};margin:22px 0 16px;text-shadow:0 4px 26px rgba(0,0,0,.55)}}
.pilots{{font:600 34px/1.5 {UI};color:#eaf6f7}}
.note{{background:var(--sand);color:var(--deep);text-align:left;justify-content:flex-start}}
.kick{{font:800 24px/1 {UI};letter-spacing:.2em;text-transform:uppercase;color:var(--mid)}}
h2{{font:800 82px/1.1 {ST};margin:18px 0 26px}}
.rule{{width:150px;height:8px;background:var(--accent);border-radius:4px;margin-bottom:38px}}
.note p{{font:400 36px/1.6 {UI};margin-bottom:26px;max-width:44ch}}
.note p b{{color:var(--mid)}}
.beats{{display:flex;gap:26px;justify-content:center;margin:40px 0;width:100%}}
.beat{{flex:1 1 0;background:rgba(255,255,255,.10);border:5px solid var(--mid);
  border-radius:26px;padding:30px 12px}}
.beat .n{{font:800 54px/1 {ST};color:var(--accent)}}
.beat .w{{font:800 40px/1.2 {ST};margin:10px 0 6px}}
.beat .d{{font:400 24px/1.3 {UI};color:var(--light)}}
.dial{{font:700 42px/1.5 {ST};color:var(--light)}}
.motto{{margin-top:34px;font:600 26px/1.5 {UI};color:var(--accent);font-style:italic}}
@page{{size:1920px 1080px;margin:0}}
@media print{{body{{background:#fff}}.slide{{margin:0;page-break-after:always;break-after:page}}
.slide:last-child{{page-break-after:auto;break-after:auto}}}}
"""


def svg(b, n):
    return (f'<svg viewBox="0 0 1000 640" preserveAspectRatio="xMidYMid slice" role="img" '
            f'aria-hidden="true">{art.bleed(b, n)}{art.scene(b, n)}</svg>')


def story(lines):
    return "".join("<span class='sp'></span>" if not l else l + "<br>" for l in lines)


def render(book):
    bn = book["number"]
    out = [f'<title>The Wonder Ship — {html.escape(book["title"])} (presentation)</title>',
           f"<style>{css(book['palette'])}</style>"]
    for p in book["model"]:
        n = p["n"]
        notes = (f'{p["beat"]}. PAUSE: {p["pause"]} GROWN-UPS: '
                 f'{art.__dict__.get("_", "")}{p["grown"]}') if p["kind"] == "story" else p["beat"]
        notes = html.escape(__import__("re").sub(r"<[^>]+>", "", notes), quote=True)
        head = (f'<section class="slide" data-document-role="page" '
                f'data-label="p{n} · {html.escape(p["beat"])}" data-speaker-notes="{notes}">')

        if p["kind"] == "title":
            out.append(f'''{head}<div class="wide cover"><div class="bg">{svg(bn, n)}</div>
<div class="scrim" style="background:linear-gradient(180deg,rgba(8,26,34,.32),rgba(8,26,34,.18) 32%,rgba(8,26,34,.74) 62%,rgba(8,26,34,.92))"></div>
<div class="in"><div class="sup">{p["series"]}</div><h1>{html.escape(p["title"])}</h1>
<div class="pilots">{html.escape(p["pilots"])}</div></div></div>
<div class="folio">{n}</div></section>''')
        elif p["kind"] == "note":
            ps = "".join(f"<p>{t}</p>" for t in p["text"])
            out.append(f'''{head}<div class="wide note"><div class="in" style="max-width:56ch">
<div class="kick">{html.escape(p["kicker"])}</div><h2>{html.escape(p["heading"])}</h2>
<div class="rule"></div>{ps}</div></div><div class="folio" style="color:var(--mid)">{n}</div></section>''')
        elif p["kind"] == "theme":
            beats = "".join(f'<div class="beat"><div class="n">{a}</div><div class="w">{b}</div>'
                            f'<div class="d">{c}</div></div>' for a, b, c in p["clap"])
            out.append(f'''{head}<div class="wide"><div class="bg">{svg(bn, n)}</div>
<div class="scrim" style="background:rgba(8,26,34,.68)"></div>
<div class="in" style="max-width:46ch"><h1 style="font-size:86px">{html.escape(p["heading"])}</h1>
<div class="pilots">{html.escape(p["sub"])}</div><div class="beats">{beats}</div>
<div class="dial">{"<br>".join(p["dial"])}</div>
<div class="motto">{html.escape(p["motto"])}</div></div></div>
<div class="folio">{n}</div></section>''')
        else:
            out.append(f'''{head}<div class="left">{svg(bn, n)}</div>
<div class="right"><div class="copy">{story(p["text"])}</div>
<div class="band"><div class="p"><b>PAUSE:</b> {p["pause"]}</div>
<div class="g"><b>GROWN-UPS:</b> {p["grown"]}</div></div></div>
<div class="folio">{n}</div></section>''')
    return "\n".join(out)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for b in all_books():
        doc = render(b)
        with open(os.path.join(OUT, b["slug"] + "-presentation.html"), "w", encoding="utf-8") as f:
            f.write(doc)
        print(f'{b["slug"]}-presentation.html — {doc.count("data-document-role")} slides, '
              f'{len(doc)/1024:.0f} KB')
