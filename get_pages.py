'''
Created on Feb 15, 2016
@author: hanhanwu
test how to get urls from a web page, and get urls from each url
just for wiki pages
'''
# from urllib2 import urlopen
import  urllib2
from bs4 import BeautifulSoup
from urlparse import urljoin
from sets import Set

seed_page = 'https://en.wikipedia.org/wiki/Recommender_system'
wiki_prefix = 'https://en.wikipedia.org'

ignorewords = Set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it'])
seed_page = urllib2.urlopen('https://en.wikipedia.org/wiki/Recommender_system')
contents = seed_page.read()
soup = BeautifulSoup(contents, 'lxml')
links = soup('a')
for link in links:
    if 'href' in dict(link.attrs):
        print link



