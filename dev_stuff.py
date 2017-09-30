#!/usr/bin/env python
'''
random dev stuff
'''
import settings
import googlemaps
from pprint import pprint


def search_google_maps():
	# read file
	input_file = settings.STATIONS_INPUT_FILE
	output_file = settings.STATIONS_OUTPUT_FILE
	fi = open(input_file, 'r')
	fo = open(output_file, 'w')

	# set up googlemaps client
	gmaps = googlemaps.Client(key='AIzaSyDuAjs6LKD41NkLJK-aVYoIChA5mFYGZNM')

	print("Reading file '{}'...".format(input_file))
	stations = {}
	for line in fi:
		line = line.strip()
		search_term = line + ' station vancouver'
		print("Searching Google Maps for '{}'...".format(search_term))

		#result = gmaps.places(search_term)
		try:
			result = gmaps.geocode(search_term)

		except:
			e = sys.exc_info()[0]
			print('Error:', e)

		else:
			#print('Result:')
			#pprint(result)
			coordinates = result[0]['geometry']['location']
			stations[line] = [coordinates['lat'], coordinates['lng']]
			''' gmaps.places
			station_name = result['results'][0]['name']

			coordinates = result['results'][0]['geometry']['location']
			stations[station_name] = [coordinates['lat'], coordinates['lng']]
			'''

			output = "\"{}\": {},\n".format(line, stations[line])
			#print('Output:', output)
			fo.write(output)


	fi.close()
	fo.close()

	print('{} stations found:'.format(len(stations)))
	pprint(stations)


def filter_by_proximity():

def main():
	search_google_maps()
	filter_by_proximity()


if __name__ == '__main__':
    main()