from TwitterThread import TwitterThread
from dbFacade import dbFacade
from Scorer import Scorer
from SearchPacket import SearchPacket
from TwitterGeoPics.Geocoder import Geocoder
import time
import thread
import threading

'''
This class serves as an interface for controlling
social media crawling and analysis

@author: Brenden Romanowski
@date: 24 Feb 2015
'''

# For testing purposes
words = ['pizza']
weights = [1,3,2,2]
targetSentiment = [1,1,1,1]    
args = { 'location' : None }

class Interface:
	def __init__(self, search_packet):
		self.db = dbFacade()
		self.db.connect()
		self.db.create_keyspace_and_schema()
		self.scorer = Scorer(search_packet)
	
	'''
	Starts search crawling threads with inputed query string.
	'''
	def search(self, query, args):
		self.twitterThread = TwitterThread(self.db, self.scorer, query, args)
		self.twitterThread.start()
		self.twitterThread.join()

	'''
	Ends search crawling threads; 
	waits for them to terminate before continuing.
	'''
	def stop_search(self):
		print "Closing threads.."
		try:		
			self.twitterThread.raiseExc(KeyboardInterrupt)
		except threading.ThreadError:
			pass

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

	'''
	Takes wordlist and forms OR search query string.
	 input 	: ["word1", "word2", "word3"]
	 output	: "word1 OR word2 OR word3"
	'''
	def get_query(self, words):
		return ' OR '.join(words)


if __name__ == "__main__":
	Interface().main()
