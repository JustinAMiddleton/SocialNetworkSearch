import threading
import ctypes
import inspect
from CrawlThread import CrawlThread

'''
This class inherets the CrawlThread interface and
defines and controls Twitter crawler search threads. 

@author: Brenden Romanowski
@date: 24 Feb 2015
'''

class TwitterThread(CrawlThread):

	def __init__(self, crawler, db, scorer, query):
		threading.Thread.__init__(self)
		self.crawler = crawler
		self.db = db
		self.scorer = scorer
		self.query = query

	def run(self):
		try:
			print "Starting Twitter Thread"
			tweetCount = self.crawler.BasicSearch(self.query, self.db, self.scorer)
		except KeyboardInterrupt:
			print "Thread ended by main"

    	

