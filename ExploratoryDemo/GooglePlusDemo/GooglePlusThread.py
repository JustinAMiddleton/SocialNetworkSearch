import threading
from SocialNetworkSearch.CrawlThread import CrawlThread
from GoogleAPIWrapper import GoogleAPIWrapper as googleAPI
from BasicGooglePlusSearch import BasicSearch

"""
This class inherets the CrawlThread interface and
defines and controls Google+ crawler search threads.

@author: Luke Lindsey
@date: 15 March 2015
"""


class GooglePlusThread(CrawlThread):

	def __init__(self, db, scorer, query, params=None):
		# if not isinstance(db, dbFacade):
		# 	raise TypeError('dbFacade instance required')
		# elif not isinstance(scorer, Scorer):
		# 	raise TypeError('Scorer instance required')
		# elif not isinstance(query, str):
		# 	raise TypeError('Query must be a string')
		# elif not isinstance(args, dict):
		# 	raise TypeError('Args must be a dictionary')
		# elif not 'location' in args.keys():
		# 	raise KeyError('Location not defined in args')

		threading.Thread.__init__(self)
		self.api_key = googleAPI.get_api_key()
		self.db = db
		self.scorer = scorer
		self.query = query
		self.params = params

		# if self.args['location']:
		# 	self.set_location_argument()

	def run(self):
		self.search()

	def search(self):
		search = BasicSearch(self.api_key, self.db, self.scorer, self.query, self.params)
		return search.search()


	# def set_location_argument(self):
	# 	geocoder = Geocoder()
	# 	lat, lng, radius = geocoder.get_region_circle(self.args['location'])
	# 	region = (lat, lng, str(radius)+"km")
	# 	self.args['location'] = region
