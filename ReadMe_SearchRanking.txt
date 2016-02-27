1. stemming_test.py
  * In get_pages.py, after getting page text and esperate them into words using python regular expression, the words will be converted to their stems at the same time. So that the search time will be shorter, for example, we search "look" which will include "looking", "looked" too.

2. get_pages.py
  * Give a set of seedpages and crawl links inside.
  * For each newly crawled links, read each of them and crawl other new links.
  * BFS (breath first search), the search layer depends on the defined depth in the code.
  * As for direct sources which can be read for reseach directly, will be collected along the way.
  * Clean urls takes time and will vary based on the seed pages. I am using wiki pages so you will see some settings can be used for wiki engligh pages only.
  
3. Build DB connection, using SQLite
* Using sqlite3 as database
  Download sqlite here: http://www.sqlite.org/download.html
  Opern your terminal, cd to the sqlite folder, type "sqlite3"
* Create 5 tables and build index for each table
a. urllist - stores crawled urls
b. wordlist - stores all the words
c. link - stores from_page id and to_page id
d. linkwords - stores wordid and the relative linkid
e. wordlocation - stores the location of the words in the relative url

4. crawler_and_searcher.py
* Build tables and indexs.
* Crawl pages using a set of seed pages, the search level depends on the defined depth. Directed sources will be collected along the way.
* Add crawled page url id and the id of each word on this page (not ignore words), as well as the word location on this page into table wordlocation. While checking the urlid, wordid from table urllist and worlist along the way, new items will be added into these 2 tables and return the created rowid. Finally do a simple test after the insertion.
* The result returned by crawl() only supports 1 word search. Therefore, I have created a method called multi_word_query() which will return all the rows, each row has the id of the url that contain the words appeared in the query which has multiple words, and the word ids for these query words.
Note: The code in multi_words_query() looks complex, but the query is like this: (use 2 words search as an example)
  select t0.urlid, t0.location, t1.location
  from wordlocation t0, wordlocation t1
  where t0.wordid = 2 and t1.wordid = 247
  and t0.urlid = t1.urlid
* Rank the returned urls in scores descending order

* In order to acieve the ranking, I am using some methods to calculate the scores
  a. All the scores have to be rescaled into the range of [0, 1] and all represent the same meaning, which means, the higher value means higher score while the lower value means the lowers score. Since when calculating scores, some lower value may represent higher score.
  b. Methods to calcuate different scores:
  Method 1 - Calculating the frequency of the words in the query appear on each same page.
  In this case, using wiki page as the seed page, word frequency may not be the best score calculation method. For example, when I am using query "new Recommendation System", it returns New York City as the top 1 result, the real Recommender System page just ranked No.4
  
  Method 2 - Checking words location, the earlier, score higher. Assuming most of the major topics or important content will appear near the top of the page.
