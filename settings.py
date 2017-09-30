'''
settings.py
'''

## Cragislist Search

CRAIGSLIST_SEARCH_LIMIT = 50
CRAIGSLIST_RESULTS = 'craigslist_results.txt'
CANDIDATE_PLACES = 'candidate_places.txt'

## Location preferences

# The Craigslist site you want to search on.
# For instance, https://vancouver.craigslist.org is Vancouver Area.
# You only need the beginning of the URL.
CRAIGSLIST_SITE = 'vancouver'

# search filter
CRAIGSLIST_HOUSE_FILTERS={
	'max_price': 1500, 
    'min_price': 300,
    'laundry': [
    	'w/d in unit',
    	'laundry in bldg'
    	],
    'private_room': True,
    'private_bath': True,
    'parking': [
    	'street parking',
    	'off-street parking',
    	'attached garage',
    	'detached garage',
    	'carport'
    	],
}

# A list of neighborhoods and coordinates that you want to look for apartments in.  Any listing that has coordinates
# attached will be checked to see which area it is in.  If there's a match, it will be annotated with the area
# name.  If no match, the neighborhood field, which is a string, will be checked to see if it matches
# anything in NEIGHBORHOODS.
AREAS_OF_INTEREST = {
    "Chinatown": [
        [49.2778350197,-123.1032528803],
        [49.2805329803,-123.1005549197],
    ],
    "Coal Harbour": [
        [49.284436,-123.133843],
        [49.293603,-123.114012],
    ],
    "Davie Village": [
        [49.274512,-123.149364],
        [49.289069,-123.117349],
    ],
    "Downtown": [
        [49.270443,-123.135679],
        [49.289976,-123.09988],
    ],
    "False Creek": [
        [49.267306,-123.145229],
        [49.284168,-123.102917],
    ],
    "Granville Island": [
        [49.2682764,-123.1374752],
        [49.2733879,-123.1300753],
    ],
    "Kerrisdale": [
        [49.205662,-123.18053],
        [49.23475,-123.139609],
    ],
    "Killarney": [
        [49.201469,-123.056824],
        [49.234183,-123.023068],
    ],
    "Kitsilano": [
        [49.257177,-123.185964],
        [49.279369,-123.138936],
    ],
    "Main St. (Riley Park)": [
        [49.233134,-123.102106],
        [49.25658,-123.100243],
    ],
    "Oakridge": [
        [49.217721,-123.140116],
        [49.234344,-123.105658],
    ],
    "Olympic Village": [
        [49.2651627197,-123.1170870803],
        [49.2678606803,-123.1143891197],
    ],
    "Fairview": [
        [49.256931,-123.146003],
        [49.274801,-123.114707],
    ],
    "Riley Park": [
        [49.232898,-123.118349],
        [49.256931,-123.089855],
    ],
    "Shaughnessy": [
        [49.233992,-123.155325],
        [49.257935,-123.12729],
    ],
    "Southlands": [
        [49.242667,-123.201201],
        [49.257234,-123.169187],
    ],
    "Strathcona": [
        [49.265176,-123.102314],
        [49.27945,-123.077157],
    ],
    #"Vancouver": [
    #    [49.198177,-123.22474],
    #    [49.317294,-123.023068],
    #],
    "West End": [
        [49.275795,-123.146696],
        [49.294429,-123.121076],
    ],
    "West Point Grey": [
        [49.257912,-123.224764],
        [49.279138,-123.183956],
    ],
    "Yaletown": [
        [49.27197,-123.126995],
        [49.278838,-123.113979],
    ]  
}


## Transit preferences

STATIONS_INPUT_FILE = 'skytrain_stations_list.txt'
STATIONS_OUTPUT_FILE = 'skytrain_stations_coordinates.txt'

SKYTRAIN_STATIONS = {
	"22nd Street": [49.1999948, -122.9491245],
	"29th Avenue": [49.2443298, -123.0462403],
	"Aberdeen": [49.1839547, -123.1364705],
	"Braid": [49.2332626, -122.8828625],
	"Brentwood Town Centre": [49.2664082, -123.0017618],
	"Bridgeport*": [49.19552909999999, -123.1260478],
	"Broadway–City Hall": [49.2629521, -123.1144996],
	"Burquitlam": [49.261381, -122.8898],
	"Burrard": [49.2856399, -123.1201878],
	"Columbia*": [49.2048287, -122.9060995],
	"Commercial–Broadway*[c]": [49.2626441, -123.0692566],
	"Coquitlam Central": [49.2748251, -122.800624],
	"Edmonds": [49.2122617, -122.9591407],
	"Gateway": [49.1988985, -122.8506622],
	"Gilmore": [49.264981, -123.0135116],
	"Granville": [49.283276, -123.1161202],
	"Holdom": [49.2647455, -122.9821661],
	"Inlet Centre": [49.2772516, -122.8281843],
	"Joyce–Collingwood[d]": [49.2383924, -123.0317903],
	"King Edward": [49.2492562, -123.1158516],
	"King George†": [49.182755, -122.8446418],
	"Lafarge Lake–Douglas†": [49.28558350000001, -122.791644],
	"Lake City Way": [49.2546304, -122.9392344],
	"Langara–49th Avenue": [49.2263277, -123.1160772],
	"Lansdowne": [49.1747384, -123.1365696],
	"Lincoln": [40.81589, -96.71393979999999],
	"Lougheed Town Centre*": [49.2485741, -122.8968732],
	"Main Street–Science World[e]": [49.2731564, -123.1004548],
	"Marine Drive": [49.2095948, -123.1169071],
	"Metrotown": [49.2257737, -123.0037583],
	"Moody Centre": [49.2779497, -122.8459077],
	"Nanaimo": [49.2483697, -123.0558706],
	"New Westminster": [49.201406, -122.912573],
	"Oakridge–41st Avenue": [49.2331568, -123.116637],
	"Olympic Village": [49.2665117, -123.1157381],
	"Patterson": [49.2297874, -123.0126752],
	"Production Way–University**": [49.2534047, -122.9181552],
	"Renfrew": [49.2588952, -123.045092],
	"Richmond–Brighouse†": [49.16808049999999, -123.1362376],
	"Royal Oak": [49.2200706, -122.9884628],
	"Rupert": [49.2608105, -123.0330238],
	"Sapperton": [49.22468689999999, -122.8893704],
	"Scott Road": [49.20441640000001, -122.8741659],
	"Sea Island Centre": [49.1930546, -123.1579993],
	"Sperling–Burnaby Lake": [49.2592013, -122.9640792],
	"Stadium–Chinatown[g]": [49.2793024, -123.1091541],
	"Surrey Central": [49.1894944, -122.8478491],
	"Templeton": [49.1966853, -123.1464086],
	"Vancouver City Centre": [49.28248319999999, -123.118555],
	"VCC–Clark†": [49.2657013, -123.0791219],
	"Waterfront**": [49.2859597, -123.1116501],
	"Yaletown–Roundhouse": [49.2745211, -123.1218596],
	"YVR–Airport†": [49.1966913, -123.1815123],
}

# The token that allows us to connect to slack.
# Should be put in private.py, or set as an environment variable.
try:
	from private import *
except Exception:
	pass