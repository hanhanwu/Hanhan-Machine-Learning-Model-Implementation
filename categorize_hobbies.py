from __future__ import print_function
'''
Created on Feb 1, 2016
@author: hanhanwu
analysis the hobbies and create hobby hierarchy
In reality, if we have more data and can find attributes of the category, we can try 
Jaccard Similarity to calculate the similarity of the categories, items. Then the hierarchy will be more accurate.
'''
from sets import Set

def hobby_hierarchy():
    hobby_dict = {}
    hobby_dict['art'] = ['fashion', 'art', 'photography', 'opera']
    hobby_dict['indoor'] = ['scrabble', 'cooking', 'reading', 'writing', 'knitting', 'tv', 'computers', 'movies']
    hobby_dict['outdoor'] = ['skiing', 'shopping', 'camping', 'dancing', 'travel', 'football', 'running', 'soccer', 'snowboarding']
    hobby_dict['animal'] = ['animals']
    
    return hobby_dict


def main():
     matchmaker_path = '[use your matchmaker.csv path]'  # change to your matchmaker.csv path
     f = file(matchmaker_path)
     
     hobby_dict = hobby_hierarchy()
     print (hobby_dict, end="")
     
     hobby_list = []
     
     for l in f:
         ans = l.split(',')
         hobbies_str = ans[3]+':'+ ans[8]
         hobbies = hobbies_str.split(':')
         hobby_list.extend(hobbies)
     unique_hobby = Set(filter(lambda x: x!='',hobby_list))
     unique_hobby = list(unique_hobby)
     ct = len(unique_hobby)
     for i in range(ct):
         print(unique_hobby[i]+' ', end="")
         if i%7==0: print('\n')

        
    
if __name__ == '__main__':
    main()
