'''
Created on May 5, 2016

@author: hanhanwu
'''
import create_group_schedule_data as data_source


def get_solutions(slst, dest, people, flights):
    for i in range(len(people)):
        p = people[i][0]
        origin = people[i][1]
        idx1 = slst[i*2]
        idx2 = slst[i*2+1]
        arrival = flights[(origin, dest)][idx1]
        leave = flights[(dest, origin)][idx2]
        print '%10s  %15s: arrive flight %5s %5s $%3s  return flight %5s %5s $%3s'\
        % (p, origin, arrival[0], arrival[1], arrival[2], leave[0], leave[1], leave[2])
        


def main():
    flights_path = "[your flights.txt path]"
    flights = data_source.get_fights(flights_path)
    people, dest = data_source.get_people_location()
    
    test_solution = [4,1,3,7,2,3,6,3,4,2,5,3]
    get_solutions(test_solution, dest, people, flights)
    
if __name__ == '__main__':
    main()
