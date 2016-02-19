'''
Created on Feb 15, 2016
@author: hanhanwu
Get urls from the seed web page, and get urls from each url
The code aims at collecting urls in an indicated academic topics, 
academic papers, related news, links will be put into a set of direct_resource
Just for wiki english pages
In this example, I am trying to get new links about Recommendation System from the seed page, 
and record directed sources like academic papers, news report, demo urls.
'''
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
direct_sources = Set()

def url_editor(hrf):
    if 'wikimedia' in hrf or 'mediawiki' in hrf or 'wikidata' in hrf or 'index.php?' in hrf: 
        return None
    if hrf == '/wiki/Main_Page': return None
    if hrf.startswith('#') or hrf.startswith('/w/index.php'): 
        return None
    m1 = re.search('[\w\W]*/wiki/\w+:[\w\W]*', hrf)
    if m1 != None: return None
    m2 = re.search('//(\w+)\.wikipedia\.org.*?', hrf)
    if m2 != None:
        if m2.group(1) in foreign_filter: return None
    
    if hrf.startswith('/wiki/'):
        hrf = wiki_prefix1+hrf
    elif hrf.startswith('//dx.doi.org'):
        hrf = wiki_prefix2+hrf
    if 'http' not in hrf and 'https' not in hrf: return None
    
    return hrf

for link in links:
    if 'href' in dict(link.attrs):
        hrf = link['href']
        edited_url = url_editor(hrf)
        if edited_url != None:
            if 'wiki' in edited_url: crawled_links.add(edited_url)
            else: direct_sources.add(edited_url)
            
for new_link in crawled_links:
    print new_link
    
print '*************************'
    
for dsource in direct_sources:
    print dsource
    
