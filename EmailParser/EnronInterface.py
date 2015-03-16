from dbFacade import dbFacade
from Scorer import Scorer
import EnronSearch
import time


class EnronInterface:

	def __init__(self, words, weights, sentiments):
		self.db = dbFacade()
		self.words = words
		self.db.connect()
		self.db.create_keyspace_and_schema()
		self.scorer = Scorer(zip(words, weights, sentiments))


	def score(self):
		print "Scoring..\n"
		users = self.db.get_users_dict()
		scores = self.db.calculate_user_scores(users)

		self.db.populate_user_scores(users, scores)

		# Retrieve and print top 10 scores
		users = self.db.get_scored_users()
		for i in range(0,len(users)):
			print "[%s] %s" % (str(round(users[i]['score'], 1)), users[i]['username'])

	@staticmethod
	def print_statistics(enron_search):
		total_time = enron_search.end_time - enron_search.start_time
		total_seconds = total_time.seconds
		hours = total_seconds // 3600
		total_seconds = total_seconds % 3600
		minutes = total_seconds // 60
		seconds = total_seconds % 60

		print "Searching Enron took: " + str(hours) + " hours, " + str(minutes) + \
		      " minutes, and " + str(seconds) + " seconds."

		print "Searched " + str(enron_search.total_users) + " users."
		print "Searched " + str(enron_search.total_emails) + " emails."
		print str(enron_search.total_sentences_matched) + " sentences were matches."

	def main(self):
		enron_search = EnronSearch.EnronSearch(self.words, self.db, self.scorer)
		enron_search.search_enron()

		EnronInterface.print_statistics(enron_search)

		self.score()

		self.db.close()
		time.sleep(1)


# For testing purposes
words_test = ['tacos', 'pizza', 'burgers', 'gas']
weights_test = [1, 3, 2, 2]
sentiment_test = [1, 1, 1, 1]

if __name__ == "__main__":
	EnronInterface(words_test, weights_test, sentiment_test).main()
