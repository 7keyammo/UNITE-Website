#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The Wonder Ship book bot.

One book a week, until the school year is full.

    python3 bot.py status          what exists, what is next
    python3 bot.py next            the brief for the next unwritten week
    python3 bot.py template [wk]   a ready-to-fill spec to paste into specs.py
    python3 bot.py check           validate every spec
    python3 bot.py build [--pdf]   regenerate every output format + the website
    python3 bot.py ship            check, build, and report what changed

Writing the words is the one step a machine should not fake: `next` prints
the brief, an author (or Claude, on the weekly run) writes ten beats, and
everything downstream is generated.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from plan import PLAN, TERMS, by_week, term_of        # noqa: E402


def written():
    import specs
    return set(specs.SPECS) | {1, 2, 3}               # 1-3 predate the engine


def next_week():
    have = written()
    for row in PLAN:
        if row[0] not in have:
            return row
    return None


def cmd_status():
    have = sorted(written())
    print(f"The Wonder Ship — {len(have)} of {len(PLAN)} books written")
    for a, z, name, _ in TERMS:
        got = [w for w in have if a <= w <= z]
        bar = "".join("#" if w in have else "." for w in range(a, z + 1))
        print(f"  {name:38} [{bar}] {len(got)}/{z - a + 1}")
    nxt = next_week()
    print(f"\nnext: week {nxt[0]} — {nxt[2]}" if nxt else "\nThe year is complete.")


def cmd_next(week=None):
    row = by_week(int(week)) if week else next_week()
    if not row:
        print("The year is complete — nothing left to write.")
        return
    wk, slug, title, world, concepts, tag, big = row
    name, blurb = term_of(wk)
    from worlds import WORLDS
    w = WORLDS[world]
    print(f"""
================ BRIEF: WEEK {wk} ================
Title       {title}
World       {world}  ({w.kind})
Term        {name} — {blurb}
Big feeling {big}
Curriculum  {tag}

Ten beats to write, two pages each:
  beats 1-2   first discovery      scene: {concepts[0]}
  beats 3-4   its movement break   scene: {concepts[1]}
  beats 5-6   second discovery     scene: {concepts[2]}
  beats 7-8   its movement break   scene: {concepts[3]}
  beats 9-10  the wonder moment    scene: {concepts[4]}

House rules
  - Ages 3. Short rhythmic lines. Around 280-310 story words for the book.
  - "" in a line list is a blank line. Read it aloud before you keep it.
  - Every beat needs a PAUSE (a movement cue, six words or fewer) and a
    GROWN-UPS note naming the EFV lesson or STEAM class it feeds.
  - The wonder moment is quiet. End the book calm.
  - Do not restate the ritual pages; the engine supplies 1-6 and 21-24.

Run  python3 bot.py template {wk}  for the skeleton to paste into specs.py.
=================================================
""")


TEMPLATE = '''
# ============================================================ week {wk}
spec(Spec(
    week={wk},
    up=["window", "birds", "clouds"],
    porthole=("COLOUR", "COLOUR again", "TEASER"),
    land=("SOUND.", "ONE DETAIL LINE."),
    here="WHERE WE ARE",
    log="MISSION LOG QUESTION?",
    home=["Home LINE.", "", "Home, home, <b>HOME!</b>"],
    beats=[
{beats}    ]))
'''


def cmd_template(week=None):
    row = by_week(int(week)) if week else next_week()
    wk, slug, title, world, concepts, tag, big = row
    labels = ["discovery 1", "discovery 2", "movement 1", "movement 2",
              "discovery 3", "discovery 4", "movement 3", "movement 4",
              "wonder 1", "wonder 2"]
    beats = ""
    for i, lab in enumerate(labels):
        c = concepts[i // 2]
        beats += (f'        # {lab} — scene: {c}\n'
                  f'        B(["LINE.", "", "LINE.", "", "LINE."],\n'
                  f'          "PAUSE CUE.",\n'
                  f'          "GROWN-UPS NOTE."),\n')
    print(TEMPLATE.format(wk=wk, beats=beats))


def cmd_check():
    import specs                                       # noqa: F401
    from compose import build
    from content import all_books
    bad = []
    for wk, s in sorted(specs.SPECS.items()):
        try:
            b = build(s)
            words = sum(len(" ".join(p.get("text", [])).split()) for p in b["pages"])
            if not 180 <= words <= 460:
                bad.append(f"week {wk}: {words} story words (expected 180-460)")
            for p in b["pages"]:
                if p["kind"] == "story" and not p.get("pause"):
                    bad.append(f"week {wk}: a story page has no PAUSE cue")
        except Exception as e:
            bad.append(f"week {wk}: {e}")
    import art
    for b in all_books():
        for p in b["model"]:
            try:
                art.scene(b["week"], p["n"])
            except Exception as e:
                bad.append(f"week {b['week']} page {p['n']}: art failed — {e}")
    if bad:
        print("PROBLEMS:")
        for m in bad:
            print("  -", m)
        return 1
    n = len(all_books())
    print(f"ok — {n} books, {n * 24} pages, every spec and every scene valid")
    return 0


def _run(mod):
    print(f"  {mod} ...", end=" ", flush=True)
    r = subprocess.run([sys.executable, os.path.join(HERE, mod)],
                       capture_output=True, text=True)
    if r.returncode:
        print("FAILED")
        print(r.stdout[-2000:], r.stderr[-2000:])
        raise SystemExit(1)
    print("ok")


CHROME = os.environ.get("CHROME", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")


def cmd_build(pdf=False):
    print("building every format:")
    for m in ("render.py", "app.py", "deck.py", "epub.py", "website.py"):
        _run(m)
    if pdf:
        print("  PDFs ...", end=" ", flush=True)
        import glob
        n = 0
        for src in sorted(glob.glob(os.path.join(ROOT, "print", "*.html"))
                          + glob.glob(os.path.join(ROOT, "presentation", "*-presentation.html"))):
            out = src[:-5] + ".pdf"
            subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                            "--no-pdf-header-footer", "--virtual-time-budget=9000",
                            f"--print-to-pdf={out}", "file://" + src],
                           capture_output=True)
            n += 1
        print(f"ok ({n})")
        _run("pack.py")          # merged print pack, after the book PDFs exist
    print("done")


def cmd_ship(pdf=False):
    if cmd_check():
        raise SystemExit(1)
    cmd_build(pdf)
    cmd_status()


if __name__ == "__main__":
    a = sys.argv[1:] or ["status"]
    c = a[0]
    if c == "status":
        cmd_status()
    elif c == "next":
        cmd_next(a[1] if len(a) > 1 else None)
    elif c == "template":
        cmd_template(a[1] if len(a) > 1 else None)
    elif c == "check":
        raise SystemExit(cmd_check())
    elif c == "build":
        cmd_build("--pdf" in a)
    elif c == "ship":
        cmd_ship("--pdf" in a)
    else:
        print(__doc__)
        raise SystemExit(2)
