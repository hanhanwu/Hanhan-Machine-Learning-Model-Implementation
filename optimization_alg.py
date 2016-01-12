'''
Created on Jan 11, 2016
@author: hanhanwu
using annealing optimization here
The algorithm starts from very high temperature (the willingness to accept a worse solution)
this algorithm is willing to accept a worse solution near the beginning of the process,
but later will become less and less likely to accept worse solution,
till the end, it only accepts better solutions
'''
from random import random, randint

def annealing_opt(domain, costf, T = 10000.0, cool = 0.95, step = 1):
    # random initialize the Vector
    vec = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
    
    # randomly choose a direction
    dir = random.randint(-step, step)
    
    # randomly choose an index
    i = random.randint(0, len(domain)-1)
    
    while T > 0.1:
        vec_new = vec
        vec_new[i] += dir
        if vec_new[i][0] < vec[i][0]: vec_new[i][0] = vec[i][0]
        elif vec_new[i][1] > vec[i][1]: vec_new[i][1] = vec[i][1]
        error_old = costf(vec)
        error_new = costf(vec_new)
        p = pow(math.e, (-error_new-error_old)/T)
        
        if (error_new < error_old or random.random() < p):
            vec = vec_new
            
        T *= cool
    
    return vec
        
        
    
