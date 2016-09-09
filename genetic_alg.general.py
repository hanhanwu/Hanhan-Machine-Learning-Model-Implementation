'''
Created on Sep 8, 2016
'''

import random

def mutation(solution_vec, domain, step):
    random_idx = random.randint(0, len(solution_vec)-1)
    if random.random() < 0.5 and solution_vec[random_idx] > domain[random_idx][0]:
        solution_vec[random_idx] -= step
    elif solution_vec[random_idx] < domain[random_idx][1]:
        solution_vec[random_idx] += step
    return solution_vec


def crossover(svec1, svec2):
    random_idx = random.randint(1, len(svec1)-2)
    return svec1[0:random_idx]+svec2[random_idx:]


def genetic_alg_general():
    
    # TO BE CONTINUED
    pass
