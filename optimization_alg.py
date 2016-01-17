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



# return the cost function
def generatecostf(scale, data, algr, trails):
    def costf(scale):
        rescaled_data = heterogeneous_data.rescale(data, scale)
        cost = cross_validation.cross_validate(data, algr, trails)
        return cost
    return costf


def main():
    scale_annealing = [10, 10, 0.00001, 0]
    heterogeneous_data, min_max = mock_Chinese_stock_price.get_stockset_various()
    costf = generatecostf(scale_annealing, heterogeneous_data, algr=KNN.get_KNN, trails=10)
    annealing_optimized_result = annealing_opt(min_max, costf)
    print 'using annealing optimizaton: [rating, age, duration, investment, employee_number]', annealing_optimized_result
    
if __name__ == '__main__':
    main()
    
