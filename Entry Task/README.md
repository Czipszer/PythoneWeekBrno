# Python weekend entry task

**Python script, that for a given flight data in a form of `csv` file (check the examples), prints out a structured list in console of all flight combinations for a selected route between airports A -> B, sorted by the final price for the trip.**

### Description
With some semi-randomly generated example csv datasets you can use to test your solution. The datasets have following columns:
- `flight_no`: Flight number.
- `origin`, `destination`: Airport codes.
- `departure`, `arrival`: Dates and times of the departures/arrivals.
- `base_price`, `bag_price`: Prices of the ticket and one piece of baggage.
- `bags_allowed`: Number of allowed pieces of baggage for the flight.

In addition to the dataset, script require take some additional arguments as input:

| Argument name | type    | Description              | Notes                        |
|---------------|---------|--------------------------|------------------------------|
| `origin`      | string  | Origin airport code      |                              |
| `destination` | string  | Destination airport code |                              |
| `bags`        | integer | Number of requested bags | Optional (defaults to 0)     |
| `return`      | boolean | Is it a return flight?   | Optional (defaults to false) |

### Search restrictions
- Search are perform on ALL available combinations, according to search parameters.
- In case of a combination of A -> B -> C, the layover time in B should **not be less than 1 hour and more than 6 hours**.
- No repeating airports in the same trip!
    - A -> B -> A -> C is not a valid combination for search A -> C.
- Output is sorted by the final price of the trip.

### Performing return trip search
Example input (`solution.py` is the main module):
```
python -m solution example/example0.csv RFZ WIW --bags=1 --return
```
will perform a search RFZ -> WIW -> RFZ for flights which allow at least 1 piece of baggage.

- **NOTE:** Since WIW is in this case the final destination for one part of the trip, the layover rule does not apply.

- **NOTE:** Return flight is still not implemented.

#### Output
The output is a json-compatible structured list of trips sorted by price. The trip has the following schema:
| Field          | Description                                                   |
|----------------|---------------------------------------------------------------|
| `flights`      | A list of flights in the trip according to the input dataset. |
| `origin`       | Origin airport of the trip.                                   |
| `destination`  | The final destination of the trip.                            |
| `bags_allowed` | The number of allowed bags for the trip.                      |
| `bags_count`   | The searched number of bags.                                  |
| `total_price`  | The total price for the trip.                                 |
| `travel_time`  | The total travel time.                                        |

**For more information, check the example section.**

## Example behaviour

If you want to test the script by performing a flight search on route RFZ -> WIN with one bag. We run the thing:

```bash
python -m solution example/example0.csv RFZ WIW --bags=1
```
and get the following result:

```json
[
    {
        "flights": [
            {
                "flight_no": "ZH214",
                "origin": "RFZ",
                "destination": "WIW",
                "departure": "2021-09-02T05:50:00",
                "arrival": "2021-09-02T10:20:00",
                "base_price": "168.0",
                "bag_price": "12",
                "bags_allowed": "2"
            }
        ],
        "bags_allowed": "2",
        "bags_count": 2,
        "origin": "RFZ",
        "destination": "WIW",
        "total_price": 192.0,
        "travel_time": "4:30:00"
    },
    {
        "flights": [
            {
                "flight_no": "ZH214",
                "origin": "RFZ",
                "destination": "WIW",
                "departure": "2021-09-05T05:50:00",
                "arrival": "2021-09-05T10:20:00",
                "base_price": "168.0",
                "bag_price": "12",
                "bags_allowed": "2"
            }
        ],
        "bags_allowed": "2",
        "bags_count": 2,
        "origin": "RFZ",
        "destination": "WIW",
        "total_price": 192.0,
        "travel_time": "4:30:00"
    },
    {
        "flights": [
            {
                "flight_no": "ZH214",
                "origin": "RFZ",
                "destination": "WIW",
                "departure": "2021-09-10T05:50:00",
                "arrival": "2021-09-10T10:20:00",
                "base_price": "168.0",
                "bag_price": "12",
                "bags_allowed": "2"
            }
        ],
        "bags_allowed": "2",
        "bags_count": 2,
        "origin": "RFZ",
        "destination": "WIW",
        "total_price": 192.0,
        "travel_time": "4:30:00"
    }
]
```
