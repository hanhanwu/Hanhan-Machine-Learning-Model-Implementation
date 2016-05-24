'''
Created on May 5, 2016

@author: hanhanwu
'''
import create_group_schedule_data as data_source
import time
import opt_random_searching
import opt_hill_climbing


def get_mins(t):
    ts = time.strptime(t, "%H:%M")
    return ts[3]*60 + ts[4]


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
        

# In this case, assuming waiting for 1 minute equals to cost $5 for normal people but $10 for Emmanuel :)
# Assuming this group of people will wait at the airport till everyone got there, later will leave the airport on the same day
def get_cost(slst, dest, people, flights):
    total_cost = 0
    last_arrival = 0
    first_leave = 24*60
    
    for i in range(len(people)):
        p = people[i][0]
        origin = people[i][1]
        idx1 = slst[i*2]
        idx2 = slst[i*2+1]
        arrival = flights[(origin, dest)][idx1]
        leave = flights[(dest, origin)][idx2]
        arrive_time = get_mins(arrival[1])
        leave_time = get_mins(leave[0])
        total_cost += (arrival[2]+leave[2])
        if last_arrival < arrive_time: last_arrival = arrive_time
        if first_leave > leave_time: first_leave = leave_time
        
    for i in range(len(people)):
        p = people[i][0]
        origin = people[i][1]
        idx1 = slst[i*2]
        idx2 = slst[i*2+1]
        arrival = flights[(origin, dest)][idx1]
        leave = flights[(dest, origin)][idx2]
        arrive_time = get_mins(arrival[1])
        leave_time = get_mins(leave[0])
        waiting_time = (last_arrival - arrive_time) + (leave_time - first_leave)
        if p == "Emmanuel": total_cost += 10*waiting_time
        else: total_cost += 5*waiting_time
        
    return total_cost


def main():
    flights_path = "[ your flights.txt path ]"
    flights = data_source.get_fights(flights_path)
    people, dest = data_source.get_people_location()
    
    print 'test solution'
    test_solution = [4,1,3,7,2,3,6,3,4,2,5,3]
    get_solutions(test_solution, dest, people, flights)
    total_cost = get_cost(test_solution, dest, people, flights)
    print total_cost
    
    # OPTIMIZATION SOLUTIONS
    print '----------OPTIMIZATION---------'
    domain = [(0,8)]*len(people)*2
    
    # optimization method 1: random search
    # each time, the result can be different since it's random
    print 'Random Search'
    opt_solution, opt_cost = opt_random_searching.random_search(domain, get_cost, dest, people, flights)
    get_solutions(opt_solution, dest, people, flights)
    print opt_cost
    print
    
    # optimization method 2: hill climbing
    # each time, the result can be different since its initial is random
    print 'Hill Climbing'
    opt_solution, opt_cost = opt_hill_climbing.hill_climbing(domain, get_cost, dest, people, flights)
    get_solutions(opt_solution, dest, people, flights)
    print opt_cost
    print
    
    # optimization 3: simulated annealing  (avoid local optimum)
    # each time, the result can be different since its initial is random
    print 'Simulated Annealing'
    opt_solution, opt_cost = opt_simulated_annealing.simulated_annealing(domain, get_cost, dest, people, flights)
    get_solutions(opt_solution, dest, people, flights)
    print opt_cost
    print
    
if __name__ == '__main__':
    main()
