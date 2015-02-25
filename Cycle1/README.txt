Searches Twitter for posts that contain one or more words in a wordlist, scores the posts, stores the posts in the Cassandra database, and outputs the top ten scoring users.

USE:
	python Interface.py
	
	(Wordlist is hardcoded in this file)

FILES:

Interface.py	 		=> Main controlling class; starts and stops operation
dbFacade.py	 		=> Facade class for database queries
Scorer.py	 		=> Class for scoring textual posts
CrawlThread.py	 		=> Interface/Base class for social media crawling threads
TwitterThread.py 		=> Twitter crawling thread implementation class

TwitterDemo			=> Folder containing Twitter crawling files
TwitterDemo/Tweet.py		=> Class representing one Tweet post object
TwitterDemo/TwitterCrawler.py	=> Class for controlling twitter crawling
TwitterDemo/TwitterSearch.py	=> Contains Classes defining types of Twitter crawl searches
					(Currently only one type of search)


			
