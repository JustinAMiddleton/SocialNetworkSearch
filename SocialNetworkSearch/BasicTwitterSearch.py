from TwitterAPI import TwitterError
from TwitterSearch import TwitterSearch

'''
This class defines a basic Twitter api search. 
No special search parameters are used (i.e. date range).

@author: Brenden Romanowski
@date: 24 Feb 2015
'''

class BasicSearch(TwitterSearch):

	def search(self):
		results = self.get_first_100_results()
			
		if self.tweetCount < 100:
			return self.tweetCount

		try:
			self.get_next_100_results(results)		
		except KeyboardInterrupt:
			print('\n Twitter: Terminated by user (search)\n')
		except Exception as e:
			print('\n Twitter: Terminated due to error\n')
			print(e)

		return self.tweetCount
		
	def get_first_100_results(self):
		results = []
		try:
			results = super(BasicSearch, self).get_100_search_results()
			tweets = super(BasicSearch, self).create_Tweet_objects(results)
			super(BasicSearch, self).store_tweets_in_database(tweets)
		except KeyboardInterrupt:
			print ('\n Terminated by user (search)\n')
		except TwitterError.TwitterRequestError:
			try:
				super(BasicSearch, self).api_rate_limit_sleep()
			except KeyboardInterrupt:
				return results
			return self.get_first_100_results()

		except TwitterError.TwitterConnectionError:
			try:
				self.api.login()
			except KeyboardInterrupt:
				return results
			return self.get_first_100_results()
			
		return results
		
	def get_next_100_results(self, results):
		while (len(results) == 100):
			lowest_id = results[99]['id']
			
			try:
				results = super(BasicSearch, self).get_100_search_results((int)(lowest_id))
				tweets = super(BasicSearch, self).create_Tweet_objects(results)
				super(BasicSearch, self).store_tweets_in_database(tweets)
			except TwitterError.TwitterRequestError:
				super(BasicSearch, self).api_rate_limit_sleep()
				continue
			except TwitterError.TwitterConnectionError:
				self.api.login()
				continue
				
				
