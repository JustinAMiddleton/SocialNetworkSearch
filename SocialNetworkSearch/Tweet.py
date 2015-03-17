import twitter

'''
This class holds data representing one tweet received by
searching the Twitter API.

@author: Brenden Romanowski
@date: 24 Feb 2015
'''
class Tweet(object):

	def __init__(self, api_data, scorer):
		self.username = api_data['user']['screen_name'].encode('utf-8')
		self.content = api_data['text'].encode('utf-8').replace("'", "''")
		self.score = self.score_post(scorer)

	def score_post(self, scorer):
		try:
			return float(scorer.score(self.content))
		except UnicodeDecodeError:
			self.content = self.content.decode('utf-8')
			return float(scorer.score(self.content))
