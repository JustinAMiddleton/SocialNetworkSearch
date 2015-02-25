How to use:

	In command line, type:
		
		python twittercrawl.py "Search query here"

Current features:
	-Search twitter API for specified query and returns result
		-Can receive a max of 18,000 tweets per 15 minute period
		-Auto sleeps when rate limit reached
	-Terminates via CTRL+C
	-Obtains URLs to media associated with tweets
	-Obtains geolocation information via Google Maps api
	-Outputs tweets to file "tweets.txt"

Included files:
	twittercrawl.py			Driver script
	TwitterCrawler.py		Used for logging into API and starting searches
	TwitterSearch.py		Holds Search classes that define different types of searches
	Tweet.py			Object representing one Tweet search result
	

Special libraries:
	python-twitter
	TwitterGeoPics