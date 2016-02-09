'''
Created on Feb 8, 2016

@author: hanhanwu
'''
import math
import load_match_data
import preprocess_data

def sumsqures(v):
    return sum([p**2 for p in v])

# radial-basis function, used as a kernel to get best linear separation for a given data set with proper adjustments
def rbf(v1, v2, gamma=20):
    dv = [v1[i]-v2[i] for i in range(len(v1))]
    squared_dist = sumsqures(dv)
    return math.e**(-gamma*squared_dist)

# With kernel function, we won't calculate the new locations of points in the new transformed space, threfore
# it dones't make sense to calculate the new data with the average of the existing data set.
# But, by calculating the distances between the new data and the existing points in the data set, then do the average
# will get the same result.
def nlclassify(new_v, rs, offset, gamma=10):
    sum0, sum1, count0, count1 = 0.0, 0.0, 0.0, 0.0
    
    for r in rs:
        if r.match == 0:
            sum0 += rbf(new_v, r.data, gamma)
            count0 += 1
        elif r.match == 1:
            sum1 += rbf(new_v, r.data, gamma)
            count1 += 1
            
    y = sum0/count0 -sum1/count1 + offset
    
    if y > 0: return 0
    return 1


def get_offset(rs, gamma=10):
    r0 = []
    r1 = []
    count0 = 0.0
    count1 = 0.0
    
    for r in rs:
        if r.match == 0:
            r0.append(r.data)
        elif r.match == 1:
            r1.append(r.data)
            
    sum0 = sum(sum(rbf(v1, v2, gamma) for v1 in r0) for v2 in r0)
    sum1 = sum(sum(rbf(v1, v2, gamma) for v1 in r1) for v2 in r1)
    
    return sum1/(len(r1)**2) - sum0/(len(r0)**2)
    

def main():
    print 'use agesonly.csv to predict:'
    agesonly_path = '[your agesonly.csv path]'  # change to your agesonly.csv path
    agesonly_rows = load_match_data.load_csv(agesonly_path, True)
    offset1 = get_offset(agesonly_rows)
    print nlclassify([27, 30], agesonly_rows, offset1)
    print nlclassify([30, 27], agesonly_rows, offset1)
    
    print 'use scaled matchmaker.csv to predict:'
    matchmaker_path = '[your matchmaker.csv path]'  # change to your matchmaker.csv path
    ls = file(matchmaker_path)
    numerical_rows = preprocess_data.to_numerical(ls)
    rescaled_data = preprocess_data.rescale_data(numerical_rows)
    offset2 = get_offset(rescaled_data)
    new_p1 = [28.0, -1, -1, 26.0, -1, 1, 2, 0.8]   # man doesn't want children, women wants
    new_p2 = [28.0, -1, 1, 26.0, -1, 1, 2, 0.8]   # both want children
    print nlclassify(new_p1, rescaled_data, offset2)
    print nlclassify(new_p2, rescaled_data, offset2)
    
    
    
if __name__ == '__main__':
    main()
