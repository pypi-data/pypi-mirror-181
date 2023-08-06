import os
import pandas as pd

# Response configuration
CHECK_NUDITY = True
SCAN_IMAGES = True
RESPONSE_TWEETS = False

# get this root path
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

# AWS
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
BUCKET_NAME = "ds-alcohoritm-dev"
REGION_NAME = "us-east-1"

# MySQL
MySQL_CONN = {
    "host": os.getenv("mysql_host", ""),
    "port": os.getenv("mysql_port", ""),
    "user": os.getenv("mysql_user", ""),
    "pssw": os.getenv("mysql_pssw", ""),
    "db": os.getenv("mysql_db", ""),
}
# OpenAI
OPENAI_API_KEY = os.getenv("openai_api_key", "")
PROMPT_DIR = "data/prompt_gpt3_moments.txt"
OPENAI_CLF = True
# Instagram
IG_TOKEN = os.getenv("instagram_token", "")
# Twitter
TW_CONN = {
    "consumer_key": os.getenv("twitter_api_key_bavaria", ""),
    "consumer_secret": os.getenv("twitter_api_secret_bavaria", ""),
    "access_key": os.getenv("twitter_access_token_bavaria", ""),
    "access_secret": os.getenv("twitter_access_secret_bavaria", ""),
}
TW_CONN2 = {
    "consumer_key": os.getenv("twitter_api_key_2", ""),
    "consumer_secret": os.getenv("twitter_api_secret_2", ""),
    "access_key": os.getenv("twitter_access_token_2", ""),
    "access_secret": os.getenv("twitter_access_secret_2", ""),
    "bearer_token": os.getenv("twitter_bearer_token_2", ""),
}
TW_LOCS = {
    "bogota": [-74.25, 4.5, -74.01, 4.78],
    "CO": [-79.36, 0.96, -68.17, 12.49]
}
MAX_TWEETS_PER_TERM = 2000
# Directories and filenames
DATA_DIR = "{}/data".format(ROOT_PATH)
IMG_STORAGE = "img"
MODEL_IMG_DIR = "{}/models/model.h5".format(ROOT_PATH)
MODEL_TEXT_DIR = "{}/models/text_model.h5".format(ROOT_PATH)
MODEL_STTM_DIR = "models/model_group.pkl"
MODEL_NUDE_DIR = "models/nudity_model_onnx.p"
MODEL_TEXT_BERT_DIR = "models/bert_model_cpu.p"
# Field names
LANGUAGES = ["es", "en"]

# Other constants
TERMS = {
    "instagram": [
        "weekend", "beer", "cerveza", "findesemana", "tgif", "cocteles", "amigos", "cocktails", "viernes", "friday",
        "cervezapoker", "cervezaaguila", "clubcolombia", "rumba", "craftbeer", "food", "drinks", "friends",
        "beerstagram", "bar", "beertime", "cheers", "instabeer", "bartender", "beerporn", "foodie", "party", "brewery",
        "travel", "restaurante"
    ],
    "twitter": [
        "cerveza", "findesemana", "fin de semana", "cocteles", "amigos", "cocktails", "viernes", "poker", "rumba",
    ],
}

BRANDS = {
    "instagram": [
        "budcolombia", "stellaartoisco", "clubcolombia", "becks_society", "reddscolombia", "mikescolombia",
        "michelobultraco", "cervezaaguila", "colaypolaoficial", "cervezapoker", "cervezacostenabacana"
    ],
    "twitter": [
        "BudweiserCo", "CervezaCoronaCo", "StellaArtoisCo", "Club_Colombia", "Cervezabecksco", "ReddsColombia",
        "mikescolombia", "CervezaAguila", "colaypola", "CervezaPoker", "costena_bacana", "PilsenCerveza",
        "cerveza aguila", "club colombia", "BAVARIA_OFICIAL"
    ]
}

COCO_CATEGORIES = {
    0: "N/A",
    1: "person",
    2: "bicycle",
    3: "car",
    4: "motorcycle",
    5: "airplane",
    6: "bus",
    7: "train",
    8: "truck",
    9: "boat",
    10: "traffic light",
    11: "fire hydrant",
    12: "street sign",
    13: "stop sign",
    14: "parking meter",
    15: "bench",
    16: "bird",
    17: "cat",
    18: "dog",
    19: "horse",
    20: "sheep",
    21: "cow",
    22: "elephant",
    23: "bear",
    24: "zebra",
    25: "giraffe",
    26: "hat",
    27: "backpack",
    28: "umbrella",
    29: "shoe",
    30: "eye glasses",
    31: "handbag",
    32: "tie",
    33: "suitcase",
    34: "frisbee",
    35: "skis",
    36: "snowboard",
    37: "sports ball",
    38: "kite",
    39: "baseball bat",
    40: "baseball glove",
    41: "skateboard",
    42: "surfboard",
    43: "tennis racket",
    44: "bottle",
    45: "plate",
    46: "wine glass",
    47: "cup",
    48: "fork",
    49: "knife",
    50: "spoon",
    51: "bowl",
    52: "banana",
    53: "apple",
    54: "sandwich",
    55: "orange",
    56: "broccoli",
    57: "carrot",
    58: "hot dog",
    59: "pizza",
    60: "donut",
    61: "cake",
    62: "chair",
    63: "couch",
    64: "potted plant",
    65: "bed",
    66: "mirror",
    67: "dining table",
    68: "window",
    69: "desk",
    70: "toilet",
    71: "door",
    72: "tv",
    73: "laptop",
    74: "mouse",
    75: "remote",
    76: "keyboard",
    77: "cell phone",
    78: "microwave",
    79: "oven",
    80: "toaster",
    81: "sink",
    82: "refrigerator",
    83: "blender",
    84: "book",
    85: "clock",
    86: "vase",
    87: "scissors",
    88: "teddy bear",
    89: "hair drier",
    90: "toothbrush",
    91: "hair brush",
    92: "banner",
    93: "blanket",
    94: "branch",
    95: "bridge",
    96: "building-other",
    97: "bush",
    98: "cabinet",
    99: "cage",
    100: "cardboard",
    101: "carpet",
    102: "ceiling-other",
    103: "ceiling-tile",
    104: "cloth",
    105: "clothes",
    106: "clouds",
    107: "counter",
    108: "cupboard",
    109: "curtain",
    110: "desk-stuff",
    111: "dirt",
    112: "door-stuff",
    113: "fence",
    114: "floor-marble",
    115: "floor-other",
    116: "floor-stone",
    117: "floor-tile",
    118: "floor-wood",
    119: "flower",
    120: "fog",
    121: "food-other",
    122: "fruit",
    123: "furniture-other",
    124: "grass",
    125: "gravel",
    126: "ground-other",
    127: "hill",
    128: "house",
    129: "leaves",
    130: "light",
    131: "mat",
    132: "metal",
    133: "mirror-stuff",
    134: "moss",
    135: "mountain",
    136: "mud",
    137: "napkin",
    138: "net",
    139: "paper",
    140: "pavement",
    141: "pillow",
    142: "plant-other",
    143: "plastic",
    144: "platform",
    145: "playingfield",
    146: "railing",
    147: "railroad",
    148: "river",
    149: "road",
    150: "rock",
    151: "roof",
    152: "rug",
    153: "salad",
    154: "sand",
    155: "sea",
    156: "shelf",
    157: "sky-other",
    158: "skyscraper",
    159: "snow",
    160: "solid-other",
    161: "stairs",
    162: "stone",
    163: "straw",
    164: "structural-other",
    165: "table",
    166: "tent",
    167: "textile-other",
    168: "towel",
    169: "tree",
    170: "vegetable",
    171: "wall-brick",
    172: "wall-concrete",
    173: "wall-other",
    174: "wall-panel",
    175: "wall-stone",
    176: "wall-tile",
    177: "wall-wood",
    178: "water-other",
    179: "waterdrops",
    180: "window-blind",
    181: "window-other",
    182: "wood",
    184: "tree-merged",
    185: "fence-merged",
    186: "ceiling-merged",
    187: "sky-other-merged",
    188: "cabinet-merged",
    189: "table-merged",
    190: "floor-other-merged",
    191: "pavement-merged",
    192: "mountain-merged",
    193: "grass-merged",
    194: "dirt-merged",
    195: "paper-merged",
    196: "food-other-merged",
    197: "building-other-merged",
    198: "rock-merged",
    199: "wall-other-merged",
    200: "rug-merged",
}
STOP_WRDS = ["@", "#", "si", "pa", "um", "na", "of", "in", "on", "i", "mas", "q", "ser", "asi", "va", "ir"]
FEATURES = [
    "person",
    "bottle",
    "cup",
    "dining table",
    "chair",
    "sky-other-merged",
    "bowl",
    "wine glass",
    "grass-merged",
    "wall-other-merged",
    "building-other-merged",
    "sea",
    "mountain-merged",
    "table-merged",
    "floor-other-merged",
    "tree-merged",
    "light",
    "ceiling-merged",
    "knife",
    "spoon",
    "food-other-merged",
]
IMG_DB_FIELDS = [
    "filename",
    "id",
    "permalink",
    "shortcode",
    "media_url",
    "timestamp",
    "date",
    "caption",
    "clean_text",
    "owner_id",
    "owner_username",
    "owner_full_name",
    "location_lat",
    "location_lng",
    "location_name",
    "city",
    "admin1",
    "admin2",
    "country_iso2",
    "obj_img",
    "top_labels",
    "color_img",
    "gender",
    "target",
    "business_category_name",
    "category_name",
    "profile_type",
    "brands",
    "keywords",
    "top_keyword"
]
IG_BUSINESS_CATEGORY = {
    "person": ["Creators & Celebrities"],
    "business": [
        "Auto Dealers", "Business & Utility Services", "Food & Personal Goods", "Grocery & Convenience Stores",
        "Home Goods Stores", "Home Services", "Lifestyle Services", "Local Events", "Content & Apps",
        "Non-Profits & Religious Organizations", "Personal Goods & General Merchandise Stores", "Home & Auto",
        "Professional Services", "Restaurants", "Transportation & Accomodation Services", "Government Agencies"
    ],
}
IG_CATEGORY = {
    "person": [
        None, "Actor", "Artist", "Athlete", "Beauty, cosmetic & personal care", "Blogger", "Chef", "DJ", "Dancer",
        "Editor", "Fashion Model", "Fitness Model", "Fitness Trainer", "Gamer", "Gaming video creator",
        "Graphic Designer", "Just for fun", "Personal blog", "Photographer", "Photography Videography",
        "Psychotherapist", "Public figure", "Video creator", "Writer", "null"
    ],
    "business": [
        "Advertising/Marketing", "American Restaurant", "Arts & entertainment", "Automotive Parts Store", "Bar",
        "Bar & Grill", "Bartending Service", "Beach Resort", "Beer Bar", "Beer Garden", "Bicycle Shop", "Brewery",
        "Broadcasting & media production company", "Cafe", "Cafeteria", "Cars", "Clothing (Brand)", "Cocktail Bar",
        "Coffee shop", "Commercial & Industrial", "Community", "Company", "Consulting agency", "Cultural Center",
        "Dance & Night Club", "Deli", "Department Store", "E-commerce website", "Education", "Electronics Store",
        "Entertainment website", "Event", "Fan page", "Fast food restaurant", "Food Truck", "Grocery Store",
        "Hardware Store", "Hostel", "Hotel", "Hotel & Lodging", "Hotel resort", "Irish Restaurant", "Local business",
        "Lounge", "Magazine", "Management Service", "Media/news company", "Mexican Restaurant",
        "Music Production Studio", "Newspaper", "Party Entertainment Service", "Performance & Event Venue",
        "Pizza place", "Podcast", "Pop-Up Shop", "Producer", "Product/service", "Pub", "Race Track", "Radio station",
        "Real Estate", "Religious Center", "Religious organization", "Restaurant", "Retail company", "Sandwich Shop",
        "Seafood Restaurant", "Service Apartments", "Shopping & retail", "Shopping Mall", "Social Club",
        "Social Media Agency", "Sports & recreation", "Sports Bar", "Sports Club", "Steakhouse",
        "Tapas Bar & Restaurant", "Theatrical Play", "Wholesale Bakery", "Wine, Beer & Spirits Store", "Wine/spirits",
    ],
}
IMG_PER_QUERY = 300

TOP_OBJECTS = {
    "DETR_1": ["bottle", "cup"],
    "SEGFORMER_1": ["pop bottle - soda bottle", "beer bottle", "beer glass", "whiskey jug", "water bottle", "bottlecap",
                    "cocktail shaker"],
    "SEGFORMER_0": ["red wine", "wine bottle", "web site - website - internet site - site"],
}

BUSINESS_NAME_WORDS = [
    "bakery", "bar", "bbq", "beer", "bistro", "burger", "cafe", "cerveceria", "cerveza", "club", "cocktail",
    "cocteleria", "cocteles", "disco", "gastrobar", "home", "hostal", "hotel", "licorera", "licores", "lounge",
    "parrilla", "pizza", "pub", "restaurant", "restobar", "salon", "sport", "tabern", "taco", "estacion", "consultor"
]

locs = pd.read_json("{}/data/locations_co.json".format(ROOT_PATH))
LOCATIONS = list(locs["external_id"])
DAYS_LIMIT = 2

TEMPLATES_DM_DIR = "data/alcohorithm-dm-templates.json"
TEMPLATES_RP_DIR = "data/alcohorithm-response-templates.json"
GREETINGS = ["Entonces", "Qué hubo", "Hola", "Buenas", "Hey"]
COUNTRIES = ["CO"]
