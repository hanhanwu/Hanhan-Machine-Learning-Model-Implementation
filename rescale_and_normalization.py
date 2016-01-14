'''
Created on Jan 13, 2016
@author: hanhanwu
'''
import mock_Chinese_stock_price
import cross_validation
import KNN

def rescale(data_set, scale):
    scaled_data = []
    for row in data_set:
        scaled_input = [row['input'][i]*scale[i] for i in range(len(scale))]
        scaled_data.append({'input': scaled_input, 'price': row['price']})
    return scaled_data

def normalization(data_set, min_max):
    normalized_data = []
    for row in data_set:
        normalized_input = [float(row['input'][i]-min_max[i][0])/(min_max[i][1]-min_max[i][0]) for i in range(len(min_max))]
        normalized_data.append({'input': normalized_input, 'price': row['price']})
    return normalized_data
          

def main():
    # when the attributes have different data range
    heterogeneous_data, min_max = mock_Chinese_stock_price.get_stockset_various()
    
    # in this dataset, I have added investment, and employee number, 
    # they all have large numbers and will influence the results significantly without normalization, 
    # then those more important attributes with smaller values may not influence the result and the final result cannot be accurate
    print 'before re-scale/normalization'
    cv_total_error_unweighted = cross_validation.cross_validate(heterogeneous_data, algr = KNN.get_KNN, trails=100)
    cv_total_error_weighted = cross_validation.cross_validate(heterogeneous_data, algr = KNN.get_weightedKNN, trails=100)
    print 'cross validation, using un-weighted KNN: ', cv_total_error_unweighted
    print 'cross validation, using weighted KNN: ', cv_total_error_weighted
    
    print 'after re-scale'
    scale = [10, 10, 0.00001, 0]
    scaled_data = rescale(heterogeneous_data, scale)
    scaled_cv_total_error_unweighted = cross_validation.cross_validate(scaled_data, algr = KNN.get_KNN, trails=100)
    scaled_cv_total_error_weighted = cross_validation.cross_validate(scaled_data, algr = KNN.get_weightedKNN, trails=100)
    print 'cross validation, using un-weighted KNN: ', scaled_cv_total_error_unweighted
    print 'cross validation, using weighted KNN: ', scaled_cv_total_error_weighted
    
    print 'after normalization'
    normalized_data = normalization(heterogeneous_data, min_max)
    normalized_cv_total_error_unweighted = cross_validation.cross_validate(normalized_data, algr = KNN.get_KNN, trails=100)
    normalized_cv_total_error_weighted = cross_validation.cross_validate(normalized_data, algr = KNN.get_weightedKNN, trails=100)
    print 'cross validation, using un-weighted KNN: ', normalized_cv_total_error_unweighted
    print 'cross validation, using weighted KNN: ', normalized_cv_total_error_weighted
    
if __name__ == '__main__':
    main()
