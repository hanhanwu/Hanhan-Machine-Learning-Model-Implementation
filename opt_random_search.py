'''
Created on May 7, 2016
@author: hanhanwu
This is the baseline of optimization algorithms, any other optimization should be better than it
Randomly generates some solutions and find the best one among them
'''

import random
import sys

def random_search(domain, costf, dest, people, flights):
    best_result = sys.maxint
    best_solution = None
    
    for k in range(500):
        rs = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
        cost = costf(rs, dest, people, flights)
        if best_result > cost:
            best_result = cost
            best_solution = rs
        
    return best_solution, best_result
