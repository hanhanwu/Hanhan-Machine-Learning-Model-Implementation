'''
Created on Feb 1, 2016
@author: hanhanwu
convert nominal data into numerical data since classifiers only deal with numerical data
'''
import Levenshtein


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

def get_hobbies(l):
    hobby_list = []
    ans = l.split(',')
    h1_lst = ans[3].split(':')
    h2_lst = ans[8].split(':')
    
    return h1_lst, h2_lst
    

def main():
    l1 = '39,yes,no,skiing:knitting:dancing,220 W 42nd St New York NY,43,no,yes,soccer:reading:scrabble,824 3rd Ave New York NY,0'
    l2 = '23,no,no,football:fashion,102 1st Ave New York NY,30,no,no,snowboarding:knitting:computers:shopping:tv:travel,151 W 34th St New York NY,1'
    
    h1_lst1, h2_lst1 = get_hobbies(l1)
    print h1_lst1
    print h2_lst1
    score1 = common_hobby_score(h1_lst1, h2_lst1)
    print score1
    print '*******************'
    
    h1_lst2, h2_lst2 = get_hobbies(l2)
    print h1_lst2
    print h2_lst2
    score2 = common_hobby_score(h1_lst2, h2_lst2)
    print score2
    
if __name__ == '__main__':
    main()
