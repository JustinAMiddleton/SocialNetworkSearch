import sys
import os
import time
import urllib
import twitter
from TwitterGeoPics import Geocoder
import TwitterSearch
import TwitterCrawler

search_term = sys.argv[1]

class TwitterCrawler(object):
	# Login to api
	def login(self):
		api = twitter.Api(consumer_key='684nljJUHfn6SCaYSCG0yAhbW',
						consumer_secret='mIRCyxLdIC5cQc7HukUtb7KhKqIvSYOB6LjBZb3CQOQ2n4ents',
						access_token_key='2805813624-2V4XKmbtM18s8osRDpSsr4H2An7JTpMdBE5N2la',
						access_token_secret='szChpRZhXg9F7n5gmlQhG2gEXe5C5g1vgYLGfqmeViPj8'
						)
		return api
	
	# Search
	def BasicSearch(self, query):
		search = TwitterSearch.BasicTwitterSearch()
		tweets = search.search(api, search_term)
		return tweets
	
	# SearchLastXDays
	# SearchDateRange
	# Output to DB
	
	# Output to file
	def output_tweets(self, tweets):
		output = open("tweets.txt", "wb")
		output.write("SEARCH QUERY: " + search_term + "\n")

		for tweet in tweets:
			output.write("\n\n[" + tweet.api_tweet_data.user.screen_name.encode('utf-8') + "] ")
			output.write("[" + tweet.api_tweet_data.created_at + "] ")
			output.write(tweet.api_tweet_data.text.encode('utf-8'))
			
		output.close()

# LOGIN
crawler = TwitterCrawler()
api = crawler.login()
geocoder = Geocoder.Geocoder()

# Search Twitter for search query
search = TwitterSearch.BasicTwitterSearch()
Tweets = search.search(api, search_term)

# Print tweets to file
crawler.output_tweets(Tweets)
	
print "\nTweets found: " + str(len(Tweets))