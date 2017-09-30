"""
Help me find an apartment in Vancouver
"""
import settings
from craigslist import CraigslistHousing
from slackclient import SlackClient
from pprint import pprint
import json
import sys
import math

def coord_distance(lat1, lon1, lat2, lon2):
    """
    Finds the distance between two pairs of latitude and longitude.
    :param lat1: Point 1 latitude.
    :param lon1: Point 1 longitude.
    :param lat2: Point two latitude.
    :param lon2: Point two longitude.
    :return: Kilometer distance.
    """
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    km = 6367 * c
    return km


def in_box(coords, box):
    """
    Find if a coordinate tuple is inside a bounding box.
    :param coords: Tuple containing latitude and longitude.
    :param box: Two tuples, where first is the bottom left, and the second is the top right of the box.
    :return: Boolean indicating if the coordinates are in the box.
    """
    #print(coords,' vs ', box)
    if box[0][0] < coords[0] < box[1][0] and box[0][1] < coords[1] < box[1][1]:
        return True
    return False

# Search Craigslist Housing
cl = CraigslistHousing(
    site=settings.CRAIGSLIST_SITE,
    category='hhh',
    filters=settings.CRAIGSLIST_HOUSE_FILTERS
)

limit = settings.CRAIGSLIST_SEARCH_LIMIT
print('\nGetting {} results from Craigslist...'.format(limit))
results = cl.get_results(sort_by='newest', geotagged=True, limit=limit)


places = []
fo = open(settings.CRAIGSLIST_RESULTS, 'w')
for result in results:
    #pprint(result)
    output = "{}\n".format(json.dumps(result, indent=4))
    fo.write(output)
    places.append(result)

fo.close()

print('Found {} places!'.format(len(places)))


# Filter places by geography
print('\nFiltering places by geography...')
candidates = []
for place in places:
    #pprint(place)

    # filter by geolocation
    #print('Filtering by geolocation...')
    geotag = place['geotag']
    if geotag:
        area_found = False
        area = ''
        areas = []
        for area, coords in settings.AREAS_OF_INTEREST.items():
            if in_box(geotag, coords):
                areas.append(area)
                area_found = True
                #print(geotag,'vs', coords, area)

        if areas:
            place['area'] = areas
            if place not in candidates:
                candidates.append(place)
    
    # no geotag included
    else:
        # filter by location
        #print('Filtering by location...')
        location = place['where']
        if location:
            areas = []
            for area in list(settings.AREAS_OF_INTEREST.keys()):
                if area in location.lower():
                    areas.append(area)

            if areas:
                place['area'] = areas
                if place not in candidates:
                    candidates.append(place)


# Observe candidate places
print('\nFound {} candidate places!'.format(len(candidates)))
fo = open(settings.CANDIDATE_PLACES, 'w')
for candidate in candidates:
    output = "{}\n".format(json.dumps(candidate, indent=4))
    fo.write(output)
fo.close()

#sys.exit(1)
# Filter places by proximity to transit
print('\nFiltering places by proximity to transit...')

near_sky = False
sky_dist = 'N/A'
sky = ''
max_transit_dist = 2

filtered_candidates = []
for candidate in candidates:
    min_dist = None
    geotag = candidate['geotag']
    stations = {}
    
    for station, coords in settings.SKYTRAIN_STATIONS.items():
        dist = coord_distance(coords[0], coords[1], geotag[0], geotag[1])
        
        if (min_dist is None or dist < min_dist) and dist < max_transit_dist:
            print("Min dist '{}' -> '{}': '{}'".format(candidate['id'], station, dist))
            min_dist = dist
            sky = station

            stations[station] = min_dist
    
    if stations:
        #print('id', candidate['id'], 'Stations:', stations)
        candidate['stations'] = stations
        filtered_candidates.append(candidate)


# Observe filtered candidate places
print('\nFound {} transit candidate places!'.format(len(filtered_candidates)))
#for candidate in filtered_candidates:
#    pprint(candidate)


# Post to slack
print('\nPosting to slack channel...')
SLACK_TOKEN = 'xoxp-248780789472-250518579559-248914308977-8a48a6b9970481af22c08fdd35c79752'
SLACK_CHANNEL = '#housing'
sc = SlackClient(SLACK_TOKEN)

for result in filtered_candidates:
    
    stations_list = ["{}: {}km".format(k, v) for k, v in result['stations'].items()]
    stations = ";".join(stations_list)
    #station = "{} - {} km".format(station[])
    desc = "{0} | {1} | {2} | {3} | <{4}>".format(
                                                result["area"],
                                                result["price"], 
                                                stations,
                                                result["name"], 
                                                result["url"]
                                            )

    sc.api_call(
        "chat.postMessage", channel=SLACK_CHANNEL, text=desc,
        username='pybot', icon_emoji=':robot_face:'
    )

