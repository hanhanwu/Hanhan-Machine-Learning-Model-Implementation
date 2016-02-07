'''
Created on Feb 1, 2016
@author: hanhanwu
1. Convert nominal data into numerical data since classifiers only deal with numerical data
2. Using geopy to get latitude, longitude based on the address, and measure geo-distance  (Python libraries is so powerful)
geopy provides 2 formulas to calculate distances: great-circle and vincenty, I am using vincenty since it is more accurate
3. Rescale Data: for each column, vonvert the data into [0,1] range based on their min, max, in this way, for each row, 
they all share the same scale too
'''
import Levenshtein
import sys
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
import load_match_data
from matplotlib.mlab import recs_join
import linear_classifier


def yes_or_no(asw):
    if asw == 'yes': return 1
    elif asw == 'no': return -1
    else: return 0


def hobby_hierarchy():
    hobby_dict = {}
    hobby_dict['art'] = ['fashion', 'art', 'photography', 'opera']
    hobby_dict['indoor'] = ['scrabble', 'cooking', 'reading', 'writing', 'knitting', 'tv', 'computers', 'movies']
    hobby_dict['outdoor'] = ['skiing', 'shopping', 'camping', 'dancing', 'travel', 'football', 'running', 'soccer', 'snowboarding']
    hobby_dict['animal'] = ['animals']
    
    return hobby_dict


def same_category(h1, h2):
    hobby_dict = hobby_hierarchy()
    
    for k,v in hobby_dict.items():
        if h1 in v and h2 in v:
            return True
    return False
    

def common_hobby_score(h1_lst, h2_lst):
    score  = 0
    if len(h1_lst) == 0 or len(h2_lst) == 0:
        return 0
    for h1 in h1_lst:
        for h2 in h2_lst:
            # using Levenshtein helps find same items with different naming or created by spelling mistakes
            lev_ratio = Levenshtein.ratio(h1, h2)
            if lev_ratio >= 0.8:
                score += 1
                break     # using break, we can avoid repeatedly using same items to add the score
            elif same_category(h1, h2) == True:
                score += 0.8
                break
    return score

def get_hobbies(h1_str, h2_str):
    h1_lst = h1_str.split(':')
    h2_lst = h2_str.split(':')
    
    return h1_lst, h2_lst
    
def calculate_distance(add1, add2):
    geolocator = Nominatim()
    
    location1 = geolocator.geocode(add1)
    al1 = (location1.latitude, location1.longitude)
    
    location2 = geolocator.geocode(add2)
    al2 = (location2.latitude, location2.longitude)
    
    distce = vincenty(al1, al2).miles
    return distce


def to_numerical(f):
    numerical_rows = []
    
    for l in f:
        new_row = []
        elems = l.split(',')
        new_row.append(float(elems[0]))
        new_row.append(float(elems[5]))
        for i in [1,2,6,7]:
            new_row.append(yes_or_no(elems[i]))
        new_row.append(common_hobby_score(elems[3], elems[8]))
        new_row.append(calculate_distance(elems[4], elems[9]))
        new_row.append(int(elems[-1]))
        print new_row
        
        numerical_rows.append(new_row)
    return numerical_rows

        
        
def rescale_data(numerical_rows):
    results = []
    row_num = len(numerical_rows[0])
    maxs = [-sys.maxint-1]*row_num
    mins = [sys.maxint]*row_num
    
    # get max, min for each column
    for r in numerical_rows:
        for i in range(row_num):
            if r[i] > maxs[i]: maxs[i] = r[i]
            if r[i] < mins[i]: mins[i] = r[i]
                       
    # rescale each row
    for r in numerical_rows:
        for i in range(row_num):
            if maxs[i] == mins[i]: r[i] = 0
            else: r[i] = float(r[i] - mins[i])/(maxs[i]-mins[i])
        results.append(load_match_data.matchrow(r, all_num=True))
            
    return results
    


def main():
    l1 = '39,yes,no,skiing:knitting:dancing,220 W 42nd St New York NY,43,no,yes,soccer:reading:scrabble,824 3rd Ave New York NY,0'
    l2 = '23,no,no,football:fashion,102 1st Ave New York NY,30,no,no,snowboarding:knitting:computers:shopping:tv:travel,151 W 34th St New York NY,1'
    ans1 = l1.split(',')
    ans2 = l2.split(',')
    
    h1_lst1, h2_lst1 = get_hobbies(ans1[3], ans1[8])
    print h1_lst1
    print h2_lst1
    score1 = common_hobby_score(h1_lst1, h2_lst1)
    print score1
    print '*******************'
    
    h1_lst2, h2_lst2 = get_hobbies(ans2[3], ans2[8])
    print h1_lst2
    print h2_lst2
    score2 = common_hobby_score(h1_lst2, h2_lst2)
    print score2
    
    print '*******************'
    add1 = ans1[4]
    add2 = ans1[9]
    print 'distance between ', add1, ' and ', add2, 'is: ', str(calculate_distance(add1, add2))
    
    print '*******************covert all the data to numerical*******************'
    matchmaker_path = '[your matchmaker.csv path]'  # change to your matchmaker.csv path
    ls = file(matchmaker_path)
    numerical_rows = to_numerical(ls)
    print len(numerical_rows)
    print numerical_rows[0]
    
    print '*******************rescale data*******************'
    rescaled_data = rescale_data(numerical_rows)
    for r in rescaled_data:
        print r.data, ', ', r.match
        
    print '*******************train rescale data*******************'
    print 'class cenetrs'
    averages = linear_classifier.train_data(rescaled_data)
    for k,v in averages.items():
        print k, v
        
    print 'classify new points'
    testing_point = [43.0, 35.0, -1, 1, -1, 1, 15, 1.6189873022356103]
    print linear_classifier.classify_dp(testing_point, averages)

    
if __name__ == '__main__':
    main()
