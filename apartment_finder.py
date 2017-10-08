"""
Help me find an apartment in Vancouver
"""

# MODULES #
import math
import json
import os
import settings
import sys
import traceback


from craigslist import CraigslistHousing
from slackclient import SlackClient
from pprint import pprint
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.orm import sessionmaker
from dateutil.parser import parse



# DB SETUP #

engine = create_engine('sqlite:///listings.db', echo=False)

Base = declarative_base()

class Listing(Base):
    '''
    A table to store data on craigslist listings.
    '''

    __tablename__ = 'listings'


    id = Column(Integer, primary_key=True)
    link = Column(String, unique=True)
    created = Column(DateTime)
    price = Column(Float)
    location = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    name = Column(String)
    area = Column(String)
    cl_id = Column(Integer, unique=True)
    train_station = Column(String)
    train_dist = Column(Float)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


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



'''
def old_function():
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

            for area, coords in settings.AREAS_OF_INTEREST.items():
                if in_box(geotag, coords):
                    #areas.append(area)
                    #area_found = True
                    place['area'] = area
                    candidates.append(place)
                    break
                    #print(geotag,'vs', coords, area)
        
        # no geotag included
        else:
            # filter by location
            #print('Filtering by location...')
            location = place['where']
            if location:
                areas = []
                for area in list(settings.AREAS_OF_INTEREST.keys()):
                    if area in location.lower():
                        place['area'] = area
                        candidates.append(place)
                        break
                        #areas.append(area)


    # Filter places by proximity to transit
    print('\nFiltering places by proximity to transit...')

    filtered_candidates = []
    for candidate in candidates:

        min_dist = None
        near_station = False
        station_dist = 'N/A'
        station_name = ''
        
        geotag = candidate['geotag']
        print("\nLooking for place '{}'...".format(candidate['id']))
        for station, coords in settings.SKYTRAIN_STATIONS.items():
            dist = coord_distance(coords[0], coords[1], geotag[0], geotag[1])
            dist = float('{:.2f}'.format(dist))
            
            #print("Dist '{}' -> '{}': '{}'".format(candidate['id'], station, dist))
            if (min_dist is None or dist < min_dist):
                print("Min dist '{}' -> '{}': '{}'".format(candidate['id'], station, dist))
                min_dist = dist
                station_name = station
                station_dist = dist

                if dist < settings.MAX_TRANSIT_DIST:
                    near_station = True

        print("{} is closest to {} station ({} km) {}\n".format(candidate['id'], 
            station_name, station_dist, dist))
        
        candidate['station_name'] = station_name
        candidate['near_station'] = near_station
        candidate['station_dist'] = station_dist
        filtered_candidates.append(candidate)


    # Observe candidate places
    print('\nFound {} candidate places!'.format(len(filtered_candidates)))
    fo = open(settings.CANDIDATE_PLACES, 'w')
    for candidate in filtered_candidates:
        # pprint(candidate)
        output = "{}\n".format(json.dumps(candidate, indent=4))
        fo.write(output)
    fo.close()

'''

def get_geo_data(geotag, location):
    '''
    get posting's geo data
    '''
    area_found = False
    area = ''
    min_dist = None
    near_station = False
    station_dist = 0.00
    station_name = ''

    # filter by geotag
    for a, coords in settings.AREAS_OF_INTEREST.items():
        if in_box(geotag, coords):
            area_found = True
            area = a
            break

    # filter by proximity to sky train
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

    #print("Area:'{}', '{}'".format(area, len(area)))
    if area == '':
        for place in settings.AREAS_OF_INTEREST:
            if place.lower() in location.lower():
                area = place
                break

    return {
        'area_found': area_found,
        'area': area,
        'near_station': near_station,
        'station_dist': station_dist,
        'station_name': station_name
    }


def scrape_craigslist_housing():
    '''
    scrape craigslist housing
    '''

    results = []

    # query craigslist
    # Search Craigslist Housing
    cl = CraigslistHousing(
        site=settings.CRAIGSLIST_SITE,
        category=settings.CRAIGSLIST_HOUSING_SECTION,
        filters=settings.CRAIGSLIST_HOUSE_FILTERS
    )

    limit = settings.CRAIGSLIST_SEARCH_LIMIT
    print('\nGetting {} results from Craigslist...'.format(limit))
    resp = cl.get_results(sort_by='newest', geotagged=True, limit=limit)
    fo = open(settings.CRAIGSLIST_RESULTS, 'w')
    
    while True:
        try:
            result = next(resp)
        except StopIteration:
            break
        except Exception:
            continue

        # write to file
        output = "{}\n".format(json.dumps(result, indent=4))
        fo.write(output)

        listing = session.query(Listing).filter_by(cl_id=result['id']).first()
        # Don't store the listing if it already exists.
        if listing is None:
            if result['where'] is None:
                continue

            lat = 0
            lon = 0

            geotag = result['geotag']
            if geotag:
                lat = geotag[0]
                lon = geotag[1]

                #print(result['id'])
                geo_data = get_geo_data(geotag, result['where'])
                result.update(geo_data)

            else:
                result['area'] = ''
                result['station_name'] = ''
                result['station_dist'] = 0.00


            #print('\nResult:')
            #pprint(result)
            # Try parsing the price
            price = 0
            try:
                price = float(result['price'].replace('$', ''))
            except Exception:
                pass

            # Creating listing object
            listing = Listing(
                link=result['url'],
                created=parse(result['datetime']),
                lat=lat,
                lon=lon,
                name=result['name'],
                price=price,
                location=result['where'],
                cl_id=result['id'],
                area=result['area'],
                train_station=result['station_name'],
                train_dist=result['station_dist']
            )

            # Save the listing to avoid duplication
            session.add(listing)
            session.commit()

            #pprint(result)
            if len(result['station_name']) > 0 or len(result['area']) > 0:
                #pprint(result)
                results.append(result)

    fo.close()
    return results


def post_to_slack(sc, results):
    '''
    post to slack channel
    '''
    print('\nPosting to slack channel...')
    
    for result in results:
        
        desc = "{0} | {1} | {2} ({3} km)| {4} | <{5}>".format(
                                                    result["area"],
                                                    result["price"], 
                                                    result["station_name"],
                                                    result['station_dist'],
                                                    result["name"], 
                                                    result["url"]
                                                )

        sc.api_call(
            "chat.postMessage", channel=settings.SLACK_CHANNEL, text=desc,
            username='pybot', icon_emoji=':robot_face:'
        )


def display_list(places):
    '''
    prints list of places in pretty format
    '''
    for place in places:
        pprint(place)


def print_to_file(candidates):
    '''
    prints to file the candidates found
    '''
    file_name = settings.CANDIDATE_PLACES
    print('\nPrinting candidate places to file {}...'.format(file_name))
    fo = open(file_name, 'w')
    for candidate in candidates:
        # pprint(candidate)
        output = "{}\n".format(json.dumps(candidate, indent=4))
        fo.write(output)
    fo.close()


def main_program():
    '''main program'''

    # Create slack client
    sc = SlackClient(settings.SLACK_TOKEN)

    # Scrape craigslist
    candidates = scrape_craigslist_housing()
    #print('Candidates:', candidates)
    print_to_file(candidates)

    print('Found {} candidate places'.format(len(candidates)))
    display_list(candidates)

    # Post to Slack
    #post_to_slack(sc, candidates)


if __name__ == '__main__':
    try:
        main_program()

    except Exception as err:
        tb_output = traceback.format_exc()
        print(tb_output)
        error_message = "Script hit an error: '{}'".format(err)
        print("Error Type: '{}'".format(sys.exc_info()[0]))

