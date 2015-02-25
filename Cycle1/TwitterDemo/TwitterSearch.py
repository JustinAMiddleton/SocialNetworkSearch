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

MEDIA_URLS_ENABLED = False
GEOCODES_ENABLED = False
#DOWNLOAD_PHOTOS_ENABLED = True

class TwitterSearch(object):	

	def __init__(self):
		self.tweetCount = 0
		
	def api_rate_limit_sleep(self, api):
		rate_limit_status = api.GetRateLimitStatus()
		reset_time = rate_limit_status['resources']['search']['/search/tweets']['reset']
		sleep_time = (int)(reset_time - time.time())
		print ('\n Twitter rate limit exceeded. Sleeping for {0} seconds..'.format(str(sleep_time)))
		
		try:
			time.sleep(sleep_time)
		except KeyboardInterrupt:
			raise KeyboardInterrupt
		
	def lookup_media_urls(self, status):
		tweet_media = []
		for media in status.media:
			tweet_media.append(media['media_url_https'])
		
		if not tweet_media:
			return None
				
	def lookup_geocode(self, status, geo):
		"""Get geocode either from tweet's 'coordinates' field (unlikely) or from tweet's location and Google."""
		if not geo.quota_exceeded:
			try:
				geocode = geo.geocode_tweet(status)
				if geocode[0]:
					#print('geoCODE: %s %s,%s' % geocode)
					return geocode
			except Exception as e:
				if geo.quota_exceeded:
					print('geoCODER QUOTA EXCEEDED: %s' % geo.count_request)
		return None
		
	def get_100_search_results(self, api, query, starting_id=None):
		#print "Fetching next batch of tweets.."
		params = { 'term' : query,
					'count' : 100,
					'lang' : 'en',
					'result_type' : 'recent',
					'include_entities' : True
					}
					
		if starting_id:
			params['max_id'] = starting_id
			
		results = api.GetSearch(**params)
		return results
		
	def store_tweets_in_database(self, tweets, db, query, scorer):
		for tweet in tweets:
			username = tweet.api_tweet_data.user.screen_name.encode('utf-8')
			post_text = tweet.api_tweet_data.text.encode('utf-8').replace("'", "''")
			try:
				score = int(scorer.score(post_text))
			except UnicodeDecodeError:
				post_text = post_text.decode('utf-8')
				score = int(scorer.score(post_text))
			
			db.add_post(username, 'Twitter', post_text, query, score)
			db.add_user(username, 0, 'Twitter')
			self.tweetCount += 1

		print str(self.tweetCount) + " tweets gathered.."
		
	def create_Tweet_objects(self, search_results):
		tweets = []
		for search_result in search_results:
			tweet = self.create_Tweet_object(search_result)
			tweets.append(tweet)
		return tweets
		
	def create_Tweet_object(self, search_result):
		media_urls = None
		geocode = None
		
		if MEDIA_URLS_ENABLED:
			media_urls = self.lookup_media_urls(search_result)
		if GEOCODES_ENABLED:
			geocode = self.lookup_geocode(search_result, geocoder)
			
		tweet = Tweet(search_result, media_urls, geocode)
		return tweet

class BasicTwitterSearch(TwitterSearch):

	def search(self, api, query, db, scorer):
		# Get 100 (max) most recent results
		results = self.get_first_100_results(api, query, db, scorer)
			
		if self.tweetCount < 100:
			return self.tweetCount

		# Get next 100 results ignoring ones already found, and so on...
		try:
			self.get_next_100_results(api, query, results, db, scorer)			
		except KeyboardInterrupt:
			print('\n Twitter: Terminated by user (search)\n')
		except MemoryError:
			print('\n Twitter: Terminated due to memory error\n')
		except Exception as e:
			print('\n Twitter: Terminated due to error\n')
			print str(e)

		return self.tweetCount
		
	def get_first_100_results(self, api, query, db, scorer):
		results = []
		try:
			results = super(BasicTwitterSearch, self).get_100_search_results(api, query)
			tweets = super(BasicTwitterSearch, self).create_Tweet_objects(results)
			super(BasicTwitterSearch, self).store_tweets_in_database(tweets, db, query, scorer)
		except KeyboardInterrupt:
			print ('\n Terminated by user (search)\n')
		except twitter.TwitterError as e:
			
			try:
				super(BasicTwitterSearch, self).api_rate_limit_sleep(api)
			except KeyboardInterrupt:
				return results
			
			return self.get_first_100_results(api, query, db)
		return results
		
	def get_next_100_results(self, api, query, results, db, scorer):
		while (len(results) == 100):
			lowest_id = results[99].GetId()
			
			try:
				results = super(BasicTwitterSearch, self).get_100_search_results(api, query, lowest_id)
				tweets = super(BasicTwitterSearch, self).create_Tweet_objects(results)
				super(BasicTwitterSearch, self).store_tweets_in_database(tweets, db, query, scorer)
			except twitter.TwitterError as e:
				super(BasicTwitterSearch, self).api_rate_limit_sleep(api)
				continue
