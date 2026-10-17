"""4Levels Sports Advisory — every word and fact on the site lives here.

Edit this file, then run:  python3 _build/build.py
(build.py writes the pages; assets.py redraws images and needs Pillow, so run it in the
cloud workspace, not on the Mac.)

SOURCE RULE: every fact below comes from the client's own deck
("4Levels Sports Advisory Client Deck", made 17 Sep 2026, sent by Andrew 17 Oct 2026)
or from Andrew's text of 15 Oct 2026. Bios are the client's own claims, lightly
corrected for spelling only. Nothing is invented. Anything we don't have is marked TODO.
"""

# ---------------------------------------------------------------- switches
# The address the site is served from. Link-preview images must live on THIS host.
# Change it to the real domain at launch, then rebuild.
PUBLIC_URL = "https://4-levels.vercel.app"

# True = hidden from Google (noindex everywhere + a "design preview" bar).
# Flip to False only on launch day.
PRELAUNCH = True

BUILT = "2026-10-17"          # shown in llms.txt / agents.md "last updated"
GEO_ENGAGEMENT_START = "2026-08-16"   # first AI Syndicate work on this site (first draft)

# ---------------------------------------------------------------- the business
NAME = "4Levels Sports Advisory"
SHORT = "4Levels"
SLOGAN = "Enhance. Elevate. Enlighten. Empower."
MISSION = ("4Levels exists at the intersection of performance and purpose: a sports advisory "
           "firm that enhances athletes' foundations, elevates their visibility, enlightens "
           "their perspective, and empowers them to build a legacy that outlasts the game.")
ONE_LINE = ("A basketball-focused sports advisory firm guiding players in high school, college, "
            "the NBA and overseas, on and off the court.")
# TODO (blocked until the client says): email, phone, city/state, social links, domain.
EMAIL = None
PHONE = None
CITY = None

# ---------------------------------------------------------------- the four levels
# Bullets are copied from the deck's "4Levels Framework" slide. The one-line
# explanations under each bullet are ours (Andrew asked us to write them), and
# they describe the area of work only — no results, no promises.
LEVELS = [
    {
        "slug": "enhance", "n": "01", "name": "Enhance", "role": "Your foundation",
        "short": "The work before the game: training, recovery and the habits that hold up over a long career.",
        "long": ("Enhance is the foundation everything else stands on. It covers how an athlete "
                 "trains, how they recover, and the daily habits that keep them available and "
                 "improving, season after season."),
        "photo_note": "Photo to come: a workout with Ro at UCLA.",
        "items": [
            ("Strength & conditioning", "Training that builds the strength and engine the game asks for."),
            ("Skill development", "Focused work on the parts of your game that move you to the next level."),
            ("Nutrition & recovery", "Fueling and recovery habits that keep you on the floor."),
            ("Discipline & daily habits", "The routines that carry you through a long season and a long career."),
        ],
    },
    {
        "slug": "elevate", "n": "02", "name": "Elevate", "role": "Your visibility",
        "short": "Your name, your brand and the deals that come with them.",
        "long": ("Elevate is about being seen the right way. It covers how an athlete shows up "
                 "online and in the media, and how that visibility turns into NIL deals, "
                 "endorsements and partnerships."),
        "photo_note": "Photo to come: Trey working on one of his deals.",
        "items": [
            ("Branding & social media", "A clear personal brand and social channels that help instead of hurt."),
            ("NIL deals & endorsements", "Finding, weighing and closing name, image and likeness deals and endorsements."),
            ("Public relations & media", "Handling press, interviews and public moments."),
            ("Marketing & partnerships", "Connecting with brands that fit who you are, for the long run."),
        ],
    },
    {
        "slug": "enlighten", "n": "03", "name": "Enlighten", "role": "Your perspective",
        "short": "Money, relationships and decisions, understood before they matter.",
        "long": ("Enlighten is the education side of the game. It covers how money works, who "
                 "is worth knowing, and how to read an opportunity or a contract before saying "
                 "yes to it."),
        "photo_note": "Photo to come. Enlighten has no photo yet.",
        "items": [
            ("Financial literacy", "How money works: budgeting, saving and what a paycheck really means."),
            ("Networking & relationships", "Building the relationships that open doors during and after your career."),
            ("Career decision guidance", "Clear thinking for the big calls: schools, teams, transfers and offers."),
            ("Understanding opportunities & contracts", "Knowing what is in front of you, and what it is worth, before you sign."),
        ],
    },
    {
        "slug": "empower", "n": "04", "name": "Empower", "role": "Your legacy",
        "short": "Ownership, wealth and impact that outlast the game.",
        "long": ("Empower looks past the final buzzer. It covers ownership, building wealth, "
                 "giving back to the community, and planning a life after basketball that the "
                 "athlete chooses for themselves."),
        "photo_note": "Photo to come: community work or a camp.",
        "items": [
            ("Business ownership", "Learning what it takes to own and build a business of your own."),
            ("Investing & wealth building", "Understanding how wealth is built, with connections to banking and private wealth management professionals."),
            ("Community impact & philanthropy", "Camps, community work and giving back where it counts."),
            ("Legacy & life after hoops", "A plan for what comes next, made before you need it."),
        ],
    },
]

# Deck slide "NIL Strategy Framework" (the deck numbers it 1, 2, 2, 3, 4, 5;
# it is six steps, numbered correctly here).
NIL_STEPS = [
    ("Valuation & player analysis", "Evaluate market value through performance data, analytics and scouting reports to set positioning and potential."),
    ("Brand positioning", "Define identity, audience and market value to stand out in a crowded NIL landscape."),
    ("Digital presence", "Strengthen social media, content strategy and personal branding to increase visibility and engagement."),
    ("Market outreach", "Connect with brands, collectives and partners to create real NIL opportunities."),
    ("Deal execution", "Structure, negotiate and secure NIL deals that maximize both short-term earnings and long-term value."),
    ("Long-term strategy", "Align NIL opportunities with career goals, professional ambitions and success after basketball."),
]

# Who they serve — each line is supported by the deck (Matt McCall: "committing out of
# high school", transfer portal; Justin Brown: "NBA, college and overseas markets").
AUDIENCE = [
    ("High school prospects", "Players weighing college offers and getting ready to commit."),
    ("College athletes", "NIL, the transfer portal and the step to the pros."),
    ("Pros, NBA & overseas", "Contracts, transitions and the business of a pro career."),
]

# ---------------------------------------------------------------- the team (deck slides 3-7)
TEAM = [
    {
        "slug": "justin-brown", "name": "Justin Brown",
        "role": "NBA Agent · NIL Advisor · Founder & CEO", "job": "Founder & CEO",
        "bio": [
            "Justin Brown specializes in building careers that outlast the game. Founder and CEO of 4Levels Sports Advisory, Justin is certified in NBA and NIL representation and has advised 20+ clients across the NBA, college and overseas markets, guiding athletes through contracts, transitions and the decisions that shape a career.",
            "A former college athlete at the University of South Florida and UAB, where he earned his MBA before becoming a certified NBA agent, Justin knows the representation space from both sides of the table. His mission is straightforward: give this generation of hoopers the experience he and so many before him never got.",
        ],
        "focus": ["NBA + NIL representation", "Contract strategy + negotiation", "Player development", "Brand building + partnerships", "Global marketplace"],
        "founder": True,
    },
    {
        "slug": "david-cline", "name": "David Cline",
        "role": "NIL Advisor · Relocation · Mentorship · Co-Founder", "job": "Co-Founder",
        "bio": [
            "With over 18 years of experience in banking, David has assisted over 100 NBA, NFL, MLB and other professional athletes with real estate lending. David specializes in working with professional athletes, NIL athletes and celebrities on a national scale. His connections run deep into professional athletics, real estate and private equity.",
            "As a co-founder of 4Levels Sports Advisory, David brings a unique résumé to the NIL space. He understands the financial opportunities and challenges athletes face throughout their careers, and his legacy has been built on trust and privacy.",
        ],
        "focus": ["NIL representation", "Financial education + budgeting", "Athlete mentorship", "Banking & private wealth management connections", "Nationwide sports & entertainment network", "Relocation help for transfers, trades & new contracts"],
        "founder": True,
    },
    {
        "slug": "romell-witherspoon", "name": "Romell Witherspoon",
        "role": "Player Development · Leadership · NIL Advisor", "job": "Player Development",
        "bio": [
            "Romell Witherspoon specializes in developing the person behind the player. Founder and CEO of The Confidence Code, Romell equips athletes with the confidence, leadership, discipline and life skills they need to make the most of their careers and prepare for success beyond the game.",
            "A former collegiate athlete and a four-year member of the Los Angeles Lakers organization in player engagement and as team chaplain, he brings firsthand experience supporting athletes through the demands of elite performance.",
        ],
        "focus": ["Athlete + family advisory", "Player development + mentorship", "Confidence + performance mindset", "Personal development", "Career + life transition"],
        "founder": False,
    },
    {
        "slug": "matt-mccall", "name": "Matt McCall",
        "role": "Consultant · Player Development · Connector", "job": "Consultant",
        "bio": [
            "Matt McCall offers 4Levels clients a unique connection to professional and college basketball. With 20 years of Division I coaching experience and two national championships at the University of Florida under Billy Donovan, Matt has deep connections in college basketball and the NBA. He was head coach at UMass from 2017 through 2022, and was named Southern Conference Coach of the Year after leading UT Chattanooga to the NCAA Tournament.",
            "Matt's coaching history lets him advise 4Levels clients entering the transfer portal or committing out of high school. His experience running multiple Division I programs will translate to success on and off the court for 4Levels clients.",
        ],
        "focus": ["Navigating the transfer portal", "NBA & Division I talent evaluations", "College program outreach", "Player development", "Game film analysis"],
        "founder": False,
    },
    {
        "slug": "sophie-siegel", "name": "Sophie Siegel",
        "role": "Marketing & Brand Management", "job": "Head of Marketing",
        "bio": [
            "Sophie Siegel is Head of Marketing and a WNBPA-certified agent with over a decade of experience in athlete representation, brand partnerships and content strategy. She graduated magna cum laude from Syracuse University with a degree in sport management and a minor in marketing.",
            "Sophie has worked with NBA, WNBA and NFL athletes across marketing and full-service representation, with previous roles at Quality Control Sports, OneTeam Partners, the NFLPA and Octagon. Throughout her career she has helped secure partnerships with major brands such as Tostitos, Warner Bros. and Samsung, supporting campaigns for athletes including Sue Bird, Lamar Jackson, Aaron Donald, Travis Kelce, Odell Beckham Jr. and CeeDee Lamb.",
        ],
        "focus": [],   # TODO: the deck has no focus-areas list for Sophie — ask her
        "founder": False,
    },
]

# ---------------------------------------------------------------- clients
# BLOCKED: no client list yet. Each card needs name, hometown, current school or team,
# and a headshot. Leave CLIENTS empty and the page shows clearly marked placeholders.
CLIENTS = []
PLACEHOLDER_CLIENT_CARDS = 6

# ---------------------------------------------------------------- pages
PAGES = [
    {"path": "/", "file": "index.html", "nav": None, "title": "4Levels Sports Advisory | Basketball Sports Advisory & NIL",
     "h": "Home",
     "desc": "4Levels Sports Advisory guides basketball players in high school, college, the NBA and overseas. Enhance. Elevate. Enlighten. Empower."},
    {"path": "/services/", "file": "services/index.html", "nav": "What we do", "title": "Services: The Four Levels | 4Levels Sports Advisory",
     "h": "Services",
     "desc": "The 4Levels framework: Enhance your foundation, Elevate your visibility, Enlighten your perspective and Empower your legacy. Plus our six-step NIL strategy."},
    {"path": "/team/", "file": "team/index.html", "nav": "Our team", "title": "Our Team | 4Levels Sports Advisory",
     "h": "Team",
     "desc": "Meet the 4Levels team: Justin Brown, David Cline, Romell Witherspoon, Matt McCall and Sophie Siegel. NBA, NIL, player development and marketing."},
    {"path": "/clients/", "file": "clients/index.html", "nav": "Our athletes", "title": "Our Athletes | 4Levels Sports Advisory",
     "h": "Our athletes",
     "desc": "The athletes 4Levels Sports Advisory works with, from high school prospects and college players to pros in the NBA and overseas."},
    {"path": "/contact/", "file": "contact/index.html", "nav": "Contact", "title": "Contact | 4Levels Sports Advisory",
     "h": "Contact",
     "desc": "Start a conversation with 4Levels Sports Advisory about NBA and NIL representation, player development and life after basketball."},
]


# ---------------------------------------------------------------- v3: "where are you?" chooser
# Each card sends the visitor to the contact form with their answers already ticked.
# Supported by the deck: high school (Matt McCall: committing out of high school), college
# (NIL, transfer portal), pros (Justin Brown: NBA and overseas), families (Romell: athlete +
# family advisory).
PATHS = [
    {"key": "hs", "title": "High school player", "line": "Weighing offers and getting ready to commit.",
     "role": "An athlete", "level": "High school"},
    {"key": "col", "title": "College athlete", "line": "NIL deals, the transfer portal and the jump to the pros.",
     "role": "An athlete", "level": "College"},
    {"key": "pro", "title": "Pro, NBA or overseas", "line": "Contracts, transitions and the business of a pro career.",
     "role": "An athlete", "level": ""},
    {"key": "fam", "title": "Parent or family", "line": "Guidance for the people behind the player.",
     "role": "A parent or family member", "level": ""},
]

# ---------------------------------------------------------------- v3: plain-answer FAQ (home page)
# Answers use deck facts only; the NIL definition is general knowledge.
FAQ = [
    ("What is 4Levels Sports Advisory?",
     "A basketball sports advisory firm. We help players build their game, their name, their understanding of money and contracts, and a life after basketball. We call those the four levels: Enhance, Elevate, Enlighten and Empower."),
    ("Who do you work with?",
     "High school prospects, college athletes and pros in the NBA and overseas, and their families."),
    ("What is NIL?",
     "NIL stands for name, image and likeness. It means athletes can be paid for things like endorsements, appearances and social media posts. The rules differ by state and by school, so check them before you sign anything."),
    ("Who is on the 4Levels team?",
     "Justin Brown (founder and CEO, a certified NBA agent), co-founder David Cline, Romell Witherspoon, Matt McCall and Sophie Siegel. Their full bios are on the Our team page."),
    ("How do I get started?",
     "Fill in the short form on the contact page. Tell us who you are, your level of play and how to reach you."),
]
