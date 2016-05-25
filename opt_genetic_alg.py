'''
Created on May 24, 2016
Genetics Algorithm
elitism - choose the top solutions in current generation into the next generation
The rest solutions in the new generation are created by modifying the current top solutions:
    mutation - a small, random change on an existing solution
    crossover/breeding - combine 2 of the current top solutions
The new population has the same size as the old one
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
    
    

def genetic_alg(domain, costf, dest, people, flights, step = 1, 
                population = 50, mutation_prob = 0.2, elite = 0.2, max_iter = 100):
    pop = []
    top_soutions = population*elite
    # random initialization
    for i in range(population):
        svec = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
        pop.append(svec)
        
    for k in range(max_iter):
        scores = [(costf(pop[i], dest, people, flights), i) for i in range(population)]
        scores.sort()
        ranked_idx = [i for (c,i) in scores]
        
        new_pop = [pop[i] for i in ranked_idx[0:top_soutions]]
        
        while len(new_pop) < population:
            if random.random() < mutation_prob:
                ridx = random.randint(0, population-1)
                new_pop.append(mutation(pop[ridx], domain, step))
            else:
                ridx1 = random.randint(0, population-1)
                ridx2 = random.randint(0, population-1)
                new_pop.apend(crossover(pop[ridx1], pop[ridx2]))
        pop = new_pop
        
    return pop[0]
    
    


