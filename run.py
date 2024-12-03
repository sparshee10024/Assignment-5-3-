from flight import Flight
from planner import Planner

TIMEOUT = 5
TYPES = ["least_flights_earliest", "cheapest", "least_flights_cheapest"]
CALC_PARAMS = [
    lambda x: (len(x), x[-1].arrival_time),
    lambda x: sum([f.fare for f in x]),
    lambda x: (len(x), sum([f.fare for f in x]))
]

def read_file(filename):
    with open(filename, "r") as f:
        # The file is in the format := 
        #  First line contains start , end city..
        #  Second line contains n (number of vertices) , m (number of edges) , then next m lines contains u , v, cost , start_time, end_time . It means an edge from u to v.
        start_city, end_city = map(int, f.readline().split())
        n, m = map(int, f.readline().split())
        flights = []
        
        for i in range(m):
            u, v, start_time, end_time, cost = map(int, f.readline().split())
            flights.append(Flight(i, u, start_time, v, end_time, cost))
    
    t1 = 0
    t2 = 1e18
    return flights, start_city, end_city, t1, t2

def is_valid_path(route, flights, start_city, end_city):
    if not route:
        return False
    first_flight = route[0]
    if first_flight.start_city != start_city:
        print("1")
        return False
    
    last_flight = route[-1]
    if last_flight.end_city != end_city:
        print("2")
        return False
    for i in range(len(route) - 1):
        current_flight = route[i]
        next_flight = route[i + 1]
        # if current_flight.flight_no != route[i]:
        #     print("3")
        #     return False
        if current_flight.end_city != next_flight.start_city:
            print("4")
            return False
        
        if next_flight.departure_time < current_flight.arrival_time + 20:
            print("5")
            return False
    
    # Check if each route index matches the flight number in the flights list
    for i in range(len(route)):
        if flights[route[i].flight_no] != route[i]:
            print("6")
            return False
    
    return True

def find0(route, flights, start_city, end_city):
    if not is_valid_path(route, flights, start_city, end_city):
        return "Incorrect", "Path"
    num_flights = len(route)
    total_travel_time = route[-1].arrival_time
    return num_flights, total_travel_time

def find1(route, flights , start_city, end_city):
    if not is_valid_path(route, flights, start_city, end_city):
        return "Incorrect Path"
    total_cost = sum(routes.fare for routes in route)
    return total_cost

def find2(route, flights, start_city, end_city):
    if not is_valid_path(route, flights, start_city, end_city):
        return "Incorrect", "Path"
    
    num_flights = len(route)
    total_cost = sum(routes.fare for routes in route)
    return num_flights, total_cost



def run_test(filename, type):
    """
    Run the test based on the input file and type flag.
    
    Args:
        filename (str): The name of the input file.
        type (int): The type of test to run (0, 1, or 2).
    """
    flights, start_city, end_city, t1, t2 = read_file(filename)
    planner = Planner(flights)
    
    if type == 0:
        # Run the least flights earliest route
        route = planner.least_flights_earliest_route(start_city, end_city, t1, t2)
        # print(route[0])
        num_flights, ttime = find0(route, flights, start_city, end_city)
        print(f"{num_flights} {ttime}")
    elif type == 1:
        # Run the cheapest route
        route = planner.cheapest_route(start_city, end_city, t1, t2)
        cost = find1(route, flights, start_city, end_city)
        print(f"{cost}")
    elif type == 2:
        # Run the least flights cheapest route
        route = planner.least_flights_cheapest_route(start_city, end_city, t1, t2)
        num_flights, cost = find2(route, flights, start_city, end_city)
        print(f"{num_flights} {cost}")
    else:
        print("Error: Invalid type flag. Type must be 0, 1, or 2.")

import sys

if __name__ == "__main__":
    input_file = sys.argv[1]
    type_flag = int(sys.argv[2])  # Convert to integer
    run_test(input_file, type_flag)