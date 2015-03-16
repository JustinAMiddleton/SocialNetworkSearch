import threading
import ctypes
import inspect
from TwitterGeoPics.Geocoder import Geocoder
from CrawlThread import CrawlThread
from TwitterAPIWrapper import TwitterAPIWrapper
from BasicTwitterSearch import BasicSearch
from dbFacade import dbFacade
from Scorer import Scorer

'''
This class inherets the CrawlThread interface and
defines and controls Twitter crawler search threads. 

@author: Brenden Romanowski
@date: 24 Feb 2015
'''

class TwitterThread(CrawlThread):

	def __init__(self, db, scorer, query, args=None):
		if not isinstance(db, dbFacade):
			raise TypeError('dbFacade instance required')
		elif not isinstance(scorer, Scorer):
			raise TypeError('Scorer instance required')
		elif not isinstance(query, str):
			raise TypeError('Query must be a string')
		elif not isinstance(args, dict):
			raise TypeError('Args must be a dictionary')
		elif not 'location' in args.keys():
			raise KeyError('Location not defined in args')

		threading.Thread.__init__(self)
		self.api = TwitterAPIWrapper()
		self.api.login()
		self.db = db
		self.scorer = scorer
		self.query = query
		self.args = args

		self.query = query + " -filter:retweets"

		if self.args['location']:
			self.set_location_argument()
	def run(self):
		self.search()

	def search(self):
		search = BasicSearch(self.api, self.db, self.scorer, self.query, self.args)
		return search.search()
		

	def set_location_argument(self):
		geocoder = Geocoder()
		lat, lng, radius = geocoder.get_region_circle(self.args['location'])
		region = (lat, lng, str(radius)+"km")
		self.args['location'] = region


    	

