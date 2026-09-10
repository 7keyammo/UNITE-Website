# -*- coding: utf-8 -*-
"""The school year: 50 weekly Wonder Ship books.

PLAN is the whole year — destination, world, the six concept beats each book
carries, and the K-2 lessons it feeds. It is the contract the weekly bot works
against: it reads the next unwritten week, authors that book's words, and the
engine does the rest.

Concept keys come from scenes.CONCEPTS. Each book uses five:
  two discovery beats, two movement beats, and the wonder moment.
"""

# week, slug, title, world, [5 concepts], curriculum tag, the big feeling
PLAN = [
 (1,  "book-01-into-the-deep",        "Into the Deep",           "reef",
      ["listen", "wave", "two_sizes", "two_sizes", "resonance"],
      "EFV L1,L9,L12 · STEAM C2,C7", "Sound can be soft, slow and muffled"),
 (2,  "book-02-among-the-stars",      "Among the Stars",         "space",
      ["two_speeds", "two_speeds", "travel", "travel", "silence"],
      "EFV L3,L11 · STEAM C11", "Sound can be absent — and you still carry your own"),
 (3,  "book-03-back-to-the-dinosaurs","Back to the Dinosaurs",   "prehistoric",
      ["feel_ground", "count", "two_sizes", "two_speeds", "echo"],
      "EFV L2,L4,L6,L10 · STEAM C9", "Sound can be enormous, and the world answers back"),
 (4,  "book-04-the-rainforest-roof",  "The Rainforest Roof",     "rainforest",
      ["listen", "layers", "two_speeds", "count", "hero"],
      "EFV L3 · STEAM C10", "Many voices can sing at once"),
 (5,  "book-05-under-the-ice",        "Under the Ice",           "icewater",
      ["feel_ground", "travel", "absorb", "wave", "silence"],
      "EFV L11,L12 · STEAM C11", "Sound travels through solid things"),
 (6,  "book-06-the-desert-night",     "The Desert Night",        "desert",
      ["silence", "listen", "two_sizes", "count", "resonance"],
      "EFV L4 · STEAM C2,C7", "The quietest place still has sound in it"),
 (7,  "book-07-inside-a-cave",        "Inside a Cave",           "cave",
      ["echo", "listen", "two_sizes", "travel", "echo"],
      "STEAM C9 · EFV L9", "Your voice can come back to you"),
 (8,  "book-08-the-windy-meadow",     "The Windy Meadow",        "meadow",
      ["listen", "wave", "two_speeds", "count", "hero"],
      "EFV L3,L13", "You can hear something you cannot see"),
 (9,  "book-09-the-thunder-cloud",    "The Thunder Cloud",       "storm",
      ["silence", "feel_ground", "two_sizes", "count", "travel"],
      "EFV L2,L11 · STEAM C11", "Light comes first, then the sound catches up"),
 (10, "book-10-the-volcano-island",   "The Volcano Island",      "volcano",
      ["feel_ground", "two_sizes", "count", "two_sizes", "hero"],
      "EFV L2,L4", "The biggest rumble you can feel in your feet"),
 (11, "book-11-the-coral-city",       "The Coral City",          "reef",
      ["layers", "listen", "two_speeds", "wave", "resonance"],
      "STEAM C10,C12", "Everyone's sound is different, and together they are new"),
 (12, "book-12-the-bamboo-forest",    "The Bamboo Forest",       "bamboo",
      ["resonance", "listen", "two_speeds", "count", "hero"],
      "EFV L9 · STEAM C3", "Hollow things sing when you tap them"),
 (13, "book-13-the-frozen-waterfall", "The Frozen Waterfall",    "arctic",
      ["two_speeds", "silence", "travel", "wave", "resonance"],
      "EFV L3,L11", "Fast water is loud, slow water is soft"),
 (14, "book-14-the-beehive",          "The Beehive",             "meadow",
      ["two_speeds", "count", "double", "listen", "hero"],
      "EFV L3,L6,L10", "Fast wings make a high sound"),
 (15, "book-15-the-bird-market",      "The Bird Market",         "rainforest",
      ["layers", "two_speeds", "count", "listen", "hero"],
      "EFV L3 · STEAM C10,C12", "High voices carry the furthest"),
 (16, "book-16-the-whale-road",       "The Whale Road",          "openocean",
      ["listen", "travel", "two_speeds", "wave", "resonance"],
      "EFV L3,L11 · STEAM C11", "A low song can cross a whole ocean"),
 (17, "book-17-the-singing-sands",    "The Singing Sands",       "desert",
      ["feel_ground", "listen", "two_sizes", "wave", "hero"],
      "EFV L1,L2", "The ground itself can hum"),
 (18, "book-18-the-old-clock-tower",  "The Old Clock Tower",     "town",
      ["count", "double", "two_speeds", "travel", "resonance"],
      "EFV L6,L10 · STEAM C4", "A steady beat is a kind of counting"),
 (19, "book-19-the-train-yard",       "The Train Yard",          "town",
      ["count", "travel", "two_speeds", "layers", "hero"],
      "EFV L6 · STEAM C4,C10", "Wheels make a rhythm you can march to"),
 (20, "book-20-the-drum-village",     "The Drum Village",        "savanna",
      ["count", "two_sizes", "layers", "double", "resonance"],
      "STEAM C3,C4,C10 · EFV L10", "The first instrument was a body"),
 (21, "book-21-the-rice-paddy",       "The Rice Paddy",          "river",
      ["listen", "travel", "count", "layers", "hero"],
      "STEAM C10 · EFV L6", "Call out, and something calls back"),
 (22, "book-22-the-night-garden",     "The Night Garden",        "meadow",
      ["silence", "listen", "count", "two_speeds", "resonance"],
      "EFV L3,L6 · STEAM C7", "The dark is full of tiny sounds"),
 (23, "book-23-the-cliff-of-birds",   "The Cliff of Birds",      "mountain",
      ["layers", "two_sizes", "listen", "count", "hero"],
      "STEAM C2,C10", "A thousand voices are still made of one voice"),
 (24, "book-24-the-deep-mine",        "The Deep Mine",           "mine",
      ["feel_ground", "travel", "echo", "listen", "silence"],
      "EFV L2,L11 · STEAM C9", "Sound moves faster through rock than through air"),
 (25, "book-25-the-salt-flat",        "The Salt Flat",           "saltflat",
      ["silence", "echo", "two_sizes", "wave", "resonance"],
      "STEAM C9 · EFV L4", "Flat and empty makes your voice sound enormous"),
 (26, "book-26-the-rope-bridge",      "The Rope Bridge",         "canyon",
      ["feel_ground", "wave", "two_speeds", "travel", "echo"],
      "EFV L1,L13 · STEAM C11", "A shake can travel along a rope"),
 (27, "book-27-behind-the-waterfall", "Behind the Waterfall",    "river",
      ["absorb", "listen", "two_sizes", "travel", "resonance"],
      "EFV L12 · STEAM C14", "Water can hide a sound"),
 (28, "book-28-the-windmill-hill",    "The Windmill Hill",       "windy",
      ["two_speeds", "count", "double", "wave", "hero"],
      "EFV L3,L6,L10", "Turning faster makes a higher hum"),
 (29, "book-29-the-glass-house",      "The Glass House",         "town",
      ["echo", "two_sizes", "listen", "travel", "resonance"],
      "STEAM C9 · EFV L9", "Hard walls throw sound back at you"),
 (30, "book-30-the-wool-market",      "The Wool Market",         "town",
      ["absorb", "two_sizes", "listen", "count", "silence"],
      "EFV L12 · STEAM C14", "Soft things drink sound up"),
 (31, "book-31-the-space-station",    "The Space Station",       "station",
      ["silence", "feel_ground", "travel", "count", "resonance"],
      "EFV L11 · STEAM C11", "With no air, you listen with your hands"),
 (32, "book-32-the-moon-garden",      "The Moon Garden",         "moon",
      ["silence", "two_speeds", "count", "wave", "hero"],
      "EFV L3,L11", "Slow and light is its own kind of music"),
 (33, "book-33-the-comet-tail",       "The Comet Tail",          "comet",
      ["two_speeds", "travel", "double", "count", "hero"],
      "EFV L3,L10", "Fast things go by before you hear them"),
 (34, "book-34-the-ringed-planet",    "The Ringed Planet",       "ringed",
      ["wave", "count", "double", "two_speeds", "resonance"],
      "EFV L10,L13 · STEAM C4", "Big circles turn slowly and hum low"),
 (35, "book-35-the-red-planet",       "The Red Planet",          "canyon",
      ["silence", "absorb", "echo", "two_sizes", "hero"],
      "EFV L11,L12", "Thin air makes a thin sound"),
 (36, "book-36-the-ice-moon",         "The Ice Moon",            "icewater",
      ["silence", "feel_ground", "travel", "listen", "resonance"],
      "EFV L11 · STEAM C11", "Cold, hard and quiet — but not silent underneath"),
 (37, "book-37-the-suns-song",        "The Sun's Song",          "aurora",
      ["two_sizes", "layers", "two_speeds", "wave", "hero"],
      "EFV L2,L4", "Energy can arrive as light and as warmth"),
 (38, "book-38-the-aurora",           "The Aurora",              "aurora",
      ["silence", "wave", "two_speeds", "layers", "resonance"],
      "EFV L13 · STEAM C6", "Sometimes you can see energy moving"),
 (39, "book-39-the-meteor-shower",    "The Meteor Shower",       "space",
      ["count", "double", "two_speeds", "travel", "hero"],
      "EFV L6,L10 · STEAM C4", "Quick bright beats, one after another"),
 (40, "book-40-the-big-quiet",        "The Big Quiet",           "space",
      ["silence", "listen", "resonance", "wave", "silence"],
      "EFV L11 · STEAM C11", "The biggest quiet there is, and your own hum inside it"),
 (41, "book-41-inside-a-guitar",      "Inside a Guitar",         "instrument",
      ["resonance", "two_speeds", "wave", "count", "hero"],
      "EFV L1,L3,L9", "A string is quiet until it has a box to shout into"),
 (42, "book-42-inside-a-drum",        "Inside a Drum",           "instrument",
      ["feel_ground", "two_sizes", "count", "double", "resonance"],
      "EFV L1,L4,L6 · STEAM C3", "A drum is a skin that shakes"),
 (43, "book-43-inside-a-flute",       "Inside a Flute",          "instrument",
      ["two_speeds", "wave", "count", "listen", "resonance"],
      "EFV L3,L13", "Air can sing if you give it a shape"),
 (44, "book-44-inside-your-ear",      "Inside Your Ear",         "body",
      ["listen", "travel", "two_sizes", "wave", "resonance"],
      "STEAM C7 · EFV L1", "You have a tiny drum inside your head"),
 (45, "book-45-inside-your-chest",    "Inside Your Chest",       "body",
      ["feel_ground", "count", "two_speeds", "silence", "resonance"],
      "EFV L1,L6 · STEAM C13", "Your heart has been keeping a beat all along"),
 (46, "book-46-the-choir-hall",       "The Choir Hall",          "hall",
      ["layers", "two_speeds", "resonance", "two_sizes", "hero"],
      "STEAM C10,C12 · EFV L9", "Many voices can become one sound"),
 (47, "book-47-the-dance-floor",      "The Dance Floor",         "hall",
      ["count", "double", "two_sizes", "layers", "wave"],
      "STEAM C4,C6 · EFV L10", "Your body already knows where the beat is"),
 (48, "book-48-the-parade",           "The Parade",              "town",
      ["count", "travel", "layers", "two_sizes", "hero"],
      "STEAM C4,C10", "Music that walks down the street"),
 (49, "book-49-the-recording-room",   "The Recording Room",      "studio",
      ["listen", "count", "double", "layers", "silence"],
      "STEAM C5,C10 · EFV L6", "A sound can be caught and played again"),
 (50, "book-50-the-big-showcase",     "The Big Showcase",        "hall",
      ["layers", "count", "two_sizes", "two_speeds", "resonance"],
      "ALL · STEAM C15 · EFV L15", "Everything we learned, all at once, with nothing but us"),
]

TERMS = [
    (1, 10, "Term 1 · Feeling sound", "Vibration, energy and the body as an instrument"),
    (11, 20, "Term 2 · Fast, slow, big, small", "Frequency and amplitude as two separate dials"),
    (21, 30, "Term 3 · Where sound goes", "Travel, echo, absorption and acoustics"),
    (31, 40, "Term 4 · Out where there is no air", "Waves, vacuum and energy you can see"),
    (41, 50, "Term 5 · Inside the instrument", "Resonance, the body, and the showcase"),
]


def by_week(n):
    for row in PLAN:
        if row[0] == n:
            return row
    raise KeyError(n)


def term_of(week):
    for a, b, name, blurb in TERMS:
        if a <= week <= b:
            return name, blurb
    return "", ""


if __name__ == "__main__":
    import worlds
    print(f"{len(PLAN)} weeks planned")
    missing = sorted({r[3] for r in PLAN} - set(worlds.WORLDS))
    print("worlds referenced but missing:", missing or "none")
    import scenes
    bad = sorted({c for r in PLAN for c in r[4]} - set(scenes.CONCEPTS))
    print("concepts referenced but missing:", bad or "none")
    for a, b, name, _ in TERMS:
        print(f"  {name}: weeks {a}-{b}")
