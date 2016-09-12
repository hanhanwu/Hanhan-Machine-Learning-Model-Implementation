'''
Created on Sep 11, 2016
'''

import random


def genetic_alg_general(domain, costf, pop_size = 50, max_iter = 100, elite = 0.2, mutprob = 0.3, step = 1):
    
    def mutate(vec):
        mutate_idx = random.randint(0, len(domain)-1)
        if vec[mutate_idx] < domain[mutate_idx][1] and vec[mutate_idx] >= domain[mutate_idx][0]:
            return vec[0:mutate_idx] + [vec[mutate_idx]+step] + vec[mutate_idx+1:]
        else:
            return vec[0:mutate_idx] + [vec[mutate_idx]-step] + vec[mutate_idx+1:]
        
    def crossover(r1, r2):
        crossover_idx = random.randint(0, len(domain)-2)
        return r1[0:crossover_idx] + r2[crossover_idx:]
    
    # initial population
    pop = []
    for i in range(pop_size):
        vec = [random.randint(domain[j][0], domain[j][1]) for j in range(len(domain))]
        pop.append(vec)
        
    num_elites = int(pop_size * elite)
    
    for k in range(max_iter):
        scores = [(costf(v), v) for v in pop]
        scores.sort()
        print scores[0][0]
        ranked_pop = [v for (s,v) in scores]
        
        pop = ranked_pop[0:num_elites]
        
        while len(pop) < pop_size:
            if random.random() < mutprob:
                idx = random.randint(0,num_elites)
                pop.append(mutate(ranked_pop[idx]))
            else:
                idx1 = random.randint(0,num_elites)
                idx2 = random.randint(0,num_elites)
                pop.append(crossover(ranked_pop[idx1], ranked_pop[idx2]))
                
    return scores[0]
            
    
    
