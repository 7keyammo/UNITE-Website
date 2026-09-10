# -*- coding: utf-8 -*-
"""Content data for The Wonder Ship series.

Each page is a dict:
  kind  : title | note | story | theme
  art   : art-direction line shown in the illustration placeholder
  text  : list of story lines (a bare "" makes a blank line)
  pause : the PAUSE cue (story pages only)
  grown : the GROWN-UPS curriculum note (story pages only)
  beat  : which of the 8 template beats this page serves
"""

THEME_PAGE = dict(
    kind="theme",
    art="Four clean icons in a row: clapping hands, clapping hands, hands on knees, a breath swirl. Numbered 1-4.",
    beat="Series theme",
)

NOTE_PAGE = dict(
    kind="note",
    art="Low-color. A single small Wonder Ship icon at the top. Mostly type.",
    beat="Front matter",
)


def ritual_pages(book_no, pilot_line_a, pilot_line_b):
    """Pages 3-6. Identical in all three books by design."""
    return [
        dict(kind="story", beat="1 - Liftoff Ritual",
             art="Children seated on the carpet, hands flat on their chests, eyes closed. "
                 "Ship breath-lights dim. Warm classroom light from one side.",
             text=["The Wonder Ship is sleeping.", "",
                   "To wake her up, we breathe.", "",
                   "Put your hand on your chest.", "",
                   "Breathe in…"],
             pause="Hand on chest. Breathe in.",
             grown="<em>Vibration</em> — EFV Lesson 1, STEAM Class 1. Hands stay on chests for this whole spread."),
        dict(kind="story", beat="1 - Liftoff Ritual",
             art="Same camera position, one beat later. Breath-lights brighter. "
                 "One child smiling with surprise at the buzz.",
             text=["…and breathe <b>out</b>.", "",
                   "Slow. Soft. Warm.", "",
                   "Now hum. Hmmmmmmm.", "",
                   "Did you feel the little buzz?", "",
                   "That is your engine."],
             pause="Breathe out. Hum. Feel the buzz.",
             grown="Every sound starts as a vibration. They just found theirs."),
        dict(kind="story", beat="1 - Liftoff Ritual",
             art="Wide shot of the group, hands mid-clap. Clap-meter on the console showing 1 of 4 lamps lit. "
                 "Slow, heavy, sleepy feeling.",
             text=["Now the claps.", "",
                   "<b>Clap. Clap. Pat. Whoosh.</b>", "",
                   "Slow claps keep her sleepy.", "",
                   "Sloooow… claaap… paaat… whoooosh…"],
             pause="Slow it down. Four beats.",
             grown="The Wonder Ship Clap. A pattern of 4 — STEAM Class 4. Slow tempo, low energy."),
        dict(kind="story", beat="1 - Liftoff Ritual",
             art="Same shot, energy way up. Motion lines on every hand. All 4 clap-meter lamps lit. "
                 + pilot_line_a,
             text=["Faster now. Faster!", "",
                   "Clap! Clap! Pat! Whoosh!", "",
                   pilot_line_b, "",
                   "One — two — three — <b>GO!</b>"],
             pause="Speed up the claps until liftoff.",
             grown="<em>Energy</em> — EFV Lesson 2. Faster, harder claps carry more energy. The children are the engine."),
    ]


def return_pages(direction_lines, mirror_note):
    """Pages 21-22. Mirrors pages 3-6."""
    return [
        dict(kind="story", beat="7 - Return Ritual",
             art="Back inside the ship. Hands on chests. Breath-lights dimming down. "
                 "Direct mirror of page 3 - same composition.",
             text=["Time to go home.", "",
                   "Hand on your chest.", "",
                   "Breathe in…", "",
                   "…and breathe out."],
             pause="Same breath as page 3. Twice.",
             grown="The mirror. This is the regulation tool — the exact move you will reuse at line-up and nap time."),
        dict(kind="story", beat="7 - Return Ritual",
             art="The ship travelling home. Clap-meter fully lit. Direct mirror of page 6.",
             text=["Clap. Clap. Pat. Whoosh.", "",
                   "Faster! Faster!", ""] + direction_lines,
             pause="The Wonder Ship Clap. Slow to fast.",
             grown=mirror_note),
    ]


def landing_page(pilot_a, pilot_b, question):
    return dict(kind="story", beat="8 - Landing",
                art="Classroom carpet again. Ship at rest, breath-lights off. Children animated, talking to each other. "
                    "Mission Log sits in its own framed box.",
                text=["<i>Bump.</i>", "",
                      "We are back.", "",
                      pilot_a, pilot_b, "",
                      "<span class='log'><b>MISSION LOG</b><br>" + question + "</span>"],
                pause="Everyone makes their own sound. Just one.",
                grown="<em>Signature sound</em> — STEAM Class 12. Every child's sound is different. Say that out loud.")


BOOKS = []

# ---------------------------------------------------------------- BOOK 1
BOOKS.append(dict(
    number=1,
    slug="book-01-into-the-deep",
    title="Into the Deep",
    world="Underwater",
    palette=dict(deep="#0b3a4a", mid="#0f6d80", light="#7fd4d8", accent="#ff7a59",
                 sand="#f3e2c0", band="#0b3a4a", bandtext="#d8f3f5"),
    cover_art="The Wonder Ship at rest on the classroom carpet, children gathering around it. "
              "Warm light. Title above the ship.",
    pages=(
        ritual_pages(1,
                     "Mr. Domkam grinning, Mr. Johnson counting on his fingers.",
                     "Mr. Domkam grins. Mr. Johnson counts.")
        + [
            dict(kind="story", beat="2 - Departure",
                 art="Exterior. The ship rising past a classroom window, then birds, then clouds. "
                     "Tall vertical composition, lots of upward motion.",
                 text=["<b>UP</b> goes the Wonder Ship.", "",
                       "Up past the window.", "",
                       "Up past the birds.", "",
                       "Up past the clouds."],
                 pause="Stretch both arms up. Reach.",
                 grown="A big stretch resets the body after the fast claps."),
            dict(kind="story", beat="2 - Departure",
                 art="PORTHOLE FRAME. Circular vignette filling most of the page, solid blue inside it, "
                     "with the faintest hint of something very large.",
                 text=["Look in the porthole.", "",
                       "Blue.", "",
                       "All blue.", "",
                       "Something big and blue is coming."],
                 pause="Make a porthole with your hands. Peek through.",
                 grown="A quiet beat. Let it sit for three seconds before you turn the page."),
            dict(kind="story", beat="3 - Arrival",
                 art="The ship descending through a column of bubbles, settling onto pale sand. "
                     "Light shafts coming down from above.",
                 text=["Down, down, down.", "",
                       "Bubbles tickle the glass.", "",
                       "The Wonder Ship lands soft on the sand.", "",
                       "<i>bloop… bloop… bloop</i>"],
                 pause="Wiggle your fingers like bubbles going up.",
                 grown="Drop to a whisper on <i>bloop</i>. Underwater is a quiet world."),
            dict(kind="story", beat="3 - Arrival",
                 art="Wide reveal. Reef, fish, colour everywhere. The biggest and busiest page in the book.",
                 text=["We are under the sea.", "",
                       "Open your eyes big.", "",
                       "What do you see?"],
                 pause="Open your eyes wide. Look around.",
                 grown="Take every answer. Every answer is right. This is observation — the first science skill."),
            dict(kind="story", beat="4 - Explore A",
                 art="Close on two or three children with hands cupped behind their ears, "
                     "faces concentrating hard.",
                 text=["Put your hands behind your ears.", "",
                       "Cup them. Like this.", "",
                       "Listen."],
                 pause="Cup your hands behind your ears.",
                 grown="<em>Your amazing ears</em> — STEAM Class 7. The outer ear is a dish. Bigger dish, more sound."),
            dict(kind="story", beat="4 - Explore A",
                 art="One small fish drifting past. Muted, soft-edged, almost blurry — "
                     "the art itself should feel muffled.",
                 text=["Down here, sound is slow and sleepy.", "",
                       "Everything sounds far away.", "",
                       "A little fish goes by.", "",
                       "No footsteps. No stomping.", "",
                       "Just… <i>shhhhhh.</i>"],
                 pause="Say <i>shhhhh</i> very softly.",
                 grown="Water carries sound differently than air — heavy, slow, muffled. <em>Medium</em>, EFV Lesson 11."),
            dict(kind="story", beat="4 - MOVEMENT",
                 art="Children mid arm-wave. Draw the wave as an actual wave shape sweeping across the page.",
                 text=["Now <b>swim</b>.", "",
                       "Make a wave with your arm.", "",
                       "Up… and down…", "",
                       "and up… and down…"],
                 pause="Stand up. Wave one arm like a wave.",
                 grown="<em>Waves</em> — EFV Lesson 13. They are drawing a waveform in the air without knowing it."),
            dict(kind="story", beat="4 - MOVEMENT",
                 art="Whole-body waves. The children and the fish move along the same continuous wave line.",
                 text=["That is how sound moves.", "",
                       "Wave. Wave. Wave.", "",
                       "Swim it slow.", "",
                       "Swim it with two arms.", "",
                       "Swim it with your whole body!"],
                 pause="Whole-body wave. Slow.",
                 grown="Big slow waves are low and loud. Say it if you like — they meet the words again in Kindergarten."),
            dict(kind="story", beat="5 - Explore B",
                 art="A tiny shrimp with an enormous, sharp-edged sound burst exploding out of one claw. "
                     "Maximum contrast.",
                 text=["<b>CLICK!</b>", "",
                       "A tiny shrimp snaps his claw.", "",
                       "Such a big sound", "",
                       "from such a little friend."],
                 pause="Snap or clap once. Loud!",
                 grown="<em>Loud and soft</em> — STEAM Class 2. Small body, big energy."),
            dict(kind="story", beat="5 - Explore B",
                 art="Same shrimp, now buried in sand. The sound burst is small and fuzzy-edged. "
                     "Compose it as a direct comparison to the previous page.",
                 text=["Then he hides in the soft, soft sand.", "",
                       "Click…", "",
                       "Now it is tiny.", "",
                       "Soft things eat sound."],
                 pause="Clap once with soft, floppy hands.",
                 grown="<em>Absorption</em> — EFV Lesson 12, STEAM Class 14. Soft material soaks up sound energy."),
            dict(kind="story", beat="5 - MOVEMENT",
                 art="Split composition. Left: a big clap, bold and sharp. Right: a tiny clap, small and soft.",
                 text=["Your turn!", "",
                       "<b>BIG</b> clap — BOOM!", "",
                       "<b>tiny</b> clap — soft.", "",
                       "Big. Tiny. Big. Tiny."],
                 pause="Four claps. Big, tiny, big, tiny.",
                 grown="<em>Amplitude</em> — EFV Lesson 4. Same hands. Different size of vibration."),
            dict(kind="story", beat="5 - MOVEMENT",
                 art="Whale tail stomping on the left half, seahorse tiptoeing on the right half. "
                     "Children mirroring each one.",
                 text=["Now stomp like a big whale tail.", "",
                       "<b>BOOM!</b>", "",
                       "Now tiptoe like a seahorse.", "",
                       "<i>tip. tip. tip.</i>", "",
                       "Same feet. Different size."],
                 pause="Two big stomps. Six tiny tiptoes.",
                 grown="“Same feet, different size” is amplitude in five words. Reuse that line all year."),
            dict(kind="story", beat="6 - Wonder Moment",
                 art="QUIET PAGE. Near-navy. One enormous, slow whale silhouette, far away. "
                     "Almost no detail anywhere. The children are small in the frame.",
                 text=["Then…", "", "everything", "", "goes", "", "still.", "",
                       "<b>Hoooooooooo.</b>", "",
                       "A whale is singing."],
                 pause="Nobody moves. Just listen.",
                 grown="Hold this silence a full five seconds. Do not rush it. This is the heart of the book."),
            dict(kind="story", beat="6 - Wonder Moment",
                 art="Close and warm. A child's hand flat on their own chest, the whale visible through "
                     "the porthole behind them. A soft glow travelling between the two.",
                 text=["Put your hand on your chest.", "",
                       "Hum with her.", "",
                       "<b>Hoooooooooo.</b>", "",
                       "Feel that?", "",
                       "Her song is inside you now."],
                 pause="Hand on chest. Hum low and long with the whale.",
                 grown="<em>Resonance</em> — EFV Lesson 9. One vibration starts another thing vibrating. Their chest is the other thing."),
        ]
        + return_pages(["Up through the blue.", "", "Up, up, <b>UP!</b>"],
                       "Same four beats as page 5. Third time today. That is how a pattern becomes theirs.")
        + [
            landing_page("Mr. Domkam smiles.", "Mr. Johnson claps once.",
                         "What did the whale feel like inside you?"),
            dict(THEME_PAGE),
        ]
    ),
))

# ---------------------------------------------------------------- BOOK 2
BOOKS.append(dict(
    number=2,
    slug="book-02-among-the-stars",
    title="Among the Stars",
    world="Outer space",
    palette=dict(deep="#171a4a", mid="#3b3a8c", light="#a9a6f2", accent="#ffd166",
                 sand="#f5f0ff", band="#171a4a", bandtext="#e4e2ff"),
    cover_art="The Wonder Ship at rest on the classroom carpet at night, children gathering. "
              "Stars visible through the classroom window. Title above the ship.",
    pages=(
        ritual_pages(2,
                     "Mr. Johnson checking the sky through the porthole, Mr. Domkam counting.",
                     "Mr. Johnson checks the sky.<br>Mr. Domkam counts.")
        + [
            dict(kind="story", beat="2 - Departure",
                 art="Exterior. The ship climbing past roof, birds, clouds, then the top of the sky. "
                     "Five clear altitude bands stacked vertically.",
                 text=["<b>UP</b> goes the Wonder Ship.", "",
                       "Up past the roof.", "",
                       "Up past the birds.", "",
                       "Up past the clouds.", "",
                       "Up past the sky."],
                 pause="Stretch both arms up. Reach higher on each “up.”",
                 grown="Five ups, five reaches. Build the stretch each time."),
            dict(kind="story", beat="2 - Departure",
                 art="PORTHOLE FRAME. Circular vignette, solid black inside, scattered with gold sparkles.",
                 text=["Look in the porthole.", "",
                       "Black.", "",
                       "All black.", "",
                       "And… sparkles."],
                 pause="Make a porthole with your hands. Peek through.",
                 grown="A quiet beat. Three seconds before turning."),
            dict(kind="story", beat="3 - Arrival",
                 art="The ship suspended, motionless, no ground anywhere. Engine glow fading out. "
                     "Everything very still.",
                 text=["The engine goes quiet.", "",
                       "No bump.", "",
                       "No landing.", "",
                       "We just… float."],
                 pause="Go completely still. Freeze.",
                 grown="Stillness right after motion. Notice who can hold it — that is self-regulation developing."),
            dict(kind="story", beat="3 - Arrival",
                 art="Wide reveal. Stars, planets, colour. The biggest and busiest page in the book.",
                 text=["We are in space.", "",
                       "Open your eyes big.", "",
                       "What do you see?"],
                 pause="Open your eyes wide. Look around.",
                 grown="Take every answer. Observation before explanation."),
            dict(kind="story", beat="4 - Explore A",
                 art="One tiny bright star, drawn small and sharp, with quick tight little sound rings "
                     "packed close together around it.",
                 text=["Look! A tiny, tiny star.", "",
                       "Tiny stars sing <b>high</b>.", "",
                       "<i>eee — eee — eee</i>"],
                 pause="Sing high with the tiny star. <i>eee!</i>",
                 grown="<em>Frequency</em> — EFV Lesson 3. Fast vibration sounds high."),
            dict(kind="story", beat="4 - Explore A",
                 art="One enormous slow star with wide, far-apart sound rings. "
                     "Deliberate visual opposite of the previous page.",
                 text=["Look! A big, big star.", "",
                       "Big stars sing <b>low</b>.", "",
                       "<i>ohhhhhhhhhh</i>"],
                 pause="Sing low with the big star. <i>ohhh.</i>",
                 grown="Slow vibration sounds low. Same voice, different speed. That is the whole idea."),
            dict(kind="story", beat="4 - MOVEMENT",
                 art="Children reaching up tall on the high note and curled down small on the low note, "
                     "drawn side by side so the height difference reads instantly.",
                 text=["Reach up high — sing high!", "",
                       "<i>eee!</i>", "",
                       "Curl down low — sing low!", "",
                       "<i>ohhh.</i>", "",
                       "High. Low. High. Low."],
                 pause="Four times. Reach and curl.",
                 grown="Body height mapped to pitch. Pure EFV Lesson 3 — and it works on three-year-olds."),
            dict(kind="story", beat="4 - MOVEMENT",
                 art="Hands wiggling fast with tight motion lines beside hands waving slow with wide "
                     "loose lines. Mr. Johnson conducting.",
                 text=["Now wiggle your hands fast.", "",
                       "Fast wiggle — high sound!", "",
                       "Now wave them slow.", "",
                       "Slow wave — low sound!", "",
                       "Your body is the dial."],
                 pause="Wiggle fast = high. Wave slow = low.",
                 grown="They are operating a frequency control. Hold your own hand up and conduct them."),
            dict(kind="story", beat="5 - Explore B",
                 art="A child stepping out of the hatch and immediately drifting. "
                     "No up, no down — tip the whole composition off-axis.",
                 text=["Step out. Careful!", "",
                       "There is no <b>down</b> here.", "",
                       "You float."],
                 pause="Take one very slow step.",
                 grown="Slow-motion movement is hard. It builds control, not just energy release."),
            dict(kind="story", beat="5 - Explore B",
                 art="Mr. Johnson floating upside down, glasses staying put. "
                     "Mr. Domkam turning in a slow circle, scarf drifting.",
                 text=["Mr. Johnson floats upside down.", "",
                       "Mr. Domkam floats in a slow, slow circle.", "",
                       "Float with them."],
                 pause="Arms wide. Turn slowly in one circle.",
                 grown="Vestibular input. One circle only, then stop and steady."),
            dict(kind="story", beat="5 - MOVEMENT",
                 art="Three children mid-float-step, arms wide, drawn as a numbered 1-2-3 sequence "
                     "across the page.",
                 text=["<b>Float!</b>", "",
                       "Arms wide. Sloooow.", "",
                       "One… slow… step.", "",
                       "Two… slow… step.", "",
                       "Three… slow… step."],
                 pause="Three slow floating steps.",
                 grown="Counting to three while moving. Numeracy hidden inside gross motor."),
            dict(kind="story", beat="5 - MOVEMENT",
                 art="A child crouched low, then the same child high above the ground mid-jump, "
                     "then drifting down slowly. Three stages, one page.",
                 text=["Now a <b>moon jump</b>!", "",
                       "Bend down low…", "",
                       "and… <b>BOING!</b>", "",
                       "You go so high.", "",
                       "You come down so <i>slow</i>."],
                 pause="Three moon jumps. Land soft.",
                 grown="Big proprioceptive input. This is the energy-release page — spend time here."),
            dict(kind="story", beat="6 - Wonder Moment",
                 art="THE DARKEST, EMPTIEST PAGE IN THE SERIES. Almost nothing. "
                     "A few distant stars, the children very small and very still. No sound graphics at all.",
                 text=["Now stop.", "", "Listen.", "", ".", "", ".", "", ".", "",
                       "<b>Nothing.</b>"],
                 pause="Total silence. Five seconds.",
                 grown="<em>Vacuum</em> — EFV Lesson 11, STEAM Class 11. Space is empty; sound has nothing to travel through. Do not fill this page with words."),
            dict(kind="story", beat="6 - Wonder Moment",
                 art="Close on one child, hand on chest, eyes closed, with a warm glow "
                     "travelling <em>inward</em> through their own body — not outward into space.",
                 text=["Space is empty.", "",
                       "Sound needs something to swim through.", "",
                       "But hum — <b>hmmmmm</b> —", "",
                       "and you hear it.", "",
                       "Because <b>you</b> are something."],
                 pause="Hand on chest. Hum. You can hear yourself.",
                 grown="Sound travels through solids — including the child's own bones. It is the one sound that works in space, and they carry it."),
        ]
        + return_pages(["Down through the sparkles.", "", "Down, down, <b>DOWN!</b>"],
                       "Note the flip — Book 1 goes UP to come home, Book 2 comes DOWN. Ask them why.")
        + [
            landing_page("Mr. Johnson smiles.", "Mr. Domkam claps once.",
                         "What did the quiet in space sound like?"),
            dict(THEME_PAGE),
        ]
    ),
))

# ---------------------------------------------------------------- BOOK 3
BOOKS.append(dict(
    number=3,
    slug="book-03-back-to-the-dinosaurs",
    title="Back to the Dinosaurs",
    world="Prehistoric",
    palette=dict(deep="#1f3d1e", mid="#4a7c3f", light="#b9d99a", accent="#d98555",
                 sand="#f4ead3", band="#1f3d1e", bandtext="#e6f2d8"),
    cover_art="The Wonder Ship at rest on the classroom carpet, a large friendly dinosaur shadow "
              "falling across the wall behind it. Children gathering. Title above the ship.",
    pages=(
        ritual_pages(3,
                     "Mr. Domkam holding on tight to a handrail, Mr. Johnson counting.",
                     "Mr. Domkam holds on tight.<br>Mr. Johnson counts.")
        + [
            dict(kind="story", beat="2 - Departure",
                 art="Exterior. The ship rising, then streaking BACKWARDS through layered bands of time. "
                     "Horizontal motion, not vertical — deliberately unlike Books 1 and 2.",
                 text=["<b>UP</b> goes the Wonder Ship.", "",
                       "But not up to the sky.", "",
                       "Up… and <b>back</b>.", "",
                       "Back and back and back."],
                 pause="Stretch up, then lean back. Slow.",
                 grown="Time travel instead of space travel. Same liftoff, different direction. Ask them what “back” means."),
            dict(kind="story", beat="2 - Departure",
                 art="PORTHOLE FRAME. Circular vignette packed with green, and one large shape moving "
                     "behind the leaves.",
                 text=["Look in the porthole.", "",
                       "Green.", "",
                       "So much green.", "",
                       "And something is <b>moving</b>."],
                 pause="Make a porthole with your hands. Peek through.",
                 grown="A quiet beat. Three seconds."),
            dict(kind="story", beat="3 - Arrival",
                 art="The ship settling into grass taller than itself. Fronds brushing the glass. "
                     "Dappled green light.",
                 text=["Down, down, down.", "",
                       "Leaves brush the glass.", "",
                       "The Wonder Ship lands in the tall, tall grass.", "",
                       "<i>crunch.</i>"],
                 pause="Wiggle your fingers like tall grass.",
                 grown="Whisper “crunch.” The jungle is loud, but you arrive quiet."),
            dict(kind="story", beat="3 - Arrival",
                 art="Wide reveal. Dinosaurs, ferns, volcano on the horizon. "
                     "The biggest and busiest page in the book.",
                 text=["We are with the dinosaurs.", "",
                       "Open your eyes big.", "",
                       "What do you see?"],
                 pause="Open your eyes wide. Look around.",
                 grown="Take every answer."),
            dict(kind="story", beat="4 - Explore A",
                 art="Close on small hands pressed flat on the ground. Faces waiting, concentrating. "
                     "Nothing else on the page yet.",
                 text=["Put your hands flat on the ground.", "",
                       "Wait.", "", ".", "", ".", "",
                       "Do you feel that?"],
                 pause="Both palms flat on the floor. Wait. Be still.",
                 grown="<em>Energy through solids</em> — EFV Lessons 2 and 11. Sound travels through the floor faster than through the air."),
            dict(kind="story", beat="4 - Explore A",
                 art="Rings of vibration spreading through the GROUND toward the children's hands "
                     "from a huge foot at the page edge. The dinosaur is mostly off-frame.",
                 text=["<b>BOOM. BOOM. BOOM.</b>", "",
                       "Something big is coming.", "",
                       "The ground is talking", "",
                       "to your hands."],
                 pause="Keep hands down. Feel three booms.",
                 grown="“The ground is talking to your hands” is your reusable line for vibration all year."),
            dict(kind="story", beat="4 - MOVEMENT",
                 art="Children stomping, each stomp numbered 1, 2, 3, 4 with a burst under the foot.",
                 text=["Stand up!", "",
                       "<b>STOMP!</b>", "",
                       "BOOM. BOOM. BOOM. BOOM.", "",
                       "Count them:", "",
                       "one, two, three, four."],
                 pause="Four big stomps. Count out loud.",
                 grown="<em>Counting vibrations</em> — EFV Lesson 6, STEAM Class 4. Four beats, same as the Wonder Ship Clap."),
            dict(kind="story", beat="4 - MOVEMENT",
                 art="Top half: four widely spaced stomp bursts. Bottom half: eight tightly packed ones. "
                     "The doubling should be visible at a glance.",
                 text=["Now stomp <b>twice as fast</b>!", "",
                       "boom-boom-boom-boom-boom-boom-boom-boom", "",
                       "Whee!", "",
                       "Now slow.", "",
                       "Big and slow again."],
                 pause="Eight fast stomps, then four slow.",
                 grown="<em>Doubling</em> — EFV Lesson 10. Four became eight. They will meet this again as octaves."),
            dict(kind="story", beat="5 - Explore B",
                 art="The largest dinosaur in the book, one foot landing, enormous shock ring "
                     "spreading out across the whole page.",
                 text=["Here is the <b>biggest</b> dinosaur.", "",
                       "Her step is huge.", "",
                       "<b>BOOOOOM.</b>"],
                 pause="One giant stomp. As big as you can.",
                 grown="<em>Amplitude</em> — EFV Lesson 4. A big vibration."),
            dict(kind="story", beat="5 - Explore B",
                 art="A tiny dinosaur beside the big one's footprint, making three small "
                     "shock rings. Same ground, drawn identically — only the rings change size.",
                 text=["Here is the <b>littlest</b> dinosaur.", "",
                       "His step is tiny.", "",
                       "<i>tip. tip. tip.</i>", "",
                       "Same ground. Different size."],
                 pause="Six tiny tiptoes.",
                 grown="Same ground, same feet, different size of vibration. Amplitude, separate from speed."),
            dict(kind="story", beat="5 - MOVEMENT",
                 art="Children alternating: one huge stomp pose, one tiny tiptoe pose, repeating "
                     "across the page like a pattern strip.",
                 text=["Be the big one.", "",
                       "<b>BIG STOMP!</b>", "",
                       "Be the little one.", "",
                       "<i>tiny tiptoe.</i>", "",
                       "Big. Tiny. Big. Tiny."],
                 pause="Alternate four times.",
                 grown="Force grading. The hardest skill on this page is the <i>tiny</i> one."),
            dict(kind="story", beat="5 - MOVEMENT",
                 art="A big dinosaur with a low, wide, heavy sound shape and a small one with a "
                     "high, tight, spiky sound shape. Children copying both.",
                 text=["Now <b>roar</b>!", "",
                       "A big roar is low —", "",
                       "<b>RRRRAAAWWWR.</b>", "",
                       "A little roar is high —", "",
                       "<i>eek! eek!</i>", "",
                       "Try both."],
                 pause="One low roar. Three high squeaks.",
                 grown="<em>Frequency</em> again — EFV Lesson 3. Big animal, low sound. They already believe this; now they have done it."),
            dict(kind="story", beat="6 - Wonder Moment",
                 art="QUIET PAGE. A wide pale canyon opening up, huge sky, tiny figures. "
                     "Mr. Domkam very small at the edge with his hands cupped. Nearly empty composition.",
                 text=["Mr. Domkam cups his hands", "",
                       "and calls to the mountain:", "",
                       "<b>HEL-LOOOO!</b>", "",
                       "Wait.", "",
                       "<i>hel-loooo… hel-loooo… hel-loooo</i>"],
                 pause="Cup your hands. Call out. Then wait and listen.",
                 grown="<em>Acoustics and echo</em> — STEAM Class 9. The wait is the magic. Do not talk into it."),
            dict(kind="story", beat="6 - Wonder Moment",
                 art="The children calling out, with their voices drawn arcing across to the canyon wall "
                     "and bouncing back, fainter each time.",
                 text=["The mountain caught his voice", "",
                       "and threw it back.", "",
                       "Try it.", "",
                       "Say your name to the mountain.", "",
                       "It knows your name now."],
                 pause="Each child calls their own name. Everyone echoes it back softly.",
                 grown="The class becomes the mountain. Echo each name three times, quieter each time. This is the emotional peak of the book."),
        ]
        + return_pages(["Forward through the green.", "", "Home, home, <b>HOME!</b>"],
                       "Book 1 went up, Book 2 came down, Book 3 goes forward. Three directions, one clap.")
        + [
            landing_page("Mr. Domkam laughs.", "Mr. Johnson claps once.",
                         "What did the mountain say back to you?"),
            dict(THEME_PAGE),
        ]
    ),
))
