# The Wonder Ship

A three-book read-aloud picture book series for ages 3 (preschool / TK), built as the pre-K on-ramp to two existing K–2 curricula:

- **STEAM + Music** — 15 classes, Grades K–2
- **Energy, Frequency & Vibration** — 15 lessons, Grades K–2

Every book runs on the same engine as those curricula: **voice, clapping, stomping, humming, breath, movement, imagination. No materials.**

| # | Title | World | The big feeling |
|---|---|---|---|
| 1 | Into the Deep | Underwater | Sound can be soft, slow, and muffled |
| 2 | Among the Stars | Outer space | Sound can be *absent* — and you still carry your own |
| 3 | Back to the Dinosaurs | Prehistoric | Sound can be enormous, and the world answers back |

---

## What's here

```
wonder-ship/
├── CURRICULUM-MAP.md          The crosswalk: 30 K–2 lessons → the 8-beat book template
├── manuscripts/               Full page-by-page text, with PAUSE and GROWN-UPS cues
│   ├── book-01-into-the-deep.md
│   ├── book-02-among-the-stars.md
│   └── book-03-back-to-the-dinosaurs.md
├── brief/
│   ├── ILLUSTRATION-BRIEF.md  Character sheets, palettes, layout grid, per-page art direction
│   └── TEACHER-GUIDE.md       Classroom facilitation guide
├── canva/                     Print-ready HTML — one <section> per book page, Canva-importable
│   ├── book-01-into-the-deep.html
│   ├── book-02-among-the-stars.html
│   └── book-03-back-to-the-dinosaurs.html
├── print/                     Generated PDFs, 8.5 × 8.5 in, 24 pages
└── build/                     The generator (books.py = content, render.py = layout)
```

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
python3 render.py                       # rewrites canva/*.html

# then re-export the PDFs
cd ..
CHROME=/path/to/chrome
for f in canva/*.html; do
  b=$(basename "$f" .html)
  "$CHROME" --headless --disable-gpu --no-pdf-header-footer \
    --print-to-pdf="print/$b.pdf" "file://$PWD/$f"
done
```

To add **Book 4**, append one entry to `BOOKS` in `books.py` reusing `ritual_pages()`, `return_pages()`, `landing_page()`, and `THEME_PAGE`. Those helpers *are* the template — you physically cannot drift from it.

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

**Canva → Share → Download → PDF Print**, with *Crop marks and bleed* on.

| Channel | Format | Notes |
|---|---|---|
| Amazon KDP paperback | PDF Print, CMYK, 8.5 × 8.5 in + bleed | 24 pages meets the minimum; square trim is supported |
| IngramSpark | PDF/X-1a:2001 | Ask them for the exact spine width for a 24-page block |
| Ebook / Kindle Kids | Fixed-layout EPUB or PDF, sRGB | Keep the PAUSE bands — they read fine on tablet |
| Teachers Pay Teachers | PDF, sRGB | Bundle the three books with `TEACHER-GUIDE.md` |
| Classroom / school licence | PDF + printable | Highest-margin channel; sell the set plus the guide |

The **PDFs in `print/` are exportable and sellable right now** — 24 pages, correct trim, real text, teacher cues in place. What they hold instead of art is a labeled placeholder for each illustration. They are a complete dummy: readable aloud in a classroom today, and a drop-in frame for final artwork.

---

## Open items

- **Confirm the spelling of Mr. Domkam.** The planning notes spelled it "Mr. Domcom" once. Everything here uses **Domkam**, and it appears on every title page.
- Commission illustration against `brief/ILLUSTRATION-BRIEF.md`.
- Decide print channel, then set the final bleed and spine.
- Optional: record the Wonder Ship Clap as audio for the ebook edition.

*Mentality Over Excuses — no materials, no excuses, all music.*
