import unittest
import twitter
from SocialNetworkSearch.TwitterCrawler import TwitterCrawler

class test_TwitterCrawler(unittest.TestCase):

	def setUp(self):
		self.crawler = TwitterCrawler()
	
	def test_api_login(self):
		try:
			api = self.crawler.login()
		except twitter.error.TwitterError:
			self.fail("Invalid Twitter API credentials")
			

if __name__ == '__main__':
    unittest.main()
