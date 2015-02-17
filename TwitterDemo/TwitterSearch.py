import time
import twitter
from Tweet import Tweet

#DOWNLOAD_PHOTOS_ENABLED = True
MEDIA_URLS_ENABLED = False
GEOCODES_ENABLED = False

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
		
	def store_tweets_in_database(self, tweets, db, query):
		#print "Storing tweets in db.."
		for tweet in tweets:
			username = tweet.api_tweet_data.user.screen_name.encode('utf-8')
			post_text = tweet.api_tweet_data.text.encode('utf-8').replace("'", "''")
			db.add_post(username, 'Twitter', post_text, query)
			self.tweetCount += 1

		print str(self.tweetCount) + " tweets gathered.."
		
	def create_Tweet_objects(self, search_results):
		#print "Creating tweet objects.."
	
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

	def search(self, api, query, db):
		# Get 100 (max) most recent results
		results = self.get_first_100_results(api, query, db)
			
		if self.tweetCount < 100:
			return self.tweetCount

		# Get next 100 results ignoring ones already found, and so on...
		try:
			self.get_next_100_results(api, query, results, db)			
		except KeyboardInterrupt:
			print('\n Terminated by user (search)\n')
		except MemoryError:
			print('\n Terminated due to memory error\n')
		except Exception as e:
			print('\n Terminated due to error\n')
			print str(e)

		return self.tweetCount
		
	def get_first_100_results(self, api, query, db):
		results = []
		try:
			results = super(BasicTwitterSearch, self).get_100_search_results(api, query)
			tweets = super(BasicTwitterSearch, self).create_Tweet_objects(results)
			super(BasicTwitterSearch, self).store_tweets_in_database(tweets, db, query)
		except KeyboardInterrupt:
			print ('\n Terminated by user (search)\n')
		except twitter.TwitterError as e:
			
			try:
				super(BasicTwitterSearch, self).api_rate_limit_sleep(api)
			except KeyboardInterrupt:
				return results
			
			return self.get_first_100_results(api, query, db)
		return results
		
	def get_next_100_results(self, api, query, results, db):
		while (len(results) == 100):
			lowest_id = results[99].GetId()
			
			try:
				results = super(BasicTwitterSearch, self).get_100_search_results(api, query, lowest_id)
				tweets = super(BasicTwitterSearch, self).create_Tweet_objects(results)
				super(BasicTwitterSearch, self).store_tweets_in_database(tweets, db, query)
			except twitter.TwitterError as e:
				super(BasicTwitterSearch, self).api_rate_limit_sleep(api)
				continue
		

'''
class SearchLastXDays(object):
	# search
	#...
	
class SearchDateRange(object):
	# search, ...
'''

'''	
=====
Date restricted searches
=====
'''

'''	
def search_date_range(api, query, start_date, end_date):
	# search for tweets in date range
	
def search_streaming(api, query):
	# start streaming for new tweet results
'''

'''
def search_last_x_days(api, query, num_days):
	# search for tweets in the last x number of days
	tweets = []
	date = num_days * 3600 * 24
	
	results = get_first_100_results(api, query, tweets)
	remove_Tweets_older_than_date(tweets, date)
	
	if len(tweets) < 100:
		return tweets
		
	try:
		get_next_100_results(api, query, results, tweets)
		#remove_Tweets_older_than_date(tweets, date)
		
	
	return tweets

def remove_Tweets_older_than_date(tweets, date):			
	for i in range(0 to len(tweets)):
		if date < tweets[i].api_tweet_data.created_at:
			tweets[i:len(tweets)] = []
			break	
'''