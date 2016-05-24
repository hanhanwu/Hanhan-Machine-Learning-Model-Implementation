'''
Created on May 23, 2016
Simulated Annealing
When the cost is higher, the new solution can still become the current solution with certain probability.
This aims at avoiding local optimum.
The temperature - willingness to accept a worse solution
When the temperature decreases, the probability of accepting a worse solution is less
'''
import random
import math

def simulated_annealing(domain, costf, dest, people, flights, T = 10000.0, cooling_rate = 0.95, step = 1):
    # random initialization
    rs = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
    
    while T > 0.1:
        new_dir = random.randint(-step, step)
        # randomly choose one of the index
        idx = random.randint(0, len(domain) - 1)
        rsc = rs
        rsc[idx] += new_dir
        if rsc[idx] < domain[idx][0]: rsc[idx] = domain[idx][0]
        if rsc[idx] > domain[idx][1]: rsc[idx] = domain[idx][1]
        pre_cost = costf(rs, dest, people, flights)
        curr_cost = costf(rsc, dest, people, flights)
        p = pow(math.e, (-pre_cost-curr_cost)/T)
        
        if (curr_cost < pre_cost or random.random() < p):
            rs = rsc
            
        T *= cooling_rate
    return rs, curr_cost
