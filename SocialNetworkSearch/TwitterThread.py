import threading
import ctypes
import inspect
from CrawlThread import CrawlThread
from TwitterGeoPics.Geocoder import Geocoder
from dbFacade import dbFacade
from Scorer import Scorer

'''
This class inherets the CrawlThread interface and
defines and controls Twitter crawler search threads. 

@author: Brenden Romanowski
@date: 24 Feb 2015
'''

class TwitterThread(CrawlThread):

	def __init__(self, crawler, db, scorer, query, args=None):
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
		self.crawler = crawler
		self.db = db
		self.scorer = scorer
		self.query = query
		self.args = args

		if self.args['location']:
			self.set_location_argument()
	def run(self):
		self.crawler.BasicSearch(self.db, self.scorer, self.query, self.args)

	def set_location_argument(self):
		geocoder = Geocoder()
		lat, lng, radius = geocoder.get_region_circle(self.args['location'])
		region = (lat, lng, str(radius)+"km")
		self.args['location'] = region


    	

