# -*- coding: utf-8 -*-
"""Build the public website.

Generated from the same content model as every other output, so the weekly
bot keeps the site in sync automatically: a new book appears on the landing
page, gets its own page, and joins the print pack with no extra step.

Output lands in wonder-ship/ itself, so one folder serves both GitHub Pages
(/UNITE-Website/wonder-ship/) and Vercel (root directory = wonder-ship).
"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import art                                            # noqa: E402
from content import all_books                         # noqa: E402
from plan import PLAN, TERMS                          # noqa: E402
from site_css import CSS                              # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOKDIR = os.path.join(ROOT, "books")

SHIP_MARK = (
    '<svg viewBox="0 0 100 100" aria-hidden="true">'
    '<path d="M14 46q0 30 36 33t36-33q0-9-7-11H21q-7 2-7 11z" fill="#c98a4b" stroke="#23303a" stroke-width="5"/>'
    '<rect x="10" y="30" width="80" height="8" rx="4" fill="#0f6d80" stroke="#23303a" stroke-width="5"/>'
    '<circle cx="50" cy="52" r="17" fill="#eaf6f7" stroke="#23303a" stroke-width="5"/>'
    '<circle cx="50" cy="52" r="12" fill="#7fd4d8"/></svg>')


def cover(week, cls=""):
    return (f'<svg viewBox="0 0 1000 640" preserveAspectRatio="xMidYMid slice" '
            f'class="{cls}" role="img" aria-hidden="true">'
            f'{art.bleed(week, 1)}{art.scene(week, 1)}</svg>')


def head(title, desc, depth=0):
    up = "../" * depth
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#0b3a4a">
<link rel="icon" href="{up}app/icon.svg">
<link rel="stylesheet" href="{up}site.css">
</head><body>
<header class="nav"><div class="wrap">
  <a class="brand" href="{up}index.html">{SHIP_MARK}<span>The Wonder Ship</span></a>
  <a class="lnk" href="{up}index.html#books">Books</a>
  <a class="lnk" href="{up}teachers.html">Teachers</a>
  <a class="lnk" href="{up}print-pack.html">Print &amp; deliver</a>
  <a class="lnk cta" href="{up}app/index.html">Read now</a>
</div></header>"""


def foot(depth=0):
    up = "../" * depth
    return f"""<footer><div class="wrap">
<div>
  <h5>The Wonder Ship</h5>
  <p>Fifty weekly read-aloud picture books for ages 3, built on the STEAM&nbsp;+&nbsp;Music
     and Energy, Frequency &amp; Vibration K–2 curricula. Piloted by Mr.&nbsp;Domkam and
     Mr.&nbsp;Johnson.</p>
  <p class="motto">Mentality Over Excuses — no materials, no excuses, all music.</p>
</div>
<div><h5>Read</h5>
  <a href="{up}app/index.html">Open the library</a>
  <a href="{up}index.html#books">All 50 books</a>
  <a href="{up}print-pack.html">Print &amp; deliver</a>
</div>
<div><h5>Teachers</h5>
  <a href="{up}teachers.html">Curriculum map</a>
  <a href="{up}brief/TEACHER-GUIDE.md">Teacher guide</a>
  <a href="{up}brief/ILLUSTRATION-BRIEF.md">Illustration brief</a>
</div>
</div></footer></body></html>"""


ICONS = {
    "breath": '<path d="M12 3v6M8 6l4-3 4 3" stroke="#0f6d80" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/><circle cx="12" cy="15" r="6" stroke="#ff7a59" stroke-width="2.4" fill="none"/>',
    "clap": '<path d="M5 12l3-7 2 1-2 6M9 11l3-7 2 1-2 7M13 12l3-6 2 1-3 8M5 12c-1 4 2 8 6 8s6-3 6-6" stroke="#0f6d80" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
    "move": '<circle cx="12" cy="4.5" r="2.2" fill="#ff7a59"/><path d="M12 7v6m0 0l-3 6m3-6l3 6M7 10l5-1 5 1" stroke="#0f6d80" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
}


# ============================================================== landing
def landing(books):
    have = {b["week"]: b for b in books}
    n = len(books)

    shelves = []
    for a, z, name, blurb in TERMS:
        shelves.append(f'<div class="termhead"><h3>{html.escape(name)}</h3>'
                       f'<span>{html.escape(blurb)}</span></div><div class="grid four">')
        for wk, slug, title, world, concepts, tag, big in PLAN:
            if not (a <= wk <= z):
                continue
            b = have.get(wk)
            if b:
                shelves.append(
                    f'<a class="bk" href="books/{slug}.html">'
                    f'<div class="cov"><span class="wk">Week {wk}</span>{cover(wk)}</div>'
                    f'<div class="m"><h3>{html.escape(title)}</h3>'
                    f'<div class="w">{html.escape(b["world"])} · 24 pages</div>'
                    f'<div class="c">{html.escape(tag)}</div>'
                    f'<span class="go">Read or print</span></div></a>')
            else:
                shelves.append(
                    f'<div class="bk soon"><div class="cov"><span class="wk">Week {wk}</span>'
                    f'<span class="lockmsg">Arrives week {wk}</span></div>'
                    f'<div class="m"><h3>{html.escape(title)}</h3>'
                    f'<div class="w">{html.escape(big)}</div>'
                    f'<div class="c">{html.escape(tag)}</div>'
                    f'<span class="go">Scheduled</span></div></div>')
        shelves.append("</div>")

    return head("The Wonder Ship — a school year of read-aloud books for ages 3",
                "Fifty weekly picture books for 3-year-olds with a movement break on every "
                "page. Read online free, or print and have them delivered.") + f"""
<section class="hero"><div class="wrap">
  <div class="sup">The Wonder Ship</div>
  <h1>A school year of read-alouds. No materials.</h1>
  <p class="lede">Fifty weekly picture books for three-year-olds, piloted by
     Mr.&nbsp;Domkam and Mr.&nbsp;Johnson. Every page has a movement break. Every book is
     built on two K–2 curricula. Nothing to buy, nothing to prep — just bodies,
     voices and breath.</p>
  <div class="row">
    <a class="btn p" href="app/index.html">Read the books free</a>
    <a class="btn g" href="print-pack.html">Print &amp; have them delivered</a>
    <a class="btn s" href="#books">See all 50</a>
  </div>
  <div class="stats">
    <div class="stat"><b>{n}</b><span>books ready now</span></div>
    <div class="stat"><b>50</b><span>weeks planned</span></div>
    <div class="stat"><b>24</b><span>pages each</span></div>
    <div class="stat"><b>Free</b><span>to read online</span></div>
  </div>
</div>
<div class="ship" aria-hidden="true">{cover(1)}</div>
</section>

<section><div class="wrap">
  <h2 class="sec">Three things repeat in every single book</h2>
  <p class="sub">That is the whole design. A three-year-old does not need novelty — they
     need something they can own. By the third book these belong to them, and they work
     outside the story too.</p>
  <div class="feat">
    <div class="f"><div class="ic"><svg viewBox="0 0 24 24">{ICONS['breath']}</svg></div>
      <h4>The Breath</h4>
      <p>Hand on chest, breathe in, breathe out, hum. It opens and closes every book — and
         it is the same move you can use at line-up, at nap time, or when a child is
         escalating.</p></div>
    <div class="f"><div class="ic"><svg viewBox="0 0 24 24">{ICONS['clap']}</svg></div>
      <h4>The Wonder Ship Clap</h4>
      <p>Clap, clap, pat, whoosh. Four beats. Slow it down to settle a room, speed it up to
         raise energy. Beat four is a breath, so even the fast version ends in an exhale.</p></div>
    <div class="f"><div class="ic"><svg viewBox="0 0 24 24">{ICONS['move']}</svg></div>
      <h4>A movement break per page</h4>
      <p>Stomp, float, swim, cup your ears, palms flat on the floor. The illustration shows
         the movement, and a footer tells the grown-up which lesson it feeds.</p></div>
  </div>
</div></section>

<section class="alt"><div class="wrap">
  <h2 class="sec">Built on two real curricula</h2>
  <p class="sub">K–2 names a concept and explores it. A three-year-old cannot hold the name —
     so they do the physics in their body, and the vocabulary lives in the teacher sidebar
     where only the adult sees it. All 30 lessons are mapped.</p>
  <div class="tw"><table>
    <tr><th>What a K–2 class will call it</th><th>What the 3-year-old actually does</th></tr>
    <tr><td>Vibration</td><td>Hums with a hand on their chest</td></tr>
    <tr><td>Energy transfer</td><td>Claps harder to make the ship go</td></tr>
    <tr><td>Frequency</td><td>Fast wiggle sounds high, slow wave sounds low</td></tr>
    <tr><td>Amplitude</td><td>Big clap, tiny clap — same hands</td></tr>
    <tr><td>Resonance</td><td>Hums with the whale and feels it in their chest</td></tr>
    <tr><td>Vacuum</td><td>Listens to nothing, then hums and hears themselves</td></tr>
    <tr><td>Acoustics</td><td>Calls to the mountain and waits</td></tr>
  </table></div>
  <p style="margin-top:18px"><a class="btn s" style="background:var(--mid)"
     href="teachers.html">See the full curriculum map</a></p>
</div></section>

<section id="books"><div class="wrap">
  <h2 class="sec">The year, week by week</h2>
  <p class="sub">{n} of 50 written so far, and a new one every Monday. Books already
     written open right here; the rest show the week they arrive.</p>
  {''.join(shelves)}
</div></section>

<section class="alt"><div class="wrap">
  <h2 class="sec">Want them as real books?</h2>
  <p class="sub">Every book is a finished print-ready file: 8.5 × 8.5 inch square, 24 pages,
     correct trim and page order. Pick the ones you want, download one print pack, and take
     it to any print shop — they print and deliver.</p>
  <a class="btn p" href="print-pack.html">Build a print pack</a>
</div></section>
""" + foot()


# ============================================================== book page
def book_page(b):
    wk = b["week"]
    row = next(r for r in PLAN if r[0] == wk)
    _, slug, title, world, concepts, tag, big = row
    story = [p for p in b["model"] if p["kind"] == "story"]
    beats = "".join(
        f'<li><b>{html.escape(p["pause"])}</b>'
        f'<span>page {p["n"]} · {html.escape(p["beat"])}</span></li>'
        for p in story if p["pause"])
    words = sum(len(" ".join(p.get("text", [])).split()) for p in b["model"])

    return head(f'{title} — The Wonder Ship (week {wk})',
                f'{big}. A read-aloud picture book for ages 3, with a movement break on '
                f'every page. Read free online or print it.', depth=1) + f"""
<div class="bkhead"><div class="cover">{cover(wk)}</div></div>
<div class="bkbody"><div class="wrap">
  <div class="crumb"><a href="../index.html">All books</a> · Week {wk}</div>
  <h1>{html.escape(title)}</h1>
  <div class="big">{html.escape(big)}</div>
  <div class="pills">
    <span class="pill">Week {wk}</span>
    <span class="pill">{html.escape(b["world"])}</span>
    <span class="pill">24 pages</span>
    <span class="pill">{words} story words</span>
    <span class="pill">Ages 3 · TK</span>
  </div>
  <div class="cols">
    <div>
      <h2 class="sec" style="font-size:22px">Every movement break in this book</h2>
      <p class="sub" style="margin-bottom:14px">Stop reading, do the thing, then turn the
         page. The pauses are the curriculum.</p>
      <ul class="beats">{beats}</ul>
      <h2 class="sec" style="font-size:22px;margin-top:32px">Curriculum</h2>
      <p class="sub">{html.escape(tag)}</p>
      <p class="sub">EFV = <em>Energy, Frequency &amp; Vibration</em>, 15 lessons, K–2.
         STEAM = <em>STEAM + Music</em>, 15 classes, K–2. Both run on voice, clapping,
         stomping, humming, breath and movement — no materials.</p>
    </div>
    <aside class="side">
      <h4>Read or print</h4>
      <div class="dl">
        <a class="main" href="../app/index.html#b{wk}p1">Read it now <em>free, works offline</em></a>
        <a href="../print/{slug}.pdf" download>Print-ready PDF <em>8.5×8.5 in · 24 pp</em></a>
        <a href="../ebook/{slug}.epub" download>EPUB ebook <em>Kindle, Apple Books</em></a>
        <a href="../presentation/{slug}-presentation.pdf" download>Presentation <em>16:9 for smartboards</em></a>
        <a href="../print-pack.html?add={wk}">Add to print pack <em>order printed copies</em></a>
      </div>
    </aside>
  </div>
</div></div>
""" + foot(depth=1)


# ============================================================== teachers
def teachers(books):
    rows = "".join(
        f'<tr><td>{r[0]}</td><td><b>{html.escape(r[2])}</b></td>'
        f'<td>{html.escape(r[6])}</td><td>{html.escape(r[5])}</td>'
        f'<td>{"Ready" if r[0] in {b["week"] for b in books} else f"Week {r[0]}"}</td></tr>'
        for r in PLAN)
    return head("Teachers — The Wonder Ship",
                "How to run the books, the 50-week plan, and the full crosswalk to the "
                "STEAM + Music and Energy, Frequency & Vibration K–2 curricula.") + f"""
<section class="hero" style="padding:52px 0 44px"><div class="wrap">
  <div class="sup">For teachers</div>
  <h1 style="font-size:clamp(28px,5.4vw,46px)">Everything you need to run these</h1>
  <p class="lede">Total time per book: 12–18 minutes with all the pauses. Materials
     required: none.</p>
</div></section>

<section><div class="wrap">
  <h2 class="sec">How to read one</h2>
  <ol class="steps">
    <li><b>Sit low</b><p>Children on the floor, you at their level.</p></li>
    <li><b>Read page 2 to yourself, not out loud</b><p>It is for you, not them.</p></li>
    <li><b>Do every PAUSE</b><p>Read the story text, stop, do the action together, then turn.
        The pauses are the lesson — skipping them leaves you with a very short story.</p></li>
    <li><b>Hold the silences</b><p>Page 19 of every book has a written silence. Count five in
        your head. It will feel long. That is correct.</p></li>
    <li><b>Take every answer</b><p>On the "What do you see?" page there are no wrong ones.</p></li>
    <li><b>End with the Mission Log</b><p>One question, one round of answers, then everyone
        makes their own signature sound.</p></li>
  </ol>
</div></section>

<section class="alt"><div class="wrap">
  <h2 class="sec">Use it outside the book</h2>
  <div class="feat">
    <div class="f"><h4>The Breath</h4><p>"Hand on your chest, wake up the ship." Works at
      line-up, before nap, and with a child who is escalating.</p></div>
    <div class="f"><h4>The Clap</h4><p>Your attention signal. You clap the four beats;
      they clap them back. Slow to settle, fast to energise.</p></div>
    <div class="f"><h4>The Signature Sound</h4><p>Every child has one that is theirs.
      Name it out loud: "Nobody else makes that one."</p></div>
  </div>
</div></section>

<section><div class="wrap">
  <h2 class="sec">The 50-week plan</h2>
  <p class="sub">Five terms. Each book carries one big idea and feeds named lessons in both
     K–2 series. EFV = Energy, Frequency &amp; Vibration. STEAM = STEAM + Music.</p>
  <div class="tw"><table>
    <tr><th>Wk</th><th>Book</th><th>The big feeling</th><th>Feeds</th><th>Status</th></tr>
    {rows}
  </table></div>
</div></section>

<section class="alt"><div class="wrap">
  <h2 class="sec">Documents</h2>
  <div class="feat">
    <div class="f"><h4>Teacher guide</h4><p>Facilitation, behaviour notes, mixed-age groups,
      and where it leads next.</p>
      <p style="margin-top:10px"><a class="btn s" style="background:var(--mid);font-size:14px;padding:9px 18px"
         href="brief/TEACHER-GUIDE.md">Open</a></p></div>
    <div class="f"><h4>Curriculum crosswalk</h4><p>All 30 K–2 lessons mapped onto the
      8-beat book template.</p>
      <p style="margin-top:10px"><a class="btn s" style="background:var(--mid);font-size:14px;padding:9px 18px"
         href="CURRICULUM-MAP.md">Open</a></p></div>
    <div class="f"><h4>Illustration brief</h4><p>Character sheets, palettes, layout grid and
      per-page art direction.</p>
      <p style="margin-top:10px"><a class="btn s" style="background:var(--mid);font-size:14px;padding:9px 18px"
         href="brief/ILLUSTRATION-BRIEF.md">Open</a></p></div>
  </div>
</div></section>
""" + foot()


# ============================================================ print pack
SPEC = dict(trim="8.5 × 8.5 in (216 × 216 mm) square",
            pages="24 interior pages",
            bleed="none required — the PDFs are trimmed size",
            colour="full colour, both sides",
            paper="150–200 gsm silk or matt for the interior",
            binding="saddle-stitch (staple) — 24 pages is ideal for it",
            finish="optional matt lamination on the cover")


def print_pack(books):
    rows = "".join(
        f'<label class="pick"><input type="checkbox" data-wk="{b["week"]}" '
        f'data-slug="{b["slug"]}" data-title="{html.escape(b["title"], quote=True)}" checked>'
        f'<span class="th">{cover(b["week"])}</span>'
        f'<span class="t"><b>{html.escape(b["title"])}</b>'
        f'<span>Week {b["week"]} · {html.escape(b["world"])} · 24 pages</span></span>'
        f'<input class="qty" type="number" min="1" max="99" value="1" '
        f'aria-label="Copies of {html.escape(b["title"], quote=True)}"></label>'
        for b in books)

    specrows = "".join(f'<tr><th>{k.title()}</th><td>{html.escape(v)}</td></tr>'
                       for k, v in SPEC.items())

    n = len(books)
    return head("Print &amp; deliver — The Wonder Ship",
                "Pick the books you want, download one print-ready pack, and take it to any "
                "print shop. They print and deliver.") + f"""
<section class="hero" style="padding:52px 0 44px"><div class="wrap">
  <div class="sup">Print &amp; deliver</div>
  <h1 style="font-size:clamp(28px,5.4vw,46px)">Real books, delivered</h1>
  <p class="lede">Every book here is already a finished print file — correct trim, correct
     page order, ready to hand over. Pick what you want, download the pack, and any print
     shop can produce and deliver it.</p>
</div></section>

<section><div class="wrap">
  <div class="pack">
    <div>
      <h2 class="sec" style="font-size:23px">1 · Choose your books</h2>
      <div class="picklist">
        <div class="tools">
          <button type="button" id="all">Select all</button>
          <button type="button" id="none">Clear</button>
          <button type="button" id="one">One copy each</button>
          <button type="button" id="cls">A class set (12 each)</button>
        </div>
        {rows}
      </div>

      <h2 class="sec" style="font-size:23px;margin-top:34px">2 · Take it to a printer</h2>
      <ol class="steps">
        <li><b>Download the pack</b><p>You get one PDF per book you chose, plus an order
            sheet listing exactly what to print and how.</p></li>
        <li><b>Upload to any print shop</b><p>Online (Doxdirect, Mixam, Printed.com, Vistaprint,
            Office Depot, Staples) or your local one. Upload the PDFs, paste the spec, choose
            delivery.</p></li>
        <li><b>Give them the spec</b><p>It is on the order sheet and on this page. Square
            8.5 inch, 24 pages, saddle-stitch. Nothing unusual — any shop can do it.</p></li>
        <li><b>They print and deliver</b><p>Turnaround is typically 3–7 days. For one or two
            copies a high-street shop is usually cheapest; for a class set, an online printer
            almost always wins.</p></li>
      </ol>

      <h2 class="sec" style="font-size:23px;margin-top:34px">The print specification</h2>
      <div class="tw"><table>{specrows}</table></div>
      <p class="sub" style="margin-top:14px">Printing a full-bleed edition instead? The
         artwork is vector, so it can be rebuilt at 8.75 in with bleed on request — ask before
         you order if your printer requires it.</p>
    </div>

    <aside class="summary">
      <h4>Your pack</h4>
      <div class="n" id="nbooks">0 <span id="ncopies">books</span></div>
      <ul id="lines"></ul>
      <a class="btn p" href="print/wonder-ship-print-pack.pdf" download>Download all {n} as one PDF</a>
      <a class="btn s" id="dl" href="#" style="margin-top:8px">Download just my selection</a>
      <a class="btn s" id="sheet" href="#" style="margin-top:8px">Print the order sheet</a>
      <div class="spec">
        <b>Everything is free to download.</b> The one-file pack opens with a specification
        page your printer reads first. There is no checkout here — you keep the files and
        choose your own printer, which is nearly always cheaper than a middleman.
      </div>
    </aside>
  </div>
</div></section>

<section class="alt" id="ordersheet-holder"><div class="wrap">
  <h2 class="sec">Order sheet</h2>
  <p class="sub">This is what to hand your printer. It updates as you choose books above.
     Use <b>Print the order sheet</b> to send it straight to your printer or save it as a PDF.</p>
  <div id="sheetview" class="tw" style="padding:22px;background:#fff"></div>
</div></section>

<script>
(function(){{
  var picks=[].slice.call(document.querySelectorAll('.pick'));
  function state(){{
    return picks.map(function(p){{
      var cb=p.querySelector('input[type=checkbox]');
      return {{on:cb.checked, wk:+cb.dataset.wk, slug:cb.dataset.slug,
              title:cb.dataset.title, qty:Math.max(1,+p.querySelector('.qty').value||1)}};
    }}).filter(function(x){{return x.on}});
  }}
  function render(){{
    var s=state();
    var copies=s.reduce(function(a,b){{return a+b.qty}},0);
    document.getElementById('nbooks').firstChild.nodeValue=s.length+' ';
    document.getElementById('ncopies').textContent =
      s.length===1?'title · '+copies+' copies':'titles · '+copies+' copies';
    document.getElementById('lines').innerHTML=s.map(function(x){{
      return '<li><span>'+x.title+'</span><span>x'+x.qty+'</span></li>';
    }}).join('') || '<li><span>Nothing selected yet</span><span></span></li>';

    var sheet='<h3 style="font-size:20px;font-weight:800;color:#0b3a4a">'
      +'The Wonder Ship — print order</h3>'
      +'<p style="color:#5d7079;font-size:14px;margin:6px 0 16px">'
      +s.length+' title'+(s.length===1?'':'s')+', '+copies+' cop'+(copies===1?'y':'ies')
      +' &middot; generated '+new Date().toLocaleDateString()+'</p>'
      +'<table style="min-width:0"><tr><th>Title</th><th>File</th><th>Copies</th></tr>'
      +s.map(function(x){{
        return '<tr><td><b>'+x.title+'</b><br><span style="color:#5d7079;font-size:12px">'
          +'Week '+x.wk+'</span></td><td style="font-family:monospace;font-size:12px">'
          +x.slug+'.pdf</td><td><b>'+x.qty+'</b></td></tr>';
      }}).join('')
      +'</table>'
      +'<h4 style="margin:20px 0 8px;font-size:14px;text-transform:uppercase;'
      +'letter-spacing:.08em;color:#0b3a4a">Print specification</h4>'
      +'<table style="min-width:0">'
      + {{spec_js}}
      +'</table>'
      +'<p style="margin-top:16px;font-size:13px;color:#5d7079">Each PDF is a complete book. '
      +'Print all 24 pages in order, double-sided, and saddle-stitch. Do not scale to fit — '
      +'print at 100%.</p>';
    document.getElementById('sheetview').innerHTML=sheet;
  }}
  picks.forEach(function(p){{
    p.querySelector('input[type=checkbox]').addEventListener('change',render);
    p.querySelector('.qty').addEventListener('input',render);
  }});
  document.getElementById('all').onclick=function(){{
    picks.forEach(function(p){{p.querySelector('input[type=checkbox]').checked=true}});render()}};
  document.getElementById('none').onclick=function(){{
    picks.forEach(function(p){{p.querySelector('input[type=checkbox]').checked=false}});render()}};
  document.getElementById('one').onclick=function(){{
    picks.forEach(function(p){{p.querySelector('.qty').value=1}});render()}};
  document.getElementById('cls').onclick=function(){{
    picks.forEach(function(p){{p.querySelector('.qty').value=12}});render()}};
  document.getElementById('sheet').onclick=function(e){{
    e.preventDefault();
    document.getElementById('ordersheet-holder').scrollIntoView();
    setTimeout(function(){{window.print()}},350);
  }};
  document.getElementById('dl').onclick=function(e){{
    e.preventDefault();
    var s=state();
    if(!s.length){{alert('Choose at least one book first.');return}}
    if(s.length>3){{
      if(!confirm(s.length+' separate files will download. Your browser may ask permission '
        +'for multiple downloads.\n\nFor more than a few books the single "Download all" '
        +'file is easier. Continue anyway?')) return;
    }}
    s.forEach(function(x,i){{
      setTimeout(function(){{
        var a=document.createElement('a');
        a.href='print/'+x.slug+'.pdf'; a.download=x.slug+'.pdf';
        document.body.appendChild(a); a.click(); a.remove();
      }}, i*700);
    }});
    document.getElementById('ordersheet-holder').scrollIntoView();
  }};
  // deep link: print-pack.html?add=7 preselects one book
  var m=/[?&]add=(\\d+)/.exec(location.search);
  if(m){{
    picks.forEach(function(p){{
      var cb=p.querySelector('input[type=checkbox]');
      cb.checked = cb.dataset.wk===m[1];
    }});
  }}
  render();
}})();
</script>
""".replace("{spec_js}", json.dumps(
        "".join(f"<tr><th>{k.title()}</th><td>{v}</td></tr>" for k, v in SPEC.items()))
    ) + foot()


# ============================================================== build
def build():
    books = all_books()
    os.makedirs(BOOKDIR, exist_ok=True)
    with open(os.path.join(ROOT, "site.css"), "w", encoding="utf-8") as f:
        f.write(CSS)
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(landing(books))
    with open(os.path.join(ROOT, "teachers.html"), "w", encoding="utf-8") as f:
        f.write(teachers(books))
    with open(os.path.join(ROOT, "print-pack.html"), "w", encoding="utf-8") as f:
        f.write(print_pack(books))
    for b in books:
        with open(os.path.join(BOOKDIR, b["slug"] + ".html"), "w", encoding="utf-8") as f:
            f.write(book_page(b))
    return books


if __name__ == "__main__":
    bs = build()
    print(f"site built — landing + teachers + print pack + {len(bs)} book pages")
