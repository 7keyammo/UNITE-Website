# The book bot

One book a week until the school year is full.

## The idea

A Wonder Ship book is 24 pages, but only ten of them are new writing. Pages
1–6 and 21–24 are the fixed ritual — identical in every book, on purpose.
Pages 7–10 are the arrival sequence, generated from four short strings. That
leaves **ten authored beats**, and everything else is generated from them.

So the weekly job is small enough to actually do every week:

```
python3 bot.py next          # the brief for the next unwritten week
python3 bot.py template 14   # a skeleton to paste into specs.py
                             # ... write the ten beats ...
python3 bot.py check         # validates specs, word counts, cues and art
python3 bot.py build --pdf   # regenerates app, print, ebook, presentation
```

`bot.py status` shows the year:

```
The Wonder Ship — 13 of 50 books written
  Term 1 · Feeling sound          [##########] 10/10
  Term 2 · Fast, slow, big, small [###.......] 3/10
  ...
next: week 14 — The Beehive
```

## What is automated, and what is not

**Generated:** all artwork, every page layout, the app, the print PDF, the
EPUB, the presentation deck, the release schedule, and the validation.

**Written by a person (or by Claude on the weekly run):** the ten beats. The
words a three-year-old hears are the one part that should not be autofilled.
`bot.py next` exists to make that hand-off exact — it prints the world, the
term, the concept for each beat, and the house rules.

## Adding a destination

`plan.py` is the year. `worlds.py` is what each destination looks like — a
palette, a backdrop kind, a terrain and a cast, about a dozen lines. The
engine turns that into all 13 world-specific pages, so a new world needs no
new drawing code.

`scenes.py` holds the concept scenes — `two_sizes` is amplitude, `two_speeds`
is frequency, `feel_ground` is energy through solids. A book picks five; the
engine renders them in that book's world.

## Files

| File | What it holds |
|---|---|
| `plan.py` | The 50-week year: titles, worlds, concepts, curriculum links |
| `worlds.py` | 33 destinations as visual specs |
| `specs.py` | The authored words, week 4 onward |
| `books.py` | Weeks 1–3, hand-composed before the engine existed |
| `compose.py` | Spec → 24-page model |
| `scenes.py` | World class, generic beats, concept scenes |
| `fauna.py` | Parametric creatures, plants, terrain |
| `prims.py` | Characters, the ship, sound marks |
| `art.py` | Page → scene dispatch |
| `content.py` | The one page model every output format reads |
| `render.py` `app.py` `deck.py` `epub.py` | The four outputs |
| `bot.py` | The weekly workflow |
