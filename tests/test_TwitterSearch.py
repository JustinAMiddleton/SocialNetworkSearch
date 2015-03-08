import unittest
import twitter
from SocialNetworkSearch.TwitterDemo.TwitterSearch import TwitterSearch
from SocialNetworkSearch.TwitterDemo.TwitterCrawler import TwitterCrawler
from SocialNetworkSearch.TwitterDemo.Tweet import Tweet
from SocialNetworkSearch.dbFacade import dbFacade
from SocialNetworkSearch.Scorer import Scorer

class test_TwitterSearch(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		words = ['pizza', 'tacos', 'burgers', 'fries']
		weights = [1,3,2,2]
		targetSentiment = [1,1,1,1]    
		self.args = { 'location' : None }
		self.query = "pizza OR tacos OR burgers OR fries"
	
		self.db = dbFacade()
		self.db.connect()
		self.db.create_keyspace_and_schema()
		self.api = TwitterCrawler().login()
		self.scorer = Scorer(zip(words, weights, targetSentiment))
	
	def test_create_instance_with_valid_arguments(self):
		search = TwitterSearch(self.api, self.db, self.scorer, self.query, self.args)
		self.assertIsInstance(search, TwitterSearch)

	def test_create_instance_without_required_arguments(self):	
		try:
			search = TwitterSearch()
			self.fail()
		except TypeError:
			pass

	def test_create_instance_with_invalid_api_argument(self):
		try:
			search = TwitterSearch(None, self.db, self.scorer, self.query, self.args)
			self.fail()
		except TypeError:
			pass

	def test_create_instance_with_invalid_db_argument(self):
		try:
			search = TwitterSearch(self.api, None, self.scorer, self.query, self.args)
			self.fail()
		except TypeError:
			pass
			
	def test_create_instance_with_invalid_scorer_argument(self):
		try:
			search = TwitterSearch(self.api, self.db, None, self.query, self.args)
			self.fail()
		except TypeError:
			pass

	def test_create_instance_with_invalid_query_argument(self):
		try:
			search = TwitterSearch(self.api, self.db, self.scorer, None, self.args)
			self.fail()
		except TypeError:
			pass

	def test_create_instance_with_invalid_args_argument(self):
		try:
			search = TwitterSearch(self.api, self.db, self.scorer, self.query, None)
			self.fail()
		except TypeError:
			pass

	def test_create_instance_with_invalid_args_argument(self):
		try:
			search = TwitterSearch(self.api, self.db, self.scorer, self.query, None)
			self.fail()
		except TypeError:
			pass

	def test_create_instance_with_no_location_argument(self):
		invalid_args = {}
		try:
			search = TwitterSearch(self.api, self.db, self.scorer, self.query, invalid_args)
			self.fail()
		except KeyError:
			pass

	def test_get_100_search_results(self):
		search = TwitterSearch(self.api, self.db, self.scorer, self.query, self.args)
		results = search.get_100_search_results()
		self.assertEquals(len(results), 100)
		self.assertIsInstance(results[0], twitter.status.Status)
	
	def test_get_100_search_results_with_invalid_starting_id(self):
		search = TwitterSearch(self.api, self.db, self.scorer, self.query, self.args)
		try:
			search.get_100_search_results(starting_id="Invalid")
			self.fail()
		except TypeError:
			pass

	def test_create_Tweet_objects(self):
		search = TwitterSearch(self.api, self.db, self.scorer, self.query, self.args)
		results = search.get_100_search_results()
		tweets = search.create_Tweet_objects(results)
		self.assertIsInstance(tweets, list)
		self.assertIsInstance(tweets[0], Tweet)

	def test_create_Tweet_objects_with_no_argument(self):
		search = TwitterSearch(self.api, self.db, self.scorer, self.query, self.args)
		try:
			search.create_Tweet_objects()
			self.fail()
		except TypeError:
			pass

	def test_create_Tweet_objects_with_invalid_argument(self):
		search = TwitterSearch(self.api, self.db, self.scorer, self.query, self.args)
		try:
			search.create_Tweet_objects("Invalid")
			self.fail()
		except TypeError:
			pass

	def test_store_tweets_in_database_with_no_argument(self):
		search = TwitterSearch(self.api, self.db, self.scorer, self.query, self.args)
		try:
			search.store_tweets_in_database()
			self.fail()
		except TypeError:
			pass

	def test_store_tweets_in_database_with_invalid_argument(self):
		search = TwitterSearch(self.api, self.db, self.scorer, self.query, self.args)
		try:
			search.store_tweets_in_database("Invalid")
			self.fail()
		except TypeError:
			pass

if __name__ == '__main__':
    unittest.main()
