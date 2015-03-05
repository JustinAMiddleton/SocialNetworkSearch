import time
import twitter
from Tweet import Tweet

'''
This class defines Twitter api searching functionality.
It should be used in place of interacting with the api 
directly.

@author: Brenden Romanowski
@date: 24 Feb 2015
'''

class TwitterSearch(object):	

	def __init__(self, api, db, scorer, query, args):
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
		rate_limit_status = self.api.GetRateLimitStatus()
		reset_time = rate_limit_status['resources']['search']['/search/tweets']['reset']
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
		params = { 'term' : self.query,
					'count' : 100,
					'lang' : 'en',
					'result_type' : 'recent',
					'geocode' : self.args['location']
					}
					
		if starting_id:
			params['max_id'] = starting_id
			
		results = self.api.GetSearch(**params)
		return results
	
	'''
	Takes in a list of Tweet objects and inserts them
	as entries in the database
	'''
	def store_tweets_in_database(self, tweets):
		for tweet in tweets:
			username = tweet.api_tweet_data.user.screen_name.encode('utf-8')
			post_text = tweet.api_tweet_data.text.encode('utf-8').replace("'", "''")
			try:
				score = float(self.scorer.score(post_text))
			except UnicodeDecodeError:
				post_text = post_text.decode('utf-8')
				score = float(self.scorer.score(post_text))
			
			self.db.add_post(username, 'Twitter', post_text, self.query, score)
			self.db.add_user(username, 0, 'Twitter')
			self.tweetCount += 1

		print str(self.tweetCount) + " tweets gathered.."
	
	'''
	Takes in a list of search results in the Twitter API response
	format and converts them to Tweet objects
	'''
	def create_Tweet_objects(self, search_results):
		tweets = []
		for search_result in search_results:
			tweet = self.create_Tweet_object(search_result)
			tweets.append(tweet)
		return tweets

	def create_Tweet_object(self, search_result):
		media_urls = None
		geocode = None
			
		tweet = Tweet(search_result, media_urls, geocode)
		return tweet
