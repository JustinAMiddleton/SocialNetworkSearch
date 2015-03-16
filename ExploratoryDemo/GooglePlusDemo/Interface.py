from GooglePlusThread import GooglePlusThread
from SocialNetworkSearch.dbFacade import dbFacade
from SocialNetworkSearch.Scorer import Scorer
import time
import threading

'''
This class serves as an interface for controlling
social media crawling and analysis

@author: Luke Lindsey
@date: 15 March 2015
'''

# For testing purposes
my_words = ['pizza']
my_weights = [1, 3, 2, 2]
targetSentiment = [1, 1, 1, 1]
my_args = {}


class Interface:
	def __init__(self, words, weights, sentiments):
		self.db = dbFacade()
		self.db.connect()
		self.db.create_keyspace_and_schema()
		self.scorer = Scorer(zip(words, weights, sentiments))
	
	'''
	Starts search crawling threads with inputed query string.
	'''
	def search(self, query, args):
		self.googleThread = GooglePlusThread(self.db, self.scorer, query, args)
		self.googleThread.start()
		self.googleThread.join()

	'''
	Ends search crawling threads; 
	waits for them to terminate before continuing.
	'''
	def stop_search(self):
		print "Closing threads.."
		try:		
			self.googleThread.raiseExc(KeyboardInterrupt)
		except threading.ThreadError:
			pass

		while self.googleThread.isAlive():
			time.sleep(1)
		self.googleThread.join()

	'''
	Retrieves users, calculates user scores, 
	updates score in database, and prints top 10 results.
	'''	
	def score(self):
		print "Scoring..\n"
		users = self.db.get_users_dict()
		scores = self.db.calculate_user_scores(users)
		self.db.populate_user_scores(users, scores)

		users = self.db.get_scored_users()
		return users

	# '''
	# Takes wordlist and forms OR search query string.
	#  input 	: ["word1", "word2", "word3"]
	#  output	: "word1 OR word2 OR word3"
	# '''
	# def get_query(self, words):
	# 	return ' OR '.join(words)


if __name__ == "__main__":
	Interface(my_words, my_weights, targetSentiment).search('pizza', my_args)
