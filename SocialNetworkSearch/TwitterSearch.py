import time
from TwitterAPIWrapper import TwitterAPIWrapper
from Tweet import Tweet
from dbFacade import dbFacade
from Scorer import Scorer

'''
This class defines Twitter api searching functionality.
It should be used in place of interacting with the api 
directly.

@author: Brenden Romanowski
@date: 24 Feb 2015
'''

class TwitterSearch(object):	

	def __init__(self, api=None, db=None, scorer=None, query=None, args=None):
		if not isinstance(api, TwitterAPIWrapper):
			raise TypeError('TwitterAPIWrapper instance required')
		elif not isinstance(db, dbFacade):
			raise TypeError('dbFacade instance required')
		elif not isinstance(scorer, Scorer):
			raise TypeError('Scorer instance required')
		elif not isinstance(query, str):
			raise TypeError('Query must be a string')
		elif not isinstance(args, dict):
			raise TypeError('Args must be a dictionary')
		elif not 'location' in args.keys():
			raise KeyError('Location not defined in args')

		self.tweetCount = 0
		self.api = api
		self.db = db
		self.scorer = scorer
		self.query = query
		self.args = args
		
	'''
	Halt operations until api limit has been reset
	'''
	def api_rate_limit_sleep(self):
		reset_time = self.api.get_rate_limit_status()
		sleep_time = (int)(reset_time - time.time())
		print ('\n Twitter rate limit exceeded. Sleeping for {0} seconds..'.format(str(sleep_time)))
		
		try:
			time.sleep(sleep_time)
		except KeyboardInterrupt:
			raise KeyboardInterrupt
	
	'''
	Gets 100 Tweet search results with an optional 
	starting ID. The optional starting ID is to 
	enable paginated result retrieval.
	'''
	def get_100_search_results(self, starting_id=None):
		params = { 'q' : self.query,
					'count' : 100,
					'lang' : 'en',
					'result_type' : 'recent'
					}

		if self.args['location'] is not None:
			params['geocode'] = ','.join(map(str, self.args['location']))
		if self.args['since'] is not None:
			params['since'] = self.args['since']
		if self.args['until'] is not None:
			params['until'] = self.args['until']
					
		if starting_id:
			params['max_id'] = starting_id

		results = self.api.search(params)
		return results
	
	'''
	Takes in a list of Tweet objects and inserts them
	as entries in the database
	'''
	def store_tweets_in_database(self, tweets=None):
		if tweets is None:
			raise TypeError('Tweets argument required')
		elif not isinstance(tweets, list):
			raise TypeError('Tweets argument must be a list of Tweets')

		for tweet in tweets:			
			self.db.add_post(tweet.username, 'Twitter', tweet.content, self.query, tweet.score)
			self.db.add_user(tweet.username, 0, 'Twitter')
			self.tweetCount += 1

		print str(self.tweetCount) + " tweets gathered.."
	
	'''
	Takes in a list of search results in the Twitter API response
	format and converts them to Tweet objects
	'''
	def create_Tweet_objects(self, search_results=None):
		if search_results is None:
			raise TypeError('Search results argument required')
		elif not isinstance(search_results, list):
			raise TypeError('Search results argument must be a list of Tweets')

		tweets = []
		for search_result in search_results:
			tweet = Tweet(search_result, self.scorer)
			tweets.append(tweet)
		return tweets
