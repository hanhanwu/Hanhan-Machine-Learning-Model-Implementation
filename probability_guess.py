'''
Created on Jan 17, 2016
@author: hanhanwu
Provide probabilities of an item belongs to a given range by analyzing its neighbors
The probability is calculated by using the sum the neighbor weight within the range divided by the total neighbor weight
Then plot the probability
accumulative probability: show a probability less than a given value
'''
import KNN
import mock_Chinese_stock_price
from pylab import *

def prob_guess(data, new_item, low, high, k=5, weightf = KNN.gaussian_weight):
    # get sorted distance list
    dlist = KNN.get_sorted_distances(data, new_item)
    top_k = dlist[0:k]
    
    rweight = 0.0
    total_weight = 0.0
    
    for i in range(k):
        dt = top_k[i][0]
        weight = weightf(dt)
        idx = top_k[i][1]
        price = data[idx]['price']
        
        if price > low and price < high:
            rweight += weight
        total_weight += weight
    if total_weight == 0:
        return 0
    return rweight/total_weight
    
    
def accumulative_plot(data, vec, upperbound, k = 5, weightf = KNN.gaussian_weight):
    t = arange(0.0, upperbound, 0.1)
    cprob = array([prob_guess(data, vec, 0.0, v, k, weightf) for v in t])
    plot(t, cprob)
    show()
    

def main():
    data = mock_Chinese_stock_price.get_stockset()
    print prob_guess(data, (9, 2, 12), 10, 100)
    print prob_guess(data, (3, 2, 5), 10, 100)
    print prob_guess(data, (3, 2, 5), 1, 10)
    
    # plot using accumulative probability
    accumulative_plot(data, (9, 2, 12), 100)
if __name__ == '__main__':
    main()

