'''
Created on Jan 31, 2016
@author: hanhanwu
Linear Classifier finds the average of each class and constructs points for each center,
when the new data come in, they will be classified into the group of the closest center.
'''
import load_match_data
from pylab import *

# The classes in this code is 0 or 1, "match" attribute of the data
# calculate the average of each class
def train_data(rows):
    class_averages = {}
    class_counts = {}
    
    for r in rows:
        cls = r.match
        
        class_averages.setdefault(cls, [0.0]*len(r.data))
        class_counts.setdefault(cls, 0)
        
        for i in range(len(r.data)):
            class_averages[cls][i] += r.data[i]
            class_counts[cls] += 1
        
    for cls, dt in class_averages.items():
        ct = class_counts[cls]
        class_averages[cls] = [elem/ct for elem in class_averages[cls]]
    
    return class_averages


# dot product: multiple numbers of 2 vectors in the same position, then sum them up
def get_dotproduct(v1, v2):
    return sum(v1[i]*v2[i] for i in range(len(v1)))


# this function only used for class 0 and class 1
# formula = (X - (M0+M1)/2)*(M0-M1) = XM0 -XM1 + (M1M1 - M0M0)/2, the formula is used to classify new vector X
def classify_dp(new_vec,averages):
    M0 = averages[0]
    M1 = averages[1]
    
    result = get_dotproduct(new_vec, M0) - get_dotproduct(new_vec, M1) 
    + (get_dotproduct(M1, M1) - get_dotproduct(M0, M0))/2
    
    if result > 0:
        return 0    # class 0
    else:
        return 1    # class 1
    


def main():
    agesonly_path = '[your own agesonly.csv path]'    # download agesonly.csv and change to your own path
    agesonly_rows = load_match_data.load_csv(agesonly_path, True)
    
    print 'class cenetrs'
    averages = train_data(agesonly_rows)
    for k,v in averages.items():
        print k, v
        
    print 'classify new points'
    print classify_dp([18,30], averages)
    print classify_dp([27,30], averages)
    print classify_dp([30,27], averages)
    print classify_dp([25,80], averages)
    
    
    
if __name__ == '__main__':
    main()
