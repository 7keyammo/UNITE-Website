# The Wonder Ship

A **50-week school year** of read-aloud picture books for ages 3 (preschool / TK), built as the pre-K on-ramp to two existing K–2 curricula:

- **STEAM + Music** — 15 classes, Grades K–2
- **Energy, Frequency & Vibration** — 15 lessons, Grades K–2

Every book runs on the same engine as those curricula: **voice, clapping, stomping, humming, breath, movement, imagination. No materials.**

One book a week, fifty weeks, five terms. `build/plan.py` holds the whole year;
`build/bot.py` writes the next one.

| Term | Weeks | Thread |
|---|---|---|
| 1 · Feeling sound | 1–10 | Vibration, energy, the body as an instrument |
| 2 · Fast, slow, big, small | 11–20 | Frequency and amplitude as two separate dials |
| 3 · Where sound goes | 21–30 | Travel, echo, absorption, acoustics |
| 4 · Out where there is no air | 31–40 | Waves, vacuum, energy you can see |
| 5 · Inside the instrument | 41–50 | Resonance, the body, and the showcase |

## Live site

| Where | URL |
|---|---|
| **GitHub Pages** — the whole thing: site, reader, PDFs | https://7keyammo.github.io/UNITE-Website/wonder-ship/ |
| Reader app direct | https://7keyammo.github.io/UNITE-Website/wonder-ship/app/ |
| Print & deliver | https://7keyammo.github.io/UNITE-Website/wonder-ship/print-pack.html |

Pages serves straight from `main` — no build step, no workflow, no `gh-pages`
branch. Anything merged to `main` under `wonder-ship/` goes live in a minute or two.

**To add Vercel as a second host:** connect GitHub in Vercel (Settings -> Login
Connections), then import `7keyammo/UNITE-Website` and set **Root Directory** to
`wonder-ship`. No build command and no framework — it is static files. Every push
to `main` then deploys automatically.

---

## What's here

```
wonder-ship/
├── app/                       THE APP — offline, works on any device
│   ├── index.html             one self-contained file (all art, styles, code inlined)
│   ├── sw.js                  service worker: install to a home screen, run offline
│   ├── manifest.webmanifest
│   └── icon.svg
├── print/                     Print-ready PDFs, 8.5 x 8.5 in, 24 pages, illustrated
├── ebook/                     Fixed-layout EPUB 3, one per book
├── presentation/              16:9 decks (HTML for Canva import + PDF), for smartboards
├── canva/                     Book-format HTML, one <section> per page, Canva-importable
├── CURRICULUM-MAP.md          The crosswalk: 30 K–2 lessons → the 8-beat template
├── manuscripts/               Page-by-page text with PAUSE and GROWN-UPS cues
├── brief/
│   ├── ILLUSTRATION-BRIEF.md  Character sheets, palettes, layout grid, art direction
│   └── TEACHER-GUIDE.md       Classroom facilitation guide
└── build/                     The generator — everything above is built from here
    ├── books.py               story content
    ├── content.py             one page model shared by all four outputs
    ├── prims.py               SVG primitives (characters, ship, sound)
    ├── art.py                 72 scene compositions
    ├── render.py → canva/ + print/      app.py → app/
    ├── deck.py   → presentation/        epub.py → ebook/
    └── app_css.py, app_js.py  the reader's stylesheet and behaviour
```

---

## The app

`app/index.html` is a single self-contained file. No CDN, no fonts to fetch, no network
of any kind. Open it from a hard drive, a USB stick, an email attachment or a school
server and it just runs.

**On any device.** Phone portrait stacks art over words. Tablet gives the illustration
the whole upper half. On a laptop or a smartboard the page splits — art left, words
right. Type and artwork scale to the viewport rather than to a fixed page.

**What it does**

| Control | What happens |
|---|---|
| Tap the page edges, swipe, or arrow keys | Turn the page |
| **Read to me** | Speaks the page aloud (device speech, still offline) |
| **Clap** | Plays the four-beat Wonder Ship Clap — sound and light, generated live, no audio files |
| **Slow / Fast** | The tempo dial. Slow to settle a room, fast to launch |
| **Notes** | Hides the teacher band so children see only the story |
| **Full screen** | Edge-to-edge for a smartboard or a lap |
| Breathing ring | Appears on pages 3, 4 and 21 and paces the in-and-out automatically |

It remembers the book and page you were on, and `#b2p13`-style links open a specific
page directly — handy for jumping a class straight to a movement break.

**Install it.** Served over http (a school server, or GitHub Pages), the service worker
caches it and it installs to a home screen like an app. Opened from a file, it still
works completely — installation is the only thing that needs a server.

---

## The four outputs, and who each is for

| Output | Where | For |
|---|---|---|
| **Interactive app** | `app/index.html` | The classroom and the living room. Movement, sound, read-aloud. |
| **Print PDF** | `print/*.pdf` | 8.5 × 8.5 in, 24 pages — KDP, IngramSpark, any printer. |
| **EPUB 3** | `ebook/*.epub` | Kindle, Apple Books, Kobo, library platforms. Fixed layout, so art and words stay together. |
| **Presentation** | `presentation/*` | Smartboards and projectors. 16:9, illustration left, big words right. |

All four are generated from the same `build/content.py` page model, so they cannot
drift apart. Change a line of story text once and rebuild — every format updates.

---

## Book specification

| Spec | Value |
|---|---|
| Trim size | 8.5 × 8.5 in (square) |
| Page count | 24 interior pages (all three books, identical) |
| Bleed | 0.125 in — build art at 8.75 × 8.75 in |
| Safe margin | 0.5 in from trim |
| Gutter allowance | 0.375 in inner edge |
| Story word count | 230–240 words per book |
| Read-aloud time | 6–8 min; 12–18 min with all movement pauses |
| Resolution | 300 dpi minimum; CMYK for print, sRGB for ebook |

**24 pages is deliberate.** It is the minimum interior page count Amazon KDP accepts for a paperback, and it is a multiple of 2 for perfect binding.

---

## The reusable template

All three books are the same 24 pages. Only the world changes. That is what makes Books 4, 5, and 6 cheap to produce.

| Pages | Beat | Fixed in every book? |
|---|---|---|
| 1 | Title | Layout fixed, title changes |
| 2 | How to Fly This Book | **Identical text** |
| 3–4 | Liftoff Ritual — breathe | **Identical text** |
| 5–6 | Liftoff Ritual — clap | **Identical except one pilot line** |
| 7–8 | Departure | New world |
| 9–10 | Arrival | New world |
| 11–12 | Explore A — discovery | New world |
| 13–14 | Explore A — **movement** | New world |
| 15–16 | Explore B — discovery | New world |
| 17–18 | Explore B — **movement** | New world |
| 19–20 | Wonder Moment | New world |
| 21–22 | Return Ritual | **Identical except direction** |
| 23 | Landing + Mission Log | Layout fixed, question changes |
| 24 | The Wonder Ship Clap | **Identical** |

**14 of 24 pages are fixed or near-fixed.** A new title needs 10 new pages of text and 22 new illustrations.

---

## Regenerating the files

Content lives in `build/books.py`. Layout lives in `build/render.py`. Nothing else needs editing.

```bash
cd wonder-ship/build
python3 render.py     # -> canva/*.html   (book-format, Canva-importable)
python3 app.py        # -> app/index.html (the offline reader)
python3 deck.py       # -> presentation/  (16:9 slides)
python3 epub.py       # -> ebook/*.epub   (validated on build)

# then re-export the PDFs
cd ..
CHROME=/path/to/chrome
for f in canva/*.html presentation/*.html; do
  b=$(basename "$f" .html); d=$(dirname "$f")
  "$CHROME" --headless --disable-gpu --no-pdf-header-footer \
    --print-to-pdf="$d/$b.pdf" "file://$PWD/$f"
done
mv canva/*.pdf print/
```

**Where to change what**

| To change | Edit |
|---|---|
| Story words, PAUSE cues, teacher notes | `build/books.py` |
| An illustration | `build/art.py` (scenes) or `build/prims.py` (characters, ship) |
| How the app behaves | `build/app_js.py` |
| How anything looks | `build/app_css.py`, or the `css()` in `render.py` / `deck.py` |

To add **Book 4**, append one entry to `BOOKS` in `books.py` reusing `ritual_pages()`,
`return_pages()`, `landing_page()` and `THEME_PAGE`, then add its 13 world scenes to
`art.py`. Those helpers *are* the template — you physically cannot drift from it. Every
one of the four outputs picks the new book up automatically.

---

## Getting these into Canva

The HTML files are annotated with `data-document-role="page"` on every page, plus `data-label` (page name) and `data-speaker-notes` (the beat and PAUSE cue). Canva turns each `<section>` into one artboard.

**Import from this repo (the repo is public, so the raw URLs work directly):**

```
https://raw.githubusercontent.com/7keyammo/UNITE-Website/claude/wonder-ship-books-gpdxew/wonder-ship/canva/book-01-into-the-deep.html
https://raw.githubusercontent.com/7keyammo/UNITE-Website/claude/wonder-ship-books-gpdxew/wonder-ship/canva/book-02-among-the-stars.html
https://raw.githubusercontent.com/7keyammo/UNITE-Website/claude/wonder-ship-books-gpdxew/wonder-ship/canva/book-03-back-to-the-dinosaurs.html
```

**Once inside Canva:**

1. **Swap the fonts.** The HTML names `Baloo 2` (story) and `Nunito` (UI) with safe fallbacks. Both are free in Canva. Set them once in Brand Kit and they apply everywhere.
2. **Replace the dashed boxes.** Every dashed rectangle is an illustration placeholder holding its own art direction. Drop the final artwork in and delete the note.
3. **Do not move the teacher band.** The solid bar across the bottom is the same height and position on all 24 pages. It is what makes the template reusable.
4. **Save Book 1 as a Brand Template** once its layout is signed off. Books 2 and 3 then become content swaps.
5. **Resize to 8.75 × 8.75 in** before final print export if you want full bleed.

---

## Export and sell

Everything in `print/`, `ebook/` and `presentation/` is a finished, saleable file today —
illustrated, paginated and correct. Nothing is a placeholder any more.

| Channel | File to use | Notes |
|---|---|---|
| Amazon KDP paperback | `print/*.pdf` | 24 pages meets the minimum; 8.5 × 8.5 square trim is supported. Rebuild at 8.75 in for full bleed. |
| IngramSpark | `print/*.pdf` → PDF/X-1a | Ask them for the spine width of a 24-page block. |
| Kindle / Apple Books / Kobo | `ebook/*.epub` | Fixed-layout EPUB 3, so illustration and words never separate. |
| Teachers Pay Teachers | `print/*.pdf` + `TEACHER-GUIDE.md` | Bundle all three books with the guide. |
| School / district licence | The whole `app/` folder | Highest-margin channel. Put it on a school server or hand it over on a USB stick. |
| Smartboard / assembly | `presentation/*.pdf` or the Canva deck | 16:9, big type, readable from the back of a room. |

### Going through Canva

**Read this before relying on the Canva copies.**

Canva's importer does not render an imported document — it rebuilds it into
Canva's own native elements. On this artwork that conversion degrades the
figures (limbs and outlines drop out). That happened through every route
tried: HTML with inline SVG, HTML with the artwork pre-rasterised, the print
PDF, and finally HTML where each page is a single flat PNG. The source files
are not at fault — the same files render correctly in browsers, in the print
pipeline and in e-readers, all of which were checked visually.

The Canva imports exist and each has 24 pages, but **open them and look before
using them**. Canva's full-resolution export could not be checked from the
build environment (the download host is blocked there), so it is possible the
degradation is only in Canva's preview and the export is fine. Judge it in the
editor.

**If the Canva copies look wrong**, use one of these instead — all verified:

1. `print/*.pdf` is already a finished, sellable book. Upload it straight to
   KDP or a printer; Canva is not needed in the path at all.
2. Upload `print/*.pdf` to Canva by hand through Canva's own web uploader,
   which is a different code path from the API import used here.
3. Edit the source and rebuild: text lives in `build/books.py`, artwork in
   `build/art.py`, and `render.py` regenerates the PDFs.

The Canva builds are `canva/*.html` (24 square book pages) and
`presentation/*-presentation-canva.html` (24 sixteen-by-nine slides). Both are
made of flat page images, so page text is not editable inside Canva — text
edits belong in `build/books.py`. Both carry `data-document-role="page"` and
`data-label`, so each page lands as its own named artboard.

## Open items

- **Confirm the spelling of Mr. Domkam.** The planning notes spelled it "Mr. Domcom" once.
  Everything here uses **Domkam**, and it appears on every title page and cover.
- **The illustrations are original vector art, drawn to `brief/ILLUSTRATION-BRIEF.md`** —
  consistent characters, palettes and layout grid across all 72 pages. They are complete
  and shippable. If you later commission a painter, the brief and the layout grid are the
  handover document, and only `build/art.py` changes.
- Decide the print channel, then set the final bleed (8.75 in) and spine width.
- Optional: record the Wonder Ship Clap as real audio for the ebook edition. The app
  already generates its click live, so this only matters for EPUB.

*Mentality Over Excuses — no materials, no excuses, all music.*
