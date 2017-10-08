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

# HELPER FUNCTIONS #
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


def find_geo_info(geotag, location):
    '''
    find geo information
    '''
    min_dist = None
    near_station = False
    station_dist = 'N/A'
    station_name = ''
    area = ''

    # Find area
    area_found = False
    for a, coords in settings.AREAS_OF_INTEREST.items():
        if in_box(geotag, coords):
            area = a
            area_found = True
            break

    # Get proximity to transit
    for station, coords in settings.SKYTRAIN_STATIONS.items():
        dist = coord_distance(coords[0], coords[1], geotag[0], geotag[1])
        dist = float('{:.2f}'.format(dist))
        
        if (min_dist is None or dist < min_dist):
            #print("Min dist '{}' -> '{}': '{}'".format(candidate['id'], station, dist))
            min_dist = dist
            station_name = station
            station_dist = dist

            if dist < settings.MAX_TRANSIT_DIST:
                near_station = True

    # Search area against neighborhoods of interest
    if area == '':
        for hood in settings.AREAS_OF_INTEREST.keys():
            if hood.lower() in location.lower():
                area = hood
                break

    result = {
        "area_found": area_found,
        "area": area,
        "near_station": near_station,
        "station_dist": station_dist,
        "station_name": station_name
    }

    return result


# BEGIN PROGRAM #
# Search Craigslist Housing
cl = CraigslistHousing(
    site=settings.CRAIGSLIST_SITE,
    category=settings.CRAIGSLIST_HOUSING_SECTION,
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

# Filter results
print('\nGetting geographical information...')
candidates = []
for place in places:
    #pprint(place)

    geotag = place['geotag']
    location = place['where']

    # Skip places which include no location information
    if location is None:
        continue

    if geotag:
        geo_info = find_geo_info(geotag, location)
        place.update(geo_info)
    
    else:
        place['area'] = ''
        place['station_name'] = ''

    print('Area:', place['area'])
    if len(place['station_name']) > 0 or len(place['area']) > 0:
        candidates.append(place)

# Observe candidate places
print('\nFound {} candidate places!'.format(len(candidates)))
fo = open(settings.CANDIDATE_PLACES, 'w')
for candidate in candidates:
    output = "{}\n".format(json.dumps(candidate, indent=4))
    fo.write(output)
fo.close()

sys.exit(1)
# Post to slack
print('\nPosting to slack channel...')
sc = SlackClient(settings.SLACK_TOKEN)

for result in candidates:
    
    desc = "{0} | {1} | {2} ({3} km)| {4} | <{5}>".format(
                                                result["area"],
                                                result["price"], 
                                                result["station_name"],
                                                result["station_dist"],
                                                result["name"], 
                                                result["url"]
                                            )

    sc.api_call(
        "chat.postMessage", channel=settings.SLACK_CHANNEL, text=desc,
        username='pybot', icon_emoji=':robot_face:'
    )

