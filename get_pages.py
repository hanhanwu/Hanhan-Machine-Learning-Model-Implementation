'''
Created on Feb 15, 2016
@author: hanhanwu
test how to get urls from a web page, and get urls from each url
just for wiki english pages
'''
# from urllib2 import urlopen
import  urllib2
from bs4 import BeautifulSoup
from urlparse import urljoin
from sets import Set
import re

seed_page = 'https://en.wikipedia.org/wiki/Recommender_system'
wiki_prefix1 = 'https://en.wikipedia.org'
wiki_prefix2 = 'https:'

ignorewords = Set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it'])
foreign_filter = ['ca', 'cs', 'de', 'es', 'fa', 'fr', 'ko', 'he', 'hu', 'ja', 'pt', 'ru', 'sr', 'fi', 'sv', 'uk', 'zh']
seed_page = urllib2.urlopen('https://en.wikipedia.org/wiki/Recommender_system')
contents = seed_page.read()
soup = BeautifulSoup(contents, 'lxml')
links = soup('a')
crawled_links = Set()

def url_editor(hrf):
    if hrf == '/wiki/Main_Page': return None
    if hrf.startswith('#') or hrf.startswith('/w/index.php'): 
        return None
    m = re.search('//(\w+)\.wikipedia\.org.*?', hrf)
    if m != None:
        if m.group(1) in foreign_filter: return None
        
    return hrf

for link in links:
    if 'href' in dict(link.attrs):
        hrf = link['href']
        edited_url = url_editor(hrf)
        if edited_url != None:
            print edited_url
        

        
    

