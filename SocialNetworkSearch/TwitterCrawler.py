from BasicTwitterSearch import BasicSearch
from TwitterAPIWrapper import TwitterAPIWrapper

'''
This class handles all operations involving
the Twitter API. 

@author: Brenden Romanowski
@date: 24 Feb 2015
'''

class TwitterCrawler(object):

	def login(self):		
		self.api = TwitterAPIWrapper()
		self.api.login()
		return self.api
	
	def BasicSearch(self, db, scorer, query, args):
		search = BasicSearch(self.api, db, scorer, query, args)
		return search.search()
