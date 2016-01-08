'''
Created on Jan 7, 2016
@author: hanhanwu
calculating euclidean distance between 2 items, the input vector of each item contains the attributes of the item
'''
import mock_Chinese_stock_price
import math

# v1, v2 must have same attributes
def euclidean(v1, v2):
    dist = 0
    for i in range(len(v1)):
        dist += pow((v1[i]-v2[i]), 2)
    dist = math.sqrt(dist)
    return dist
    
    
def main():
    test_dataset = mock_Chinese_stock_price.get_stockset()
    v1 = test_dataset[0]['input']
    v2 = test_dataset[1]['input']
    print v1
    print v2
    print euclidean(v1, v2)
    
if __name__ == '__main__':
    main()
