from TwitterDemo.TwitterCrawler import TwitterCrawler
from TwitterThread import TwitterThread
from dbFacade import dbFacade
from Scorer import Scorer
import time
import cassandra

'''
This class serves as an interface for controlling
social media crawling and analysis

@author: Brenden Romanowski
@date: 24 Feb 2015
'''

# For testing purposes
words = ['tacos', 'pizza', 'burgers', 'fries']
weights = [1,3,2,2]
targetSentiment = [1,1,1,1]    

class Interface:
	'''def __init__(self):
		self.db = dbFacade()
		self.db.connect()
		self.db.create_keyspace_and_schema()
		self.twitterCrawler = TwitterCrawler()
		self.twitterCrawler.login()
		self.scorer = Scorer(zip(words, weights, targetSentiment))'''
		

	def __init__(self, words, weights, sentiments):
		self.db = dbFacade()
		self.db.connect()
		self.db.create_keyspace_and_schema()
		self.twitterCrawler = TwitterCrawler()
		self.twitterCrawler.login()
		self.scorer = Scorer(zip(words,weights,sentiments))
	
	'''
	Starts search crawling threads with inputed query string.
	'''
	def search(self, query):
		self.twitterThread = TwitterThread(self.twitterCrawler, self.db, self.scorer, query)
		self.twitterThread.start()

		# End Twitter search thread with Ctrl+C; temporary
		while(True):
			try:
				time.sleep(1)
			except KeyboardInterrupt:
				self.stop_search()
				break

	'''
	Ends search crawling threads; 
	waits for them to terminate before continuing.
	'''
	def stop_search(self):
		print "Closing threads.."
		self.twitterThread.raiseExc(KeyboardInterrupt)

		while self.twitterThread.isAlive():
			time.sleep(1)
		self.twitterThread.join()

	'''
	Retrieves users, calculates user scores, 
	updates score in database, and prints top 10 results.
	'''	
	def score(self):
		print "Scoring..\n"
		users = self.db.get_users_dict()
		scores = self.db.calculate_user_scores(users)
		
		self.db.populate_user_scores(users, scores)

		# Retrieve and print top 10 scores
		users = self.db.get_scored_users()
		for i in range(0,len(users)):
			print "[%s] %s" % (str(round(users[i]['score'],1)), users[i]['username'])

	'''
	Takes wordlist and forms OR search query string.
	 input 	: ["word1", "word2", "word3"]
	 output	: "word1 OR word2 OR word3"
	'''
	def get_query(self, wordlist):
		query = ""
		for word in wordlist:
			query += " OR " + word
		query = query[4:]
		return query
		
	'''
	Main method for testing
	'''
	def main(self):
		query =	self.get_query(words)

		self.search(query)
		self.score()

		self.db.close()
		time.sleep(1)

if __name__ == "__main__":
	Interface().main()
