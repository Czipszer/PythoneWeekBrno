import argparse
import csv
import json
from queue import Empty

from typing import List
from dataclasses import dataclass
from datetime import datetime
from datetime import timedelta


# Definition class for flight
@dataclass
class Flight:
    flight_no: str
    origin: str
    destination: str
    departure: datetime
    arrival: datetime
    base_price: float
    bag_price: float
    bags_allowed: int


# Definition class for airport
@dataclass
class Airport:
    name: str
    flights: List[Flight]

    def add_flight(self, new_flight):
        self.flights.append(new_flight)


# function for searching using modify BFS search algorithm
def search(airports, now, destination, departure, bags, my_flight, visited, my_possible_flights):
    visited.append(now)

    if now == destination:
        my_possible_flights.append(my_flight)
        return

    for next_destination in airports[now].flights:
        if next_destination.destination not in visited:
            if int(next_destination.bags_allowed) >= bags:
                waiting = timedelta(hours=1)

                if len(my_flight) != 0:
                    waiting = datetime.fromisoformat(next_destination.departure) - datetime.fromisoformat(departure)

                one_hour = timedelta(hours=1)
                six_houres = timedelta(hours=6)

                if one_hour <= waiting <= six_houres:
                    looking_new_flight = my_flight.copy()
                    looking_new_flight.append(next_destination)
                    search(airports, next_destination.destination, destination, next_destination.arrival, bags,
                           looking_new_flight, visited.copy(), my_possible_flights)


# function to print seach result
def print_flights(my_possible_flights, arguments):
    data = []
    for connection in my_possible_flights:
        print_data = {'flights': []}
        total_price = 0
        bags_allowed = []

        for flight in connection:
            print_data['flights'].append(flight.__dict__)
            total_price += float(flight.base_price) + float(flight.bag_price) * int(arguments.bags)
            bags_allowed.append(flight.bags_allowed)
        print_data['bags_allowed'] = min(bags_allowed)
        print_data['bags_count'] = arguments.bags
        print_data['origin'] = arguments.origin
        print_data['destination'] = arguments.destination
        print_data['total_price'] = total_price
        print_data['travel_time'] = str(
            datetime.fromisoformat(connection[-1].arrival) - datetime.fromisoformat(connection[0].departure))
        data.append(print_data)

    data.sort(key=lambda x: x['total_price'])

    print(json.dumps(data, indent=4))


# main code
if __name__ == '__main__':
    # Command line arguments parser
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str)
    parser.add_argument('origin', type=str)
    parser.add_argument('destination', type=str)
    parser.add_argument('--bags', type=int, default=0)
    parser.add_argument('--return', action='store_true', default=False)
    arguments = parser.parse_args()

    # Load data from CVS
    with open(arguments.file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        flights = [Flight(*row) for row in csv_reader]

    # Full class with data
    airports = {}
    for f in flights:
        airport = airports.get(f.origin)
        if airport is None:
            airport = Airport(f.origin, [])
            airports[f.origin] = airport
        airport.add_flight(f)

    visited = []
    my_flight = []
    my_possible_flights = []

    search(airports, arguments.origin, arguments.destination, None, int(arguments.bags), my_flight, visited,
           my_possible_flights)
    print_flights(my_possible_flights, arguments)
