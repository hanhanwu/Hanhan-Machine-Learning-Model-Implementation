'''
Created on Jan 8, 2016
@author: hanhanwu
Using K Nearest Neighbor to get similar items for a new item
'''
import mock_Chinese_stock_price
import euclidean

# get distance between the new data and the training data set, distance calculation methods is euclidean by default
def get_sorted_distances(training_data, new_data, distance = 'euclidean'):
    dist_list = []
    for i in range(len(training_data)):
        v2 = training_data[i]['input']
        dist_list.append((euclidean.euclidean(new_data, v2), i))
    dist_list = sorted(dist_list)
    
    return dist_list

# KNN returns the average of the top k
def get_KNN(training_data, new_data, distance = 'euclidean', k = 5):
    sorted_dists = get_sorted_distances(training_data, new_data)
    avge = 0.0
    
    for i in range(k):
        idx = sorted_dists[i][1]
        avge += training_data[idx]['price']
        
    avge = avge/k
    return avge
        

def main():
    training_data = mock_Chinese_stock_price.get_stockset()
    print get_KNN(training_data, (9, 2, 12), k = 3)
    print get_KNN(training_data, (5, 3, 7), k = 3)
    
if __name__ == '__main__':
    main()
