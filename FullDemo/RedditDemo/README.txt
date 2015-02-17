This is a super-proto prototype for what a Reddit crawler may eventually do.

How to use:
	In command line, type:

		python Interface.py

	Next, it will prompt you for a phrase you want to search.
	Wait for processing to finish. In current form, should not take more than a minute.

Current progression:
	Receive search query as input
	Use reddit search API to search for that phrase
		-Should receive ~1000 thread results, based on reddit cache size
		-Must pause 2 seconds before each new page, as per Reddit limitations
		-Currently no extra stipulations around time of post or subreddit
	Examine each individual thread (which includes title and main post)
	Count the number of times the searched phrase appears, and assign this as its score
	Add this score to the scoreboard, which keeps track of every name seen so far
		-Database stand-in, for prototype purposes
	Sort the names in order of score, and print them out

Included files:
	Crawler:		Superclass for RedditCrawler. No special use right now.
	Interface:		Driver file.
	PrimitiveScore:		Scorer. Scores calculated on occurrence of exact string.
	RedditCrawler:		Only file that calls the API, and searches for word.
	RedditObject:		Used to store all important information from a reddit post.
					-author
					-title
					-text
					-time (utc)
					-score (will be set after creation)
	RedditScoreboard:	Hashmap with all users and their scores.

Special libraries:
	praw: Python wrapper for Reddit API.
	Tkinter: GUI library. Included but not yet implemented.

TODO:
	As this is a prototype, many of the parameters (e.g. time, more than one word) have not yet
	been implemented. Waiting for finalization of requirements. 
	Getting comments of each thread found would also be easy.