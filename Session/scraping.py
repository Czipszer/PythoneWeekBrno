import json
import requests
import argparse
import database
import arrow

from datetime import datetime
from slugify import slugify
from redis import Redis


# function to print seach result
def print_journey(search, origin, destination):
    print_data = {'routes': []}

    for route in search:
        data = {}
        data['departureStation'] = slugify(origin)
        data['departureStationId'] = route['departureStationId']

        if isinstance(route['departureTime'], datetime):
            data['departureTime'] = route['departureTime'].strftime("%Y-%m-%d %H:%M:%S")
        else:
            data['departureTime'] = route['departureTime']

        data['arrivalStation'] = slugify(destination)
        data['arrivalStationId'] = route['arrivalStationId']

        if isinstance(route['arrivalTime'], datetime):
            data['arrivalTime'] = route['arrivalTime'].strftime("%Y-%m-%d %H:%M:%S")
        else:
            data['arrivalTime'] = route['arrivalTime']

        data['travelTime'] = slugify(route['travelTime'])
        print_data['routes'].append(data)

    print(json.dumps(print_data, indent=4))

    return print_data


def search_journey(origin, destination, date):
    host = "redis.pythonweekend.skypicker.com"
    password = "5a0285bc-2580-4909-beb6-5b3a86d5cd20"

    redis = Redis(host=f"{host}", port=6379, db=0, password=f"{password}", decode_responses=True)

    surname = "chip"
    key_location = surname + ":location:"
    key_journey = surname + ":journey:" + slugify(origin) + '_' + slugify(destination) + '_' + date

    # Verify if the city is in the cache
    departure_ask = redis.get(key_location + slugify(origin))
    if departure_ask is None:
        request_id = requests.get('https://brn-ybus-pubapi.sa.cz/restapi/consts/locations')
        for country in request_id.json():
            for city in country['cities']:
                redis.setex(key_location + slugify(city['name']), 3600, city['id'])

    # Get the id of the departure cities
    departure_city_id = redis.get(key_location + slugify(origin))
    if departure_city_id is None:
        print('Departure city not found')
        exit(1)

    # Get the id of the arrival cities
    arrival_city_id = redis.get(key_location + slugify(destination))
    if arrival_city_id is None:
        print('Arrival city not found')
        exit(1)

    result_ask = redis.get(key_journey)
    if result_ask is None:
        result_ask = database.read_from_db(departure_city_id, arrival_city_id, date)
        if result_ask == []:
            request_connection = requests.get(
                'https://brn-ybus-pubapi.sa.cz/restapi/routes/search/simple?tariffs=REGULAR&toLocationType=CITY&toLocationId=' + str(
                    arrival_city_id) + '&fromLocationType=CITY&fromLocationId=' + str(
                    departure_city_id) + '&departureDate=' + date)
            for route in request_connection.json()['routes']:
                database.write_to_db(slugify(origin), departure_city_id, route['departureStationId'],
                                     route['departureTime'], slugify(destination), arrival_city_id,
                                     route['arrivalStationId'],
                                     route['arrivalTime'], slugify(route['travelTime']))
            redis.setex(key_journey, 5, request_connection.text)
            result = request_connection.json()
            print_journey(result['routes'], origin, destination)
        else:
            result = {'routes': [result.__dict__ for result in result_ask]}
            redis.setex(key_journey, 5, json.dumps(print_journey(result['routes'], origin, destination)))
    else:
        result = json.loads(result_ask)
        print_journey(result['routes'], origin, destination)


if __name__ == '__main__':
    # Command line arguments parser
    parser = argparse.ArgumentParser()
    parser.add_argument('departure_city', type=str)
    parser.add_argument('arrival_city', type=str)
    parser.add_argument('date', type=str)
    arguments = parser.parse_args()

    search_journey(arguments.departure_city, arguments.arrival_city, arguments.date)
