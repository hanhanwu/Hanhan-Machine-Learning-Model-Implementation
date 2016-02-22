'''
Created on Feb 13, 2016
@author: hanhanwu
Using sqlite3 as database
Download sqlite here: http://www.sqlite.org/download.html
Opern your terminal, cd to the sqlite folder, type "sqlite3"
'''
from sqlite3 import dbapi2 as sqlite
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

class crawler:
    def __init__(self, dbname):
        self.con = sqlite.connect(dbname)
    
    def __del__(self):
        self.con.close()
    
    def dbcommit(self):
        self.con.commit()
    
    # Get table row id of an item, if not exist, insert it into table and return the relative row id
    def get_row_id(self, table, field, value):
        rid = self.con.execute("select rowid from %s where %s='%s'" % (table, field, value)).fetchone()
        if rid == None:
            new_insert = self.con.execute("insert into %s (%s) values ('%s')" % (table, field, value))
            return new_insert.lastrowid
        return rid[0]
    
    # add this page urlid, wordid of each word in this page into wordlocation table
    def add_to_index(self, url, page_text, ignore_wrods):
        if self.is_indexed(url): return
        
        print 'indexing ', url
        uid = self.get_row_id('urllist', 'url', url)
        
        for i in range(len(page_text)):
            w = page_text[i]
            if w in ignore_wrods: continue
            wid = self.get_row_id('wordlist', 'word', w)
            self.con.execute('insert into wordlocation (urlid, wordid, location) values (%d,%d,%d)' % (uid, wid, i))
        
        
    # check whether this page url has been indexed in urllist table and wordlocation table
    def is_indexed(self, url):
        u = self.con.execute("select rowid from urllist where url='%s'" % url).fetchone()
        if u != None:
            w = self.con.execute("select * from wordlocation where urlid=%d" % u[0]).fetchone()
            if w != None: return True
        return False    
    
    def url_editor(self, hrf):
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

    def get_textonly(self, sp):
        all_text = sp.text
        splitter = re.compile('\\W*')
        stemmer = PorterStemmer()
        text_lst = [stemmer.stem(s.lower()) for s in splitter.split(all_text) if s!='']
        return text_lst
    
    # start from a list of pages, do BFS (breath first search) to the given depth; collect direct sources along the way
    def crawl(self, pages, depth=2):
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
                page_text = self.get_textonly(soup)
                page_records.append(PageRecord(p, page_text))
            
                for link in links:
                    if 'href' in dict(link.attrs):
                        hrf = link['href']
                        edited_url = self.url_editor(hrf)
                        if edited_url != None:
                            if 'wiki' in edited_url and edited_url not in all_pages:
                                page_connections.append(PageConnection(p, edited_url))
                                crawled_links.add(edited_url)
                            else: direct_sources.add(edited_url)
            for new_link in crawled_links:
                print new_link
            pages = crawled_links
            
        return direct_sources, page_connections, page_records
    
    # create database tables and indexes
    def create_index_tables(self):
        self.con.execute('create table if not exists urllist(url)')
        self.con.execute('create table if not exists wordlist(word)')
        self.con.execute('create table if not exists wordlocation(urlid, wordid, location)')
        self.con.execute('create table if not exists link(fromid integer, toid integer)')
        self.con.execute('create table if not exists linkwords(wordid, linkid)')
         
        self.con.execute('create index if not exists wordidx on wordlist(word)')
        self.con.execute('create index if not exists urlidx on urllist(url)')
        self.con.execute('create index if not exists wordurlidx on wordlocation(wordid)')
        self.con.execute('create index if not exists urltoidx on link(toid)')
        self.con.execute('create index if not exists urlfromidx on link(fromid)')
        
        self.dbcommit()
    
    
def main():
    ignorewords = Set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it'])
    
    # create tables and the indexes
    dbname = 'searchindex.db'
    mycrawler = crawler(dbname)
    mycrawler.create_index_tables()
    
    # crawl the pages using a set of seed pages
    seed_pages = ['https://en.wikipedia.org/wiki/Recommender_system']
    direct_sources, page_connections, page_records = mycrawler.crawl(seed_pages)
    print '***********direct sources***********'
    for ds in direct_sources:
        print ds
    print '***********page connections***********'
    for pc in page_connections:
        print pc.page_from,', ', pc.page_to
    print '***********page records***********'
    for pr in page_records:
        print pr.page_url,', ', str(len(pr.page_text))
        
    # add page url and the page text into wordlocation table, the urllist, wordlist tables will be inserted along the way
    for pr in page_records:
        mycrawler.add_to_index(pr.page_url, pr.page_text, ignorewords)
        
if __name__ == '__main__':
    main()
