'''
Created on Jan 8, 2016
@author: hanhanwu
Using K Nearest Neighbor to get similar items for a new item
'''
import mock_Chinese_stock_price
import euclidean
import math

# get distance between the new data and the training data set, distance calculation methods is euclidean by default
def get_sorted_distances(training_data, new_data, distance_f = euclidean.euclidean):
    dist_list = []
    for i in range(len(training_data)):
        v2 = training_data[i]['input']
        dist_list.append((distance_f(new_data, v2), i))
    dist_list = sorted(dist_list)
    
    return dist_list

# KNN returns the average of the top k
def get_KNN(training_data, new_data, distance_f = euclidean.euclidean, k = 5):
    sorted_dists = get_sorted_distances(training_data, new_data, distance_f)
    avge = 0.0
    
    for i in range(k):
        idx = sorted_dists[i][1]
        avge += training_data[idx]['price']
        
    avge = avge/k
    return avge


# convert distances to weights, 3 methods. Based on "the weight will decline when the distance increases"
# method 1: inverse weight
# the added const is useful when items are quite similar that very small distance will lead to infinite weight
def inverse_weight(num = 1.0, const = 0.1, dist = 10):
    return num/(dist + const)
 
# method 2: subtract weight  
def subtract_weight(dist = 10, const = 1.0):
    weight = const - dist
     
    if weight < 0:
        return 0
    return weight

# method 3: Gaussian weight
def gaussian_weight(dist = 10, sigma = 10.0):
    return pow(math.e, -pow(dist, 2)/pow(sigma, 2))
        

def get_weightedKNN(training_data, new_data, distance_f = euclidean.euclidean, k = 5, weight_f = gaussian_weight):
    sorted_dists = get_sorted_distances(training_data, new_data, distance_f)
    avge = 0.0
    total_weight = 0.0
    
    for i in range(k):
        idx = sorted_dists[i][1]
        weight = weight_f(dist=sorted_dists[i][0])
        avge += weight*training_data[idx]['price']
        total_weight += weight
        
    avge = avge/total_weight
    return avge


def main():
    training_data = mock_Chinese_stock_price.get_stockset()
    
    # KNN without weight
    print 'using un-weighted KNN'
    print get_KNN(training_data, (9, 2, 12), k = 3)
    print get_KNN(training_data, (5, 3, 7), k = 3)
    
    # KNN with weight
    print 'weighted KNN using Gaussian function'
    print get_weightedKNN(training_data, (9, 2, 12))
    print get_weightedKNN(training_data, (9, 2, 12), weight_f = gaussian_weight)
    
if __name__ == '__main__':
    main()
