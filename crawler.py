'''
Created on Feb 13, 2016
@author: hanhanwu
'''

class crawler:
    def __init__(self, dbname):
        pass
    
    def __del__(self):
        pass
    
    def __dbcommit__(self):
        pass
    
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
        pass
    
