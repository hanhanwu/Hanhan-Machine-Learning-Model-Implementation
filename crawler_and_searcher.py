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
import neural_network as nn


class PageConnection:
    def __init__(self, page_from, page_to):
        self.page_from = page_from
        self.page_to = page_to
  
        
        
class PageRecord:
    def __init__(self, page_url, page_text):
        self.page_url = page_url
        self.page_text = page_text



class crawler_and_searcher:
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
        self.con.commit()
            
            
    # insert the link connections into link table
    def insert_connections(self, page_connections):
        for pc in page_connections:
            page_from = pc.page_from
            page_to = pc.page_to
            fromid = self.get_row_id('urllist', 'url', page_from)
            toid = self.get_row_id('urllist', 'url', page_to)
            self.con.execute('insert into link (fromid, toid) values (%d, %d)' % (fromid, toid))
            self.con.commit()
            
    
    def insert_linkwords(self):
        self.con.execute("""
        insert into linkwords (wordid, linkid)
        select wl.wordid, link.rowid from
        link join wordlocation wl
        on link.toid = wl.urlid
        """)
        self.con.commit()
        
        
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
    
    
    # search for the words appear in the query, and return all the urls that contain these words on the same page
    def multi_words_query(self, qry):
        field_list = 't0.urlid'
        table_list = ''
        where_clause_list = ''
        
        query_words = qry.split()
        query_words = [q.lower() for q in query_words]
        table_num = 0
        wordids = []
        
        for qw in query_words:
            wr = self.con.execute("select rowid from wordlist where word='%s'" % qw).fetchone()
            if wr != None:
                wid = wr[0]
                wordids.append(wid)
                
                if table_num > 0:
                    table_list += ', '
                    where_clause_list += ' and t%d.urlid=t%d.urlid and ' % (table_num-1, table_num)
                field_list += ', t%d.location' % table_num
                table_list += 'wordlocation t%d' % table_num
                where_clause_list += 't%d.wordid=%d' % (table_num, wid)
                table_num += 1
                
        sql_qry = 'select %s from %s where %s' % (field_list, table_list, where_clause_list)
        print sql_qry
        cur = self.con.execute(sql_qry)
        rows = [r for r in cur]
        return rows, wordids
    
    
    def get_full_url(self, urlid):
        return self.con.execute('select url from urllist where rowid=%d' % urlid).fetchone()[0]
    
    
    # re-scale scores to the range of [0,1] and show represent how close to the better score (1), 
    # since some small values maybe better while some higher values maybe better
    def rescale_scores(self, scores, small_is_better=0):
        v = 0.00001  # avoid to be divided by 0
        if small_is_better:
            min_score = float(min(scores.values()))
            new_scores = dict([(u, min_score/max(v,s)) for (u, s) in scores.items()])
        else:
            max_score = max(scores.values())
            if max_score == 0: max_score = v
            new_scores = dict([(u, float(s)/max_score) for (u, s) in scores.items()])
        return new_scores
    
    
    # count how often the words in the query appear on each same page
    def word_frequency_score(self, rows):
        word_freq_dct = dict([(row[0], 0) for row in rows])
        for row in rows:
            word_freq_dct[row[0]] += 1
        return self.rescale_scores(word_freq_dct)
    
    
    # major topics always appear near the top of the pages, so score higher if the query words appear earlier in a page
    def words_location_scores(self, rows):
        words_location_dct = dict([(row[0], 1000000) for row in rows])
        for row in rows:
            loc_score = sum(row[1:])
            if loc_score < words_location_dct[row[0]]:
                words_location_dct[row[0]] = loc_score
        return self.rescale_scores(words_location_dct, small_is_better=1)
        
    
    # if the query words are closer to each other in a page, score the page higher, here I am tolerating the words order
    def words_distance_scores(self, rows):
        # each row has the same length, of the row has just no more than 1 word, return the score as 1.0
        if len(rows[0]) <= 2: return dict([(row[0], 1.0) for row in rows])
        
        words_dist_dct = dict([(row[0], 1000000) for row in rows])
        for row in rows:
            dist_score = sum(abs(row[i] - row[i-1]) for i in range(2,len(row)))
            if dist_score < words_dist_dct[row[0]]:
                words_dist_dct[row[0]] = dist_score
        return self.rescale_scores(words_dist_dct, small_is_better=1)
    
    
    # when there is more inbound links, the higher score for the page
    def inbound_links_scores(self, rows):
        # the urls in all the rows are unique since I have used sets in the crawler
        inbound_links_dct = dict([(row[0], 
                self.con.execute('select count(*) from link where toid=%d' % row[0]).fetchone()[0]) for row in rows])
        return self.rescale_scores(inbound_links_dct)
    
    
    # PageRank            
    def page_rank(self, itr=10):
        # create a new table and initialize the score for each url as 1.0
        self.con.execute('drop table if exists pagerank')
        self.con.execute('create table pagerank(urlid primary key, score)')
        self.con.execute('insert into pagerank select rowid, 1.0 from urllist')
        self.con.commit()
            
        for i in range(itr):
            print 'iteration ', str(i)
            for (urlid,) in self.con.execute('select rowid from urllist'):
                pr = 0.15
                for (fromid,) in self.con.execute('select fromid from link where toid=%d' % urlid):
                    inbound_links_count = self.con.execute('select count(*) from link where toid=%d' % fromid).fetchone()[0]
                    if inbound_links_count == 0: inbound_links_count = 99999
                    page_score = self.con.execute('select score from pagerank where urlid=%d' % fromid).fetchone()[0]
                    pr += 0.85*page_score/inbound_links_count
                self.con.execute('update pagerank set score=%f where urlid=%d' % (pr, urlid))
                
        cur = self.con.execute('select * from pagerank order by score desc')
        for i in range(5):
            urlid, score = cur.next()
            print self.get_full_url(urlid), score
            
            
    def pagerank_scores(self, rows):
        self.page_rank()
        pagerank_dct = dict([(row[0], 
                    self.con.execute('select score from pagerank where urlid=%d' % row[0]).fetchone()[0]) for row in rows])
        return self.rescale_scores(pagerank_dct)
    
    
    # find pages that contain the query words and get PageRank scores from its from_page, calculate the score
    def link_text_scores(self, rows, wordids):
        self.insert_linkwords()
        link_text_dct = dict([(row[0], 0) for row in rows])
        
        for wid in wordids:
            cur = self.con.execute("""
            select link.fromid, link.toid from link, linkwords 
            where linkwords.wordid=%d
            and link.rowid=linkwords.linkid
            """ % wid)
            self.con.commit()
            
            for (fromid, toid) in cur:
                if toid in link_text_dct.keys():
                    pr = self.con.execute("""
                    select score from pagerank 
                    where urlid=%d
                    """ % fromid).fetchone()[0]
                    link_text_dct[toid] += pr
        return self.rescale_scores(link_text_dct)
                        
    
    # get total score for each returned url
    def get_url_scores(self, rows, wordids):
        url_totalscore_dct = dict([(row[0], 0) for row in rows])
        
        weights = [(1.0, self.word_frequency_score(rows)), (2.0, self.words_location_scores(rows)), 
                   (3.0, self.words_distance_scores(rows)), (2.5, self.inbound_links_scores(rows)),
                   (4.0, self.pagerank_scores(rows)), (4.0, self.link_text_scores(rows, wordids))]
        
        for (weight, scores) in weights:
            for url in url_totalscore_dct.keys():
                url_totalscore_dct[url] += weight*scores[url]
                
        return url_totalscore_dct
    
    
    def get_ranked_urls(self, qry):
        rows, wordids = self.multi_words_query(qry)
        url_scores = self.get_url_scores(rows, wordids)
        
        ranked_urls = sorted([(score, url) for (url, score) in url_scores.items()], reverse=1)
        for (score, url) in ranked_urls[0:10]:
            print '%f\t%s' % (score, self.get_full_url(url))
        return [r[1] for r in ranked_urls[0:10]]
            
    
    # create database tables and indexes
    def create_index_tables(self):
        self.con.execute('drop table if exists urllist')
        self.con.execute('drop table if exists wordlist')
        self.con.execute('drop table if exists wordlocation')
        self.con.execute('drop table if exists link')
        self.con.execute('drop table if exists linkwords')
        
        self.con.execute('create table urllist(url)')
        self.con.execute('create table wordlist(word)')
        self.con.execute('create table wordlocation(urlid, wordid, location)')
        self.con.execute('create table link(fromid integer, toid integer)')
        self.con.execute('create table linkwords(wordid, linkid)')
         
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
    mycrawler_searcher = crawler_and_searcher(dbname)
    mycrawler_searcher.create_index_tables()
    
    # crawl the pages using a set of seed pages
    seed_pages = ['https://en.wikipedia.org/wiki/Recommender_system']
    direct_sources, page_connections, page_records = mycrawler_searcher.crawl(seed_pages)
    print '***********direct sources***********'
    for ds in direct_sources:
        print ds
    print '***********page connections***********'
    for pc in page_connections:
        print pc.page_from,', ', pc.page_to
    mycrawler_searcher.insert_connections(page_connections) 
    
    print '***********page records***********'
    for pr in page_records:
        print pr.page_url,', ', str(len(pr.page_text))
         
    # add page url and the page text into wordlocation table, the urllist, wordlist tables will be inserted along the way
    for pr in page_records:
        mycrawler_searcher.add_to_index(pr.page_url, pr.page_text, ignorewords)
    insertion_results = [r for r in mycrawler_searcher.con.execute('select rowid from wordlocation where wordid=1')]
    print insertion_results
     
    # multiple words query
    qry = 'Recommendation System'
    rows, wordids = mycrawler_searcher.multi_words_query(qry)
    print rows
    print wordids
     
    # show ranked urls
    ranked_urls = mycrawler_searcher.get_ranked_urls(qry)
    
    nn_dbname = 'neural_network.db'
    my_nn = nn.onehidden_nn(dbname)
    my_nn.create_tables()
    
    print '********create hidden nodes********'
    rows = [r[0] for r in rows]
    my_nn.create_hidden_node(wordids, rows)
    print 'input_hidden:'
    for cont in my_nn.con.execute('select * from input_hidden'):
        print cont
    print 'hidden_output:'
    for cont in my_nn.con.execute('select * from hidden_output'):
        print cont
        
    print '********setup NN********'
    my_nn.setup_nn(wordids, rows)
    
    for selected_url in ranked_urls:
        my_nn.train_nn(wordids, rows, selected_url)
        print '\n'
    
if __name__ == '__main__':
    main()
