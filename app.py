from flask import Flask, request, render_template_string

from difflib import get_close_matches


app = Flask(__name__)

# Hardcoded dictionary for demonstration purposes
english_nuer_dict = {
    "African Bermudagrass": "buɔk",
    "African fish eagle": "kue̱y",
    "African spoonbill": "jak thok pur",
    "afternoon": "cäŋdäär",
    "agree": "mat",
    "alcohol": "kɔaŋ",
    "alcoholic beverage": "kɔaŋ",
    "also": "bä",
    "ambush": "bi̱i̱m",
    "and": "kä",
    "and (third person primary conjunct)": "kɛnɛ",
    "and (first person primary conjunct)": "kɔnɛ",
    "and (second person primary conjunct)": "yɛnɛ",
    "angel": "jääk",
    "ankle": "kuɔc",
    "another": "dɔ̱diɛn",
    "ant": "ŋiɛc",
    "appear": "jɔc",
    "aquatic grass (used to make mats)": "guɔ̱t",
    "are; were": "kɛ",
    "area before the door of a house": "bäŋ",
    "arm": "wuɔ̱ɔ̱k",
    "armpit": "rɔ̱th",
    "army": "rɛm",
    "arrow": "bäär",
    "ash": "ŋɛ̈th",
    "ask about": "thiec",
    "assemble": "dol",
    "at": "kä",
    "attack": "mam",
    "automobile": "thurbil",
    "autumn": "tɔ̱t",
    "awaken": "ker",
    "axe": "jo̱p",
    "baby": "ruɔɔr",
    "back": "jɔk",
    "back tooth": "ro̱k",
    "bad thing": "jieek",
    "bag": "ki̱i̱th",
    "bagger": "li̱i̱m",
    "ball": "kurɛ",
    "bamboo": "lɔu",
    "banana": "möth",
    "baobab": "duɔ̱ny",
    "Bar (member of the Bar tribe)": "ba̱r",
    "barn": "luak",
    "basket": "ɣo̱th",
    "battle": "ko̱r",
    "be": "ben",
    "be afraid": ["dual", "ga̱a̱c"],
    "be alone": "can",
    "be aroused (of men)": "ta̱t",
    "be dark": "cuɔl",
    "be poor": "can",
    "be pregnant with": "ruet",
    "be straight": "cuŋ",
    "be strong": "bum",
    "be surprised": "ga̱a̱c",
    "be tired": "cuc",
    "bead": "tik",
    "bead (made from ostrich eggshell)": "duɔɔŋ",
    "bean": "ŋɔ̱a̱r",
    "beast": ["le̱y", "lɛt"],
    "beat": "duäc",
    "bedding": "ko̱l",
    "beet": "uaar",
    "beg": "lim",
    "behave badly towards": "jäny",
    "behead": "guur",
    "bell": "löth",
    "belly": "bap",
    "belly button": "lo̱k",
    "belongings": ["duŋ", "ni̱n"],
    "belt": "laak",
    "bend": ["tot", "goŋ"],
    "beside": "thok",
    "big": "diit",
    "bird": ["dit", "jal"],
    "bite": "kac",
    "black ant": "cɔ̱k",
    "black-capped avocet; pied avocet": "nyarial gɛr",
    "black-crowned night-heron": "kën ŋo̱k",
    "black-headed heron": "ŋo̱k tik yua̱k",
    "black-winged stilt": "kët yier",
    "blacksmith plover": "kët rɛc",
    "blade": "reet",
    "bless": "puɔth",
    "blood": "riɛm",
    "blue crane": "yiël wɛɛc",
    "boast about (something)": "liɛk",
    "boast to (someone)": "liɛk",
    "boat": "riey",
    "body": "puɔ̱ny",
    "body decoration": "wuɔ̱t",
    "bone": "cɔ̱a̱a̱",
    "bonfire": "gɔl",
    "book": "bok",
    "border": "ke̱e̱y",
    "boss around": "cuɔ̱k",
    "bottom": "thar",
    "bow": "rɔɔc",
    "bow to": "goŋ",
    "bowl (traditional)": "tuɔk",
    "bowl lyre": "thom",
    "boy": ["dhɔl", "dho̱l"],
    "boyfriend/girlfriend": "luum",
    "bracelet": "ciɛk",
    "brain": "ŋith",
    "branch": "kaar",
    "branch, dry": "tɛ̈ɛ̈",
    "bread": "juray",
    "break (pencil or maize-like objects)": "to̱l",
    "break off": "puny",
    "breast": "thi̱n",
    "breath": "yiëë",
    "breeze": "li̱i̱r",
    "brew": "bim",
    "bride": "kaw",
    "bring": "nööŋ",
    "bring back to life": "tek",
    "bring together": "dol",
    "broadleaf fig": "kuel",
    "brook": "lil",
    "broom": "yi̱ec",
    "brother, his/her/its": "däman",
    "brother, my": "dämaar",
    "brown-backed honeybird": "tol",
    "buffalo": "mo̱k",
    "buffalo fly": "ruɔ̱m",
    "build with grass": "dit",
    "build with mud": "täth",
    "building": "ti̱c",
    "bull": "tuut",
    "bullfrog": "thiɛp",
    "bunch": "liny",
    "burn (hair, skin)": "rɔl",
    "burrow": "ɣo̱t",
    "burst": "pät",
    "bury": "kuɔny",
    "but": "kä",
    "butter": "liɛɛth",
    "buttock": ["wɔ̱th", "thar"],
    "by": ["ɛ", "thok"],
    "calf": ["dɔw", "kɔ̱a̱l"],
    "call": "cɔl",
    "caller": "cio̱o̱t",
    "camel": "thɔ̱rɔ̱l",
    "canal": "tɛ̈t",
    "cancer": "liir",
    "cane": "yɔ̱t",
    "canine tooth": "ka̱p",
    "car": "thurbil",
    "carry horizontally": "gɔn",
    "carry on head": "kap",
    "cat (WN)": "kuɔ̱ɔ̱t",
    "catch": "käp",
    "catfish": ["yew", "cuur"],
    "cattle": "dɛl",
    "cattle camp": "wec",
    "cattle egret": "kën yaŋ",
    "celebrate": "ŋar",
    "ceremonial scar": "pia̱a̱r",
    "chain": "kuat",
    "chair": "kɔm",
    "change": ["gɛr", "yek"],
    "chase": "joc",
    "cheek (EN)": "jio̱m",
    "cheek (WN)": "tha̱ŋ",
    "cheetah": "thɔ̱a̱a̱n",
    "chest": "kaw",
    "chicken": "manpalɛ̈k",
    "chief": "kuäär",
    "child": "gat",
    "chin": "ti̱k",
    "choose": "kuɛny",
    "circumcise": "cuɛl",
    "claim back": "tɛt",
    "clap": "pat",
    "clavicle": "pet",
    "clay": "tuäk",
    "clean": "gɛth",
    "click tongue at when thinking": "cuit",
    "clock": "thaak",
    "cloth": "bi̱i̱y",
    "cloud": ["pɔ̱a̱r", "po̱o̱l", "ti̱k"],
    "coffee": "bun",
    "coin": "yiëëth",
    "collector": "duul",
    "colour": "biɛl",
    "come": ["ben", "luny"],
    "come back": "luny",
    "compensate": "col",
    "compete": "köŋ",
    "competition": "kööŋ",
    "complain about": "cic",
    "conch shell": "kaaŋ",
    "container (for grain or dura)": "yi̱ɛɛr",
    "container (for storing grain)": "tuäc",
    "conversation": "mɔŋ",
    "cook": ["thäät", "thal"],
    "cooking pot (large)": "dhaar",
    "cooking pot (small)": "bul",
    "cormorant": "lip",
    "corn": "manytap",
    "corner (between the wall and the roof)": "thöl",
    "cotton": "lath",
    "cough": "kiɛl",
    "count": "kuɛn",
    "country": "ro̱o̱l",
    "court": "luk",
    "cover": "kum",
    "cow": "yaŋ",
    "cow byre": "luak",
    "cow hide": "ko̱l",
    "coward": "buɔc",
    "crack": "rɛ̈ɛ̈t",
    "craving": "gi̱i̱r",
    "creator": "cääk",
    "cricket": "diɛɛr",
    "crockery": "kuak",
    "crocodile": "nyaŋ",
    "crocodile bird; Egyptian plover": "guicpiw",
    "cross over": "bäl",
    "crowd": "buɔ̱n",
    "crowned plover": "nyaguic piw",
    "crumble (food)": "puɔ̱t",
    "crumple (clothes)": "coŋ",
    "crush": ["ɣo̱p", "dɔany"],
    "cry about": ["wi̱k", "ro̱t"],
    "cup": "yio̱m",
    "cut": ["ŋuɔ̱k", "ba̱k"],
    "dance": "dɔny",
    "darkness": "muth",
    "date": "thɔ̱w",
    "date seed": "tɔac",
    "day": ["cäŋ", "ni̱en"],
    "Dead Sea apple": "pak",
    "deaf": "miŋ",
    "deafness": "mi̱i̱ŋ",
    "debt": "ŋua̱l",
    "decorate": "bil",
    "deer": "kɛ̈w",
    "Deng": "Dɛŋ",
    "deny": "gak",
    "depression": "ti̱el",
    "desert date": "thɔ̱w",
    "die": "li̱w",
    "dig": "pur",
    "dip under water": "buɔny",
    "disease": "liir",
    "dishes": "kuak",
    "disturb (someone)": "jut",
    "divide": "dääk",
    "divorce": "da̱k",
    "divorced woman": "kɛ̈ɛ̈",
    "doctor": "kim",
    "dodge": ["kɔl", "buɔny", "ric"],
    "dog": "jio̱k",
    "Dok (member of the Dok tribe)": "dɔak",
    "donkey": ["muul", "kacik"],
    "door": "thi̱i̱k",
    "door post": "thuɔk duel",
    "doum palm": "lel",
    "dove": "guuk",
    "dream": ["läk", "la̱k"],
    "drink": ["rueth", "math"],
    "drinking": "mäth",
    "drive": "gɛɛr",
    "drop (of liquid)": "nyuɛ̈r",
    "drought": "rɛ̈ɛ̈th",
    "drown": "mɔc",
    "drum": "bul",
    "drump": "pɔ̱t",
    "drunkard": "ɣo̱ŋ",
    "dung": "wäär",
    "dung heap": "gɔl",
    "dura": "beel",
    "dust": "coth",
    "dustbin": "di̱r",
    "dwelling": "cieŋ",
    "ear": "ji̱th",
    "ear piercing (for a wedding)": "bo̱r",
    "earth": ["mun", "piny"],
    "earwax": "ciɛl",
    "eat": ["cam", "mi̱th"],
    "eat cartilages off (bone)": "joc",
    "eat dry food": "mɔm",
    "eat watery food": "rueth",
    "eat without being invited": "guiɛc",
    "ebb (of river)": "dɔ̱n",
    "edge": "pek",
    "eel": "riel",
    "egg": "tuɔɔŋ",
    "eggshell": "köm",
    "eight": "bädäk",
    "eighteen": "wäl bädäk",
    "elbow": "ci̱el",
    "elect": "kuɛny",
    "election": "kuaany",
    "elephant": "guɔ̱r",
    "eleven": "wäl kɛl",
    "empty land": "pan",
    "enclose": "göl",
    "enclosure": "kal",
    "encourage": ["com", "bum"],
    "environment": "ɣɔw",
    "evening": "thiaŋ",
    "excrement": "ceth",
    "exist": "te",
    "exodus": "ɣööth",
    "extinguish": "yeny",
    "eye": "waŋ",
    "face": "nhiam",
    "fall": "tɛth",
    "fall in love": "bɛɛc",
    "fame": "ko̱k",
    "famine": "buɔth",
    "fancy": "bɛɛc",
    "farm": "kak",
    "fast": "thɛk",
    "fat (of animal or human)": "kɔl",
    "father, his/her/its": "gua̱n",
    "father, my": "gua̱a̱r",
    "fatten": "dho̱k",
    "feather": "jua̱t",
    "feed": "mi̱eth",
    "fence": "kal",
    "fever tree": "kɔaar",
    "field": "kak",
    "fifteen": "wäl dhieec",
    "fifty": "jiɛn da̱ŋ dhieec",
    "fight with hands": "NO FORM",
    "fill with": "pik",
    "fin": "miɛth",
    "finger": "yɛ̈t",
    "fingernail": "riöp",
    "finish": "thuk",
    "fire": "mac",
    "firefly": "miit",
    "firewood": "tɔaŋ",
    "firstborn": "kɛ̱̈ɛ̱̈",
    "fish": ["rec", "mac"],
    "fish (sp.)": "ti̱el",
    "fish scale": "kuac",
    "fish with net": "dɛp",
    "fisherman": "deep",
    "fishing blade": "rip",
    "fishing hook": "cibat",
    "five": "dhieec",
    "flag": "bɛɛr",
    "flame": "bo̱l",
    "flee": "put",
    "float": "thɔr",
    "floating device": "thiɛɛk",
    "flood": "nyɔc",
    "floor": "do̱r",
    "flour": "do̱o̱k",
    "fly": "luaŋ",
    "foam": "guɔ̱ɔ̱p",
    "focus particle": "ni",
    "fold": ["ban", "mat"],
    "follow": "guur",
    "food": ["kuän", "mi̱eth"],
    "food lover (WN)": "cuer",
    "foot": "cio̱o̱k",
    "for": "ɛ",
    "foreigner": "jur",
    "forest": "rup",
    "forty": "jiɛn da̱ŋ ŋuaan",
    "forty eight": "jiɛn da̱ŋ ŋuaan wi̱cdɛ bädäk",
    "forty five": "jiɛn da̱ŋ ŋuaan wi̱cdɛ dhieec",
    "forty four": "jiɛn da̱ŋ ŋuaan wi̱cdɛ ŋuaan",
    "forty nine": "jiɛn da̱ŋ ŋuaan wi̱cdɛ bäŋuan",
    "forty one": "jiɛn da̱ŋ ŋuaan wi̱cdɛ kɛl",
    "forty seven": "jiɛn da̱ŋ ŋuaan wi̱cdɛ bärɔw",
    "forty six": "jiɛn da̱ŋ ŋuaan wi̱cdɛ bäkɛl",
    "forty three": "jiɛn da̱ŋ ŋuaan wi̱cdɛ diɔ̱k",
    "forty two": "jiɛn da̱ŋ ŋuaan wi̱cdɛ rɛw",
    "four": "ŋuaan",
    "fourteen": "wäl ŋuaan",
    "fresh wind": "li̱i̱r",
    "friend": "määth",
    "frighten": "par",
    "frog": "guɛk",
    "front of body": "nhiam",
    "front tooth": "ley",
    "fruit": "dɔw",
    "fruit tree": "bua̱w",
    "future auxiliary": "bi",
    "gallbladder": "kɛɛth",
    "gazelle": "kɛ̈w",
    "get frightened": "par",
    "ghost": "jɔak",
    "gift": "muc",
    "giraffe": "guec",
    "girl": "nyal",
    "give": ["ka̱m", "muɔc"],
    "give orders to": "cuɔ̱k",
    "give way": "guëny",
    "go": ["wä", "räth"],
    "goat": ["dɛl", "bo̱w"],
    "god": "kuɔth",
    "Goliath heron": "ŋo̱k rɛc",
    "good": "gɔa",
    "good thing": "gɔɔy",
    "goose": "tuɔ̱t",
    "gourd": ["keer", "diaar"],
    "grain": "mɔany",
    "grape": "pomacethiŋ",
    "grass": ["dut", "waar", "juac", "muɔ̱ɔ̱th", "lum"],
    "grasshopper": "rak",
    "grave": "kɔ̱a̱a̱k",
    "graze": "laak",
    "great egret": "kën ka̱w ka̱w",
    "great grey shrike": "lɛ̈ɛ̈m",
    "greater flamingo": "jak yier",
    "greater honeyguide": "kɛ̈c",
    "greet": ["ner", "kɔŋ"],
    "grey heron": "go̱k wijua̱t",
    "grey-crowned crane": "riak",
    "grey-leaved cordia": "nyuot",
    "grieve": "par",
    "grind": "gwär",
    "grinding stone": "pil",
    "grow": "pith",
    "gum": ["niäär", "nyär"],
    "gum acacia": "ki̱r",
    "gun": "mac",
    "hair": "mi̱em",
    "hammer": ["puɔ̱ɔ̱t", "dey"],
    "hammer in": "pɔ̱a̱t",
    "hammerkop": "do̱p gɛɛl",
    "hand": "tet",
    "hare": "pɛl pɛl",
    "harvest": ["ŋër", "to̱l"],
    "hat": "kum",
    'haul': "yɔ̱c",
    "haul": "yɔ̱c",
    "have": "te",
    "have diarrhoea": "ci̱th",
    "hawk": "käät",
    "head": "wi̱c",
    "head support": "cääk",
    "hear": "liŋ",
    "heart": "lɔc",
    "heartwood": "buɔ̱ɔ̱tlɔac",
    "heel": "ŋuɔ̱l",
    "heifer": "nac",
    "hello": "maalɛ",
    "helmeted guineafowl": "guɔŋ",
    "help": "luäk",
    "hen": "manpalɛ̈k",
    "her": "jɛ",
    "herd": "dɛ",
    "hide": "tɛ̱̈ɛ̱̈",
    "hill": "rɛl",
    "him": "jɛ",
    "hip": "lɛ̈t",
    "hip joint": "juɔɔl",
    "hippo": ["rɔw", "informal"],
    "hippopotamus": "rɔw",
    "his": "dɛ",
    "hoe": ["to̱o̱k", "puur"],
    "hoe handle": "cɔp",
    "hole": ["kɔ̱a̱a̱k", "ɣo̱t"],
    "home": ["wic", "cieŋ"],
    "homestead": "dhɔr",
    "hoof, part of": "mio̱t",
    "hoopoe": "nyakuoth-gɛɛr",
    "horn": "tuŋ",
    "house": ["jiath", "esp. for women duel"],
    "hug": "bom",
    "hunger": "buɔth",
    "hunt": "kak",
    "hunter": "kääk",
    "husband": "cɔw",
    "hut": "ɣo̱t",
    "hyena": "yak",
    "I": "ɣän",
    "include": "mat",
    "infant": "ruɔɔr",
    "insect": ["kɔ̱m", "WN ti̱i̱y"],
    "insert": "cuɔth",
    "inside": "rɛy",
    "invade": "mäk",
    "is; am; was": ["ɛ", "a"],
    "island, small": "pul",
    "it": "jɛ",
    "its": "dɛ",
    "jackal": "wan",
    "jar": "cuk",
    "Jok": "Jɔk",
    "judge": "luk",
    "jump over": "yor",
    "Kang": "Kaŋ",
    "kayak door": "duaany",
    "keep": "tɔ̱w",
    "kick": "kuɛt",
    "kidnap": "pɛc",
    "kidney": "ruɔk",
    "kill": ["näk", "in secret luc"],
    "king": ["kuäär", "rue̱e̱c"],
    "knee": "muɔ̱l",
    "knife": "ŋɔ̱m",
    "knock on": "dɔŋ",
    "know": "ŋa̱c",
    "kob antelope": "thi̱l",
    "kuɔl cucumber": "kuɔl",
    "labour push": "cɔt",
    "lake": ["pul", "large bar"],
    "land": "ro̱o̱l",
    "large intestine": "cuɔt",
    "lazy": ["talaŋ", "nyuɔ̱n"],
    "leaf of a tree": "ji̱thjiath",
    "learn": "ŋi̱ec",
    "leash": "dep",
    "leave and come back": "jɛn",
    "leave for": "yek",
    "leech": "cuɛɛy",
    "left hand": "cam",
    "leg": "cio̱o̱k",
    "Lek (member of the Lek tribe)": "lëk",
    "leopard": "kuac",
    "let": "jak",
    "letter": "warɛgak",
    "lick": "bɛl",
    "lie to": "ka̱a̱ŋ",
    "lightning": "biɛɛr",
    "limp": "thiëp",
    "lion": "lony",
    "listen to": "liŋ",
    "little egret": "kën yier",
    "liver": "cueny",
    "living area (for men)": "kät",
    "lizard": ["roor", "kërkër"],
    "lobby": "bäŋ",
    "location": "gua̱a̱th",
    "lock": ["gäk", "ga̱a̱k"],
    "loft bed": "dhaŋ",
    "look at": "guic",
    "lord": "kuäär",
    "lose": "bath",
    "louse": "nyɔ̱a̱k",
    "love": "nhɔk",
    "lover": "luum",
    "Low (member of the Low tribe)": "lɔaa",
    "lower part of an object": "thar",
    "lung": "puɔ̱th",
    "mad person in the street": "ɣo̱ŋ",
    "maggot": "lɔ̱a̱t",
    "make equal": "pa̱r",
    "make noise about": "ro̱t",
    "make rotten": "bol",
    "make sit": "guɔ̱l",
    "make sleep": "tɔ̱a̱c",
    "make smelly": "bol",
    "make someone pregnant": "ruet",
    "make stand": "cuŋ",
    "make swim": "kët",
    "make tribal marks": "ga̱r",
    "make warm": "ɔl",
    "man": "wut",
    "manage": "guir",
    "marabou": "kiɛl",
    "march (person)": "cuɔ̱k",
    "marry": "kuɛn",
    "mate (animals)": "tut",
    "me": "ɣä",
    "meat": "ri̱ŋ",
    "medicine (for illness)": "wäl",
    "meerkat": "gor",
    "meet joyfully": "kɔŋ",
    "metal implement or tool": "yiëëth",
    "metal ornament": "ciɛk",
    "milk": ["cak", "ŋa̱c"],
    "milk tooth": "nyiɛm",
    "mirror": "neen",
    "miss (target)": "dui̱r",
    "misuse": "riɛw",
    "moan about": "cic",
    "money": "yiëëth",
    "monkey": "gɔɔk",
    "month": "pay",
    "moon": "pay",
    "morning": "runwaŋ",
    "mortar": "ko̱u",
    "mosquito": "nyi̱i̱th",
    "mother, his/her/its": "man",
    "mother, my": "maar",
    "mould": "täth",
    "mountain": "päm",
    "mourn": "par",
    "mouth": "thok",
    "move": ["woc", "guëny"],
    "movement": "ɣööth",
    "mud, hard clump of": "do̱l",
    "mudbowl": "thak",
    "mudfish": "luth",
       "name": "ciöt",
    "narrate": "ca̱t",
    "nation": ["ro̱o̱l", "wec"],
    "navel": "lo̱k",
    "neck": "ŋuäk",
    "need": ["go̱r", "ro̱t"],
    "needle": "lipɛ",
    "nerve": "ra̱a̱l",
    "night": "wäär",
    "nightjar": "nyaŋlew",
    "Nile perch": "cäl",
    "nine": "bäŋuan",
    "nineteen": "wäl bäŋuan",
    "no": "ɣëëy",
    "nose": "wum",
    "numeral classifier": "da̱ŋ",
    "Nyaluaak": "Nyaluaak",
    "observe": "tit",
    "offspring": "dɔw",
    "one": "kɛl",
    "onion (wild)": "lɛ̈ɛ̈w",
    "open": "lɛp",
    "open living space with a fireplace": "gɛ̈w",
    "operate on": "rɛt",
    "or": "kiɛ",
    "order around": "cuɔ̱k",
    "orphan": "rɛɛt",
    "ostrich": "wuut",
    "other": "dɔ̱diɛn",
    "owl": ["murguc", "gumut"],
    "ox": ["thäk", "larger do̱r"],
    "oystercatcher": "jiec thok-jak",
    "palm tree": "no̱r",
    "pancreas": "tak",
    "paper": "warɛgak",
    "paperbark acacia": "ŋuer",
    "part": "guɛny",
    "path": "duɔ̱ɔ̱p",
    "pay back (money)": "pik",
    "peace": "mal",
    "peanut": "tɔŋpiny",
    "pearl": "dɔ̱k",
    "pebble": "guɛɛ",
    "peek under at": "guŋ",
    "peel soft skin": "ŋat",
    "peg": "lo̱c",
    "pelican": "bo̱ŋ",
    "perfective auxiliary": "ci",
    "person": "raan",
    "pestle": "lɛk",
    "photograph": "thur",
    "pick from tree": "pon",
    "picture": "thuurɛ",
    "piece of dry fish": "ka̱r",
    "pied crow": "jakɔ̱k",
    "piercing (of an ear, etc.)": "mut",
    "pig": "kundur",
    "pillow, traditional": "cääk",
    "pipe (for smoking)": "tony",
    "pit": ["kɔ̱a̱a̱k", "large cuk"],
    "pitcher": "liɛɛr",
    "place": "gua̱a̱th",
    "placenta": "lap",
    "plait": "tak",
    "plaster": ["nyath", "with mud ruɛth"],
    "play": "ŋar",
    "plot of cleared land": "yiɔ̱p",
    "pocket": "ki̱i̱th",
    "point in time": "gua̱a̱th",
    "poison": "luɛ̈ŋ",
    "pond grass": "tuytuy",
    "porcupine": "rum",
    "porridge": ["puɔr", "kuän"],
    "port": "wadh",
    "pot (traditional)": "cuk",
    "potato": "tac",
    "pound": "ɣɔ̱l",
    "pour": "woc",
    "pray": "pal",
    "problem": ["ri̱ɛk", "riɛk"],
    "property": ["duŋ", "ni̱n"],
    "prophet": "gök",
    "prostitute": "lër",
    "protector": "gääŋ",
     "pumpkin": ["kɔlɔŋ", "munyjo̱k"],
    "punch": "pi̱m",
    "pupil (of the eye)": "ti̱eey",
    "push": ["thuc", "ɣɔk"],
    "push (heavy items)": "thi̱c",
    "put": "la̱th",
    "put aside": "cak",
    "python": "nyäl",
    "quarrel": "rɔaal",
    "queen": "kuäär mään",
    "question": "thiec",
    "raft": "thiɛɛk",
    "rain": "nhiaal",
    "rainbow": "mi̱i̱t",
    "rat": "kun",
    "razor": "reet",
    "reach": "cop",
    "read": "kuɛn",
    "receive": "käp",
    "reclaim": "tɛt",
    "red": "lual",
    "red acacia": "luɔr",
    "red-knobbed coot": "kuey lual yier",
    "refuse": "lo̱k",
    "relationship": "maar",
    "relax": "lɔ̱ŋ",
    "remove": ["guur", "gɛth"],
    "repeat": "loc",
    "resumptive pronoun": "ɔ",
    "resuscitate": "tek",
    "return": "luny",
    "rhinoceros": "kiɛl",
    "Rialgieer": "Rialgiɛɛr",
    "rib": "nyet",
    "rice": "ruth",
    "rifle": "mac",
    "right hand": "cuec",
    "ring (ornamental)": "tiɛl",
    "rinse in mouth": "lok",
    "rip": "rɛ̈ɛ̈t",
    "river": "yier",
    "river bend where the water is calm": "waŋ",
    "river tide": "mɔak",
    "river, large": "kir",
    "road": ["caar", "duɔ̱ɔ̱p"],
    "roan antelope": "mɔ̱m",
    "roaring": "ro̱tdä",
    "roast": "bol",
    "rob": "mac",
    "rock": "päm",
    "roll": "ric",
    "room": "duel",
    "root of a plant (fine)": "mɛ̈ɛ̈c",
    "rope": ["rɔk", "for tying cattle dep"],
    "rubbish": "thɔc",
    "run": ["riŋ", "wuɔ̱r", "ŋuɔc"],
    "run away": "put",
    "rust": "kɛɛth",
        "sacred garlic pear": "kɛ̈c",
    "sacred ibis": "rumputh",
    "saddle-billed stork": "rial bɛɛk",
    "sadness": "ti̱el",
    "saliva": "ruɛy",
    "sand": "liɛt",
    "save": "tɔ̱a̱w",
    "say": ["lat", "ri̱t"],
    "scarify": "ga̱r",
    "school": "duelgɔ̱ɔ̱rä",
    "scorpion": ["gith", "jith"],
    "sea": "bar",
    "secret": "tɛ̱̈ɛ̱̈",
    "secretary bird": "bolwi̱cjua̱t",
    "see": "nɛn",
    "seed": "kuɛ̈ɛ̈",
    "send": "ja̱k",
    "separate": "da̱k",
    "September": "laath",
    "serpent": "thɔ̱l",
    "serve": ["wuc", "tɔk"],
    "sesame": "nyuɔ̱m",
    "set free": "lony",
    "seven": "bärɔw",
    "seventeen": "wäl bärɔw",
    "sew": ["kɔc", "ɣɔ̱n"],
    "shadow": "ti̱eep",
    "shake by making small movements": "tiɛŋ",
    "she": "jɛn",
    "sheep": ["rɔaam", "dɛl"],
    "shell": "cöm",
    "shift": "woc",
    "Shilluk (member of the Shilluk tribe)": "tɛ̈t",
    "shine": "tɛ̈ɛ̈l",
    "shin bone": "ko̱m",
    "ship": "murkäb",
    "shirt": ["luɔ̱t", "WN ruɔny"],
    "shoe": "war",
    "shoebill": "ŋo̱k thok pur",
    "shoelace": "laak",
    "shoot": "bär",
    "shooter": "bäär",
    "shot": "ba̱r",
    "shoulder": "wuɔ̱ɔ̱k",
    "shoulder blade": "jiar",
    "side": "pek",
    "sinew": "ra̱a̱l",
    "sing": ["kɛt", "start to kit"],
    "singer": "ki̱i̱t",
    "sink": "di̱ŋ",
    "sister, his/her/its": "nyiman",
    "sister, my": "nyimaar",
    "sit curled up in a ball": "guɔ̱l",
    "sit on": "nyuɔ̱ɔ̱r",
    "situation": "ɣɔw",
    "six": "bäkɛl",
    "sixteen": "wäl bäkɛl",
    "size": "pek",
    "skin": ["guɔ̱ɔ̱p", "guur"],
    "skirt": ["ban", "traditional pac"],
    "skull": "pöör",
    "sky": "nhial",
    "slap": "pat",
    "sleep": "niɛn",
    "small intestine": "ci̱een",
    "smoke (gas)": "tol",
    "snail": "luɛk",
    "snake": ["thɔ̱l", "sp. gör"],
    "sneeze": "thiɛm",
    "sniff": ["ŋuɔ̱c", "ruat"],
    "snore": "ruat",
    "soak": "bim",
    "soil": ["piny", "mun"],
    "song": ["dit", "k.o. tuar"],
    "sorcerer": "ti̱et",
    "sort by putting in bunches": "liny",
    "sound": "jɔw",
    "spank": "yɔ̱t",
    "speak": "ri̱t",
    "spear": "yɛth",
    "spear, round": "bith",
    "spend cold season": "ruel",
    "spend rainy season": "tɔ̱̱a̱t",
    "spend summer": "ma̱c",
    "spend windy season": "jɔm",
    "spiky fish": "yiiw",
    "spirit": "yiëë",
    "spit": ["ŋol", "ruɛy"],
    "spoil": "slua̱ŋ",
    "spoon without a handle, traditional": "guɛk",
    "spoon, traditional": "tuŋ",
    "spread rumours about": "guir",
    "spring": "mäy",
    "squacco heron": "ŋo̱k kɔa̱m",
    "squat": "cuël",
    "squeeze": "nhiɛc",
    "stalk": "rɔany",
    "stand": "cuŋ",
    "star": "cier",
    "start": "tuɔk",
    "state": "wic",
    "stay": "te",
    "steal": "wän",
    "stick": "kɛɛt",
    "stir": "kɛr",
    "stirring stick": "pi̱c",
    "stomach": ["jia̱c", "jic"],
    "stone": "päm",
    "stretch": "riny",
    "string (for beads)": "wiɛɛy",
    "string (of a musical instrument)": "puɔ̱c",
    "suck out (bone marrow)": "lot",
    "suckle": "luɛth",
    "sun": "cäŋ",
    "surgeon": "reet",
    "surgery": "rët",
    "surprise": "pär",
    "surround": "göl",
    "sustain": "tek",
    "swamp": "toc",
    "sweep": "yɛc",
    "sweetheart": "luum",
    "swimming": "ket",
    "swing (in a cradle)": "yɔ̱k",
    "sword": "thɛp",
    "sycamore": ["sp.", "rɔ̱k"],
    "sycamore fig; fig-mulberry": "ŋɔ̱p",
    "table (traditional)": "jio̱ŋ",
    "tail": "juäl",
    "take": ["naŋ", "back tɛt"],
    "take off": ["par", "ka̱m"],
    "talk badly to": "jäny",
    "tamarind": "kɔat",
    "tambura lyre": "thom",
    "tassel (to decorate bull horns)": "dhur",
    "taste": ["met", "with tip of tongue bil"],
    "tear": "mër",
    "tell": ["jiök", "lies ka̱c", "stories ca̱t"],
    "ten": "wäl",
    "termite mound": "rɛl",
    "test": "ɣɔ̱n",
    "that": "ɛmɔ",
    "them": "kɛ",
    "there": "thi̱n",
    "they": "kɛn",
    "thief": ["kueel", "EN cuer"],
    "thigh": "ɣäm",
    "thing": "duɔ̱ɔ̱r",
    "think about": "caar",
    "thirteen": "wäl diɔ̱k",
    "thirty": "jiɛn da̱ŋ diɔ̱k",
    "this": ["mɛmɛ", "ɛmɛ"],
    "thistle": "thiɛl",
    "thorn": "kuɔɔk",
    "three": "diɔ̱k",
    "throat": ["ro̱l", "sack dhök"],
    "throw": ["yuɔr", "away yäk"],
    "tiang antelope": "thiäŋ",
    "tick": "cak",
    "tickle": "li̱ek",
    "tie": ["yɛn", "to tethering stick pɔat"],
    "tilapia": ["lɛk", "sp. rueth"],
    "time": "ni̱en",
    "tobacco": "tap",
    "together": "kɛɛl",
    "tongue": "lɛp",
    "too": "bä",
    "touch": ["thiɛp", "with tip of tongue bil"],
    "town": "rɛk",
    "track (of an animal)": "pöör",
    "trader": "ko̱o̱k",
    "tray": "pa̱t",
    "tree": "jiath",
    "tree (sp.)": ["luel", "gɔ̱k"],
    "tree bark": "köm",
    "tree resin": "lɔac",
    "tributary": "waŋ",
    "trick": "ka̱a̱ŋ",
    "try": ["ɣɔ̱a̱n", "with tip of tongue bil"],
    "turn": "ri̱t",
    "turtle": ["large mi̱eer", "small kuɛ̈ɛ̈t"],
    "twelve": "wäl rɛw",
    "twenty": "jiɛn da̱ŋ rɛw",
    "twin": "cuɛ̈k",
    "twist": ["wop", "ric"],
    "two": "rɛw",
    "udder": "yieen",
    "umbilical cord": ["lo̱k", "ca̱a̱r"],
    "umbrella thorn acacia": "thep",
    "undress": ["woc", "ka̱m"],
    "unite": "mat",
    "urinate": ["lac", "cuow"],
    "us (excluding addressee)": "kɔ",
    "us (including addressee)": "kɔn",
    "vagina": "mur",
    "valley": "lo̱o̱l",
    "vein": "ra̱a̱l",
    "very": "ɛlɔ̱ŋ",
    "viper": "pi̱en",
    "visit": "gui̱l",
    "vulture": ["cuɔɔr", "nyigol"],
    "wait for": "lip",
    "walk": "jäl",
    "want": "go̱r",
    "war": "ko̱r",
    "wardrobe (traditional)": "lel",
    "warthog": ["kul", "di̱är"],
    "wash": "lak",
    "wasp": "piɛɛn",
    "watch": "thaak",
    "water": ["pi̱", "wac"],
    "water bag (made of leather)": "go̱u",
    "water lily": "yil",
    "waterbuck": "pɔ̱a̱a̱r",
    "wave": "muaŋ",
    "we": ["kɔn", "excluding addressee kɔ"],
    "weave": "tuth",
    "weed": "buɔk",
    "week": "juɔk",
    "well": ["jiw", "dry ji̱er"],
    "wheat (wild)": "lääp",
    "whip": "yɔ̱t",
    "whistle at": "lok",
    "white stork": "jak-gɛ̈r-gɛ̈ɛ̈r",
    "who": "ɛŋa",
    "whore": "lër",
    "wild animal": "le̱y",
    "wilderness": "dɔr",
    "wind": ["jiom", "WN jiɔm"],
    "window": "wärnyi̱n",
    "wine": "koaŋ",
    "wing": "gɔ̱ak",
    "winter": "ji̱ɔm",
    "witch doctor": "ti̱et",
    "with": "kɛ",
    "within": "rɛy",
    "withhold": "put",
    "witness": "neen",
    "woman": "ciek",
    "wood": "jiath",
    "word": "ri̱et",
    "world": "ɣɔw",
    "worry": "diɛɛr",
    "wound": "buɔ̱t",
    "wrap": ["kum", "rith"],
    "wrestle down": "kuir",
    "wrist": "cuɔp",
    "write": "gɔ̱r",
    "yawn": "ŋam",
    "year": "ruɔ̱n",
    "yell": "yɔal",
    "yes": "ɣää",
    "yesterday": "pan",
    "you (plural object)": "yɛ",
    "you (plural subject)": "yɛn",
    "you (singular object)": "ji̱",
    "you (singular subject)": "ji̱n",
    "zebra": "cɔ̱trial",
    "zero": "baŋ"

    }

# Function to suggest close matches from the dictionary
def get_suggestions(word, n=1, cutoff=0.1):
    return get_close_matches(word, english_nuer_dict.keys(), n=n, cutoff=cutoff)

# Translation function with suggestions for missing words
def translate_to_nuer(text):
    words = text.lower().split()
    translated_words = []
    for word in words:
        translation = english_nuer_dict.get(word)
        if translation:
            translated_words.append(translation)
        else:
            close_matches = get_suggestions(word)
            if close_matches:
                match = close_matches[0]
                suggested_translation = english_nuer_dict[match]
                translated_words.append(f"No direct translation for '{word}'. Did you mean '{match}' (Nuer: {suggested_translation})?")
            else:
                translated_words.append(f"No translation available for '{word}'.")
    return ' '.join(translated_words)

@app.route("/", methods=["GET", "POST"])
def home():
    translated_text = ""
    if request.method == "POST":
        english_text = request.form["englishText"]
        translated_text = translate_to_nuer(english_text)
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>English to Nuer Translator</title>
</head>
<body>
    <h2>English to Nuer Translator</h2>
    <form method="post">
        English: <input type="text" name="englishText"><br>
        <input type="submit" value="Translate">
    </form>
    <p>Translation: {{ translated_text }}</p>
</body>
</html>
    """, translated_text=translated_text)

if __name__ == "__main__":
    app.run(host='localhost', port=9874)