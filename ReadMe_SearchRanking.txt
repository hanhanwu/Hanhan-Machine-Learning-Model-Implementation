1. get_pages.py
  * Give a set of seedpages and crawl links inside.
  * For each newly crawled links, read each of them and crawl other new links.
  * BFS (breath first search), the search layer depends on the defined depth in the code.
  * As for direct sources which can be read for reseach directly, will be collected along the way.
  * Clean urls takes time and will vary based on the seed pages. I am using wiki pages so you will see some settings can be used for wiki engligh pages only.
  
2. stemming_test.py
  * In get_pages.py, I am simply seperating words from the page_text using python regular expression, but in fact I can convert words to their stems. So that the search time will be shorter, for example, we search "look" which will include "looking", "looked" too.
  
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
