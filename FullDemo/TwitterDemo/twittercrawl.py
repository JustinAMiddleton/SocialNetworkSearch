import sys
import os
import time
import urllib
import twitter
#from TwitterGeoPics import Geocoder
import TwitterSearch
import TwitterCrawler

query = sys.argv[1]

# LOGIN
crawler = TwitterCrawler.TwitterCrawler()
api = crawler.login()
#geocoder = Geocoder.Geocoder()

# Search Twitter for search query
Tweets = crawler.BasicSearch(query)

# Print tweets to file
crawler.output_tweets(Tweets)
	
print "\nTweets found: " + str(len(Tweets))