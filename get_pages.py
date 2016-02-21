'''
Created on Feb 15, 2016
@author: hanhanwu
The code aims at collecting urls in an indicated academic topics, 
academic papers, related news, links will be put into a set of direct_resource
* Get urls from the seed web page, and get urls from each url, how many layers to on depends o the defined depth
* Return:
    direct_sources - the sources read for research directly
    page_connections - the from page and the to page
    page_records - the page url and its text
Just for wiki english pages
'''
import  urllib2
from bs4 import BeautifulSoup
from sets import Set
import re
from nltk.stem.porter import *

class PageConnection:
    def __init__(self, page_from, page_to):
        self.page_from = page_from
        self.page_to = page_to
        
class PageRecord:
    def __init__(self, page_url, page_text):
        self.page_url = page_url
        self.page_text = page_text

def url_editor(hrf):
    wiki_prefix1 = 'https://en.wikipedia.org'
    wiki_prefix2 = 'https:'
    foreign_filter = ['ca', 'cs', 'de', 'es', 'fa', 'fr', 'ko', 'he', 'hu', 'ja', 'pt', 'ru', 'sr', 'fi', 'sv', 'uk', 'zh']
    
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

def get_textonly(sp):
    all_text = sp.text
    splitter = re.compile('\\W*')
    stemmer = PorterStemmer()
    text_lst = [stemmer.stem(s.lower()) for s in splitter.split(all_text) if s!='']
    return text_lst

def crawl(pages, depth=2):
    all_pages = Set()
    
    direct_sources = Set()
    page_connections = []
    page_records = []
    
    for d in range(depth):
        crawled_links = Set()
        all_pages.update(pages)
        for p in pages:
            try:
                page = urllib2.urlopen(p)
            except:
                print 'Cannot open: ',p
                continue
            contents = page.read()
            soup = BeautifulSoup(contents, 'lxml')
            links = soup('a')
            page_text = get_textonly(soup)
            page_records.append(PageRecord(p, page_text))
        
            for link in links:
                if 'href' in dict(link.attrs):
                    hrf = link['href']
                    edited_url = url_editor(hrf)
                    if edited_url != None:
                        if 'wiki' in edited_url and edited_url not in all_pages:
                            page_connections.append(PageConnection(p, edited_url))
                            crawled_links.add(edited_url)
                        else: direct_sources.add(edited_url)
        for new_link in crawled_links:
            print new_link
        pages = crawled_links
        
    return direct_sources, page_connections, page_records
            
   
   
def main():
    seed_pages = ['https://en.wikipedia.org/wiki/Recommender_system']
    direct_sources, page_connections, page_records = crawl(seed_pages)
    print '***********direct sources***********'
    for ds in direct_sources:
        print ds
    print '***********page connections***********'
    for pc in page_connections:
        print pc.page_from,', ', pc.page_to
    print '***********page records***********'
    for pr in page_records:
        print pr.page_url,', ', str(len(pr.page_text))
    
    
if __name__ == '__main__':
    main()
