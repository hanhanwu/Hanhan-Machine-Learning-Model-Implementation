'''
Created on Feb 20, 2016
@author: hanhanwu
using nltk built in PorterStemming Algorithm
'''
from nltk.stem.porter import *


def main():
    words = ['looking', 'look', 'looked', 'lookup', 'sat', 'sit', 'sitting', 'sitted', 'hanhan', 'emmanuel!']
    
    stemmer = PorterStemmer()
    new_words = [stemmer.stem(w) for w in words]
    print new_words
    
if __name__ == '__main__':
    main()
