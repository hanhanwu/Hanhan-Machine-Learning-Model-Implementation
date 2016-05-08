'''
Created on May 7, 2016
@author: hanhanwu
 Hill climbing starts from a random solution, looking for better neighbor solutions
 In this process, it walks in the most steep slope till it reached a flat point
 This method will find local optimum but may not be global optimum
 Need to run the method several times, hoping one could get close to the global optimum
'''

import random

def hill_climbing(domain, costf, dest, people, flights):
    rs = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
    best_solution = None
    best_result = costf(rs, dest, people, flights)
    
    while True:
        
        neighbors = []
        
        for j in range(len(domain)):
            if rs[j]-1 > domain[j][0]:
                neighbors.append(rs[0:j]+[rs[j]-1]+rs[j+1:])
            if rs[j]+1 < domain[j][1]:
                neighbors.append(rs[0:j]+[rs[j]+1]+rs[j+1:])
                
        for k in range(len(neighbors)):
            cost = costf(neighbors[k], dest, people, flights)
            if cost < best_result:
                best_result = cost
                best_solution = neighbors[k]
            if cost == best_result:
                return best_solution, best_result
        
