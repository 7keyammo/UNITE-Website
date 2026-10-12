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
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import art                                            # noqa: E402
from content import all_books                         # noqa: E402
from plan import PLAN, TERMS                          # noqa: E402
from site_css import CSS                              # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOKDIR = os.path.join(ROOT, "books")

# When the site is hosted somewhere that does not carry the heavy files
# (PDFs, EPUBs, the reader's book chunks), point those at the public repo
# instead. Set by build(asset_base=..., reader=...).
ASSETS = ""      # prefix for print/ ebook/ presentation/
READER = ""      # absolute URL of the reader app, if hosted elsewhere

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
  <a class="brand" href="{up}index.html">{SHIP_MARK}<span>UNITE STEAM</span></a>
  <nav class="navlinks">
    <a class="lnk" href="{up}books.html">Books</a>
    <a class="lnk" href="{up}saturday-school.html">Saturday School</a>
    <a class="lnk" href="{up}pricing.html">Pricing</a>
    <a class="lnk" href="{up}teachers.html">Teachers</a>
    <a class="lnk" href="{up}print-pack.html">Print</a>
  </nav>
  <a class="lnk cta" href="{READER or up + 'app/index.html'}">Read now</a>
</div></header>"""


def foot(depth=0):
    up = "../" * depth
    return f"""<footer><div class="wrap">
<div>
  <h5>UNITE STEAM</h5>
  <p>Unique Natives Interacting Together Elevating. An Afrocentric, youth-led future
     grounded in truth, love, and science. Oakland, California.</p>
  <p>The Wonder Ship is fifty weekly read-aloud picture books for ages 3, built on the
     STEAM&nbsp;+&nbsp;Music and Energy, Frequency &amp; Vibration K–2 curricula, piloted
     by Mr.&nbsp;Domkam and Mr.&nbsp;Johnson.</p>
  <p class="motto">Mentality Over Excuses — no materials, no excuses, all music.</p>
</div>
<div><h5>Learn</h5>
  <a href="{READER or up + 'app/index.html'}">Open the library</a>
  <a href="{up}books.html">All 50 books</a>
  <a href="{up}saturday-school.html">Saturday School</a>
  <a href="{up}pricing.html">Offerings &amp; pricing</a>
  <a href="{up}print-pack.html">Print &amp; deliver</a>
</div>
<div><h5>More</h5>
  <a href="{up}teachers.html">For teachers</a>
  <a href="https://unitehella.org" target="_blank" rel="noopener">unitehella.org</a>
  <a href="mailto:unitehella@gmail.com">unitehella@gmail.com</a>
  <a href="{up}privacy.html">Privacy</a>
  <a href="{up}terms.html">Terms</a>
</div>
</div></footer></body></html>"""


ICONS = {
    "breath": '<path d="M12 3v6M8 6l4-3 4 3" stroke="#0f6d80" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/><circle cx="12" cy="15" r="6" stroke="#ff7a59" stroke-width="2.4" fill="none"/>',
    "clap": '<path d="M5 12l3-7 2 1-2 6M9 11l3-7 2 1-2 7M13 12l3-6 2 1-3 8M5 12c-1 4 2 8 6 8s6-3 6-6" stroke="#0f6d80" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
    "move": '<circle cx="12" cy="4.5" r="2.2" fill="#ff7a59"/><path d="M12 7v6m0 0l-3 6m3-6l3 6M7 10l5-1 5 1" stroke="#0f6d80" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
}


# ============================================================== landing
def books_page(books):
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

    return head("The books — The Wonder Ship · UNITE STEAM",
                "Fifty weekly picture books for 3-year-olds with a movement break on every "
                "page. Read online free, or print and have them delivered.") + f"""
<section class="hero"><div class="wrap">
  <div class="sup">The Homeschool Hub · The Wonder Ship</div>
  <h1>A school year of read-alouds. No materials.</h1>
  <p class="lede">Fifty weekly picture books for three-year-olds, piloted by
     Mr.&nbsp;Domkam and Mr.&nbsp;Johnson. Every page has a movement break. Every book is
     built on two K–2 curricula. Nothing to buy, nothing to prep — just bodies,
     voices and breath.</p>
  <div class="row">
    <a class="btn p" href="{READER or 'app/index.html'}">Read the books free</a>
    <a class="btn g" href="print-pack.html">Print &amp; have them delivered</a>
    <a class="btn s" href="index.html">About UNITE STEAM</a>
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
  <div class="crumb"><a href="../books.html">All books</a> · Week {wk}</div>
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
        <a class="main" href="{(READER + '#b' + str(wk) + 'p1') if READER else '../app/index.html#b' + str(wk) + 'p1'}">Read it now <em>free, works offline</em></a>
        <a href="{ASSETS or "../"}print/{slug}.pdf" download>Print-ready PDF <em>8.5×8.5 in · 24 pp</em></a>
        <a href="{ASSETS or "../"}ebook/{slug}.epub" download>EPUB ebook <em>Kindle, Apple Books</em></a>
        <a href="{ASSETS or "../"}presentation/{slug}-presentation.pdf" download>Presentation <em>16:9 for smartboards</em></a>
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


# ============================================================ UNITE pages
import unite as U                                      # noqa: E402


def _icon(kind):
    d = {
        "school": "<path d='M4 10 12 5l8 5v9H4z'/><path d='M9 19v-5h6v5'/>",
        "ship": "<path d='M4 13q0 6 8 6t8-6'/><path d='M3 10h18'/><circle cx='12' cy='12' r='2.6'/>",
        "seed": "<path d='M12 21V11'/><path d='M12 11c0-4 3-6 7-6 0 4-3 6-7 6z'/>"
                "<path d='M12 14C9 14 6 12 5 8c4-1 7 1 7 6z'/>",
    }[kind]
    return (f"<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.9' "
            f"stroke-linecap='round' stroke-linejoin='round'>{d}</svg>")


def impact_band():
    stats = "".join(f'<div class="stat"><b>{v}</b><span>{html.escape(l)}</span></div>'
                    for v, l in U.IMPACT)
    return (f'<div class="statband">{stats}</div>'
            f'<p class="statnote">{html.escape(U.IMPACT_NOTE)}</p>')


def price_grid(order=("homeschool", "saturday")):
    """All three billing periods, switched client-side. No JS, no prices."""
    plans = {p["key"]: p for p in U.PLANS}
    def _tog(k, lab):
        cls = ' class="active"' if k == "monthly" else ""
        return f'<button type="button" data-cad="{k}"{cls}>{lab}</button>'

    toggle = "".join(_tog(k, lab) for k, lab, _sfx, _m in U.CADENCES)
    cards = []
    for key in order:
        p = plans[key]
        feats = "".join(f"<li>{html.escape(f)}</li>" for f in p["features"])
        prices = []
        for k, _lab, sfx, months in U.CADENCES:
            amount = p["price"][k]
            per = amount / months
            sub = ("" if k == "monthly" else
                   f'<span class="permo">about ${per:.2f}/mo · save '
                   f'{round((1 - per / p["price"]["monthly"]) * 100)}%</span>')
            prices.append(f'<div class="pr" data-cad="{k}"{"" if k == "monthly" else " hidden"}>'
                          f'<span class="amt">${amount}</span><span class="sfx">{sfx}</span>{sub}</div>')
        cards.append(
            f'<div class="pricecard{" featured" if p["featured"] else ""}">'
            + ('<span class="badge">Most complete</span>' if p["featured"] else "")
            + f'<h3>{html.escape(p["name"])}</h3>'
            f'<p class="pblurb">{html.escape(p["blurb"])}</p>'
            f'<div class="prices">{"".join(prices)}</div>'
            f'<ul class="feats">{feats}</ul>'
            f'<a class="btn p" href="mailto:{U.ORG["email"]}'
            f'?subject={quote("UNITE STEAM — " + p["name"])}">Ask about this plan</a></div>')
    return (f'<div class="cadence" role="group" aria-label="Billing period">{toggle}</div>'
            f'<div class="pricegrid">{"".join(cards)}</div>'
            + PRICE_JS)


PRICE_JS = """
<script>
(function(){
  var btns=[].slice.call(document.querySelectorAll('.cadence button'));
  btns.forEach(function(b){
    b.addEventListener('click',function(){
      var c=b.dataset.cad;
      btns.forEach(function(x){x.classList.toggle('active',x===b)});
      [].forEach.call(document.querySelectorAll('.pr'),function(p){
        p.hidden = p.dataset.cad!==c;
      });
    });
  });
})();
</script>"""


def shelves_block(n_books):
    out = []
    for s in U.SHELVES:
        if s["on"]:
            out.append(
                f'<a class="acard on" href="{s["href"]}"><span class="wm">{html.escape(s["name"])}</span>'
                f'<span class="sub">{html.escape(s["sub"])}</span>'
                f'<span class="count">{s["count"].format(n=n_books)}</span></a>')
        else:
            out.append(
                f'<div class="acard off"><span class="wm">{html.escape(s["name"])}</span>'
                f'<span class="sub">{html.escape(s["sub"])}</span>'
                f'<span class="count">{html.escape(s["count"])}</span>'
                f'<span class="note">{html.escape(s.get("note",""))}</span></div>')
    return '<div class="ages">' + "".join(out) + "</div>"


def unite_home(books):
    n = len(books)
    progs = "".join(
        f'<a class="prog" href="{p["href"]}"><span class="ico">{_icon(p["icon"])}</span>'
        f'<h3>{html.escape(p["name"])}</h3><p>{html.escape(p["text"])}</p>'
        f'<span class="go">{html.escape(p["go"])} &rarr;</span></a>' for p in U.PROGRAMS)
    custom = "".join(f'<div><b>{html.escape(t)}</b><span>{html.escape(d)}</span></div>'
                     for t, d in U.CUSTOM)
    steps = "".join(f'<li><div><b>{html.escape(t)}</b><span>{html.escape(d)}</span></div></li>'
                    for t, d in U.STEPS)
    return head(f'{U.ORG["name"]} — {U.ORG["tagline"]}', U.ORG["lede"]) + f"""
<section class="hero"><div class="wrap">
  <div class="sup">UNITE · {html.escape(U.ORG["expand"])}</div>
  <h1>Building stronger communities, <em>one step at a time.</em></h1>
  <p class="lede">{html.escape(U.ORG["lede"])}</p>
  <div class="row">
    <a class="btn g" href="#register">Register today</a>
    <a class="btn p" href="pricing.html">See offerings &amp; pricing</a>
    <a class="btn s" href="books.html">Read the books free</a>
  </div>
</div>
<div class="ship" aria-hidden="true">{cover(1)}</div>
</section>

<section><div class="wrap">
  {impact_band()}
  <div class="sechead" style="margin-top:46px">
    <span class="label">Our programs</span>
    <h2 class="sec">Three ways to learn with UNITE.</h2>
    <p class="sub">Pick the one that fits your family. Saturday School always includes
       the Homeschool Hub.</p>
  </div>
  <div class="progs">{progs}</div>
  <div class="custom">{custom}</div>
</div></section>

<section class="alt"><div class="wrap">
  <span class="label">The Homeschool Hub</span>
  <h2 class="sec">The Wonder Ship — a school year of read-alouds.</h2>
  <p class="sub">Fifty weekly picture books for three-year-olds, piloted by
     Mr.&nbsp;Domkam and Mr.&nbsp;Johnson. Every page has a movement break. Every book is
     built on two K–2 curricula. {n} are written so far, and a new one arrives every week.</p>
  <div class="row" style="margin-bottom:26px">
    <a class="btn p" href="books.html">Browse all 50 books</a>
    <a class="btn s" style="background:var(--mid)" href="print-pack.html">Print &amp; deliver</a>
  </div>
  <h3 style="font-size:20px;font-weight:800;color:var(--deep);margin-bottom:6px">
    Browse the Homeschool Hub by age</h3>
  <p class="sub">1 of 5 shelves built.</p>
  {shelves_block(n)}
</div></section>

<section id="register"><div class="wrap">
  <span class="label">How to register</span>
  <h2 class="sec">Four steps to get started.</h2>
  <p class="sub">Tell us what you’re interested in, or go straight to a plan.</p>
  <div class="regwrap">
    <ol class="steps4">{steps}</ol>
    <div class="regbox">
      <h4>Register your interest</h4>
      <p>Accounts and card payment open with the members site. Until then, email us and
         we’ll get you set up by hand — tell us your child’s age range and whether you
         want the Hub, Saturday School, or something custom.</p>
      <a class="btn p" href="mailto:{U.ORG["email"]}?subject={quote("UNITE STEAM — register my interest")}&amp;body={quote("Child age range:%0D%0AInterested in (Hub / Saturday School / custom):%0D%0ACity:%0D%0AAnything else:")}">Email {U.ORG["email"]}</a>
      <p class="small">Or visit <a href="{U.ORG["org_site"]}" target="_blank" rel="noopener">unitehella.org</a>.</p>
    </div>
  </div>
</div></section>

<section class="alt"><div class="wrap">
  <span class="label">Our mission</span>
  <h2 class="sec">Truth, love, and science.</h2>
  <p class="sub" style="font-size:clamp(16px,2.2vw,20px);max-width:66ch">
    {html.escape(U.ORG["mission"])}</p>
</div></section>
""" + foot()


def saturday_page(books):
    S_ = U.SATURDAY
    running = "".join(f"<p>{html.escape(t)}</p>" for t in S_["running"])
    meta = "".join(f"<span>{html.escape(m)}</span>" for m in S_["meta"])
    inc = "".join(f"<li>{html.escape(i)}</li>" for i in S_["included"])
    return head("Saturday School — UNITE STEAM", S_["lede"]) + f"""
<section class="hero" style="padding:52px 0 44px"><div class="wrap">
  <div class="sup">{html.escape(S_["kicker"])}</div>
  <h1 style="font-size:clamp(30px,6vw,52px)">Saturday School</h1>
  <p class="lede">{html.escape(S_["lede"])}</p>
</div></section>

<section><div class="wrap"><div class="satwrap">
  <div class="satcard">
    <span class="label">Currently running</span>
    <h3>{html.escape(S_["running_title"])}</h3>
    {running}
    <div class="satmeta">{meta}</div>
  </div>
  <div class="satcard tint">
    <h3>What’s included</h3>
    <ul class="ticks">{inc}</ul>
    <p class="seatnote">{html.escape(S_["seatnote"])}</p>
  </div>
</div></div></section>

<section class="alt"><div class="wrap">
  <h2 class="sec">Choose how you join</h2>
  <p class="sub">{html.escape(U.PRICE_NOTE)}</p>
  {price_grid(("saturday", "homeschool"))}
</div></section>
""" + foot()


def pricing_page(books):
    rungs = "".join(
        f'<div class="rung"><div class="num">{i+1}</div><div><h3>{html.escape(t)}</h3>'
        f'<p>{html.escape(d)}</p><span class="tag">{html.escape(tag)}</span></div></div>'
        for i, (t, d, tag) in enumerate(U.LADDER))
    return head("Offerings &amp; pricing — UNITE STEAM",
                "From free open content to custom curriculum design for organizations.") + f"""
<section class="hero" style="padding:52px 0 44px"><div class="wrap">
  <div class="sup">UNITE STEAM offerings</div>
  <h1 style="font-size:clamp(30px,6vw,52px)">Five ways to work with us.</h1>
  <p class="lede">From free open content to custom curriculum design for organizations.
     Pick the level that fits your family or your team.</p>
</div></section>

<section><div class="wrap">
  <div class="ladder">{rungs}</div>
</div></section>

<section class="alt"><div class="wrap">
  <h2 class="sec">Homeschool Hub &amp; Saturday School</h2>
  <p class="sub">{html.escape(U.PRICE_NOTE)}</p>
  {price_grid(("homeschool", "saturday"))}
  <div class="notice">
    <b>Card payment isn’t switched on yet.</b> Email
    <a href="mailto:{U.ORG["email"]}">{U.ORG["email"]}</a> and we’ll set you up by hand
    in the meantime. The books on this site stay free to read and print either way.
  </div>
</div></section>

<section id="custom"><div class="wrap">
  <h2 class="sec">Custom work &amp; community projects</h2>
  <p class="sub">Personalized curriculum, private tutoring and organization work are
     priced to fit. Tell us what you need and we’ll follow up with a quote.</p>
  <a class="btn p" href="mailto:{U.ORG["email"]}?subject={quote("UNITE STEAM — custom work enquiry")}">Email us about custom work</a>
</div></section>
""" + foot()


def legal_page(title, sections, desc):
    body = "".join(
        f"<h2>{html.escape(h)}</h2>" + "".join(
            (b if b.lstrip().startswith("<") else f"<p>{b}</p>") for b in paras)
        for h, paras in sections)
    return head(f"{title} — UNITE STEAM", desc) + f"""
<section><div class="wrap prose">
  <h1 class="sec" style="font-size:clamp(28px,5vw,42px)">{html.escape(title)}</h1>
  <div class="notice">{html.escape(U.LEGAL_NOTE)}</div>
  {body}
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
    pack_base = json.dumps((ASSETS or "") + "print/")
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
      <a class="btn p" href="{ASSETS}print/wonder-ship-print-pack.pdf" download>Download all {n} as one PDF</a>
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
        a.href={pack_base}+x.slug+'.pdf'; a.download=x.slug+'.pdf';
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
def build(asset_base="", reader=""):
    global ASSETS, READER
    ASSETS, READER = asset_base, reader
    books = all_books()
    os.makedirs(BOOKDIR, exist_ok=True)
    with open(os.path.join(ROOT, "site.css"), "w", encoding="utf-8") as f:
        f.write(CSS)
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(unite_home(books))
    with open(os.path.join(ROOT, "books.html"), "w", encoding="utf-8") as f:
        f.write(books_page(books))
    with open(os.path.join(ROOT, "saturday-school.html"), "w", encoding="utf-8") as f:
        f.write(saturday_page(books))
    with open(os.path.join(ROOT, "pricing.html"), "w", encoding="utf-8") as f:
        f.write(pricing_page(books))
    with open(os.path.join(ROOT, "privacy.html"), "w", encoding="utf-8") as f:
        f.write(legal_page("Privacy policy", U.PRIVACY,
                           "How UNITE STEAM handles accounts, payments and form data."))
    with open(os.path.join(ROOT, "terms.html"), "w", encoding="utf-8") as f:
        f.write(legal_page("Terms of service", U.TERMS,
                           "Membership, cancelling, Saturday School and content terms."))
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
    print(f"site built — home, books, Saturday School, pricing, teachers, print pack, "
          f"privacy, terms + {len(bs)} book pages")
