from GoogleAPIWrapper import GoogleAPIWrapper as API
from GooglePost import GooglePost
import cassandra.protocol
import sys


"""
This class defines google+ api searching functionality.
It should be used in place of interacting with the api
directly.

@author: Luke Lindsey
@date: 14 March 2015
"""


class GooglePlusSearch(object):

	def __init__(self, api_key, db, scorer, query, params={}):
		self.api_key = api_key
		self.db = db
		self.scorer = scorer
		self.query = query
		self.params = params
		self.postCount = 0

	def get_20_search_results(self, next_page_token=None):

		# dictionary for containing the GET query parameters.
		payload = {}
		# setting the query parameter
		payload["query"] = self.query
		# setting the google plus api key
		payload["key"] = self.api_key
		# setting the parameter for the number of returned results to 20
		payload["maxResults"] = 20
		# setting the order of the returned results to recent.
		payload["orderBy"] = "recent"
		# setting the language parameter to English, so that the returned activity feeds are only in english
		payload["language"] = "en"

		if next_page_token is not None:
			payload["pageToken"] = next_page_token

		for param in self.params:
			payload[param] = self.params[param]

		results = API.default_search(payload)
		return results

	def store_posts_in_database(self, plus_posts=None):

		if plus_posts is None:
			raise TypeError('Posts argument required')
		elif not isinstance(plus_posts, list):
			raise TypeError('Posts argument must be a list of Google Posts')

		for plus_post in plus_posts:
			author = plus_post.author.encode('utf-8')
			try:
				post = plus_post.post.encode('utf-8').replace("'", "''")
			except UnicodeDecodeError:
				post = plus_post.post.decode('utf-8').replace("'", "''")
				post = post.encode('utf-8')
			try:
				score = float(self.scorer.score(post))
			except UnicodeDecodeError:
				post = post.decode('utf-8')
				score = float(self.scorer.score(post))

			try:
				self.db.add_post(author, 'Google+', post, self.query, score)
				self.db.add_user(author, 0, 'Google+')
			except cassandra.protocol.SyntaxException as e:
				# print "failing at line 74 in GooglePlusSearch"
				# exc_type, exc_obj, exc_tb = sys.exc_info()
				# print 'type: ' + str(exc_type)
				# print(e)
				# sys.exit(0)
				post = post + "'''"
			self.postCount += 1

		print str(self.postCount) + " posts gathered.."

	def create_google_objects(self, search_results=None):
		if search_results is None:
			raise TypeError('Search results argument required')
		elif not isinstance(search_results, list):
			raise TypeError('Search results argument must be a list of Google+ posts')

		google_posts = []
		for search_result in search_results:
			post = self.create_google_object(search_result)
			google_posts.append(post)
		return google_posts

	@staticmethod
	def create_google_object(search_result):

		post = GooglePost(search_result)
		return post
