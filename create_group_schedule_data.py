'''
Created on May 4, 2016
@author: hanhanwu
A group of friends from different cities will meet in the same place.
They will arrive on the same day, leave on the same day, share transportation to and from the airport
Need to find a way to minimize the cost (flight cost, car renting cost, waiting time and so on)
This file is to create such a dataset first
'''

def get_people_location():
    people = [
              ('Emmanuel', 'LA'),
              ('Hanhan', 'Vancouver'),
              ('Zoe', 'San Francisco'),
              ('Alice', 'Surrey'),
              ('Sam', 'Taiwan'),
              ('Steven', 'Shanghai')
              ]
    destination = 'Hawaii'
    return people, destination


def get_fights(f_path):
    f = open(f_path)
    flights = {}
    
    for l in f:
        origin, dest, depart_time, arrive_time, price = l.strip().split(",")
        flights.setdefault((origin, dest), [])
        flights[(origin, dest)].append((depart_time, arrive_time, int(price)))
    return flights


def main():
    flights_path = "[your path for flights.txt]"
    flights = get_fights(flights_path)
    print flights
    
    people, dest = get_people_location()
    print people
    print dest
    
if __name__ == '__main__':
    main()

