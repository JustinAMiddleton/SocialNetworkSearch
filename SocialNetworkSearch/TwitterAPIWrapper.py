from TwitterAPI import TwitterAPI, TwitterError

'''
Wrapper for TwitterAPI

@author: Brenden Romanowski
@date: 13 March 2015
'''

class TwitterAPIWrapper(object):
	def login(self):
		self.api = TwitterAPI(consumer_key='684nljJUHfn6SCaYSCG0yAhbW',
						consumer_secret='mIRCyxLdIC5cQc7HukUtb7KhKqIvSYOB6LjBZb3CQOQ2n4ents',
						access_token_key='2805813624-2V4XKmbtM18s8osRDpSsr4H2An7JTpMdBE5N2la',
						access_token_secret='szChpRZhXg9F7n5gmlQhG2gEXe5C5g1vgYLGfqmeViPj8')
		return self.api

	def search(self, params):
		results = self.api.request('search/tweets', params).json()		

		if 'errors' in results:
			raise  TwitterError.TwitterRequestError(results['errors'][0]['code'])

		return results['statuses']
	
	def get_rate_limit_status(self):
		rate_limit_status = self.api.request('application/rate_limit_status')
		
		reset_time = rate_limit_status.json()['resources']['search']['/search/tweets']['reset']
		return reset_time
