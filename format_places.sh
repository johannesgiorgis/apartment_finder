#!/bin/bash

# format places_to_live.txt to properly order the coordinates

file_name="/Users/jawg/dev/python/apartment_finder/orig_places_to_live.txt"

places=`cat "$file_name" | egrep -v '(#|^$)'`

#echo "Places:, $places"
areas=`echo "$places" | awk -F'[' '{print $1}'`
#echo "Areas:, $areas"

#first_coordinates=`echo "$places" | awk -F'[' '{print $2}' | awk -F',' '{print $2 "," $1}'`
#echo "$first_coordinates"

#second_coordinates=`echo "$places" | awk -F']' '{print $1}' | awk -F',' '{print $4 "," $3}'`
#echo "$second_coordinates"

while read -r place
do
	#echo "$place"
	area=`echo "$place" | awk -F'[' '{print $1}' | tr -d '[:space:]'`
	first_coordinates=`echo "$place" | awk -F'[' '{print $2}' | awk -F',' '{print $2 "," $1}'`
	second_coordinates=`echo "$place" | awk -F']' '{print $1}' | awk -F',' '{print $4 "," $3}'`
	echo -e "\"$area\": [\n\t[$first_coordinates],\n\t[$second_coordinates],\n],"
	#echo ""
done <<< "$places"