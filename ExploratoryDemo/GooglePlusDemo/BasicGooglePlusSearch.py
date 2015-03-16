from GooglePlusSearch import GooglePlusSearch
import sys
import cassandra.cluster
import cassandra.query
import cassandra.protocol

"""
This class defines a basic Google+ api search.
No special search parameters are used (i.e. date range).

@author: Luke Lindsey
@date: 14 March 2015
"""


class BasicSearch(GooglePlusSearch):

	def search(self):
		next_page_token = self.get_first_20_results()

		if self.postCount < 20:
			return self.postCount

		try:
			# may change parameter
			self.get_next_20_results(next_page_token)
		except KeyboardInterrupt:
			print('\n Google+: Terminated by user (search)\n')
		except Exception as e:
			print('\n Google+: Terminated due to error\n')
			print(e)

		return self.postCount

	def get_first_20_results(self):
		next_page_token = ''
		try:
			results_total = super(BasicSearch, self).get_20_search_results()
			results = results_total["items"]
			posts = super(BasicSearch, self).create_google_objects(results)
			super(BasicSearch, self).store_posts_in_database(posts)
			next_page_token = results_total["nextPageToken"]
		except KeyboardInterrupt:
			print ('\n Terminated by user (search)\n')
		# except TwitterError.TwitterRequestError:
		# 	try:
		# 		super(BasicSearch, self).api_rate_limit_sleep()
		# 	except KeyboardInterrupt:
		# 		return results_total
		# 	return self.get_first_20_results()
		#
		# except TwitterError.TwitterConnectionError:
		# 	try:
		# 		self.api.login()
		# 	except KeyboardInterrupt:
		# 		return results_total
		# 	return self.get_first_20_results()

		return next_page_token

	def get_next_20_results(self, page_token):
		while page_token != '':

			try:
				results_total = super(BasicSearch, self).get_20_search_results(page_token)
				results = results_total["items"]
				posts = super(BasicSearch, self).create_google_objects(results)
				super(BasicSearch, self).store_posts_in_database(posts)
			# except TwitterError.TwitterRequestError:
			# 	super(BasicSearch, self).api_rate_limit_sleep()
			# 	continue
			# except TwitterError.TwitterConnectionError:
			# 	self.api.login()
			# 	continue
			except Exception as e:
				print "failing at line 73 in BasicGooglePlusSearch"
				exc_type, exc_obj, exc_tb = sys.exc_info()
				print 'type: ' + str(exc_type)
				print(e)
				sys.exit(0)
			try:
				page_token = results_total["nextPageToken"]
			except KeyError:
				page_token = ''