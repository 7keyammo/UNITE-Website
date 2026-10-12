# -*- coding: utf-8 -*-
"""UNITE STEAM facts, carried over from the members site.

Single source of truth for everything the free site states about the
organization, its programs and its prices. The figures and wording come from
unite-steam/ (lib/plans.ts, lib/shelves.ts, app/page.tsx, app/pricing,
app/saturday-school, app/privacy, app/terms) so the two sites cannot disagree.
Change a price here and on lib/plans.ts together.
"""

ORG = dict(
    name="UNITE STEAM",
    expand="Unique Natives Interacting Together Elevating",
    tagline="Building stronger communities, one step at a time.",
    lede="An Afrocentric, youth-led future grounded in truth, love, and science. "
         "Learn at home with the Homeschool Hub, join us in person at Saturday "
         "School, or work with us on a curriculum built for your family or "
         "organization.",
    mission="UNITE supports people in underserved and low-income communities "
            "through education, unity, and progress, building skills, boosting "
            "learning, and creating strong futures.",
    place="Oakland, California",
    email="unitehella@gmail.com",     # already published on unitehella.org
    org_site="https://unitehella.org",
)

IMPACT = [
    ("275", "youth served in a typical year"),
    ("75%", "average gain in STEM confidence"),
    ("90%", "report a lift in cultural pride"),
    ("1,200+", "instructional hours delivered"),
]
IMPACT_NOTE = "From UNITE’s Impact Hub at unitehella.org."

PROGRAMS = [
    dict(icon="school", name="Saturday School", href="saturday-school.html",
         text="Weekly in-person STEAM sessions in Oakland with Mr. Domkam and "
              "Mr. Johnson. Hands-on, movement-rich, and tied to the Hub so "
              "learning continues at home.",
         go="Explore Saturday School"),
    dict(icon="ship", name="STEAM Curriculum", href="books.html",
         text="The Homeschool Hub: the Wonder Ship read-aloud series for ages 5 "
              "and under today, with more age shelves on the way.",
         go="Open the library"),
    dict(icon="seed", name="Community Projects", href="pricing.html#custom",
         text="Lab work, building planter boxes, hip-hop and more. Real projects "
              "that connect STEAM to neighborhood life.",
         go="Get involved"),
]

CUSTOM = [
    ("Personalized curriculum",
     "A consultation-based curriculum built for your child, with regular check-ins."),
    ("Private tutoring", "A one-on-one version of Saturday School."),
    ("For organizations",
     "Curriculum development for schools, nonprofits and youth programs."),
]

LADDER = [
    ("Community & open content",
     "Free digital content from UNITE, plus a space where homeschool parents can "
     "post and share their own tasks and activities.", "Free / low cost"),
    ("Saturday School",
     "Weekly in-person STEAM sessions in Oakland, led by our teachers. Includes "
     "full Homeschool Hub access.", "Includes tier 1 + Homeschool Hub"),
    ("Personalized homeschool curriculum",
     "An ongoing consultation. We build and tune a curriculum for your child, "
     "with regular check-ins.", "Consultation"),
    ("Private tutoring",
     "A one-on-one version of Saturday School: the same ritual and hands-on "
     "approach, just for your child.", "1:1 sessions"),
    ("Curriculum development for organizations",
     "We design STEAM curriculum for schools, nonprofits and youth programs, "
     "drawing on the UNITE STEAM method.", "Custom / contract"),
]

CADENCES = [("monthly", "Monthly", "/mo", 1),
            ("semester", "Semester", "/semester", 6),
            ("annual", "Annual", "/yr", 12)]

PLANS = [
    dict(key="homeschool", name="Homeschool Hub", featured=False,
         blurb="Full digital book library, guided Read mode and homeschool tasks.",
         price=dict(monthly=14, semester=75, annual=120),
         features=["All Wonder Ship books, plus every age shelf as it launches",
                   "Fullscreen guided Read mode for projector, laptop or tablet",
                   "Post and browse community homeschool tasks"]),
    dict(key="saturday", name="Saturday School", featured=True,
         blurb="Weekly in-person sessions in Oakland, plus everything in Homeschool Hub.",
         price=dict(monthly=89, semester=420, annual=750),
         features=["Weekly Saturday session with our teachers",
                   "Small cohorts of about 10 students",
                   "Everything in Homeschool Hub included",
                   "Progress notes shared with parents"]),
]

PRICE_NOTE = ("Saturday School always includes everything in Homeschool Hub. "
              "Semester plans cover 6 months; longer commitments cost less per "
              "month. Cancel anytime from your account.")

SATURDAY = dict(
    kicker="In person · Oakland",
    lede="Weekly hands-on STEAM sessions, led live by Mr. Domkam and Mr. Johnson. "
         "Every Saturday School seat includes full Homeschool Hub access, so "
         "families get the in-person energy and the at-home follow-through together.",
    running_title="Saturday pilot sessions at Circuit Launch",
    running=["Small-group pilot cohorts meeting at Circuit Launch in Oakland, "
             "building toward a dedicated UNITE STEAM classroom space.",
             "Each session mirrors the Wonder Ship ritual: calm the ship, power it "
             "up, travel somewhere new, explore hands-on, and land together."],
    meta=["Saturdays", "Circuit Launch, Oakland", "About 10 students per cohort"],
    included=["A seat in the weekly in-person session",
              "Full Homeschool Hub access (all books and tasks)",
              "Progress shared with parents after each session",
              "Priority access as new age shelves launch"],
    seatnote="After you join, we email you to confirm your cohort and start date.",
)

STEPS = [
    ("Pick your path", "Homeschool Hub, Saturday School, or a custom offering."),
    ("Create your account",
     "A parent or guardian holds the account. Members log in to reach the library."),
    ("Choose a plan",
     "Pay monthly, by semester, or annually. Longer costs less per month."),
    ("Start learning",
     "The Hub opens right away, and we confirm your Saturday School seat by email."),
]

SHELVES = [
    dict(name="5 & under", sub="The Wonder Ship book series", on=True,
         count="{n} books · 20–30 min each", href="books.html"),
    dict(name="Pre-teen", sub="Coming soon", on=False, count="0 items",
         note="Once the 5-and-under series is finished, this shelf holds the "
              "pre-teen curriculum and titles."),
    dict(name="Teenager", sub="Coming soon", on=False, count="0 items",
         note="Reserved for teen-level UNITE STEAM content."),
    dict(name="Young adult", sub="Coming soon", on=False, count="0 items",
         note="Reserved for young-adult UNITE STEAM content."),
    dict(name="Beyond", sub="Coming soon", on=False, count="0 items",
         note="Reserved for adult and lifelong-learning content."),
]

LEGAL_NOTE = ("Draft for review before launch. Have this checked by someone "
              "qualified for your situation.")

PRIVACY = [
    ("Who holds the account",
     ["UNITE STEAM accounts are held by a parent, guardian or organization "
      "contact. Children do not create accounts or log in, and we do not ask for "
      "children’s names, birthdates, photos or contact details through this site."]),
    ("What we collect",
     ["<ul><li>Account details: your email address and a password (stored securely "
      "by our authentication provider, Supabase).</li>"
      "<li>Membership details: your plan, billing period and subscription status.</li>"
      "<li>Payments: handled by Stripe. We never see or store your full card number.</li>"
      "<li>Forms: the name, email, age range and interests you send through our "
      "registration and contact forms.</li></ul>"]),
    ("How we use it",
     ["To give members access to what they paid for, to confirm Saturday School "
      "seats, to reply to your questions, and to send occasional updates you asked "
      "for. We do not sell your information."]),
    ("Your choices",
     ["You can cancel your plan anytime from your account. To have your account "
      "and data deleted, contact us and we will remove it."]),
    ("Contact",
     ["UNITE, Oakland, California. Email "
      "<a href='mailto:unitehella@gmail.com'>unitehella@gmail.com</a>."]),
]

TERMS = [
    ("Memberships",
     ["Homeschool Hub and Saturday School are subscriptions billed monthly, every "
      "six months (semester), or yearly. Saturday School includes Homeschool Hub "
      "access. Plans renew automatically until cancelled."]),
    ("Cancelling",
     ["You can cancel anytime from your account. Access continues until the end of "
      "the period you have paid for."]),
    ("Saturday School",
     ["Sessions run in person in Oakland. Cohorts are small, about 10 students. We "
      "confirm your cohort and start date by email after you join. A parent or "
      "guardian is responsible for drop-off and pick-up."]),
    ("Content",
     ["The Wonder Ship books and other library content are for your household’s own "
      "learning. Please don’t share your login or redistribute the material."]),
    ("Changes",
     ["We may update prices or these terms. We will tell members by email before a "
      "price change affects them."]),
]
