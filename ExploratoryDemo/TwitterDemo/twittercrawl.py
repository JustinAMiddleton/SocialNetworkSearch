import sys
import os
import time
import urllib
import twitter
from TwitterGeoPics import Geocoder
import TwitterSearch
import TwitterCrawler
from dbFacade import dbFacade

query = sys.argv[1]

# DATABASE PREPERATION
db = dbFacade()
db.connect()
db.create_keyspace_and_schema()

# LOGIN
crawler = TwitterCrawler.TwitterCrawler()
api = crawler.login()
geocoder = Geocoder.Geocoder()

# Search Twitter for search query
tweetCount = crawler.BasicSearch(query, db)

# Print tweets to file
#crawler.output_tweets(Tweets)
	
print "\nTweets found: " + str(tweetCount)