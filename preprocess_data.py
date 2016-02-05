'''
Created on Feb 1, 2016
@author: hanhanwu
convert nominal data into numerical data since classifiers only deal with numerical data
Using geopy to get latitude, longitude based on the address, and measure geo-distance  (Python libraries is so powerful)
geopy provides 2 formulas to calculate distances: great-circle and vincenty, I am using vincenty since it is more accurate
'''
import Levenshtein
from geopy.geocoders import Nominatim
from geopy.distance import vincenty

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
                print 'same: ', h1,',', h2
                score += 1
                break     # using break, we can avoid repeatedly using same items to add the score
            elif same_category(h1, h2) == True:
                print 'same category: ', h1,',', h2
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
    
if __name__ == '__main__':
    main()
