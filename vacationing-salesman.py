#!/usr/bin/python
__author__ = "Ellen Fu"
__date__ = "March 29, 2017"

import sys
import itertools
from geopy.geocoders import Nominatim
from geopy.distance import vincenty

def findDist(cities, unit):
    """ accepts an ordered list of strings, each string of the form above designating
    a "City, Country", and a string indicating the unit (only supports inputs as
    "mi" or "km" right now). Returns a list with the distance, in the indicated units,
    between each successive pair of cities.
    Input: a list (cities), a string (unit)
    Output: a list containing the distances between each successive city
    """
    # Instantiates a Nominatim object that can find the coordinates from a given
    # address
    geolocator = Nominatim()

    # Instantiate an empty list to store the coordinates of each city and loops
    # through the cities list and finds each city's coordinates
    locations = []
    for city in cities:
        # Gets the latitude and longitude of the city
        location = geolocator.geocode(city)
        latitude = location.latitude
        longitude = location.longitude

        # Appends the city's latitude and longitude into the locations list as a tuple
        locations.append((latitude,longitude))

    distances = []
    curr = locations[0]
    for i in range(1,len(locations)):
        next = locations[i]
        if unit == "mi":
            distance = vincenty(curr, next).miles
        elif unit == "km":
            distance = vincenty(curr,next).kilometers
        distances.append(distance)
        curr = next

    return distances

def runScript():
    """ Processes the input into the shell script and calls the findDist function
    to return the list of distances between successive cities.
    Input: None (from )
    """
    # Storing the input from the text file given in the terminal command and calling
    # the findDist function
    cities = []
    cities_file = open(sys.argv[1], 'r')
    for line in cities_file:
        cities.append(line.strip('\n'))
    cities_file.close()

    unit = sys.argv[2]
    # distances = findDist(cities, unit)
    optimized_results = optimizeDist(cities,unit)
    cities = optimized_results[0]
    distances = optimized_results[1]

    # Print the output to stdout
    print "Success! Your vacation itinerary is:\n"
    for i in range(len(cities)-1):
        print "    " + cities[i]+ " -> " + cities[i+1] + ": " + str(round(distances[i],2)) + " " + unit
    print "\nTotal distance covered in your trip: " + str(round(sum(distances),2)) + " " + unit

def optimizeDist(cities, unit):
    """ Returns the route to minimize the distance traveled """
    # Gets all permutations of the given ordered list of cities so we can check
    # the distance of each possible route
    routes = list(itertools.permutations(cities))

    # Finds the distance of each route and each route's total distance and stores
    # them in two lists
    distances = []
    distance_sums = []
    for route in routes:
        route_distance = findDist(route, unit)

        # Stores the route with its corresponding distances between cities
        distances.append([route, route_distance])
        distance_sums.append(sum(route_distance))

    # Iterate through the distance_sums list to find the index of the minimum
    # distance for the vacation
    min_dist = float('Inf')
    min_ind = 0
    for i in range(len(distances)):
        if distance_sums[i] <= min_dist:
            min_dist = distance_sums[i]
            min_ind = i

    # Returns the route and the distance with the minimum total distance, as stored
    # in the distances list
    return distances[min_ind]

# Calls the runScript function to produce the output
runScript()
