import twitter

class Tweet(object):
	
	def __init__(self, api_tweet_data, media, geocode):
		self.api_tweet_data = api_tweet_data
		self.media = media
		self.geocode = geocode