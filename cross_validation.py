'''
Created on Jan 9, 2016
@author: hanhanwu
'''
import random
import mock_Chinese_stock_price
import KNN

# 5 percent testing data by default
def divide_data(data_set, test_precent = 0.05):
    training_data = []
    testing_data = []
    
    for i in range(len(data_set)):
        if random.random() < test_precent:
            testing_data.append(data_set[i])
        else:
            training_data.append(data_set[i])
            
    return training_data, testing_data

def get_error_per_trail(training_data, testing_data, algr):
    error = 0.0
    for i in range(len(testing_data)):
        calculated_result = algr(training_data, testing_data[i]['input'])
        ground_truth = testing_data[i]['price']
        error += pow((calculated_result - ground_truth), 2)
        
    error /= len(testing_data)
    return error 

def cross_validate(data_set, algr, trails = 100):
    total_error = 0.0
    
    for i in range(trails):
        training_data, testing_data = divide_data(data_set)
        total_error += get_error_per_trail(training_data, testing_data, algr)
        
    total_error /= trails
    return total_error


def main():
    data_set = mock_Chinese_stock_price.get_stockset()
    cv_total_error_unweighted = cross_validate(data_set, algr = KNN.get_KNN, trails=200)
    cv_total_error_weighted = cross_validate(data_set, algr = KNN.get_weightedKNN, trails=200)
    
    print 'cross validation, using un-weighted KNN: ', cv_total_error_unweighted
    print 'cross validation, using weighted KNN: ', cv_total_error_weighted
    
    
if __name__ == '__main__':
    main()
