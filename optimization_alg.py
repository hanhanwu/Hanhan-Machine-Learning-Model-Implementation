'''
Created on Jan 11, 2016
@author: hanhanwu
using annealing optimization here
The algorithm starts from very high temperature (the willingness to accept a worse solution)
this algorithm is willing to accept a worse solution near the beginning of the process,
but later will become less and less likely to accept worse solution,
till the end, it only accepts better solutions
'''
import random as rd
import math
import heterogeneous_data
import mock_Chinese_stock_price
import cross_validation
import KNN
import numpy as np


# annealing optimization
# domain if the value range for each attribute
def annealing_opt(domain, costf, T = 10000.0, cool = 0.95, step = 5):
    # random initialize the Vector
    vec = [rd.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
    
    # randomly choose a direction
    dir = rd.randint(-step, step)
    
    # randomly choose an index
    i = rd.randint(0, len(domain)-1)
    
    while T > 0.1:
        vec_new = vec
        vec_new[i] += dir
        if vec_new[i] < domain[i][0]: vec_new[i] = domain[i][0]
        elif vec_new[i] > domain[i][1]: vec_new[i] = domain[i][1]
        error_old = costf(vec)
        error_new = costf(vec_new)
        p = pow(math.e, (-error_new-error_old)/T)
        
        if (error_new < error_old or rd.random() < p):
            vec = vec_new
            
        T *= cool
        print T
    
    return vec 


# genetic optimization
# elite_frac is the fraction of good solutions in the population
def genetic_optimization(domain, costf, generations_num=100, population_size=50, prob_mutation=0.4, elite_frac=0.2, step=1):
    def mutation(vec):
        mutate_idx = rd.randint(0, len(vec)-1)
        if rd.random() < 0.5 and vec[mutate_idx] > domain[mutate_idx][0]:
            return vec[0:mutate_idx] + [vec[mutate_idx]+step] + vec[mutate_idx+1:]
        elif vec[mutate_idx] < domain[mutate_idx][1]:
            return vec[0:mutate_idx] + [vec[mutate_idx]-step] + vec[mutate_idx+1:]
        return vec
    
    def crossover(vec1, vec2):
        cross_idx = rd.randint(1, len(vec1)-2)
        return vec1[0:cross_idx] + vec2[cross_idx:]
    
    # initialize population
    population = []
    for i in range(population_size):
        pv = [rd.randint(domain[j][0], domain[j][1]) for j in range(len(domain))]
        population.append(pv)
        
    num_elites = int(population_size*elite_frac)
        
    for k in range(generations_num):
        scores = [(costf(v), v) for v in population]
        # sort by the cost(key), get the winners
        scores.sort()
        ranked = [v for (c,v) in scores]
        population = ranked[0:num_elites]
        
        # Each generation has the same number of population
        while len(population) < population_size:
            if rd.random() < prob_mutation:
                # do mutation
                v_idx = rd.randint(0, num_elites)
                population.append(mutation(ranked[v_idx])) 
            else:
                # do crossover
                v1_idx = rd.randint(0,num_elites)
                v2_idx = rd.randint(0,num_elites)
                population.append(crossover(ranked[v1_idx], ranked[v2_idx]))
            
            # print current best score
        print 'current best score and the vector: ', scores[0]
        allscores = [c for (c,v) in scores]
        current_avg_score = np.average(allscores)
        print 'current average score: ', current_avg_score
            
        # print final best score
    print 'best score and the vector: ', scores[0][0]
    return scores[0][1]
        

# return the cost function
def generatecostf(scale, data, algr, trails):
    def costf(scale):
        rescaled_data = heterogeneous_data.rescale(data, scale)
        cost = cross_validation.cross_validate(data, algr, trails)
        return cost
    return costf


def main():
    scale = [10, 10, 0.00001, 0]
    heterogeneous_data, min_max = mock_Chinese_stock_price.get_stockset_various()
    costf = generatecostf(scale, heterogeneous_data, algr=KNN.get_KNN, trails=10)
#     annealing_optimized_result = annealing_opt(min_max, costf)
#     print 'using annealing optimizaton: [rating, age, duration, investment, employee_number]', annealing_optimized_result
    
    genetic_optimized_resule = genetic_optimization(min_max, costf)
    print 'using genetic optimizaton: [rating, age, duration, investment, employee_number]', genetic_optimized_result
    
if __name__ == '__main__':
    main()
    
