'''
Created on Feb 13, 2016
@author: hanhanwu
Using sqlite3 as database
Download sqlite here: http://www.sqlite.org/download.html
Opern your terminal, cd to the sqlite folder, type "sqlite3"
'''
from urllib2 import urlopen
from bs4 import BeautifulSoup
from urlparse import urljoin
from sets import Set
from sqlite3 import dbapi2 as sqlite


class crawler:
    def __init__(self, dbname):
        self.con = sqlite.connect(dbname)
    
    def __del__(self):
        self.con.close()
    
    def dbcommit(self):
        self.con.commit()
    
    def get_entry_id(self, table, field, value, create_new=True):
        return None
    
    def add_to_index(self, url, soup):
        print 'Indexing %s' %url
        
    # extract text from HTML
    def extract_text(self, soup):
        return None
   
   # separate words by non-whitesapce character
    def seperate_words(self, txt):
        return None
    
    def is_indexed(self, url):
        return False
    
    # add a link between 2 pages
    def add_link(self, url_from, url_to, link_txt):
        pass
    
    # start from a list of pages, do BFS (breath first search) to the given depth, then indexing pages
    def crawl(self, pages, depth=2):
        pass
    
    # create database tables
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
        
if __name__ == '__main__':
    main()
