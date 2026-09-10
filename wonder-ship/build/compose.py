# -*- coding: utf-8 -*-
"""Expand a compact book spec into the full 24-page model.

Pages 1-6 and 21-24 are the template's fixed ritual — identical in every book
by design. Pages 7-10 are the arrival sequence, generated from four short
strings. That leaves pages 11-20 as the only genuinely bespoke writing: five
concept beats, two pages each. That is the authoring unit, and it is what the
weekly bot writes.
"""
from books import ritual_pages, return_pages, landing_page, THEME_PAGE
from plan import by_week

# Which scene partners each concept on the second page of its pair, so a pair
# never draws the same picture twice.
PARTNER = {
    "listen": "close_up", "two_sizes": "close_up", "two_speeds": "wave",
    "wave": "travel", "count": "double", "double": "count",
    "feel_ground": "close_up", "echo": "listen", "silence": "hero",
    "resonance": "hero", "layers": "close_up", "travel": "wave",
    "absorb": "listen", "hero": "resonance", "close_up": "listen",
}


class Beat:
    """One authored page: the words, the movement cue, the teacher note."""

    def __init__(self, lines, pause, grown, art=""):
        self.lines, self.pause, self.grown, self.art = lines, pause, grown, art


def B(lines, pause, grown, art=""):
    return Beat(lines, pause, grown, art)


class Spec:
    """The compact form of a book. Ten Beats plus a handful of strings."""

    def __init__(self, week, up, porthole, land, here, beats, log,
                 pilots=None, home=None):
        assert len(beats) == 10, f"week {week}: need 10 beats, got {len(beats)}"
        self.week = week
        self.up = up                    # 3-4 "Up past the ___" nouns
        self.porthole = porthole        # (colour word, echo line, teaser)
        self.land = land                # (landing sound, one detail line)
        self.here = here                # "in the rainforest"
        self.beats = beats
        self.log = log
        self.pilots = pilots or ("Mr. Domkam grins.", "Mr. Johnson counts.")
        self.home = home or ["Home through the green.", "", "Home, home, <b>HOME!</b>"]


def _interleave(lines):
    """Blank line between each spoken line — the read-aloud rhythm."""
    out = []
    for i, ln in enumerate(lines):
        if i:
            out.append("")
        out.append(ln)
    return out


def arrival_pages(s, world_key):
    """Pages 7-10 — the same four beats in every book, in this book's world."""
    colour, echo, teaser = s.porthole
    sound, detail = s.land
    return [
        dict(kind="story", beat="2 - Departure", art="Exterior. The ship climbing away.",
             text=_interleave(["<b>UP</b> goes the Wonder Ship."]
                              + [f"Up past the {n}." for n in s.up]),
             pause="Stretch both arms up. Reach.",
             grown="A big stretch resets the body after the fast claps."),
        dict(kind="story", beat="2 - Departure",
             art="PORTHOLE FRAME. Circular vignette onto the new world.",
             text=_interleave(["Look in the porthole.", colour + ".", echo + ".", teaser]),
             pause="Make a porthole with your hands. Peek through.",
             grown="A quiet beat. Let it sit three seconds before you turn."),
        dict(kind="story", beat="3 - Arrival", art="The ship coming down into the world.",
             text=_interleave(["Down, down, down.", detail,
                               "The Wonder Ship lands.", f"<i>{sound}</i>"]),
             pause="Wiggle your fingers as we come down.",
             grown=f"Drop to a whisper on <i>{sound.rstrip('.')}</i>."),
        dict(kind="story", beat="3 - Arrival", art="Wide reveal. The whole world at once.",
             text=_interleave([f"We are {s.here}.", "Open your eyes big.", "What do you see?"]),
             pause="Open your eyes wide. Look around.",
             grown="Take every answer. Observation before explanation."),
    ]


BEAT_NAMES = ["4 - Explore A", "4 - Explore A", "4 - MOVEMENT", "4 - MOVEMENT",
              "5 - Explore B", "5 - Explore B", "5 - MOVEMENT", "5 - MOVEMENT",
              "6 - Wonder Moment", "6 - Wonder Moment"]


def build(spec):
    """Spec -> the same page list shape books.py produces for books 1-3."""
    week, slug, title, world, concepts, tag, big = by_week(spec.week)
    pages = ritual_pages(spec.week, spec.pilots[0] + " " + spec.pilots[1],
                         f"{spec.pilots[0]}<br>{spec.pilots[1]}")
    pages += arrival_pages(spec, world)
    for i, b in enumerate(spec.beats):
        pages.append(dict(kind="story", beat=BEAT_NAMES[i], art=b.art or "",
                          text=b.lines, pause=b.pause, grown=b.grown))
    pages += return_pages(spec.home,
                          "Same four beats as page 5. That is how a pattern becomes theirs.")
    pages.append(landing_page(spec.pilots[0], spec.pilots[1], spec.log))
    pages.append(dict(THEME_PAGE))
    assert len(pages) == 22, f"week {spec.week}: {len(pages)} pages, expected 22"
    from worlds import WORLDS
    wd = WORLDS[world]
    return dict(number=week, slug=slug, title=title, world=WORLD_LABEL.get(world, world),
                week=week, world_key=world, concepts=concepts, curriculum=tag, big=big,
                palette=wd.pal(),
                cover_art=f"The Wonder Ship at rest on the classroom carpet, children "
                          f"gathering. A hint of {WORLD_LABEL.get(world, world).lower()} "
                          f"through the window. Title below the ship.",
                pages=pages)


WORLD_LABEL = {
    "reef": "Coral reef", "openocean": "Open ocean", "kelp": "Kelp forest",
    "icewater": "Under the ice", "river": "River", "prehistoric": "Prehistoric",
    "rainforest": "Rainforest", "meadow": "Meadow", "desert": "Desert",
    "arctic": "Arctic", "savanna": "Savanna", "mountain": "Mountain",
    "forest": "Forest", "bamboo": "Bamboo forest", "volcano": "Volcano",
    "cave": "Cave", "mine": "Deep mine", "saltflat": "Salt flat",
    "canyon": "Canyon", "farm": "Farm", "town": "Town", "storm": "Storm cloud",
    "windy": "Windy hills", "aurora": "Northern lights", "space": "Outer space",
    "moon": "The moon", "station": "Space station", "ringed": "Ringed planet",
    "comet": "Comet", "instrument": "Inside an instrument", "body": "Inside the body",
    "studio": "Recording studio", "hall": "Concert hall",
}


def scene_plan(concepts):
    """Pages 11-20 -> a scene key each, alternating concept and partner."""
    out = []
    for c in concepts:
        out.append(c)
        out.append(PARTNER.get(c, "close_up"))
    return out
